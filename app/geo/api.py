import json
import time, math, statistics

from flask import request, render_template

import app.data_managers.event_data_manager as edm
import app.data_managers.places_data_manager as pdm
from app import server
from app.data_managers.common import search_parameter_to_db_filter
from app.data_managers.event_data_manager import EventDataManager
from app.utility import action_handler


@server.route(rule='/here', endpoint='here_get_score', methods=['GET'])
def here():
    long = float(request.args['long'])
    lat = float(request.args['lat'])
    return json.dumps({'dynamic_senti_score': action_handler.get_dynamic_score_for_geolocation(long, lat)})


@server.route(rule='/global', endpoint='get_map', methods=['GET'])
def get_map():
    horizontal_distance = float(request.args['length'])
    vertical_distance = 2.5*horizontal_distance
    long = float(request.args['long'])
    lat = float(request.args['lat'])
    radius = 0.15 * horizontal_distance

    if 'radius' in request.args:
        radius = float(request.args['radius'])

    nearby_events = edm.EventDataManager().find_events_near(long=long,
                                                            lat=lat, radius=2*radius + horizontal_distance * math.sqrt(3))
    nearby_places = pdm.PlaceDataManager().find_places_near(long=long, lat=lat, radius=2*radius + horizontal_distance * math.sqrt(3))

    vertical_resolution = int(request.args['h'])
    if vertical_resolution > 60:
        vertical_resolution = 60
    horizontal_resolution = vertical_resolution * 2
    meters_per_degree_longitude = (111320 * math.cos(math.radians(lat)))
    xstep = ((horizontal_distance/horizontal_resolution) / meters_per_degree_longitude)
    meters_per_degree_latitude = 110574
    ystep = ((vertical_distance/vertical_resolution) / meters_per_degree_latitude)

    x_left = long - (horizontal_resolution / 2) * xstep
    x_right = x_left + horizontal_resolution * xstep
    print(('x range, x diff, ', x_left, x_right), x_right-x_left)

    y_top = lat + (vertical_resolution / 2) * ystep
    y_bottom = y_top - vertical_resolution * ystep
    print(('y range, y diff', y_top, y_bottom), y_top-y_bottom)

    data_points = []
    for i in range(0, vertical_resolution):
        y = y_top - i * ystep
        row = []
        for j in range(0, horizontal_resolution):
            x = x_left + j * xstep
            score = action_handler.get_dynamic_score_for_heatmap_efficient(x, y, radius=radius,
                                                                           nearby_events=nearby_events,
                                                                           nearby_places=nearby_places)
            # if score < min_score:
            #     min_score = score
            # elif score > max_score:
            #     max_score = score
            row.append(score)
        data_points += row
    stdev = statistics.stdev(data_points)
    mean = statistics.mean(data_points)
    min_score = min(data_points)
    max_score = max(data_points)
    out_events = []
    x_diff = x_right - x_left
    y_diff = y_top - y_bottom
    for event in nearby_events:
        action_handler.refresh_score_for_entity(event, action_handler.event_senti_lifetime_in_days)
        long = event['geo_coordinates']['coordinates'][0]
        lat = event['geo_coordinates']['coordinates'][1]
        out_events.append({"x": ((long - x_left) / x_diff),
                           "y": ((y_top - lat) / y_diff),
                           "name": event['name'],
                           "type": "event",
                           "score": event['senti_score'],
                           "id": event['event_id']})

    out_places = []
    for place in nearby_places:
        action_handler.refresh_score_for_entity(place, action_handler.place_senti_lifetime_in_days)
        long = place['geo_coordinates']['coordinates'][0]
        lat = place['geo_coordinates']['coordinates'][1]
        out_places.append({"x": ((long - x_left) / x_diff),
                           "y": ((y_top - lat) / y_diff),
                           "name": place['name'],
                           "type": "place",
                           "id": place['place_id'],
                           "score": place['senti_score']})
        #print(place)

    volcano = {"width": horizontal_resolution, "height": vertical_resolution, 'values': data_points}

    # return json.dumps(
    #    {"width":w, "height": h, 'values': data_points})
    return render_template('heatmap_volcano.html', data_points=volcano, stdev=stdev, mean=mean,
                           entities=out_events + out_places,
                           min_value=min_score, max_value=max_score,
                           long_left=x_left, long_right=x_right, lat_top=y_top, lat_bottom=y_bottom,
                           w=horizontal_resolution, h=vertical_resolution, vdist=vertical_distance)
