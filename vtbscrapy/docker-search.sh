#!/bin/bash


sudo docker run --rm -v $(pwd):/runtime/app myscrapydocker:1.2 scrapy crawl search -a studio=$1 -a queryKey="$2" -a filedate="$3" -a showFullresult=$4
