from app import server
from flask import make_response, request
import json
from app.data_managers.message_data_manager import MessageDataManager


@server.route(rule='/messages/create', endpoint='message_create_get', methods=['GET'])
def fetch_template():
    return MessageDataManager().create_empty_message_without_id()


@server.route(rule='/messages/create', endpoint='message_create_post', methods=['POST'])
def create_message():
    dm = MessageDataManager()
    # request should be {'name': 'e1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    dm.insert_message_one(posted_dict)
    return json.dumps(posted_dict)


@server.route(rule='/messages/<string:message_id>/update', endpoint='replace_message', methods=['POST'])
def complete_update(message_id: str):
    if not message_id.__contains__('ms-'):
        raise Exception('invalid input')
    return 'valid'


@server.route(rule='/messages/<string:message_id>', endpoint='get_one_message', methods=['GET'])
def get_one(message_id: str):
    return json.dumps(MessageDataManager().find_message_by_id(message_id))


@server.route(rule='/messages/parent/<string:parent_id>/', endpoint='list_messages_by_parent', methods=['GET'])
def list_all_for_parent(parent_id):
    dm = MessageDataManager()
    message_dicts = dm.find_all_messages_for_parent(parent_id)
    return json.dumps({'messages': message_dicts})


@server.route(rule='/messages', endpoint='list_messages_by_thread', methods=['GET'])
def list_all():
    dm = MessageDataManager()
    message_dicts = dm.find_all_messages()
    return json.dumps({'messages': message_dicts})
