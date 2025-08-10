#!/usr/bin/env python3
"""
Open WebUI MCP Integration Setup Helper

This script helps you configure Open WebUI to connect to your MCP server.
It provides the exact configuration values and can test the connection.
"""

import json
import requests
import sys

class OpenWebUISetup:
    def __init__(self):
        self.mcp_server_url = "http://192.168.0.7:8000"
        self.api_key = "mcp-secret-key-1754822293"
        
    def generate_config(self):
        """Generate the configuration for Open WebUI"""
        config = {
            "name": "MCP Tools (Time, Memory, Filesystem)",
            "url": self.mcp_server_url,
            "headers": {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "OpenWebUI-MCP-Client"
            },
            "enabled": True,
            "description": "Access to Time operations, Knowledge graph, and Filesystem tools via MCP"
        }
        return config
    
    def test_connection(self):
        """Test connection to MCP server"""
        print(f"🔍 Testing connection to {self.mcp_server_url}...")
        
        try:
            # Test basic connectivity
            response = requests.get(f"{self.mcp_server_url}/docs", timeout=10)
            if response.status_code == 200:
                print("✅ MCP server is accessible")
            else:
                print(f"⚠️  MCP server returned status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to MCP server: {e}")
            return False
        
        # Test authentication with a simple tool call
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.mcp_server_url}/time/get_current_time",
                json={"timezone": "UTC"},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Authentication successful!")
                print(f"   Current UTC time: {result.get('datetime', 'N/A')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication test failed: {e}")
            return False
    
    def list_available_tools(self):
        """List all available tools from the MCP server"""
        print("\n📋 Available MCP Tools:")
        print("=" * 50)
        
        # Get OpenAPI spec
        try:
            response = requests.get(f"{self.mcp_server_url}/openapi.json", timeout=10)
            if response.status_code != 200:
                print("❌ Could not retrieve tool list")
                return
                
            spec = response.json()
            
            # Extract tool information from each service
            services = {
                "Time Server": f"{self.mcp_server_url}/time/openapi.json",
                "Memory Server": f"{self.mcp_server_url}/memory/openapi.json", 
                "Filesystem Server": f"{self.mcp_server_url}/filesystem/openapi.json"
            }
            
            for service_name, spec_url in services.items():
                try:
                    service_response = requests.get(spec_url, timeout=5)
                    if service_response.status_code == 200:
                        service_spec = service_response.json()
                        paths = service_spec.get("paths", {})
                        
                        print(f"\n🔧 {service_name}:")
                        for path, methods in paths.items():
                            for method, details in methods.items():
                                if method.lower() == "post":
                                    tool_name = path.strip("/")
                                    description = details.get("description", "No description")
                                    print(f"   • {tool_name}: {description}")
                                    
                except:
                    print(f"   ⚠️  Could not load {service_name} tools")
                    
        except Exception as e:
            print(f"❌ Error listing tools: {e}")
    
    def print_setup_instructions(self):
        """Print setup instructions for Open WebUI"""
        config = self.generate_config()
        
        print("\n" + "="*60)
        print("🚀 OPEN WEBUI MCP SETUP INSTRUCTIONS")
        print("="*60)
        
        print("\n1. Open WebUI Configuration:")
        print("   • Log into Open WebUI as administrator")
        print("   • Go to Settings → Admin Panel → Tools")
        print("   • Look for 'OpenAPI Servers' or 'MCP Servers'")
        
        print("\n2. Add New Server with these settings:")
        print(f"   • Name: {config['name']}")
        print(f"   • URL: {config['url']}")
        print(f"   • API Key: {self.api_key}")
        print("   • Authentication: Bearer Token")
        
        print("\n3. JSON Configuration (if needed):")
        print(json.dumps(config, indent=2))
        
        print("\n4. Testing in Open WebUI:")
        print("   • Save the configuration")
        print("   • Start a new chat")
        print("   • Look for tools icon (🔧) in chat interface")
        print("   • Try: 'What time is it in Tokyo?'")
        
        print("\n5. Example Prompts to Try:")
        print("   🕐 Time: 'Convert 3 PM UTC to New York time'")
        print("   🧠 Memory: 'Create an entity called Python with type Programming Language'") 
        print("   📁 Files: 'List all files in my workspace'")
        
        print(f"\n📚 Documentation: See docs/openwebui_integration.md for details")
        print(f"🌐 Server Docs: {self.mcp_server_url}/docs")
        
        print("\n" + "="*60)
    
    def run_full_setup(self):
        """Run complete setup process"""
        print("🔧 Open WebUI MCP Integration Setup")
        print("="*40)
        
        # Test connection
        if not self.test_connection():
            print("\n❌ Setup cannot continue - fix connection issues first")
            return False
        
        # List available tools
        self.list_available_tools()
        
        # Print setup instructions
        self.print_setup_instructions()
        
        return True

def main():
    """Main setup function"""
    setup = OpenWebUISetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            setup.test_connection()
        elif command == "tools":
            setup.list_available_tools()
        elif command == "config":
            config = setup.generate_config()
            print(json.dumps(config, indent=2))
        elif command == "instructions":
            setup.print_setup_instructions()
        else:
            print("Usage: python3 openwebui_setup.py [test|tools|config|instructions]")
    else:
        setup.run_full_setup()

if __name__ == "__main__":
    main()