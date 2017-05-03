import sys
from pymongo import MongoClient
from app.data_managers import chatbot_test_set, common
from app.test_data import generate_events_and_cb, cb_and_sl, restaurants

sys.path.append('/root/project-clipper-2')
client = MongoClient('localhost', 27017)
client.drop_database(common.database_name)
generate_events_and_cb.create_campus_buildings_and_events()
restaurants.create_all_restaurants()
