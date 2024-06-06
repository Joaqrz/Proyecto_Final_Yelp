import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import io

def Transformar_data(data, opcion):
    df_data= data
    if opcion ==1: 
        df_data = df_data[(df_data['date'].dt.year >= 2010) & (df_data['date'].dt.year <= 2021)]
        df_data= df_data.drop(['compliment_count'], axis=1)       #Elimina la columnas
        df_data= df_data[['business_id','user_id', 'date','text']]
    else:
        df_data= df_data.drop(['elite', 'friends', 'compliment_hot', 'compliment_more', 'compliment_profile', 
                                'compliment_cute', 'compliment_list', 'compliment_note', 'compliment_plain', 
                                'compliment_cool', 'compliment_funny', 'compliment_writer','compliment_photos'], axis=1)
        df_data['yelping_since'] = pd.to_datetime(df_data['yelping_since'])        
    
    print(' ........ PROCESO DE TRANSFORMACION COMPLETADO .....')
    return df_data


def Cargar_Data(file_name, bucket_name, opcion):
    storage_client = storage.Client()

    # Descargar el archivo CSV desde GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string()
    
    # Crear un DataFrame de Pandas a partir del contenido del archivo json
    if opcion == 1:        
        df_data = pd.read_json(io.BytesIO(content),lines=True)
    else:
        df_data = pd.read_parquet(io.BytesIO(content))
    

    print(f'... SE HA CARGADO EL ARCHIVO: {file_name} ...')
    return df_data


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


def Procesar_Data_users_tips_Yelp(data, context):
    file_name= data['name']
    bucket_name= data['bucket']
    dataset_id= 'BD_Henry'
    opcion= 0
    if file_name == 'tip.json':
        opcion= 1
        table_id = 'tips_yelp'
        schema = [
            bigquery.SchemaField("business_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("user_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.DATETIME),
            bigquery.SchemaField("text", bigquery.enums.SqlTypeNames.STRING)            
        ]
    else:
        opcion= 2
        table_id = 'users_yelp'
        schema = [
            bigquery.SchemaField("user_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("review_count", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField("yelping_since", bigquery.enums.SqlTypeNames.DATETIME),
            bigquery.SchemaField("useful", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField("funny", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField("cool", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField("fans", bigquery.enums.SqlTypeNames.INT64),
            bigquery.SchemaField("average_stars", bigquery.enums.SqlTypeNames.FLOAT)
        ] 

    # Carga los archivo a procesar en un dataframe 
    df_data = Cargar_Data(file_name, bucket_name, opcion)
    # Realiza las transformaciones y limpieza del archivo y lo devuelve junto con 2 df resultantes
    df_procesado = Transformar_data(df_data,opcion)
    # Guardas los datos procesados en BigQuery
    Guardar_en_BigQuery(df_procesado, dataset_id, table_id, schema)



