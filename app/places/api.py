from app import server, constants
from flask import make_response, request, current_app, redirect, url_for
from flask_cors import CORS, cross_origin
import time
import math
import json
from app.data_managers.places_data_manager import PlaceDataManager
import app.data_managers.places_data_manager as pdm
from app.sentiment.emotion import emotion_data
from app.data_managers.common import search_parameter_to_db_filter


@server.route(rule='/places/template', endpoint='get_place_template', methods=['GET'])
def fetch_place_template():
    return json.dumps(pdm.min_place_dict)


@server.route(rule='/places/create', endpoint='place_create_post', methods=['POST'])
def create_place():
    dm = PlaceDataManager()
    # request should be {'name': 'p1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    dm.insert_one_place(posted_dict)
    return posted_dict


'''replace does not replace ID'''


@server.route(rule='/places/replace', endpoint='replace_place', methods=['POST'])
def replace_one_place():
    dm = PlaceDataManager()
    # request should be {"name": 'e1', 'senti_socre': '5.2' .....}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    place_id = posted_dict['place_id']
    if not place_id.__contains__('pl-'):
        raise Exception('invalid input')
    return dm.replace_one_place(posted_dict)


'''update by a list of diffs '''


@server.route(rule='/places/<string:place_id>/update', endpoint='update_an_place_by_diff', methods=['POST'])
def update_place(place_id: str):
    if not place_id.__contains__('pl-'):
        raise Exception('invalid input')
    dm = PlaceDataManager()
    # update request should be {"updates": [{"key":"some_key", "new_value","some_value"},  ... ]}
    decoded_json = request.get_data().decode("utf-8")
    posted_dict = json.loads(decoded_json)
    updates = posted_dict['updates']
    # each update
    for update in updates:
        key = update['key']
        new_value = update['new_value']
        dm.update_one_place(place_id=place_id, key=key, new_val=new_value)
    return dm.find_one_place_by_id(place_id)


'''listing endpoints'''

'''list one place given ID
/places/pl-WL3AF09tc8EauQdu
'''


@server.route(rule='/places/<string:place_id>', endpoint='get_one_place', methods=['GET'])
def get_one_place(place_id: str):
    return json.dumps(PlaceDataManager().find_one_place_by_id(place_id))


'''
alias for search, should never be passed in without parameters in production
list ALL places - /places/
/places/?name=cake or /places?name=cake
is the same as
/places/search?name=cake
'''


@server.route(rule='/places/', endpoint='list_places', methods=['GET'])
def list_places():
    return search_place()


'''search for places based on a certain criteria
ex.
Search for places whose name is exactly cake factory -  /places/search?name=cake factory
Search for places whose name contains pizza -  /places/search?name_search=pizza
Search for places whose rating is larger than 3.5 - /places/search?score={"$gt":3.5}
Search for places that is not verified - /places/search?verified=false (note the lower case false)
Search for places by multiple criteria /places/search?f1=criteria_1&f2=criteria2
'''


@server.route(rule='/places/search', endpoint='search_place', methods=['GET'])
def search_place():
    filter = search_parameter_to_db_filter(request.args)
    dm = PlaceDataManager()
    print('filtering by' + filter.__str__())
    place_dicts = dm.find_places_by_filter(filter)
    return json.dumps({'places': place_dicts})


if __name__ == '__main__':
    print(time.time())
