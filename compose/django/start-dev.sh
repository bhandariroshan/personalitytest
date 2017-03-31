#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver_plus 0.0.0.0:8005
