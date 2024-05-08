# Diccionario de Datos

Este documento describe la estructura de datos utilizados en el proyecto, con detalles sobre las columnas y su significado.

## Google Maps

### Metadatos de Sitios (`metadata_sitios`)

Contiene información sobre los negocios y sus características.

- **`name`**: Nombre del negocio.
- **`address`**: Dirección completa del negocio.
- **`gmap_id`**: ID único en Google Maps.
- **`description`**: Descripción del negocio.
- **`latitude`**: Latitud de la ubicación.
- **`longitude`**: Longitud de la ubicación.
- **`category`**: Lista de categorías del negocio.
- **`avg_rating`**: Calificación promedio del negocio.
- **`num_of_reviews`**: Número de reseñas recibidas.
- **`price`**: Indicador de precios.
- **`hours`**: Horarios del negocio.
- **`MISC`**: Información adicional, como opciones de servicio, medidas de seguridad, accesibilidad, entre otros.
- **`state`**: Estado actual del negocio (por ejemplo, "Cierra pronto a las 1:30 PM").
- **`relative_results`**: IDs relacionados en Google Maps.
- **`url`**: URL del negocio en Google Maps.

### Reseñas por Estado (`review-estados`)

Contiene las reseñas de usuarios, organizadas por estado en EE. UU.

- **`user_id`**: ID del usuario que hizo la reseña.
- **`name`**: Nombre del usuario.
- **`time`**: Fecha y hora del review en formato UNIX.
- **`rating`**: Calificación del review (1 a 5 estrellas).
- **`text`**: Texto del review.
- **`pics`**: Lista de imágenes asociadas al review.
- **`resp`**: Respuesta del negocio al review.
- **`gmap_id`**: ID del negocio en Google Maps.

## Yelp

### Información del Negocio (`business.pkl`)

Información detallada de negocios, incluyendo localización y atributos.

- **`business_id`**: ID único del negocio.
- **`name`**: Nombre del negocio.
- **`address`**: Dirección del negocio.
- **`city`**: Ciudad donde está el negocio.
- **`state`**: Código de dos letras del estado.
- **`postal_code`**: Código postal.
- **`latitude`**: Latitud.
- **`longitude`**: Longitud.
- **`stars`**: Calificación en estrellas.
- **`review_count`**: Número de reseñas recibidas.
- **`is_open`**: Estado del negocio (1 para abierto, 0 para cerrado).
- **`attributes`**: Atributos del negocio.
- **`categories`**: Lista de categorías.
- **`hours`**: Horarios de operación del negocio.

### Reseñas (`review.json`)

Contiene las reseñas de Yelp.

- **`review_id`**: ID único de la reseña.
- **`user_id`**: ID del usuario que hizo la reseña.
- **`business_id`**: ID del negocio.
- **`stars`**: Calificación del review (1 a 5 estrellas).
- **`date`**: Fecha de la reseña.
- **`text`**: Texto del review.
- **`useful`**: Votos como útil.
- **`funny`**: Votos como gracioso.
- **`cool`**: Votos como cool.

### Información del Usuario (`user.parquet`)

Datos de usuarios, incluyendo relaciones y metadata asociada.

- **`user_id`**: ID único del usuario.
- **`name`**: Nombre del usuario.
- **`review_count`**: Número de reseñas escritas.
- **`yelping_since`**: Fecha de creación del usuario en Yelp.
- **`friends`**: Lista de IDs de amigos.
- **`useful`, `funny`, `cool`**: Número de votos para estos atributos.
- **`fans`**: Número de fans.
- **`elite`**: Años en que fue miembro élite.
- **`compliments`**: Varios tipos de cumplidos recibidos.

### Registros de Visitas (`checkin.json`)

Contiene registros de visitas a negocios.

- **`business_id`**: ID único del negocio.
- **`date`**: Fechas separadas por comas en formato YYYY-MM-DD HH:MM:SS.

### Tips (`tip.json`)

Consejos rápidos escritos por usuarios.

- **`text`**: Texto del tip.
- **`date`**: Fecha del tip en formato YYYY-MM-DD.
- **`compliment_count`**: Número total de cumplidos del tip.
- **`business_id`**: ID del negocio asociado.
- **`user_id`**: ID del usuario que escribió el tip.
