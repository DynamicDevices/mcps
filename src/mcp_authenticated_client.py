#!/usr/bin/env python3
"""
Authenticated MCP OpenAPI Proxy Client
"""

import requests
import json
import sys
import os
from typing import Dict, List, Any, Optional

class MCPAuthenticatedClient:
    """Authenticated client for MCP OpenAPI Proxy"""
    
    def __init__(self, base_url: str = "http://192.168.0.7:8000", token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Get token from parameter, environment variable, or config file
        if not token:
            token = self._get_token()
        
        if not token:
            print("⚠️  No authentication token provided!")
            print("Options:")
            print("1. Set MCP_API_TOKEN environment variable")
            print("2. Create 'mcp_token.txt' file with your token")
            print("3. Pass token directly: client = MCPAuthenticatedClient(token='your-token')")
            print("4. Contact server administrator for authentication details")
            sys.exit(1)
        
        # Set up authentication
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "MCP-Authenticated-Client/1.0"
        })
        
        # Test authentication
        if not self._test_auth():
            print("❌ Authentication failed!")
            print("Please check your token and try again.")
            sys.exit(1)
        else:
            print("✅ Authentication successful!")

    def _get_token(self) -> Optional[str]:
        """Get token from various sources"""
        
        # Try environment variable
        token = os.getenv("MCP_API_TOKEN")
        if token:
            print("📝 Using token from MCP_API_TOKEN environment variable")
            return token
        
        # Try token file
        try:
            with open("mcp_token.txt", "r") as f:
                token = f.read().strip()
                if token:
                    print("📝 Using token from mcp_token.txt file")
                    return token
        except FileNotFoundError:
            pass
        
        # Try config file
        try:
            with open("auth_config_template.json", "r") as f:
                config = json.load(f)
                token = config.get("authentication", {}).get("token")
                if token and token != "YOUR_TOKEN_HERE":
                    print("📝 Using token from auth_config_template.json")
                    return token
        except FileNotFoundError:
            pass
        
        return None

    def _test_auth(self) -> bool:
        """Test if authentication is working"""
        try:
            response = self.session.post(f"{self.base_url}/time/get_current_time", 
                                       json={"timezone": "UTC"}, 
                                       timeout=10)
            return response.status_code == 200
        except:
            return False

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make authenticated HTTP request"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    return {"error": str(e), "detail": error_detail}
                except:
                    return {"error": str(e), "response": e.response.text[:200]}
            return {"error": str(e)}

    # ===== MEMORY SERVER METHODS =====
    
    def memory_create_entities(self, entities: List[Dict]) -> Dict:
        """Create entities in the knowledge graph"""
        return self._make_request("POST", "/memory/create_entities", {"entities": entities})
    
    def memory_create_relations(self, relations: List[Dict]) -> Dict:
        """Create relations between entities"""
        return self._make_request("POST", "/memory/create_relations", {"relations": relations})
    
    def memory_add_observations(self, observations: List[Dict]) -> Dict:
        """Add observations to entities"""
        return self._make_request("POST", "/memory/add_observations", {"observations": observations})
    
    def memory_read_graph(self) -> Dict:
        """Read the entire knowledge graph"""
        return self._make_request("POST", "/memory/read_graph")
    
    def memory_search_nodes(self, query: str) -> Dict:
        """Search for nodes in the knowledge graph"""
        return self._make_request("POST", "/memory/search_nodes", {"query": query})
    
    def memory_open_nodes(self, names: List[str]) -> Dict:
        """Open specific nodes by name"""
        return self._make_request("POST", "/memory/open_nodes", {"names": names})

    # ===== TIME SERVER METHODS =====
    
    def time_get_current_time(self, timezone: str = "Etc/UTC") -> Dict:
        """Get current time in specified timezone"""
        return self._make_request("POST", "/time/get_current_time", {"timezone": timezone})
    
    def time_convert_time(self, source_timezone: str, time: str, target_timezone: str) -> Dict:
        """Convert time between timezones"""
        return self._make_request("POST", "/time/convert_time", {
            "source_timezone": source_timezone,
            "time": time,
            "target_timezone": target_timezone
        })

    # ===== FILESYSTEM SERVER METHODS =====
    
    def fs_list_allowed_directories(self) -> Dict:
        """List allowed directories"""
        return self._make_request("POST", "/filesystem/list_allowed_directories")
    
    def fs_read_text_file(self, path: str, head: Optional[int] = None, tail: Optional[int] = None) -> Dict:
        """Read a text file"""
        data = {"path": path}
        if head is not None:
            data["head"] = head
        if tail is not None:
            data["tail"] = tail
        return self._make_request("POST", "/filesystem/read_text_file", data)
    
    def fs_list_directory(self, path: str) -> Dict:
        """List directory contents"""
        return self._make_request("POST", "/filesystem/list_directory", {"path": path})
    
    def fs_directory_tree(self, path: str) -> Dict:
        """Get directory tree structure"""
        return self._make_request("POST", "/filesystem/directory_tree", {"path": path})

def main():
    """CLI interface for the authenticated MCP client"""
    if len(sys.argv) < 2:
        print("Usage: python3 mcp_authenticated_client.py <command> [args...]")
        print("\nAvailable commands:")
        print("  time_now [timezone]         - Get current time")
        print("  time_convert <time> <from_tz> <to_tz>  - Convert time between timezones")
        print("  fs_list_dirs               - List allowed directories")
        print("  fs_list <path>             - List directory contents")
        print("  fs_read <path>             - Read a file")
        print("  memory_graph               - Read knowledge graph")
        print("  memory_search <query>      - Search knowledge graph")
        print("\nAuthentication:")
        print("  Set MCP_API_TOKEN environment variable or create mcp_token.txt file")
        return

    try:
        client = MCPAuthenticatedClient()
        command = sys.argv[1]

        if command == "time_now":
            timezone = sys.argv[2] if len(sys.argv) > 2 else "Etc/UTC"
            result = client.time_get_current_time(timezone)
            print(json.dumps(result, indent=2))
            
        elif command == "time_convert":
            if len(sys.argv) < 5:
                print("Usage: time_convert <time> <from_tz> <to_tz>")
                return
            time, from_tz, to_tz = sys.argv[2], sys.argv[3], sys.argv[4]
            result = client.time_convert_time(from_tz, time, to_tz)
            print(json.dumps(result, indent=2))
            
        elif command == "fs_list_dirs":
            result = client.fs_list_allowed_directories()
            print(json.dumps(result, indent=2))
            
        elif command == "fs_list":
            if len(sys.argv) < 3:
                print("Usage: fs_list <path>")
                return
            path = sys.argv[2]
            result = client.fs_list_directory(path)
            print(json.dumps(result, indent=2))
            
        elif command == "fs_read":
            if len(sys.argv) < 3:
                print("Usage: fs_read <path>")
                return
            path = sys.argv[2]
            result = client.fs_read_text_file(path)
            print(json.dumps(result, indent=2))
            
        elif command == "memory_graph":
            result = client.memory_read_graph()
            print(json.dumps(result, indent=2))
            
        elif command == "memory_search":
            if len(sys.argv) < 3:
                print("Usage: memory_search <query>")
                return
            query = " ".join(sys.argv[2:])
            result = client.memory_search_nodes(query)
            print(json.dumps(result, indent=2))
            
        else:
            print(f"Unknown command: {command}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()