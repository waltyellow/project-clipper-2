import base64
from typing import Any

from bson.objectid import ObjectId
from pymongo import MongoClient, IndexModel, GEOSPHERE
from geojson import Point
from app.utility import geo
import time

min_event_dict = {
    'event_id': '',
    'keywords': [],
    'mood_tag_counter': {},
    'name': '',
    'description': '',
    'deleted': False,
    'location': '',
    'geo_coordinates': Point((0, 0)),  # in format of geojson.Point((x,y))
    'place_id': '',
    'senti_score': 0,
    'senti_score_updated_time': time.time(),
    'dynamic_senti_score': 0 # dynamic_senti_score is the senti_score given contexts like where it is happening
}


class EventDataManager:
    '''establish the database and import the collection
        Note: In mongo, the index is "_id: ObjectId", in our system, it is event_id:str
        ObjectId should be completely invisible from other places
    '''

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database('experimental_2')
        self.event_collection = self.db.get_collection('events')
        self.event_collection.ensure_index([('geo_coordinates', GEOSPHERE)])

    @staticmethod
    def validate_event(event_dict: dict) -> bool:
        for key in min_event_dict:
            if key not in event_dict:
                error_message = 'missing required key ' + key + ' in this event'
                raise ValueError(error_message)
        return True

    @staticmethod
    def convert_to_event_id(_id: ObjectId) -> str:
        event_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
        event_id = 'ev-' + event_id
        return event_id

    @staticmethod
    def convert_to_object_id(event_id: str) -> ObjectId:
        return ObjectId(base64.urlsafe_b64decode(event_id[3:]))

    def create_empty_event(self) -> dict:
        return min_event_dict

    '''inserts an event, updates the event's _id and event_id and returns the object'''

    def insert_event_one(self, event_dict: dict) -> dict:

        event_dict['deleted'] = False
        self.event_collection.insert_one(event_dict)
        event_dict['event_id'] = EventDataManager.convert_to_event_id(event_dict['_id'])
        self.replace_one_event(event_dict)
        print('inserted event' + event_dict['event_id'])
        return event_dict

    '''finds an event by its event id'''

    def find_event_by_id(self, event_id: str) -> dict:
        print('finding event' + event_id)
        event_dict = self.event_collection.find_one({'_id': EventDataManager.convert_to_object_id(event_id)})
        if event_dict is None:
            return None
        if event_dict['deleted']:
            print(str(event_id) + ' has been deleted')
            return None
        event_dict.pop('_id')
        return event_dict

    def find_one_event_by_filter(self, filter: dict) -> [dict]:
        event_dict = self.event_collection.find_one(filter)
        event_dict.pop('_id')
        return event_dict

    def find_events_by_filter(self, filter: dict) -> [dict]:
        event_dicts = self.event_collection.find(filter)
        event_dicts_output = []
        for event_dict in event_dicts:
            event_dict.pop('_id')
            event_dicts_output.append(event_dict)
        return event_dicts_output

    def find_one_event_near(self, long, lat, radius=500):
        return self.find_one_event_by_filter(
            filter=self.create_geo_filter(lat, long, radius))

    def find_events_near(self, long, lat, radius=500):
        return self.find_events_by_filter(
            filter=self.create_geo_filter(lat, long, radius))

    def find_all_events(self) -> [dict]:
        return self.find_events_by_filter({})

    '''re-inserts an event and replaces it'''

    def replace_one_event(self, event_dict: dict):
        print('replacing event' + str(event_dict['event_id']))
        event_dict['deleted'] = False
        self.event_collection.replace_one({'_id': EventDataManager.convert_to_object_id(event_dict['event_id'])},
                                          event_dict)

    '''updates one key of the event by event_id'''

    def update_one_event_by_diff(self, event_id: str, key: str, new_value: Any):
        self.event_collection.update_one({'_id': EventDataManager.convert_to_object_id(event_id)},
                                         {'$set': {key: new_value}})

    '''deletes an event by event_id'''

    def delete_event_by_id(self, event_id: str):
        self.event_collection.update_one({'_id': EventDataManager.convert_to_object_id(event_id)},
                                         {'$set': {'deleted': True}})

    def create_geo_filter(self, lat, long, radius):
        return {'geo_coordinates': geo.get_query_for_coordinates_in_circle(long=long, lat=lat, radius=radius)}


'''TESTING SECTION'''

'''insert 3 events'''


def insert():
    event1 = min_event_dict.copy()
    event1['name'] = 'ev1'
    event1['geo_coordinates'] = Point((125, 30))
    event2 = min_event_dict.copy()
    event2['name'] = 'ev2'
    event2['geo_coordinates'] = Point((125, 30.00002))
    event3 = min_event_dict.copy()
    event3['name'] = 'ev3'
    event3['geo_coordinates'] = Point((125, 35))
    dm = EventDataManager()
    dm.insert_event_one(event1)
    dm.insert_event_one(event2)
    dm.insert_event_one(event3)
    print(event1)


'''play with find'''


def find():
    eventDataManager = EventDataManager()
    events = eventDataManager.find_events_near(125, 35.0000, radius=5)
    events = eventDataManager.find_event_by_id('ev-WQEHXE9tc1py6OPs')
    print(events)


def test2():
    # _id = ObjectId('58bd00034f6d73ae4811b7f5')
    # print(_id.binary)
    # event_id = base64.urlsafe_b64encode(_id.binary).decode("utf-8")
    # print(str(event_id))
    # bi = base64.urlsafe_b64decode(event_id)
    # print(bi)
    # print('ev-WL2wUk9tc7v2hxKG'[3:])
    eventDataManager = EventDataManager()
    es = eventDataManager.find_event_by_id('ev-WQEHXE9tc1py6OPs')


if __name__ == '__main__':
    find()
