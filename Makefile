.PHONY run migrate pipinstall startapp

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

pipinstall:
    python -m pip install $(package)

startapp:
    python manage.py startapp $(app)