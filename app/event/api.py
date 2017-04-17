from app import server
from flask import make_response, request, current_app
from flask_cors import CORS, cross_origin
import json
from app.models.event import Event
from app.data_managers.event_data_manager import EventDataManager
from app.data_managers.message_data_manager import MessageDataManager
from app.sentiment.emotion import emotion_data

@server.route(rule='/events/create', endpoint='event_create_get', methods=['GET'])
def fetch_template():
    return Event().toJson()


@server.route(rule='/events/create', endpoint='event_create_post', methods=['POST'])
def create_event():
    dm = EventDataManager()
    # request should be {'name': 'e1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    posted_event = Event.event_from_dict(posted_dict)
    posted_event.headers.add('Access-Control-Allow-Origin', '*')
    dm.insert_event_one(posted_event)
    return posted_event.toJson()


@server.route(rule='/events/<string:event_id>/update', endpoint='replace an event', methods=['POST'])
def complete_update(event_id: str):
    if not event_id.__contains__('ev-'):
        raise Exception('invalid input')
    return 'valid'


@server.route(rule='/events/<string:event_id>', endpoint='get_one_event', methods=['GET'])
def get_one(event_id: str):
    return EventDataManager().find_event_by_id(event_id).toJson()


@server.route(rule='/events/', endpoint='list_events', methods=['GET'])
def list_all():
    dm = EventDataManager()
    events = dm.find_all_events()
    event_dicts = []
    for event in events:
        event_dicts.append(event.__dict__)
    return json.dumps({'events': event_dicts})


@server.route(rule='/messages/create', endpoint='add_comment', methods=['POST'])
def add_comment():
    comment_dict = request.form
    comment_sentics = emotion_data(comment_dict['message_body'])['sentics']
    comment_dict['message_senti_score'] = sum(comment_sentics.values())
    comment_dict = MessageDataManager.insert_message_one(comment_dict)
    return json.dumps(dict(message_senti_score=comment_dict['message_senti_score']))
