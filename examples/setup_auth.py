#!/usr/bin/env python3
"""
Setup authentication for MCP OpenAPI Proxy
"""

import os
import sys
import json

def main():
    """Help user set up authentication"""
    
    print("🔐 MCP OpenAPI Proxy Authentication Setup")
    print("=" * 45)
    
    print("\nYour MCP server at http://192.168.0.7:8000 requires authentication.")
    print("We discovered that it expects a Bearer token in the format:")
    print("   Authorization: Bearer <your-token>")
    
    print("\n📋 Setup Options:")
    print("1. Environment Variable (Recommended)")
    print("2. Token File")
    print("3. Configuration File")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        setup_env_var()
    elif choice == "2":
        setup_token_file()
    elif choice == "3":
        setup_config_file()
    else:
        print("Invalid choice. Exiting.")
        return
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Get your actual API token from the server administrator")
    print("2. Replace the placeholder with your real token")
    print("3. Test with: python3 mcp_authenticated_client.py time_now")

def setup_env_var():
    """Setup environment variable method"""
    print("\n📝 Setting up environment variable...")
    
    token = input("Enter your API token (or 'placeholder' for now): ").strip()
    if not token:
        token = "placeholder-token-replace-me"
    
    # Add to shell profile
    shell = os.getenv("SHELL", "/bin/bash")
    
    if "zsh" in shell:
        profile_file = os.path.expanduser("~/.zshrc")
    elif "bash" in shell:
        profile_file = os.path.expanduser("~/.bashrc")
    else:
        profile_file = os.path.expanduser("~/.profile")
    
    export_line = f'export MCP_API_TOKEN="{token}"'
    
    print(f"\nAdd this line to your {profile_file}:")
    print(f"   {export_line}")
    
    try:
        with open(profile_file, "a") as f:
            f.write(f"\n# MCP API Token\n{export_line}\n")
        print(f"✅ Added to {profile_file}")
        
        # Set for current session
        os.environ["MCP_API_TOKEN"] = token
        print("✅ Set for current session")
        
        print(f"\n⚠️  Restart your terminal or run: source {profile_file}")
        
    except Exception as e:
        print(f"❌ Could not write to {profile_file}: {e}")
        print(f"Please manually add: {export_line}")

def setup_token_file():
    """Setup token file method"""
    print("\n📝 Setting up token file...")
    
    token = input("Enter your API token (or 'placeholder' for now): ").strip()
    if not token:
        token = "placeholder-token-replace-me"
    
    try:
        with open("mcp_token.txt", "w") as f:
            f.write(token)
        print("✅ Created mcp_token.txt")
        print("⚠️  Remember to replace the placeholder with your real token!")
        
        # Add to .gitignore
        try:
            gitignore_content = "mcp_token.txt\n"
            if os.path.exists(".gitignore"):
                with open(".gitignore", "r") as f:
                    existing = f.read()
                if "mcp_token.txt" not in existing:
                    with open(".gitignore", "a") as f:
                        f.write(gitignore_content)
            else:
                with open(".gitignore", "w") as f:
                    f.write(gitignore_content)
            print("✅ Added to .gitignore for security")
        except:
            print("⚠️  Consider adding mcp_token.txt to .gitignore")
            
    except Exception as e:
        print(f"❌ Could not create token file: {e}")

def setup_config_file():
    """Setup configuration file method"""
    print("\n📝 Setting up configuration file...")
    
    token = input("Enter your API token (or 'placeholder' for now): ").strip()
    if not token:
        token = "placeholder-token-replace-me"
    
    # Update the existing template
    try:
        with open("auth_config_template.json", "r") as f:
            config = json.load(f)
            
        config["authentication"]["token"] = token
        
        with open("mcp_config.json", "w") as f:
            json.dump(config, f, indent=2)
            
        print("✅ Created mcp_config.json")
        print("⚠️  Remember to replace the placeholder with your real token!")
        
    except Exception as e:
        print(f"❌ Could not create config file: {e}")

if __name__ == "__main__":
    main()