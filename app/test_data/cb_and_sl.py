__author__ = 'navyakandkuri'
__author__ = 'navyakandkuri'
from app.data_managers import places_data_manager, event_data_manager
from geojson import Point
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager
import time

'''campus buildings'''
def create_yost():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Yost Hall'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.608950, 41.503553))
    place['senti_score'] = -3.55
    place['rating_average'] = 3.9
    place['rating_count'] = 21
    return place

def create_strosacker():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Strosacker Auditorium'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.607330, 41.503304))
    place['senti_score'] = 8
    place['rating_average'] = 4.1
    place['rating_count'] = 18
    return place

def create_nord():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Nord Hall'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.607824, 41.502485))
    place['senti_score'] = 8.66
    place['rating_average'] = 4.7
    place['rating_count'] = 43
    return place

def create_white():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'White Building'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.607416, 41.501922))
    place['senti_score'] = 4.20
    place['rating_average'] = 2.6
    place['rating_count'] = 33
    return place

def create_glennan():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Glennan Student Building'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.606998, 41.501553))
    place['senti_score'] = 5
    place['rating_average'] = 3.7
    place['rating_count'] = 42
    return place

def create_bingham():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Bingham Hall'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.606955, 41.502412))
    place['senti_score'] = -1
    place['rating_average'] = 4
    place['rating_count'] = 61
    return place

def create_tink():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Tinkham Veale University Center'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.608752, 41.508473))
    place['senti_score'] = 4
    place['rating_average'] = 4
    place['rating_count'] = 83
    return place


def create_thwing():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Thwing Student Center'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.608199, 41.507386))
    place['senti_score'] = 6
    place['rating_average'] = 4
    place['rating_count'] = 14
    return place


def create_veale():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Veale Athletic Center'
    place['type'] = 'CampusBuilding'
    place['geo_coordinates'] = Point((-81.606295, 41.500936))
    place['senti_score'] = 7
    place['rating_average'] = 4
    place['rating_count'] = 45
    return place

'''study locations'''
def create_ksl():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Kelvin Smith Library'
    place['type'] = 'StudyLocation'
    place['geo_coordinates'] = Point((-81.609578, 41.507348))
    place['senti_score'] = -9
    place['rating_average'] = 4.1
    place['rating_count'] = 20
    return place

def create_glennan_lounge():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Glennan Lounge'
    place['type'] = 'StudyLocation'
    place['geo_coordinates'] = Point((-81.606998, 41.501553))
    place['senti_score'] = 1
    place['rating_average'] = 3
    place['rating_count'] = 42
    return place

def create_bingham_lounge():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Bingham Lounge'
    place['type'] = 'StudyLocation'
    place['geo_coordinates'] = Point((-81.606955, 41.502412))
    place['senti_score'] = 7
    place['rating_average'] = 3
    place['rating_count'] = 81
    return place

def create_wade_commons():

    proto = places_data_manager.min_place_dict

    place = proto.copy()
    place['name'] = 'Wade Commons'
    place['type'] = 'StudyLocation'
    place['geo_coordinates'] = Point((-81.605211, 41.513051))
    place['senti_score'] = 12
    place['rating_average'] = 2
    place['rating_count'] = 17
    return place

def create_all_cb_and_sl():
    pm = PlaceDataManager()
    yost = create_yost()
    strosacker = create_strosacker()
    nord = create_nord()
    white = create_white()
    glennan = create_glennan()
    bingham = create_bingham()
    tink =create_tink()
    thwing = create_thwing()
    veale = create_veale()
    pm.insert_one_place(yost)
    pm.insert_one_place(strosacker)
    pm.insert_one_place(nord)
    pm.insert_one_place(white)
    pm.insert_one_place(glennan)
    pm.insert_one_place(bingham)
    pm.insert_one_place(tink)
    pm.insert_one_place(veale)
    ksl = create_ksl()
    glennan_lounge = create_glennan_lounge()
    b_lounge = create_bingham_lounge()
    wade = create_wade_commons()
    pm.insert_one_place(ksl)
    pm.insert_one_place(glennan_lounge)
    pm.insert_one_place(b_lounge)
    pm.insert_one_place(wade)

if __name__ == '__main__':
    create_all_cb_and_sl()
