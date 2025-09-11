#!/usr/bin/env python3
"""
Test script for Dashboard API endpoints
Run this after starting the Django server to test dashboard functionality
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_dashboard_endpoints():
    print("🧪 Testing Dashboard API Endpoints")
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
    
    # Test Dashboard Metrics
    print("\n2. Testing Dashboard Metrics")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/dashboard/metrics/', headers=headers)
        print(f"GET /dashboard/metrics/ - Status: {response.status_code}")
        if response.status_code == 200:
            metrics = response.json()
            count = len(metrics['results']) if 'results' in metrics else len(metrics)
            print(f"✅ Found {count} dashboard metrics")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Activity Logs
    print("\n3. Testing Activity Logs")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/dashboard/activities/', headers=headers)
        print(f"GET /dashboard/activities/ - Status: {response.status_code}")
        if response.status_code == 200:
            activities = response.json()
            count = len(activities['results']) if 'results' in activities else len(activities)
            print(f"✅ Found {count} activity logs")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Dashboard Overview
    print("\n4. Testing Dashboard Overview")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/dashboard/overview/', headers=headers)
        print(f"GET /dashboard/overview/ - Status: {response.status_code}")
        if response.status_code == 200:
            overview = response.json()
            print("✅ Dashboard overview data:")
            for key, value in overview.items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Metrics Chart Data
    print("\n5. Testing Metrics Chart Data")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/dashboard/metrics/chart/', headers=headers)
        print(f"GET /dashboard/metrics/chart/ - Status: {response.status_code}")
        if response.status_code == 200:
            chart_data = response.json()
            print("✅ Metrics chart data retrieved")
            if isinstance(chart_data, list):
                print(f"   Found {len(chart_data)} chart data points")
            else:
                print(f"   Chart data keys: {list(chart_data.keys())}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Recent Activities
    print("\n6. Testing Recent Activities")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/dashboard/activities/recent/', headers=headers)
        print(f"GET /dashboard/activities/recent/ - Status: {response.status_code}")
        if response.status_code == 200:
            recent = response.json()
            count = len(recent) if isinstance(recent, list) else len(recent.get('results', []))
            print(f"✅ Found {count} recent activities")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new dashboard metric
    print("\n7. Testing Metric Creation")
    print("-" * 30)
    
    from datetime import date
    new_metric = {
        'metric_type': 'website_visitors',
        'value': 2500.0,
        'date': str(date.today())
    }
    
    try:
        response = requests.post(f'{BASE_URL}/dashboard/metrics/', 
                               json=new_metric, headers=headers)
        print(f"POST /dashboard/metrics/ - Status: {response.status_code}")
        if response.status_code == 201:
            metric = response.json()
            metric_id = metric['id']
            print(f"✅ Created metric: {metric['metric_type']} (ID: {metric_id})")
        else:
            print(f"❌ Error creating metric: {response.text}")
            metric_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        metric_id = None
    
    # Create new activity log
    print("\n8. Testing Activity Log Creation")
    print("-" * 30)
    
    new_activity = {
        'action': 'view',
        'model_name': 'Dashboard',
        'object_id': 1,
        'description': 'Viewed dashboard overview via API test',
        'ip_address': '127.0.0.1',
        'user_agent': 'Test Script'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/dashboard/activities/', 
                               json=new_activity, headers=headers)
        print(f"POST /dashboard/activities/ - Status: {response.status_code}")
        if response.status_code == 201:
            activity = response.json()
            activity_id = activity['id']
            print(f"✅ Created activity log: {activity['description']} (ID: {activity_id})")
        else:
            print(f"❌ Error creating activity: {response.text}")
            activity_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        activity_id = None
    
    # Cleanup - Delete test data
    print("\n9. Cleanup - Deleting test data")
    print("-" * 30)
    
    # Delete test metric
    if metric_id:
        try:
            response = requests.delete(f'{BASE_URL}/dashboard/metrics/{metric_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test metric")
            else:
                print(f"❌ Error deleting metric: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Delete test activity
    if activity_id:
        try:
            response = requests.delete(f'{BASE_URL}/dashboard/activities/{activity_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test activity log")
            else:
                print(f"❌ Error deleting activity: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Dashboard API testing completed!")

if __name__ == '__main__':
    test_dashboard_endpoints()
