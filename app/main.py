from flask import *
from flask_cors import CORS, cross_origin
from app import server
from app.event import api
from app.message import api
from app.places import api
from app.utility import webhook_endpoint
from app.geo import api
import os

CORS(server)


@server.route('/')
def hello_world2():
    return 'hello'


@server.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(server.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@server.route(rule='/example/<string:event_id>/create', endpoint='optional')
def create2(event_id):
    ret = str(event_id) + '-> example create'
    url = url_for('createevent', event_id=event_id)
    # this is one way to internally refer to endpoint/createevent from endpoint/createexample
    return redirect(url)


@server.route(rule='/example/<string:event_id>/update')
def update2(event_id):
    ret = str(event_id) + ' -> example update'
    return ret


if __name__ == '__main__':
    server.run(debug=True)
