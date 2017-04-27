'use strict';

mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3IyNDI3IiwiYSI6ImNqMWI2NWR5azBhaDAyeG82MHBjcXVsOWgifQ.FWM5lIs5O3GIWD-UBZYxoA';

function generateMap() {
    if (!!navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            createMap([position.coords.longitude, position.coords.latitude])
        });
    } else {
        createMap([-81.6944, 41.4933]);
    }
}

function createMap(position) {
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v9',
        center: position, // should have a props file or something...
        zoom: 11
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
                'circle-color': '#00FF00'
            }
        }, 'waterway-label');
        
        map.setPaintProperty('events', 'circle-radius', {
            property: 'excitement',
            stops: [
                [-1, 1],
                [1, 25]
            ]
        });
        
        var popup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false
        });
        map.on('mousemove', function(e) {
            var features = map.queryRenderedFeatures(e.point, {
                layers: ['events']
            });
    
            map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';
    
            if (!features.length) {
            	return popup.remove();
            }
    
            var feature = features[0];
            popup.setLngLat(feature.geometry.coordinates)
        	    .setHTML('<a href="events/' + feature.properties.id + '/event">' + feature.properties.name + '</a><br />' +
                      feature.properties.location + '<br />' + 'Excitement: ' + feature.properties.excitement)
        	    .addTo(map);
        });
    });
}