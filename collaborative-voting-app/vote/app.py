from flask import Flask, render_template, request, make_response, g
import requests

import os
import socket
import random
import json
import http.client

option_a = os.getenv('OPTION_A', 'Cats')
option_b = os.getenv('OPTION_B', 'Dogs')
hostname = socket.gethostname()
namespace = os.getenv('CND_KUBERNETES_NAMESPACE', 'localhost')

client_id = os.getenv('CLIENT_ID', '')
client_secret = os.getenv('CLIENT_SECRET', '')

app = Flask(__name__)

def get_token():
    payload = {"client_id":client_id,"client_secret":client_secret,"audience":"https://okteto/vote","grant_type":"client_credentials"}
    _r = requests.post("https://okteto.auth0.com/oauth/token", json=payload)
    _r.raise_for_status()
    return _r.json()


@app.route("/", methods=['POST','GET'])
def vote():
    token = get_token()
    headers = {"authorization": "Bearer {}".format(token["access_token"])}
    vote = None
    if request.method == 'POST':
        if request.form['vote'] == 'a':
            vote = option_a
        else:
            vote = option_b
            
        _r = requests.post("http://api:8080", json={"vote": vote}, headers=headers)
        _r.raise_for_status()
    else:
        _r = requests.get("http://api:8080", headers=headers)
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
