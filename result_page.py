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


original_title = '<p style="font-family:Courier; color:Green; font-size: 20px;">Answer : </p>'

def loadImage(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    new_width = 300
    new_height = 200
    img_resized = img.resize((new_width, new_height))
    st.image(img_resized)   

def question_one():
    st.write("Question : "+constant.QUESTION_1)
    my_query =("SELECT ch.channel_name,v.video_id,v.video_name,v.view_count,v.like_count,v.dislike_count,"
               "v.comment_count,v.favourite_count FROM channel ch JOIN playlist pl ON ch.channel_id = pl.channel_id"
               " JOIN videos v ON v.playlist_id = pl.playlist_id ")
    result = db.read_data(my_query)
    result =result.drop_duplicates(['video_id'])
    rows = result.shape[0]
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Record Found : ",rows)
    st.write(result)
    
    print("question one")

def question_two():
    st.write("Question : "+constant.QUESTION_2)
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
    st.write("Question : "+constant.QUESTION_3)
    query = ("SELECT DISTINCT ch.channel_name,v.video_name,v.view_count FROM channel ch JOIN playlist pl" 
             " ON ch.channel_id = pl.channel_id "
             "JOIN videos v ON v.playlist_id = pl.playlist_id order by v.view_count")
    result_data = db.read_data(query)
    first_resul = result_data.sort_values('view_count',ascending=False)
    print(result_data.info())
    st.markdown(original_title, unsafe_allow_html=True)
    st.write(first_resul.head(10).reset_index(drop=True) )
    for videoItem in len(first_resul.head(10)):
         ch_col1,ch_col2 = st.columns([0.1,0.9])
         with ch_col1:
              loadImage(first_resul[videoItem].iloc[0].iloc[0])
         with ch_col2:
            st.write(f"<h3 style='color:#f29652'>{top_one['channel_name'].iloc[0]}</h3>",unsafe_allow_html=True)
            st.write(top_one['channel_description'].iloc[0])
            st.write(f"<b style='color:#f29652'>Videos:</b> {top_one['channel_video_count'].iloc[0]}",unsafe_allow_html=True)
    
   

def question_four():
    st.write("Question : "+constant.QUESTION_4)
    query =("SELECT DISTINCT v.video_name,v.comment_count FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             "  JOIN videos v ON v.playlist_id = pl.playlist_id")
    result_data = db.read_data(query)
    rows = result_data.shape[0]
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Record Found : ",rows)
    st.write(result_data)
    print("")   

def question_five():
    st.write("Question : "+constant.QUESTION_5)
    query = ("SELECT DISTINCT ch.channel_name,v.video_name,v.like_count FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id order by v.like_count desc LIMIT 10") 
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    st.write(result_data.head(1))
    print("")    

def question_six():
    st.write("Question : "+constant.QUESTION_6)
    query = ("SELECT DISTINCT ch.channel_name,v.video_name,v.like_count,v.dislike_count FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id ") 
    result_data = db.read_data(query)
    print(result_data.info())
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total Record: ",result_data.shape[0])
    st.write(result_data)
    print("")    

def question_seven():
    st.write("Question : "+constant.QUESTION_7)
    query = ("SELECT DISTINCT channel_name, channel_views from channel") 
    result_data = db.read_data(query)
    print(result_data.info())
    st.markdown(original_title, unsafe_allow_html=True)
    st.write(result_data)
    bars=  plt.bar(result_data['channel_name'], result_data['channel_views'],color = "#4CAF50")
    for bar in bars:
        yval = bar.get_height()
    plt.text(bar.get_x()+0.05, yval+20, yval)
    plt.xlabel('Channel Name')
    plt.xticks(rotation=90)
    plt.ylabel("Number of Views")
    plt.title('Channel Views')
    st.pyplot(plt.gcf())      

def question_eight():
    st.write("Question : "+constant.QUESTION_8)
    query = ("SELECT ch.channel_id,ch.channel_name,v.video_name,v.published_date FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id where" 
             " Year(STR_TO_DATE(v.published_date, '%Y-%m-%dT%H:%i:%sZ')) = 2022") 
    result_data = db.read_data(query)
    result_data = result_data.drop_duplicates(['channel_id'],ignore_index=True)
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("Total found: ",result_data.shape[0])
    st.write(result_data)  

def question_nine():
    st.write("Question : "+constant.QUESTION_9)
    query = ("SELECT ch.channel_id,ch.channel_name,v.video_name,v.duration FROM channel ch" 
             " JOIN playlist pl ON ch.channel_id = pl.channel_id"
             " JOIN videos v ON v.playlist_id = pl.playlist_id")
    result_data = db.read_data(query)
    data_cleaned = result_data.dropna(subset=['duration'])
    data_cleaned['Duration(In Seconds)'] = data_cleaned['duration'].apply(YTDurationToSeconds)
    average_duration = data_cleaned.groupby('channel_name')['Duration(In Seconds)'].mean().reset_index()
    average_duration["Duration(H:MM:SSS)"] = data_cleaned['Duration(In Seconds)'].apply(convert_seconds_to_hms)
    st.markdown(original_title, unsafe_allow_html=True)
    st.write(average_duration) 


def question_ten():
    st.write("Question : "+constant.QUESTION_10)
    query =("SELECT ch.channel_name,v.video_name,v.comment_count FROM channel ch" 
            " JOIN playlist pl ON ch.channel_id = pl.channel_id"
            " JOIN videos v ON v.playlist_id = pl.playlist_id order by v.comment_count desc LIMIT 1") 
    result_data = db.read_data(query)
    st.markdown(original_title, unsafe_allow_html=True)
    st.write(result_data)  

# def show_graph_view():
#     if(top_five.shape[0]<10):
#        bars=  plt.bar(top_five['channel_name'], top_five['channel_video_count'],color = "#4CAF50")
#        for bar in bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x()+0.05, yval+20, yval)
#        plt.xlabel('Channel Name')
#        plt.xticks(rotation=90)
#        plt.ylabel("Number of Videos")
#        plt.title('Top 5 channels with the most videos')
#        st.pyplot(plt.gcf()) 
#     print("")


def YTDurationToSeconds(duration):
    match = re.match('PT((\d+)H)?((\d+)M)?((\d+)S)?', duration).groups()
    hours = int(match[1]) if match[1] else 0
    minutes = int(match[3]) if match[3] else 0
    seconds = int(match[5]) if match[5] else 0
    return hours * 3600 + minutes * 60 + seconds

def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours*3600) // 60
    remaining_seconds = seconds - hours*3600 - minutes*60
    return f"{hours}:{minutes}:{seconds}"
    


