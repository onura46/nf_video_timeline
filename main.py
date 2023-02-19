import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd
import datetime

st.title( "watchmeforever clip timeline" )

# create variables
directory = "watchmeforever_test/"
num_of_file = 0

all_videos_df = None

# iterate across each video
for filename in os.listdir(directory):
    if filename.endswith("mp4"):
        with open(os.path.join(directory, filename), 'rb') as f:
            video_bytes = f.read()
            num_of_file += 1

            # decode related json
            jsonname = filename.replace("mp4", "info.json")
            jsonfile = json.load(open(os.path.join(directory, jsonname), 'rb'))
            timestamp = jsonfile["timestamp"]
            duration = jsonfile["duration"]
            video_id = jsonfile["id"]
            video_end = timestamp + duration
            decodedtimestamp = str(datetime.datetime.fromtimestamp(timestamp))
            video_real_date = decodedtimestamp[0:10]
            video_year = decodedtimestamp[0:4]
            video_month = decodedtimestamp[5:7]
            video_day = decodedtimestamp[8:10]
            video_hour = decodedtimestamp[11:13]
            video_minute = decodedtimestamp[14:16]
            video_second = decodedtimestamp[17:19]

            video_title = jsonfile["title"]

            file_definitions = {
                "video_id" : video_id,
                "video_title" : video_title,
                "timestamp" : timestamp,
                "video_real_date" : video_real_date,
                "video_year" : video_year,
                "video_month" : video_month,
                "video_day" : video_day,
                "video_hour" : video_hour,
                "video_minute" : video_minute,
                "video_second" : video_second,
                "duration" : duration,
                "video_end" : video_end
            }
            newdef = pd.DataFrame([file_definitions])
            if all_videos_df is None:
                all_videos_df = newdef
            else:
                all_videos_df = pd.concat([all_videos_df,newdef])

st.dataframe(all_videos_df)
graph = px.timeline(all_videos_df, x_start="timestamp", x_end="video_end", y="video_real_date")
st.plotly_chart(graph)
