#!/usr/bin/python3

import geojson
from geojson import FeatureCollection, Feature
from app.data_managers.event_data_manager import EventDataManager


def create_feature_collection(events):
    return FeatureCollection(list(map(create_feature, events)))

def create_feature(event):
    return Feature(geometry=event['geo_coordinates'], properties={
        'id': event['event_id'],
        'name': event['name'],
        'location': event['location'],
        'excitement': event['senti_score']
    })

edm = EventDataManager()
events = edm.find_all_events()
print(create_feature_collection(events))
