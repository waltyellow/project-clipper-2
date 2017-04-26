import json
import time

from flask import request

import app.data_managers.event_data_manager as edm
from app import server
from app.data_managers.common import search_parameter_to_db_filter
from app.data_managers.event_data_manager import EventDataManager
from app.utility import action_handler


@server.route(rule='/events/template', endpoint='event_create_get', methods=['GET'])
def fetch_event_template():
    return json.dumps(edm.min_event_dict)


@server.route(rule='/events/create', endpoint='event_create_post', methods=['POST'])
def create_event():
    dm = EventDataManager()
    # request should be {'name': 'e1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    dm.insert_event_one(posted_dict)
    action_handler.generate_dynamic_score_for_event(event=posted_dict)
    return posted_dict


'''replace does not replace ID'''


@server.route(rule='/events/replace', endpoint='replace_event', methods=['POST'])
def replace_one_event():
    dm = EventDataManager()
    # request should be {"name": 'e1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    event_id = posted_dict['event_id']
    if not event_id.__contains__('ev-'):
        raise Exception('invalid input')
    action_handler.generate_dynamic_score_for_event(event=posted_dict)
    return dm.replace_one_event(posted_dict)


'''update by a list of diffs '''


@server.route(rule='/events/<string:event_id>/update', endpoint='update_an_event_by_diff', methods=['POST'])
def update_event(event_id: str):
    if not event_id.__contains__('ev-'):
        raise Exception('invalid input')
    dm = EventDataManager()
    # update request should be {"updates": [{"key":"some_key", "new_value","some_value"},  ... ]}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    updates = posted_dict['updates']
    # each update
    for update in updates:
        key = update['key']
        new_value = update['new_value']
        dm.update_one_event_by_diff(event_id=event_id, key=key, new_value=new_value)
    event = dm.find_event_by_id(event_id)
    action_handler.generate_dynamic_score_for_event(event=event)
    return event



'''listing endpoints'''

'''list one event given ID
/events/ev-WL3AF09tc8EauQdu
'''


@server.route(rule='/events/<string:event_id>', endpoint='get_one_event', methods=['GET'])
def get_one_event(event_id: str):
    event = EventDataManager().find_event_by_id(event_id)
    action_handler.generate_dynamic_score_for_event(event)
    return json.dumps(event)


'''
alias for search, should never be passed in without parameters in production
list ALL events - /events/
/events/?name=cake or /events?name=cake
is the same as
/events/search?name=cake
'''


@server.route(rule='/events/', endpoint='list_events', methods=['GET'])
def list_events():
    return search_event()


'''search for events based on a certain criteria
ex.
Search for events whose name is exactly cake -  /events/search?name=cake
Search for events whose name contains frosting -  /events/search?name_search=frosting
Search for events whose score is larger than 25 - /events/search?score={"$gt":25}
Search for events that is not repeated - /events/search?repeated=false (note the lower case false)
Search for events by multiple criterias /events/search?f1=criteria_1&f2=criteria2
'''


@server.route(rule='/events/search', endpoint='search_event', methods=['GET'])
def search_event():
    filter = search_parameter_to_db_filter(request.args)
    dm = EventDataManager()
    print('filtering by' + filter.__str__())
    event_dicts = dm.find_events_by_filter(filter)
    for e in event_dicts:
        action_handler.generate_dynamic_score_for_event(event=e)
    return json.dumps({'events': event_dicts})



if __name__ == '__main__':
    print(time.time())
