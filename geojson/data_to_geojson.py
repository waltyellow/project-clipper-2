#!/usr/bin/python3

import geojson
from geojson import FeatureCollection, Feature, Point

def create_feature_collection(lat, lon, ev_id):
    return FeatureCollection([create_feature(lat, lon, ev_id)])

def create_feature(lat, lon, ev_id):
    pt = Point((lat, lon))
    return Feature(geometry=pt, properties={'id': ev_id})

print(geojson.dumps(create_feature_collection(-81.6944, 41.4933, 'ev-56'), sort_keys=True))