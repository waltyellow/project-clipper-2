from app import server
from flask import make_response, request
import json
from app.models.message import Message
from app.data_managers.message_data_manager import MessageDataManager


@server.route(rule='/messages/create', endpoint='message_create_get', methods=['GET'])
def fetch_template():
    return Message().toJson()


@server.route(rule='/messages/create', endpoint='message_create_post', methods=['POST'])
def create_message():
    dm = MessageDataManager()
    # request should be {'name': 'e1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    posted_message = Message.message_from_dict(posted_dict)
    dm.insert_message_one(posted_message)
    return posted_message.toJson()


@server.route(rule='/messages/<string:message_id>/update', endpoint='replace_message', methods=['POST'])
def complete_update(message_id: str):
    if not message_id.__contains__('ms-'):
        raise Exception('invalid input')
    return 'valid'


@server.route(rule='/messages/thread/<string:thread_id>', endpoint='get_one_message', methods=['GET'])
def get_one(message_id: str, type: str):
    return MessageDataManager().find_message_by_id(message_id).toJson()


@server.route(rule='/messages/<string:thread_id>/', endpoint='list_messages_by_thread', methods=['GET'])
def list_all():
    dm = MessageDataManager()
    messages = dm.find_all_messages()
    message_dicts = []
    for message in messages:
        message_dicts.append(message.__dict__)
    return json.dumps({'messages': message_dicts})
