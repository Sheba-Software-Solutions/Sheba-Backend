from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from content.models import WebsiteContent, BlogPost, PortfolioProject, Service, TeamMember
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate sample content data for testing'

    def handle(self, *args, **options):
        # Get admin user for assignments
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Admin user not found. Please create an admin user first.')
            )
            return

        # Create sample website content
        website_content_data = [
            {
                'section': 'hero',
                'title': 'Welcome to Sheba Software',
                'content': 'We build innovative software solutions that transform businesses and drive growth.',
                'is_active': True
            },
            {
                'section': 'about',
                'title': 'About Our Company',
                'content': 'Sheba Software is a leading technology company specializing in custom software development, web applications, and digital transformation solutions.',
                'is_active': True
            },
            {
                'section': 'services',
                'title': 'Our Services',
                'content': 'We offer comprehensive software development services including web development, mobile apps, cloud solutions, and consulting.',
                'is_active': True
            },
            {
                'section': 'contact',
                'title': 'Get In Touch',
                'content': 'Ready to start your next project? Contact us today for a free consultation.',
                'is_active': True
            }
        ]

        for content_data in website_content_data:
            content, created = WebsiteContent.objects.get_or_create(
                section=content_data['section'],
                defaults=content_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created website content: {content.section}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Website content already exists: {content.section}')
                )

        # Create sample blog posts
        blog_posts_data = [
            {
                'title': 'The Future of Web Development in 2024',
                'slug': 'future-web-development-2024',
                'content': '''
                <h2>Introduction</h2>
                <p>Web development continues to evolve rapidly, with new technologies and frameworks emerging constantly.</p>
                
                <h3>Key Trends</h3>
                <ul>
                    <li>Progressive Web Applications (PWAs)</li>
                    <li>Serverless Architecture</li>
                    <li>AI-Powered Development Tools</li>
                    <li>WebAssembly Integration</li>
                </ul>
                
                <p>These trends are shaping how we build modern web applications.</p>
                ''',
                'excerpt': 'Explore the latest trends and technologies shaping web development in 2024.',
                'author': admin_user,
                'category': 'technology',
                'status': 'published',
                'published_at': date.today() - timedelta(days=5),
                'featured_image': ''
            },
            {
                'title': 'Building Scalable APIs with Django REST Framework',
                'slug': 'scalable-apis-django-rest-framework',
                'content': '''
                <h2>Why Django REST Framework?</h2>
                <p>Django REST Framework (DRF) provides powerful tools for building robust APIs.</p>
                
                <h3>Best Practices</h3>
                <ol>
                    <li>Use proper serializers for data validation</li>
                    <li>Implement pagination for large datasets</li>
                    <li>Add proper authentication and permissions</li>
                    <li>Use filtering and searching capabilities</li>
                </ol>
                
                <p>Following these practices ensures your API is production-ready.</p>
                ''',
                'excerpt': 'Learn how to build scalable and maintainable APIs using Django REST Framework.',
                'author': admin_user,
                'category': 'development',
                'status': 'published',
                'published_at': date.today() - timedelta(days=12),
                'featured_image': ''
            },
            {
                'title': 'React vs Vue.js: Choosing the Right Frontend Framework',
                'slug': 'react-vs-vue-frontend-framework',
                'content': '''
                <h2>Framework Comparison</h2>
                <p>Both React and Vue.js are excellent choices for modern web development.</p>
                
                <h3>React Advantages</h3>
                <ul>
                    <li>Large ecosystem and community</li>
                    <li>Strong corporate backing (Meta)</li>
                    <li>Excellent job market</li>
                </ul>
                
                <h3>Vue.js Advantages</h3>
                <ul>
                    <li>Gentle learning curve</li>
                    <li>Excellent documentation</li>
                    <li>Great developer experience</li>
                </ul>
                ''',
                'excerpt': 'Compare React and Vue.js to make the right choice for your next project.',
                'author': admin_user,
                'category': 'development',
                'status': 'draft',
                'published_at': None,
                'featured_image': ''
            }
        ]

        for post_data in blog_posts_data:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created blog post: {post.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Blog post already exists: {post.title}')
                )

        # Create sample portfolio projects
        portfolio_projects_data = [
            {
                'title': 'E-commerce Platform',
                'description': 'A comprehensive e-commerce solution with advanced features including inventory management, payment processing, and analytics dashboard.',
                'category': 'Web Development',
                'technologies': ['React', 'Node.js', 'MongoDB', 'Stripe'],
                'project_url': 'https://techmart-demo.com',
                'github_url': 'https://github.com/sheba/ecommerce-platform',
                'status': 'featured',
                'order': 1
            },
            {
                'title': 'Healthcare Management System',
                'description': 'Digital healthcare platform for patient management, appointment scheduling, and medical records.',
                'category': 'Web Application',
                'technologies': ['Django', 'PostgreSQL', 'Vue.js', 'Docker'],
                'project_url': 'https://medcare-demo.com',
                'github_url': '',
                'status': 'featured',
                'order': 2
            },
            {
                'title': 'Mobile Banking App',
                'description': 'Secure mobile banking application with biometric authentication and real-time transaction monitoring.',
                'category': 'Mobile App',
                'technologies': ['React Native', 'Firebase', 'Node.js'],
                'project_url': '',
                'github_url': '',
                'status': 'active',
                'order': 3
            }
        ]

        for project_data in portfolio_projects_data:
            project, created = PortfolioProject.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created portfolio project: {project.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Portfolio project already exists: {project.title}')
                )

        # Create sample services
        services_data = [
            {
                'title': 'Custom Web Development',
                'description': 'Full-stack web development services using modern technologies and frameworks.',
                'features': ['Responsive Design', 'SEO Optimization', 'Performance Optimization', 'Security Implementation'],
                'price': '$5,000 - $15,000',
                'icon': 'web',
                'status': 'active',
                'order': 1
            },
            {
                'title': 'Mobile App Development',
                'description': 'Native and cross-platform mobile application development for iOS and Android.',
                'features': ['Cross-platform', 'Native Performance', 'App Store Deployment', 'Maintenance Support'],
                'price': '$8,000 - $25,000',
                'icon': 'mobile',
                'status': 'active',
                'order': 2
            },
            {
                'title': 'API Development & Integration',
                'description': 'RESTful API development and third-party service integration.',
                'features': ['RESTful APIs', 'Authentication', 'Documentation', 'Testing'],
                'price': '$3,000 - $8,000',
                'icon': 'api',
                'status': 'active',
                'order': 3
            },
            {
                'title': 'Technical Consulting',
                'description': 'Expert technical consultation for architecture and technology decisions.',
                'features': ['Architecture Review', 'Technology Selection', 'Best Practices', 'Code Review'],
                'price': '$150/hour',
                'icon': 'consulting',
                'status': 'active',
                'order': 4
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created service: {service.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Service already exists: {service.title}')
                )

        # Create sample team members
        team_members_data = [
            {
                'name': 'Ahmed Hassan',
                'role': 'Senior Full-Stack Developer',
                'bio': 'Ahmed is a seasoned developer with 8+ years of experience in web and mobile development. He specializes in React, Node.js, and cloud technologies.',
                'email': 'ahmed@shebasoftware.com',
                'linkedin_url': 'https://linkedin.com/in/ahmed-hassan',
                'github_url': 'https://github.com/ahmed-hassan',
                'status': 'active',
                'order': 1
            },
            {
                'name': 'Sarah Johnson',
                'role': 'UI/UX Designer',
                'bio': 'Sarah is a creative designer passionate about creating intuitive and beautiful user experiences. She has worked with startups and Fortune 500 companies.',
                'email': 'sarah@shebasoftware.com',
                'linkedin_url': 'https://linkedin.com/in/sarah-johnson',
                'github_url': '',
                'status': 'active',
                'order': 2
            },
            {
                'name': 'Michael Chen',
                'role': 'DevOps Engineer',
                'bio': 'Michael ensures our applications run smoothly in production. He specializes in cloud infrastructure, CI/CD, and monitoring.',
                'email': 'michael@shebasoftware.com',
                'linkedin_url': 'https://linkedin.com/in/michael-chen',
                'github_url': 'https://github.com/michael-chen',
                'status': 'active',
                'order': 3
            }
        ]

        for member_data in team_members_data:
            member, created = TeamMember.objects.get_or_create(
                email=member_data['email'],
                defaults=member_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created team member: {member.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Team member already exists: {member.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated content data!')
        )
