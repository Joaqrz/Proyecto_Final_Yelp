# Sistema Avanzado de Recomendación de Restaurantes - Yelp y Google Maps

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter_Notebook-F37626?style=flat&logo=jupyter)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat&logo=seaborn)
![PowerBI](https://img.shields.io/badge/PowerBI-F2C811?style=flat&logo=powerbi)


![Banner](6_docs/other_docs/Test1.jpg)


## Índice

1. [Introducción](#introducción)
2. [Objetivos del Proyecto](#objetivos-del-proyecto)
    - [Objetivo General](#objetivo-general)
    - [Objetivos Específicos](#objetivos-específicos)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Indicadores Clave de Rendimiento (KPIs)](#indicadores-clave-de-rendimiento-kpis)
    - [KPI 1: Monitorear el comportamiento de nuevos usuarios](#kpi-1-monitorear-el-comportamiento-de-nuevos-usuarios)
    - [KPI 2: Analizar el nivel de engagement de los usuarios](#kpi-2-analizar-el-nivel-de-engagement-de-los-usuarios)
    - [KPI 3: Evaluar el nivel de satisfacción de los clientes](#kpi-3-evaluar-el-nivel-de-satisfacción-de-los-clientes)
5. [Dashboard - Power BI](#dashboard---power-bi)
6. [Diccionario de Datos](#diccionario-de-datos)
    - [business](#business)
    - [Reseñas](#reseñas)
    - [users_yelp](#users_yelp)
7. [Modelo de Machine Learning](#modelo-de-machine-learning)
8. [Proceso de Construcción del Modelo](#proceso-de-construcción-del-modelo)
9. [Diccionario de Datos para el Modelo](#diccionario-de-datos-para-el-modelo)

## Introducción

Este proyecto representa un esfuerzo significativo en el análisis y la optimización del servicio de recomendación de restaurantes, fusionando datos de Yelp y Google Maps mediante Power BI para comprender el comportamiento de los usuarios, evaluar el rendimiento de los restaurantes y diseñar un modelo de recomendación eficiente.

## Objetivos del Proyecto

### Objetivo General

Desarrollar un sistema de análisis avanzado para mejorar la experiencia culinaria en Yelp y Google Maps en seis estados de EE. UU. El sistema ofrecerá recomendaciones personalizadas y análisis detallados a restaurantes, mejorando la satisfacción de los clientes y la precisión en decisiones de expansión.

### Objetivos Específicos

1. Analizar mercados potenciales para la expansión.
2. Desarrollar un análisis de sentimiento para mejorar el servicio.
3. Crear un sistema de recomendaciones personalizadas.
4. Asegurar la calidad de los datos.
5. Explorar y analizar datos de reseñas.
6. Implementar un modelo predictivo.
7. Desarrollar un dashboard interactivo.

## Arquitectura del Sistema

![Diagrama Arquitectura](imagen_diagrama_arquitectura.png)

### Herramientas y Tecnologías

Para desarrollar el proyecto, se utilizarán las siguientes herramientas y tecnologías:

- **Github**: Alojamiento del repositorio.
- **Trello**: Organización de tareas.
- **Visual Studio Code**: Desarrollo local.
- **Google Colab**: Colaboración en la nube.
- **Google Cloud Platform**: Servicios en la nube.
- **Google Cloud Storage**: Almacenamiento en la nube.
- **Google BigQuery**: Análisis de datos.
- **Google Cloud Run API**: Acceso a servicios en la nube.
- **Power BI**: Visualización de datos.
- **Python**: Programación.
- **Pandas, Matplotlib, Seaborn, Plotly**: Análisis y visualización de datos.
- **Postman**: Pruebas de API.
- **Scikit-learn**: Aprendizaje automático.
- **FastAPI**: Creación de APIs.
- **Streamlit**: Aplicaciones web interactivas.
- **VADER**: Análisis de sentimiento.
- **Folium**: Visualización geoespacial.

## Indicadores Clave de Rendimiento (KPIs)

### KPI 1: Monitorear el comportamiento de nuevos usuarios

- **Descripción:** Este monitoreo ayuda a medir el crecimiento del negocio y el engagement de los usuarios.
- **Meta:** Aumentar el registro de nuevos usuarios en más de 5% vs el trimestre anterior.
- **Cálculo:** 
  ``` 
  aumento de usuarios = (usuarios trimestre Actual - Usuarios trimestre anterior) / usuarios trimestre anterior
  ```

### KPI 2: Analizar el nivel de engagement de los usuarios

- **Descripción:** Comprender el engagement de los usuarios indica la popularidad de los restaurantes y la lealtad de los clientes.
- **Meta:** Aumentar en al menos 10% el número de reseñas del restaurante vs el trimestre anterior.
- **Cálculo:** 
  ``` 
  aumento de reseñas = (reseñas trimestre Actual - reseñas trimestre anterior) / reseñas trimestre anterior
  ```

### KPI 3: Evaluar el nivel de satisfacción de los clientes

- **Descripción:** La satisfacción del cliente refleja la calidad del servicio y la experiencia de los consumidores.
- **Meta:** Aumentar la calificación en estrellas del negocio en al menos 5% vs el trimestre anterior.
- **Cálculo:** 
  ``` 
  aumento de prom rating = (rating prom trimestre actual - rating prom trimestre anterior) / rating prom trimestre anterior
  ```

## Dashboard - Power BI

![Dashboard-Panel General](imagen_dashboard_panel_general.png)

En el panel principal de Power BI se ofrece una visión general con información relevante como la cantidad de reseñas, clientes, restaurantes y estados representados. Incluye filtros por año y diversos gráficos para un análisis temporal y geográfico detallado.

## Diccionario de Datos

### business

Esta tabla contiene información relacionada con los restaurantes de Google Maps y Yelp.

- `business_id`: Identificación única del negocio.
- `name`: Nombre del negocio.
- `city`: Ciudad donde está ubicado el negocio.
- `state`: Estado o región donde está ubicado el negocio.
- `latitude`: Coordenada de latitud de la ubicación del negocio.
- `longitude`: Coordenada de longitud de la ubicación del negocio.
- `stars`: Calificación o puntuación del negocio.
- `price`: Rango de precios del negocio.
- `platform`: Plataforma de origen del dato (1: Google, 2: Yelp).

### Reseñas

Tabla que contiene información sobre las reviews de los usuarios.

- `business_id`: Identificación única del negocio.
- `user_id`: Identificación única del usuario que realiza la reseña.
- `date`: Fecha de la reseña.
- `stars`: Calificación dada en la reseña.
- `useful`: Número de votos útiles.
- `funny`: Número de votos graciosos.
- `cool`: Número de votos cool.
- `text`: Texto de la reseña.
- `platform`: Plataforma de origen del dato (1: Google, 2: Yelp).

### users_yelp

Tabla con información sobre los usuarios de Yelp.

- `user_id`: Identificación única del usuario.
- `name`: Nombre del usuario.
- `review_count`: Número de reseñas realizadas.
- `yelping_since`: Fecha de inicio en Yelp.
- `useful`: Número de votos útiles.
- `funny`: Número de votos graciosos.
- `cool`: Número de votos cool.
- `fans`: Número de fans.
- `average_stars`: Calificación promedio de las reseñas del usuario.
- `Año`: Año desde que están activos los usuarios (columna calculada).

## Modelo de Machine Learning

![Proceso de Construcción del Modelo](imagen_proceso_construccion_modelo.png)

Se llevó a cabo un proceso exhaustivo de preparación y transformación de datos utilizando BigQuery, donde se unieron todas las tablas relevantes mediante una cuenta de servicio que contaba con una clave de servicio.

### Proceso de Construcción del Modelo

1. **Obtención de Datos:** Unificación de las tablas más relevantes.
2. **Limpieza y Transformación de Datos:** Validación de categorías, eliminación de atributos no compartidos, manejo de valores nulos, y ajustes de coordenadas.
3. **Verificación de Datos:** Verificación de datos en las columnas de tipo de comida y estado.
4. **Feature Engineering:** Cálculo de la densidad de restaurantes por estado y distancia a restaurantes populares.
5. **Preparación del Modelo:** Escalado de variables numéricas, implementación del modelo K-means.
6. **Clusterización:** Creación de clusters según su tipo de comida y estado.
7. **Visualización:** Mapa interactivo mostrando los centroides del modelo usando la librería Folium.

## Diccionario de Datos para el Modelo

Esta tabla unificada extraída de BigQuery combina información de Yelp y Google Maps.

- `business_id`: Identificación única del negocio.
- `business_name`: Nombre del negocio.
- `city`: Ciudad donde está ubicado el negocio.
- `state`: Estado o región donde está ubicado el negocio.
- `latitude`: Coordenada de latitud de la ubicación del negocio.
- `longitude`: Coordenada de longitud de la ubicación del negocio.
- `business_stars`: Calificación o puntuación del negocio.
- `price`: Rango de precios del negocio.
- `business_platform`: Plataforma de origen del negocio.
- `review_user_id`: Identificación única del usuario que realiza la reseña.
- `review_date`: Fecha y hora de la reseña.
- `review_stars`: Calificación dada en la reseña.
- `review_text`: Texto de la reseña.
- `review_platform`: Plataforma desde la cual se realizó la reseña.
- `category_name`: Nombre de la categoría del negocio.
- `RestaurantsDelivery`: Indica si el negocio ofrece servicio de entrega a domicilio.
- `OutdoorSeating`: Indica si el negocio cuenta con asientos al aire libre.
- `BusinessAcceptsCreditCards`: Indica si el negocio acepta tarjetas de crédito.
- `GoodForKids`: Indica si el negocio es apropiado para niños.
- `RestaurantsPriceRange2`: Rango de precios de los restaurantes.
- `RestaurantsTakeOut`: Indica si el negocio ofrece servicio para llevar.
- `RestaurantsReservations`: Indica si el negocio acepta reservaciones.
- `HasTV`: Indica si el negocio tiene televisión disponible.

## Equipo de Trabajo

| **Rol** | **Nombre** | **GitHub** | **LinkedIn** |
|:---:|:---:|---|---|
| Data Analyst | Joaquin Rodríguez | [Joaqrz](https://github.com/Joaqrz) | [LinkedIn](enlace_a_linkedin) |
| Data Engineer | Nelvin Velazco | [nelvinvelazco](https://github.com/nelvinvelazco) | [LinkedIn](enlace_a_linkedin) |
| Data Engineer | Cristian Barreto | [CristianBarreto08](https://github.com/CristianBarreto08) | [cristian-barreto13](https://www.linkedin.com/in/cristian-barreto13/) |
| Data Scientist | Manuel Trujillo | [mdtrujillo73](https://github.com/mdtrujillo73) | [mdtrujillo73](https://www.linkedin.com/in/mdtrujillo73/) |
| Data Scientist | Diego Vélez | [GitHub](enlace_a_github) | [LinkedIn](enlace_a_linkedin) |

## Estructura del Repositorio

- **`data/`**: Contiene datos necesarios para el proyecto.
- **`notebooks/`**: Cuadernos Jupyter para análisis y desarrollo de modelos.
- **`scripts/`**: Scripts para procesos de ETL y otras tareas.
- **`models/`**: Modelos entrenados y recursos relacionados.
- **`dashboards/`**: Código y recursos para el dashboard interactivo.
- **`docs/`**: Documentación, incluido el diccionario de datos y otros informes.
- **`tests/`**: Scripts para pruebas automáticas.
- **`results/`**: Resultados intermedios y finales.

## Instalación y Configuración

Para ejecutar el proyecto, se recomienda utilizar un entorno virtual como `venv` o `Conda`. Los requisitos para el entorno de desarrollo se encuentran en el archivo `requirements.txt`. Para configurarlo, sigue estos pasos:

1. Clona el repositorio en tu máquina local.
2. Crea un entorno virtual.
3. Instala las dependencias del proyecto usando `pip install -r requirements.txt`.

## Contribuciones y Licencia

- **Contribuciones**: Si deseas contribuir al proyecto, abre un "issue" o un "pull request" con tus sugerencias o mejoras.
- **Licencia**: Este proyecto está bajo la licencia [nombre de la licencia], que se puede encontrar en el archivo `LICENSE`.

## Enlaces Importantes

- [Diccionario de Datos](enlace_al_diccionario_de_datos)
- [Documentación Técnica](enlace_a_documentacion)
- [Dashboard Interactivo](enlace_a_dashboard)

## Contacto

Para preguntas o sugerencias, puedes contactarnos a través de [Correo Electrónico](mailto:cfbn13@hotmail.com) o en [LinkedIn](enlace_a_linkedin).
