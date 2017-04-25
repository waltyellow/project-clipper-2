"""`main` is the top level module for this Flask application."""
import os
import sys
import json
import logging
import json

from flask import Flask, request
import requests

#from google.appengine.api import urlfetch
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/', methods=['POST'])
def webhook():
    logging.info("we heard from api.ai, request is here")
    logging.info(request.method.__str__())
    logging.info(request.headers.__str__())
    logging.info(request.data.__str__())

    resp = requests.post(
        url='https://cl1.zhenglinhuang.com:5000/wh',
        data=request.data)

    logging.info("we heard from clipper, resp is here")
    logging.info(resp.headers.__str__())
    logging.info(resp.status_code.__str__())
    logging.info(resp.text.__str__())

    flask_resp = (resp.text, resp.status_code, resp.headers.items())

    return flask_resp

@app.route('/', methods=['GET'])
def webhook_get():
    logging.info("we heard from a human!")
    return "Welcome to get", 200

if __name__ == '__main__':
    resp = requests.request('GET', 'https://cl1.zhenglinhuang.com:5000/wh')
    print(resp)