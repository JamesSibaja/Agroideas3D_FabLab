#!/bin/sh

if [ "$IS_PRODUCTION" = "y" ]; then
  cp /etc/nginx/conf.d/default.conf.production.template /etc/nginx/conf.d/default.conf
else
  cp /etc/nginx/conf.d/default.conf.development.template /etc/nginx/conf.d/default.conf
fi

# Reemplaza las variables de entorno en el archivo de configuración de Nginx
envsubst '$CERTBOT_DOMAIN' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf

# Inicia Nginx en primer plano
nginx -g 'daemon off;'