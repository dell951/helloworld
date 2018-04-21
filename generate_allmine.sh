#!/bin/bash

rm -rf /volume1/nas-share/helloworld/allmine.txt
find /volumeUSB1/usbshare1-2/porn/ /volume3/iReady2/ /volume2/formated/ -type f \( -iname \*.mp4 -o -iname \*.avi -o -iname \*.mkv -o -iname \*.rmvb \) |sort -u >> /volume1/nas-share/helloworld/allmine.txt
