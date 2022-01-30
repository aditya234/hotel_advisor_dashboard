import streamlit as st
from helpers.data_manager import KeyStrings, DashboardDataManager
import plotly.express as px
import pydeck as pdk

# ----- PAGE CONFIG (title bar)------
st.set_page_config(
    page_title="Hotel Advisor",
    page_icon=":hotel:",
    layout="wide",
    initial_sidebar_state="expanded",
)

data_manager = DashboardDataManager()
data_manager.get_filter_data()

# ---- SIDEBAR ----
# st.header("Apply Filters:")
st.write("")
city = st.selectbox(
    "Select a City:",
    options=data_manager.cities,
    key=KeyStrings.CITY_FILTER
)

# setting the above filters
data_manager.set_filters(city=city)

data_manager.get_top_20_hotels()
# ----MAIN SECTION ----
st.markdown(f"""This visualisation aims to explore the dynamics of the hotel business in {city}. The Map shows the 
distribution of hotels over various geographic locations around {city}. And the other plots represent the class 
distribution of various important factors one must consider while opening a hotel.""")
st.markdown("##")
# header stats
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.subheader(f"Best Restaurant Style\n{data_manager.get_top_cusine()}")
with c2:
    st.subheader(f"Most Spoken\n{data_manager.get_top_language()}")
with c3:
    st.subheader(f"Top Hotel Type\n{data_manager.get_class()}")
with c4:
    st.subheader(f"Average Price\n{round(data_manager.data.price.mean(), 2)}")
# make a map
st.markdown("##")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    layer = pdk.Layer(
        "GridLayer", data_manager.map_df, pickable=True, extruded=True, cell_size=200, elevation_scale=40,
        get_position="[lon, lat]",
    )

    view_state = pdk.ViewState(latitude=data_manager.data_operations.coordinates[city][0],
                               longitude=data_manager.data_operations.coordinates[city][1], zoom=10.5, bearing=0,
                               pitch=45,height=300, width=400)

    map = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_state, tooltip={"text": "{position}\nTotal Hotels: {count}"})
    st.pydeck_chart(map)
    st.write("Hotel Densities across different locations")

with col2:
    layer = pdk.Layer(
        "GridLayer", data_manager.map_df, pickable=True, extruded=True, cell_size=200, elevation_scale=40,
        get_position="[lon, lat]",
    )

    view_state = pdk.ViewState(latitude=data_manager.data_operations.coordinates[city][0],
                               longitude=data_manager.data_operations.coordinates[city][1], zoom=10.5, bearing=0,
                               pitch=45,height=300, width=400)

    map = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_state, tooltip={"text": "{position}\nTotal Hotels: {count}"}, height=100, )
    st.pydeck_chart(map)
    st.write("Hotel Ratings across different locations")

with col3:
    layer = pdk.Layer(
        "GridLayer", data_manager.map_df, pickable=True, extruded=True, cell_size=200, elevation_scale=40,
        get_position="[lon, lat]",
    )

    view_state = pdk.ViewState(latitude=data_manager.data_operations.coordinates[city][0],
                               longitude=data_manager.data_operations.coordinates[city][1], zoom=10.5, bearing=0,
                               pitch=45,height=300, width=400)

    map = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_state, tooltip={"text": "{position}\nTotal Hotels: {count}"}, height=100, )
    st.pydeck_chart(map)
    st.write("Hotel Ratings across different locations")

st.markdown("##")
######################################################
cuisine_data = data_manager.get_cusines_for_donut()
cusines = px.pie(
    cuisine_data,
    names='Cuisine',
    values='Total',
    title=f"Restaurant Styles",
)

class_data = data_manager.get_classes_for_donut()
hotel_classes = px.pie(
    class_data,
    names='Class',
    values='Total',
    title=f'Hotel Types',
)

amenities_data = data_manager.get_amenities_for_donut()
amenities = px.pie(
    amenities_data,
    names='Amenity',
    values='Total',
    title=f'Hotel Amenities'
)

language_data = data_manager.get_languages_for_donut()
languages_donut = px.pie(
    language_data,
    names='Language',
    values='Total',
    title=f'Language Spoken'
)

features_data = data_manager.get_best_features_for_donut()
features = px.pie(
    features_data,
    names='Feature',
    values='Total',
    title=f'Top features as per user reviews',
)

column_one, column_two, column_three = st.columns(3)
with column_one:
    st.plotly_chart(cusines, use_container_width=True)
with column_two:
    st.plotly_chart(hotel_classes, use_container_width=True)
with column_three:
    st.plotly_chart(languages_donut, use_container_width=True)

column_one, column_two = st.columns(2)
with column_one:
    st.plotly_chart(amenities, use_container_width=True)
with column_two:
    st.plotly_chart(features, use_container_width=True)
# ---- HIDE STREAMLIT STYLE ----
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)
