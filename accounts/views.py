from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CitizenRegistrationForm, AddOfficerForm, AddTechnicianForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
import uuid


def register_view(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to DigiSevaKendra, {user.full_name}!")
            return redirect('dashboard')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role == 'CITIZEN':
        from complaints.models import Complaint
        complaints = Complaint.objects.filter(citizen=user).order_by('-created_at')
        context['complaints'] = complaints
        context['stats'] = {
            'total': complaints.count(),
            'in_progress': complaints.filter(status__in=['ASSIGNED', 'IN_PROGRESS']).count(),
            'resolved': complaints.filter(status='RESOLVED').count(),
        }
        return render(request, 'accounts/citizen_dashboard.html', context)

    elif user.role == 'TECHNICIAN':
        from complaints.models import Complaint
        context['assigned_tasks'] = Complaint.objects.filter(assigned_to=user).exclude(status__in=['RESOLVED', 'CLOSED']).order_by('sla_deadline')
        context['resolved_count'] = Complaint.objects.filter(assigned_to=user, status__in=['RESOLVED', 'CLOSED']).count()
        return render(request, 'accounts/technician_dashboard.html', context)

    elif user.role == 'OFFICER':
        from complaints.models import Complaint
        dept_complaints = Complaint.objects.filter(city=user.city, department=user.department).order_by('-created_at')
        technicians = CustomUser.objects.filter(role='TECHNICIAN', city=user.city, department=user.department)
        context['dept_complaints'] = dept_complaints
        context['technicians'] = technicians
        context['stats'] = {
            'pending': dept_complaints.filter(status='PENDING').count(),
            'sla_risks': dept_complaints.filter(sla_breached=True).count(),
        }
        return render(request, 'accounts/officer_dashboard.html', context)

    elif user.role == 'HEAD':
        return redirect('head_dashboard')

    return render(request, 'accounts/dashboard.html', context)


# ─── Head: Manage Officers ───────────────────────────────────────────────────

@login_required
def add_officer_view(request):
    if request.user.role != 'HEAD':
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    city = request.user.city

    if request.method == 'POST':
        form = AddOfficerForm(city=city, data=request.POST)
        if form.is_valid():
            d = form.cleaned_data
            # Check for duplicate email / phone
            if CustomUser.objects.filter(email=d['email']).exists():
                messages.error(request, "A user with this email already exists.")
            elif CustomUser.objects.filter(phone=d['phone']).exists():
                messages.error(request, "A user with this phone number already exists.")
            else:
                username = f"officer_{uuid.uuid4().hex[:8]}"
                officer = CustomUser.objects.create_user(
                    username=username,
                    email=d['email'],
                    password=d['password'],
                    full_name=d['full_name'],
                    phone=d['phone'],
                    role='OFFICER',
                    city=city,
                    department=d['department'],
                )
                messages.success(request, f"Officer '{officer.full_name}' added to {officer.department.name}.")
                return redirect('head_dashboard')
    else:
        form = AddOfficerForm(city=city)

    officers = CustomUser.objects.filter(role='OFFICER', city=city)
    return render(request, 'accounts/add_officer.html', {'form': form, 'officers': officers, 'city': city})


# ─── Officer: Manage Technicians ─────────────────────────────────────────────

@login_required
def add_technician_view(request):
    if request.user.role != 'OFFICER':
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    officer = request.user
    department = officer.department
    city = officer.city

    if request.method == 'POST':
        form = AddTechnicianForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            if CustomUser.objects.filter(email=d['email']).exists():
                messages.error(request, "A user with this email already exists.")
            elif CustomUser.objects.filter(phone=d['phone']).exists():
                messages.error(request, "A user with this phone number already exists.")
            else:
                username = f"tech_{uuid.uuid4().hex[:8]}"
                tech = CustomUser.objects.create_user(
                    username=username,
                    email=d['email'],
                    password=d['password'],
                    full_name=d['full_name'],
                    phone=d['phone'],
                    role='TECHNICIAN',
                    city=city,
                    department=department,
                )
                messages.success(request, f"Technician '{tech.full_name}' added to {department.name}. They are now eligible for auto-assignment.")
                return redirect('dashboard')
    else:
        form = AddTechnicianForm()

    technicians = CustomUser.objects.filter(role='TECHNICIAN', city=city, department=department)
    return render(request, 'accounts/add_technician.html', {
        'form': form,
        'technicians': technicians,
        'department': department,
        'city': city,
    })


# ─── Officer: Remove Technician ─────────────────────────────────────────────

@login_required
def remove_technician_view(request, tech_id):
    if request.user.role != 'OFFICER':
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    officer = request.user
    tech = get_object_or_404(
        CustomUser,
        id=tech_id,
        role='TECHNICIAN',
        city=officer.city,
        department=officer.department,
    )

    if request.method == 'POST':
        name = tech.full_name
        tech.delete()
        messages.success(request, f"Technician '{name}' has been removed successfully.")
        return redirect('add_technician')

    # If accessed via GET, just redirect back
    return redirect('add_technician')
