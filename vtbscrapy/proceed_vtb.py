#!/usr/bin/python
# coding:utf-8

import os.path
import sys
import logging
import shutil
import re
import subprocess

logging.getLogger().setLevel(logging.INFO)

search_path = str(sys.argv[1])

search_string_pattern= r'(.*)\.(\d\d\.\d\d\.\d\d)\.(.*).xxx.*\.mp4'

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
                search_target = filename.lower()
                if search_target.startswith("blacked") or search_target.startswith("tushy") or search_target.startswith("vixen"):
#                    print search_target
                    target_match = re.match(search_string_pattern, search_target)
                    if target_match:
                        cmd = "./docker-search.sh %s %s %s %s" %(target_match.group(1), target_match.group(3),target_match.group(2),'False')
                        print "#%s" % cmd
                        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        output, err = p.communicate()
                        scrapycmd = output.split(b'\n')[0]
                        print "output - [[[%s]]]" % scrapycmd
                        if scrapycmd == "Nothing found":
                            pass
                        else:
                            print scrapycmd
                            targetFileName = scrapycmd.split(' ')[2]
                            print "mv %s %s.mp4" % (full_path, os.path.join(parent,targetFileName))


        else:
            pass
            #logging.info("skip file " + filename)
