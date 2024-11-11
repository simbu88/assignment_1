import streamlit as st
import my_constant as constant
from PIL import Image
import base64
import altair as alt



st.set_page_config(
    page_title=constant.APPLICATION_NAME,
    page_icon="https://img.icons8.com/color/48/youtube-play.png",
    layout="wide",
    initial_sidebar_state="expanded")

def add_logo(logo_path):
    return Image.open(logo_path)


welcome_page = st.Page("./pages/Welcome.py", title="Welcome", icon=":material/waving_hand:")
add_channel_page = st.Page("./pages/Add_Channel.py", title="Add Channel", icon=":material/add_to_queue:")
view_query_page = st.Page("./pages/View_Query.py", title="View Queries", icon=":material/visibility:")
about_us = st.Page("./pages/About_Us.py", title="About us", icon=":material/person:")

my_logo = add_logo(logo_path="./images/video.png")
pages = st.navigation(
      [welcome_page, add_channel_page,view_query_page,about_us]
     )

pages.run()