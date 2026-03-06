from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

@login_required
def head_dashboard(request):
    if request.user.role != 'HEAD':
        return render(request, '403_error.html')

    from accounts.models import CustomUser
    city = request.user.city
    complaints = Complaint.objects.filter(city=city)

    total_complaints = complaints.count()
    resolved_count = complaints.filter(status='RESOLVED').count()
    breached_count = complaints.filter(sla_breached=True).count()

    status_data = complaints.values('status').annotate(total=Count('id'))
    efficiency_rate = int((resolved_count / total_complaints * 100)) if total_complaints > 0 else 100

    # Staff overview for management panel
    officers = CustomUser.objects.filter(role='OFFICER', city=city).select_related('department')
    from departments.models import Department
    departments = Department.objects.filter(city=city, is_active=True)

    return render(request, 'analytics/head_dashboard.html', {
        'total_complaints': total_complaints,
        'resolved_count': resolved_count,
        'breached_count': breached_count,
        'efficiency_rate': efficiency_rate,
        'status_data': list(status_data),
        'officers': officers,
        'departments': departments,
    })


