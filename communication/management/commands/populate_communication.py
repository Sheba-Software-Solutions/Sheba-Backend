from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from communication.models import ContactSubmission, EmailTemplate, Newsletter, NewsletterSubscriber, Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate sample communication data for testing'

    def handle(self, *args, **options):
        # Get admin user for assignments
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Admin user not found. Please create an admin user first.')
            )
            return

        # Create sample contact submissions
        contact_submissions = [
            {
                'name': 'Alice Johnson',
                'email': 'alice@example.com',
                'phone': '+1-555-1111',
                'subject': 'Website Development Inquiry',
                'message': 'Hi, I need a professional website for my small business. Can you help?',
                'status': 'new',
                'ip_address': '192.168.1.100',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            {
                'name': 'Bob Smith',
                'email': 'bob@techcorp.com',
                'phone': '+1-555-2222',
                'subject': 'Mobile App Development',
                'message': 'We need a mobile app for our e-commerce platform. What are your rates?',
                'status': 'in_progress',
                'assigned_to': admin_user,
                'response': 'Thank you for your inquiry. We will send you a detailed proposal.',
                'ip_address': '192.168.1.101',
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            },
            {
                'name': 'Carol Davis',
                'email': 'carol@nonprofit.org',
                'phone': '+1-555-3333',
                'subject': 'Non-profit Website',
                'message': 'Our non-profit organization needs a website to showcase our work and accept donations.',
                'status': 'resolved',
                'assigned_to': admin_user,
                'response': 'We have sent you our non-profit package details. Looking forward to working with you.',
                'ip_address': '192.168.1.102',
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            },
            {
                'name': 'David Wilson',
                'email': 'david@startup.io',
                'phone': '+1-555-4444',
                'subject': 'MVP Development',
                'message': 'We are a startup looking to build our MVP. Do you work with startups?',
                'status': 'new',
                'ip_address': '192.168.1.103',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        ]

        for submission_data in contact_submissions:
            submission, created = ContactSubmission.objects.get_or_create(
                email=submission_data['email'],
                defaults=submission_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created contact submission: {submission.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Contact submission already exists: {submission.name}')
                )

        # Create sample email templates
        email_templates = [
            {
                'name': 'Welcome Email',
                'template_type': 'welcome',
                'subject': 'Welcome to Sheba Software!',
                'content': '''
                <h2>Welcome to Sheba Software!</h2>
                <p>Thank you for choosing us for your software development needs.</p>
                <p>We're excited to work with you and bring your ideas to life.</p>
                <p>Best regards,<br>The Sheba Software Team</p>
                ''',
                'is_active': True
            },
            {
                'name': 'Project Update',
                'template_type': 'notification',
                'subject': 'Project Update: {{project_name}}',
                'content': '''
                <h2>Project Update</h2>
                <p>Hello {{client_name}},</p>
                <p>We have an update on your project: <strong>{{project_name}}</strong></p>
                <p>Current Status: {{project_status}}</p>
                <p>Progress: {{project_progress}}%</p>
                <p>{{update_message}}</p>
                <p>Best regards,<br>Project Team</p>
                ''',
                'is_active': True
            },
            {
                'name': 'Invoice Reminder',
                'template_type': 'invoice',
                'subject': 'Invoice Reminder - {{invoice_number}}',
                'content': '''
                <h2>Invoice Reminder</h2>
                <p>Dear {{client_name}},</p>
                <p>This is a friendly reminder that invoice {{invoice_number}} is due on {{due_date}}.</p>
                <p>Amount: ${{amount}}</p>
                <p>Please process payment at your earliest convenience.</p>
                <p>Thank you,<br>Accounting Team</p>
                ''',
                'is_active': True
            }
        ]

        for template_data in email_templates:
            template, created = EmailTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created email template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Email template already exists: {template.name}')
                )

        # Create sample newsletter subscribers
        subscribers = [
            {'email': 'subscriber1@example.com', 'name': 'John Subscriber', 'is_active': True},
            {'email': 'subscriber2@example.com', 'name': 'Jane Reader', 'is_active': True},
            {'email': 'subscriber3@example.com', 'name': 'Mike Follower', 'is_active': True},
            {'email': 'unsubscribed@example.com', 'name': 'Former Subscriber', 'is_active': False},
        ]

        for subscriber_data in subscribers:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=subscriber_data['email'],
                defaults=subscriber_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created newsletter subscriber: {subscriber.email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Newsletter subscriber already exists: {subscriber.email}')
                )

        # Create sample newsletter
        newsletter_data = {
            'title': 'Monthly Update - December 2024',
            'content': '''
            <h1>Sheba Software Monthly Update</h1>
            <h2>What's New This Month</h2>
            <p>We've been busy working on exciting new projects and features!</p>
            
            <h3>Recent Projects</h3>
            <ul>
                <li>Launched e-commerce platform for TechStartup Inc.</li>
                <li>Completed mobile app for RetailPlus Solutions</li>
                <li>Started new healthcare management system</li>
            </ul>
            
            <h3>Company News</h3>
            <p>We're excited to announce our expansion into mobile app development!</p>
            
            <p>Thank you for being part of our community!</p>
            <p>Best regards,<br>The Sheba Software Team</p>
            ''',
            'status': 'draft',
            'created_by': admin_user,
            'recipients_count': 0,
            'opened_count': 0,
            'clicked_count': 0
        }

        newsletter, created = Newsletter.objects.get_or_create(
            title=newsletter_data['title'],
            defaults=newsletter_data
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created newsletter: {newsletter.title}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Newsletter already exists: {newsletter.title}')
            )

        # Create sample notifications
        notifications = [
            {
                'title': 'New Contact Submission',
                'message': 'You have a new contact form submission from Alice Johnson.',
                'notification_type': 'info',
                'recipient': admin_user,
                'is_read': False,
                'action_url': '/admin/communication/contactsubmission/'
            },
            {
                'title': 'Project Deadline Approaching',
                'message': 'The TechStartup Inc. project deadline is in 3 days.',
                'notification_type': 'warning',
                'recipient': admin_user,
                'is_read': False,
                'action_url': '/admin/projects/project/'
            },
            {
                'title': 'Newsletter Sent Successfully',
                'message': 'Monthly newsletter has been sent to 150 subscribers.',
                'notification_type': 'success',
                'recipient': admin_user,
                'is_read': True,
                'action_url': '/admin/communication/newsletter/'
            }
        ]

        for notification_data in notifications:
            notification, created = Notification.objects.get_or_create(
                title=notification_data['title'],
                recipient=notification_data['recipient'],
                defaults=notification_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created notification: {notification.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Notification already exists: {notification.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated communication data!')
        )
