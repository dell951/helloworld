#!/bin/bash

rm -rf /volume1/nas-share/helloworld/allmine.txt
#find /volume2/14TB/allinone/ /volume3/czimu/ /volume4/8TB/czimu/ /volume4/8TB/iReady2/ /volume1/3TB/czimu/ /volume1/3TB/iReady2/ /volume3/iReady2/ /volume5/formated/ /volume2/14TB/HDsMovie/ /volumeUSB1/usbshare1-2/porn/ -type f \( -iname \*.mp4 -o -iname \*.avi -o -iname \*.mkv -o -iname \*.rmvb -o -iname \*.wmv \) |sort -u >> /volume1/nas-share/helloworld/allmine.txt

find /volume4/8TB/hczimu/ /volume1/3TB/hczimu/ /volume2/14TB/allinone/ /volume3/czimu/ /volume4/8TB/czimu/ /volume1/3TB/czimu/ /volume4/8TB/iReady2/ /volume1/3TB/iReady2/ /volume3/iReady2/ /volume5/formated/ /volumeUSB1/usbshare1-2/porn/ -type f \( -iname \*.mp4 -o -iname \*.avi -o -iname \*.mkv -o -iname \*.rmvb -o -iname \*.wmv \) |sort -u >> /volume1/nas-share/helloworld/allmine.txt

find /volume2/14TB/HDsMovie/ /volumeUSB1/usbshare1-2/HDsMovie -type f \( -iname \*.mp4 -o -iname \*.avi -o -iname \*.mkv -o -iname \*.rmvb -o -iname \*.wmv \) |sort -u >> /volume1/nas-share/helloworld/allmine.txt

echo "all done." >> /volume1/nas-share/helloworld/allmine.txt
