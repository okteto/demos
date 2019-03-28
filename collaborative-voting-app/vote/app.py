from flask import Flask, render_template, request, make_response, g
import requests

import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', 'Otters')
option_b = os.getenv('OPTION_B', 'Dogs')
hostname = socket.gethostname()
namespace = os.getenv('CND_KUBERNETES_NAMESPACE', 'localhost')

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def hello():
    vote = None
    if request.method == 'POST':
        if request.form['vote'] == 'a':
            vote = option_a
        else:
            vote = option_b
            
        _r = requests.post("http://api:8080", json={"vote": vote})
        _r.raise_for_status()
    
    _r = requests.get("http://api:8080")
    _r.raise_for_status()
    votes = _r.json()
    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        votes_a=votes.get(option_a, 0),
        votes_b=votes.get(option_b, 0),
        namespace=namespace))

    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
