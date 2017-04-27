import time, math
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager
from app.sentiment import emotion
import geojson

'''this file handles the bottom layer that adds comment-senti-score to raw scores for entities'''

'''this is lifetime, 'tao', in millisecond'''
event_senti_lifetime_in_days = 2
place_senti_lifetime_in_days = 5
delete_threshold = 0.02
seconds_per_day = 86400

'''calculate dynamic score for entities'''


def generate_dynamic_score_for_event(event: dict):
    event['dynamic_senti_score'] = event['senti_score']
    if 'place_id' in event and event['place_id'] != '':
        place_score = get_raw_score_for_place(event['place_id'])
    else:
        place_score = 0

    if 'geo_coordinates' in event and event['geo_coordinates'] != geojson.Point((0, 0)):
        nearby_events = EventDataManager().find_events_near(long=event['geo_coordinates']['coordinates'][0],
                                                            lat=event['geo_coordinates']['coordinates'][1])
        geo_score = aggregate_raw_score_from_entities(nearby_events, event_senti_lifetime_in_days)
    else:
        geo_score = 0

    event_score = event['senti_score']
    dynamic_score = event_score + place_score + 0.2 * geo_score
    event['dynamic_senti_score'] = dynamic_score
    return dynamic_score


def generate_dynamic_score_for_place(place: dict):
    place['dynamic_senti_score'] = place['senti_score']

    venue_events = EventDataManager().find_events_by_filter({'place_id': place['place_id']})
    event_score = aggregate_raw_score_from_entities(venue_events, event_senti_lifetime_in_days)

    if 'geo_coordinates' in place and place['geo_coordinates'] != geojson.Point((0, 0)):
        nearby_events = EventDataManager().find_events_near(long=place['geo_coordinates']['coordinates'][0],
                                                            lat=place['geo_coordinates']['coordinates'][1])
        geo_score = aggregate_raw_score_from_entities(nearby_events, event_senti_lifetime_in_days)
    else:
        geo_score = 0

    place_score = place['senti_score']
    dynamic_score = event_score + place_score + 0.2 * geo_score
    place['dynamic_senti_score'] = dynamic_score
    return dynamic_score


def get_dynamic_score_for_geolocation(long: float, lat: float):
    nearby_events = EventDataManager().find_events_near(long=long,
                                                        lat=lat)
    nearby_events_score = aggregate_raw_score_from_entities(nearby_events, event_senti_lifetime_in_days)

    nearby_places = PlaceDataManager().find_places_near(long=long, lat=lat)
    nearby_places_score = aggregate_raw_score_from_entities(nearby_places, place_senti_lifetime_in_days)
    dynamic_score = nearby_places_score + nearby_events_score
    return dynamic_score


def get_raw_score_for_place(place_id: str):
    dm = PlaceDataManager()
    place = dm.find_one_place_by_id(place_id)
    refresh_score_for_entity(place)
    return place['senti_score']


def aggregate_raw_score_from_entities(entities, lifetime):
    sum = 0
    for entity in entities:
        sum += extract_raw_score_from_entity(entity, lifetime)
    return sum


def extract_raw_score_from_entity(entity, lifetime):
    refresh_score_for_entity(entity, lifetime)
    return entity['senti_score']



'''when a qualified message is received for place/ratings or comments on places and events'''


def on_message_received_for_event(event_id: str, message: dict):
    dm = EventDataManager()
    event = dm.find_event_by_id(event_id)
    precondition_check_for_required_keys(entity=event,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])

    refresh_score_for_entity(entity=event, lifetime_in_days=event_senti_lifetime_in_days)
    on_message_received(event, message)
    dm.replace_one_event(event)


def on_message_received_for_place(place_id: str, message: dict):
    dm = PlaceDataManager()
    place = dm.find_one_place_by_id(place_id)
    precondition_check_for_required_keys(entity=place,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])

    refresh_score_for_entity(entity=place, lifetime_in_days=place_senti_lifetime_in_days)
    if message['type'] == 'rating' or message['type'] == 'review':
        on_rating_received(place, message)
    if message['type'] != 'rating':
        on_message_received(place, message)
    dm.replace_one_place(place)


'''rating is the simple average of all ratings
precondition: each message has a score
'''


def on_rating_received(entity: dict, message: dict) -> dict:
    precondition_check_for_required_keys(entity, required_keys=['rating_count', 'rating_average'])
    precondition_check_for_required_keys(message, required_keys=['rating'])

    rating_count = entity['rating_count']
    rating_average = entity['rating_average']
    new_rating = message['rating']
    rating_average = (rating_count * rating_average + new_rating) / (rating_count + 1)
    entity['rating_average'] = rating_average
    entity['rating_count'] = rating_count + 1
    return entity


'''only refresh the senti-score without adding anything new'''


def refresh_score_for_entity(entity: dict, lifetime_in_days: float):
    try:
        precondition_check_for_required_keys(entity,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])
    except ValueError:
        return

    # get decay factor
    current_time = time.time()
    last_updated_time = entity['senti_score_updated_time']
    decay_factor = get_decay_factor(last_updated_time=last_updated_time,
                                    current_time=current_time,
                                    lifetime_in_days=lifetime_in_days)

    # decay senti_score
    entity['senti_score_updated_time'] = current_time
    entity['senti_score'] *= decay_factor

    # decay tag scores
    tag_counter = entity['mood_tag_counter']
    for tag in tag_counter:
        tag_counter[tag] *= decay_factor
        if tag_counter[tag] < delete_threshold:
            tag_counter.pop(tag)


'''messages contribute to senti_score, and is subjected to the mean life time specified'''


def on_message_received(entity: dict, message: dict) -> dict:
    precondition_check_for_required_keys(entity,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])

    # initialize the values
    senti_score = entity['senti_score']
    message = process_message(message)
    mood_tags = message['moodtags']
    message_score = message['senti_score']

    # add this comment
    current_time = time.time()
    entity['senti_score_updated_time'] = current_time
    entity['senti_score'] = senti_score + message_score

    # collect mood tags
    aggregate_mood_tags(tag_counter=entity['mood_tag_counter'], mood_tags=mood_tags)
    return entity


def aggregate_mood_tags(tag_counter, mood_tags):
    # aggregate
    for tag in mood_tags:
        if tag not in tag_counter:
            tag_counter[tag] = 0
        tag_counter[tag] += 1


def process_message(message: dict) -> dict:
    body = message['body']
    raw = emotion.comment_to_score(body)
    message['moodtags'] = raw['mood tags']
    message['senti_score'] = float(raw['score'])
    return message


'''decay current score for e^-(delta_t/lifetime)'''


def get_decay_factor(current_time, last_updated_time, lifetime_in_days):
    time_delta_in_days = (current_time - last_updated_time) / seconds_per_day
    decay_factor = math.exp(0 - (time_delta_in_days / lifetime_in_days))
    return decay_factor


def precondition_check_for_required_keys(entity, required_keys):
    for key in required_keys:
        missing_keys = []
        is_ok = True
        if key not in entity:
            missing_keys.append(key)
            is_ok = False

        if not is_ok:
            raise ValueError('the eneity is missing keys:' + key.__str__())

def find():
    eventDataManager = EventDataManager()
    #events = eventDataManager.find_events_near(125, 35.0000, radius=5)
    event = eventDataManager.find_event_by_id('ev-WQEHXE9tc1py6OPs')
    generate_dynamic_score_for_event(event)
    print(event)

if __name__ == '__main__':
    find()
