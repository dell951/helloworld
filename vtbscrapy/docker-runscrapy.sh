#!/bin/bash

mkdir -p alldone

sudo docker run --rm -v $(pwd):/runtime/app myscrapydocker scrapy crawl vtb -a studio=$1 -a title=$2
mv -n alldone/* /volumeUSB1/usbshare1-2/porn/pretty/

rm -rf alldone
