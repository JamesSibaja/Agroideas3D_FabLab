.PHONY: setup run

setup:
	@read -p "¿Estás trabajando en un entorno de producción? (y/n): " IS_PRODUCTION; \
	export IS_PRODUCTION; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		make env start_services generate_certs; \
	else \
		make env start_services; \
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
	echo "POSTGRES_PASSWORD=agro3D" >> .env; \
	echo "POSTGRES_HOST=db" >> .env; \
	echo "POSTGRES_PORT=5432" >> .env; \
	echo "DJANGO_SECRET_KEY=$$secret_key" >> .env; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		echo "DJANGO_DEBUG=False" >> .env; \
	else \
		echo "DJANGO_DEBUG=True" >> .env; \
	fi; \
	echo "DJANGO_SUPERUSER_EMAIL=$$email" >> .env; \
	echo "CERTBOT_EMAIL=$$email" >> .env;

generate_certs:
	@echo "Generando certificados para el entorno de producción..."
	sudo docker compose run --rm --user=root --entrypoint "certbot certonly --nginx --agree-tos --email $$(cat .env | grep CERTBOT_EMAIL | cut -d '=' -f2) -d $$(cat .env | grep CERTBOT_DOMAIN | cut -d '=' -f2)" certbot
	sudo mkdir -p ./nginx/snippets
	sudo docker cp certbot:/etc/letsencrypt/options-ssl-nginx.conf ./nginx/snippets/
	sudo docker cp certbot:/etc/letsencrypt/ssl-dhparams.pem ./nginx/snippets/

start_services: start_django start_nginx

start_django:
	@echo "Configurando el entorno virtual y las dependencias..."
	mkdir -p agroideas/media/slide agroideas/media/archivo
	sudo apt-get install python3-pip python3-venv
	python3 -m venv agroideas/venv
	. agroideas/venv/bin/activate && pip install --upgrade pip
	sudo docker compose build db gunicorn
	sudo docker compose up --no-build -d --no-recreate db gunicorn

	# Run database migrations
	docker compose exec gunicorn python manage.py makemigrations
	docker compose exec gunicorn python manage.py migrate
	sleep 10

	# Create superuser
	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"

start_nginx:
	@echo "Iniciando Nginx..."
	sudo docker compose up --build -d nginx

run:
	export DJANGO_SETTINGS_MODULE=settings; \
	if [ "$$IS_PRODUCTION" = "y" ]; then \
		docker compose up --no-build --no-recreate db gunicorn nginx certbot; \
	else \
		docker compose up --no-build --no-recreate db gunicorn nginx; \
	fi; \

migration:
	export DJANGO_SETTINGS_MODULE=settings
	docker compose up --no-build -d --no-recreate db gunicorn nginx certbot
	docker compose exec gunicorn python manage.py makemigrations
	docker compose exec gunicorn python manage.py migrate
	docker compose down

clean:
	docker compose down
	rm -rf docs/

reset:
	docker compose up --no-build -d --no-recreate db gunicorn nginx certbot
	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"

# .PHONY: setup run

# setup:
#  	# sudo apt-get install docker-ce docker-ce-cli containerd.io
# 	export DJANGO_SETTINGS_MODULE=agroideas.agroideas.settings
# 	mkdir -p agroideas/media/slide agroideas/media/archivo
# 	sudo apt-get install python3-pip
# 	sudo apt-get install python3-venv
# 	python3 -m venv agroideas/venv
# 	touch .env
# 	. agroideas/venv/bin/activate && pip install --upgrade pip
	
#     #sudo docker compose build redis db db_setup gunicorn daphne celery nginx

# 	sudo docker compose build db gunicorn nginx certbot

#     # Iniciar los servicios para obtener certificados SSL
# 	sudo docker compose up --no-build -d --no-recreate db gunicorn nginx
# 	sudo docker compose run --rm certbot certonly --webroot --webroot-path=/app --email tu-email@example.com --agree-tos --no-eff-email -d tu-dominio.com -d www.tu-dominio.com
    

#     # Iniciar y configurar las bases de datos PostgreSQL
# 	sudo docker compose down
# 	docker compose up --no-build -d --no-recreate db gunicorn nginx

	
# 	docker compose exec gunicorn python manage.py makemigrations
# 	docker compose exec gunicorn python manage.py migrate
# 	sleep 10
	
#     # Crear un superusuario (cambiar los valores de acuerdo a tus necesidades) 
#     # docker compose exec gunicorn python manage.py createsuperuser --username=postgres --email=jsibajagranados2@gmail.com
# 	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"

#     # sudo docker compose build db_setup 
#     # docker compose up --no-build -d --no-recreate db_setup
	
# init-docs: # docker compose run documentation make -C agroideas/docs html
# 	if [ ! -d "./docs" ]; then \
#         mkdir docs; \
# 		. agroideas/venv/bin/activate && pip install --upgrade pip; \
# 		pip install -U sphinx; \
#         cd docs && sphinx-quickstart; \
#     fi
# 	sudo docker compose build documentation	

# generate-docs:
# 	docker compose up --no-build -d --no-recreate documentation
# 	# docker compose exec documentation make -C /app/docs html
# 	cd ./docs/build/html && python3 -m http.server 8080

# generate-pdf: generate-docs
# 	docker compose run documentation make -C agroideas/docs latexpdf

# # Arrancar el servidor Django y Celery
# run:
# 	export DJANGO_SETTINGS_MODULE=settings
# 	docker compose up --no-build  --no-recreate db gunicorn nginx

# migration:
# 	export DJANGO_SETTINGS_MODULE=settings
# 	docker compose up --no-build -d --no-recreate db gunicorn nginx
# 	docker compose exec gunicorn python manage.py makemigrations
# 	docker compose exec gunicorn python manage.py migrate
# 	docker compose down

# clean:
# 	docker compose down
# 	rm -rf docs/

# reset:
# 	docker compose up --no-build -d --no-recreate db gunicorn nginx
# 	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"

