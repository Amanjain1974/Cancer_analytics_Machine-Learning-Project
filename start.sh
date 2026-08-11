#!/usr/bin/env bash
set -o errexit

echo "Applying Database Migrations..."
python manage.py migrate --noinput

echo "Collecting Static Files..."
python manage.py collectstatic --noinput --clear || true

echo "Starting Gunicorn Web Server..."
exec gunicorn cancer_ai.wsgi:application --bind 0.0.0.0:${PORT:-8000}
