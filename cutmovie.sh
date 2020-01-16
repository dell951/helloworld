#!/bin/bash
#set -x
# filename
# start
# end
dur=$(date -ud@$(($(date -ud"1970-01-01 $3" +%s)-$(date -ud"1970-01-01 $2" +%s))) +%T)
ffmpeg -ss $2 -i $1 -to $dur -c copy output.mp4
mv output.mp4 $1
#set +x
