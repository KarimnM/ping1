from flask import Flask, app
from flask.json import jsonify
from flask_httpauth import HTTPDigestAuth
import time
import requests
from requests.auth import HTTPDigestAuth as HTTPAuth


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "vcu": "rams"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message':'Wrong page'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message':'Something is Broke'}), 500


@app.route('/ping', methods=['GET'])
@auth.login_required
def ping():
    url = 'http://127.0.0.1:7005/'
    start_time = time.time()
    r = requests.get(url + 'pong', auth=HTTPAuth('vcu','rams'))
    end_time = time.time()
    pingpong_t = (end_time-start_time) * 1000
    return jsonify({"pingpong_t": pingpong_t}) , 201
