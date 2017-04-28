from app.data_managers import places_data_manager, event_data_manager
from geojson import Point
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager
import time

def insert():
    place_proto = places_data_manager.min_place_dict
    event_proto = event_data_manager.min_event_dict

    white = place_proto.copy()
    white['name'] = 'White Building at CWRU'
    white['senti_score'] = 8
    white['rating_average'] = 2.8
    white['rating_count'] = 6
    white['geo_coordinates'] = Point((100.003, 10))

    tink = place_proto.copy()
    tink['name'] = 'Tinkham Veale University Center'
    tink['senti_score'] = 2
    tink['rating_average'] = 4.20
    tink['rating_count'] = 7
    tink['geo_coordinates'] = Point((100.001, 10.001))

    tomlinson = place_proto.copy()
    tomlinson['name'] = 'Tomlinson Food Court'
    tomlinson['senti_score'] = -6
    tomlinson['rating_average'] = 2.1
    tomlinson['rating_count'] = 12
    tomlinson['geo_coordinates'] = Point((100.002, 10))

    melt = place_proto.copy()
    melt['name'] = 'Melt University'
    melt['senti_score'] = 2
    melt['rating_average'] = 0
    melt['rating_count'] = 0
    melt['geo_coordinates'] = Point((100.0011, 10.001))

    pdm = PlaceDataManager()
    edm = EventDataManager()
    pdm.insert_one_place(white)
    pdm.insert_one_place(tink)
    pdm.insert_one_place(tomlinson)
    pdm.insert_one_place(melt)


    ece = event_proto.copy()
    ece['name'] = 'Electrical and computer engineering senior project presentations'
    ece['description'] = 'People from the EE and CE departments presenting their stuff'
    ece['senti_score'] = 2
    ece['place_id'] = white['place_id']
    ece['location'] = 'white'
    ece['geo_coordinates'] = Point((100.003, 10.0003))

    cmp = event_proto.copy()
    cmp['name'] = 'Computer science senior project presentations Day 2'
    cmp['description'] = 'our project, Evention is presenting at this event'
    cmp['senti_score'] = 15
    cmp['place_id'] = white['place_id']
    cmp['location'] = 'white'
    cmp['geo_coordinates'] = Point((100.0032, 10.0001))

    food_week = event_proto.copy()
    food_week['name'] = 'Bon Appetit International Week Gourmet and Wine Tasting'
    food_week[
        'description'] = 'Enjoy great food from Bon Appetit that comes from all over' \
                         ' the world. Absolutely amazing food. Note that Meal swipes ' \
                         'cannot be used to enjoy this food.'
    food_week['senti_score'] = -7
    food_week['place_id'] = tomlinson['place_id']
    food_week['location'] = 'Tomlinson'
    food_week['geo_coordinates'] = Point((100.0021, 10.0004))

    edm.insert_event_one(ece)
    edm.insert_event_one(cmp)
    edm.insert_event_one(food_week)

if __name__ == '__main__':
    insert()