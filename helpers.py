import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap


# Convert time string in format HH:MM:SS to seconds
def time_string_to_secs(time_string):
    time_string = time_string.split(':')
    return (int(time_string[0]) * 3600) + (int(time_string[1]) * 60) + int(time_string[2])


def time_string_to_mins(time_string):
    time_string = time_string.split(':')
    return (int(time_string[0]) * 3600) + int(time_string[1])


def time_string_to_hours(time_string):
    time_string = time_string.split(':')
    return float(time_string[0]) + float(time_string[1]) / 60


# Convert seconds to string in format HH:MM:SS
def get_watch_time(seconds):
    hours = seconds // 3600
    seconds -= 3600 * hours
    minutes = seconds // 60
    seconds -= 60 * minutes
    return "%d:%02d:%02d" % (hours, minutes, seconds)


# Get series name by removing everything starting with the "Season", "Book" or "Episode" suffix
def get_clean_series_name(title):
    suffixes = [
        " (Season", ": Season", ": Part", ": Book", " (Chapter ", ': Chapter', ' (Episode', ': Episode',
        ' (Temporada', ': Temporada', ': Parte', ': Libro', " (Episodio", ': Episodio', ' (Capítulo ', ": Capítulo"
    ]

    for s in suffixes:
        suffix_index = title.find(s)
        if s == ': Episodio':
            a = True
        if suffix_index != -1:
            clean_title = title[:suffix_index]
            return clean_title


def graph_top_shows(shows, qty, title="", ylabel="", width=15, height=6, ):
    sns.set_style('darkgrid')
    fig = plt.figure(figsize=(width, height))
    sns.set_context('notebook', font_scale=1, rc={"grid.linewidth": 2})

    plt.bar(shows, qty, color=['#C0392B', '#D35400', '#E67E22', '#F39C12', '#F1C40F'])
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(shows, rotation=3)

    st.pyplot(fig)


def adjust_df_columns(df):
    cpdf = df.copy()
    cpdf.columns = ['name', 'start', 'duration', 'attrs', 'title', 'svt', 'device', 'bookmark', 'latestbookmark',
                    'country']
    cpdf = cpdf.drop(['attrs', 'svt', 'bookmark', 'latestbookmark'], axis=1)

    # Add columns that indicate show duration in minutes and seconds
    cpdf['duration_mins'] = cpdf.duration.map(time_string_to_mins)
    cpdf['duration_secs'] = cpdf.duration.map(time_string_to_secs)

    return cpdf


def filter_by_profile_and_duration(df, profile_name):
    cpdf = df.copy()
    cpdf = cpdf.loc[cpdf.name == profile_name]
    cpdf = cpdf.loc[cpdf.duration_mins >= 5]
    return cpdf


class AccountLongevity:
    def __init__(self, dates):
        date_str_format = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.datetime.strptime(dates.head(1).values[0], date_str_format)
        d2 = datetime.datetime.strptime(dates.tail(1).values[0], date_str_format)

        self.time = d2 - d1
        self.years = self.time.days // 365
        self.months = (self.time.days - (self.years * 365)) // 30
        self.days = self.time.days - (self.years * 365) - (self.months * 30)
        self.start = dates.head(1).values[0].split(" ")[0]
        self.end = dates.tail(1).values[0].split(" ")[0]


def get_first_show_info(df, dates):
    first_show_index = dates.head().index[0]
    first_show = df.loc[first_show_index].title
    first_show_date = df.loc[first_show_index].start.split(' ')[0]
    return first_show, first_show_date


def get_top_played_content(df):
    df.loc[:, 'plays'] = df.title.map(df.title.value_counts())
    df.loc[:, 'count'] = 1
    sorted_by_plays = df.loc[df.title.duplicated() == False]
    sorted_by_plays = sorted_by_plays.sort_values('plays', ascending=False)
    return sorted_by_plays


def get_top_movies(df):
    ts = df.title.str
    # Remove content which title indicates that is part of a series
    non_series_df = pd.DataFrame(
        df.loc[
            ~ts.contains(': Season') & ~ts.contains(': Book') & ~ts.contains(': Part') & ~ts.contains(
                ' \(Episode') & ~ts.contains(': Episode') & ~ts.contains(' \(Chapter ') & ~ts.contains(
                ': Chapter') & ~ts.contains(': Temporada ') & ~ts.contains(': Libro') & ~ts.contains(
                ' \(Capítulo') & ~ts.contains(': Capítulo') & ~ts.contains(': Parte') & ~ts.contains(
                ': Episodio ') & ~ts.contains(" \(Episodio ")
            ])

    # Sort by number of plays
    non_series_df.loc[:, 'plays'] = df.title.map(df.title.value_counts())
    non_series_df = non_series_df.loc[non_series_df.title.duplicated() == False]
    non_series_df = non_series_df.sort_values('plays', ascending=False)
    return non_series_df


# TODO: Check if dataset complement solves this
# Analyze TV Series (Content with multiple episodes)
# Select content which name indicates that it's a series
# seriesDf = df[~df.isin(nonSeriesDf).all(1)]
def get_series_df(df):
    ts = df.title.str
    return pd.DataFrame(
        df.loc[
            ts.contains(': Season') | ts.contains(': Book') | ts.contains(': Part') | ts.contains(' \(Episode')
            | ts.contains(': Episode') | ts.contains(' \(Chapter ') | ts.contains(': Chapter')
            | ts.contains(': Temporada ') | ts.contains(': Libro') | ts.contains(' \(Capítulo')
            | ts.contains(': Capítulo') | ts.contains(': Parte') | ts.contains(': Episodio ')
            | ts.contains(" \(Episodio ")
            ])


def get_top_series_by_play_count(series_df):
    top_watched_series_by_plays = pd.DataFrame(series_df)
    top_watched_series_by_plays.loc[:, 'plays'] = top_watched_series_by_plays.title.map(
        top_watched_series_by_plays.title.value_counts())
    top_watched_series_by_plays = top_watched_series_by_plays \
        .loc[top_watched_series_by_plays.title.duplicated() == False]
    top_watched_series_by_plays = top_watched_series_by_plays.sort_values('plays', ascending=False)
    return top_watched_series_by_plays


def get_top_series_by_episodes_played(series_df):
    top_watched_by_episodes = pd.DataFrame(series_df.loc[series_df.title.duplicated() == False])
    top_watched_by_episodes.title = top_watched_by_episodes.title.map(get_clean_series_name)
    series_df.title = series_df.title.map(get_clean_series_name)
    top_watched_by_episodes.loc[:, 'plays'] = top_watched_by_episodes.title.map(
        top_watched_by_episodes.title.value_counts()
    )
    top_watched_by_episodes = top_watched_by_episodes.loc[top_watched_by_episodes.title.duplicated() == False]
    top_watched_by_episodes = top_watched_by_episodes.sort_values('plays', ascending=False)
    return top_watched_by_episodes


def get_top_series_by_watch_time(series_df):
    # get sum of watched time
    top_watched_series = series_df.groupby(['title'])['duration_secs'].sum()
    top_watched_series_df = pd.DataFrame(
        {
            'title': top_watched_series.index,
            'duration_secs': top_watched_series.values
        }
    ).sort_values('duration_secs', ascending=False)
    top_watched_series_df['duration_mins'] = top_watched_series_df.duration_secs / 60
    top_watched_series_df['duration_hours'] = top_watched_series_df.duration_mins / 60
    return top_watched_series_df


def add_day_and_hour_columns(df):
    # Watch events by weekday and hour of day
    df.start = pd.to_datetime(df.start, utc=True)
    df = df.set_index('start')
    df.index = df.index.tz_convert('America/Mexico_City')
    df = df.reset_index()
    df['day'] = df.start.dt.weekday
    df['hour'] = df.start.dt.hour
    # set days Monday-Sunday
    df['day'] = pd.Categorical(df['day'], categories=list(range(7)), ordered=True)
    return df


def create_df_per_day(df):
    # create data per day and sort by day using sort_index function
    df_per_day = df['day'].value_counts().sort_index()
    # print(df_per_day)
    return df_per_day


def create_df_per_hour(df):
    # set hours of day as numeric values
    df['hour'] = pd.Categorical(df['hour'], categories=list(range(24)), ordered=True)
    # create data per hour and sort by hour using sort_index function
    df_per_hour = df['hour'].value_counts().sort_index()
    # print(df_per_hour)
    return df_per_hour


def graph_watch_times(df):
    out = df.groupby(['day', 'hour'])['count'].sum().unstack()
    out.sum().sum()
    heatmap_fig = plt.figure(figsize=(16, 8))
    plt.title('Shows iniciados por día de la semana y hora', fontsize=20)
    ax = sns.heatmap(out, linewidths=1, square=True, yticklabels=['L', 'M', 'M', 'J', 'V', 'S', 'D'], cmap='flare',
                     annot=True, fmt='g')
    plt.xlabel('Hora', fontsize=15)
    plt.ylabel('Día de la semana', fontsize=15)
    ax.invert_yaxis()
    st.pyplot(heatmap_fig)
