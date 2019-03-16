#!/bin/bash

mkdir -p alldone

sudo docker run --rm -v $(pwd):/runtime/app myscrapydocker:1.2 scrapy crawl scute -a fid="$1"
mv alldone/* /volumeUSB1/usbshare1-2/porn/mgstmp/

#scrapy crawl mgs -a fid="$1"
#sshpass -f /Users/atext scp -rp alldone/. admin@192.168.1.150:/volumeUSB1/usbshare1-2/porn/mgs

rm -rf alldone
