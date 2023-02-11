# Instagram project part 2: Analysis on reels and photos data pulled from part 1 and transfered into a dashboard

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import plotly.express as px
import streamlit as st

print('hkjjh')
# Import Reels data file created in part 1
reels_data = pd.read_csv("Reels_Data.csv")

# Create an index column because for some reason pycharm doesn't understand when we call it
index = []
count = 0
for i in reels_data['id']:
        index.append(count)
        count = count + 1

reels_data.insert(0, 'index', index)

# Create a column that measures the enjoyment: the percentage of viewers that liked the video
reels_data['enjoyment'] = (reels_data['likes']/reels_data['plays']) * 100

# Create a shortened version of the caption columns to make it fit better in the tooltip of the graphs below
reels_data['shortcap'] = reels_data['caption'].str[:25]

# Bar plots for all variables

likesplot = px.bar(reels_data, x="index", y="likes", color="day_of_week", title="Likes", hover_data=['shortcap', 'hour posted', 'hashtags'])

# likesplot.show()

enjoyplot = px.bar(reels_data, x="index", y="enjoyment", color="day_of_week", title="Enjoyment", hover_data=['shortcap', 'hour posted', 'hashtags'])

# enjoyplot.show()

playsplot = px.bar(reels_data, x="index", y="plays", color="day_of_week", title="Plays", hover_data=['shortcap','hour posted', 'hashtags'])

# playsplot.show()

commentsplot = px.bar(reels_data, x="index", y="comments", color="day_of_week", title="Comments", hover_data=['shortcap', 'hour posted', 'hashtags'])

# commentsplot.show()

# count how many reels where posted on each day of the week
postsperday = reels_data.groupby('day_of_week')['index'].count()

# convert pandas series to dataframes
postdailycount = postsperday.to_frame()

# Set index as new column (day_of_week)
postdailycount.reset_index(inplace=True)

# rename 'index' column to 'dailycount'
postdailycount.rename({'index': 'dailycount'}, axis=1, inplace=True)

# set 'dailycount' column as a variable
dailycount = postdailycount['dailycount']

# get the play counts for each day separately, not using this yet
saturdayposts = postdailycount.loc[postdailycount['day_of_week'] == 'Sat']

# get daily average plays
avgdailyplays = reels_data.groupby('day_of_week')['plays'].mean()

# convert pandas series to dataframes
dailyplaysmean = avgdailyplays.to_frame()

# Set index as new column (day_of_week)
dailyplaysmean.reset_index(inplace=True)

# add daily count as a new column
dailyplaysmean['dailycount'] = dailycount

# Reorder index according to day of the week
dailyplaysmean = dailyplaysmean.reindex([1, 5, 6, 4, 0, 2, 3])

# Make a bar plots of average plays per day
dailyplaysplot = px.bar(dailyplaysmean, x="day_of_week", y="plays", title='Average Daily Plays', hover_data=['dailycount'])
# dailyplaysplot.show()

# Extract data from each day of the week separately
sunday = reels_data.loc[reels_data['day_of_week'] == 'Sun']
monday = reels_data.loc[reels_data['day_of_week'] == 'Mon']
tuesday = reels_data.loc[reels_data['day_of_week'] == 'Tues']
wednesday = reels_data.loc[reels_data['day_of_week'] == 'Weds']
thursday = reels_data.loc[reels_data['day_of_week'] == 'Thurs']
friday = reels_data.loc[reels_data['day_of_week'] == 'Fri']
saturday = reels_data.loc[reels_data['day_of_week'] == 'Sat']

# calculate the average of plays per hour each day
meanplayssun = sunday.groupby('hour posted')['plays'].mean()
meanplaysmon = monday.groupby('hour posted')['plays'].mean()
meanplaystues = tuesday.groupby('hour posted')['plays'].mean()
meanplaysweds = wednesday.groupby('hour posted')['plays'].mean()
meanplaysthurs = thursday.groupby('hour posted')['plays'].mean()
meanplaysfri = friday.groupby('hour posted')['plays'].mean()
meanplayssat = saturday.groupby('hour posted')['plays'].mean()

# convert pandas series to dataframes
sunplays = meanplayssun.to_frame()
monplays = meanplaysmon.to_frame()
tuesplays = meanplaystues.to_frame()
wedsplays = meanplaysweds.to_frame()
thursplays = meanplaysthurs.to_frame()
friplays = meanplaysfri.to_frame()
satplays = meanplayssat.to_frame()

# Set index as new column (hour posted), so that it can be used in the barplot
sunplays.reset_index(inplace=True)
monplays.reset_index(inplace=True)
tuesplays.reset_index(inplace=True)
wedsplays.reset_index(inplace=True)
thursplays.reset_index(inplace=True)
friplays.reset_index(inplace=True)
satplays.reset_index(inplace=True)

# calculate the count of plays per hour each day
postcountsun = sunday.groupby('hour posted')['plays'].count()
postcountmon = monday.groupby('hour posted')['plays'].count()
postcounttues = tuesday.groupby('hour posted')['plays'].count()
postcountweds = wednesday.groupby('hour posted')['plays'].count()
postcountthurs = thursday.groupby('hour posted')['plays'].count()
postcountfri = friday.groupby('hour posted')['plays'].count()
postcountsat = saturday.groupby('hour posted')['plays'].count()

# convert pandas series to dataframes
postcsun = postcountsun.to_frame()
postcmon = postcountmon.to_frame()
postctues = postcounttues.to_frame()
postcweds = postcountweds.to_frame()
postcthurs = postcountthurs.to_frame()
postcfri = postcountfri.to_frame()
postcsat = postcountsat.to_frame()

# Rename the column as 'count'
# Set index as new column (hour posted) in order to be able to add it as a new column to the plays charts
# Set the count column as a variable
# Add count column to each day's plays chart
postcsun.rename({'plays': 'count'}, axis=1, inplace=True)
postcsun.reset_index(inplace=True)
count = postcsun['count']
sunplays['count'] = count

postcmon.rename({'plays': 'count'}, axis=1, inplace=True)
postcmon.reset_index(inplace=True)
count = postcmon['count']
monplays['count'] = count

postctues.rename({'plays': 'count'}, axis=1, inplace=True)
postctues.reset_index(inplace=True)
count = postctues['count']
tuesplays['count'] = count

postcweds.rename({'plays': 'count'}, axis=1, inplace=True)
postcweds.reset_index(inplace=True)
count = postcweds['count']
wedsplays['count'] = count

postcthurs.rename({'plays': 'count'}, axis=1, inplace=True)
postcthurs.reset_index(inplace=True)
count = postcthurs['count']
thursplays['count'] = count

postcfri.rename({'plays': 'count'}, axis=1, inplace=True)
postcfri.reset_index(inplace=True)
count = postcfri['count']
friplays['count'] = count

postcsat.rename({'plays': 'count'}, axis=1, inplace=True)
postcsat.reset_index(inplace=True)
count = postcsat['count']
satplays['count'] = count

# Make bar plots of average plays per hour each day
sunplaysplot = px.bar(sunplays, x="hour posted", y="plays", title="Sunday", hover_data=['count'])
# sunplaysplot.show()

monplaysplot = px.bar(monplays, x="hour posted", y="plays", title="Monday", hover_data=['count'])
# monplaysplot.show()

tuesplaysplot = px.bar(tuesplays, x="hour posted", y="plays", title="Tuesday", hover_data=['count'])
# tuesplaysplot.show()

wedsplaysplot = px.bar(wedsplays, x="hour posted", y="plays", title="Wednesday", hover_data=['count'])
# wedsplaysplot.show()

thursplaysplot = px.bar(thursplays, x="hour posted", y="plays", title="Thursday", hover_data=['count'])
# thursplaysplot.show()

friplaysplot = px.bar(friplays, x="hour posted", y="plays", title="Friday", hover_data=['count'])
# friplaysplot.show()

satplaysplot = px.bar(satplays, x="hour posted", y="plays", title='Saturday', hover_data=['count'])
# satplaysplot.show()

# Show all charts in streamlit
# st.plotly_chart(dailyplaysplot, use_container_width=True)
# st.plotly_chart(sunplaysplot, use_container_width=True)
# st.plotly_chart(monplaysplot, use_container_width=True)
# st.plotly_chart(tuesplaysplot, use_container_width=True)
# st.plotly_chart(wedsplaysplot, use_container_width=True)
# st.plotly_chart(thursplaysplot, use_container_width=True)
# st.plotly_chart(friplaysplot, use_container_width=True)
# st.plotly_chart(satplaysplot, use_container_width=True)
# st.plotly_chart(likesplot, use_container_width=True)
# st.plotly_chart(enjoyplot, use_container_width=True)
# st.plotly_chart(commentsplot, use_container_width=True)
# st.plotly_chart(playsplot, use_container_width=True)

# Import Photos data file created in part 1
photos_data = pd.read_csv("Photos_Data.csv")

# Create an index column because for some reason pycharm doesn't understand when we call it
index = []
count = 0
for i in photos_data['id']:
        index.append(count)
        count = count + 1

photos_data.insert(0, 'index', index)


# Create a shortened version of the caption columns to make it fit better in the tooltip of the graphs below
photos_data['shortcap'] = photos_data['caption'].str[:25]

# Bar plots for all variables

likesplot = px.bar(photos_data, x="index", y="likes", color="day_of_week", title="Likes", hover_data=['shortcap', 'hour posted', 'hashtags'])

# likesplot.show()

commentsplot = px.bar(photos_data, x="index", y="comments", color="day_of_week", title="Comments", hover_data=['shortcap', 'hour posted', 'hashtags'])

# commentsplot.show()

# count how many photos where posted on each day of the week
postsperday = photos_data.groupby('day_of_week')['index'].count()

# convert pandas series to dataframes
postdailycount = postsperday.to_frame()

# Set index as new column (day_of_week)
postdailycount.reset_index(inplace=True)

# rename 'index' column to 'dailycount'
postdailycount.rename({'index': 'dailycount'}, axis=1, inplace=True)

# set 'dailycount' column as a variable
dailycount = postdailycount['dailycount']

# get the likes counts for each day separately, not using this yet
saturdayposts = postdailycount.loc[postdailycount['day_of_week'] == 'Sat']

# get daily average plays
avgdailylikes = photos_data.groupby('day_of_week')['likes'].mean()

# convert pandas series to dataframes
dailylikesmean = avgdailylikes.to_frame()

# Set index as new column (day_of_week)
dailylikesmean.reset_index(inplace=True)

# add daily count as a new column
dailylikesmean['dailycount'] = dailycount

# Reorder index according to day of the week
dailyplaysmean = dailylikesmean.reindex([1, 5, 6, 4, 0, 2, 3])

# Make a bar plots of average plays per day
dailylikesplot = px.bar(dailylikesmean, x="day_of_week", y="likes", title='Average Daily Likes', hover_data=['dailycount'])
# dailylikesplot.show()

# Extract data from each day of the week separately
sunday = photos_data.loc[photos_data['day_of_week'] == 'Sun']
monday = photos_data.loc[photos_data['day_of_week'] == 'Mon']
tuesday = photos_data.loc[photos_data['day_of_week'] == 'Tues']
wednesday = photos_data.loc[photos_data['day_of_week'] == 'Weds']
thursday = photos_data.loc[photos_data['day_of_week'] == 'Thurs']
friday = photos_data.loc[photos_data['day_of_week'] == 'Fri']
saturday = photos_data.loc[photos_data['day_of_week'] == 'Sat']

# calculate the average of plays per hour each day
meanlikessun = sunday.groupby('hour posted')['likes'].mean()
meanlikesmon = monday.groupby('hour posted')['likes'].mean()
meanlikestues = tuesday.groupby('hour posted')['likes'].mean()
meanlikesweds = wednesday.groupby('hour posted')['likes'].mean()
meanlikesthurs = thursday.groupby('hour posted')['likes'].mean()
meanlikesfri = friday.groupby('hour posted')['likes'].mean()
meanlikessat = saturday.groupby('hour posted')['likes'].mean()

# convert pandas series to dataframes
sunlikes = meanlikessun.to_frame()
monlikes = meanlikesmon.to_frame()
tueslikes = meanlikestues.to_frame()
wedslikes = meanlikesweds.to_frame()
thurslikes = meanlikesthurs.to_frame()
frilikes = meanlikesfri.to_frame()
satlikes = meanlikessat.to_frame()

# Set index as new column (hour posted), so that it can be used in the barplot
sunlikes.reset_index(inplace=True)
monlikes.reset_index(inplace=True)
tueslikes.reset_index(inplace=True)
wedslikes.reset_index(inplace=True)
thurslikes.reset_index(inplace=True)
frilikes.reset_index(inplace=True)
satlikes.reset_index(inplace=True)

# calculate the count of likes per hour each day
postcountsun = sunday.groupby('hour posted')['likes'].count()
postcountmon = monday.groupby('hour posted')['likes'].count()
postcounttues = tuesday.groupby('hour posted')['likes'].count()
postcountweds = wednesday.groupby('hour posted')['likes'].count()
postcountthurs = thursday.groupby('hour posted')['likes'].count()
postcountfri = friday.groupby('hour posted')['likes'].count()
postcountsat = saturday.groupby('hour posted')['likes'].count()

# convert pandas series to dataframes
postcsun = postcountsun.to_frame()
postcmon = postcountmon.to_frame()
postctues = postcounttues.to_frame()
postcweds = postcountweds.to_frame()
postcthurs = postcountthurs.to_frame()
postcfri = postcountfri.to_frame()
postcsat = postcountsat.to_frame()

# Rename the column as 'count'
# Set index as new column (hour posted) in order to be able to add it as a new column to the plays charts
# Set the count column as a variable
# Add count column to each day's plays chart
postcsun.rename({'likes': 'count'}, axis=1, inplace=True)
postcsun.reset_index(inplace=True)
count = postcsun['count']
sunlikes['count'] = count

postcmon.rename({'likes': 'count'}, axis=1, inplace=True)
postcmon.reset_index(inplace=True)
count = postcmon['count']
monlikes['count'] = count

postctues.rename({'likes': 'count'}, axis=1, inplace=True)
postctues.reset_index(inplace=True)
count = postctues['count']
tueslikes['count'] = count

postcweds.rename({'likes': 'count'}, axis=1, inplace=True)
postcweds.reset_index(inplace=True)
count = postcweds['count']
wedslikes['count'] = count

postcthurs.rename({'likes': 'count'}, axis=1, inplace=True)
postcthurs.reset_index(inplace=True)
count = postcthurs['count']
thurslikes['count'] = count

postcfri.rename({'likes': 'count'}, axis=1, inplace=True)
postcfri.reset_index(inplace=True)
count = postcfri['count']
frilikes['count'] = count

postcsat.rename({'likes': 'count'}, axis=1, inplace=True)
postcsat.reset_index(inplace=True)
count = postcsat['count']
satlikes['count'] = count

# Make bar plots of average plays per hour each day
sunlikesplot = px.bar(sunlikes, x="hour posted", y="likes", title="Sunday", hover_data=['count'])
# sunlikesplot.show()

monlikesplot = px.bar(monlikes, x="hour posted", y="likes", title="Monday", hover_data=['count'])
# monlikesplot.show()

tueslikesplot = px.bar(tueslikes, x="hour posted", y="likes", title="Tuesday", hover_data=['count'])
# tueslikesplot.show()

wedsplaysplot = px.bar(wedslikes, x="hour posted", y="likes", title="Wednesday", hover_data=['count'])
# wedslikesplot.show()

thursplaysplot = px.bar(thurslikes, x="hour posted", y="likes", title="Thursday", hover_data=['count'])
# thurslikesplot.show()

friplaysplot = px.bar(frilikes, x="hour posted", y="likes", title="Friday", hover_data=['count'])
# frilikesplot.show()

satplaysplot = px.bar(satlikes, x="hour posted", y="likes", title='Saturday', hover_data=['count'])
# satlikesplot.show()

# Show all charts in streamlit
# st.plotly_chart(dailylikesplot, use_container_width=True)
# st.plotly_chart(sunlikesplot, use_container_width=True)
# st.plotly_chart(monlikesplot, use_container_width=True)
# st.plotly_chart(tueslikesplot, use_container_width=True)
# st.plotly_chart(wedslikesplot, use_container_width=True)
# st.plotly_chart(thurslikesplot, use_container_width=True)
# st.plotly_chart(frilikesplot, use_container_width=True)
# st.plotly_chart(satlikesplot, use_container_width=True)
# st.plotly_chart(commentsplot, use_container_width=True)

Reelsbutton = st.button("Reels")

Photosbutton = st.button("Photos")

if Reelsbutton:
        # streamlit Title
        st.markdown("<h1 style='text-align: center; color: Black;'>Instagram Dashboard</h1>", unsafe_allow_html=True)

        # total statistics: likes, plays, average enjoyment, comments

        # Reels Data Label
        st.markdown("<h2 style='text-align: center; color: black;'>Reels Data</h2>", unsafe_allow_html=True)
        # total reel statistics: likes, plays, average enjoyment, comment

        # lifetime statistics per post using a drop down menu: likes, plays, enjoyment, comments
        st.markdown("<h4 style='text-align: left; color: black;'>Statistics Per Post</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Statistics per post',
                ('Likes', 'Plays', 'Enjoyment', 'Comments'),
                label_visibility="hidden")
        if option == 'Likes':
                st.plotly_chart(likesplot, use_container_width=True)
        if option == 'Plays':
                st.plotly_chart(playsplot, use_container_width=True)
        if option == 'Enjoyment':
                st.plotly_chart(enjoyplot, use_container_width=True)
        if option == 'Comments':
                st.plotly_chart(commentsplot, use_container_width=True)

        # Daily chart
        st.markdown("<h4 style='text-align: left; color: black;'>Daily Plays</h4>", unsafe_allow_html=True)

        st.plotly_chart(dailyplaysplot, use_container_width=True)

        # Hourly plays per day using a drop down menu: monday-sunday
        st.markdown("<h4 style='text-align: left; color: black;'>Average Hourly Plays</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Average Hourly Plays',
                ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                label_visibility="hidden")
        if option == 'Monday':
                st.plotly_chart(monplaysplot, use_container_width=True)
        elif option == 'Tuesday':
                st.plotly_chart(tuesplaysplot, use_container_width=True)
        elif option == 'Wednesday':
                st.plotly_chart(wedsplaysplot, use_container_width=True)
        elif option == 'Thursday':
                st.plotly_chart(thursplaysplot, use_container_width=True)
        elif option == 'Friday':
                st.plotly_chart(friplaysplot, use_container_width=True)
        elif option == 'Saturday':
                st.plotly_chart(satplaysplot, use_container_width=True)
        elif option == 'Sunday':
                st.plotly_chart(sunplaysplot, use_container_width=True)

if Photosbutton:
        # streamlit Title
        st.markdown("<h1 style='text-align: center; color: Black;'>Instagram Dashboard</h1>", unsafe_allow_html=True)

        # total statistics: likes, comments

        # Photos Data Label
        st.markdown("<h2 style='text-align: center; color: black;'>Photos Data</h2>", unsafe_allow_html=True)
        # total reel statistics: likes, comment

        # lifetime statistics per post using a drop down menu: likes, comments
        st.markdown("<h4 style='text-align: left; color: black;'>Statistics Per Post</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Statistics per post',
                ('Likes', 'Comments'),
                label_visibility="hidden")
        if option == 'Likes':
                st.plotly_chart(likesplot, use_container_width=True)
        if option == 'Comments':
                st.plotly_chart(commentsplot, use_container_width=True)

        # Daily chart
        st.markdown("<h4 style='text-align: left; color: black;'>Daily Likes</h4>", unsafe_allow_html=True)

        st.plotly_chart(dailylikesplot, use_container_width=True)

        # Hourly likes per day using a drop down menu: monday-sunday
        st.markdown("<h4 style='text-align: left; color: black;'>Average Hourly Likes</h4>", unsafe_allow_html=True)

        option = st.selectbox(
                'Average Hourly Likes',
                ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                label_visibility="hidden")
        if option == 'Monday':
                st.plotly_chart(monlikesplot, use_container_width=True)
        elif option == 'Tuesday':
                st.plotly_chart(tueslikesplot, use_container_width=True)
        elif option == 'Wednesday':
                st.plotly_chart(wedslikesplot, use_container_width=True)
        elif option == 'Thursday':
                st.plotly_chart(thurslikesplot, use_container_width=True)
        elif option == 'Friday':
                st.plotly_chart(frilikesplot, use_container_width=True)
        elif option == 'Saturday':
                st.plotly_chart(satlikesplot, use_container_width=True)
        elif option == 'Sunday':
                st.plotly_chart(sunlikesplot, use_container_width=True)

