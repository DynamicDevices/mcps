#!/usr/bin/env python3
"""
Test script to verify connection to the remote MCP server
"""

import requests
import json
import sys

def test_mcp_server_connection():
    """Test connection to the MCP server at 192.168.0.7:8000"""
    
    base_url = "http://192.168.0.7:8000"
    
    print(f"Testing connection to MCP server at {base_url}")
    
    # Test basic connectivity
    try:
        print("\n1. Testing basic connectivity...")
        response = requests.get(f"{base_url}/docs", timeout=10)
        print(f"   ✓ Documentation endpoint accessible (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Failed to connect to documentation endpoint: {e}")
        return False
    
    # Test MCP endpoint
    try:
        print("\n2. Testing MCP endpoint...")
        # Try different possible MCP endpoints
        mcp_endpoints = ["/mcp", "/sse", "/api/mcp"]
        
        for endpoint in mcp_endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                print(f"   ✓ MCP endpoint {endpoint} accessible (Status: {response.status_code})")
                break
            except requests.exceptions.RequestException:
                print(f"   - MCP endpoint {endpoint} not accessible")
                continue
        else:
            print("   ! No standard MCP endpoints found - server may use custom endpoint")
    
    except Exception as e:
        print(f"   ✗ Error testing MCP endpoints: {e}")
    
    # Test for server info
    try:
        print("\n3. Testing server information...")
        info_endpoints = ["/info", "/status", "/health", "/mcp/info"]
        
        for endpoint in info_endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"   ✓ Server info endpoint {endpoint} found")
                    try:
                        data = response.json()
                        print(f"   Server info: {json.dumps(data, indent=2)}")
                    except:
                        print(f"   Response: {response.text[:200]}...")
                    break
            except:
                continue
        else:
            print("   - No server info endpoints found")
    
    except Exception as e:
        print(f"   ✗ Error getting server info: {e}")
    
    print(f"\n✓ Connection test completed. Server appears to be running at {base_url}")
    return True

if __name__ == "__main__":
    success = test_mcp_server_connection()
    sys.exit(0 if success else 1)