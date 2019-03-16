#!/bin/bash

python nfoupdate.py $1 $2
sed -i ""  '/^[[:space:]]*$/d' $1
