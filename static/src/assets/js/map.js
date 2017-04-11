'use strict';

mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3IyNDI3IiwiYSI6ImNqMWI2NWR5azBhaDAyeG82MHBjcXVsOWgifQ.FWM5lIs5O3GIWD-UBZYxoA';

function generateMap() {
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v9',
        center: [-90, 38],
        zoom: 4
    });
}