#!/bin/bash

export PATH=$PATH:/var/packages/Java8/target/j2sdk-image/bin
export JAVA_HOME=/var/packages/Java8/target/j2sdk-image

cd /volume1/nas-share/helloworld
python /volume1/nas-share/helloworld/scrapy_wrapper.py $1
#/volume2/formated
