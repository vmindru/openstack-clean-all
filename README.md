# openstack-cleanall

this tool will automatically remove opnestack resources
of your tenant.
openstack resources will be removed in following order.
this tool will prevent you running this as user admin or under project amdin.

    - instances 
    - floating_ip
    - routers 
    - networks
    - security groups
    - keypairs


## setup  

following ENV variables must be set in your shell, this are similar to standard
nova client auth mechanism.

```
OS_AUTH_URL
OS_USERNAME
OS_PASSWORD
OS_PROJECT_NAME
```

e.g.

```
export 
OS_AUTH_URL=http://openstack.com/v2.0/ # URL to access Open Stack nova API
OS_USERNAME=user # your Open Stack user
OS_PASSWORD=somesecretpassword # your Open Stack password
OS_PROJECT_NAME=someopenstackproject # your Open Stack project|tenant name
```
## help message

```
Usage: openstack-clean-all [options]

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -y, --yes   do not ask for confirmation during removal.
              WARNING: this will remove all your resources without
              confirmation, use with care!!!
```

## demo 
[./osremove.gif]
