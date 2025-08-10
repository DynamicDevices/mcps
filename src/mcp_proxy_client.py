#!/usr/bin/env python3
"""
MCP OpenAPI Proxy Client
A client for interacting with the MCP OpenAPI Proxy at http://192.168.0.7:8000
"""

import requests
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

class MCPProxyClient:
    """Client for interacting with MCP OpenAPI Proxy"""
    
    def __init__(self, base_url: str = "http://192.168.0.7:8000", token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Set up authentication if token is provided
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "MCP-Proxy-Client/1.0"
        })

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request to the proxy"""
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
    
    def memory_delete_entities(self, entity_names: List[str]) -> Dict:
        """Delete entities from the knowledge graph"""
        return self._make_request("POST", "/memory/delete_entities", {"entityNames": entity_names})

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
    
    def fs_write_file(self, path: str, content: str) -> Dict:
        """Write content to a file"""
        return self._make_request("POST", "/filesystem/write_file", {"path": path, "content": content})
    
    def fs_list_directory(self, path: str) -> Dict:
        """List directory contents"""
        return self._make_request("POST", "/filesystem/list_directory", {"path": path})
    
    def fs_list_directory_with_sizes(self, path: str, sort_by: str = "name") -> Dict:
        """List directory contents with sizes"""
        return self._make_request("POST", "/filesystem/list_directory_with_sizes", {"path": path, "sortBy": sort_by})
    
    def fs_create_directory(self, path: str) -> Dict:
        """Create a directory"""
        return self._make_request("POST", "/filesystem/create_directory", {"path": path})
    
    def fs_search_files(self, path: str, pattern: str, exclude_patterns: List[str] = None) -> Dict:
        """Search for files"""
        data = {"path": path, "pattern": pattern}
        if exclude_patterns:
            data["excludePatterns"] = exclude_patterns
        return self._make_request("POST", "/filesystem/search_files", data)
    
    def fs_get_file_info(self, path: str) -> Dict:
        """Get file information"""
        return self._make_request("POST", "/filesystem/get_file_info", {"path": path})
    
    def fs_directory_tree(self, path: str) -> Dict:
        """Get directory tree structure"""
        return self._make_request("POST", "/filesystem/directory_tree", {"path": path})

def main():
    """CLI interface for the MCP Proxy Client"""
    if len(sys.argv) < 2:
        print("Usage: python3 mcp_proxy_client.py <command> [args...]")
        print("\nAvailable commands:")
        print("  time_now [timezone]         - Get current time")
        print("  time_convert <time> <from_tz> <to_tz>  - Convert time between timezones")
        print("  fs_list_dirs               - List allowed directories")
        print("  fs_list <path>             - List directory contents")
        print("  fs_read <path>             - Read a file")
        print("  memory_graph               - Read knowledge graph")
        print("  memory_search <query>      - Search knowledge graph")
        return

    client = MCPProxyClient()
    command = sys.argv[1]

    try:
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
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()