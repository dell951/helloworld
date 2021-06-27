#!/usr/bin/python
# coding:utf-8

import os
import sys
import logging
import shutil

logging.getLogger().setLevel(logging.INFO)

search_path = str(sys.argv[1])

for parent, dirnames, filenames in os.walk(search_path):
    for filename in filenames:
        if (filename.lower().endswith('rmvb') or filename.lower().endswith('mp4') or filename.lower().endswith('m4v') or filename.lower().endswith('mkv') or filename.lower().endswith('avi') or filename.lower().endswith('wmv')) and not filename.startswith("."):
            full_path = os.path.join(parent, filename)
            name, ext = os.path.splitext(full_path)
            cmd = "/volume5/Downloaded/ffmpeg-git-20210501-amd64-static/ffmpeg -i " + full_path + " -r 1 -f image2 " + "/volume5/Downloaded/hczimu_snapshots/" + filename.split(".")[0] + "-snpashot.jpg"
            print(cmd)
            os.system(cmd + " >/dev/null 2>&1")
