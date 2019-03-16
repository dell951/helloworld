#!/bin/bash

scrapy crawl search -a studio=$1 -a queryKey="$2" -a titledate="$3"