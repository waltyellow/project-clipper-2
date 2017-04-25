from app import server
from flask import request, make_response
from app.data_managers import common
from app.data_managers.event_data_manager import EventDataManager
from app.data_managers.places_data_manager import PlaceDataManager
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

    reply = "sorry, I did not understand this command"

    if action == 'get_place':
        try:
            location, place = find_location_and_place(data_object)
            if location == '':
                return "Ask for location", 404
        except KeyError:
            return "No location", 404

        if not place:
            reply = reply_no_location(location, reply)
        else:
            reply = reply_for_place_metadata(place)

    elif action == 'find_events':
        try:
            location, place = find_location_and_place(data_object)
            if not place:
                reply = reply_no_location(location, reply)
            else:
                query_position = place['geo_coordinate']
                reply = reply_for_events(query_position, location_name=place['name'])
        except KeyError:
            return "No location", 404

    # get place location
    # find nearby events
    elif action == 'events_near_me':
        try:
            coordinates = data_object['originalRequest']['data']['device']
            query_position = geojson.Point((coordinates['longitude'], coordinates['latitude']))
        except KeyError:
            try:
                location, place = find_location_and_place(data_object)
                query_position = place['geo_coordinate']
            except KeyError:
                if location == '':
                    return "No coordinate", 404
                else:
                    reply = reply_no_location(location, reply)
        reply = reply_for_events(query_position, location_name='you')

        # find nearby events

    res = {
        "speech": reply,
        "source": "evention"
    }

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def reply_no_location(location, reply):
    reply = "Sorry, we cannot find" + location + ", try a different name?"
    return reply


def reply_for_place_metadata(place):
    name = place['name']
    rating = place['rating_average']
    adjective = rating_to_quality(rating)
    # place = action_handler.refresh_score_for_entity(place, action_handler.place_senti_lifetime_in_days)
    excitement_level = score_to_quality(place['senti_score'])
    reply = "Here is the rating and excitement level for " + name + \
            ". The rating is " + str(rating) + " which is " + adjective + \
            ". The excitement level is " + excitement_level + " right now."
    return reply


def reply_for_events(query_position, location_name='you asked for'):
    query_position = geojson.Point((123, 45))
    return "many events near " + location_name


def find_location_and_place(data_object):
    location = data_object['result']['parameters']['location']
    location = sanitize_location(location)
    place = PlaceDataManager().find_one_by_filter({'name': common.generate_search_query(location)})
    place = {'name': "Tomlinson Food Court", 'rating_average': 3.3, 'senti_score': 16}
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
    else:
        return "poorly rated"


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
