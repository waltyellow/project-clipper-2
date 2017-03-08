import pymongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from app.models.event import Location
import base64
from typing import Any

class FoodDataManager:
    ''' connect to mongo through init
        static methods for database connections
    '''

    def __init__(self):
        self.client = MongoClient('localhost',27017) #localhost for now, may change to properties file if time permits
        self.db = self.client.get_database('experimental1_2') #not sure what this is yet, using same as events
        self.food_collection = self.db.get_collection('locations')


    @staticmethod
    def convert_to_food_id(_id: ObjectId) -> str:
        b64_obj_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        food_id = 'fe-' + b64_obj_id
        return food_id


    @staticmethod
    def convert_to_object_id(food_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(food_id[3:]))


    def create_empty_food(self):
        food_dict = Location().__dict__
        food_dict['deleted']=False
        food_dict['type'] = 'food'
        return Location()


    def insert_one_food(self, food: Location) -> Location:
        food_dict = food.__dict__
        food_dict['deleted'] = False
        food_dict['type'] = 'food'
        self.food_collection.insert_one(food_dict)
        food.food_id = FoodDataManager.convert_to_food_id(food_dict['_id'])
        self.replace_one_food(food)
        print('inserted food ' + food.food_id)
        return food


    def replace_one_food(self, food: Location):
        print('replacing food ' + food.food_id)
        food_dict = food.__dict__
        food_dict['deleted'] = False
        food_dict['type'] = 'food'
        self.food_collection.replace_one({'_id': FoodDataManager.convert_to_object_id(food.food_id)},food_dict)


    def update_one_food(self, food_id: str, key: str, new_val: Any):
        self.food_collection.update_one({'id': FoodDataManager.convert_to_object_id(food_id)},{'$set':{key: new_value}})


    def delete_food(self, food_id: str):
        self.food_collection.update_one({'_id': FoodDataManager.convert_to_object_id(food_id)},{'$set':{'deleted': True}})


    def find_food(self, food_id: str):
        print('finding food ' + food_id)
        food_dict = self.food_collection.find_one({'_id':FoodDataManager.convert_to_object_id(food_id)})
        if food_dict is None:
            return None
        elif food_dict['deleted']:
            print(str(food_id) + ' has been deleted')
            return None
        else:
            return Location.location_from_dict(food_dict)


    def find_all_food(self):
        food_dicts = self.food_collection.find({'type':'food'})
        foods = []
        for food_dict in food_dicts:
            foods.append(Location.location_from_dict(food_dict))
        return foods