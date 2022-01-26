import streamlit as st
from shapely.geometry import Point, Polygon
# import geopandas as gpd
import pandas as pd
import geopy
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk
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

# map_data = pd.read_csv('./data/data.csv')
# map_data = map_data[map_data.city == 'Singapore']
# map_data = map_data[map_data.lat.notna()]
# map_data = map_data[['lat','lon']]
# st.map(data=map_data,zoom=1)


df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.write(df)
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=30,
     ),
     layers=[
         # pdk.Layer(
         #    'HexagonLayer',
         #    data=df,
         #    get_position='[lon, lat]',
         #    radius=200,
         #    elevation_scale=4,
         #    elevation_range=[0, 1000],
         #    pickable=True,
         #    extruded=True,
         # ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))
