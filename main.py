import streamlit as st
import youtube as yt
import pandas as pd
import numpy as np
import my_constant as constant
import result_page as rp


dataFrame = pd.DataFrame()
col1, col2 = st.columns(2)
channel_list =[]


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
   channelItem =yt.get_channel_details(text_input)
   if channelItem is None:
       st.write("Channel Not Found")
   else:
       
        st.write(channelItem)  
        save_btn_clicked = st.button("Save Into DB",type="primary",key="save_db")     

if st.session_state.get("save_db"):   
   yt.get_playlist_details(text_input)
   
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


# if finalValue:
#    left, middle, right = st.columns(3)
#    channelItem =  yt.get_channel_info(text_input)
#    channel_list.append(channelItem)
#    dataFrame = pd.DataFrame(channel_list)
#    st.write(dataFrame) 
#    save_btn_clicked = st.button("Save Into DB",type="primary",key="save_db")




   




   
 
   

   
      



   









    
