import streamlit as st

st.set_page_config(
        page_title='Infografía Netflix - Ejemplo - @mkfnx',
)

st.title('Ejemplo de Infografía Netflix')
st.text('Este es un ejemplo de las imágenes que genera esta app.')
st.text('Cuando proporciones tu archivo las imágenes se generaran con tu información.')

st.subheader('Infografía')
st.image('img/ejemplo-infografia.png')

st.subheader('Nube de títulos de contenidos más vistos')
st.text('Muestra los títulos de los contenidos en proporción a la cantidad de veces que se han visto.')
st.text('Es decir, los textos más grandes son los contenidos más vistos y los textos pequeños los menos vistos.')
st.text('Está limitado a 85 títulos.')
st.image('img/ejemplo-wordcloud.png')

st.subheader('Gráfica de Actividad por día y hora')
st.text('Cada cuadro representa una hora de un día de la semana')
st.text('Por ejemplo, el primer cuadro es el de las 12:00 am del domingo')
st.text('El número dentro de cada cuadro representa la cantidad de shows que comenzaste a ver ese día y hora')
st.text('Un color claro representa menos actividad y un color oscuro representa más actividad')
st.image('img/ejemplo-heatmap.png')
