import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
from helpers import *

#
# Streamlit page Start
#
st.title('Create your Netflix Viewing Activity Infographic')
st.text('This app will help you create a custom infographic for your Netflix Viewing Activity')
file = st.file_uploader('Upload the "ViewingActivity.csv from your Netflix data export"')

if file is None:
    st.stop()

df = None
try:
    df = pd.read_csv(file)
except Exception as e:
    st.text('There was a problem processing the file. Please verify the file format.')
    st.stop()

df = adjust_df_columns(df)

# Select a Netflix profile to analyze
profile_name = st.selectbox('Select a profile', df.name.unique())

# Keep only shows watched by the selected profile and for more than 5 minutes
df = filter_by_profile_and_duration(df, profile_name)

#
# General stats
#

total_watch_time = get_watch_time(df.duration_secs.sum()).split(':')
dates = df.start.sort_values()
account_longevity = AccountLongevity(dates)
watch_hours_per_week = int(total_watch_time[0]) / (account_longevity.days / 7)
first_show_info = get_first_show_info(df, dates)

top_played_content = get_top_played_content(df)
top_movies = get_top_movies(df)
series_df = get_series_df(df)
top_watched_series_by_plays = get_top_series_by_play_count(series_df)
top_watched_by_episodes = get_top_series_by_episodes_played(series_df)
top_watched_series = get_top_series_by_watch_time(series_df)

#
# Top shows charts
#
graph_top_shows(top_watched_by_episodes.head().title, top_watched_by_episodes.head().plays, 'Top Series por Episodios',
                'Episodios')
graph_top_shows(top_watched_series.head().title, top_watched_series.head().duration_hours, 'Top Series por Horas',
                'Horas')
graph_top_shows(top_movies.head().title, top_movies.head().plays, 'Top Películas', 'Veces Vista')

#
# Common watching times
#
df = add_day_and_hour_columns(df)
df_per_day = create_df_per_day(df)
df_per_hour = create_df_per_hour(df)

# Most watch time heatmap
graph_watch_times(df)

#
# Summary Image
#
im = Image.open('img/template.jpeg')
sns.set_context('poster', font_scale=1, rc={"grid.linewidth": 0})
# plt.axes([0.0, 0.0, 1.5, 3.3])
plt.axes([0.0, 0.0, 1, 2])
plt.axis('off')

draw = ImageDraw.Draw(im)

font_type = {
    'medium': 'fonts/Montserrat-Medium.ttf',
    'bold': 'fonts/Montserrat-Bold.ttf'
}

font = ImageFont.truetype(font_type['bold'], 65)
# Total hours
draw.text((120, 530), f'{int(total_watch_time[0]):,}', font=font, fill='white')
# Hours per week
draw.text((680, 630), f'{watch_hours_per_week:.1f}', font=font, fill='white')
# Account age
font = ImageFont.truetype(font_type['bold'], 55)
account_age_x = 345
draw.text((account_age_x, 1360), f'{account_longevity.years} años {account_longevity.months} meses', font=font,
          fill='white')
font = ImageFont.truetype(font_type['medium'], 35)
draw.text((account_age_x, 1430), f'Desde {account_longevity.start}', font=font, fill='white')

# Top movie
top_movie = top_movies.head(1)
top_movie_title = top_movie.title.values[0]

font = ImageFont.truetype(font_type['bold'], 45)
lines = textwrap.wrap(top_movie_title, width=22)
top_movie_x = 425
draw.text((top_movie_x, 330), lines[0], font=font, fill='white')
if len(lines) > 1:
    draw.text((top_movie_x, 380), lines[1], font=font, fill='white')
font = ImageFont.truetype(font_type['medium'], 32)
if len(lines) == 1:
    draw.text((top_movie_x, 385), f'{top_movie.head(1).plays.values[0]} reproducciones', font=font, fill='white')
else:
    draw.text((top_movie_x, 435), f'{top_movie.head(1).plays.values[0]} reproducciones', font=font, fill='white')

# Top series
top_series = top_watched_series.head(1)
top_series_title = top_series.head(1).title.values[0]
# st.dataframe(topWatchedSeriesByPlays)
top_series_by_plays = top_watched_series_by_plays.loc[top_watched_series_by_plays.title == top_series_title]
top_series_by_episodes = top_watched_by_episodes.loc[top_watched_by_episodes.title == top_series_title]
font = ImageFont.truetype(font_type['bold'], 45)
lines = textwrap.wrap(top_series_title, width=18)
top_series_x = 55
draw.text((top_series_x, 920), lines[0], font=font, fill='white')
if len(lines) > 1:
    draw.text((top_series_x, 970), lines[1], font=font, fill='white')
font = ImageFont.truetype(font_type['medium'], 35)
if len(lines) == 1:
    draw.text((top_series_x, 980), f'{top_series.duration_hours.values[0]:.0f} Horas', font=font, fill='white')
    draw.text((top_series_x, 1025), f'{top_series_by_plays.plays.values[0]} reproducciones', font=font, fill='white')
    draw.text((top_series_x, 1070), f'{top_series_by_episodes.plays.values[0]} episodios', font=font, fill='white')
else:
    draw.text((top_series_x, 1030), f'{top_series.duration_hours.values[0]:.0f} Horas', font=font, fill='white')
    draw.text((top_series_x, 1075), f'{top_series_by_plays.plays.values[0]} reproducciones', font=font, fill='white')
    draw.text((top_series_x, 1120), f'{top_series_by_episodes.plays.values[0]} episodios', font=font, fill='white')

# First content
font = ImageFont.truetype(font_type['bold'], 45)
first_show_x = 435
lines = textwrap.wrap(first_show_info[0], width=21)
draw.text((first_show_x, 1110), lines[0], font=font, fill='white')
if len(lines) > 1:
    draw.text((first_show_x, 1160), lines[1], font=font, fill='white')
if len(lines) > 2:
    draw.text((first_show_x, 1210), lines[2], font=font, fill='white')

st.image(im)
