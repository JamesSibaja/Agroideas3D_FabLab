.PHONY: setup run

setup:
 	# sudo apt-get install docker-ce docker-ce-cli containerd.io
	export DJANGO_SETTINGS_MODULE=agroideas.agroideas.settings
	mkdir -p agroideas/media/slide agroideas/media/archivo
	sudo apt-get install python3-pip
	sudo apt-get install python3-venv
	python3 -m venv agroideas/venv
	touch .env
	. agroideas/venv/bin/activate && pip install --upgrade pip
	
    #sudo docker compose build redis database database_setup gunicorn daphne celery nginx
	sudo docker compose build database gunicorn nginx

    # Iniciar y configurar las bases de datos PostgreSQL
	docker compose up --no-build -d --no-recreate database gunicorn nginx

	
	docker compose exec gunicorn python manage.py makemigrations
	docker compose exec gunicorn python manage.py migrate
	sleep 10
	
    # Crear un superusuario (cambiar los valores de acuerdo a tus necesidades) 
    # docker compose exec gunicorn python manage.py createsuperuser --username=postgres --email=jsibajagranados2@gmail.com
	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"

    # sudo docker compose build database_setup 
    # docker compose up --no-build -d --no-recreate database_setup
	
init-docs: # docker compose run documentation make -C agroideas/docs html
	if [ ! -d "./docs" ]; then \
        mkdir docs; \
		. agroideas/venv/bin/activate && pip install --upgrade pip; \
		pip install -U sphinx; \
        cd docs && sphinx-quickstart; \
    fi
	sudo docker compose build documentation	

generate-docs:
	docker compose up --no-build -d --no-recreate documentation
	# docker compose exec documentation make -C /app/docs html
	cd ./docs/build/html && python3 -m http.server 8080

generate-pdf: generate-docs
	docker compose run documentation make -C agroideas/docs latexpdf

# Arrancar el servidor Django y Celery
run:
	export DJANGO_SETTINGS_MODULE=settings
	docker compose up --no-build  --no-recreate database gunicorn nginx

migration:
	export DJANGO_SETTINGS_MODULE=settings
	docker compose up --no-build -d --no-recreate database gunicorn nginx
	docker compose exec gunicorn python manage.py makemigrations
	docker compose exec gunicorn python manage.py migrate
	docker compose down

clean:
	docker compose down
	rm -rf docs/

reset:
	docker compose up --no-build -d --no-recreate database gunicorn nginx
	@docker compose exec gunicorn python manage.py shell -c "from django.contrib.auth.models import User; from getpass import getpass; username='postgres'; email='jsibajagranados2@gmail.com'; password=getpass('Enter password for superuser: '); User.objects.create_superuser(username, email, password) if not User.objects.filter(username=username).exists() else print('Superuser already exists')"

