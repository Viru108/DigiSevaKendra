from accounts.models import CustomUser
from departments.models import City, Department, Category
from complaints.models import Complaint
from complaints.services import assign_technician
from django.utils import timezone
import io
import sys

# Capture output
output = io.StringIO()
sys.stdout = output

# 1. Setup
city = City.objects.get(name='Hubli')
dept = Department.objects.get(name='Road Maintenance')
cat = Category.objects.filter(department=dept).first()
citizen = CustomUser.objects.filter(role='CITIZEN').first()

# Identify ALL techs in this dept/city
all_techs = list(CustomUser.objects.filter(role='TECHNICIAN', city=city, department=dept))
print(f'DEBUG: Found {len(all_techs)} technicians in {city.name}/{dept.name}')

# Clear all their tasks
Complaint.objects.filter(assigned_to__in=all_techs, status__in=['ASSIGNED', 'IN_PROGRESS']).update(status='RESOLVED', assigned_to=None)
Complaint.objects.filter(ticket_id__startswith='VERIF-').delete()

# 2. Fill up all technicians
for i, tech in enumerate(all_techs):
    tid = f'VERIF-BUSY-{i}'
    c = Complaint.objects.create(
        citizen=citizen, city=city, department=dept, category=cat,
        description=f'Busy Task {i}', ticket_id=tid, status='PENDING',
        latitude=15.0, longitude=75.0, pincode='000000', formatted_address='Test',
        before_image='test.jpg'
    )
    assign_technician(c)
    c.refresh_from_db()
    print(f'--- Task {tid} assigned to {c.assigned_to.full_name if c.assigned_to else "NONE"} (Status: {c.status})')

# 3. Try to assign one more (should remain PENDING)
c_extra = Complaint.objects.create(
    citizen=citizen, city=city, department=dept, category=cat,
    description='Extra Task', ticket_id='VERIF-PENDING-1', status='PENDING',
    latitude=15.0, longitude=75.0, pincode='000000', formatted_address='Test',
    before_image='test.jpg'
)
assign_technician(c_extra)
c_extra.refresh_from_db()
print(f'--- Extra Task Status: {c_extra.status} (Expected: PENDING)')

# 4. Free up ONE technician and trigger auto-assignment
# Resolve the first busy task
c_busy_1 = Complaint.objects.get(ticket_id='VERIF-BUSY-0')
freed_tech = c_busy_1.assigned_to
c_busy_1.status = 'RESOLVED'
c_busy_1.save()
print(f'--- Handled Task {c_busy_1.ticket_id}. Technician {freed_tech.full_name} is now free.')

# Simulate view logic (find next pending and assign)
next_task = Complaint.objects.filter(status='PENDING', city=city, department=dept).order_by('created_at').first()
if next_task:
    assign_technician(next_task)

c_extra.refresh_from_db()
print(f'--- Extra Task Status after freeing tech: {c_extra.status}, Assigned To: {c_extra.assigned_to.full_name if c_extra.assigned_to else "NONE"}')

# Write results
with open(r'c:\Users\aniki\Desktop\DigiSevaKendra\verif_results.txt', 'w') as f:
    f.write(output.getvalue())
