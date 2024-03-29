#!/usr/bin/python

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import os
import datetime
import json
import sys
import logging
import subprocess

logging.getLogger().setLevel(logging.INFO)

reload(sys)
sys.setdefaultencoding('utf8')
filename = '/volume1/nas-share/helloworld/allmine.txt'
#filename = '/volume1/nas-share/helloworld/allmine.txt'
datafile = file(filename)
app = Flask(__name__)
CORS(app)

@app.route("/postnfo", methods=['POST'])
def handlenfo():
    nfoJson = request.get_json()
    cmd = './nfomaker.py -i ' + nfoJson["file"] + ' -m "' + nfoJson["title"] + '" -s "' + nfoJson["studio"] + '" -r "' + nfoJson["date"] + '" -d "' + nfoJson["desc"] + '"' + ' -f "' + nfoJson["fanart"] + '"' + ' -p "' + nfoJson["poster"] + '"'
    for star in nfoJson["stars"]:
        if (star.strip() != ""):
            cmd = cmd + ' -a "' + star.strip() + '"'
    os.system(cmd)
    response = app.make_response(jsonify(details={"Status":"Succeeded"}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

@app.route("/jid=<jid>")
def queryJid(jid):
    if (jid == 'favicon.ico'):
        return app.make_response(jsonify(details={}))
    logging.info("searching %s ..." % jid)
    start = datetime.datetime.now()
    details = search_in_local(jid)
    end = datetime.datetime.now()
    logging.info(end-start)
    response = app.make_response(jsonify(details=details))
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'POST'  
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  
    return response 

@app.route('/find', methods=['POST'])
def find():
    start = datetime.datetime.now()
    lines = [line.rstrip('\n') for line in open(filename)]

    rtn_json = {}
    data = request.get_json(force=True)
    ids_list = data['ids_list']
    for qid in ids_list:
        logging.info("check %s " % qid)
        path = ''
        found = False
        czimu = False
        res = ''
        hbackup = False
        for line in lines:
            if qid.lower().replace('-','') in line.lower().replace('-',''):
                found = True
                path = line.strip()
                res = retrieve_resolution(path)    
                if 'czimu' in line:
                    czimu = True                
                break
        
        total = hasHighBackup(qid)
        logging.info("has backup %s" % total)
        if len(total) >= 2:
            hbackup = True
        
        details = {
            "found": found,
            "czimu": czimu,
            "path": path,
            "resolution": res,
            "hbackup": hbackup
        }
        rtn_json[qid] = details

    #logging.info('rtn_json data is : %s' % rtn_json )
    response = app.make_response(jsonify(details_list=rtn_json))
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'POST'  
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  
    end = datetime.datetime.now()
    logging.info( end - start)
    return response

def search_in_local(jid):
    path = ''
    res = ''
    found = False
    czimu = False
    hbackup = False
    for line in datafile:
        if jid.lower().replace('-','') in line.lower().replace('-',''):
            found = True
            path = line.strip()
            res = retrieve_resolution(path)
            if 'czimu' in line:
                czimu = True
            break
    
    total = hasHighBackup(jid)
    if len(total) >= 2:
        hbackup = True

    details = {
        "found": found,
        "czimu": czimu,
        "path": path,
        "resolution": res,
        "hbackup": hbackup
    }
    if found:
        logging.info(jid + " Found!")
    else:
        logging.info(jid + " Not exist.")
    datafile.seek(0)
    return details

def hasHighBackup(jid):
    cmd = "grep -i " + jid + " " + filename
    process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    ret = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '':
            ret.append(line[:-1])
            #ret.append(line.strip())
    
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')
    return ret

def retrieve_resolution(path):
    cmd = "ffmpeg -i "+ path +" 2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}' | cut -d'x' -f2"
    print cmd
    process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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

if __name__ == "__main__":
#    app.run(threaded=True,host='0.0.0.0',port=5556,ssl_context='adhoc')
    app.run(threaded=True,host='0.0.0.0',port=5556,ssl_context=('cert.pem','key.pem'))

