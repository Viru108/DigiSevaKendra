from django.core.management.base import BaseCommand
from departments.models import City, Department, Category

class Command(BaseCommand):
    help = 'Seed initial data for Cities and Departments'

    def handle(self, *args, **kwargs):
        # Create Cities
        cities_data = [
            {'name': 'Hubli', 'state': 'Karnataka', 'city_code': 'HBL', 'latitude': 15.3647, 'longitude': 75.1240},
            {'name': 'Dharwad', 'state': 'Karnataka', 'city_code': 'DWD', 'latitude': 15.4589, 'longitude': 75.0078},
            {'name': 'Bangalore', 'state': 'Karnataka', 'city_code': 'BLR', 'latitude': 12.9716, 'longitude': 77.5946},
        ]
        
        for city_info in cities_data:
            city, created = City.objects.get_or_create(city_code=city_info['city_code'], defaults=city_info)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created City: {city.name}'))

        # Create Departments for Hubli
        hubli = City.objects.get(city_code='HBL')
        deps_data = [
            {'name': 'Water Supply', 'description': 'Maintenance of water infrastructure'},
            {'name': 'Waste Management', 'description': 'Garbage collection and disposal'},
            {'name': 'Road Maintenance', 'description': 'Fixing potholes and street lights'},
            {'name': 'Health & Sanitation', 'description': 'Public health services'},
        ]

        for dep_info in deps_data:
            dep, created = Department.objects.get_or_create(name=dep_info['name'], city=hubli, defaults={'description': dep_info['description']})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Department: {dep.name} for Hubli'))
                
                # Create Categories for each department
                if dep.name == 'Road Maintenance':
                    Category.objects.create(name='Pothole Detection', department=dep)
                    Category.objects.create(name='Street Light Malfunction', department=dep)
                elif dep.name == 'Water Supply':
                    Category.objects.create(name='Pipe Leakage', department=dep)
                    Category.objects.create(name='Dirty Water', department=dep)
