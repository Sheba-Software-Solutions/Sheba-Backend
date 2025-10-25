from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import ActivityLog
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Fix timezone issues in ActivityLog entries'

    def handle(self, *args, **options):
        # Get all ActivityLog entries
        activities = ActivityLog.objects.all()
        
        fixed_count = 0
        for activity in activities:
            # Check if created_at is naive
            if activity.created_at.tzinfo is None:
                # Convert to timezone-aware datetime
                # Assuming the naive datetime was in the default timezone
                default_tz = timezone.get_default_timezone()
                activity.created_at = default_tz.localize(activity.created_at)
                activity.save(update_fields=['created_at'])
                fixed_count += 1
                
        self.stdout.write(
            self.style.SUCCESS(f'Fixed {fixed_count} ActivityLog entries with timezone issues')
        )