import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
import webbrowser
import geocoder
from geopy.geocoders import Nominatim
import json
with open('flats.json') as f:
    flats = json.load(f)

# address we need to geocode
loc = 'Москва,  Нижние Мнёвники,  37Б'

# making an instance of Nominatim class
geolocator = Nominatim(user_agent="my_request")

# applying geocode method to get the location
location = geolocator.geocode(loc)
map = folium.Map(
    location = [55.753300, 37.624239],    # широта и долгота России
    zoom_start = 10
)
# printing address and coordinates
print(location.address)
print((location.latitude, location.longitude))

for flat in flats:
    if flat['coordinates']:
        folium.Marker(
              location=flat['coordinates'],
              popup=flat['address'],
           ).add_to(map)

#g = geocoder.yandex('Moscow Russia')

map.save(r'C:\Users\Zlata\PycharmProjects\map_of_flats\map.html')
#display(russia_map)
webbrowser.open('map.html')