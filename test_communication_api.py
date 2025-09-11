#!/usr/bin/env python3
"""
Test script for Communication API endpoints
Run this after starting the Django server to test communication functionality
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_communication_endpoints():
    print("🧪 Testing Communication API Endpoints")
    print("=" * 50)
    
    # Get auth token
    print("\n1. Getting authentication token...")
    try:
        login_response = requests.post(f'{BASE_URL}/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print("✅ Logged in successfully")
        else:
            print("❌ Login failed")
            return
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test Contact Submissions
    print("\n2. Testing Contact Submissions")
    print("-" * 30)
    
    # Get all contact submissions
    try:
        response = requests.get(f'{BASE_URL}/communication/contacts/', headers=headers)
        print(f"GET /contacts/ - Status: {response.status_code}")
        if response.status_code == 200:
            contacts = response.json()
            count = len(contacts['results']) if 'results' in contacts else len(contacts)
            print(f"✅ Found {count} contact submissions")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new contact submission
    new_contact = {
        'name': 'Test Contact API',
        'email': 'testcontact@api.com',
        'phone': '+1-555-9999',
        'subject': 'API Testing Contact',
        'message': 'This is a test contact submission created via API.',
        'status': 'new',
        'ip_address': '127.0.0.1',
        'user_agent': 'Test Script'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/communication/contacts/', 
                               json=new_contact, headers=headers)
        print(f"POST /contacts/ - Status: {response.status_code}")
        if response.status_code == 201:
            contact = response.json()
            contact_id = contact['id']
            print(f"✅ Created contact submission: {contact['name']} (ID: {contact_id})")
        else:
            print(f"❌ Error creating contact: {response.text}")
            contact_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        contact_id = None
    
    # Test Email Templates
    print("\n3. Testing Email Templates")
    print("-" * 30)
    
    # Get all email templates
    try:
        response = requests.get(f'{BASE_URL}/communication/email-templates/', headers=headers)
        print(f"GET /email-templates/ - Status: {response.status_code}")
        if response.status_code == 200:
            templates = response.json()
            count = len(templates['results']) if 'results' in templates else len(templates)
            print(f"✅ Found {count} email templates")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new email template
    new_template = {
        'name': 'Test Template API',
        'template_type': 'follow_up',
        'subject': 'Test Email Template',
        'content': '<h2>Test Template</h2><p>This is a test email template created via API.</p>',
        'is_active': True
    }
    
    try:
        response = requests.post(f'{BASE_URL}/communication/email-templates/', 
                               json=new_template, headers=headers)
        print(f"POST /email-templates/ - Status: {response.status_code}")
        if response.status_code == 201:
            template = response.json()
            template_id = template['id']
            print(f"✅ Created email template: {template['name']} (ID: {template_id})")
        else:
            print(f"❌ Error creating template: {response.text}")
            template_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        template_id = None
    
    # Test Newsletter Subscribers
    print("\n4. Testing Newsletter Subscribers")
    print("-" * 30)
    
    # Get all subscribers
    try:
        response = requests.get(f'{BASE_URL}/communication/subscribers/', headers=headers)
        print(f"GET /subscribers/ - Status: {response.status_code}")
        if response.status_code == 200:
            subscribers = response.json()
            count = len(subscribers['results']) if 'results' in subscribers else len(subscribers)
            print(f"✅ Found {count} newsletter subscribers")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new subscriber
    new_subscriber = {
        'email': 'testsubscriber@api.com',
        'name': 'Test Subscriber API',
        'is_active': True
    }
    
    try:
        response = requests.post(f'{BASE_URL}/communication/subscribers/', 
                               json=new_subscriber, headers=headers)
        print(f"POST /subscribers/ - Status: {response.status_code}")
        if response.status_code == 201:
            subscriber = response.json()
            subscriber_id = subscriber['id']
            print(f"✅ Created subscriber: {subscriber['email']} (ID: {subscriber_id})")
        else:
            print(f"❌ Error creating subscriber: {response.text}")
            subscriber_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        subscriber_id = None
    
    # Test Newsletters
    print("\n5. Testing Newsletters")
    print("-" * 30)
    
    # Get all newsletters
    try:
        response = requests.get(f'{BASE_URL}/communication/newsletters/', headers=headers)
        print(f"GET /newsletters/ - Status: {response.status_code}")
        if response.status_code == 200:
            newsletters = response.json()
            count = len(newsletters['results']) if 'results' in newsletters else len(newsletters)
            print(f"✅ Found {count} newsletters")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Notifications
    print("\n6. Testing Notifications")
    print("-" * 30)
    
    # Get all notifications
    try:
        response = requests.get(f'{BASE_URL}/communication/notifications/', headers=headers)
        print(f"GET /notifications/ - Status: {response.status_code}")
        if response.status_code == 200:
            notifications = response.json()
            count = len(notifications['results']) if 'results' in notifications else len(notifications)
            print(f"✅ Found {count} notifications")
            
            # Test mark notification as read
            if count > 0:
                first_notification = notifications['results'][0] if 'results' in notifications else notifications[0]
                notification_id = first_notification['id']
                
                response = requests.post(f'{BASE_URL}/communication/notifications/{notification_id}/mark-read/', 
                                       headers=headers)
                print(f"POST /notifications/{notification_id}/mark-read/ - Status: {response.status_code}")
                if response.status_code == 200:
                    print("✅ Marked notification as read")
                else:
                    print(f"❌ Error marking notification: {response.text}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Communication Statistics
    print("\n7. Testing Communication Statistics")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/communication/stats/', headers=headers)
        print(f"GET /stats/ - Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Communication statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Cleanup - Delete test data
    print("\n8. Cleanup - Deleting test data")
    print("-" * 30)
    
    # Delete test contact
    if contact_id:
        try:
            response = requests.delete(f'{BASE_URL}/communication/contacts/{contact_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test contact submission")
            else:
                print(f"❌ Error deleting contact: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Delete test template
    if template_id:
        try:
            response = requests.delete(f'{BASE_URL}/communication/email-templates/{template_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test email template")
            else:
                print(f"❌ Error deleting template: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Delete test subscriber
    if subscriber_id:
        try:
            response = requests.delete(f'{BASE_URL}/communication/subscribers/{subscriber_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test subscriber")
            else:
                print(f"❌ Error deleting subscriber: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Communication API testing completed!")

if __name__ == '__main__':
    test_communication_endpoints()
