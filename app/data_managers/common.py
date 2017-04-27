import json
import app.utility.geo as geo


def search_parameter_to_db_filter(arguments: dict):
    filter = {}
    for key in arguments:
        value = arguments[key]

        if key == 'geo_coordinates':
            value = json.loads(value)
            if 'radius' in arguments:
                value = geo.get_query_for_point_in_circle(value, float(arguments['radius']))
            else:
                value = geo.get_query_for_point_in_circle(value)

        elif key[-7:] == '_search':
            key = key[:-7]
            value = generate_search_query(value)

        elif key == 'radius':
            continue

        else:
            try:
                value = json.loads(value)
            except ValueError:
                pass

        filter[key] = value

    print(filter)
    return filter


def generate_search_query(value):
    return {'$regex': value, '$options': 'i'}
