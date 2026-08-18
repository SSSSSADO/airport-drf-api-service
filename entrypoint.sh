#!/bin/sh

set -e

echo "Applying database migrations..."
python manage.py migrate --noinput
echo "----------Migrate-OK----------"

echo "Creating demo superuser..."
python manage.py create_demo_superuser
echo "----------SuperUser-OK----------"

echo "Loading demo data..."
python manage.py loaddata airport_data
echo "----------Data-OK----------"

echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:8000
echo "----------ServerUP-OK----------"