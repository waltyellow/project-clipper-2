import pymongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from app.models.user import User
import base64
from typing import Any

class UserDataManager:

    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.db = self.client.get_database('experimental_2')
        self.user_collection = self.db.get_collection('users')

        def create_new_user(self, fb_id : str):
            user_dict = User().__dict__
            user_dict['fb_id'] = fb_id
            return User()

        def insert_user(self,user:User) -> User:
            user_dict = user.__dict__
            self.user_collection.insert_one(user_dict)
            print('inserted user ' + user.fb_id)
            return user

        def find_user(self,, fb_id: str):
            print('finding user' + fb_id)
            user_dict = self.user_collection.find_one({'fb_id':fb_id})
            if user_dict is None:
                return None
            return User.user_from_dict(user_dict)

