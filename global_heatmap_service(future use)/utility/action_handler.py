import time, math
from geopy.distance import great_circle

'''this file handles the bottom layer that adds comment-senti-score to raw scores for entities'''

'''this is lifetime, 'tao', in millisecond'''
event_senti_lifetime_in_days = 2
place_senti_lifetime_in_days = 5
delete_threshold = 0.02
seconds_per_day = 86400

'''calculate dynamic score for entities'''


def get_dynamic_score_for_heatmap_efficient(long: float, lat: float, radius: float, nearby_events, nearby_places):
    nearby_events_score = aggregate_raw_score_from_entities_distance_based(nearby_events, event_senti_lifetime_in_days,
                                                                           long, lat, radius)
    nearby_places_score = aggregate_raw_score_from_entities_distance_based(nearby_places, place_senti_lifetime_in_days,
                                                                           long, lat, radius)
    dynamic_score = nearby_places_score + nearby_events_score
    return dynamic_score


def aggregate_raw_score_from_entities_distance_based(entities, lifetime, long, lat, radius):
    sum = 0
    for entity in entities:
        entity_loc = (entity['geo_coordinates']['coordinates'][0], entity['geo_coordinates']['coordinates'][1])
        center_loc = (long, lat)
        distance = great_circle(entity_loc, center_loc).meters
        fraction = (1 - distance / radius)
        if fraction < 0:
            fraction = 0
        sum += extract_raw_score_from_entity(entity, lifetime) * fraction * fraction
    return sum


def extract_raw_score_from_entity(entity, lifetime):
    refresh_score_for_entity(entity, lifetime)
    return entity['senti_score']


'''when a qualified message is received for place/ratings or comments on places and events'''
'''only refresh the senti-score without adding anything new'''


def refresh_score_for_entity(entity: dict, lifetime_in_days: float):
    try:
        precondition_check_for_required_keys(entity,
                                             required_keys=['senti_score', 'senti_score_updated_time',
                                                            'mood_tag_counter'])
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


def aggregate_mood_tags(tag_counter, mood_tags):
    # aggregate
    for tag in mood_tags:
        if tag not in tag_counter:
            tag_counter[tag] = 0
        tag_counter[tag] += 1


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
