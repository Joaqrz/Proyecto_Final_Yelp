import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import io

def Transformar_data(data, df_estados):
    df_data= data
    df_data= df_data.dropna(subset=['address']) # Elimina filas con address nulas
    df_data= df_data.dropna(subset=['category']) # Elimina filas con category nulas
    df_data= df_data.explode('category')
    df_data= df_data[df_data['category'] == "Restaurant"]
    df_data= df_data.fillna({'price':'SIN DATO', 'state':'SIN DATO'})     # Se imputan los valores nulos a 'SIN DATO'

    # Se guardan las columnas MISC y el gmap_id en un df
    df_misc= df_data[['gmap_id','MISC']]
    df_misc= df_misc.dropna(subset=['MISC']) # Elimina filas con MISC nulo

    # Funcion para cargar los json a una serie de pandas
    def expandir_diccionario(diccionario):
        return pd.Series(diccionario)

    # Se concatenas las series al df original
    df_expandido = pd.concat([df_misc, df_misc['MISC'].apply(expandir_diccionario)], axis=1)
    df_expandido.drop('MISC', axis=1, inplace=True)     # Se elimina la columna de MISC
    df_misc= df_expandido

    df_Service_options= df_misc[['gmap_id','Service options']]      # Se crea un df solo las columnas gmap_id y Service Options
    df_Service_options= df_Service_options.rename(columns={'gmap_id': 'business_id','Service options': 'service_option'}) # cambiar nombre de las columnas
    df_Service_options= df_Service_options.dropna(subset=['service_option']) # Elimina filas con columna 'Service Opciones nulas'
    df_Service_options= df_Service_options.explode('service_option')

    df_Planning= df_misc[['gmap_id','Planning']]      # Se crea un df solo las columnas gmap_id y Planning
    df_Planning= df_Planning.rename(columns={'gmap_id': 'business_id', 'Planning': 'planning_option'}) # cambiar nombre de la columna
    df_Planning= df_Planning.dropna(subset=['planning_option']) # Elimina filas con columna 'Service Opciones nulas'
    df_Planning= df_Planning.explode('planning_option')

    # En pruebas se detecto que esta fila estaba dando problemas con la funcion para extraer, asi que se procede a eliminarla
    df_data= df_data[df_data['address'] != "〒10028 New York, Lexington Ave, (New) Ichie Japanese Restaurant"]

    # Funcion para sacar la ciudad y el estado de la direccion
    def Ext_Ciudad_Estado(dir):
        ciudad= "SIN DATO"
        estado= "SIN DATO"     
        if len(str(dir)) > 10:  
            lista= str(dir).split(',')
            if len(lista) > 2:
                codigo= lista[-1][1:3]
                df_filtro= df_estados[df_estados['nombre_corto'].str.contains(codigo)]        
                if not df_filtro.empty:            
                    ciudad = lista[-2].strip()
                    estado= df_filtro.nombre_largo.values[0].strip()
        return ciudad, estado
    
    # Extraer ciudad y estado de la columna direccion y guardarda en 2 columnas
    df_data[['city','state']] = df_data.apply(lambda x: Ext_Ciudad_Estado(x['address']), axis=1, result_type='expand')
    lista_estados= ['Florida', 'Pennsylvania', 'Tennessee', 'California', 'Texas', 'New York']
    df_data= df_data[df_data['state'].isin(lista_estados)]      #Selecionar solo los estados definidos en la lista

    #Borrar Columnas
    df_data= df_data.drop(['relative_results','address', 'num_of_reviews', 'description', 'url','category', 'MISC', 'hours'], axis=1) 
    # Ordena el orden de las columnas
    df_data= df_data[['gmap_id','name', 'city', 'state', 'latitude', 'longitude', 'avg_rating', 'price']]
    df_data= df_data.rename(columns={'gmap_id': 'business_id', 'avg_rating': 'stars'}) # cambiar nombre de la columnas
    df_data['platform']= 1

    print(' ........ PROCESO DE TRANSFORMACION COMPLETADO .....')
    return df_data, df_Service_options, df_Planning


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
    print(f'----- REGISTROS AGREGADOS CORRECTAMENTE EN: {table_id} -------')
    return


def Procesar_Data_Sitios_Gmaps(data, context):
    file_name= data['name']
    bucket_name= data['bucket']
    dataset_id= 'BD_Henry'
    table_id = 'business'
    schema_sitios = [
        bigquery.SchemaField("business_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("city", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("state", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("latitude", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("longitude", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("stars", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("price", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("platform", bigquery.enums.SqlTypeNames.STRING),
    ]

    schema_service = [
        bigquery.SchemaField("business_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("service_option", bigquery.enums.SqlTypeNames.STRING),        
    ]
    
    schema_planning = [
        bigquery.SchemaField("business_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("planning_option", bigquery.enums.SqlTypeNames.STRING),        
    ]
        
    # Carga los archivo a procesar en un dataframe 
    df_data, df_estados = Cargar_Data(file_name, bucket_name)
    # Realiza las transformaciones y limpieza del archivo y lo devuelve junto con 2 df resultantes
    df_procesado, df_Service_options, df_Planning= Transformar_data(df_data, df_estados)
    
    # Guardas los datos procesados en BigQuery
    Guardar_en_BigQuery(df_procesado, dataset_id, table_id, schema_sitios)
    Guardar_en_BigQuery(df_Service_options, dataset_id, 'service_business', schema_service)
    Guardar_en_BigQuery(df_Planning, dataset_id, 'planning_busines', schema_planning)

