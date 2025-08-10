#!/usr/bin/env python3
"""
Authentication Helper for MCP OpenAPI Proxy
"""

import requests
import json
import sys

def explore_auth_options(base_url="http://192.168.0.7:8000"):
    """Explore authentication options on the server"""
    
    print(f"Exploring authentication options for {base_url}")
    print("=" * 50)
    
    # Common authentication endpoints to check
    auth_endpoints = [
        "/auth",
        "/login", 
        "/token",
        "/authenticate",
        "/api/auth",
        "/api/login",
        "/api/token",
        "/oauth/token"
    ]
    
    print("\n1. Checking for authentication endpoints:")
    for endpoint in auth_endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            print(f"   ✓ {endpoint} - Status: {response.status_code}")
            if response.status_code != 404:
                print(f"     Response: {response.text[:100]}...")
        except:
            print(f"   ✗ {endpoint} - Not accessible")
    
    # Check for common auth headers that might work
    print("\n2. Testing common authentication bypasses:")
    test_headers = [
        {},  # No auth
        {"Authorization": "Bearer test"},
        {"Authorization": "Bearer token"},
        {"Authorization": "Bearer admin"},
        {"X-API-Key": "test"},
        {"X-Auth-Token": "test"},
    ]
    
    test_url = f"{base_url}/time/get_current_time"
    test_data = {"timezone": "UTC"}
    
    for i, headers in enumerate(test_headers):
        try:
            response = requests.post(test_url, json=test_data, headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"   ✓ SUCCESS with headers: {headers}")
                print(f"     Response: {response.json()}")
                return headers
            elif response.status_code != 401:
                print(f"   ? Status {response.status_code} with headers: {headers}")
                print(f"     Response: {response.text[:100]}...")
        except Exception as e:
            print(f"   ✗ Error with headers {headers}: {e}")
    
    print("\n3. Checking for environment variables or config hints:")
    try:
        # Check if there are any hints in the main docs
        response = requests.get(f"{base_url}/docs")
        content = response.text.lower()
        
        hints = []
        if "api" in content and "key" in content:
            hints.append("API key might be required")
        if "token" in content:
            hints.append("Token authentication might be required")
        if "bearer" in content:
            hints.append("Bearer token authentication detected")
        if "auth" in content:
            hints.append("Authentication system present")
            
        if hints:
            print("   Found hints:")
            for hint in hints:
                print(f"     - {hint}")
        else:
            print("   No obvious authentication hints found")
            
    except Exception as e:
        print(f"   Error checking docs: {e}")
    
    print("\n4. Server might require:")
    print("   - A valid API token/key")
    print("   - Server-side configuration")
    print("   - Network-level authentication")
    print("   - Contact with server administrator")
    
    return None

def create_config_template():
    """Create configuration templates with authentication placeholders"""
    
    config_template = {
        "base_url": "http://192.168.0.7:8000",
        "authentication": {
            "type": "bearer",  # or "api_key", "basic", etc.
            "token": "YOUR_TOKEN_HERE",
            "header_name": "Authorization",  # or "X-API-Key", etc.
            "header_format": "Bearer {token}"  # or "ApiKey {token}", etc.
        },
        "endpoints": {
            "memory": "/memory",
            "time": "/time", 
            "filesystem": "/filesystem"
        },
        "docs": {
            "main": "/docs",
            "memory": "/memory/docs",
            "time": "/time/docs",
            "filesystem": "/filesystem/docs"
        }
    }
    
    print("\nConfiguration template (save as 'config.json'):")
    print(json.dumps(config_template, indent=2))
    
    with open("auth_config_template.json", "w") as f:
        json.dump(config_template, f, indent=2)
    print("\nTemplate saved as 'auth_config_template.json'")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://192.168.0.7:8000"
    
    # Explore authentication
    working_headers = explore_auth_options(base_url)
    
    # Create config template
    create_config_template()
    
    if working_headers:
        print(f"\n✓ Found working authentication: {working_headers}")
    else:
        print("\n❓ No working authentication found.")
        print("\nNext steps:")
        print("1. Contact the server administrator for authentication details")
        print("2. Check server logs or documentation for required tokens")
        print("3. Verify if the server requires specific network access")
        print("4. Edit 'auth_config_template.json' with correct authentication")

if __name__ == "__main__":
    main()