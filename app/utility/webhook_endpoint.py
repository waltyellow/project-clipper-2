from app import server
from flask import request, make_response
from app.data_managers import common

from app.data_managers.event_data_manager import EventDataManager
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.message_data_manager import MessageDataManager
from app.utility import action_handler
import json
import geojson

import logging

logging.basicConfig(filename='webhook.log', level=logging.DEBUG)


@server.route('/wh', methods=['POST'])
def webhook():
    decoded_json = request.get_data().decode("utf-8")
    data_object = json.loads(decoded_json)

    action = data_object['result']['action']

    print(action)
    print(data_object)

    reply = "sorry, I did not understand this command"

    if action == 'get_place':
        try:
            location, place = find_location_and_place(data_object)
            print("getting" + location)
            if location == '':
                return "No location", 404
        except KeyError:
            return "No location", 404

        if not place:
            # we cannot find a place
            reply = reply_no_location(location)
        else:
            print(place)
            reply = reply_for_place(place)

    elif action == 'find_events':
        try:
            location, place = find_location_and_place(data_object)
            print("getting" + location)
            if not place:
                reply = reply_for_events_vague_location(location, location)
            else:
                print(place)
                reply = reply_for_events_at_place(place, location_name=place['name'])
        except KeyError:
            return "No location", 404

    # get place location
    # find nearby events
    elif action == 'events_near_me':
        try:
            coordinates = data_object['originalRequest']['data']['device']
            long = float(coordinates['longitude'])
            lat = float(coordinates['latitude'])
        except KeyError:
            return 'permission_failed'
        reply = reply_for_events_exact_coordinates(long=long, lat=lat, location_name='you')
        # find nearby events

    elif action == 'get_messages_for_place':
        try:
            location, place = find_location_and_place(data_object)
        except KeyError:
            return 'failed lookup'
        if not place:
            reply = "sorry, I did not understand where you are looking at"

        messages = MessageDataManager().find_messages_by_filter({'parent': place['place_id']})
        reply = reply_comments(messages, place['name'])

        # find nearby events

    elif action == 'create_event_yes':
        try:
            location, place = find_location_and_place(data_object)
            print(location)
            print(place)
            edm = EventDataManager()
            event = edm.create_empty_event()
            print(event)
            parameters = data_object['result']['parameters']
            print(parameters)
            event['name'] = parameters['name']
            print(event)
            event['description'] = parameters['description']
            print(event)
            event['time'] = parameters['time']
            print(event)

            event['location'] = location
            print(event)
            edm.insert_event_one(event)
            if place:
                event['geo_coordinates'] = place['geo_coordinates']
                event['place_id'] = place['place_id']
                edm.replace_one_event(event)
            print('created')
            print(event)
            reply = "Success " + serialize_event(event, 'created') + " from Google Assistant"

        except KeyError:
            reply = "Event Creation failed due to unknown reasons"
    res = {
        "speech": reply,
        "source": "evention"
    }
    print("sent" + reply)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def reply_no_location(location: str):
    reply = "Sorry, we cannot find " + location + ", try a different name?"
    return reply


def reply_for_place(place: dict):
    name = place['name']
    rating = place['rating_average']
    adjective = rating_to_quality(rating)

    print(place)
    action_handler.refresh_score_for_entity(place, action_handler.place_senti_lifetime_in_days)
    print(place)

    excitement_level = score_to_quality(place['senti_score'])
    reply = "Here is the rating and excitement level for " + name + \
            ". The rating is " + str(rating) + " which is " + adjective + \
            ". The excitement level is " + excitement_level + " right now."
    print(place)
    return reply


def reply_for_events_at_place(place: dict, location_name: str):
    print("events for" + place['place_id'])
    events = EventDataManager().find_events_by_filter({'place_id': place['place_id']})
    print(events)
    return reply_for_events(events, place['name'])


def reply_for_events_exact_coordinates(long: float, lat: float, location_name: str = 'where you are'):
    events = EventDataManager().find_events_near(long=long, lat=lat)
    return reply_for_events(events, location_name)


def reply_for_events_vague_location(location: str, location_name: str = 'the location you asked for'):
    events = EventDataManager().find_events_by_filter({'location': common.generate_search_query(location)})
    return reply_for_events(events, location_name)


def reply_for_events(events: [dict], location_name: str):
    first_string = 'first '
    if len(events) == 0:
        reply = "sorry, we cannot find any events at {0}.".format(location_name)
    else:
        if len(events) == 1:
            reply = "I found one event at {0}. ".format(location_name)
            first_string = ''
        else:
            reply = "Here are the {0} events. ".format(len(events))
    print(reply)
    first = False
    for event in events:
        if not first:
            reply += serialize_event(event, first_string)
            first = True
        else:
            reply += serialize_event(event, 'next ')
    return reply


def serialize_event(event: dict, seq: str = 'next'):
    name = event['name']
    excitement_level = score_to_quality(event['senti_score'])
    location = event['location']
    description = event['description']

    reply = "The {0} event is {1} at {2}. Our data show it is {3} at this moment. ".format(seq, name, location,
                                                                                           excitement_level)
    if description != '':
        reply += "This event is about {0}.".format(description)
    else:
        pass

    if 'food' in event and event['food'] != '':
        reply += "In terms of food, there is also {0} offered there.".format(event['food'])
    return reply


def reply_comments(comments: [dict], location_name: str):
    first_string = 'first '
    if len(comments) == 0:
        reply = "sorry, we cannot find any comments at {0}.".format(location_name)
    else:
        if len(comments) == 1:
            reply = "I found one event at {0}. ".format(location_name)
            first_string = ''
        else:
            reply = "Here are the {0} events. ".format(len(events))
    print(reply)
    first = False
    for comment in comments:
        if not first:
            reply += serialize_event(comment, first_string)
            first = True
        else:
            reply += serialize_event(comment, 'next ')
    return reply


def serialize_comment(comment: dict, seq: str = 'next'):
    body = comment['body']

    reply = "The {0} comment says {1}. ".format(seq, body)
    return reply


def find_location_and_place(data_object):
    location = data_object['result']['parameters']['location']
    location = sanitize_location(location)
    place = PlaceDataManager().find_one_by_filter({'name': common.generate_search_query(location)})
    # place = {'name': "Tomlinson Food Court",
    #          'rating_average': 3.3,
    #          'senti_score': 16,
    #          'coordinate': {"type": "Point",
    #                         "coordinates": [100.0, 0.0]}
    #          }
    return location, place


def sanitize_location(location):
    return location


def rating_to_quality(rating):
    rating = float(rating)
    if rating > 4:
        return "excellent"
    elif rating > 3:
        return "pretty good"
    elif rating > 2:
        return "ok"
    elif rating > 0:
        return "poorly rated"
    else:
        return "not yet rated"


def score_to_quality(score):
    score = float(score)
    if score > 10:
        return "very exciting"
    elif score > 5:
        return "trending"
    elif score > 2:
        return "a bit exciting"
    else:
        return "not really exciting"


def test():
    location = 'Tomlinson'
    location = sanitize_location(location)
    place = PlaceDataManager().find_one_by_filter({'name': common.generate_search_query(location)})
    print(place)
    print(reply_for_place(place))


if __name__ == "__main__":
    test()
