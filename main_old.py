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

## Use to set the page tab
st.set_page_config(
    page_title=constant.APPLICATION_NAME,
    page_icon="https://img.icons8.com/color/48/youtube-play.png",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

dataFrame = pd.DataFrame()
col1, col2 = st.columns(2)
channel_list =[]

##title_container = st.beta_container()
slide_col1, slide_col2 = st.columns(2)

style_heading = 'text-align: left; color:#ffffff'
style_image = 'display: block; margin-left: auto; margin-right: auto; color:#ffffff' 



st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #17153B;
    }
</style>
""", unsafe_allow_html=True)

def add_logo(logo_path, width, height):
    return Image.open(logo_path)



with st.sidebar:
     with slide_col1:
               my_logo = add_logo(logo_path="./images/video.png", width=50, height=60)
               st.sidebar.image(my_logo)
     with slide_col2:
               st.markdown(f"<h1 style='{style_heading}'>{constant.APPLICATION_NAME}</h1>", unsafe_allow_html=True)
     
     st.markdown("<span style='color:#FFD3B6'>Add Channel</span>",
             unsafe_allow_html=True)
     st.markdown("<span style='color:#FFD3B6'>View Queries</span>",
             unsafe_allow_html=True)
     st.markdown("<span style='color:#FFD3B6'>About Us</span>",
             unsafe_allow_html=True)
with col1:
  text_input = st.text_input(
      "Enter channel Id",
      placeholder="Enter channel Id",key='channelId',
      label_visibility='collapsed'
  )
with col2:
     search = st.button("Search", type="primary")

if search:
   left, middle, right = st.columns(3)
   result = yt.getChannelIsAvaialble(text_input)
   if(result >0):
       st.warning('Channel is already availabe,try different channel id') 
   else:
       st.write("Channel Not Found")      
   
   channelItem =yt.get_channel_details(text_input)
   if channelItem is None:
       st.write("Channel Not Found")
   else:
        st.write(channelItem)  
        save_btn_clicked = st.button("Save Into DB",type="primary",key="save_db")     

if st.session_state.get("save_db"):   
   yt.get_playlist_details(text_input)
   
question_option = ["Question 1","Question 2","Question 3","Question 4","Question 5","Question 6","Question 7","Question 8","Question 9","Question 10"]
option = st.selectbox(
    "Select the question",
    question_option,
    index=None,
    placeholder="Select the question...",
    label_visibility='collapsed'
)

if option == "Question 1": 
   rp.question_one()
elif option == "Question 2":   
    rp.question_two()
elif option == "Question 3":
      rp.question_three()   
elif option ==  "Question 4":   
     rp.question_four() 
elif option ==  "Question 5":   
     rp.question_five() 
elif option ==  "Question 6":   
    rp.question_six() 
elif option ==  "Question 7":   
    rp.question_seven() 
elif option ==  "Question 8":   
    rp.question_eight() 
elif option ==  "Question 9":   
    rp.question_nine() 
elif option ==  "Question 10":   
    rp.question_ten()                                


# if finalValue:
#    left, middle, right = st.columns(3)
#    channelItem =  yt.get_channel_info(text_input)
#    channel_list.append(channelItem)
#    dataFrame = pd.DataFrame(channel_list)
#    st.write(dataFrame) 
#    save_btn_clicked = st.button("Save Into DB",type="primary",key="save_db")




   




   
 
   

   
      



   









    
