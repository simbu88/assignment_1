import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import database as db
import seaborn as sns
import re
import my_constant as constant
import requests
from io import BytesIO
from PIL import Image
from itertools import cycle


original_title = '<p style="font-family:Courier; color:Green; font-size: 20px;">Answer : </p>'

def stop_long_task():
    st.session_state.stop_task = True

def loadImage(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    new_width = 300
    new_height = 200
    img_resized = img.resize((new_width, new_height))
    st.image(img_resized)   

def question_one():
    st.write(constant.QUESTION_1)
    my_query =("SELECT ch.channel_name,v.video_id,v.video_name,v.thumbnail FROM channel ch JOIN playlist pl ON ch.channel_id = pl.channel_id"
               " JOIN videos v ON v.playlist_id = pl.playlist_id ")
    result = db.read_data(my_query)
    result =result.drop_duplicates(['video_id'])
    rows = result.shape[0]
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Record Found : ",rows)
    
    for i in range(0, len(result), 4):
        cols = st.columns(4)  
        for j, col in enumerate(cols):
            if i + j < len(result):
               videoInfo = result.iloc[i + j]
               col.image(videoInfo['thumbnail'],width=100)
               col.write(f"<b style='color:#f29652'>Video Name:</b>{videoInfo['video_name']}",unsafe_allow_html=True)
               col.write(f"<b style='color:#f29652'>channel Name:</b>{videoInfo['channel_name']}",unsafe_allow_html=True)
               col.write("________________________________________")
        
    

def question_two():
    st.write(constant.QUESTION_2)
    query = "select channel_image,channel_name, channel_description,channel_video_count from channel"
    result_data = db.read_data(query)
    print(result_data.info())
    result_data =result_data.sort_values("channel_video_count",ascending=False)
    top_one = result_data.head(1)
    st.markdown(original_title, unsafe_allow_html=True)
    ch_col1,ch_col2 = st.columns([0.1,0.9])
    with ch_col1:
         loadImage(top_one['channel_image'].iloc[0])
    with ch_col2:
         st.write(f"<h3 style='color:#f29652'>{top_one['channel_name'].iloc[0]}</h3>",unsafe_allow_html=True)
         st.write(top_one['channel_description'].iloc[0])
         st.write(f"<b style='color:#f29652'>Videos:</b> {top_one['channel_video_count'].iloc[0]}",unsafe_allow_html=True)
    

def question_three():
    st.write(constant.QUESTION_3)
    query = ("SELECT DISTINCT ch.channel_name,v.video_name,v.view_count,v.thumbnail FROM channel ch JOIN playlist pl" 
             " ON ch.channel_id = pl.channel_id "
             "JOIN videos v ON v.playlist_id = pl.playlist_id order by v.view_count DESC LIMIT 10")
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    for index in result_data.index:
             ch_col1,ch_col2,ch_col3 = st.columns([0.05,0.1,0.85])
             with ch_col1:
                count = index+1
                print(count)
                st.write(f"<b style='color:#f29652'>{count}.</b>",unsafe_allow_html=True)
             with ch_col2:
                loadImage(result_data['thumbnail'][index])
             with ch_col3:
                st.write(f"<b style='color:#f29652'>Video Name:</b> {result_data['video_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Channel Name:</b> {result_data['channel_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Views:</b> {result_data['view_count'][index]}",unsafe_allow_html=True)
             st.divider()         
   

def question_four():
    st.write(constant.QUESTION_4)
    query =("SELECT DISTINCT v.video_name,v.comment_count,v.thumbnail FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             "  JOIN videos v ON v.playlist_id = pl.playlist_id")
    result_data = db.read_data(query)
    rows = result_data.shape[0]
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Record Found : ",rows)
    for i in range(0, len(result_data), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(result_data):
                videoInfo = result_data.iloc[i + j]
                col.image(videoInfo['thumbnail'],width=100)
                limited_string = (videoInfo['video_name'][:50] + '...') if len(videoInfo['video_name']) > 30 else videoInfo['video_name']
                col.write(f"<b style='color:#f29652'>Video Name:</b>{limited_string}",unsafe_allow_html=True)
                comment_count = 0
                if pd.notna(videoInfo['comment_count']):
                    comment_count = int(videoInfo['comment_count'])
                col.write(f"<b style='color:#f29652'>Comments: </b>{comment_count}",unsafe_allow_html=True)
                col.write("________________________________________")
      

def question_five():
    st.write(constant.QUESTION_5)
    query = ("SELECT DISTINCT ch.channel_name,v.video_name,v.like_count,v.thumbnail FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id order by v.like_count desc LIMIT 1") 
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    ch_col1,ch_col2 = st.columns([0.1,0.9])
    with ch_col1:
         loadImage(result_data['thumbnail'].iloc[0])
    with ch_col2:
         st.write(f"<b style='color:#f29652'>Video Name: </b>{result_data['video_name'].iloc[0]}",unsafe_allow_html=True)
         st.write(f"<b style='color:#f29652'>Channel Name: </b>{result_data['channel_name'].iloc[0]}",unsafe_allow_html=True)
         st.write(f"<b style='color:#f29652'>likes: </b> {result_data['like_count'].iloc[0]}",unsafe_allow_html=True)
       

def question_six():
    st.write(constant.QUESTION_6)
    query = ("SELECT DISTINCT v.video_name,v.like_count,v.thumbnail FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id ") 
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Record: ",result_data.shape[0])
    for i in range(0, len(result_data), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(result_data):
                videoInfo = result_data.iloc[i + j]
                col.image(videoInfo['thumbnail'],width=100)
                limited_string = (videoInfo['video_name'][:50] + '...') if len(videoInfo['video_name']) > 30 else videoInfo['video_name']
                col.write(f"<b style='color:#f29652'>Video Name:</b>{limited_string}",unsafe_allow_html=True)
                like_count = 0
                if pd.notna(videoInfo['like_count']):
                    like_count = int(videoInfo['like_count'])
                col.write(f"<b style='color:#f29652'>Likes: </b>{like_count}",unsafe_allow_html=True)
                col.write("________________________________________")
         

def question_seven():
    st.write(constant.QUESTION_7)
    query = ("SELECT DISTINCT channel_name, channel_description,channel_views,channel_image from channel") 
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    for index in result_data.index:
             ch_col1,ch_col2,ch_col3 = st.columns([0.05,0.1,0.85])
             with ch_col1:
                count = index+1
                print(count)
                st.write(f"<b style='color:#f29652'>{count}.</b>",unsafe_allow_html=True)
             with ch_col2:
                if pd.notna(result_data['channel_image'][index]):
                    loadImage(result_data['channel_image'][index])
                else:
                    loadImage("https://img.icons8.com/color/48/youtube-play.png")
                
             with ch_col3:
                st.write(f"<b style='color:#f29652'>Channel Name: </b> {result_data['channel_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Description: </b> {result_data['channel_description'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Views:</b> {result_data['channel_views'][index]}",unsafe_allow_html=True)
             st.divider()   

def question_eight():
    st.write(constant.QUESTION_8)
    query = ("SELECT distinct ch.channel_id,ch.channel_image,ch.channel_name,v.video_name,v.published_date FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id where" 
             " Year(STR_TO_DATE(v.published_date, '%Y-%m-%dT%H:%i:%sZ')) = 2022") 
    result_data = db.read_data(query)
    result_data = result_data.drop_duplicates(['channel_id'],ignore_index=True)
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Found: ",result_data.shape[0])
    for index in result_data.index:
             ch_col1,ch_col2,ch_col3 = st.columns([0.05,0.1,0.85])
             with ch_col1:
                count = index+1
                print(count)
                st.write(f"<b style='color:#f29652'>{count}.</b>",unsafe_allow_html=True)
             with ch_col2:
                if pd.notna(result_data['channel_image'][index]):
                    loadImage(result_data['channel_image'][index])
                else:
                    loadImage("https://img.icons8.com/color/48/youtube-play.png")
                
             with ch_col3:
                st.write(f"<b style='color:#f29652'>Channel Name: </b> {result_data['channel_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Video Name: </b> {result_data['video_name'][index]}",unsafe_allow_html=True)
             st.divider()    

def question_nine():
    st.write(constant.QUESTION_9)
    query = ("SELECT ch.channel_id,ch.channel_name,ch.channel_image,ch.channel_description,v.video_name,v.duration FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id")
    result_data = db.read_data(query)
    data_cleaned = result_data.dropna(subset=['duration'])
    
    data_cleaned['Duration(In Seconds)'] = data_cleaned['duration'].apply(YTDurationToSeconds)
    average_duration = data_cleaned.groupby('channel_id')['Duration(In Seconds)'].mean().reset_index()
    average_duration["Duration(H:MM:SSS)"] = data_cleaned['Duration(In Seconds)'].apply(convert_seconds_to_hms)
    st.markdown(original_title, unsafe_allow_html=True)
    merge = pd.merge(result_data,average_duration,on='channel_id',how='inner')
    average_duration = merge.drop_duplicates("channel_id").reset_index(drop=True)
    for index in average_duration.index:
             ch_col1,ch_col2,ch_col3 = st.columns([0.05,0.1,0.85])
             with ch_col1:
                count = index+1
                print(count)
                st.write(f"<b style='color:#f29652'>{count}.</b>",unsafe_allow_html=True)
             with ch_col2:
                if pd.notna(average_duration['channel_image'][index]):
                    loadImage(average_duration['channel_image'][index])
                else:
                    loadImage("https://img.icons8.com/color/48/youtube-play.png")
                
             with ch_col3:
                st.write(f"<b style='color:#f29652'>Channel Name: </b> {average_duration['channel_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Description: </b> {average_duration['channel_description'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Duration (HH:MM:SSS):</b> {average_duration['Duration(H:MM:SSS)'][index]}",unsafe_allow_html=True)
             st.divider()  


def question_ten():
    st.write(constant.QUESTION_10)
    query =("SELECT ch.channel_name,v.thumbnail,v.video_name,v.comment_count,v.video_description FROM channel ch" 
            " JOIN playlist pl ON ch.channel_id = pl.channel_id"
            " JOIN videos v ON v.playlist_id = pl.playlist_id order by v.comment_count desc LIMIT 1") 
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    for index in result_data.index:
             ch_col1,ch_col2,ch_col3 = st.columns([0.05,0.1,0.85])
             with ch_col1:
                count = index+1
                print(count)
                st.write(f"<b style='color:#f29652'>{count}.</b>",unsafe_allow_html=True)
             with ch_col2:
                loadImage(result_data['thumbnail'][index])
             with ch_col3:
                st.write(f"<b style='color:#f29652'>Video Name:</b> {result_data['video_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Channel Name:</b> {result_data['channel_name'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>comments:</b> {result_data['comment_count'][index]}",unsafe_allow_html=True)
                st.write(f"<b style='color:#f29652'>Video Descriptions:</b> {result_data['video_description'][index]}",unsafe_allow_html=True)
 

def YTDurationToSeconds(duration):
    print(duration)
    if pd.notna(duration):
        match_check = re.match(r'PT((\d+)H)?((\d+)M)?((\d+)S)?', duration)
        if match_check:
           match= match_check.groups()
           hours = int(match[1]) if match[1] else 0
           minutes = int(match[3]) if match[3] else 0
           seconds = int(match[5]) if match[5] else 0
           return hours * 3600 + minutes * 60 + seconds
        else:
            return 0
    else:
        return 0

def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours*3600) // 60
    remaining_seconds = seconds - hours*3600 - minutes*60
    return f"{hours}:{minutes}:{seconds}"
    


