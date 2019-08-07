#!/bin/bash

now="$(date +'%Y%m%d')"
echo $now

backup_nfo.py /volume1/3TB/czimu/ $now/czimu
backup_nfo.py /volume1/3TB/iReady2/ $now/iReady
backup_nfo.py /volume3/czimu/ $now/czimu
backup_nfo.py /volume3/iReady2/ $now/iReady
backup_nfo.py /volume4/8TB/czimu/ $now/czimu/
backup_nfo.py /volume4/8TB/iReady2/ $now/iReady
backup_nfo.py /volume2/14TB/allinone/iReady2/ $now/iReady
backup_nfo.py /volume2/14TB/allinone/czimu/ $now/czimu
backup_nfo.py /volume2/14TB/allinone/hczimu/ $now/czimu
backup_nfo.py /volume2/14TB/allinone/S-Cute/ $now/scute
backup_nfo.py /volume2/14TB/allinone/seriesformated/ $now/series
backup_nfo.py /volumeUSB1/usbshare1-2/porn/plexready/ $now/iReady
backup_nfo.py /volumeUSB1/usbshare1-2/porn/seriesformated $now/series
backup_nfo.py /volumeUSB1/usbshare1-2/porn/S-Cute/ $now/scute
backup_nfo.py /volumeUSB1/usbshare1-2/porn/pretty/ $now/pretty
backup_nfo.py /volume2/14TB/pretty/ $now/pretty

tar cvzf fullnfo_bk.tgz $now/
echo "backup done."
rm -rf $now
