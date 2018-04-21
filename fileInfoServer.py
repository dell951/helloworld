from flask import Flask
from flask import jsonify
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/<jid>")
def queryJid(jid):
    details = search_in_local(jid)

    response = app.make_response(jsonify(details=details))
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'POST'  
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  
    return response 

def search_in_local(jid):
    datafile = file('iready.txt')
    path = ''
    found = False
    for line in datafile:
        print jid.lower() + ',' + line.lower()
        if jid.lower() in line.lower():
            found = True
            path = line.strip()
            break
    
    details = {
        "found": found,
        "path": path,
        "size": 1234
    }
    return details

if __name__ == "__main__":
    app.run(threaded=True)
