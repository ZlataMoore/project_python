import folium
import webbrowser
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import json


geolocator = Nominatim(user_agent="my_request")

all_pages = ['1-100', '101-200', '201-300', '301-500',
             '501-700', '701-800', '801-1000', '1001-1200', '1201-1300']
start = 'flats'


def flats_to_map(pages, lst):

    map = folium.Map(
        location=[55.753300, 37.624239],  # широта и долгота России
        zoom_start=10
    )
    start = ''
    start_new = './flats/new/flats'
    start_old = './flats/old/flats'
    if pages[:3] == 'new':
        start = start_new
    else:
        start = start_old
    pages = pages[4:]
    mCluster = MarkerCluster(name='Marker').add_to(map)

    result = start + pages + '.json'

    with open(result, 'r', encoding='utf-8') as f:
        flats = json.loads(f.read())

    for flat in flats:
        string = flat['title'] + '\n' + flat['cost'] + '\n' + flat['address'][0]
        popup_t = f'<a href="/mortgage/{flat["cost"]}">{string}</a>'
        test = folium.Html(popup_t, script=True)


        folium.Marker(
            location=flat['coordinates'],
            popup=folium.Popup(test, min_width=150, max_width=500),
        ).add_to(mCluster)

    map.save(r'map.html')
    #webbrowser.open('map.html')

#flats_to_map('new 201-300', [1])