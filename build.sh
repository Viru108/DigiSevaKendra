#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

rm -rf staticfiles
python manage.py collectstatic --noinput
python manage.py migrate
