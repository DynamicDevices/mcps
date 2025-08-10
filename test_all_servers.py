#!/usr/bin/env python3
"""Test all MCP servers to verify they're working correctly."""

import requests
import json

SERVER_URL = "http://192.168.0.7:8000"
API_KEY = "mcp-secret-key-1754822293"

def test_all_servers():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing All MCP Servers")
    print("=" * 50)
    
    # Test 1: Time Server
    print("\n1. ⏰ Testing Time Server...")
    try:
        response = requests.post(
            f"{SERVER_URL}/time/get_current_time",
            headers=headers,
            json={"timezone": "UTC"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: Current time is {result['datetime']}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Memory Server
    print("\n2. 🧠 Testing Memory Server...")
    try:
        response = requests.post(
            f"{SERVER_URL}/memory/read_graph",
            headers=headers,
            json={}
        )
        if response.status_code == 200:
            print(f"   ✅ Success: Memory server accessible")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Filesystem Server
    print("\n3. 📁 Testing Filesystem Server...")
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
    
    # Test 4: Fetch Server (NEW!)
    print("\n4. 🌐 Testing Fetch Server...")
    try:
        response = requests.post(
            f"{SERVER_URL}/fetch/fetch",
            headers=headers,
            json={"url": "https://httpbin.org/json"}
        )
        if response.status_code == 200:
            result = response.json()
            if "slideshow" in result:
                print(f"   ✅ Success: Fetch server working - retrieved JSON data")
            else:
                print(f"   ✅ Success: Fetch server working - retrieved content")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Check available endpoints
    print("\n5. 📋 Available Servers Summary...")
    try:
        response = requests.get(f"{SERVER_URL}/openapi.json")
        if response.status_code == 200:
            openapi = response.json()
            description = openapi.get('info', {}).get('description', '')
            print("   Available servers:")
            for line in description.split('\n'):
                if '- [' in line and '](/' in line:
                    print(f"   {line.strip()}")
        else:
            print(f"   ❌ Failed to get OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Server test completed!")
    print(f"\nNext steps:")
    print(f"1. The fetch server is now available in Open WebUI")
    print(f"2. You can now ask things like:")
    print(f"   - 'Fetch the content from https://example.com'")
    print(f"   - 'Get the JSON data from https://api.github.com/users/octocat'")
    print(f"   - 'Scrape the headlines from https://news.ycombinator.com'")

if __name__ == "__main__":
    test_all_servers()
