def get_query_for_coordinates_in_circle(long, lat, radius):
    point = {'type': "Point", 'coordinates': [long, lat]}
    query = get_query_for_point_in_circle(point, radius)
    return query


def get_query_for_point_in_circle(point, radius=500):
    query = {
        '$nearSphere': {
            '$geometry': point,
            '$minDistance': 0,
            '$maxDistance': radius
        }
    }
    return query


def create_geo_filter(point, radius=500):
    return {'geo_coordinates': get_query_for_point_in_circle(point, radius=radius)}
