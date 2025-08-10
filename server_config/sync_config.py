#!/usr/bin/env python3
"""
MCP Server Configuration Sync Tool

Helps manage and synchronize MCP server configurations between 
the remote server and local development environment.
"""

import json
import subprocess
import sys
import os
from datetime import datetime

class MCPConfigManager:
    def __init__(self):
        self.remote_host = "ajlennon@ollama"
        self.remote_config_path = "/home/ajlennon/mcp-service/mcp-config.json"
        self.local_config_path = "server_config/mcp-config.json"
        self.notes_path = "server_config/server_notes.md"
        
    def fetch_remote_config(self):
        """Fetch configuration from remote server"""
        print(f"Fetching configuration from {self.remote_host}...")
        
        try:
            result = subprocess.run([
                "ssh", self.remote_host, 
                f"cat {self.remote_config_path}"
            ], capture_output=True, text=True, check=True)
            
            config = json.loads(result.stdout)
            print("✅ Successfully fetched remote configuration")
            return config
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error fetching config: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in remote config: {e}")
            return None
    
    def save_local_config(self, config):
        """Save configuration to local file"""
        try:
            with open(self.local_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Saved configuration to {self.local_config_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving local config: {e}")
            return False
    
    def load_local_config(self):
        """Load local configuration"""
        try:
            with open(self.local_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Local config not found: {self.local_config_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in local config: {e}")
            return None
    
    def compare_configs(self, remote_config, local_config):
        """Compare remote and local configurations"""
        if local_config is None:
            return {"status": "no_local", "differences": []}
        
        if remote_config == local_config:
            return {"status": "identical", "differences": []}
        
        differences = []
        remote_servers = set(remote_config.get("mcpServers", {}).keys())
        local_servers = set(local_config.get("mcpServers", {}).keys())
        
        # New servers on remote
        new_servers = remote_servers - local_servers
        if new_servers:
            differences.append(f"New servers on remote: {', '.join(new_servers)}")
        
        # Removed servers
        removed_servers = local_servers - remote_servers
        if removed_servers:
            differences.append(f"Servers removed from remote: {', '.join(removed_servers)}")
        
        # Modified servers
        for server in remote_servers & local_servers:
            remote_server = remote_config["mcpServers"][server]
            local_server = local_config["mcpServers"][server]
            if remote_server != local_server:
                differences.append(f"Server '{server}' configuration changed")
        
        return {
            "status": "different" if differences else "identical",
            "differences": differences
        }
    
    def update_notes(self, config):
        """Update the server notes with current timestamp and server list"""
        try:
            with open(self.notes_path, 'r') as f:
                content = f.read()
            
            # Update the last updated timestamp
            current_time = datetime.now().strftime("%B %d, %Y at %H:%M")
            updated_content = content.replace(
                "- **Last Updated**: August 10, 2025",
                f"- **Last Updated**: {current_time}"
            )
            
            # Update server count
            server_count = len(config.get("mcpServers", {}))
            server_names = ", ".join(config.get("mcpServers", {}).keys())
            updated_content = updated_content.replace(
                "- **MCP Servers**: 3 servers (memory, time, filesystem)",
                f"- **MCP Servers**: {server_count} servers ({server_names})"
            )
            
            with open(self.notes_path, 'w') as f:
                f.write(updated_content)
                
            print(f"✅ Updated notes in {self.notes_path}")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not update notes: {e}")
            return False
    
    def sync_from_remote(self):
        """Sync configuration from remote server"""
        print("🔄 Syncing MCP configuration from remote server...")
        
        # Fetch remote config
        remote_config = self.fetch_remote_config()
        if not remote_config:
            return False
        
        # Load local config for comparison
        local_config = self.load_local_config()
        
        # Compare configurations
        comparison = self.compare_configs(remote_config, local_config)
        
        print(f"\n📊 Configuration Status: {comparison['status']}")
        if comparison['differences']:
            print("📝 Changes detected:")
            for diff in comparison['differences']:
                print(f"  - {diff}")
        
        # Save updated config
        if self.save_local_config(remote_config):
            self.update_notes(remote_config)
            print("✅ Configuration sync complete!")
            return True
        
        return False
    
    def list_servers(self):
        """List current servers in configuration"""
        config = self.load_local_config()
        if not config:
            print("❌ No local configuration found")
            return
        
        servers = config.get("mcpServers", {})
        print(f"\n📋 Current MCP Servers ({len(servers)}):")
        print("=" * 40)
        
        for name, details in servers.items():
            command = details.get("command", "unknown")
            args = " ".join(details.get("args", []))
            print(f"🔧 {name}")
            print(f"   Command: {command}")
            print(f"   Args: {args}")
            print()
    
    def show_service_status(self):
        """Show remote service status"""
        print("🔍 Checking remote MCP service status...")
        
        try:
            # Check if mcpo process is running
            result = subprocess.run([
                "ssh", self.remote_host,
                "ps aux | grep mcpo | grep -v grep"
            ], capture_output=True, text=True)
            
            if result.stdout.strip():
                print("✅ MCP Proxy service is running")
                print(f"Process: {result.stdout.strip()}")
            else:
                print("❌ MCP Proxy service not found")
                
            # Check service accessibility
            result = subprocess.run([
                "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                "http://192.168.0.7:8000/docs"
            ], capture_output=True, text=True)
            
            if result.stdout.strip() == "200":
                print("✅ MCP service is accessible at http://192.168.0.7:8000")
            else:
                print(f"⚠️  MCP service returned status: {result.stdout.strip()}")
                
        except Exception as e:
            print(f"❌ Error checking service status: {e}")

def main():
    """Main CLI interface"""
    manager = MCPConfigManager()
    
    if len(sys.argv) < 2:
        print("Usage: python3 sync_config.py <command>")
        print("\nCommands:")
        print("  sync     - Sync configuration from remote server")
        print("  list     - List current MCP servers")
        print("  status   - Check remote service status")
        return
    
    command = sys.argv[1]
    
    if command == "sync":
        manager.sync_from_remote()
    elif command == "list":
        manager.list_servers()
    elif command == "status":
        manager.show_service_status()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()