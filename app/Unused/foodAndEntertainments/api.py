from app import server
from flask import make_response, request


@server.route(rule='/foodAndEntertainments/<string:food_id>/create', endpoint='createFood')
def create(food_id):
    ret = str(food_id) + 'create'
    return ret


@server.route(rule='/foodAndEntertainments/<string:food_id>/update', endpoint='createFood')
def create(food_id):
    ret = str(food_id) + 'update'
    return ret


@server.route(rule='/foodAndEntertainments/search', endpoint='createFood')
def search(food_id):
    ret = str(food_id) + 'search food'
    return ret


@server.route(rule='/foodAndEntertainments/<string:food_id>', endpoint='createFood')
def fetch(food_id):
    ret = str(food_id) + 'fetch'
    return ret

