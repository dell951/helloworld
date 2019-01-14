#!/bin/bash

export PATH=$PATH:/var/packages/Java8/target/j2sdk-image/bin
export JAVA_HOME=/var/packages/Java8/target/j2sdk-image

cd /volume1/nas-share/helloworld
git checkout -- settings.xml
if [ ! -n "$2" ] ;then
    python /volume1/nas-share/helloworld/scrapy_wrapper.py $1 javbus
else
    python /volume1/nas-share/helloworld/scrapy_wrapper.py $1 $2
fi    
#/volume2/formated
