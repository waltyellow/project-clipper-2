import json

from flask import request

import app.data_managers.message_data_manager as mdm
from app import server
from app.data_managers import common
from app.data_managers.message_data_manager import MessageDataManager


@server.route(rule='/messages/template', endpoint='message_create_get', methods=['GET'])
def fetch_message_template():
    return json.dumps(mdm.min_message_dict)


@server.route(rule='/messages/create', endpoint='message_create_post', methods=['POST'])
def create_message():
    dm = MessageDataManager()
    # request should be {'name': 'm1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    dm.insert_message_one(posted_dict)
    return json.dumps(posted_dict)


'''replace message does not replace ID'''


@server.route(rule='/messages/replace', endpoint='replace_message', methods=['POST'])
def replace_one_message():
    dm = MessageDataManager()
    # request should be {"name": 'm1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    message_id = posted_dict['message_id']
    if not message_id.__contains__('ms-'):
        raise Exception('invalid input')
    return dm.replace_one_message(posted_dict)


'''update by a list of diffs '''


@server.route(rule='/messages/<string:event_id>/update', endpoint='replace', methods=['POST'])
def uodate_message(message_id: str):
    if not message_id.__contains__('ms-'):
        raise Exception('invalid input')
    dm = MessageDataManager()
    # update request should be {"updates": [{"key":"some_key", "new_value","some_value"},  ... ]}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    updates = posted_dict['updates']
    # each update
    for update in updates:
        key = update['key']
        new_value = update['new_value']
        dm.update_one_message_by_diff(message_id=message_id, key=key, new_value=new_value)
    return dm.find_messages_by_filter(message_id)


'''get one message'''


@server.route(rule='/messages/<string:message_id>', endpoint='get_one_message', methods=['GET'])
def get_one_message(message_id: str):
    return json.dumps(MessageDataManager().find_message_by_id(message_id))


'''search for messages based on a certain criteria'''
'''
Search for messages whose parent is ev-1234 AND other criterias
-  /messages?parent=ev-1234&criteria=something

'''
'''search for messages based on a certain criteria'''


@server.route(rule='/messages', endpoint='list_messages_by_filter', methods=['GET'])
def list_all_messages_for_filter():
    filter = common.search_parameter_to_db_filter(request.args)
    return query_for_message_filter(filter)


def query_for_message_filter(filter):
    dm = MessageDataManager()
    print('filtering messages by' + filter.__str__())
    message_dicts = dm.find_messages_by_filter(filter)
    return json.dumps({'messages': message_dicts})
