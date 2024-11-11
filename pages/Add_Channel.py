import streamlit as st
import youtube as yt
import pandas as pd
import numpy as np
import my_constant as constant
import result_page as rp
import altair as alt
from PIL import Image
import base64
import streamlit.components.v1 as components
import requests
from io import BytesIO

col1,col2 = st.columns([0.1,0.9])
col11,col22 = st.columns([0.9,0.1])

style_heading = 'text-align: left; color:#ffffff'

with col1:
     st.image("images/video.png")
with col2:
     st.markdown(f"<h2 style='{style_heading}'>Add Channel</h2>", unsafe_allow_html=True)

def clearText():
    st.session_state.my_text = st.session_state.channelId
    st.session_state.channelId = ""

with col11:
  text_input = st.text_input(
      "Enter channel Id",
      placeholder="Enter channel Id",key='channelId',
      label_visibility='collapsed'
  )
with col22:
     search = st.button("Search", type="primary")

@st.dialog("Alert!")
def show_dialog(message):
    st.write(message)
    if st.button("Close"):
       clearText()
       st.rerun()   

def loadImage(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    new_width = 300
    new_height = 200
    img_resized = img.resize((new_width, new_height))
    st.image(img_resized)       

def showChannelInfo(channelData):
    ch_col1,ch_col2 = st.columns([0.1,0.9])
    with ch_col1:
         loadImage(channelData['channel_image'].iloc[0])
    with ch_col2:
         channel_name = channelData['channel_name'].iloc[0]
         channel_subscriber = channelData['channel_subscriber_count'].iloc[0]
         channel_video_count = channelData['channel_video_count'].iloc[0]
         channel_views_count = channelData['channel_views'].iloc[0]

         st.write(f"<h3 style='color:#f29652'>{channel_name}</h3>",unsafe_allow_html=True)
         st.write(channelData['channel_description'].iloc[0])
         st.write(f"<b style='color:#f29652'>Subscriber:</b> {channel_subscriber}",unsafe_allow_html=True)
         st.write(f"<b style='color:#f29652'>Videos:</b> {channel_video_count}",unsafe_allow_html=True)
         st.write(f"<b style='color:#f29652'>Views:</b> {channel_views_count}",unsafe_allow_html=True)
         inside_col1,inside_col2 = st.columns([0.8,0.2])
         with inside_col2:
              save_btn_clicked = st.button("Save Into DB",type="primary",key="save_db") 

if st.session_state.get("save_db"):   
   with st.spinner("Retriving and storing... Please wait."):
        yt.get_playlist_details(text_input)

   show_dialog("Channel store inside the data base")       

def getChannelInfo():
    with st.spinner("Processing... Please wait."):
          channelItem =yt.get_channel_details(text_input) 

    if channelItem is not None:      
      showChannelInfo(channelItem)
    else:
      show_dialog("Channel not found")        

if search:
   if not text_input:
      show_dialog("Enter the channel id")
   else:
      with st.spinner("Processing... Please wait."):
           result = yt.getChannelIsAvaialble(text_input) 
      if(result >0):
          show_dialog('Channel is already availabe,try different channel id') 
      else:
          getChannelInfo()
          
       
 
    