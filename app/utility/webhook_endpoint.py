from app import server
from flask import request, make_response
from app.data_managers import common
from app.data_managers.event_data_manager import EventDataManager
from app.data_managers.places_data_manager import PlaceDataManager
from app.utility import action_handler
import json

import logging

logging.basicConfig(filename='webhook.log', level=logging.DEBUG)


@server.route('/wh', methods=['POST'])
def webhook():
    decoded_json = request.get_data().decode("utf-8")
    data_object = json.loads(decoded_json)

    action = data_object['result']['action']

    if action == 'get_place':
        location = data_object['result']['parameters']['location']
        location = sanitize_location(location)
        # places = PlaceDataManager().find_places_by_filter({'name':common.generate_search_query(location)})
        places = [{'name': "Tomlinson Food Court", 'rating_average': 3.3}]
        if not places:
            reply = "Sorry, we cannot find" + location + ", try a different name?"
        else:
            place = places[0]
            name = place['name']
            rating = place['rating_average']
            adjative = rating_to_quality(rating)
            place = action_handler.refresh_score_for_entity(place, action_handler.place_senti_lifetime_in_days)
            excitement_level = score_to_quality(place['senti_score'])
            reply = "Here is the rating and excitement level for " + name + \
                    ". The rating is " + rating + " which is " + adjative + \
                    ". The excitement level is " + excitement_level + " right now."

    elif action == 'find_event':
        location = data_object['result']['parameters']['location']
        location = sanitize_location(location)
        places = PlaceDataManager().find_places_by_filter(common.generate_search_query(location))
        # get place location
        # find nearby events
    

    if location == '':
        return "Nope", 404

    res = {
        "speech": reply,
        "source": "evention"
    }

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


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
