import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digisevakendra.settings')

import django
django.setup()

from accounts.models import CustomUser
from departments.models import City

# picking Hubli (ID: 1) as confirmed in previous step
city = City.objects.get(id=1)

# Delete existing if any
CustomUser.objects.filter(username='head_hubli').delete()

# Create Municipal Head
CustomUser.objects.create_user(
    username='head_hubli',
    email='head@dsk.com',
    password='Head@1234',
    full_name='Hubli Municipal Head',
    phone='9888877777',
    role='HEAD',
    city=city,
)

print("✅ Municipal Head account created!")
print("   Email:    head@dsk.com")
print("   Password: Head@1234")
print("   City:     Hubli")
print("   Login at: http://127.0.0.1:8000/accounts/login/")
