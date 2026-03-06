import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digisevakendra.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Delete existing admin if any
User.objects.filter(username='admin').delete()

# Create fresh superuser
User.objects.create_superuser(
    username='admin',
    email='admin@dsk.com',
    password='Admin@1234',
    full_name='Super Admin',
    phone='9000000000',
)

print("✅ Superuser created!")
print("   Email:    admin@dsk.com")
print("   Password: Admin@1234")
print("   Login at: http://127.0.0.1:8000/admin/")
