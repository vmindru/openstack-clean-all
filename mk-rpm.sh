#!/bin/bash

pwd=$(pwd)

if [ $# -ne 1 ]
then
  name=openstack-clean-all
  version=$( grep Version ${name}.spec | cut -d\: -f2)
  
  package=${name//[[:blank:]]/}-${version//[[:blank:]]/}
  echo "Building $package"
  
  
  mkdir $package
  cp ${name}.py $package
  tar -cvf $package.tar $package
  /bin/mv -vf  $package.tar $HOME/rpmbuild/SOURCES/
  rm -rvf $pwd/$package
  rpmbuild -ba ${name}.spec
else 
  name=openstack-clean-all
  version=$1
  ./change_version.sh $version 
  package=${name//[[:blank:]]/}-${version//[[:blank:]]/}
  echo "Building $package"
  
  
  mkdir $package
  cp ${name}.py $package
  tar -cvf $package.tar $package
  /bin/mv -vf  $package.tar $HOME/rpmbuild/SOURCES/
  rm -rvf $pwd/$package
  rpmbuild -ba ${name}.spec
fi 
