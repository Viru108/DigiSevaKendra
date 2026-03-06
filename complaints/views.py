from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm, ComplaintResolveForm
from .services import generate_ticket_id, assign_technician
from django.http import JsonResponse
from django.utils import timezone
from .models import Complaint
from departments.models import Category

@login_required
def raise_complaint(request):
    user = request.user

    # Guard: citizen must have a city assigned
    if not user.city:
        messages.error(request, "Your account is not linked to a city. Please contact support.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                complaint = form.save(commit=False)
                complaint.citizen = user
                complaint.city = user.city
                complaint.ticket_id = generate_ticket_id(user.city.city_code, complaint.pincode)
                complaint.save()

                # Attempt auto-assignment
                assign_technician(complaint)

                messages.success(request, f"Complaint submitted! Your ticket ID is {complaint.ticket_id}.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Submission failed: {e}")
        else:
            # Surface form field errors as a message for easy debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ComplaintForm()
    return render(request, 'complaints/raise_complaint.html', {'form': form})

def get_categories(request):
    department_id = request.GET.get('department_id')
    categories = Category.objects.filter(department_id=department_id, is_active=True).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

@login_required
def resolve_complaint(request, ticket_id):
    complaint = get_object_or_404(Complaint, ticket_id=ticket_id)
    
    # Security: Only assigned technician can resolve
    if request.user.role != 'TECHNICIAN' or complaint.assigned_to != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ComplaintResolveForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.status = 'RESOLVED'
            complaint.resolved_at = timezone.now()
            complaint.save()

            # Auto-assign next pending task if any
            next_task = Complaint.objects.filter(
                status='PENDING',
                city=complaint.city,
                department=complaint.department
            ).order_by('created_at').first()

            if next_task:
                from .services import assign_technician
                assign_technician(next_task)
                messages.success(request, f"Complaint {ticket_id} marked as RESOLVED. Next task {next_task.ticket_id} has been auto-assigned to you.")
            else:
                messages.success(request, f"Complaint {ticket_id} marked as RESOLVED. Good work!")
            
            return redirect('dashboard')
        else:
            messages.error(request, "Please upload a valid completion photo.")
    else:
        form = ComplaintResolveForm(instance=complaint)
    
    return render(request, 'complaints/resolve_complaint.html', {
        'form': form,
        'complaint': complaint
    })
