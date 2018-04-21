from flask import Flask
from flask import jsonify
import json

app = Flask(__name__)

@app.route("/data")
def queryJid():
    details = {}

    response = app.make_response(jsonify(details=details))
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'POST'  
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  
    return response 

def find_in_local():
    

if __name__ == "__main__":
    app.run(threaded=True)