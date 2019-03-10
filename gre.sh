#!/bin/bash

VAR1="$1"
VAR2="$2"

echo "------------------------------------------"
MOREF=`grep -i "$VAR1"-"$VAR2" allmine.txt`
echo "$MOREF"

SIZE=`du -sh "$MOREF"`
echo "$SIZE"
echo "------------------------------------------"
