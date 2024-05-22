import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import io

def Transformar_data(data, df_estados):
    df_estados= df_estados.rename(columns={'nombre_largo': 'estado', 'nombre_corto':'state'}) # cambiar nombre de la columna
    df_estados= df_estados.drop(['codigos'], axis=1) # Elimina la columna
    df_estados['estado']= df_estados['estado'].convert_dtypes(convert_string=True)
    df_estados['estado']= df_estados['estado'].str.strip()  # quita los espacios vacios

    df_data= data
    df_data['time'] = pd.to_datetime(df_data['time'],unit='ms')     #Transforma la columna de tipo timestamp a formato datetime
    df_data = df_data[(df_data['time'].dt.year >= 2010) & (df_data['time'].dt.year <= 2021)]
    
    # Se guardan las columnas resp y el gmap_id en un df
    df_respuestas= df_data[['gmap_id','resp']]
    df_respuestas= df_respuestas.dropna(subset=['resp']) # Elimina filas con resp nulo
    df_respuestas= df_respuestas.rename(columns={'gmap_id': 'business_id'})

    # Funcion para cargar los json a una serie de pandas
    def expandir_diccionario(diccionario):
        return pd.Series(diccionario)

    # Se concatenas las series al df original
    df_expandido = pd.concat([df_respuestas, df_respuestas['resp'].apply(expandir_diccionario)], axis=1)
    df_expandido.drop('resp', axis=1, inplace=True)     # Se elimina la columna de MISC
    df_expandido['time'] = pd.to_datetime(df_expandido['time'],unit='ms')     #Transforma la columna de tipo timestamp a formato datetime
    df_respuestas= df_expandido

    df_data= df_data.drop(['pics','resp','name'], axis=1)       #Elimina la columna pics
    df_data= df_data.rename(columns={'time': 'date', 'gmap_id':'business_id', 'rating':'stars'})
    df_data[['useful','funny','cool']] = 0
    df_data['platform']= 1

    df_data['user_id']= df_data['user_id'].astype(str)
    df_data= df_data[['business_id','user_id', 'date', 'stars','useful','funny','cool', 'text', 'platform']]


    print(' ........ PROCESO DE TRANSFORMACION COMPLETADO .....')
    return df_data, df_respuestas


def Cargar_Data(file_name, bucket_name):
    storage_client = storage.Client()

    # Descargar el archivo CSV desde GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string()
    
    # Crear un DataFrame de Pandas a partir del contenido del archivo json
    df_data = pd.read_json(io.BytesIO(content),lines=True)
    
    # Crear Dataframe de pandas con los estados
    blob_estados= bucket.blob('estados_usa.csv')
    df_estados= pd.read_csv(io.BytesIO(blob_estados.download_as_string()), delimiter = ';', encoding = "utf-8")
    

    print(f'... SE HA CARGADO EL ARCHIVO: {file_name} ...')

    return df_data, df_estados


def Guardar_en_BigQuery(data, dataset_id, table_id, schema):
    bigquery_client = bigquery.Client()
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    try:
        tabla = bigquery_client.get_table(table_ref)
        tabla_existe = True
    except:
        tabla_existe = False

    if tabla_existe:
        print(f'----- La tabla {table_id} ya existe en el dataset {dataset_id} -----')
    else:
        print(f'----- La tabla {table_id} no existe en el dataset {dataset_id} -----')
        # Crear la tabla si no existe
        tabla = bigquery.Table(table_ref, schema=schema)
        tabla = bigquery_client.create_table(tabla)
        print(f'----- Se ha creado la tabla {table_id} en el dataset {dataset_id} -----')
        
    # Agregar los registros de data a la tabla existente o recién creada
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND if tabla_existe else bigquery.WriteDisposition.WRITE_TRUNCATE
    job = bigquery_client.load_table_from_dataframe(data, table_ref, job_config=job_config)
    job.result()
    print(f'----- REGISTROS DE AGREGADOS CORRECTAMENTE EN: {table_id} -------')
    return


def Procesar_Data_reviews_Gmaps(data, context):
    file_name= data['name']
    bucket_name= data['bucket']
    dataset_id= 'BD_Henry'
    table_id = 'reviews'
    schema_review = [
        bigquery.SchemaField("business_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("user_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.DATETIME),
        bigquery.SchemaField("stars", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("useful", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("funny", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("cool", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("text", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("platform", bigquery.enums.SqlTypeNames.INTEGER)
    ]
    schema_resp = [
        bigquery.SchemaField("business_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("resp", bigquery.enums.SqlTypeNames.STRING)        
    ]
        
    # Carga los archivo a procesar en un dataframe 
    df_data, df_estados = Cargar_Data(file_name, bucket_name)
    # Realiza las transformaciones y limpieza del archivo y lo devuelve junto con 2 df resultantes
    df_procesado, df_respuestas= Transformar_data(df_data, df_estados)
    # Guardas los datos procesados en BigQuery
    Guardar_en_BigQuery(df_procesado, dataset_id, table_id, schema_review)
    Guardar_en_BigQuery(df_respuestas, dataset_id, 'resp_reviews', schema_resp)

