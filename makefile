.PHONY: setup run

setup:
	@read -p "¿Estás trabajando en un entorno de producción? (y/n): " IS_PRODUCTION; \
	export IS_PRODUCTION; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		make env create_directories set_permissions start_services generate_certs enable_https; \
	else \
		make env create_directories set_permissions start_services; \
	fi

env:
	@echo "Configurando el archivo .env..." 
	@if [ "$$IS_PRODUCTION" = "y" ]; then \
		read -p "Introduce el dominio del servidor (p.ej., example.com): " domain; \
	else \
		domain="localhost"; \
	fi; \
	echo "DJANGO_ALLOWED_HOSTS=$$domain" > .env; \
	echo "CSRF_TRUSTED_ORIGINS=https://$$domain" >> .env; \
	echo "CERTBOT_DOMAIN=$$domain" >> .env; \
	read -p "Introduce el correo electrónico para el superusuario: " email; \
	secret_key=$$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))'); \
	echo "POSTGRES_DB=agro" >> .env; \
	echo "POSTGRES_USER=postgres" >> .env; \
	echo "NGINX_HTTP_PORT=80" >> .env; \
	echo "POSTGRES_PASSWORD=agro3D" >> .env; \
	echo "POSTGRES_HOST=db" >> .env; \
	echo "POSTGRES_PORT=5432" >> .env; \
	echo "DJANGO_SECRET_KEY=$$secret_key" >> .env; \
	echo "IS_PRODUCTION=$$IS_PRODUCTION" >> .env; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		echo "DJANGO_DEBUG=False" >> .env; \
		echo "NGINX_HTTPS_PORT=443" >> .env; \
	else \
		echo "DJANGO_DEBUG=True" >> .env; \
		echo "NGINX_HTTPS_PORT=" >> .env; \
	fi; \
	echo "DJANGO_SUPERUSER_EMAIL=$$email" >> .env; \
	echo "CERTBOT_EMAIL=$$email" >> .env;

create_directories:
	@echo "Creando directorios necesarios..."
	mkdir -p ./certbot/www
	mkdir -p ./certbot/conf
	mkdir -p ./nginx/snippets
	sudo mkdir -p /var/www/certbot/.well-known/acme-challenge

set_permissions:
	@echo "Ajustando permisos de directorios..."
	sudo chmod -R 755 ./certbot/www
	sudo chmod -R 755 ./certbot/conf
	sudo chmod -R 755 ./nginx/snippets
	sudo chmod -R 755 /var/www/certbot/.well-known/acme-challenge

generate_certs:
	@echo "Generando certificados para el entorno de producción..."
	docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email $$(grep CERTBOT_EMAIL .env | cut -d '=' -f2) --agree-tos --no-eff-email -d $$(grep CERTBOT_DOMAIN .env | cut -d '=' -f2)
	sudo mkdir -p ./nginx/snippets
	sudo docker cp $$(docker compose ps -q certbot):/etc/letsencrypt/options-ssl-nginx.conf ./nginx/snippets/
	sudo docker cp $$(docker compose ps -q certbot):/etc/letsencrypt/ssl-dhparams.pem ./nginx/snippets/

start_services:
	@echo "Iniciando Nginx y otros servicios..."
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		CERTBOT_DOMAIN=$$(grep CERTBOT_DOMAIN .env | cut -d '=' -f2) && \
		envsubst '$$CERTBOT_DOMAIN' < nginx.conf.http.template > nginx.conf; \
	else \
		CERTBOT_DOMAIN=$$(grep CERTBOT_DOMAIN .env | cut -d '=' -f2) && \
		envsubst '$$CERTBOT_DOMAIN' < nginx.conf.development.template > nginx.conf; \
	fi;

	@echo "Instalando dependencias del sistema necesarias para lxml..."
	# Instalar dependencias del sistema necesarias para lxml (libxml2, libxslt, python3-dev)
	sudo apt-get update && sudo apt-get install -y \
		libxml2-dev \
		libxslt1-dev \
		ffmpeg \
		python3-dev

	@echo "Configurando el entorno virtual y las dependencias de Python..."
	mkdir -p agroideas/media/slide agroideas/media/archivo

	# Crear entorno virtual solo si no existe
	if [ ! -d "agroideas/venv" ]; then \
		python3 -m venv agroideas/venv; \
	fi;
	@echo "Activando el entorno virtual y actualizando pip..."
	. agroideas/venv/bin/activate && pip install --upgrade pip

	# Instalar las dependencias del proyecto desde requirements.txt
	@echo "Instalando las dependencias de Python desde requirements.txt..."
	. agroideas/venv/bin/activate && pip install -r requirements.txt

	@echo "Construyendo y levantando servicios Docker..."
	sudo docker compose build db gunicorn nginx
	sudo docker compose up --no-build -d --no-recreate db gunicorn nginx

	# Ejecutar migraciones de base de datos

	@docker compose exec gunicorn python manage.py makemigrations
	@docker compose exec gunicorn /app/wait-for-db.sh db python manage.py migrate
	sleep 10

	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='fablab';email='jsibajagranados2@gmail.com'; password=getpass('Introducir contraseña para superusuario: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"
 
enable_https:
	@echo "Reconfigurando Nginx para HTTPS..."
	sudo docker compose down
	CERTBOT_DOMAIN=$$(grep CERTBOT_DOMAIN .env | cut -d '=' -f2) envsubst '$$CERTBOT_DOMAIN' < nginx.conf.production.template > nginx.conf; \
	sudo docker compose up -d db gunicorn nginx

run:
	export DJANGO_SETTINGS_MODULE=settings; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		docker compose up --no-build --no-recreate db gunicorn nginx certbot; \
	else \
		docker compose up --no-build --no-recreate db gunicorn nginx; \
	fi; \

run2:
	export DJANGO_SETTINGS_MODULE=settings; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		docker compose up -d --no-build --no-recreate db gunicorn nginx certbot; \
	else \
		docker compose up -d --no-build --no-recreate db gunicorn nginx; \
	fi; \

migration:
	export DJANGO_SETTINGS_MODULE=settings
	docker compose up --no-build -d --no-recreate db gunicorn nginx
	docker compose exec gunicorn python manage.py makemigrations
	docker compose exec gunicorn python manage.py migrate
	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='fablab';email='jsibajagranados2@gmail.com'; password=getpass('Introducir contraseña para superusuario: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"
	docker compose down

clean:
	docker compose down
	rm -rf docs/

reset:
	docker compose up --no-build -d --no-recreate db gunicorn nginx certbot
	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"
