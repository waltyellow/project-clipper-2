from app import server
from flask import make_response, request


@server.route(rule='/events/<string:event_id>/create', endpoint='createevent')
def create(event_id):
    ret = str(event_id) + 'create'
    return ret


@server.route(rule='/events/<string:event_id>/update', methods=['GET'])
def update(event_id):
    ret = str(event_id) + 'update'
    return ret