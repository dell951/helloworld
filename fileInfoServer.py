from flask import Flask
from flask import jsonify
from flask import request
import datetime
import json
import sys
import logging

logging.getLogger().setLevel(logging.INFO)

reload(sys)
sys.setdefaultencoding('utf8')
filename = '/volume1/nas-share/helloworld/allmine.txt'
#filename = '/volume1/nas-share/helloworld/allmine.txt'
datafile = file(filename)
app = Flask(__name__)

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
        for line in lines:
            if qid.lower().replace('-','') in line.lower().replace('-',''):
                found = True
                if 'czimu' in line:
                    czimu = True
                path = line.strip()
                break
        details = {
            "found": found,
            "czimu": czimu,
            "path": path
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
    found = False
    czimu = False
    for line in datafile:
        if jid.lower().replace('-','') in line.lower().replace('-',''):
            found = True
            if 'czimu' in line:
                czimu = True
            path = line.strip()
            break
    
    details = {
        "found": found,
        "czimu": czimu,
        "path": path
    }
    if found:
        logging.info(jid + " Found!")
    else:
        logging.info(jid + " Not exist.")
    datafile.seek(0)
    return details

if __name__ == "__main__":
    app.run(threaded=True,host='0.0.0.0',port=5555)
