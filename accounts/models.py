from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('TECHNICIAN', 'Technician'),
        ('OFFICER', 'Department Officer'),
        ('HEAD', 'Municipal Head'),
        ('SUPERADMIN', 'Superadmin'),
    )
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    city = models.ForeignKey('departments.City', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone']

    def __str__(self):
        return f"{self.full_name} ({self.role})"
