#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver_plus 104.131.26.107:8000
