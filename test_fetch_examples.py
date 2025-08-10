#!/usr/bin/env python3
"""Test fetch server with reliable endpoints."""

import requests
import json

SERVER_URL = "http://192.168.0.7:8000"
API_KEY = "mcp-secret-key-1754822293"

def test_fetch_examples():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🌐 Testing Fetch Server with Reliable Endpoints")
    print("=" * 60)
    
    # Test 1: Simple HTML page
    print("\n1. 🌍 Testing simple HTML page...")
    try:
        response = requests.post(
            f"{SERVER_URL}/fetch/fetch",
            headers=headers,
            json={"url": "https://example.com"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: Fetched example.com")
            print(f"   📄 Content preview: {result[:100]}...")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: GitHub API (JSON)
    print("\n2. 📦 Testing GitHub API...")
    try:
        response = requests.post(
            f"{SERVER_URL}/fetch/fetch",
            headers=headers,
            json={"url": "https://api.github.com/repos/octocat/Hello-World"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: Fetched GitHub repo data")
            if "name" in result:
                print(f"   📦 Found repo: {result.get('name', 'Unknown')}")
            else:
                print(f"   📄 Content preview: {result[:100]}...")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Plain text endpoint
    print("\n3. 📝 Testing plain text endpoint...")
    try:
        response = requests.post(
            f"{SERVER_URL}/fetch/fetch",
            headers=headers,
            json={"url": "https://www.iana.org/domains/example"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: Fetched IANA page")
            print(f"   📄 Content preview: {result[:150]}...")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Different fetch options
    print("\n4. ⚙️ Testing with options...")
    try:
        response = requests.post(
            f"{SERVER_URL}/fetch/fetch",
            headers=headers,
            json={
                "url": "https://example.com",
                "max_length": 200,  # Limit content length
                "raw": False        # Convert to markdown
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: Fetched with options")
            print(f"   📄 Limited content: {result}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 Open WebUI Examples:")
    print(f"Try asking your AI these questions:")
    print(f"")
    print(f"💡 'Fetch the content from https://example.com and tell me what it says'")
    print(f"💡 'Get information about the octocat/Hello-World repository from GitHub'")
    print(f"💡 'Fetch https://www.iana.org/domains/example and summarize it'")
    print(f"💡 'Get the latest Python news from https://www.python.org'")
    print(f"")
    print(f"Note: The fetch server converts HTML to markdown automatically,")
    print(f"making it easy for the AI to understand web content!")

if __name__ == "__main__":
    test_fetch_examples()
