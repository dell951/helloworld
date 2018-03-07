#!/bin/bash

export PATH=$PATH:/var/packages/Java8/target/j2sdk-image/bin
export JAVA_HOME=/var/packages/Java8/target/j2sdk-image

cd /volume1/mystaff
python /volume1/mystaff/scrapy_wrapper.py /volume1/Downloaded
