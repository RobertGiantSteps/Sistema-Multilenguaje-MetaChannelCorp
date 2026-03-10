FROM nginx:alpine

LABEL maintainer="Roberto Martínez P"
LABEL description="META Channel Corporation — Nginx con SSL para metachannelcorp.com/.ie"

# Instalar openssl para generar certificados si no existen
RUN apk add --no-cache openssl bash

# Copiar configuración de Nginx
COPY default.conf /etc/nginx/conf.d/default.conf

# Copiar script que genera los certificados SSL al iniciar
COPY generate-ssl-and-start.sh /generate-ssl-and-start.sh
RUN chmod +x /generate-ssl-and-start.sh

EXPOSE 80 443

CMD ["/generate-ssl-and-start.sh"]
