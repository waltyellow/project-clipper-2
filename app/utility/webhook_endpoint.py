from app import server
from flask import request, make_response
import json

import logging
logging.basicConfig(filename='webhook.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

@server.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    logging.info("Request:")
    logging.info(json.dumps(req, indent=4))

    res = {
        "speech": "hello",
        "displayText": "back",
        # "data": data,
        # "contextOut": [],
        "source": "evention"
    }

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@server.route('/webhook', methods=['GET'])
def webhook_get():
    return "you have reached the webhook"

