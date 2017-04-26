import time, math
from app.data_managers.places_data_manager import PlaceDataManager
from app.data_managers.event_data_manager import EventDataManager
from app.sentiment import emotion

'''this file handles the bottom layer that adds comment-senti-score to raw scores for entities'''

'''this is lifetime, 'tao', in millisecond'''
event_senti_lifetime_in_days = 2
place_senti_lifetime_in_days = 5
delete_threshold = 0.02
seconds_per_day = 86400

'''when a qualified message is received for place/ratings or comments on places and events'''


def on_message_received_for_event(event_id: str, message: dict):
    dm = EventDataManager()
    event = dm.find_event_by_id(event_id)
    precondition_check_for_required_keys(entity=event,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])

    refresh_score_for_entity(entity=event, lifetime_in_days=event_senti_lifetime_in_days)
    if message['type'] == 'rating' or message[type] == 'review':
        on_rating_received(event, message)
    if message['type'] != 'rating':
        on_message_received(event, message)
    dm.replace_one_event(event)


def on_message_received_for_place(place_id: str, message: dict):
    dm = PlaceDataManager()
    place = dm.find_one_place_by_id(place_id)
    precondition_check_for_required_keys(entity=place,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])

    refresh_score_for_entity(entity=place, lifetime_in_days=place_senti_lifetime_in_days)
    if message['type'] == 'rating' or message[type] == 'review':
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
    precondition_check_for_required_keys(entity,
                                         required_keys=['senti_score', 'senti_score_updated_time', 'mood_tag_counter'])

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
    raw = emotion.score_calculation(message['body'])
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
