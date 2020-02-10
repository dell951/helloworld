#!/bin/bash

RED='\033[0;37m'
NC='\033[0m'

VAR1="$1"
VAR2="$2"

echo -e "${RED}------------------------------------------${NC}"
MOREF=`grep -i "$VAR1"-"$VAR2" allmine.txt`
if [ "$?" = "1" ]
then
	echo "file $VAR1-$VAR2 not found"
	exit 1
fi

grep -i "$VAR1"-"$VAR2" allmine.txt > temp_terms.txt

temp_input="/volume1/nas-share/helloworld/temp_terms.txt"

while IFS= read -r MOREF
do
  SIZE=`du -sh "$MOREF"`
  echo -e "${RED}$SIZE${NC}"

  RESOLUTION=`ffmpeg -i $MOREF  2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}' | cut -d'x' -f2`
  echo -e "${RED}$RESOLUTION${NC}"

  if [[ "$MOREF" == *"czimu"* ]]; then
    echo -e "${RED}**${NC}"
  fi

  NFOFILE=${MOREF/mp4/nfo}
  NFOFILE=${NFOFILE/wmv/nfo}
  NFOFILE=${NFOFILE/avi/nfo}
  NFOFILE=${NFOFILE/mkv/nfo}
  grep '<title' $NFOFILE
  grep 'name' $NFOFILE
  echo -e "${RED}------${NC}"
done < "$temp_input"
echo -e "${RED}------------------------------------------${NC}"
