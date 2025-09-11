from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from settings_app.models import CompanySettings, SystemSettings, UserPermission, SystemLog
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate settings app with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting settings data population...'))
        
        # Create or update company settings
        company_settings, created = CompanySettings.objects.get_or_create(
            defaults={
                'name': 'Sheba Software',
                'tagline': 'Innovative Software Solutions for Modern Business',
                'description': 'Sheba Software is a leading software development company specializing in web applications, mobile apps, and enterprise solutions. We help businesses transform their ideas into powerful digital solutions.',
                'email': 'info@shebasoftware.com',
                'phone': '+1-555-123-4567',
                'address': '123 Tech Street, Silicon Valley, CA 94000, USA',
                'website': 'https://shebasoftware.com',
                'facebook_url': 'https://facebook.com/shebasoftware',
                'twitter_url': 'https://twitter.com/shebasoftware',
                'linkedin_url': 'https://linkedin.com/company/shebasoftware',
                'instagram_url': 'https://instagram.com/shebasoftware',
                'github_url': 'https://github.com/shebasoftware',
                'tax_id': 'TAX123456789',
                'registration_number': 'REG987654321'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created company settings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Company settings already exist')
            )
        
        # Create or update system settings
        system_settings, created = SystemSettings.objects.get_or_create(
            defaults={
                'smtp_host': 'smtp.gmail.com',
                'smtp_port': 587,
                'smtp_username': 'noreply@shebasoftware.com',
                'smtp_password': 'app_password_here',
                'smtp_use_tls': True,
                'auto_backup_enabled': True,
                'backup_frequency': 'daily',
                'session_timeout': 30,
                'max_login_attempts': 5,
                'password_expiry_days': 90,
                'api_rate_limit': 1000
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created system settings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('System settings already exist')
            )
        
        # Get admin user for permissions and logs
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(
                    self.style.ERROR('No admin user found. Please create one first.')
                )
                return
        
        # Create sample user permissions
        permissions_data = [
            ('dashboard.view', True),
            ('projects.view', True),
            ('projects.add', True),
            ('projects.change', True),
            ('clients.view', True),
            ('clients.add', True),
            ('content.view', True),
            ('content.change', True),
            ('communication.view', True),
            ('settings.view', True),
            ('users.view', True),
        ]
        
        # Get or create a manager user for permission examples
        manager_user, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@shebasoftware.com',
                'first_name': 'Project',
                'last_name': 'Manager',
                'role': 'manager',
                'is_active': True
            }
        )
        
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            self.stdout.write(
                self.style.SUCCESS('Created manager user for permission examples')
            )
        
        for permission, granted in permissions_data:
            user_permission, created = UserPermission.objects.get_or_create(
                user=manager_user,
                permission=permission,
                defaults={
                    'granted': granted,
                    'granted_by': admin_user
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created permission: {permission} for {manager_user.username}')
                )
        
        # Create sample system logs
        logs_data = [
            {
                'level': 'info',
                'message': 'System started successfully',
                'module': 'system',
                'user': admin_user,
                'ip_address': '127.0.0.1',
                'extra_data': {'startup_time': '2.3s'}
            },
            {
                'level': 'info',
                'message': 'User logged in successfully',
                'module': 'authentication',
                'user': admin_user,
                'ip_address': '192.168.1.100',
                'extra_data': {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            },
            {
                'level': 'warning',
                'message': 'Failed login attempt detected',
                'module': 'authentication',
                'user': None,
                'ip_address': '192.168.1.200',
                'extra_data': {'attempted_username': 'hacker', 'attempts': 3}
            },
            {
                'level': 'info',
                'message': 'Database backup completed successfully',
                'module': 'backup',
                'user': None,
                'ip_address': None,
                'extra_data': {'backup_size': '45.2 MB', 'duration': '12s'}
            },
            {
                'level': 'error',
                'message': 'Email sending failed',
                'module': 'communication',
                'user': admin_user,
                'ip_address': '127.0.0.1',
                'extra_data': {'smtp_error': 'Connection timeout', 'recipient': 'client@example.com'}
            },
            {
                'level': 'info',
                'message': 'New project created',
                'module': 'projects',
                'user': admin_user,
                'ip_address': '192.168.1.100',
                'extra_data': {'project_name': 'E-commerce Platform', 'client_id': 1}
            },
            {
                'level': 'debug',
                'message': 'API request processed',
                'module': 'api',
                'user': manager_user,
                'ip_address': '192.168.1.150',
                'extra_data': {'endpoint': '/api/projects/', 'method': 'GET', 'response_time': '0.15s'}
            },
            {
                'level': 'warning',
                'message': 'High API usage detected',
                'module': 'api',
                'user': manager_user,
                'ip_address': '192.168.1.150',
                'extra_data': {'requests_count': 950, 'limit': 1000, 'time_window': '1 hour'}
            },
            {
                'level': 'info',
                'message': 'System settings updated',
                'module': 'settings',
                'user': admin_user,
                'ip_address': '127.0.0.1',
                'extra_data': {'changed_fields': ['session_timeout', 'api_rate_limit']}
            },
            {
                'level': 'critical',
                'message': 'Disk space running low',
                'module': 'system',
                'user': None,
                'ip_address': None,
                'extra_data': {'available_space': '2.1 GB', 'threshold': '5 GB'}
            }
        ]
        
        for i, log_data in enumerate(logs_data):
            # Create logs with different timestamps
            created_at = datetime.now() - timedelta(hours=i*2)
            
            system_log, created = SystemLog.objects.get_or_create(
                level=log_data['level'],
                message=log_data['message'],
                module=log_data['module'],
                defaults={
                    'user': log_data['user'],
                    'ip_address': log_data['ip_address'],
                    'extra_data': log_data['extra_data'],
                    'created_at': created_at
                }
            )
            if created:
                # Update the created_at field manually since get_or_create doesn't use it
                system_log.created_at = created_at
                system_log.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created system log: {log_data["message"][:30]}...')
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated settings data!'))
