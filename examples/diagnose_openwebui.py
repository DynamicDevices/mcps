#!/usr/bin/env python3
"""
Open WebUI MCP Integration Diagnostic Tool

This script helps diagnose why MCP tools might not be working in Open WebUI.
"""

import requests
import json
import time

def test_mcp_server():
    """Test MCP server connectivity and authentication"""
    print("🔍 Testing MCP Server...")
    print("=" * 40)
    
    base_url = "http://192.168.0.7:8000"
    api_key = "mcp-secret-key-1754822293"
    
    # Test 1: Basic connectivity
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ MCP server is accessible")
        else:
            print(f"❌ MCP server returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to MCP server: {e}")
        return False
    
    # Test 2: OpenAPI spec
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            print("✅ OpenAPI spec accessible")
            spec = response.json()
            print(f"   Server title: {spec.get('info', {}).get('title', 'Unknown')}")
        else:
            print(f"❌ OpenAPI spec failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI spec error: {e}")
    
    # Test 3: Authentication
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{base_url}/time/get_current_time",
            json={"timezone": "UTC"},
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Authentication working")
            print(f"   Current time: {result.get('datetime', 'N/A')}")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        return False

def check_openwebui_config():
    """Provide configuration guidance"""
    print("\n🔧 Open WebUI Configuration Check")
    print("=" * 40)
    
    print("1. Verify these settings in Open WebUI:")
    print("   Settings → Admin Panel → Tools → OpenAPI Servers")
    print()
    print("2. Required configuration:")
    print("   • Name: MCP Tools")
    print("   • URL: http://192.168.0.7:8000")
    print("   • Authentication: Bearer Token")
    print("   • API Key: mcp-secret-key-1754822293")
    print()
    
    config = {
        "name": "MCP Tools",
        "url": "http://192.168.0.7:8000",
        "headers": {
            "Authorization": "Bearer mcp-secret-key-1754822293",
            "Content-Type": "application/json"
        },
        "enabled": True
    }
    
    print("3. JSON Configuration (copy this):")
    print(json.dumps(config, indent=2))

def test_tool_endpoints():
    """Test individual tool endpoints"""
    print("\n🛠️  Testing Individual Tools...")
    print("=" * 40)
    
    base_url = "http://192.168.0.7:8000"
    headers = {
        "Authorization": "Bearer mcp-secret-key-1754822293",
        "Content-Type": "application/json"
    }
    
    # Test time tool
    try:
        response = requests.post(
            f"{base_url}/time/get_current_time",
            json={"timezone": "America/New_York"},
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Time tool: New York time is {result.get('datetime', 'N/A')}")
        else:
            print(f"❌ Time tool failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Time tool error: {e}")
    
    # Test memory tool
    try:
        response = requests.post(
            f"{base_url}/memory/read_graph",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            entity_count = len(result.get('entities', []))
            print(f"✅ Memory tool: {entity_count} entities in knowledge graph")
        else:
            print(f"❌ Memory tool failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Memory tool error: {e}")
    
    # Test filesystem tool
    try:
        response = requests.post(
            f"{base_url}/filesystem/list_allowed_directories",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Filesystem tool: Allowed directories accessible")
        else:
            print(f"❌ Filesystem tool failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Filesystem tool error: {e}")

def provide_troubleshooting_steps():
    """Provide specific troubleshooting steps"""
    print("\n🚨 Troubleshooting Steps")
    print("=" * 40)
    
    print("If tools aren't working in Open WebUI, try these steps:")
    print()
    print("1. CHECK TOOL VISIBILITY:")
    print("   • Look for a tools icon (🔧) in the chat interface")
    print("   • Click it to see if MCP tools are listed")
    print("   • Enable/select the tools you want to use")
    print()
    print("2. TRY EXPLICIT REQUESTS:")
    print("   Instead of: 'What time is it?'")
    print("   Try: 'Use the get_current_time tool to show me the current time'")
    print()
    print("3. CHECK OPEN WEBUI VERSION:")
    print("   • Requires Open WebUI v0.6 or later")
    print("   • Check: Settings → About")
    print()
    print("4. BROWSER ISSUES:")
    print("   • Hard refresh (Ctrl+F5)")
    print("   • Clear browser cache")
    print("   • Check browser console for errors")
    print()
    print("5. NETWORK CONNECTIVITY:")
    print("   • Ensure Open WebUI can reach 192.168.0.7:8000")
    print("   • Check Docker network settings if applicable")
    print()
    print("6. MODEL COMPATIBILITY:")
    print("   • Try different models (GPT-4, Claude, etc.)")
    print("   • Ensure function calling is enabled")

def main():
    """Run complete diagnostic"""
    print("🏥 Open WebUI MCP Integration Diagnostic")
    print("=" * 50)
    print()
    
    # Test MCP server
    server_ok = test_mcp_server()
    
    # Check configuration
    check_openwebui_config()
    
    # Test tools if server is working
    if server_ok:
        test_tool_endpoints()
    
    # Provide troubleshooting guidance
    provide_troubleshooting_steps()
    
    print("\n" + "=" * 50)
    if server_ok:
        print("✅ MCP Server is working correctly!")
        print("❓ If tools still don't work in Open WebUI, it's a configuration issue.")
        print("📚 See docs/troubleshooting_openwebui.md for detailed help.")
    else:
        print("❌ MCP Server has issues - fix these first!")
    print("=" * 50)

if __name__ == "__main__":
    main()