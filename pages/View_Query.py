import streamlit as st
import youtube as yt
import pandas as pd
import numpy as np
import my_constant as constant
import result_page as rp

col1,col2 = st.columns([0.1,0.9])
col11,col22 = st.columns([0.9,0.1])

style_heading = 'text-align: left; color:#ffffff'

with col1:
     st.image("images/video.png")
with col2:
     st.markdown(f"<h2 style='{style_heading}'>View Query</h2>", unsafe_allow_html=True)

question_option = [constant.QUESTION_1,constant.QUESTION_2,constant.QUESTION_3,constant.QUESTION_4,constant.QUESTION_5,constant.QUESTION_6
     ,constant.QUESTION_7,constant.QUESTION_8,constant.QUESTION_9,constant.QUESTION_10]
option = st.selectbox(
    "Select the question",
    question_option,
    index=None,
    placeholder="Select the question...",
    label_visibility='collapsed'
)

if option == constant.QUESTION_1: 
   rp.question_one()
elif option == constant.QUESTION_2:   
    rp.question_two()
elif option == constant.QUESTION_3:
      rp.question_three()   
elif option == constant.QUESTION_4:   
     rp.question_four() 
elif option == constant.QUESTION_5:   
     rp.question_five() 
elif option == constant.QUESTION_6:   
    rp.question_six() 
elif option == constant.QUESTION_7:   
    rp.question_seven() 
elif option == constant.QUESTION_8:   
    rp.question_eight() 
elif option == constant.QUESTION_9:   
    rp.question_nine() 
elif option == constant.QUESTION_10:   
    rp.question_ten()  





