import streamlit as st
from wordcloud import WordCloud

from helpers import *
from infographic import get_infographic

#
# Streamlit page Start
#
st.title('Crea una infografía de tu actividad en Netflix')
st.subheader('Para crear tu infografía solo necesitas subir el archivo "ViewingActivity.csv" que se encuentra en tu'
             'reporte de datos de Netflix.')
st.subheader('Puedes obtener tu reporte de datos de Netflix en el siguiente enlace')
st.markdown('#### [https://www.netflix.com/account/getmyinfo](https://www.netflix.com/account/getmyinfo)')
file = st.file_uploader('Sube el archivo "ViewingActivity.csv de tu reporte de datos de Netflix"')

if file is None:
    st.stop()

df = None
try:
    df = pd.read_csv(file)
except Exception as e:
    st.text('Hubo un problema procesando el archivo. Por favor verifica que sea el formato correcto.')
    st.stop()

df = adjust_df_columns(df)

# Select a Netflix profile to analyze
st.markdown('##### Selecciona un perfil de tu cuenta de Netflix para generar tu infografía')
profile_name = st.selectbox('Selecciona un perfil', df.name.unique())

# Keep only shows watched by the selected profile and for more than 5 minutes
df = filter_by_profile_and_duration(df, profile_name)

#
# General stats
#

total_watch_time = get_watch_time(df.duration_secs.sum()).split(':')
dates = df.start.sort_values()
account_longevity = AccountLongevity(dates)
watch_hours_per_week = int(total_watch_time[0]) / (account_longevity.time.days / 7)
first_show_info = get_first_show_info(df, dates)

top_movies = get_top_movies(df)

series_df = get_series_df(df)
top_series_by_play_count = get_top_played_series(series_df)
top_watched_by_episodes = get_top_series_by_unique_episodes_played(series_df)
top_watched_series = get_top_series_by_watch_time(series_df)

#
# Summary Image
#

# Top movie
top_movie = top_movies.head(1)
top_movie_title = top_movie.title.values[0]

# Top series
top_series = top_watched_series.head(1)
top_series_title = top_series.head(1).title.values[0]

top_series_by_episodes = top_watched_by_episodes.loc[top_watched_by_episodes.title == top_series_title]

st.image(
    get_infographic(account_longevity, total_watch_time, watch_hours_per_week, top_series_title, top_series,
                    top_series_by_episodes, top_movie, top_movie_title, first_show_info)
)

#
# Word Cloud
#
movies_freq_dict = dict(zip(top_movies.title, top_movies.plays))
series_freq_dict = dict(zip(top_series_by_play_count.title, top_series_by_play_count.plays))
all_content_dict = movies_freq_dict | series_freq_dict
wordcloud = WordCloud(collocations=False, max_words=85, background_color="rgba(255, 255, 255, 0)", mode="RGBA") \
    .generate_from_frequencies(all_content_dict)
fig = plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.subheader('Nube de títulos de contenidos más vistos')
st.text('Muestra los títulos de los contenidos en proporción a la cantidad de veces que se han visto.')
st.text('Es decir, los textos más grandes son los contenidos más vistos y los textos pequeños los menos vistos.')
st.text('Está limitado a 85 títulos.')
st.pyplot(fig)


#
# Common watching times
#
df = add_day_and_hour_columns(df)
df_per_day = create_df_per_day(df)
df_per_hour = create_df_per_hour(df)

# Most watch time heatmap
fig = create_watch_times_heatmap(df)
st.subheader('Gráfica de Actividad por día y hora')
st.text('Cada cuadro representa una hora de un día de la semana')
st.text('Por ejemplo, el primer cuadro es el de las 12:00 am del domingo')
st.text('El número dentro de cada cuadro representa la cantidad de shows que comenzaste a ver ese día y hora')
st.text('Un color claro representa menos actividad y un color oscuro representa más actividad')
st.pyplot(fig)

st.divider()
st.text('Creado por Miguel López (@mkfnx)')
st.markdown('Más de mi contenido y proyectos en [https://beacons.ai/mkfnx](https://beacons.ai/mkfnx)')
