#!/usr/bin/python
# coding:utf-8

import os.path
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
            fanart_file = os.path.join(parent, name + '-fanart.jpg')
            poster_file = os.path.join(parent, name + '-poster.jpg')
            nfo_file = os.path.join(parent, name + '.nfo')
            if os.path.exists(fanart_file) and os.path.exists(poster_file) and os.path.exists(nfo_file):
                pass
                #logging.info('Succeed.')
            else:
                logging.info("%s is not ready." % filename)
        else:
            pass
            #logging.info("skip file " + filename)
