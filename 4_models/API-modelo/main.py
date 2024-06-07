# se cargan las librerias necesarias
from fastapi import FastAPI
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import List

app = FastAPI()

# Cargamos el DataFrame desde el archivo pickle
df_modelo = pd.read_pickle('data/Dataset_filtrado.pickle')
 

@app.get("/recomendacion/{estado},{tipo_comida}", response_model=List[List[float]])
def recomendacion (estado: str, tipo_comida: str):
    # Filtrar los datos por estado y tipo de comida
    # En el deploy cambiará por el Estado y la selección de tipo de comida del usuario

    df_filtrado = df_modelo[(df_modelo['state'] == estado) & (df_modelo['category_name'] == tipo_comida)]
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