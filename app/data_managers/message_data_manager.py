import pymongo
from pymongo import MongoClient, GEOSPHERE
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
import base64, time
from typing import Any
from app.utility import geo
import geojson

min_message_dict = {
    'message_id': '',
    'body': '',
    'posted': '',
    'parent': '',
    'type': '',
    'username': '',
    'ancestors': [],
    'moodtags': [],
    'timestamp': time.time(),
    'senti_score': 0,
    'geo_coordinates': '',  # geojson.Point(0 ,0)
    'deleted': False
}

message_dict_with_optionals = {
    'message_id': '',
    'body': '',
    'posted': '',
    'parent': '',
    'type': '',
    'username': '',
    'ancestors': [],
    'deleted': False,
    'senti_vector': {},
}


class MessageDataManager:
    '''establish the database and import the collection
        Note: In mongo, the index is "_id: ObjectId", in our system, it is message_id:str
        ObjectId should be completely invisible from other places
    '''

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database('experimental_2')
        self.message_collection = self.db.get_collection('messages')
        # self.message_collection.create_index([("thread_id", pymongo.ASCENDING),
        #                                       ("type", pymongo.ASCENDING)])
        # self.message_collection.create_index([("thread_id", pymongo.ASCENDING))
        self.message_collection.ensure_index([('geo_coordinates', GEOSPHERE)])


    def validate_message(message_dict: dict):
        for key in min_message_dict:
            if key not in message_dict:
                error_message = 'missing required key ' + key + ' in this message'
                raise ValueError(error_message)
        return True

    @staticmethod
    def convert_to_message_id(_id: ObjectId) -> str:
        message_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        message_id = 'ms-' + message_id
        return message_id

    @staticmethod
    def convert_to_object_id(message_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(message_id[3:]))

    def create_empty_message_without_id(self) -> dict:

        return min_message_dict

    '''inserts an message, updates the message's _id and message_id and returns the object'''

    def insert_message_one(self, message_dict: dict) -> dict:

        self.message_collection.insert_one(message_dict)
        message_dict['message_id'] = MessageDataManager.convert_to_message_id(message_dict['_id'])
        self.replace_one_message(message_dict)
        print('inserted message' + message_dict['message_id'])
        message_dict['_id'] = str(message_dict['_id'])
        return message_dict

    '''finds an message by its message id'''

    def find_message_by_id(self, message_id: str) -> dict:
        print('finding message' + message_id)
        message_dict = self.message_collection.find_one({'_id': MessageDataManager.convert_to_object_id(message_id)})
        if message_dict is None:
            return None
        if message_dict['deleted']:
            print(str(message_id) + ' has been deleted')
            return None
        message_dict['_id'] = str(message_dict['_id'])
        return message_dict

    def find_messages_by_filter(self, filter) -> [dict]:
        message_dicts_cursor = self.message_collection.find(filter)
        message_dicts = []
        for message_dict in message_dicts_cursor:
            message_dict['_id'] = str(message_dict['_id'])
            message_dicts.append(message_dict)
        return message_dicts

    def find_all_messages(self) -> [dict]:
        return self.find_messages_by_filter({})

    def find_messages_near(self, long, lat, radius=500):
        return self.find_messages_by_filter(
            filter={'geo_coordinates': geo.get_query_for_coordinates_in_circle(long=long, lat=lat, radius=radius)})

    def find_all_messages_for_parent(self, parent_id) -> [dict]:
        message_dicts_cursor = self.message_collection.find({'parent': parent_id})
        message_dicts = []
        for message_dict in message_dicts_cursor:
            message_dict['_id'] = str(message_dict['_id'])
            message_dicts.append(message_dict)
        return message_dicts

    '''re-inserts an message and replaces it'''

    def replace_one_message(self, message_dict: dict):
        print('replacing message' + message_dict['message_id'])
        message_dict['_id'] = MessageDataManager.convert_to_object_id(message_dict['message_id'])
        self.message_collection.replace_one(
            {'_id': MessageDataManager.convert_to_object_id(message_dict['message_id'])},
            message_dict)

    '''updates one key of the message by message_id'''

    def update_one_message_by_diff(self, message_id: str, key: str, new_value: Any):
        self.message_collection.update_one({'_id': MessageDataManager.convert_to_object_id(message_id)},
                                           {'$set': {key: new_value}})

    '''deletes an message by message_id'''

    def delete_message_by_id(self, message_id: str):
        self.message_collection.update_one({'_id': MessageDataManager.convert_to_object_id(message_id)},
                                           {'$set': {'deleted': True}})


def test():
    messageDataManager = MessageDataManager()
    newMessage = messageDataManager.create_empty_message_without_id()
    print(newMessage)
    newMessage['name'] = 'placeholder'
    print(newMessage)
    messageDataManager.insert_message_one(newMessage)
    founded_message = messageDataManager.find_message_by_id(str(newMessage['message_id']))
    print(founded_message)
    founded_message['parent'] = 'ms-WL9vBU9tc-5k93Yt'  # update name
    messageDataManager.replace_one_message(founded_message)
    print(founded_message)
    messageDataManager.update_one_message_by_diff(founded_message['message_id'], 'name', 'pl4')
    # messageDataManager.delete_message_by_id(str(newMessage.message_id))
    messageDataManager.find_message_by_id(str(newMessage['message_id']))
    es = messageDataManager.find_all_messages()
    for e in es:
        print(e)


def test2():
    # _id = ObjectId('58bd00034f6d73ae4811b7f5')
    # print(_id.binary)
    # message_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
    # print(str(message_id))
    # bi = base64.urlsafe_b64decode(message_id)
    # print(bi)
    # print('ev-WL2wUk9tc7v2hxKG'[3:])
    messageDataManager = MessageDataManager()
    es = messageDataManager.find_all_messages()


if __name__ == '__main__':
    test()
