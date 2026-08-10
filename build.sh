#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying Database Migrations..."
python manage.py migrate --noinput

echo "Collecting Static Files..."
python manage.py collectstatic --noinput
