def get_query_for_coordinates_in_circle(long, lat, radius):
    query = {
        '$nearSphere': {
            '$geometry': {
                'type': "Point",
                'coordinates': [long, lat]
            },
            '$minDistance': 0,
            '$maxDistance': radius
        }
    }
    return query
