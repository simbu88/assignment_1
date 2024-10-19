import googleapiclient.discovery
import streamlit as st
import my_constant as constant
import pandas as pd
import database as db


try:
    youtube = googleapiclient.discovery.build(
         constant.YOUTUBE_API_SERVICE_NAME,  constant.YOUTUBE_API_VERSION, developerKey = constant.YOUTUBE_DEVELOPER_KEY)
except:
    print("Youtube api crdential is missing")



def get_channel_details(channelId):
        original_data = None
        needed_column = ['id','snippet.title','snippet.description','statistics.viewCount','statistics.subscriberCount','statistics.videoCount'] 
        column_rename = ["channel_id","channel_name","channel_description","channel_views","channel_subscriber_count","channel_video_count"]
        channel_request = youtube.channels().list( 
        part='snippet,statistics', 
        id=channelId) # Query execution
        response = channel_request.execute()
        if  'items' in response:
            original_data = pd.json_normalize(response['items'])[needed_column]
            original_data.columns = column_rename
            return original_data
        else:
            return None    
        
       


def get_playlist_details(channelId): 
    insert_channel_table(channelId)
    video_list = pd.DataFrame()
    needed_column = ['id','snippet.channelId','snippet.title','snippet.description'] 
    column_rename = ['playlist_id','channel_id','playlist_title','description']       
    pl_request = youtube.playlists().list( 
        part='snippet',
        channelId=channelId, 
        maxResults=50
    ) 
    pl_response = pl_request.execute()
    original_data = pd.json_normalize(pl_response['items'])[needed_column]
    original_data.columns = column_rename
    db.insert_into_db("playlist",original_data)
    for playlist_id in original_data['playlist_id']:
        print("playlist_id ",playlist_id)
        video_list= pd.concat([video_list,get_video_list(playlist_id)],ignore_index=True) 
    
    get_video_details(video_list)
    
    

def get_video_list(playlist_Id):
    needed_column = ['snippet.playlistId','snippet.resourceId.videoId'] 
    column_rename = ['playlist_id','video_id'] 
    nextPageToken = None
    all_videos = []
    original_data = pd.DataFrame()
    while True:
        video_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_Id,
        maxResults=50,
        pageToken=nextPageToken
        )
        video_list_response = video_request.execute()
        if  'items' in video_list_response:
            for item in video_list_response['items']:
                all_videos.append(item)
            nextPageToken = video_list_response.get('nextPageToken')
        if not nextPageToken: 
           break        
        else:
           print("") 
    if len(all_videos) > 0:    
       original_data=pd.json_normalize(all_videos)[needed_column]
       original_data.columns = column_rename
    return original_data
   

def get_video_details(video_data):
    needed_column = ['id','snippet.title','snippet.description','snippet.publishedAt','statistics.viewCount','statistics.likeCount','statistics.dislikeCount','statistics.favoriteCount','statistics.commentCount','contentDetails.duration','snippet.thumbnails.default.url'] 
    column_rename = ['video_id','video_name','video_description','published_date','view_count','like_count','dislike_count','favourite_count','comment_count','duration','thumbnail'] 
    start_index = 0
    all_videos = []
    comments_list = pd.DataFrame()
    while start_index < len(video_data):
        end_index = start_index + 50
        video_list_ids = ','.join(video_data.iloc[start_index:end_index]['video_id'])
        request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        maxResults=50, 
        id=video_list_ids
        )
        video_response = request.execute()
        for item in video_response['items']:
            if "dislikeCount" not in item['statistics']:
                item['statistics']["dislikeCount"] = 0
            if "dislikeCount" not in item['statistics']:
                item['statistics']["dislikeCount"] = 0    
            all_videos.append(item)

        start_index += 50

    original_data=pd.json_normalize(all_videos)[needed_column]
    original_data.columns = column_rename
    combine_data = pd.merge(video_data, original_data, on='video_id',how="right")     
    db.insert_into_db("videos",combine_data)
   
    # after_duplicat_removed = combine_data.drop_duplicates(['video_id'])
    # remove_empty_comment_video = after_duplicat_removed.drop(after_duplicat_removed[after_duplicat_removed['comment_count'] ==0].index)
    # for vide_id in remove_empty_comment_video['video_id']:
    #     comments_list= pd.concat([comments_list,get_video_comment(vide_id)],ignore_index=True) 
    # db.insert_into_db("comments",comments_list)


def get_video_comment(videoId):
    needed_column = ['snippet.videoId','snippet.topLevelComment.id','snippet.topLevelComment.snippet.textDisplay','snippet.topLevelComment.snippet.authorDisplayName','snippet.topLevelComment.snippet.authorProfileImageUrl','snippet.topLevelComment.snippet.authorChannelUrl','snippet.topLevelComment.snippet.authorChannelId.value','snippet.topLevelComment.snippet.publishedAt']
    column_rename = ['video_id','commen_id','comments','author_name','author_profile_imageUrl','author_channel_url','author_channelId','publishedAt'] 
    nextPageToken = None
    all_comments = []
    original_comments = pd.DataFrame()
    while True:
        try:
            request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=videoId,
            maxResults=100,
            pageToken=nextPageToken,
            textFormat= "plainText"
            )
            comment_response = request.execute()
            
            for item in comment_response['items']:
                all_comments.append(item)

            nextPageToken = comment_response.get('nextPageToken')
            if not nextPageToken: 
                break
            original_comments=pd.json_normalize(all_comments)[needed_column]
            original_comments.columns = column_rename
        except googleapiclient.errors.HttpError as e:
            print("exception:",e.error_details)
    
    return original_comments

def insert_channel_table(channelId):
     channelItem = get_channel_details(channelId) 
     db.insert_into_db("channel",channelItem)   

   