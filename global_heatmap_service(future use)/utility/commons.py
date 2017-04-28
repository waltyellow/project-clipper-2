import time, math

seconds_per_day = 86400
delete_threshold = 0.02

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
