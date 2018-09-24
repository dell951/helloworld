#!/bin/bash

mkdir -p alldone

scrapy crawl vtb -a studio=$1 -a title=$2

sshpass -f /Users/atext scp -rp alldone/. admin@192.168.1.150:/volumeUSB1/usbshare1-2/porn/pretty

rm -rf alldone
