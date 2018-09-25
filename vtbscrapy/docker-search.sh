#!/bin/bash

sudo docker run --rm -v $(pwd):/runtime/app myscrapydocker scrapy crawl search -a studio=$1 -a queryKey="$2"
