#!/usr/bin/env python3
"""
Test examples for MCP OpenAPI Proxy tools
"""

from mcp_authenticated_client import MCPAuthenticatedClient
import json
import time

def test_time_server():
    """Test the time server functionality"""
    print("=== TESTING TIME SERVER ===")
    client = MCPAuthenticatedClient()
    
    # Test getting current time
    print("\n1. Getting current time in UTC:")
    result = client.time_get_current_time("Etc/UTC")
    print(json.dumps(result, indent=2))
    
    # Test getting time in different timezone
    print("\n2. Getting current time in New York:")
    result = client.time_get_current_time("America/New_York")
    print(json.dumps(result, indent=2))
    
    # Test time conversion
    print("\n3. Converting 14:30 from UTC to Tokyo time:")
    result = client.time_convert_time("Etc/UTC", "14:30", "Asia/Tokyo")
    print(json.dumps(result, indent=2))

def test_filesystem_server():
    """Test the filesystem server functionality"""
    print("\n=== TESTING FILESYSTEM SERVER ===")
    client = MCPAuthenticatedClient()
    
    # Test listing allowed directories
    print("\n1. Listing allowed directories:")
    result = client.fs_list_allowed_directories()
    print(json.dumps(result, indent=2))
    
    # If we have allowed directories, test more operations
    if 'error' not in result and result:
        # Try to list the first allowed directory
        try:
            # Extract directories from the result
            if isinstance(result, list) and len(result) > 0:
                test_dir = result[0]
            elif isinstance(result, dict) and 'directories' in result:
                test_dir = result['directories'][0] if result['directories'] else None
            else:
                test_dir = "/"  # fallback
                
            if test_dir:
                print(f"\n2. Listing contents of {test_dir}:")
                result = client.fs_list_directory(test_dir)
                print(json.dumps(result, indent=2))
                
                print(f"\n3. Getting directory tree for {test_dir}:")
                result = client.fs_directory_tree(test_dir)
                print(json.dumps(result, indent=2))
                
        except Exception as e:
            print(f"Error testing filesystem operations: {e}")

def test_memory_server():
    """Test the memory server functionality"""
    print("\n=== TESTING MEMORY SERVER ===")
    client = MCPAuthenticatedClient()
    
    # Test reading the current graph
    print("\n1. Reading current knowledge graph:")
    result = client.memory_read_graph()
    print(json.dumps(result, indent=2))
    
    # Test creating some entities
    print("\n2. Creating test entities:")
    entities = [
        {
            "name": "MCP Server",
            "entityType": "Technology",
            "observations": [
                "Provides API access to tools",
                "Uses OpenAPI specification",
                "Supports multiple transport protocols"
            ]
        },
        {
            "name": "Time Tool",
            "entityType": "Feature",
            "observations": [
                "Handles timezone conversions",
                "Provides current time in any timezone"
            ]
        }
    ]
    result = client.memory_create_entities(entities)
    print(json.dumps(result, indent=2))
    
    # Test creating relations
    print("\n3. Creating relations between entities:")
    relations = [
        {
            "from": "MCP Server",
            "to": "Time Tool",
            "relationType": "provides"
        }
    ]
    result = client.memory_create_relations(relations)
    print(json.dumps(result, indent=2))
    
    # Test searching
    print("\n4. Searching for 'MCP' in knowledge graph:")
    result = client.memory_search_nodes("MCP")
    print(json.dumps(result, indent=2))
    
    # Test reading graph again to see changes
    print("\n5. Reading updated knowledge graph:")
    result = client.memory_read_graph()
    print(json.dumps(result, indent=2))

def main():
    """Run all tests"""
    try:
        test_time_server()
        test_filesystem_server()
        test_memory_server()
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()