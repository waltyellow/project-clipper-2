__author__ = 'navyakandkuri'
from app.data_managers import places_data_manager, event_data_manager
from geojson import Point
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager
import time
from app.test_data import cb_and_sl

def create_cs_presentation(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'CS Capstone Presentations'
    event['geo_coordinates'] = place['geo_coordinates']
    event['location'] = 'Nord'
    event['description'] =  'Free food for CWRU Students'
    event['place_id'] = place['place_id']
    event['senti_score'] = 10
    return event

def create_bio_presentation(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'Bio Capstone Presentations'
    event['geo_coordinates'] = place['geo_coordinates']
    event['location'] = 'Bingham'
    event['description'] =  'Free food for CWRU Students'
    event['place_id'] = place['place_id']
    event['senti_score'] = 8
    return event

def create_basketball_game(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'Basketball Game'
    event['geo_coordinates'] = place['geo_coordinates']
    event['location'] = 'Veale'
    event['description'] =  'Free food for CWRU Students'
    event['place_id'] = place['place_id']
    event['senti_score'] = 4
    return event

def create_lecture(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'Lecture on Internet of Things'
    event['geo_coordinates'] = place['geo_coordinates']
    event['location'] = 'Strosacker'
    event['description'] =  'Free food for CWRU Students'
    event['place_id'] = place['place_id']
    event['senti_score'] = 6
    return event

def create_undergrad(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'Undergrad Appreciation Week'
    event['geo_coordinates'] = place['geo_coordinates']
    event['location'] = 'Tinkham Veale Center'
    event['description'] =  'Free food for CWRU Students'
    event['place_id'] = place['place_id']
    event['senti_score'] = 8
    return event

def create_karaoke(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'Karaoke Night'
    event['geo_coordinates'] = place['geo_coordinates']
    event['location'] = 'Thwing Center'
    event['description'] =  'Come sing songs with your friends!'
    event['place_id'] = place['place_id']
    event['senti_score'] = 5
    return event

def create_campus_buildings_and_events():
    pm = PlaceDataManager()
    yost = cb_and_sl.create_yost()
    strosacker = cb_and_sl.create_strosacker()
    nord = cb_and_sl.create_nord()
    white = cb_and_sl.create_white()
    glennan = cb_and_sl.create_glennan()
    bingham = cb_and_sl.create_bingham()
    tink =cb_and_sl.create_tink()
    thwing = cb_and_sl.create_thwing()
    veale = cb_and_sl.create_veale()
    pm.insert_one_place(yost)
    pm.insert_one_place(strosacker)
    pm.insert_one_place(nord)
    pm.insert_one_place(white)
    pm.insert_one_place(glennan)
    pm.insert_one_place(bingham)
    pm.insert_one_place(tink)
    pm.insert_one_place(veale)

    em = EventDataManager()
    cs_presentation = create_cs_presentation(nord)
    bio_pres = create_bio_presentation(bingham)
    basketball = create_basketball_game(veale)
    lect = create_lecture(strosacker)
    undergrad = create_undergrad(tink)
    karaoke = create_karaoke(thwing)
    em.insert_event_one(cs_presentation)
    em.insert_event_one(bio_pres)
    em.insert_event_one(basketball)
    em.insert_event_one(lect)
    em.insert_event_one(undergrad)
    em.insert_event_one(karaoke)

if __name__ == '__main__':
    create_campus_buildings_and_events()
