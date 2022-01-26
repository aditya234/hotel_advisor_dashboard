import pandas as pd
import streamlit as st
from data_manager import KeyStrings, DashboardDataManager
import extra_streamlit_components as stx
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

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

column_one, column_two, column_three, column_four = st.columns(4)
with column_one:
    st.subheader(f"Best Cuisine:\n{data_manager.get_top_cusine()}")
with column_two:
    st.subheader(f"Most Spoken:\n{data_manager.get_top_language()}")
with column_three:
    st.subheader(f"Best Class:\n{data_manager.get_class()}")
with column_four:
    st.subheader(f"Average Price:\n{round(data_manager.data.price.mean(), 2)}")

st.markdown("""---""")
st.markdown("## Top Hotels")
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="All Hotels", description=""),
    stx.TabBarItemData(id=2, title="Top 20 Hotels", description=""),
], default=1)
if chosen_id == '2':
    if len(data_manager.top_20) == 0:
        st.write("No Data")
    else:
        wc = WordCloud(background_color="white", width=1200, height=500).fit_words(data_manager.top_20)
        # Display the generated image:
        st.image(wc.to_array())
else:
    st.write(data_manager.get_df())
######################################################
cuisine_names, cuisine_counts = data_manager.get_cusines_for_donut()
cusines = px.pie(
    hole=0.35,
    labels=cuisine_counts,
    names=cuisine_names,
    values=cuisine_counts,
    title=f"Top {len(cuisine_names)} Cuisines",
)
class_name, class_counts = data_manager.get_classes_for_donut()
hotel_classes = px.pie(
    hole=0.2,
    labels=class_counts,
    names=class_name,
    values=class_counts,
    title=f'Hotel {len(class_name)} Classes',
)
left_column, right_column = st.columns(2)
with left_column:
    if len(cuisine_names) > 0:
        st.plotly_chart(cusines, use_container_width=True)
    else:
        st.write("No Data for Top Cuisines")
        st.markdown("##")
        st.markdown("##")
with right_column:
    if len(class_name) > 0:
        st.plotly_chart(hotel_classes, use_container_width=True)
    else:
        st.write("No Data regarding Top Classes")
        st.markdown("##")
        st.markdown("##")
st.markdown("##")

amenities_names, amenities_counts = data_manager.get_amenities_for_donut()
amenities = px.pie(
    hole=0.2,
    labels=amenities_counts,
    names=amenities_names,
    values=amenities_counts,
    title=f'Top {len(amenities_names)} Amenities'
)

language_names, language_counts = data_manager.get_languages_for_donut()
languages_donut = px.pie(
    hole=0.2,
    labels=language_counts,
    names=language_names,
    values=language_counts,
    title=f'Top {len(language_names)} Languages'
)
left_column, right_column = st.columns(2)
with left_column:
    if len(amenities_names) > 0:
        left_column.plotly_chart(amenities, use_container_width=True)
    else:
        st.write("No Data regarding Top Amenities")
        st.markdown("##")
        st.markdown("##")
with right_column:
    if len(language_names) > 0:
        st.plotly_chart(languages_donut, use_container_width=True)
    else:
        st.write("No Data regarding most used Languages")
        st.markdown("##")
        st.markdown("##")
st.markdown("##")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
