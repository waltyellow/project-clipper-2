'use strict';

mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3IyNDI3IiwiYSI6ImNqMWI2NWR5azBhaDAyeG82MHBjcXVsOWgifQ.FWM5lIs5O3GIWD-UBZYxoA';

function generateMap() {
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v9',
        center: [-81.6944, 41.4933],
        zoom: 10
    });
    
    map.on('load', function() {
        map.addSource('events', {
            'type': 'geojson',
            'data': 'assets/data/data.json'
        });
        
        map.addLayer({
            'id': 'events',
            'source': 'events',
            'type': 'circle',
            'paint': {
                'circle-opacity': 0.45,
                'circle-color': '#00FF00',
                'circle-radius': 10
            }
        }, 'waterway-label'); // before?
    });
}