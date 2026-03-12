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
python create_admin.py
<<<<<<< HEAD

=======
>>>>>>> ed9a743ae40ff6c5c1318a3acda992d0f4889eb5
# Sanity check for logs
echo "Static file collection summary (staticfiles folder):"
ls -R staticfiles | head -n 30
