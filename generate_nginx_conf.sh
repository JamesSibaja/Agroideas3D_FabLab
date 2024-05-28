#!/bin/sh

# Comprueba si los certificados SSL están presentes
if [ -f /etc/letsencrypt/options-ssl-nginx.conf ]; then
    SSL_BLOCK=$(cat <<EOF
server {
    listen 443 ssl;
    server_name ${CERTBOT_DOMAIN};

    ssl_certificate /etc/letsencrypt/live/${CERTBOT_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${CERTBOT_DOMAIN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://gunicorn:8765;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }
}
EOF
)
else
    SSL_BLOCK=""
fi

envsubst '${CERTBOT_DOMAIN} ${SSL_BLOCK}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'

