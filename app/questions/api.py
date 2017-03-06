from app import server
from flask import make_response, request

@server.route(rule='/questions/<string:question_id>/create', endpoint='createQuestion')
def create(question_id):
    ret = str(question_id) + 'create'
    return ret


@server.route(rule='/questions/<string:question_id>/update', endpoint='updateQuestion')
def create(question_id):
    ret = str(question_id) + 'update'
    return ret


@server.route(rule='/questions/<string:question_id>/delete', endpoint='deleteQuestion')
def create(question_id):
    ret = str(question_id) + 'delete'
    return ret


@server.route(rule='/questions/search', endpoint='searchQuestion')
def create():
    ret = 'search questions'
    return ret


@server.route(rule='/questions/<string:question_id>', endpoint='fetchQuestion')
def create(question_id):
    ret = str(question_id) + 'fetch'
    return ret


@server.route(rule='/questions', endpoint='questions')
def create(question_id):
    ret = str(question_id) + 'questions'
    return ret
