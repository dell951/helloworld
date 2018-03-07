#!/usr/bin/python
#coding:utf-8

import os.path
import sys, getopt
import logging
import shutil
import subprocess
import re

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(raw_input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

logging.getLogger().setLevel(logging.DEBUG)
#search_path = '/Users/azu/dell951git/forPlex'

search_path = str(sys.argv[1])
to_path = ''

if len(sys.argv) >= 3 and str(sys.argv[2]):
    to_path = str(sys.argv[2])
    logging.info("Files will be moved to %s finally." % to_path)
else:
    logging.info("List information only")

p = re.compile(r'(\[Thz.la\])?(?P<s_name>[a-zA-Z]*)-?(?P<num_id>\d*)(\[.*\])?\.(?P<ext>[mp4aviwmk]*)')
n_p = re.compile(r'[a-zA-Z]+-\d+.[mp4aviwm]+')

n = 0
k = 0
for parent, dirnames, filenames in os.walk(search_path):
    pass
    for filename in filenames:
        n += 1
        if (filename.endswith('rmvb') or filename.endswith('mp4') or filename.endswith('m4v') or filename.endswith('mkv') or filename.endswith('avi') or filename.endswith('wmv')) and not filename.startswith("."):
            m = p.search(filename)
            new_name = m.group("s_name") + "-" + m.group("num_id") + "." + m.group("ext")
            k += 1
            ismatch = n_p.match(new_name)
            full_path = os.path.join(parent, filename)
            if ismatch:
                logging.debug("Succeed --> " + filename + " --> " + new_name )  
                if (to_path != ''):
                    dest_path = os.path.join(to_path, new_name.lower())
                    if (yes_or_no("Shall I move the file %s (y/n)?" % full_path)):
                        shutil.move(full_path, dest_path)
                        logging.info("file %s moved to %s" % (full_path, dest_path))
                    else:
                        reply = str(raw_input('Provide a new name:')).lower().strip()
                        dest_path = os.path.join(to_path, reply)
                        shutil.move(full_path, dest_path)
                        logging.info("New Name provided, file %s moved to %s" % (full_path, dest_path)) 
            else:
                logging.warn("******WRONG***** --> " + filename + " --> " + new_name )
                if (yes_or_no("**DELETE THE FILE?** (y/n)?")):
                    os.remove(full_path)
                    logging.info("file %s REMOVED." % full_path )
                else:
                    reply = str(raw_input('Provide a new name:')).lower().strip()
                    if (reply == 'n'):
                        logging.info("Do nothing for now.") 
                    else:
                        dest_path = os.path.join(to_path, reply)
                        shutil.move(full_path, dest_path)
                        logging.info("New Name provided, file %s moved to %s" % (full_path, dest_path)) 

print "Totally : %d/%d " % (k,n)
