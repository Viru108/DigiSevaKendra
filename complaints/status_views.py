from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Complaint
from django.utils import timezone

@login_required
def update_complaint_status(request, ticket_id):
    complaint = get_object_or_404(Complaint, ticket_id=ticket_id)
    
    # Permission check: Only assigned technician or officer can update
    if request.user.role == 'TECHNICIAN' and complaint.assigned_to != request.user:
        return redirect('dashboard')
        
    new_status = request.POST.get('status')
    if new_status in dict(Complaint.STATUS_CHOICES):
        complaint.status = new_status
        if new_status == 'RESOLVED':
            complaint.resolved_at = timezone.now()
        elif new_status == 'CLOSED':
            complaint.closed_at = timezone.now()
        complaint.save()
        
    return redirect('dashboard')
