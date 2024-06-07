import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import numpy as np
import os

# Obtenemos la ruta absoluta del directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construimos la ruta al archivo de imagen
image_path = os.path.join(script_dir, 'src', 'dataminds.png')

# Distribución de columnas para el encabezado y la imagen
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image_path)  # Ajusta la ruta según sea necesario
with col2:
    st.header("Sistema de Recomendación Geográfico")

# Distribución de columnas para los botones de selección y el mapa
col3, col4 = st.columns([0.5, 0.5])  # Ajusta la proporción de las columnas para hacer el mapa más pequeño
with col3:
    st.write('Seleccione el tipo de comida y el estado para recibir ubicaciones sugeridas para nuevos restaurantes')
    col5, col6 = st.columns(2)
    with col5:
        tipo_de_comida = st.radio(
            "Seleccione un tipo de comida:",
            options=["Americana", "Asiática", "Francés", "Hindú", "Italiana", "Mariscos", "Mediterránea", "Mexicana"],
        )
    with col6:
        estado = st.radio(
            "Seleccione un estado:",
            options=["Florida", "Pennsylvania", "Tennessee", 'California', 'Texas', 'New York'],
        )

    if st.button("Enviar"):
        def obtener_datos(estado: str, tipo_de_comida: str):
            url = f"https://api-modelo-nyo7ju5e4q-rj.a.run.app/recomendacion/{estado},{tipo_de_comida}"  # Asegúrate de que esta URL sea la correcta para tu API
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                # Convertir los datos a un arreglo de NumPy
                arreglo = np.array(datos)
                return arreglo
            else:
                response.raise_for_status()

        try:
            centroides = obtener_datos(estado, tipo_de_comida)

            # Diccionario para centrar el mapa en los estados seleccionados
            centro_estados = {
                'California': [36.7783, -119.4179],
                'Florida': [27.9944024, -81.7602544],
                'Pennsylvania': [41.2033, -77.1945],
                'Tennessee': [35.5175, -86.5804],
                'Texas': [31.9686, -99.9018],
                'New York': [40.7128, -74.0060]
            }
            # Crear un mapa centrado en el estado seleccionado
            centro_estado = centro_estados[estado]
            mapa = folium.Map(location=centro_estado, zoom_start=7)

            # Agregar solo los centroides (ubicaciones recomendadas) al mapa con latitud y longitud en el popup
            for centroide in centroides:
                folium.Marker(
                    location=[centroide[0], centroide[1]],
                    popup=f'Ubicación Recomendada<br>Latitud: {centroide[0]}<br>Longitud: {centroide[1]}',
                    icon=folium.Icon(color='red', icon='star')
                ).add_to(mapa)
            
            with col4:
                folium_static(mapa)

        except Exception as e:
            st.error(f"Error al obtener datos: {e}")