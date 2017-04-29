#!/usr/bin/python3

import geojson
import argparse
from geojson import FeatureCollection, Feature
from app.data_managers.event_data_manager import EventDataManager
from app.utility.action_handler import generate_dynamic_score_for_event


def create_feature_collection(events):
    return FeatureCollection(list(map(create_feature, events)))

def create_feature(event):
    generate_dynamic_score_for_event(event)
    return Feature(geometry=event['geo_coordinates'], properties={
        'id': event['event_id'],
        'name': event['name'],
        'location': event['location'],
        'excitement': event['dynamic_senti_score']
    })

parser = argparse.ArgumentParser()
parser.add_argument("dest")
args = parser.parse_args()
edm = EventDataManager()
events = edm.find_all_events()

outfile = open(args.dest, 'w')
outfile.write(create_feature_collection(events).__str__())
