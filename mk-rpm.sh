#!/bin/bash

pwd=$(pwd)

if [ $# -ne 1]
then
  echo "provide version"
  exit 1
else
  
  name=openstack-clean-all
  version=$1
  
  package=$name-$version
  
  
  mkdir $package
  cp ${name}.py $package
  tar -cvf $package.tar $package
  /bin/mv -vf  $package.tar $HOME/rpmbuild/SOURCES/
  rm -rvf $pwd/$package
  rpmbuild -ba ${name}.spec
fi
