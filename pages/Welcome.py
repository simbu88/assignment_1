import streamlit as st
import my_constant as constant


style_heading = 'text-align: left; color:#ffffff'
st.image("images/video.png")
st.markdown(f"<h1 style='{style_heading}'>Welcome to {constant.APPLICATION_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"A YouTube Data Harvesting application that allows users to access and analyze data from multiple YouTube channels.")
st.markdown(f"This application has three main menu options:<ul><li> Add Channel</li><li>View Query</li><li>About Us</li></ul> In the <b style='color:#f29652'>Add Channel</b> section, users can search for a channel by entering the channel ID, which retrieves the channel details. If the user wishes, they have the option to add this channel information to the database",unsafe_allow_html=True)
st.markdown(f"In the <b style='color:#f29652'>View Queries</b> menu, all sets of queries with answers related to YouTube will be displayed.",unsafe_allow_html=True)
st.markdown(f"In the <b style='color:#f29652'>About Us</b> menu, displays details about the developer(Me).",unsafe_allow_html=True)
