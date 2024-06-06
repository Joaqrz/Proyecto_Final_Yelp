# se cargan las librerias necesarias
from fastapi import FastAPI
import pandas as pd
import numpy as np
from transformers import pipeline
from sklearn.cluster import KMeans
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from typing import List

app = FastAPI()

# Cargamos el DataFrame desde el archivo pickle
df_modelo = pd.read_pickle('data/ML_Dataset_filtrado.pickle')

# Función para determinar el estado basado en latitud y longitud
def determinar_estado(lat, lon):
    if 32.5 <= lat <= 42 and -124 <= lon <= -114:
        return 'California'
    elif 24.5 <= lat <= 31 and -87.5 <= lon <= -80:
        return 'Florida'
    elif 39 <= lat <= 42 and -80.5 <= lon <= -74.5:
        return 'Pennsylvania'
    elif 35 <= lat <= 36.7 and -90 <= lon <= -81.5:
        return 'Tennessee'
    elif 25.8 <= lat <= 36.5 and -106.5 <= lon <= -93.5:
        return 'Texas'
    elif 40.5 <= lat <= 45 and -79.75 <= lon <= -71.75:
        return 'New York'
    else:
        return 'Unknown'
    
# Calcular densidad de restaurantes
def calcular_densidad(latitudes, longitudes, radio=1.0):
    coords = np.array(list(zip(latitudes, longitudes)))
    nbrs = NearestNeighbors(radius=radio, metric='haversine').fit(np.radians(coords))
    densidad = nbrs.radius_neighbors_graph(np.radians(coords)).sum(axis=1)
    return densidad

# Eliminar la columna 'city'
df_modelo.drop(columns=['city'], inplace=True)
# Asignar el estado correcto basado en latitud y longitud
df_modelo['state'] = df_modelo.apply(lambda row: determinar_estado(row['latitude'], row['longitude']), axis=1)
# Filtrar el dataset para mantener solo los registros con estados conocidos
df_modelo = df_modelo[df_modelo['state'] != 'Unknown']


@app.get("/recomendacion/{estado},{tipo_comida}", response_model=List[List[float]])
def recomendacion (estado: str, tipo_comida: str):
    # Filtrar los datos por estado y tipo de comida
    # En el deploy cambiará por el Estado y la selección de tipo de comida del usuario

    df_filtrado = df_modelo[(df_modelo['state'] == estado) & (df_modelo['category_name'] == tipo_comida)]

    df_filtrado['densidad_restaurantes'] = calcular_densidad(df_filtrado['latitude'], df_filtrado['longitude'])

    # Calcular distancia a restaurantes populares
    df_restaurantes_populares = df_modelo[df_modelo['business_stars'] >= 4][['latitude', 'longitude']]
    coords_populares = np.array(list(zip(df_restaurantes_populares['latitude'], df_restaurantes_populares['longitude'])))
    nbrs_populares = NearestNeighbors(n_neighbors=1, metric='haversine').fit(np.radians(coords_populares))
    distancias, _ = nbrs_populares.kneighbors(np.radians(df_filtrado[['latitude', 'longitude']]))
    df_filtrado['distancia_restaurantes_populares'] = distancias * 6371  # Convertir a kilómetros
    columnas_para_escalar = ['business_stars', 'business_platform', 'review_stars', 'review_platform', 
                            'sentimiento', 'densidad_restaurantes', 'distancia_restaurantes_populares']   

    # Escalado de características numéricas (sin incluir latitude y longitude)
    scaler = StandardScaler()
    df_filtrado[columnas_para_escalar] = scaler.fit_transform(df_filtrado[columnas_para_escalar])
    # Aplicar KMeans clustering para encontrar clusters de ubicaciones positivas, sin escalar latitud y longitud
    locations = df_filtrado[['latitude', 'longitude']]
    otras_caracteristicas = df_filtrado[columnas_para_escalar]

    # Concatenar las características sin escalar latitud y longitud
    features = pd.concat([locations.reset_index(drop=True), otras_caracteristicas.reset_index(drop=True)], axis=1)

    # Parámetro para personalizar el número de centroides
    num_centroides = 5  # Este valor se puede cambiar según las necesidades

    kmeans = KMeans(n_clusters=num_centroides, random_state=42)
    kmeans.fit(features)

    # Obtener los centroides de los clusters como las ubicaciones recomendadas
    centroides = kmeans.cluster_centers_
    datos= centroides.tolist()
    return datos