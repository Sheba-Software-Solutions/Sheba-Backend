#!/usr/bin/env python3
"""
Test script for Projects API endpoints
Run this after starting the Django server to test projects functionality
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = 'http://127.0.0.1:8000/api'

def test_projects_endpoints():
    print("🧪 Testing Projects API Endpoints")
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
    
    # Test Projects
    print("\n2. Testing Projects")
    print("-" * 30)
    
    # Get all projects
    try:
        response = requests.get(f'{BASE_URL}/projects/', headers=headers)
        print(f"GET /projects/ - Status: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            count = len(projects['results']) if 'results' in projects else len(projects)
            print(f"✅ Found {count} projects")
            
            # Get first project for testing
            if count > 0:
                first_project = projects['results'][0] if 'results' in projects else projects[0]
                project_id = first_project['id']
                print(f"   First project: {first_project['name']} (ID: {project_id})")
        else:
            print(f"❌ Error: {response.text}")
            project_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        project_id = None
    
    # Get clients for project creation
    try:
        clients_response = requests.get(f'{BASE_URL}/clients/', headers=headers)
        if clients_response.status_code == 200:
            clients = clients_response.json()
            client_id = clients['results'][0]['id'] if clients['results'] else None
        else:
            client_id = None
    except:
        client_id = None
    
    # Create new project
    if client_id:
        new_project = {
            'name': 'Test Project API',
            'description': 'This is a test project created via API for testing purposes.',
            'client_id': client_id,
            'status': 'planning',
            'priority': 'medium',
            'start_date': str(date.today()),
            'end_date': str(date.today() + timedelta(days=90)),
            'budget': 15000.00,
            'progress': 0,
            'technologies': ['Python', 'Django', 'React'],
            'repository_url': 'https://github.com/test/test-project',
            'live_url': ''
        }
        
        try:
            response = requests.post(f'{BASE_URL}/projects/', 
                                   json=new_project, headers=headers)
            print(f"POST /projects/ - Status: {response.status_code}")
            if response.status_code == 201:
                project = response.json()
                test_project_id = project['id']
                print(f"✅ Created project: {project['name']} (ID: {test_project_id})")
            else:
                print(f"❌ Error creating project: {response.text}")
                test_project_id = None
        except Exception as e:
            print(f"❌ Error: {e}")
            test_project_id = None
    else:
        print("⚠️ No clients found, skipping project creation")
        test_project_id = None
    
    # Test project detail
    if project_id:
        try:
            response = requests.get(f'{BASE_URL}/projects/{project_id}/', headers=headers)
            print(f"GET /projects/{project_id}/ - Status: {response.status_code}")
            if response.status_code == 200:
                project = response.json()
                print(f"✅ Retrieved project details: {project['name']}")
            else:
                print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test Projects Summary
    print("\n3. Testing Projects Summary")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/projects/summary/', headers=headers)
        print(f"GET /projects/summary/ - Status: {response.status_code}")
        if response.status_code == 200:
            summary = response.json()
            count = len(summary) if isinstance(summary, list) else 1
            print(f"✅ Found {count} project summaries")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Projects Statistics
    print("\n4. Testing Projects Statistics")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/projects/stats/', headers=headers)
        print(f"GET /projects/stats/ - Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Project statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Project Tasks
    print("\n5. Testing Project Tasks")
    print("-" * 30)
    
    # Get all tasks
    try:
        response = requests.get(f'{BASE_URL}/projects/tasks/', headers=headers)
        print(f"GET /projects/tasks/ - Status: {response.status_code}")
        if response.status_code == 200:
            tasks = response.json()
            count = len(tasks['results']) if 'results' in tasks else len(tasks)
            print(f"✅ Found {count} project tasks")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new task
    if test_project_id:
        new_task = {
            'project_id': test_project_id,
            'title': 'Test Task API',
            'description': 'This is a test task created via API.',
            'status': 'todo',
            'due_date': str(date.today() + timedelta(days=7)),
            'estimated_hours': 8.0,
            'actual_hours': 0.0
        }
        
        try:
            response = requests.post(f'{BASE_URL}/projects/tasks/', 
                                   json=new_task, headers=headers)
            print(f"POST /projects/tasks/ - Status: {response.status_code}")
            if response.status_code == 201:
                task = response.json()
                task_id = task['id']
                print(f"✅ Created task: {task['title']} (ID: {task_id})")
            else:
                print(f"❌ Error creating task: {response.text}")
                task_id = None
        except Exception as e:
            print(f"❌ Error: {e}")
            task_id = None
    else:
        task_id = None
    
    # Update project progress
    if test_project_id:
        print("\n6. Testing Project Update")
        print("-" * 30)
        
        update_data = {
            'progress': 25,
            'status': 'in_progress'
        }
        
        try:
            response = requests.patch(f'{BASE_URL}/projects/{test_project_id}/', 
                                    json=update_data, headers=headers)
            print(f"PATCH /projects/{test_project_id}/ - Status: {response.status_code}")
            if response.status_code == 200:
                project = response.json()
                print(f"✅ Updated project progress to {project['progress']}%")
            else:
                print(f"❌ Error updating project: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Update task status
    if task_id:
        update_task_data = {
            'status': 'in_progress',
            'actual_hours': 2.5
        }
        
        try:
            response = requests.patch(f'{BASE_URL}/projects/tasks/{task_id}/', 
                                    json=update_task_data, headers=headers)
            print(f"PATCH /projects/tasks/{task_id}/ - Status: {response.status_code}")
            if response.status_code == 200:
                task = response.json()
                print(f"✅ Updated task status to {task['status']}")
            else:
                print(f"❌ Error updating task: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Cleanup - Delete test data
    print("\n7. Cleanup - Deleting test data")
    print("-" * 30)
    
    # Delete test task
    if task_id:
        try:
            response = requests.delete(f'{BASE_URL}/projects/tasks/{task_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test task")
            else:
                print(f"❌ Error deleting task: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Delete test project
    if test_project_id:
        try:
            response = requests.delete(f'{BASE_URL}/projects/{test_project_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test project")
            else:
                print(f"❌ Error deleting project: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Projects API testing completed!")

if __name__ == '__main__':
    test_projects_endpoints()
