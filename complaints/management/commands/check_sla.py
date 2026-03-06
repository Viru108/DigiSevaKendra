from django.core.management.base import BaseCommand
from django.utils import timezone
from complaints.models import Complaint

class Command(BaseCommand):
    help = 'Check and mark complaints that have breached SLA'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        breached_complaints = Complaint.objects.filter(
            status__in=['PENDING', 'ASSIGNED', 'IN_PROGRESS'],
            sla_deadline__lt=now,
            sla_breached=False
        )
        
        count = breached_complaints.count()
        breached_complaints.update(sla_breached=True)
        
        if count > 0:
            self.stdout.write(self.style.WARNING(f'Marked {count} complaints as SLA breached.'))
        else:
            self.stdout.write(self.style.SUCCESS('No new SLA breaches detected.'))
