#!/usr/bin/python

import os
import time
import sys


from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
from optparse import OptionParser


def opt_parse():
        parser = OptionParser(version="%prog 1.2")
        parser.add_option("-q",
                          "--quite",
                          dest="quite",
                          default=False,
                          help="do not ask for confirmation during removal")
        parser.add_option("-a",
                          "--all",
                          dest="all",
                          default=True,
                          help="remoev all resources")
        parser.add_option("-n",
                          "--element",
                          dest="network",
                          default=False,
                          help="remove specified resource, available options"
                          "are\nuno")
        (options, args) = parser.parse_args()
        my_options = {
            "options":  {
                "quite":  options.quite,
                "all":    options.all,
            }
        }
        return my_options


def init_openstack_connection():
    API_VERSION = 2
    AUTH_URL = os.environ['OS_AUTH_URL']
    USERNAME = os.environ['OS_USERNAME']
    PASSWORD = os.environ['OS_PASSWORD']
    PROJECT_NAME = os.environ['OS_PROJECT_NAME']
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=AUTH_URL,
                                    username=USERNAME,
                                    password=PASSWORD,
                                    project_name=PROJECT_NAME)
    sess = session.Session(auth=auth)

    if USERNAME == "admin" or PROJECT_NAME == "admin":
        sys.exit("do not run this command as ADMIN!!!!!")

    return novaclient.Client(API_VERSION, session=sess),
    neutronclient.Client(session=sess)


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [Y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def delete_servers(nova):
    """Delete all nova instances
       "nova" is an instance of novaclient.Client() from novaclient
        returns true if succesfull
    """

    servers = nova.servers.list()
    yes_no_msg = "starting instance delete, will delete {}"\
        " servers".format(len(servers))
    if query_yes_no(yes_no_msg):
        while servers != []:
            servers = nova.servers.list()
            for server in servers:
                nova.servers.delete(server._info['id'])
            print "waiting, pending delete {} servers".format(len(servers))
            time.sleep(2)
        return True
    else:
        return False


def delete_floating_ips(neutron):
    """Delete all floating IP's
       "nova" is an instance of novaclient.Client() from novaclient
        returns true if succesful
    """

    floating_ips = neutron.list_floatingips()['floatingips']
    yes_no_msg = "starting floating IP delete, will delete {} ips"\
        .format(len(floating_ips))
    if query_yes_no(yes_no_msg):
        while floating_ips != []:
            floating_ips = neutron.list_floatingips()['floatingips']
            for flip in floating_ips:
                flipid = flip['id']
                neutron.delete_floatingip(flipid)
            print "waiting, pending delete {} floatings"\
                .format(len(floating_ips))
            time.sleep(2)
            floating_ips = neutron.list_floatingips()['floatingips']
        return True
    else:
        return False


def delete_router(neutron):
    """ delete all routers
        "neutron" is an instance of neutronclient.Client(session=sess)
        returns false if succesful
    """

    routers = neutron.list_routers()['routers']
    yes_no_msg = "starting router delete, will delete {} routers"\
        .format(len(routers))
    if query_yes_no(yes_no_msg):
        while routers != []:
            routers = neutron.list_routers()['routers']
            for router in routers:
                rt = router['id']
                # first remove gateways
                try:
                    neutron.remove_gateway_router(rt)
                    ports = neutron.list_ports()['ports']
                    for port in ports:
                        if port['device_owner'] == "network:router_interface":
                            portid = {"port_id": port['id']}
                            neutron.remove_interface_router(rt, body=portid)
                    # after gateway is removed , remove routers
                    neutron.delete_router(rt)
                except ValueError:
                    print "coudl not remote router {}".format(rt)
                print "removing routers, {} router left".format(len(routers))
                time.sleep(2)
        return True
    else:
        return False


def delete_networks(neutron):
    """ delete neutron networks
        "neutron" is an instance of neutronclient.Client(session=sess)
        returns false if succesful
    """

    """ openstck returns all networks including shared one when asked
        for a list, we need to diferentiate public from private before
        delete. createa  new array of networks and remove those.
    """
    def __net_list():
        nets = []
        for network in neutron.list_networks()['networks']:
            if network['router:external'] is False:
                nets.append(network)
        return nets

    nets = __net_list()
    yes_no_msg = "starting net delete, will delete {} networks"\
        .format(len(nets))
    if query_yes_no(yes_no_msg):
        while len(nets) > 0:
            print "waiting, pending delete {} nets".format(len(nets))
            for net in nets:
                neutron.delete_network(net['id'])
            time.sleep(2)
            nets = __net_list()
        return True
    else:
        return False


def delete_security_groups(neutron):
    """ delete security groups
        "neutron" is an instance of neutronclient.Client(session=sess)
        returns false if succesful
    """

    security_groups = neutron.list_security_groups()['security_groups']
    yes_no_msg = "starting security group delete, will delete {} security groups"\
        .format(len(security_groups)-1)
    if query_yes_no(yes_no_msg):
        # there is always a default security group, we don't want to delet that
        # one
        while len(security_groups) != 1:
            for sc in security_groups:
                # there is always a default security group, we don't want to
                # delet that one
                if sc['name'] != "default":
                    neutron.delete_security_group(sc['id'])

            print "waiting, pending delete {} security_groups"\
                .format(len(security_groups)-1)
            time.sleep(2)
            security_groups = neutron.list_security_groups()['security_groups']

        return True

    else:
        return False


def delete_keypair(nova):
    """ delete keypair
       "nova" is an instance of novaclient.Client() from novaclient
        returns true if succesfull
    """

    keypairs = nova.keypairs.list()
    yes_no_msg = "starting keypairs delete, will delete {} keypairs"\
        .format(len(keypairs))
    if query_yes_no(yes_no_msg):
        while len(keypairs) != 0:
            for keypair in keypairs:
                keypair_name = keypair._info['keypair']['name']
                nova.keypairs.delete(keypair_name)
            print "waiting, pending delete {} keypairs".format(len(keypairs))
            time.sleep(2)
            keypairs = nova.keypairs.list()
        return True
    else:
        return False

"""
nova, neutron = init_openstack_connection()
delete_servers(nova)
delete_floating_ips(neutron)
delete_router(neutron)
delete_networks(neutron)
delete_security_groups(neutron)
delete_keypair(nova)
"""

opt_parse()
