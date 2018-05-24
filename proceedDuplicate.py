#!/usr/bin/python

import os
import sys
import subprocess
import logging

logging.getLogger().setLevel(logging.INFO)
work_path = str(sys.argv[1])

fetch_all_dup_cmd = "ls -la %s/*-cd2.* | awk '{print $NF}' | sed -re 's/-cd2//g' > dup_list.txt" % work_path
ffmpeg_join_cmd = "ffmpeg -f concat -safe 0 -i dup_file.txt -c copy "

def run_command(command, runIt):
    logging.info(command)
    if runIt:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, shell=True)
        out, err = p.communicate()
        logging.info('--------Command Output Start-----\n%s' % out)
    else:
        pass

def gen_dup_file(lead_filename, ext):
    run_command("for i in `ls -la %s*%s | awk '{print $NF}'`; do LEN=`expr length $i`; echo $LEN $i; done | sort -n | sed -re \"s/^.*\s/file '/g\" | sed -re \"s/$/'/g\"> dup_file.txt " % (lead_filename, ext), True)
    run_command(ffmpeg_join_cmd + lead_filename + "-full" + ext, True)
    with open('dup_file.txt', 'r') as f:
        for line in f:
                filename = line.rstrip('\n').replace("file '","").replace("'","")
                if not os.path.isfile(filename):
                        logging.info("File %s not exist." % filename)
                else:
                        run_command("mv %s %s.done" % (filename,filename), True)
    run_command("mv %s %s" % (lead_filename + "-full" + ext, lead_filename + ext), True)

run_command(fetch_all_dup_cmd, True)

with open('dup_list.txt', 'r') as f:
    for line in f:
        filename = line.rstrip('\n')
        if not os.path.isfile(filename):
            logging.info("File %s not exist." % filename)
        else:
            gen_dup_file(os.path.splitext(filename)[0],os.path.splitext(filename)[1])
            sys.exit(0)