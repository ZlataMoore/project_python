import folium
import webbrowser
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import json


geolocator = Nominatim(user_agent="my_request")

all_pages = ['1-100', '101-200', '201-300', '301-500',
             '501-700', '701-800', '801-1000', '1001-1200', '1201-1300']
start = 'flats'
def flats_to_map(pages):

    map = folium.Map(
        location=[55.753300, 37.624239],  # широта и долгота России
        zoom_start=10
    )
    start = './flats/flats'
    mCluster = MarkerCluster(name='Marker').add_to(map)
    result = start + pages + '.json'
    with open(result) as f:
        flats = json.load(f)

    for flat in flats:
        string = flat['title'] + '\n' + flat['cost'] + '\n' + flat['address'][0]
        html = string.replace('\n', '<br>').replace('\t', 'nbsp;')

        folium.Marker(
            location=flat['coordinates'],
            popup=string,
        ).add_to(mCluster)

    map.save(r'map.html')
    #webbrowser.open('map.html')

#flats_to_map('1-100')