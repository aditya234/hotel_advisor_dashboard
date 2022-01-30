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
st.sidebar.header("Apply Filters:")
st.sidebar.write("")
city = st.sidebar.selectbox(
    "Select a City:",
    options=data_manager.cities,
    key=KeyStrings.CITY_FILTER
)

# setting the above filters
data_manager.set_filters(city=city)

data_manager.get_top_20_hotels()
# ----MAIN SECTION ----
st.header(f"*Do you wish to open a hotel in {city}?*")
st.markdown(f"""This visualisation aims to explore the dynamics of the hotel business in {city}. The Map shows the 
distribution of hotels over various geographic locations around {city}. And the other plots represent the class 
distribution of various important factors one must consider while opening a hotel.""")
st.markdown("##")


layer = pdk.Layer(
        "GridLayer", data_manager.map_df, pickable=True, extruded=True, cell_size=200, elevation_scale=40, get_position="[lon, lat]",
    )

view_state = pdk.ViewState(latitude=data_manager.data_operations.coordinates[city][0],
                               longitude=data_manager.data_operations.coordinates[city][1], zoom=11, bearing=0, pitch=45)

map = pdk.Deck(layers=[layer],
               initial_view_state=view_state, tooltip={"text": "{position}\nTotal Hotels: {count}"}, )
st.pydeck_chart(map)

    # st.subheader(f"Best Style:\n{data_manager.get_top_cusine()}")
    # st.subheader(f"Most Spoken:\n{data_manager.get_top_language()}")
    # st.subheader(f"Best Class:\n{data_manager.get_class()}")
    # st.subheader(f"Average Price:\n{round(data_manager.data.price.mean(), 2)}")

######################################################
cuisine_data = data_manager.get_cusines_for_donut()
cusines = px.pie(
    cuisine_data,
    names='Cuisine',
    values='Total',
    title=f"Top {len(cuisine_data)} Styles",
)

class_data = data_manager.get_classes_for_donut()
hotel_classes = px.pie(
    class_data,
    names='Class',
    values='Total',
    title=f'Hotel {len(class_data)} Classes',
)

amenities_data = data_manager.get_amenities_for_donut()
amenities = px.pie(
    amenities_data,
    names='Amenity',
    values='Total',
    title=f'Top {len(amenities_data)} Amenities'
)

language_data = data_manager.get_languages_for_donut()
languages_donut = px.pie(
    language_data,
    names='Language',
    values='Total',
    title=f'Top {len(language_data)} Languages'
)

features_data = data_manager.get_best_features_for_donut()
features = px.pie(
    features_data,
    names='Feature',
    values='Total',
    title=f'Top features as per user reviews',
)

column_one,column_two,column_three = st.columns(3)
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
