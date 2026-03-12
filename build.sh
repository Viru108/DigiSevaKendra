#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Diagnostics for debugging static files
echo "Current directory: $(pwd)"
echo "Listing core/static contents:"
ls -R core/static

rm -rf staticfiles
python manage.py collectstatic --noinput
python manage.py migrate

# Sanity check for logs
echo "Static file collection summary (staticfiles folder):"
ls -R staticfiles | head -n 30
