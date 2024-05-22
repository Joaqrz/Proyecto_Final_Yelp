import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import io

def Transformar_data(data, df_estados, df_business):
    df_estados= df_estados.rename(columns={'nombre_largo': 'estado', 'nombre_corto':'state'}) # cambiar nombre de la columna
    df_estados= df_estados.drop(['codigos'], axis=1) 
    df_estados['estado']= df_estados['estado'].convert_dtypes(convert_string=True)
    df_estados['estado']= df_estados['estado'].str.strip()  # quita los espacios vacios

    # Se cargan los business para filtrar los reviews de la categoria restaurantes solamente
    df_business = df_business.loc[:, ~df_business.columns.duplicated()]
    df_business['categories'] = df_business['categories'].str.split(',')
    df_business= df_business.explode('categories')
    df_business= df_business.dropna(subset=['categories']) # Elimina datos nulos de la columna
    df_business['categories']= df_business['categories'].str.strip()    # Elimina los espacios
    df_business= df_business[df_business['categories']== 'Restaurants']
    df_business = df_business.merge(df_estados, on='state', how='left')

    lista_estados= ['Florida', 'Pennsylvania', 'Tennessee', 'California', 'Texas', 'New York']
    df_business= df_business[df_business['estado'].isin(lista_estados)]
    df_business= df_business[['business_id', 'name']]
    
    
    df_data= data
    df_data = df_data.merge(df_business, on='business_id', how='inner')
    df_data = df_data[(df_data['date'].dt.year >= 2010) & (df_data['date'].dt.year <= 2021)]
    
    df_data= df_data.drop(['review_id','name'], axis=1)       #Elimina la columna pics
    df_data['platform']= 2
    df_data= df_data[['business_id','user_id', 'date', 'stars','useful','funny','cool', 'text', 'platform']]

    print(' ........ PROCESO DE TRANSFORMACION COMPLETADO .....')
    return df_data


def Cargar_Data(file_name, bucket_name):
    storage_client = storage.Client()

    # Descargar el archivo CSV desde GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string()
    
    # Crear un DataFrame de Pandas a partir del contenido del archivo json
    df_data = pd.read_json(io.BytesIO(content))
    
    # Crear Dataframe de pandas con los estados
    blob_estados= bucket.blob('estados_usa.csv')
    df_estados= pd.read_csv(io.BytesIO(blob_estados.download_as_string()), delimiter = ';', encoding = "utf-8")

    # Crear Dataframe de pandas con los business
    blob_business= bucket.blob('business.pkl')
    df_business = pd.read_pickle(io.BytesIO(blob_business.download_as_string()))

    print(f'... SE HA CARGADO EL ARCHIVO: {file_name} ...')

    return df_data, df_estados, df_business


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


def Procesar_Data_reviews_Yelp(data, context):
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
        
    # Carga los archivo a procesar en un dataframe 
    df_data, df_estados, df_business = Cargar_Data(file_name, bucket_name)
    # Realiza las transformaciones y limpieza del archivo y lo devuelve junto con 2 df resultantes
    df_procesado = Transformar_data(df_data, df_estados, df_business)
    # Guardas los datos procesados en BigQuery
    Guardar_en_BigQuery(df_procesado, dataset_id, table_id, schema_review)


