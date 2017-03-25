from app import server
from flask import make_response, request
from app.data_managers.places_data_manager import PlacesDataManager


@server.route(rule='/place/<string:place_id>/create', endpoint='createPlace')
def create(place_id):
    return PlacesDataManager.create_empty_place(place_id)


@server.route(rule='/place/<string:place_id>/update', endpoint='updatePlace')
def update(place_id):
    j = request.get_json()
    return PlacesDataManager.update_one_place(PlacesDataManager,place_id,j['key'],j['new_val'])


@server.route(rule='/place/search', endpoint='searchPlace')
def search(place_id):
    return PlacesDataManager.find_all_places(PlacesDataManager)


@server.route(rule='/place/<string:place_id>', endpoint='fetchPlace')
def fetch(place_id):
    return PlacesDataManager.find_place(PlacesDataManager,place_id)