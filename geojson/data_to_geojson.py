#!/usr/bin/python3

from geojson import FeatureCollection, Feature, Point

def create_feature(lat, lon, ev_id):
    pt = Point((lat, lon))
    return Feature(geometry=pt, properties={'id': ev_id})
