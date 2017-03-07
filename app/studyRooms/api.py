from app import server
from flask import make_response,request

@server.route(rule='/studyRooms/<string:study_id>/create', endpoint='createStudy')
def create(study_id):
    ret = str(study_id) + 'create'
    return ret

@server.route(rule='/studyRooms/<string:study_id>/update', endpoint='updateStudy')
def create(study_id):
    ret = str(study_id) + 'update'
    return ret

@server.route(rule='/studyRooms/<string:study_id>/delete', endpoint='deleteStudy')
def create(study_id):
    ret = str(study_id) + 'delete'
    return ret

@server.route(rule='/studyRooms/search', endpoint='searchStudy')
def create():
    ret = 'search study rooms'
    return ret

@server.route(rule='/studyRooms/<string:study_id>', endpoint='fetchStudy')
def create(study_id):
    ret = str(study_id) + 'fetch'
    return ret

@server.route(rule='/studyRooms', endpoint='studyRooms')
def create(study_id):
    ret = str(study_id) + 'study rooms'
    return ret
