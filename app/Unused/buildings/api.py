from app import server
from flask import make_response,request

@server.route(rule='/buildings/<string:building_id>/create', endpoint='createBuilding')
def create(building_id):
    ret = str(building_id) + 'create'
    return ret

@server.route(rule='/buildings/<string:building_id>/update', endpoint='updateBuilding')
def create(building_id):
    ret = str(building_id) + 'update'
    return ret

@server.route(rule='/buildings/<string:building_id>/delete', endpoint='deleteBuilding')
def create(building_id):
    ret = str(building_id) + 'delete'
    return ret

@server.route(rule='/buildings/search', endpoint='searchBuilding')
def create():
    ret = 'search buildings'
    return ret

@server.route(rule='/buildings/<string:building_id>', endpoint='fetchBuilding')
def create(building_id):
    ret = str(building_id) + 'fetch'
    return ret

@server.route(rule='/buildings', endpoint='buildings')
def create(building_id):
    ret = str(building_id) + 'buildings'
    return ret
