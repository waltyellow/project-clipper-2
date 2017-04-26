from app.data_managers import places_data_manager, event_data_manager
from geojson import Point

proto = places_data_manager.min_place_dict

place1 = proto.copy()
place1['name'] = 'Tinkham Veale University Center'
place1['geo_coordinates'] = Point((123, 45.002))
place1['senti_score'] = 25
place1['rating_average'] = 4.5

place2 = proto.copy()
place2['name'] = 'Tomlinson Food Court'
place2['geo_coordinates'] = Point((123, 45))
place2['senti_score'] = 7
place2['rating_average'] = 3.26

place2 = proto.copy()
place2['name'] = 'White Building'
place2['geo_coordinates'] = Point((123, 45.2))
place2['senti_score'] = 400
place2['rating_average'] = 0

place2 = proto.copy()
place2['name'] = 'Weatherhead School'
place2['geo_coordinates'] = Point((123, 45.12))
place2['senti_score'] = 1
place2['rating_average'] = 4.8


# insert those things here first so we get ids

event_proto = event_data_manager.min_event_dict

event1 = proto.copy()
event1['name'] = 'Tomlinson food week'
event1['geo_coordinates'] = Point((123, 45))
event1['location'] = 'Tomlinson'
event1['place_id'] = place2['place_id']
event1['senti_score'] = 7

event1 = proto.copy()
event1['name'] = 'Computer Science Senior Project Presentations'
event1['geo_coordinates'] = Point((123, 45))
event1['location'] = 'White'
event1['place_id'] = place2['place_id'] #white's id
event1['senti_score'] = 500

event1 = proto.copy()
event1['name'] = 'Senior Capstone Presentations of Operation Management'
event1['geo_coordinates'] = Point((123, 45))
event1['location'] = 'Weatherhead'
event1['place_id'] = place2['place_id'] #weatherhead
event1['senti_score'] = 3