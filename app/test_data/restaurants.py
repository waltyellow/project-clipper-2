__author__ = 'navyakandkuri'
from app.data_managers import places_data_manager, event_data_manager
from geojson import Point
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager
import time

def create_qdoba():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Qdoba Mexican Grill'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.605453, 41.508404))
    place['senti_score'] = 12
    place['rating_average'] = 3.9
    place['rating_count'] = 20
    return place

def create_jimmy_johns():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Jimmy Johns Sub Shop'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.603951, 41.509651))
    place['senti_score'] = -3
    place['rating_average'] = 4.1
    place['rating_count'] = 16
    return place

def create_chipotle():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Chipotle Mexican Grill'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.603951, 41.509799))
    place['senti_score'] = -20
    place['rating_average'] = 1.7
    place['rating_count'] = 52
    return place

def create_potbelly():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Potbelly Sandwich Shop'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.604890, 41.509554))
    place['senti_score'] = 10
    place['rating_average'] = 2.6
    place['rating_count'] = 26
    return place

def create_panera_bread():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Panera Bread'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.603854, 41.509765))
    place['senti_score'] = 2.87
    place['rating_average'] = 3.7
    place['rating_count'] = 61
    return place

def create_kenkos():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Kenkos Sushi'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.605740, 41.508316))
    place['senti_score'] = -2
    place['rating_average'] = 4
    place['rating_count'] = 11
    return place


def create_chipotle2():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Chipotle Mexican Grill at Coventry'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.591951, 41.509799))
    place['senti_score'] = 4.51
    place['rating_average'] = 4.1
    place['rating_count'] = 52
    return place

def create_pacific_east():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Pacific East Coventry'
    place['type'] = 'FoodEntertainment'
    place['geo_coordinates'] = Point((-81.591951, 41.509929))
    place['senti_score'] = 7.5
    place['rating_average'] = 4.4
    place['rating_count'] = 52
    return place

def create_all_restaurants():
    pm = PlaceDataManager()
    qdoba = create_qdoba()
    potbelly = create_potbelly()
    jimmyjohns = create_jimmy_johns()
    kenkos = create_kenkos()
    panera = create_panera_bread()
    chipotle = create_chipotle()
    pm.insert_one_place(qdoba)
    pm.insert_one_place(potbelly)
    pm.insert_one_place(jimmyjohns)
    pm.insert_one_place(kenkos)
    pm.insert_one_place(panera)
    pm.insert_one_place(chipotle)
    pm.insert_one_place(create_chipotle2())
    pm.insert_one_place(create_pacific_east())



if __name__ == '__main__':
    create_all_restaurants()
