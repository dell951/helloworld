#!/bin/bash

VAR1="$1"
VAR2="$2"

echo "------------------------------------------"
MOREF=`grep -i "$VAR1"-"$VAR2" allmine.txt`
if [ "$?" = "1" ]
then
	echo "file $VAR1-$VAR2 not found"
	exit 1
fi

echo "$MOREF"

SIZE=`du -sh "$MOREF"`
echo "$SIZE"

RESOLUTION=`ffmpeg -i $MOREF  2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}' | cut -d'x' -f2`
echo "$RESOLUTION"

NFOFILE=${MOREF/mp4/nfo}
NFOFILE=${NFOFILE/wmv/nfo}
NFOFILE=${NFOFILE/avi/nfo}
NFOFILE=${NFOFILE/mkv/nfo}
grep '<title' $NFOFILE
grep 'name' $NFOFILE
echo "------------------------------------------"
