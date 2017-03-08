import pymongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from app.models.message import Message
import base64
from typing import Any


class MessageDataManager:
    '''establish the database and import the collection
        Note: In mongo, the index is "_id: ObjectId", in our system, it is message_id:str
        ObjectId should be completely invisible from other places
    '''

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database('experimental_2')
        self.message_collection = self.db.get_collection('messages')
        self.message_collection.create_index([("thread_id", pymongo.ASCENDING),
                                              ("type", pymongo.ASCENDING)])
        self.message_collection.create_index([("thread_id", pymongo.ASCENDING))

    @staticmethod
    def validate_message(message):
        return True

    @staticmethod
    def convert_to_message_id(_id: ObjectId) -> str:
        message_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        message_id = 'ev-'+message_id
        return message_id

    @staticmethod
    def convert_to_object_id(message_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(message_id[3:]))


    def create_empty_message_without_id(self):
        message_dict = Message().__dict__
        message_dict['deleted'] = False
        return Message()

    '''inserts an message, updates the message's _id and message_id and returns the object'''

    def insert_message_one(self, message: Message) -> Message:

        message_dict = message.__dict__
        message_dict['deleted'] = False
        self.message_collection.insert_one(message_dict)
        message.message_id = MessageDataManager.convert_to_message_id(message_dict['_id'])
        self.replace_one_message(message)
        print('inserted message' + message.message_id)
        return message

    '''finds an message by its message id'''

    def find_message_by_id(self, message_id: str):
        print('finding message' + message_id)
        message_dict = self.message_collection.find_one({'_id': MessageDataManager.convert_to_object_id(message_id)})
        if message_dict is None:
            return None
        if message_dict['deleted']:
            print(str(message_id) + ' has been deleted')
            return None
        return Message.message_from_dict(message_dict)

    def find_all_messages(self):
        message_dicts = self.message_collection.find({})
        messages = []
        for message_dict in message_dicts:
            messages.append(Message.message_from_dict(message_dict))
        return messages


    '''re-inserts an message and replaces it'''

    def replace_one_message(self, message: Message):
        print('replacing message' + message.message_id)
        message_dict = message.__dict__
        message_dict['deleted'] = False
        self.message_collection.replace_one({'_id': MessageDataManager.convert_to_object_id(message.message_id)}, message_dict)

    '''updates one key of the message by message_id'''

    def update_one_message_by_diff(self, message_id: str, key: str, new_value: Any):
        self.message_collection.update_one({'_id': MessageDataManager.convert_to_object_id(message_id)}, {'$set': {key: new_value}})

    '''deletes an message by message_id'''

    def delete_message_by_id(self, message_id: str):
        self.message_collection.update_one({'_id': MessageDataManager.convert_to_object_id(message_id)}, {'$set': {'deleted': True}})


def test():
    messageDataManager = MessageDataManager()
    newMessage = Message()
    print(newMessage)
    newMessage.name = 'placeholder'
    print(newMessage)
    messageDataManager.insert_message_one(newMessage)
    founded_message = messageDataManager.find_message_by_id(str(newMessage.message_id))
    print(founded_message)
    founded_message.name = 'plc' #update name
    messageDataManager.replace_one_message(founded_message)
    print(founded_message)
    messageDataManager.update_one_message_by_diff(founded_message.message_id,'name','pl4')
    #messageDataManager.delete_message_by_id(str(newMessage.message_id))
    messageDataManager.find_message_by_id(str(newMessage.message_id))
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
