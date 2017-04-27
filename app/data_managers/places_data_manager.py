import base64
from typing import Any

from bson.objectid import ObjectId
from pymongo import MongoClient, GEOSPHERE
from app.utility import geo
from geojson import Point
from app.utility import action_handler
import time

min_place_dict = {
    'place_id': '',
    'type': 'place',
    'name': '',
    'rating_count': 0,
    'rating_average': 0,
    'senti_score': 0,
    'senti_score_updated_time': time.time(),
    'mood_tag_counter': {},
    'geo_coordinates': Point((0, 0)),  # in format of geojson.Point((x,y))
    'deleted': False
}

class PlaceDataManager:
    ''' connect to mongo through init
        static methods for database connections
    '''

    def __init__(self):
        self.client = MongoClient('localhost',
                                  27017)  # localhost for now, may change to properties file if time permits
        self.db = self.client.get_database('experimental_2')  # not sure what this is yet, using same as events
        self.place_collection = self.db.get_collection('locations')
        self.place_collection.ensure_index([('geo_coordinates', GEOSPHERE)])

    @staticmethod
    def convert_to_place_id(_id: ObjectId) -> str:
        b64_obj_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        place_id = 'pl-' + b64_obj_id
        return place_id

    @staticmethod
    def convert_to_object_id(place_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(place_id[3:]))

    def validate_place(place_dict: dict):
        for key in min_place_dict:
            if key not in place_dict:
                error_message = 'missing required key ' + key + ' in this place'
                raise ValueError(error_message)
        return True

    def create_empty_place(self) -> dict:
        return min_place_dict

    def insert_one_place(self, place_dict: dict) -> dict:
        self.place_collection.insert_one(place_dict)
        place_dict['place_id'] = PlaceDataManager.convert_to_place_id(place_dict['_id'])
        self.replace_one_place(place_dict)
        print('inserted place' + place_dict['place_id'])
        place_dict['_id'] = str(place_dict['_id'])
        return place_dict

    def replace_one_place(self, place_dict: dict):
        print('replacing place ' + place_dict['place_id'])
        place_dict['_id'] = PlaceDataManager.convert_to_object_id(place_dict['place_id'])
        place_dict['deleted'] = False
        place_dict['type'] = 'place'
        self.place_collection.replace_one({'_id': PlaceDataManager.convert_to_object_id(place_dict['place_id'])}
                                          , place_dict)

    def update_one_place(self, place_id: str, key: str, new_val: Any):
        self.place_collection.update_one({'id': PlaceDataManager.convert_to_object_id(place_id)},
                                         {'$set': {key: new_val}})

    def delete_place(self, place_id: str):
        self.place_collection.update_one({'_id': PlaceDataManager.convert_to_object_id(place_id)},
                                         {'$set': {'deleted': True}})

    def find_one_place_by_id(self, place_id: str) -> dict:
        print('finding place ' + place_id)
        place_dict = self.place_collection.find_one({'_id': PlaceDataManager.convert_to_object_id(place_id)})
        if place_dict is None:
            return None
        elif place_dict['deleted']:
            print(str(place_id) + ' has been deleted')
            return None
        else:
            place_dict['_id'] = str(place_dict['_id'])
            return place_dict

    def find_one_by_filter(self, filter: dict):
        place_dict = self.place_collection.find_one(filter=filter)
        if place_dict is not None:
            place_dict['_id'] = str(place_dict['_id'])
        return place_dict

    def find_places_by_filter(self, filter: dict):
        place_dicts = self.place_collection.find(filter)
        places = []
        for place_dict in place_dicts:
            place_dict['_id'] = str(place_dict['_id'])
            places.append(place_dict)
        return places

    def find_one_place_near(self, long, lat, radius=500):
        return self.find_one_by_filter(
            filter=self.create_geo_filter(lat, long, radius))

    def find_places_near(self, long, lat, radius=500):
        return self.find_places_by_filter(
            filter=self.create_geo_filter(lat, long, radius))

    def find_all_places(self):
        filter = {'deleted': False}
        return self.find_places_by_filter(filter=filter)

    def create_geo_filter(self, lat, long, radius):
        return {'geo_coordinates': geo.get_query_for_coordinates_in_circle(long=long, lat=lat, radius=radius)}


def insert():
    place1 = min_place_dict.copy()
    place1['name'] = 'Tink Food Court'
    place1['geo_coordinates'] = Point((123, 45))
    place1['senti_score'] = 25
    place1['rating_average'] = 4.5
    dm = PlaceDataManager()
    dm.insert_one_place(place1)
    print(place1)


def find():
    dm = PlaceDataManager()
    p = dm.find_one_place_near(110, 30.0000, radius=5000)

    p['senti_score_updated_time'] = time.time() - 86400
    p['senti_score'] = 25
    print(p)
    action_handler.refresh_score_for_entity(p, lifetime_in_days=1)
    print(p)


if __name__ == '__main__':
    insert()
