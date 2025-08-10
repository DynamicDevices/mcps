#!/usr/bin/env python3
"""Test filesystem server after configuration fix."""

import requests
import json
import os

SERVER_URL = "http://192.168.0.7:8000"
API_KEY = "mcp-secret-key-1754822293"

def test_filesystem_operations():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🔧 Testing Filesystem Server Operations")
    print("=" * 50)
    
    # Test 1: List allowed directories
    print("\n1. Testing list_allowed_directories...")
    try:
        response = requests.post(
            f"{SERVER_URL}/filesystem/list_allowed_directories",
            headers=headers,
            json={}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {result}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: List directory contents
    print("\n2. Testing list_directory...")
    try:
        response = requests.post(
            f"{SERVER_URL}/filesystem/list_directory",
            headers=headers,
            json={"path": "/home/ajlennon/mcp-service/files"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {result}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Try to access parent directory (should fail)
    print("\n3. Testing security - accessing parent directory (should fail)...")
    try:
        response = requests.post(
            f"{SERVER_URL}/filesystem/list_directory",
            headers=headers,
            json={"path": "/home/ajlennon/mcp-service"}
        )
        if response.status_code == 500:
            print(f"   ✅ Security working: Access denied as expected")
            print(f"   📝 Response: {response.text}")
        else:
            print(f"   ⚠️  Unexpected: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Create a test file
    print("\n4. Testing file creation...")
    try:
        response = requests.post(
            f"{SERVER_URL}/filesystem/write_file",
            headers=headers,
            json={
                "path": "/home/ajlennon/mcp-service/files/test.txt",
                "content": "Hello from MCP filesystem test!"
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ File created: {result}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Read the test file
    print("\n5. Testing file reading...")
    try:
        response = requests.post(
            f"{SERVER_URL}/filesystem/read_text_file",
            headers=headers,
            json={"path": "/home/ajlennon/mcp-service/files/test.txt"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ File read: {result}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("Testing filesystem server after configuration fix...")
    test_filesystem_operations()
    print("\n✅ Filesystem test completed!")
