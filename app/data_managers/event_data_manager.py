import pymongo
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from app.models.event import Event
import base64
from typing import Any


class EventDataManager:
    '''establish the database and import the collection
        Note: In mongo, the index is "_id: ObjectId", in our system, it is event_id:str
        ObjectId should be completely invisible from other places
    '''

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database('experimental_2')
        self.event_collection = self.db.get_collection('events')

    @staticmethod
    def validate_event(event):
        return True

    @staticmethod
    def convert_to_event_id(_id: ObjectId) -> str:
        event_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        event_id = 'ev-'+event_id
        return event_id

    @staticmethod
    def convert_to_object_id(event_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(event_id[3:]))


    def create_empty_event_without_id(self):
        event_dict = Event().__dict__
        event_dict['deleted'] = False
        return Event()

    '''inserts an event, updates the event's _id and event_id and returns the object'''

    def insert_event_one(self, event: Event) -> Event:

        event_dict = event.__dict__
        event_dict['deleted'] = False
        self.event_collection.insert_one(event_dict)
        event.event_id = EventDataManager.convert_to_event_id(event_dict['_id'])
        self.replace_one_event(event)
        print('inserted event' + event.event_id)
        return event

    '''finds an event by its event id'''

    def find_event_by_id(self, event_id: str):
        print('finding event' + event_id)
        event_dict = self.event_collection.find_one({'_id': EventDataManager.convert_to_object_id(event_id)})
        if event_dict is None:
            return None
        if event_dict['deleted']:
            print(str(event_id) + ' has been deleted')
            return None
        return Event.event_from_dict(event_dict)

    def find_all_events(self):
        event_dicts = self.event_collection.find({})
        events = []
        for event_dict in event_dicts:
            events.append(Event.event_from_dict(event_dict))
        return events


    '''re-inserts an event and replaces it'''

    def replace_one_event(self, event: Event):
        print('replacing event' + event.event_id)
        event_dict = event.__dict__
        event_dict['deleted'] = False
        self.event_collection.replace_one({'_id': EventDataManager.convert_to_object_id(event.event_id)}, event_dict)

    '''updates one key of the event by event_id'''

    def update_one_event_by_diff(self, event_id: str, key: str, new_value: Any):
        self.event_collection.update_one({'_id': EventDataManager.convert_to_object_id(event_id)}, {'$set': {key: new_value}})

    '''deletes an event by event_id'''

    def delete_event_by_id(self, event_id: str):
        self.event_collection.update_one({'_id': EventDataManager.convert_to_object_id(event_id)}, {'$set': {'deleted': True}})


def test():
    eventDataManager = EventDataManager()
    newEvent = Event()
    print(newEvent)
    newEvent.name = 'placeholder'
    print(newEvent)
    eventDataManager.insert_event_one(newEvent)
    founded_event = eventDataManager.find_event_by_id(str(newEvent.event_id))
    print(founded_event)
    founded_event.name = 'plc' #update name
    eventDataManager.replace_one_event(founded_event)
    print(founded_event)
    eventDataManager.update_one_event_by_diff(founded_event.event_id,'name','pl4')
    #eventDataManager.delete_event_by_id(str(newEvent.event_id))
    eventDataManager.find_event_by_id(str(newEvent.event_id))
    es = eventDataManager.find_all_events()
    for e in es:
        print(e)

def test2():
    # _id = ObjectId('58bd00034f6d73ae4811b7f5')
    # print(_id.binary)
    # event_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
    # print(str(event_id))
    # bi = base64.urlsafe_b64decode(event_id)
    # print(bi)
    # print('ev-WL2wUk9tc7v2hxKG'[3:])
    eventDataManager = EventDataManager()
    es = eventDataManager.find_all_events()




if __name__ == '__main__':
    test()
