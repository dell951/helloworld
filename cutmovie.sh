#!/bin/bash

# filename
# start
# end
ffmpeg -ss $2 -i $1 -to $3 -c copy output.mp4
mv output.mp4 $1
