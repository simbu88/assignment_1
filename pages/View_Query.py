import streamlit as st
import youtube as yt
import pandas as pd
import numpy as np
import my_constant as constant
import result_page as rp
from concurrent.futures import ThreadPoolExecutor, Future
import time

col1,col2 = st.columns([0.1,0.9])
col11,col22 = st.columns([0.9,0.1])

style_heading = 'text-align: left; color:#ffffff'
executor = ThreadPoolExecutor(max_workers=1)

if "future" not in st.session_state:
    st.session_state.future = None
    st.session_state.answer = ""
    st.session_state.previous_question = None

with col1:
     st.image("images/video.png")
with col2:
     st.markdown(f"<h2 style='{style_heading}'>View Query</h2>", unsafe_allow_html=True)

question_option = ["Question 1","Question 2","Question 3","Question 4","Question 5","Question 6","Question 7","Question 8","Question 9","Question 10"]
option = st.selectbox(
    "Select the question",
    question_option,
    index=None,
    placeholder="Select the question...",
    label_visibility='collapsed'
)


def load_answer(option):
    time.sleep(5)
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

if option != st.session_state.previous_question:
    # Cancel previous task if it's still loading
    if st.session_state.future is not None:
        st.session_state.future.cancel()
    
    # Start loading answer for new question
    st.session_state.future = executor.submit(load_answer(option), option)
    st.session_state.previous_question = option   





