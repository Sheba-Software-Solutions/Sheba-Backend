#!/usr/bin/env python3
"""
Test script for Content API endpoints
Run this after starting the Django server to test content functionality
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_content_endpoints():
    print("🧪 Testing Content API Endpoints")
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
    
    # Test Website Content
    print("\n2. Testing Website Content")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/content/website/', headers=headers)
        print(f"GET /content/website/ - Status: {response.status_code}")
        if response.status_code == 200:
            content = response.json()
            count = len(content['results']) if 'results' in content else len(content)
            print(f"✅ Found {count} website content sections")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Blog Posts
    print("\n3. Testing Blog Posts")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/content/blog/', headers=headers)
        print(f"GET /content/blog/ - Status: {response.status_code}")
        if response.status_code == 200:
            posts = response.json()
            count = len(posts['results']) if 'results' in posts else len(posts)
            print(f"✅ Found {count} blog posts")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new blog post
    new_post = {
        'title': 'Test Blog Post API',
        'slug': 'test-blog-post-api',
        'content': '<h2>Test Content</h2><p>This is a test blog post created via API.</p>',
        'excerpt': 'Test blog post created for API testing purposes.',
        'category': 'technology',
        'status': 'draft'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/content/blog/', 
                               json=new_post, headers=headers)
        print(f"POST /content/blog/ - Status: {response.status_code}")
        if response.status_code == 201:
            post = response.json()
            post_id = post['id']
            print(f"✅ Created blog post: {post['title']} (ID: {post_id})")
        else:
            print(f"❌ Error creating blog post: {response.text}")
            post_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        post_id = None
    
    # Test Portfolio Projects
    print("\n4. Testing Portfolio Projects")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/content/portfolio/', headers=headers)
        print(f"GET /content/portfolio/ - Status: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            count = len(projects['results']) if 'results' in projects else len(projects)
            print(f"✅ Found {count} portfolio projects")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new portfolio project
    new_portfolio = {
        'title': 'Test Portfolio Project API',
        'description': 'This is a test portfolio project created via API.',
        'category': 'Web Development',
        'technologies': ['Python', 'Django', 'React'],
        'project_url': 'https://test-project.com',
        'github_url': 'https://github.com/test/project',
        'status': 'active',
        'order': 99
    }
    
    try:
        response = requests.post(f'{BASE_URL}/content/portfolio/', 
                               json=new_portfolio, headers=headers)
        print(f"POST /content/portfolio/ - Status: {response.status_code}")
        if response.status_code == 201:
            project = response.json()
            portfolio_id = project['id']
            print(f"✅ Created portfolio project: {project['title']} (ID: {portfolio_id})")
        else:
            print(f"❌ Error creating portfolio project: {response.text}")
            portfolio_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        portfolio_id = None
    
    # Test Services
    print("\n5. Testing Services")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/content/services/', headers=headers)
        print(f"GET /content/services/ - Status: {response.status_code}")
        if response.status_code == 200:
            services = response.json()
            count = len(services['results']) if 'results' in services else len(services)
            print(f"✅ Found {count} services")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Team Members
    print("\n6. Testing Team Members")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/content/team/', headers=headers)
        print(f"GET /content/team/ - Status: {response.status_code}")
        if response.status_code == 200:
            team = response.json()
            count = len(team['results']) if 'results' in team else len(team)
            print(f"✅ Found {count} team members")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Create new team member
    new_member = {
        'name': 'Test Member API',
        'role': 'Test Developer',
        'bio': 'This is a test team member created via API.',
        'email': 'test@shebasoftware.com',
        'status': 'active',
        'order': 99
    }
    
    try:
        response = requests.post(f'{BASE_URL}/content/team/', 
                               json=new_member, headers=headers)
        print(f"POST /content/team/ - Status: {response.status_code}")
        if response.status_code == 201:
            member = response.json()
            member_id = member['id']
            print(f"✅ Created team member: {member['name']} (ID: {member_id})")
        else:
            print(f"❌ Error creating team member: {response.text}")
            member_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        member_id = None
    
    # Test Content Statistics
    print("\n7. Testing Content Statistics")
    print("-" * 30)
    
    try:
        response = requests.get(f'{BASE_URL}/content/stats/', headers=headers)
        print(f"GET /content/stats/ - Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Content statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Cleanup - Delete test data
    print("\n8. Cleanup - Deleting test data")
    print("-" * 30)
    
    # Delete test blog post
    if post_id:
        try:
            response = requests.delete(f'{BASE_URL}/content/blog/{post_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test blog post")
            else:
                print(f"❌ Error deleting blog post: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Delete test portfolio project
    if portfolio_id:
        try:
            response = requests.delete(f'{BASE_URL}/content/portfolio/{portfolio_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test portfolio project")
            else:
                print(f"❌ Error deleting portfolio project: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Delete test team member
    if member_id:
        try:
            response = requests.delete(f'{BASE_URL}/content/team/{member_id}/', headers=headers)
            if response.status_code == 204:
                print("✅ Deleted test team member")
            else:
                print(f"❌ Error deleting team member: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Content API testing completed!")

if __name__ == '__main__':
    test_content_endpoints()
