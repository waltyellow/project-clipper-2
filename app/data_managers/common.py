import json


def search_parameter_to_db_filter(arguments: dict):
    filter = {}
    for key in arguments:
        value = arguments[key]

        if key[-7:] == '_search':
            key = key[:-7]
            value = generate_search_query(value)

        else:
            try:
                value = json.loads(value)
            except ValueError:
                pass

        filter[key] = value

    return filter


def generate_search_query(value):
    return {'$regex': value, '$options': 'i'}
