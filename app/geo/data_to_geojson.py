#!/usr/bin/python3

import geojson
from geojson import FeatureCollection, Feature, Point
from app.data_managers.event_data_manager import EventDataManager


def create_feature_collection(events):
    return FeatureCollection(list(map(create_feature, events)))

def create_feature(event):
    coords = event.coords
    pt = Point((coords['long'], coords['lat']))
    return Feature(geometry=pt, properties={'id': event.event_id})

edm = EventDataManager()
events = edm.find_all_events()
print(create_feature_collection(events))
