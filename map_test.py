import streamlit as st
from shapely.geometry import Point, Polygon
# import geopandas as gpd
import pandas as pd
import geopy

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# # location 1
# location1 = geolocator.geocode("Ariake, Tokyo Prefecture, Japan")
#
# lat1 = location1.latitude
# lon1 = location1.longitude
#
# location2 = geolocator.geocode("Nishiikebukuro, Tokyo Prefecture, Japan")
#
# lat2 = location2.latitude
# lon2 = location2.longitude

# map_data = pd.DataFrame({'lat': [lat1, lat2], 'lon': [lon1, lon2]})
map_data = pd.read_csv('new_york_data.csv')
map_data = map_data[map_data.lat.notna()]
map_data = map_data[['lat','lon']]
st.map(data=map_data,zoom=7)
# print(f"Loc 1 --> {location1}")

