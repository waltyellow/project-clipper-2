"""`main` is the top level module for this Flask application."""
import os
import sys
import json
import logging, geojson
import time, math, statistics

from flask import request, render_template
from global_heatmap_service.utility import action_handler, commons, geo

from flask import Flask, request
import requests
from app.geo import api

# from google.appengine.api import urlfetch
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)

event_url = "https://cl1.zhenglinhuang.com:5000/events/search?"

place_url = "https://cl1.zhenglinhuang.com:5000/places/search?"


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route(rule='/', endpoint='get_map', methods=['GET'])
def get_map():
    length = float(request.args['length'])
    long = float(request.args['long'])
    lat = float(request.args['lat'])
    influence_radius = 0.45 * length

    if 'radius' in request.args:
        influence_radius = float(request.args['radius'])

    request_radius = influence_radius + length + 0.5 * length * math.sqrt(
        3)

    args = "geo_coordinates={0}&radius={1}".format(geojson.Point((long, lat)), request_radius)
    nearby_events = requests.request(event_url + args)

    h = int(request.args['h'])
    if h > 30:
        h = 30
    w = h * 2
    xstep = (length / 110574) / w
    ystep = (0.5 * length / (111320 * math.cos(math.radians(lat)))) / h
    x_left = long - (w / 2) * xstep
    x_right = x_left + w * xstep
    print(('x', x_left, x_right))

    y_top = lat + (h / 2) * ystep
    y_bottom = y_top - h * ystep
    print(('y', y_top, y_bottom))
    min_score = 0
    max_score = 0
    data_points = []
    for i in range(0, h):
        y = y_top - i * ystep
        for j in range(0, w):
            x = x_left + j * xstep
            score = action_handler.get_dynamic_score_for_heatmap_efficient(x, y, radius=influence_radius,
                                                                           nearby_events=nearby_events,
                                                                           nearby_places=nearby_places)
            if score < min_score:
                min_score = score
            elif score > max_score:
                max_score = score
            data_points.insert(len(data_points), score)
    stdev = statistics.stdev(data_points)
    mean = statistics.mean(data_points)

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
                           "id": place['place_id'],
                           "score": place['senti_score']})

    volcano = {"width": w, "height": h, 'values': data_points}
    # return json.dumps(
    #    {"width":w, "height": h, 'values': data_points})
    return render_template('heatmap_volcano.html', data_points=volcano, stdev=stdev, mean=mean, events=out_events,
                           places=out_places, min_value=min_score, max_value=max_score,
                           long_left=x_left, long_right=x_right, lat_top=y_top, lat_bottom=y_bottom,
                           w=w, h=h)


if __name__ == '__main__':
    resp = requests.request('GET', 'https://cl1.zhenglinhuang.com:5000/places')
    print(resp)
