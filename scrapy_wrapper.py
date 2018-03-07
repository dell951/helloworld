#!/usr/bin/python
#coding:utf-8

import os.path
import sys, getopt
import logging
import shutil
import subprocess
import re

def jarWrapper(path):
    process = subprocess.Popen(['java -jar JAVMovieScraper.jar -scrape dmm ' + path ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ret = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith('\n'):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')
    return ret

logging.getLogger().setLevel(logging.INFO)

search_path = str(sys.argv[1])

n = 0
k = 0

for parent, dirnames, filenames in os.walk(search_path):
    for filename in filenames:
        if (filename.endswith('rmvb') or filename.endswith('mp4') or filename.endswith('m4v') or filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('wmv')) and not filename.startswith("."):
            full_path = os.path.join(parent, filename)
            name, ext = os.path.splitext(full_path)
            fanart_file = os.path.join(parent, name + '-fanart.jpg')
            poster_file = os.path.join(parent, name + '-poster.jpg')
            nfo_file = os.path.join(parent, name + '.nfo')
            if os.path.exists(fanart_file) and os.path.exists(poster_file) and os.path.exists(nfo_file):
                pass
                #logging.info('Succeed.')
            else:
                k += 1
                result = jarWrapper(full_path)
                logging.info(result)
        else:
            pass
            #logging.info("skip file " + filename)

logging.info("procceed %d files " % k)
