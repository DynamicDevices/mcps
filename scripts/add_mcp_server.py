#!/usr/bin/env python3
"""
Script to help add new MCP servers to your configuration.
Usage: python3 scripts/add_mcp_server.py <server-name>
"""

import json
import sys
import os
from pathlib import Path

# Available servers with their configurations
AVAILABLE_SERVERS = {
    "fetch": {
        "command": "uvx",
        "args": ["mcp-server-fetch"],
        "description": "Web scraping and API access",
        "requires_auth": False
    },
    "brave-search": {
        "command": "npx", 
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "description": "Web search capabilities",
        "requires_auth": True,
        "auth_note": "Requires BRAVE_API_KEY environment variable"
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "description": "GitHub repository management",
        "requires_auth": True,
        "auth_note": "Requires GITHUB_TOKEN environment variable"
    },
    "sqlite": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"],
        "description": "SQLite database operations",
        "requires_auth": False,
        "note": "Update the database path in the args"
    },
    "postgresql": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgresql"],
        "description": "PostgreSQL database operations",
        "requires_auth": True,
        "auth_note": "Requires DATABASE_URL environment variable"
    },
    "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "description": "Slack workspace management",
        "requires_auth": True,
        "auth_note": "Requires SLACK_BOT_TOKEN environment variable"
    },
    "google-drive": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-drive"],
        "description": "Google Drive file management",
        "requires_auth": True,
        "auth_note": "Requires Google API credentials"
    },
    "puppeteer": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
        "description": "Browser automation and web scraping",
        "requires_auth": False
    },
    "openscad": {
        "command": "/home/ajlennon/stable-diffusion-webui/venv/bin/python",
        "args": ["/home/ajlennon/mcp-service/OpenSCAD-MCP-Server/src/main.py"],
        "description": "3D modeling and CAD operations with OpenSCAD",
        "requires_auth": False,
        "note": "Uses existing Stable Diffusion venv, requires OpenSCAD binary"
    }
}

def load_config():
    """Load the current MCP configuration."""
    config_path = Path("server_config/mcp-config.json")
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return None
    
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save the updated MCP configuration."""
    config_path = Path("server_config/mcp-config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Updated local configuration: {config_path}")

def list_available_servers():
    """Display all available servers."""
    print("\n🔧 Available MCP Servers:")
    print("=" * 50)
    
    for server_name, server_config in AVAILABLE_SERVERS.items():
        auth_indicator = "🔐" if server_config.get("requires_auth") else "🆓"
        print(f"\n{auth_indicator} **{server_name}**")
        print(f"   📝 {server_config['description']}")
        
        if server_config.get("requires_auth"):
            print(f"   🔑 {server_config.get('auth_note', 'Requires authentication')}")
        
        if server_config.get("note"):
            print(f"   ⚠️  {server_config['note']}")

def add_server(server_name):
    """Add a server to the configuration."""
    if server_name not in AVAILABLE_SERVERS:
        print(f"❌ Unknown server: {server_name}")
        print("\nAvailable servers:")
        for name in AVAILABLE_SERVERS.keys():
            print(f"  - {name}")
        return False
    
    # Load current config
    config = load_config()
    if not config:
        return False
    
    # Check if server already exists
    if server_name in config.get("mcpServers", {}):
        print(f"⚠️  Server '{server_name}' already exists in configuration!")
        return False
    
    # Add the new server
    server_config = AVAILABLE_SERVERS[server_name]
    config["mcpServers"][server_name] = {
        "command": server_config["command"],
        "args": server_config["args"]
    }
    
    # Save updated config
    save_config(config)
    
    print(f"\n✅ Added server: {server_name}")
    print(f"📝 Description: {server_config['description']}")
    
    if server_config.get("requires_auth"):
        print(f"\n🔑 Authentication Required:")
        print(f"   {server_config.get('auth_note')}")
        print(f"\n   To set up authentication on your server:")
        print(f"   ssh ajlennon@ollama")
        if "GITHUB_TOKEN" in server_config.get("auth_note", ""):
            print(f"   export GITHUB_TOKEN='your-github-token'")
        elif "BRAVE_API_KEY" in server_config.get("auth_note", ""):
            print(f"   export BRAVE_API_KEY='your-brave-api-key'")
        elif "SLACK_BOT_TOKEN" in server_config.get("auth_note", ""):
            print(f"   export SLACK_BOT_TOKEN='your-slack-bot-token'")
        else:
            print(f"   # Set up required environment variables")
    
    if server_config.get("note"):
        print(f"\n⚠️  Note: {server_config['note']}")
    
    print(f"\n🔄 Next steps:")
    print(f"   1. Copy this configuration to your server:")
    print(f"      scp server_config/mcp-config.json ajlennon@ollama:/home/ajlennon/mcp-service/")
    print(f"   2. Restart the MCP proxy service:")
    print(f"      ssh ajlennon@ollama 'sudo systemctl restart mcp-proxy'")
    print(f"   3. Test the new server in Open WebUI")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("MCP Server Management Script")
        print("=" * 30)
        print("\nUsage:")
        print("  python3 scripts/add_mcp_server.py list")
        print("  python3 scripts/add_mcp_server.py <server-name>")
        print("\nExamples:")
        print("  python3 scripts/add_mcp_server.py fetch")
        print("  python3 scripts/add_mcp_server.py github")
        list_available_servers()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_available_servers()
    elif command in AVAILABLE_SERVERS:
        add_server(command)
    else:
        print(f"❌ Unknown command or server: {command}")
        print("\nUse 'list' to see available servers")
        list_available_servers()

if __name__ == "__main__":
    main()
