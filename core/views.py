from django.shortcuts import render
from departments.models import Department, City

def landing(request):
    departments = Department.objects.filter(is_active=True)[:6]
    cities = City.objects.filter(is_active=True)
    return render(request, 'core/landing.html', {
        'departments': departments,
        'cities': cities
    })
