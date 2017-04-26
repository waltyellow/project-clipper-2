__author__ = 'navyakandkuri'
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager

place_nord_dict = {
    'place_id': '',
    'name': 'Nord',
    'type': 'place',
    'deleted': False
}

place_olin_dict = {
    'place_id': '',
    'name': 'Olin',
    'type': 'place',
    'deleted': False

}

place_white_dict = {
    'place_id': '',
    'name': 'White',
    'type': 'place',
    'deleted': False

}

place_smith_dict = {
    'place_id': '',
    'name': 'Smith',
    'type': 'place',
    'deleted': False
}

def generatePlaces():
    pm = PlaceDataManager()
    nord=pm.insert_one_place(place_nord_dict)
    olin = pm.insert_one_place(place_olin_dict)
    white = pm.insert_one_place(place_white_dict)
    smith = pm.insert_one_place(place_smith_dict)

def generateEvents():
    em = EventDataManager()



if __name__ == '__main__':
    generatePlaces()