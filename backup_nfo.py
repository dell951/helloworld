#!/usr/bin/python
# coding:utf-8

import os.path
import sys
import logging
import shutil

logging.getLogger().setLevel(logging.INFO)

back_path = str(sys.argv[1])
target_path = str(sys.argv[2]) #target dir, not full path. must exist.

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info("folder %s created" % directory)
    except OSError:
        logging.info('Error: Creating directory. ' +  directory)

createFolder(target_path)

count = 0
for parent, dirnames, filenames in os.walk(back_path):
    for filename in filenames:
        if (filename.lower().endswith('rmvb') or filename.lower().endswith('mp4') or filename.lower().endswith('m4v') or filename.lower().endswith('mkv') or filename.lower().endswith('avi') or filename.lower().endswith('wmv')) and not filename.startswith("."):
            full_path = os.path.join(parent, filename)
            name, ext = os.path.splitext(full_path)
            fanart_file = os.path.join(parent, name + '-fanart.jpg')
            poster_file = os.path.join(parent, name + '-poster.jpg')
            nfo_file = os.path.join(parent, name + '.nfo')
            if os.path.exists(fanart_file) and os.path.exists(poster_file) and os.path.exists(nfo_file):
                logging.info('%s - %s -%s' % (nfo_file, poster_file, fanart_file))
                shutil.copy(nfo_file, target_path)
                shutil.copy(poster_file, target_path)
                shutil.copy(fanart_file, target_path)
                count += 1
            else:
                logging.info("%s is not ready." % filename)
        else:
            pass
            #logging.info("skip file " + filename)

logging.info('Proceed total %d' %count)
