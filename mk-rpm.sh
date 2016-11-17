#!/bin/bash

pwd=$(pwd)

name=$1
version=$2

package=$name-$version


mkdir $package
cp ${name}.py $package
tar -cvf $package.tar $package
/bin/mv -vf  $package.tar $HOME/rpmbuild/SOURCES/
rm -rvf $pwd/$package
rpmbuild -ba ${name}.spec
