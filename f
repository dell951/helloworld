#!/bin/bash

target_folder=/volume5/formated/

docker run --rm -it -v $target_folder:/app/data -e FAILED_MOVE=1 -e LOCATION_RULE="number" -e MAX_TITLE_LEN=300 -e NAMING_RULE="title" vergilgao/avdc:latest
