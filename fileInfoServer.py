from flask import Flask
from flask import jsonify
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/<jid>")
def queryJid(jid):
    if (jid == 'favicon.ico'):
        return app.make_response(jsonify(details={}))
    start = datetime.datetime.now()
    details = search_in_local(jid)
    end = datetime.datetime.now()
    print (end-start)
    response = app.make_response(jsonify(details=details))
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'POST'  
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  
    return response 

def search_in_local(jid):
    datafile = file('allmine.txt')
    path = ''
    found = False
    for line in datafile:
        if jid.lower() in line.lower():
            found = True
            path = line.strip()
            break
    
    details = {
        "found": found,
        "path": path
    }
    return details

if __name__ == "__main__":
    app.run(threaded=True)
