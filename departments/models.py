from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departments')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.city.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='categories')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
