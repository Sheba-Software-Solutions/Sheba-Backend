#!/usr/bin/env python3
"""
Test script for Clients API endpoints
Run this after starting the Django server to test client functionality
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_client_endpoints():
    print("🧪 Testing Clients API Endpoints")
    print("=" * 50)
    
    # First, create a user and get auth token
    print("\n1. Creating test user and getting auth token...")
    
    # Create user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'admin'
    }
    
    try:
        # Try to login first (user might already exist)
        login_response = requests.post(f'{BASE_URL}/auth/login/', {
            'username': 'admin',
            'password': 'admin123'  # Updated superuser password
        })
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print("✅ Logged in with admin user")
        else:
            print("❌ Login failed, creating new user...")
            return
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test 2: Get all clients
    print("\n2. Testing GET /api/clients/ - List all clients")
    try:
        response = requests.get(f'{BASE_URL}/clients/', headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            clients = response.json()
            print(f"✅ Found {len(clients['results']) if 'results' in clients else len(clients)} clients")
            if clients:
                first_client = clients['results'][0] if 'results' in clients else clients[0]
                print(f"   First client: {first_client['name']} ({first_client['email']})")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get client statistics
    print("\n3. Testing GET /api/clients/stats/ - Client statistics")
    try:
        response = requests.get(f'{BASE_URL}/clients/stats/', headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Client statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Create a new client
    print("\n4. Testing POST /api/clients/ - Create new client")
    new_client_data = {
        'name': 'Test Client API',
        'email': 'testclient@api.com',
        'phone': '+1-555-9999',
        'company': 'API Test Company',
        'website': 'https://apitest.com',
        'address': '123 API Street, Test City, TC 12345',
        'client_type': 'small_business',
        'contact_person': 'Test Client API',
        'notes': 'Created via API test script',
        'is_active': True
    }
    
    try:
        response = requests.post(f'{BASE_URL}/clients/', 
                               json=new_client_data, 
                               headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            client = response.json()
            client_id = client['id']
            print(f"✅ Created client: {client['name']} (ID: {client_id})")
            
            # Test 5: Get specific client
            print(f"\n5. Testing GET /api/clients/{client_id}/ - Get specific client")
            response = requests.get(f'{BASE_URL}/clients/{client_id}/', headers=headers)
            if response.status_code == 200:
                client_detail = response.json()
                print(f"✅ Retrieved client: {client_detail['name']}")
                print(f"   Company: {client_detail['company']}")
                print(f"   Type: {client_detail['client_type']}")
            else:
                print(f"❌ Error getting client: {response.text}")
            
            # Test 6: Update client
            print(f"\n6. Testing PUT /api/clients/{client_id}/ - Update client")
            update_data = new_client_data.copy()
            update_data['notes'] = 'Updated via API test script'
            update_data['company'] = 'Updated API Test Company'
            
            response = requests.put(f'{BASE_URL}/clients/{client_id}/', 
                                  json=update_data, 
                                  headers=headers)
            if response.status_code == 200:
                updated_client = response.json()
                print(f"✅ Updated client: {updated_client['company']}")
            else:
                print(f"❌ Error updating client: {response.text}")
            
            # Test 7: Create client contact
            print(f"\n7. Testing POST /api/clients/{client_id}/contacts/ - Create client contact")
            contact_data = {
                'name': 'John Doe',
                'email': 'john@apitest.com',
                'phone': '+1-555-8888',
                'position': 'Technical Lead',
                'is_primary': True
            }
            
            response = requests.post(f'{BASE_URL}/clients/{client_id}/contacts/', 
                                   json=contact_data, 
                                   headers=headers)
            if response.status_code == 201:
                contact = response.json()
                print(f"✅ Created contact: {contact['name']} ({contact['position']})")
            else:
                print(f"❌ Error creating contact: {response.text}")
            
            # Test 8: Delete client (cleanup)
            print(f"\n8. Testing DELETE /api/clients/{client_id}/ - Delete client")
            response = requests.delete(f'{BASE_URL}/clients/{client_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Client deleted successfully")
            else:
                print(f"❌ Error deleting client: {response.text}")
                
        else:
            print(f"❌ Error creating client: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Client API testing completed!")

if __name__ == '__main__':
    test_client_endpoints()
