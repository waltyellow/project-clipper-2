from app import server
from flask import request, make_response
import json

@server.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

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