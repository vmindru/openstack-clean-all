#!/usr/bin/sh

VERSION=$1 

if [ $# -eq 1 ]
then
  echo "upadting spec file"
  sed -i "s/Version:.*/Version: $VERSION/g" openstack-clean-all.spec 
  echo "updating openstack-clean-all.py"
  sed -i "s/parser = OptionParser(version.*/parser = OptionParser(version=\"%prog $VERSION\", usage=usage)/g" openstack-clean-all.py 
else
  echo "Provide verison number"
fi
