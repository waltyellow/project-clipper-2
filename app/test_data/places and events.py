from app.data_managers import places_data_manager, event_data_manager
from geojson import Point
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager

def create_place1():

    proto = places_data_manager.min_place_dict

    place1 = proto.copy()
    place1['name'] = 'Tinkham Veale University Center'
    place1['geo_coordinates'] = Point((123, 45.002))
    place1['senti_score'] = 25
    place1['rating_average'] = 4.5
    return place1


def create_place2():
    proto = places_data_manager.min_place_dict
    place2 = proto.copy()
    place2['name'] = 'Tomlinson Food Court'
    place2['geo_coordinates'] = Point((123, 45))
    place2['senti_score'] = 7
    place2['rating_average'] = 3.26
    return place2


def create_place3():
    proto = places_data_manager.min_place_dict
    place3 = proto.copy()
    place3['name'] = 'White Building'
    place3['geo_coordinates'] = Point((123, 45.2))
    place3['senti_score'] = 400
    place3['rating_average'] = 0
    return place3

def create_place4():
    proto = places_data_manager.min_place_dict
    place4 = proto.copy()
    place4['name'] = 'Weatherhead School'
    place4['geo_coordinates'] = Point((123, 45.12))
    place4['senti_score'] = 1
    place4['rating_average'] = 4.8
    return place4

# insert those things here first so we get ids


def create_event_1(place):
    proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    event = proto.copy()
    event['name'] = 'Tomlinson food week'
    event['geo_coordinates'] = Point((123, 45))
    event['location'] = 'Tomlinson'
    event['place_id'] = place['place_id']
    event['senti_score'] = 7
    return event


def create_event_2(place):
    proto = places_data_manager.min_place_dict
    event = proto.copy()
    event['name'] = 'Computer Science Senior Project Presentations'
    event['geo_coordinates'] = Point((123, 45))
    event['location'] = 'White'
    event['place_id'] = place['place_id']
    event['senti_score'] = 500
    return event


def create_event_3(place):
    proto = places_data_manager.min_place_dict
    event = proto.copy()
    event['name'] = 'Senior Capstone Presentations of Operation Management'
    event['geo_coordinates'] = Point((123, 45))
    event['location'] = 'Weatherhead'
    event['place_id'] = place['place_id']
    event['senti_score'] = 3
    return event

def insert_events_and_places():
    #create data managers
    em = EventDataManager()
    pm = PlaceDataManager()

    #create places
    tink = create_place1()
    tomlinson = create_place2()
    white = create_place3()
    weatherhead = create_place4()

    #insert places into database
    pm.insert_one_place(tomlinson)
    pm.insert_one_place(tink)
    pm.insert_one_place(white)
    pm.insert_one_place(weatherhead)

    #create events
    food = create_event_1(tomlinson)
    presentation_cs = create_event_2(white)
    presentation_om = create_event_3(weatherhead)

    #insert events
    em.insert_event_one(food)
    em.insert_event_one(presentation_cs)
    em.insert_event_one(presentation_om)



if __name__ == '__main__':
    insert_events_and_places()