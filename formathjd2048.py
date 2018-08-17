#!/usr/bin/python

import os
import sys
import subprocess
import logging
import re
import shutil

logging.getLogger().setLevel(logging.INFO)
work_path = str(sys.argv[1])

p = re.compile(r'hjd2048.com-\d\d\d\d(?P<s_name>[a-zA-Z]*)-?(?P<num_id>\d*)-h264.(?P<ext>[mp4aviwmkpg]*)')

k = 0

for parent, dirnames, filenames in os.walk(work_path):
    for filename in filenames:
        if (filename.endswith('rmvb') or filename.endswith('mp4') or filename.endswith('m4v') or filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('wmv')) and not filename.startswith("."):
            m = p.search(filename)
            if m:
                k += 1 
                full_path = os.path.join(parent, filename)
                new_name = m.group("s_name") + "-" + m.group("num_id") + "." + m.group("ext")
                dest_path = os.path.join(parent, new_name)
                shutil.move(full_path, dest_path)
                logging.info("%s --> %s" % (full_path, dest_path))

logging.info("%d files proceeded." % k)
