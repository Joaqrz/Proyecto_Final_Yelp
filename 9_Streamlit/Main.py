import streamlit as st
import folium 
from streamlit_folium import st_folium
from streamlit_folium import folium_static


# Column layout for the header and image
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image('9_Streamlit/src/dataminds.png')  # Adjust the path as needed
with col2:
    st.header("Sistema de Recomendación Geográfico")

# Columns layout for the checkboxes and map
col3, col4 = st.columns([0.5, 0.5])  # Adjusting the column ratio to make the map smaller
with col3:
    st.write('Seleccione el tipo de comida y el estado para recibir ubicaciones sugeridas para nuevos restaurantes')
    col5, col6 = st.columns(2)
    with col5:
        st.header('Tipo de comida')
        Americana = st.checkbox('Americana')
        Asiatica = st.checkbox('Asiatica')
        Francesa = st.checkbox('Francesa')
        India = st.checkbox('India')
        Italiana = st.checkbox('Italiana')
        Mariscos = st.checkbox('Mariscos')
        Mediterranea = st.checkbox('Mediterranea')
        Mexicana = st.checkbox('Mexicana')
    with col6:
        st.header('Estado')
        Florida = st.checkbox('Florida')
        Pennsylvania = st.checkbox('Pennsylvania')
        Tennessee = st.checkbox('Tennessee')
        California = st.checkbox('California')
        Texas = st.checkbox('Texas')
        NewYork = st.checkbox('New York')

with col4:
    mapa = folium.Map(location=[36.7783, -119.4179], zoom_start=7) 
    folium_static(mapa)