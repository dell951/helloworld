#!/bin/bash

export PATH=$PATH:/var/packages/Java8/target/j2sdk-image/bin
export JAVA_HOME=/var/packages/Java8/target/j2sdk-image

cd /volume1/nas-share/helloworld
cp settings.xml.bk settings.xml
if [ ! -n "$2" ] ;then
    python /volume1/nas-share/helloworld/scrapy_wrapper.py $1 javlibrary
else
    python /volume1/nas-share/helloworld/scrapy_wrapper.py $1 $2
fi    
#/volume2/formated
