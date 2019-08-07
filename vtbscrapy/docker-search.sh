#!/bin/bash


CRAWLER="search"

if [ $1 == "letsdoeit" ]
then
   CRAWLER="searchletsdoeit"
fi

#echo $CRAWLER

sudo docker run --rm -v $(pwd):/runtime/app myscrapydocker:1.2 scrapy crawl $CRAWLER -a studio=$1 -a queryKey="$2" -a filedate="$3" -a showFullresult=$4
