from django.core.management.base import BaseCommand
from clients.models import Client, ClientContact

class Command(BaseCommand):
    help = 'Populate sample client data for testing'

    def handle(self, *args, **options):
        # Create sample clients
        clients_data = [
            {
                'name': 'John Smith',
                'email': 'john@techstartup.com',
                'phone': '+1-555-0101',
                'company': 'TechStartup Inc.',
                'website': 'https://techstartup.com',
                'address': '123 Innovation Drive, Silicon Valley, CA 94025',
                'client_type': 'business',
                'contact_person': 'John Smith',
                'notes': 'Interested in web development and mobile app solutions.',
                'is_active': True
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@gmail.com',
                'phone': '+1-555-0202',
                'company': '',
                'website': '',
                'address': '456 Main Street, New York, NY 10001',
                'client_type': 'individual',
                'contact_person': 'Sarah Johnson',
                'notes': 'Freelance photographer looking for portfolio website.',
                'is_active': True
            },
            {
                'name': 'Michael Chen',
                'email': 'mike@retailplus.com',
                'phone': '+1-555-0303',
                'company': 'RetailPlus Solutions',
                'website': 'https://retailplus.com',
                'address': '789 Commerce Blvd, Chicago, IL 60601',
                'client_type': 'business',
                'contact_person': 'Michael Chen',
                'notes': 'E-commerce platform development and integration services.',
                'is_active': True
            },
            {
                'name': 'Emily Davis',
                'email': 'emily@healthcaretech.org',
                'phone': '+1-555-0404',
                'company': 'HealthCare Tech',
                'website': 'https://healthcaretech.org',
                'address': '321 Medical Center Dr, Boston, MA 02101',
                'client_type': 'business',
                'contact_person': 'Emily Davis',
                'notes': 'Healthcare management system with HIPAA compliance requirements.',
                'is_active': True
            },
            {
                'name': 'Robert Wilson',
                'email': 'robert.wilson@email.com',
                'phone': '+1-555-0505',
                'company': '',
                'website': 'https://robertwilsonart.com',
                'address': '654 Artist Lane, Austin, TX 78701',
                'client_type': 'individual',
                'contact_person': 'Robert Wilson',
                'notes': 'Artist looking for online gallery and e-commerce functionality.',
                'is_active': False
            }
        ]

        for client_data in clients_data:
            client, created = Client.objects.get_or_create(
                email=client_data['email'],
                defaults=client_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created client: {client.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Client already exists: {client.name}')
                )

        # Create sample client contacts
        contacts_data = [
            {
                'client_email': 'john@techstartup.com',
                'name': 'Jane Smith',
                'email': 'jane@techstartup.com',
                'phone': '+1-555-0111',
                'position': 'CTO',
                'is_primary': False
            },
            {
                'client_email': 'mike@retailplus.com',
                'name': 'Lisa Wang',
                'email': 'lisa@retailplus.com',
                'phone': '+1-555-0333',
                'position': 'Project Manager',
                'is_primary': False
            },
            {
                'client_email': 'emily@healthcaretech.org',
                'name': 'Dr. James Brown',
                'email': 'james@healthcaretech.org',
                'phone': '+1-555-0444',
                'position': 'Medical Director',
                'is_primary': False
            }
        ]

        for contact_data in contacts_data:
            try:
                client = Client.objects.get(email=contact_data['client_email'])
                contact_data.pop('client_email')
                contact, created = ClientContact.objects.get_or_create(
                    client=client,
                    email=contact_data['email'],
                    defaults=contact_data
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created contact: {contact.name} for {client.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Contact already exists: {contact.name}')
                    )
            except Client.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Client not found for email: {contact_data["client_email"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated client data!')
        )
