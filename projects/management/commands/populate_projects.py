from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clients.models import Client
from projects.models import Project, ProjectTask
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate sample projects and tasks data for testing'

    def handle(self, *args, **options):
        # Get admin user and clients
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Admin user not found. Please create an admin user first.')
            )
            return

        # Get some clients for projects
        clients = Client.objects.all()
        if not clients:
            self.stdout.write(
                self.style.ERROR('No clients found. Please create clients first.')
            )
            return

        # Create sample projects
        projects_data = [
            {
                'name': 'E-commerce Website Development',
                'description': 'Complete e-commerce platform with payment integration, inventory management, and admin dashboard.',
                'client': clients[0] if len(clients) > 0 else None,
                'status': 'in_progress',
                'priority': 'high',
                'start_date': date.today() - timedelta(days=30),
                'end_date': date.today() + timedelta(days=60),
                'budget': 25000.00,
                'progress': 65,
                'technologies': ['React', 'Node.js', 'MongoDB', 'Stripe API'],
                'repository_url': 'https://github.com/sheba/ecommerce-project',
                'live_url': 'https://staging.ecommerce-demo.com'
            },
            {
                'name': 'Mobile App for Healthcare',
                'description': 'Cross-platform mobile application for patient management and appointment scheduling.',
                'client': clients[1] if len(clients) > 1 else clients[0],
                'status': 'planning',
                'priority': 'medium',
                'start_date': date.today() + timedelta(days=15),
                'end_date': date.today() + timedelta(days=120),
                'budget': 35000.00,
                'progress': 10,
                'technologies': ['React Native', 'Firebase', 'Node.js'],
                'repository_url': 'https://github.com/sheba/healthcare-app',
                'live_url': ''
            },
            {
                'name': 'Corporate Website Redesign',
                'description': 'Modern responsive website with CMS integration and SEO optimization.',
                'client': clients[2] if len(clients) > 2 else clients[0],
                'status': 'completed',
                'priority': 'low',
                'start_date': date.today() - timedelta(days=90),
                'end_date': date.today() - timedelta(days=10),
                'budget': 8000.00,
                'progress': 100,
                'technologies': ['WordPress', 'PHP', 'MySQL', 'Bootstrap'],
                'repository_url': 'https://github.com/sheba/corporate-website',
                'live_url': 'https://corporate-demo.com'
            },
            {
                'name': 'Inventory Management System',
                'description': 'Web-based inventory tracking system with barcode scanning and reporting.',
                'client': clients[0] if len(clients) > 0 else None,
                'status': 'testing',
                'priority': 'high',
                'start_date': date.today() - timedelta(days=45),
                'end_date': date.today() + timedelta(days=15),
                'budget': 18000.00,
                'progress': 85,
                'technologies': ['Django', 'PostgreSQL', 'Vue.js', 'Docker'],
                'repository_url': 'https://github.com/sheba/inventory-system',
                'live_url': 'https://inventory-demo.com'
            }
        ]

        created_projects = []
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                defaults=project_data
            )
            if created:
                # Add admin user to assigned users
                project.assigned_to.add(admin_user)
                created_projects.append(project)
                self.stdout.write(
                    self.style.SUCCESS(f'Created project: {project.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Project already exists: {project.name}')
                )

        # Create sample tasks for projects
        if created_projects:
            tasks_data = [
                # Tasks for E-commerce Website
                {
                    'project': created_projects[0] if len(created_projects) > 0 else None,
                    'title': 'Setup Database Schema',
                    'description': 'Design and implement database schema for products, users, and orders.',
                    'status': 'completed',
                    'assigned_to': admin_user,
                    'due_date': date.today() - timedelta(days=20),
                    'estimated_hours': 16,
                    'actual_hours': 18
                },
                {
                    'project': created_projects[0] if len(created_projects) > 0 else None,
                    'title': 'Implement Payment Gateway',
                    'description': 'Integrate Stripe payment processing for secure transactions.',
                    'status': 'in_progress',
                    'assigned_to': admin_user,
                    'due_date': date.today() + timedelta(days=7),
                    'estimated_hours': 24,
                    'actual_hours': 12
                },
                {
                    'project': created_projects[0] if len(created_projects) > 0 else None,
                    'title': 'Admin Dashboard Development',
                    'description': 'Create comprehensive admin panel for managing products and orders.',
                    'status': 'todo',
                    'assigned_to': admin_user,
                    'due_date': date.today() + timedelta(days=14),
                    'estimated_hours': 32,
                    'actual_hours': 0
                },
                # Tasks for Mobile App
                {
                    'project': created_projects[1] if len(created_projects) > 1 else None,
                    'title': 'UI/UX Design Review',
                    'description': 'Review and finalize mobile app design mockups.',
                    'status': 'in_progress',
                    'assigned_to': admin_user,
                    'due_date': date.today() + timedelta(days=5),
                    'estimated_hours': 8,
                    'actual_hours': 4
                },
                {
                    'project': created_projects[1] if len(created_projects) > 1 else None,
                    'title': 'API Development',
                    'description': 'Develop REST API for mobile app backend.',
                    'status': 'todo',
                    'assigned_to': admin_user,
                    'due_date': date.today() + timedelta(days=21),
                    'estimated_hours': 40,
                    'actual_hours': 0
                }
            ]

            for task_data in tasks_data:
                if task_data['project']:
                    task, created = ProjectTask.objects.get_or_create(
                        title=task_data['title'],
                        project=task_data['project'],
                        defaults=task_data
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Created task: {task.title}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Task already exists: {task.title}')
                        )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated projects and tasks data!')
        )
