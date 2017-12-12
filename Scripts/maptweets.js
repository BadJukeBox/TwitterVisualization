mapboxgl.accessToken = '';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v9',
    center: [-117.25, 32.77],
    zoom: 11.5
});

var hours = [
    "00","01","02","03","04","05",
    "06","07","08","09","10","11",
    "12","13","14","15","16","17",
    "18","19","20","21","22","23"
];

function filterBy(hour) {

    var filters = ['==', 'hour', hour];
    map.setFilter('tweets-heat', filters);

    // Set the label to the hour
    document.getElementById('Hour').textContent = parseInt(hour);
}

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

map.on('load', function() {

    d3.json('http://localhost:8000/Data/SDGeoPoints.geojson', function(err, data) {
        if (err) throw err;

        map.addSource('tweets', {
            "type": "geojson",
            "data": data
        });
        console.log("success");
        map.addLayer({
            "id": "tweets-heat",
            "type": "heatmap",
            "source": "tweets",
            "maxzoom": 20,
            "paint": {
                "heatmap-weight": {
                    "property": "coordinates",
                    "type": "exponential",
                    "stops": [
                        [0, 0],
                        [6, 1]
                    ]
                },
                "heatmap-intensity": {
                    "stops": [
                        [0, 1],
                        [9, 3]
                    ]
                },
                "heatmap-color": [
                    "interpolate",
                    ["linear"],
                    ["heatmap-density"],
                    0, "rgba(33,102,172,0)",
                    0.2, "rgb(103,169,207)",
                    0.4, "rgb(209,229,240)",
                    0.6, "rgb(253,219,199)",
                    0.8, "rgb(239,138,98)",
                    1, "rgb(178,24,43)"
                ],
                "heatmap-radius": {
                    "stops": [
                        [0, 2],
                        [9, 20]
                    ]
                },
            }
        }, 'waterway-label');
        filterBy("00");

        document.getElementById('slider').addEventListener('input', function(e) {
            var hour = pad(e.target.value);
            console.log(hour);
            filterBy(hour);
        });
    });
});
