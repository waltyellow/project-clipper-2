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

event_senior_proj_dict = {
    'event_id': '',
    'keywords': [],
    'name': 'Senior Project Presentations',
    'description': 'The Class of 2017 Computer Science majors are all presenting their senior research projects.',
    'deleted': False,
    'location': 'Nord',
    'place_id': 'pl-WP_2MRutGg91w55q'
}

def generatePlaces():
    pm = PlaceDataManager()
    nord=pm.insert_one_place(place_nord_dict)
    olin = pm.insert_one_place(place_olin_dict)
    white = pm.insert_one_place(place_white_dict)
    smith = pm.insert_one_place(place_smith_dict)

def generateEvents():
    em = EventDataManager()
    senior_proj = em.insert_event_one(event_senior_proj_dict)



if __name__ == '__main__':
    #generatePlaces()
    generateEvents()