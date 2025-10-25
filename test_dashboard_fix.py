#!/usr/bin/env python
"""
Test script to verify dashboard API endpoints are working correctly
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_dashboard_endpoints():
    """Test dashboard endpoints"""
    print("🧪 Testing Dashboard API Endpoints...")
    
    endpoints = [
        "/dashboard/overview/",
        "/dashboard/activities/recent/",
        "/dashboard/metrics/chart/?type=revenue_monthly",
        "/dashboard/combined/"  # New combined endpoint
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n📡 Testing: {endpoint}")
            start_time = time.time()
            
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success - {response.status_code} ({response_time}ms)")
                if isinstance(data, dict):
                    print(f"   Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"   Items: {len(data)}")
            else:
                print(f"❌ Failed - {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")

def test_cors_headers():
    """Test CORS headers"""
    print("\n🌐 Testing CORS Headers...")
    
    try:
        response = requests.options(f"{BASE_URL}/dashboard/overview/", 
                                  headers={'Origin': 'http://localhost:5173'})
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print("CORS Headers:")
        for header, value in cors_headers.items():
            if value:
                print(f"  ✅ {header}: {value}")
            else:
                print(f"  ❌ {header}: Not set")
                
    except Exception as e:
        print(f"❌ CORS Test Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Backend API Tests...")
    print("=" * 50)
    
    test_dashboard_endpoints()
    test_cors_headers()
    
    print("\n" + "=" * 50)
    print("✨ Tests completed!")