from flask import *
from app import server
from app.event import api

@server.route('/')
def hello_world2():
    return 'Hello HOME and ONLY HOME!'


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
