#!/bin/bash

echo "Applying migrations..."
python manage.py migrate

echo "Starting ASGI application with Daphne..."
daphne -b 0.0.0.0 -p ${PORT:-8080} django_chat.asgi:application
