#!/bin/bash

echo "Creating tables..."
python manage.py create_db

echo "Initializing tables..."
python manage.py db init

echo "Apply database migrations..."
python manage.py db migrate

echo "Running the server..."
python manage.py runserver