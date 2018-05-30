from flask import Flask
from flask import jsonify
import datetime
import json
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/<jid>")
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

def search_in_local(jid):
    datafile = file('/volume1/nas-share/helloworld/allmine.txt')
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
    return details

if __name__ == "__main__":
    app.run(threaded=True,host='0.0.0.0',port=5555)
