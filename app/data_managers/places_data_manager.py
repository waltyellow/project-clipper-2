import pymongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from app.models.places import Places
import base64
from typing import Any

class PlacesDataManager:
    ''' connect to mongo through init
        static methods for database connections
    '''

    def __init__(self):
        self.client = MongoClient('localhost',27017) #localhost for now, may change to properties file if time permits
        self.db = self.client.get_database('experimental1_2') #not sure what this is yet, using same as events
        self.place_collection = self.db.get_collection('locations')


    @staticmethod
    def convert_to_place_id(_id: ObjectId) -> str:
        b64_obj_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        place_id = 'pl-' + b64_obj_id
        return place_id


    @staticmethod
    def convert_to_object_id(place_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(place_id[3:]))


    def create_empty_place(self, place_id: str):
        place_dict = Places().__dict__
        place_dict['ObjectId']= PlacesDataManager.convert_to_object_id(place_id)
        place_dict['deleted']=False
        place_dict['type'] = 'place'
        return Places()


    def insert_one_place(self, place: Places) -> Places:
        place_dict = place.__dict__
        place_dict['deleted'] = False
        place_dict['type'] = 'place'
        self.place_collection.insert_one(place_dict)
        place.place_id = PlacesDataManager.convert_to_place_id(place_dict['_id'])
        self.replace_one_place(place)
        print('inserted place ' + place.place_id)
        return place


    def replace_one_place(self, place: Places):
        print('replacing place ' + place.place_id)
        place_dict = place.__dict__
        place_dict['deleted'] = False
        place_dict['type'] = 'place'
        self.place_collection.replace_one({'_id': PlacesDataManager.convert_to_object_id(place.place_id)},place_dict)


    def update_one_place(self, place_id: str, key: str, new_val: Any):
        self.place_collection.update_one({'id': PlacesDataManager.convert_to_object_id(place_id)},{'$set':{key: new_val}})


    def delete_place(self, place_id: str):
        self.place_collection.update_one({'_id': PlacesDataManager.convert_to_object_id(place_id)},{'$set':{'deleted': True}})


    def find_place(self, place_id: str):
        print('finding place ' + place_id)
        place_dict = self.place_collection.find_one({'_id':PlacesDataManager.convert_to_object_id(place_id)})
        if place_dict is None:
            return None
        elif place_dict['deleted']:
            print(str(place_id) + ' has been deleted')
            return None
        else:
            return Places.location_from_dict(place_dict)


    def find_all_places(self):
        place_dicts = self.place_collection.find({'type':'place'})
        places = []
        for place_dict in place_dicts:
            places.append(Places.location_from_dict(place_dict))
        return places