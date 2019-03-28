from flask import Flask, jsonify, request
from collections import defaultdict

votes = defaultdict(int)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def post():
    content = request.get_json()
    vote = content["vote"]
    votes[vote] = votes[vote] + 1
    return ('', 204)

@app.route("/", methods=['GET'])
def get():
    return jsonify(votes)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
