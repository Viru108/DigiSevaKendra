import random
import string
from django.db import models
from django.utils import timezone

from .models import Complaint

def generate_ticket_id(city_code, pincode):
    year = timezone.now().year
    # Sequence: Count complaints for this city and year
    count = Complaint.objects.filter(city__city_code=city_code, created_at__year=year).count() + 1
    sequence = str(count).zfill(4)
    # CITYCODE-PINCODE-YEAR-SEQUENCE
    return f"{city_code}-{pincode}-{year}-{sequence}"

def assign_technician(complaint):
    from accounts.models import CustomUser
    technicians = CustomUser.objects.filter(
        role='TECHNICIAN',
        department=complaint.department,
        city=complaint.city,
        is_available=True
    ).annotate(
        active_count=models.Count(
            'assigned_tasks', 
            filter=models.Q(assigned_tasks__status__in=['ASSIGNED', 'IN_PROGRESS'])
        )
    ).filter(active_count=0)
    
    if technicians.exists():
        assigned_tech = technicians.first()
        complaint.assigned_to = assigned_tech
        complaint.status = 'ASSIGNED'
        complaint.save()
        return assigned_tech
    return None
