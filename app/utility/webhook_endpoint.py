from app import server
from flask import request, make_response
import json

import logging

logging.basicConfig(filename='webhook.log', level=logging.DEBUG)


@server.route('/wh', methods=['POST'])
def webhook():
    data = json.loads(request.data)

    location = data['parameters']['location']

    reply =  "Here is the rating and excitement level for" + location + \
    "The rating is 4.25 which is excellent. " \
    "The excitement level is high right now."

    res = {
        "speech": reply,
        "source": "evention"
    }

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
