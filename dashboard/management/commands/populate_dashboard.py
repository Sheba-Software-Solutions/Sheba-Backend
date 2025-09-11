from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dashboard.models import DashboardMetric, ActivityLog
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate sample dashboard data for testing'

    def handle(self, *args, **options):
        # Get admin user for assignments
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Admin user not found. Please create an admin user first.')
            )
            return

        # Create sample dashboard metrics
        from datetime import date
        
        metrics_data = [
            {
                'metric_type': 'projects_total',
                'value': 15.0,
                'date': date.today()
            },
            {
                'metric_type': 'projects_active',
                'value': 8.0,
                'date': date.today()
            },
            {
                'metric_type': 'clients_total',
                'value': 12.0,
                'date': date.today()
            },
            {
                'metric_type': 'revenue_monthly',
                'value': 45000.0,
                'date': date.today()
            },
            {
                'metric_type': 'revenue_yearly',
                'value': 540000.0,
                'date': date.today()
            },
            {
                'metric_type': 'tasks_completed',
                'value': 127.0,
                'date': date.today()
            },
            {
                'metric_type': 'blog_views',
                'value': 2340.0,
                'date': date.today()
            },
            {
                'metric_type': 'website_visitors',
                'value': 1850.0,
                'date': date.today()
            }
        ]

        for metric_data in metrics_data:
            metric, created = DashboardMetric.objects.get_or_create(
                metric_type=metric_data['metric_type'],
                date=metric_data['date'],
                defaults=metric_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created dashboard metric: {metric.get_metric_type_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Dashboard metric already exists: {metric.get_metric_type_display()}')
                )

        # Create sample activity logs
        activities_data = [
            {
                'user': admin_user,
                'action': 'create',
                'model_name': 'Project',
                'object_id': 1,
                'description': 'Created new project: E-commerce Platform',
                'created_at': datetime.now() - timedelta(hours=2)
            },
            {
                'user': admin_user,
                'action': 'update',
                'model_name': 'Project',
                'object_id': 2,
                'description': 'Updated project status to In Progress',
                'created_at': datetime.now() - timedelta(hours=4)
            },
            {
                'user': admin_user,
                'action': 'create',
                'model_name': 'Client',
                'object_id': 3,
                'description': 'Added new client: TechStart Solutions',
                'created_at': datetime.now() - timedelta(hours=6)
            },
            {
                'user': admin_user,
                'action': 'update',
                'model_name': 'User',
                'object_id': admin_user.id,
                'description': 'Updated user profile information',
                'created_at': datetime.now() - timedelta(hours=8)
            },
            {
                'user': admin_user,
                'action': 'create',
                'model_name': 'BlogPost',
                'object_id': 1,
                'description': 'Published new blog post: Web Development Trends 2024',
                'created_at': datetime.now() - timedelta(days=1)
            },
            {
                'user': admin_user,
                'action': 'delete',
                'model_name': 'ContactSubmission',
                'object_id': 5,
                'description': 'Resolved and archived contact submission',
                'created_at': datetime.now() - timedelta(days=1, hours=3)
            },
            {
                'user': admin_user,
                'action': 'update',
                'model_name': 'Project',
                'object_id': 4,
                'description': 'Marked project as completed',
                'created_at': datetime.now() - timedelta(days=2)
            },
            {
                'user': admin_user,
                'action': 'create',
                'model_name': 'Newsletter',
                'object_id': 2,
                'description': 'Created monthly newsletter campaign',
                'created_at': datetime.now() - timedelta(days=3)
            },
            {
                'user': admin_user,
                'action': 'update',
                'model_name': 'Service',
                'object_id': 2,
                'description': 'Updated service pricing and features',
                'created_at': datetime.now() - timedelta(days=4)
            },
            {
                'user': admin_user,
                'action': 'create',
                'model_name': 'TeamMember',
                'object_id': 4,
                'description': 'Added new team member: Senior Developer',
                'created_at': datetime.now() - timedelta(days=5)
            }
        ]

        for activity_data in activities_data:
            activity, created = ActivityLog.objects.get_or_create(
                user=activity_data['user'],
                action=activity_data['action'],
                model_name=activity_data['model_name'],
                object_id=activity_data['object_id'],
                created_at=activity_data['created_at'],
                defaults=activity_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created activity log: {activity.description}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Activity log already exists: {activity.description}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated dashboard data!')
        )
