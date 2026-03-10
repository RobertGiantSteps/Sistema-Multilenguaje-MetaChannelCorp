FROM wordpress:6.7-php8.2-fpm

LABEL maintainer="Roberto Martínez P"
LABEL description="META Channel Corporation — WordPress Multidioma (ES/EN) con TranslatePress"
LABEL version="1.0"

# Instalar cliente MySQL para el script de inicialización
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar wp-content al directorio de staging de WordPress
# (el entrypoint oficial copia de /usr/src/wordpress/ a /var/www/html/ en el primer arranque)
COPY wp-content/ /usr/src/wordpress/wp-content/

# Copiar el SQL a una ruta fuera del volumen para que siempre esté disponible
RUN mkdir -p /docker
COPY wp-content/mcc-init.sql /docker/mcc-init.sql

# Copiar nuestro entrypoint personalizado
COPY docker-entrypoint-mcc.sh /docker-entrypoint-mcc.sh
RUN chmod +x /docker-entrypoint-mcc.sh

# Sobreescribir el entrypoint: nuestro script espera la BD, importa el SQL
# y luego llama al entrypoint oficial de WordPress
ENTRYPOINT ["/docker-entrypoint-mcc.sh"]
CMD ["php-fpm"]
