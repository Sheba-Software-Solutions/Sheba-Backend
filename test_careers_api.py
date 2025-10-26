#!/usr/bin/env python3
"""
Test script for Careers API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_careers_api():
    print("🧪 Testing Careers API...")
    
    # Test 1: Login to get auth token
    print("\n1. Testing login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"✅ Login successful, token: {token[:20]}...")
            headers = {"Authorization": f"Token {token}"}
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 2: Create a job posting
    print("\n2. Testing job creation...")
    job_data = {
        "title": "Test Software Developer",
        "slug": "test-software-developer-123",
        "department": "engineering",
        "location": "Addis Ababa, Ethiopia",
        "job_type": "full_time",
        "experience_level": "mid",
        "description": "We are looking for a talented software developer to join our team.",
        "requirements": ["Python", "Django", "React", "3+ years experience"],
        "responsibilities": ["Develop web applications", "Write clean code", "Collaborate with team"],
        "benefits": ["Health insurance", "Flexible hours", "Learning budget"],
        "salary_display": "Competitive",
        "status": "published",
        "application_email": "careers@sheba.et"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/careers/jobs/", json=job_data, headers=headers)
        if response.status_code == 201:
            job = response.json()
            print(f"✅ Job created successfully: {job['title']} (ID: {job['id']})")
            job_id = job['id']
        else:
            print(f"❌ Job creation failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Job creation error: {e}")
        return
    
    # Test 3: Get public jobs (no auth needed)
    print("\n3. Testing public job listing...")
    try:
        response = requests.get(f"{BASE_URL}/careers/public/jobs/")
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Public jobs retrieved: {len(jobs.get('results', jobs))} jobs found")
            if jobs.get('results'):
                for job in jobs['results'][:2]:  # Show first 2 jobs
                    print(f"   - {job['title']} ({job['department']})")
        else:
            print(f"❌ Public jobs failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Public jobs error: {e}")
    
    # Test 4: Submit job application (no auth needed)
    print("\n4. Testing job application submission...")
    application_data = {
        "job_id": job_id,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+251911123456",
        "cover_letter": "I am very interested in this position and believe I would be a great fit for your team.",
        "portfolio_url": "https://johndoe.dev",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "years_of_experience": 4,
        "current_position": "Software Developer",
        "current_company": "Tech Corp"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/careers/public/apply/", json=application_data)
        if response.status_code == 201:
            application = response.json()
            print(f"✅ Application submitted successfully: {application['full_name']} applied for {application['job']['title']}")
        else:
            print(f"❌ Application failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Application error: {e}")
    
    # Test 5: Get job applications (admin only)
    print("\n5. Testing job applications listing...")
    try:
        response = requests.get(f"{BASE_URL}/careers/applications/", headers=headers)
        if response.status_code == 200:
            applications = response.json()
            print(f"✅ Applications retrieved: {len(applications.get('results', applications))} applications found")
            if applications.get('results'):
                for app in applications['results'][:2]:  # Show first 2 applications
                    print(f"   - {app['full_name']} applied for {app.get('job_title', 'Unknown Job')}")
        else:
            print(f"❌ Applications failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Applications error: {e}")
    
    print("\n🎉 Careers API test completed!")

if __name__ == "__main__":
    test_careers_api()