#!/usr/bin/env python3
"""
Comprehensive test script for all Sheba Admin Backend API endpoints
Run this after starting the Django server to test all functionality
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_all_endpoints():
    print("🧪 Testing All Sheba Admin Backend API Endpoints")
    print("=" * 60)
    
    # Get auth token
    print("\n1. Authentication Test")
    print("-" * 30)
    try:
        login_response = requests.post(f'{BASE_URL}/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print("✅ Authentication successful")
        else:
            print("❌ Authentication failed")
            return
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test all endpoint categories
    endpoints_to_test = [
        # Authentication endpoints
        ('Authentication', [
            ('GET', '/auth/profile/', 'User profile'),
            ('GET', '/auth/users/', 'Users list'),
            ('GET', '/auth/sessions/', 'User sessions')
        ]),
        
        # Clients endpoints
        ('Clients', [
            ('GET', '/clients/', 'Clients list'),
            ('GET', '/clients/summary/', 'Clients summary'),
            ('GET', '/clients/stats/', 'Clients statistics'),
            ('GET', '/clients/contacts/', 'Client contacts')
        ]),
        
        # Projects endpoints
        ('Projects', [
            ('GET', '/projects/', 'Projects list'),
            ('GET', '/projects/summary/', 'Projects summary'),
            ('GET', '/projects/stats/', 'Projects statistics'),
            ('GET', '/projects/tasks/', 'Project tasks')
        ]),
        
        # Communication endpoints
        ('Communication', [
            ('GET', '/communication/contacts/', 'Contact submissions'),
            ('GET', '/communication/email-templates/', 'Email templates'),
            ('GET', '/communication/newsletters/', 'Newsletters'),
            ('GET', '/communication/subscribers/', 'Newsletter subscribers'),
            ('GET', '/communication/notifications/', 'Notifications'),
            ('GET', '/communication/stats/', 'Communication statistics')
        ]),
        
        # Content endpoints
        ('Content', [
            ('GET', '/content/website/', 'Website content'),
            ('GET', '/content/blog/', 'Blog posts'),
            ('GET', '/content/portfolio/', 'Portfolio projects'),
            ('GET', '/content/services/', 'Services'),
            ('GET', '/content/team/', 'Team members'),
            ('GET', '/content/stats/', 'Content statistics')
        ]),
        
        # Dashboard endpoints
        ('Dashboard', [
            ('GET', '/dashboard/metrics/', 'Dashboard metrics'),
            ('GET', '/dashboard/activity/', 'Activity logs'),
            ('GET', '/dashboard/overview/', 'Dashboard overview'),
            ('GET', '/dashboard/metrics-chart/', 'Metrics chart'),
            ('GET', '/dashboard/recent-activities/', 'Recent activities')
        ]),
        
        # Settings endpoints
        ('Settings', [
            ('GET', '/settings/company/', 'Company settings'),
            ('GET', '/settings/system/', 'System settings'),
            ('GET', '/settings/permissions/', 'User permissions'),
            ('GET', '/settings/logs/', 'System logs'),
            ('GET', '/settings/health/', 'Health check')
        ])
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for category, endpoints in endpoints_to_test:
        print(f"\n2.{len([c for c, _ in endpoints_to_test if c <= category])} Testing {category}")
        print("-" * 30)
        
        for method, endpoint, description in endpoints:
            total_tests += 1
            try:
                if method == 'GET':
                    response = requests.get(f'{BASE_URL}{endpoint}', headers=headers)
                elif method == 'POST':
                    response = requests.post(f'{BASE_URL}{endpoint}', headers=headers)
                
                if response.status_code in [200, 201]:
                    print(f"✅ {method} {endpoint} - {description}")
                    passed_tests += 1
                elif response.status_code == 404:
                    print(f"⚠️  {method} {endpoint} - {description} (Not Found)")
                else:
                    print(f"❌ {method} {endpoint} - {description} (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"❌ {method} {endpoint} - {description} (Error: {e})")
    
    # Test logout
    print(f"\n3. Logout Test")
    print("-" * 30)
    try:
        logout_response = requests.post(f'{BASE_URL}/auth/logout/', headers=headers)
        if logout_response.status_code == 200:
            print("✅ Logout successful")
            passed_tests += 1
        else:
            print(f"❌ Logout failed (Status: {logout_response.status_code})")
        total_tests += 1
    except Exception as e:
        print(f"❌ Logout error: {e}")
        total_tests += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🎯 Test Summary: {passed_tests}/{total_tests} endpoints working")
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 Excellent! Backend is ready for production")
    elif success_rate >= 75:
        print("👍 Good! Minor issues to address")
    else:
        print("⚠️  Needs attention - several endpoints have issues")

if __name__ == '__main__':
    test_all_endpoints()
