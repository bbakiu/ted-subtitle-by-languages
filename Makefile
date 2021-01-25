.PHONY: run migrate pipinstall startapp up down build

run:
	python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
pipinstall:
	python -m pip install $(package)
startapp:
	python manage.py startapp $(app)
up:
	docker-compose up -d --build
build: 
	docker-compose build
down: 
	docker-compose down
