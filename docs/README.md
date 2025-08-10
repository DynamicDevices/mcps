# MCP OpenAPI Proxy Client

This repository contains tools and configurations to connect to an MCP OpenAPI Proxy server running at `http://192.168.0.7:8000`.

## What is MCP OpenAPI Proxy?

Your server is an **MCP OpenAPI Proxy** that exposes MCP (Model Context Protocol) tools as REST API endpoints. It provides access to three powerful tool sets:

### Available Tools:

1. **Memory Server** (`memory-server` v0.6.3)
   - Knowledge graph with entities, relations, and observations
   - Create, search, and manage knowledge structures
   - Perfect for building AI memory systems

2. **Time Server** (`mcp-time` v1.12.4) 
   - Get current time in any timezone
   - Convert times between timezones
   - Handles IANA timezone names

3. **Filesystem Server** (`secure-filesystem-server` v0.2.0)
   - Read, write, and manage files
   - List directories and search files
   - Security-restricted file operations

## Quick Start

### 1. Test the Connection
```bash
python3 test_mcp_connection.py
```

### 2. Use the Python Client
```bash
# Get current time
python3 mcp_proxy_client.py time_now "America/New_York"

# List allowed directories
python3 mcp_proxy_client.py fs_list_dirs

# Search knowledge graph
python3 mcp_proxy_client.py memory_search "technology"
```

### 3. Run Full Test Suite
```bash
python3 test_mcp_tools.py
```

## Python Client Usage

```python
from mcp_proxy_client import MCPProxyClient

client = MCPProxyClient("http://192.168.0.7:8000")

# Time operations
time_result = client.time_get_current_time("Europe/London")
convert_result = client.time_convert_time("UTC", "14:30", "Asia/Tokyo")

# Memory operations
graph = client.memory_read_graph()
search_results = client.memory_search_nodes("AI")

# Filesystem operations
directories = client.fs_list_allowed_directories()
files = client.fs_list_directory("/some/path")
```

## Configuration for MCP Clients

Since this is an OpenAPI proxy rather than a traditional MCP server, you'll need to create custom integrations for MCP clients like Claude Desktop or Cline. The JSON configuration files provided are templates for reference.

### For Direct HTTP Integration:
Use the Python client (`mcp_proxy_client.py`) or create HTTP requests directly to:
- `http://192.168.0.7:8000/memory/*` - Memory operations
- `http://192.168.0.7:8000/time/*` - Time operations  
- `http://192.168.0.7:8000/filesystem/*` - File operations

## API Documentation

Visit these URLs in your browser for interactive API documentation:
- **Main docs**: http://192.168.0.7:8000/docs
- **Memory tools**: http://192.168.0.7:8000/memory/docs
- **Time tools**: http://192.168.0.7:8000/time/docs
- **Filesystem tools**: http://192.168.0.7:8000/filesystem/docs

## Authentication

**⚠️ IMPORTANT**: This server requires authentication via Bearer token.

### Setup Authentication

Run the setup helper:
```bash
python3 setup_auth.py
```

Or manually set up authentication using one of these methods:

#### Method 1: Environment Variable (Recommended)
```bash
export MCP_API_TOKEN="your-actual-token-here"
python3 mcp_authenticated_client.py time_now
```

#### Method 2: Token File
```bash
echo "your-actual-token-here" > mcp_token.txt
python3 mcp_authenticated_client.py time_now
```

#### Method 3: Config File
Edit `auth_config_template.json` and replace `YOUR_TOKEN_HERE` with your actual token.

### Getting Your Token
Contact the server administrator for your API token. The server expects:
- **Format**: `Authorization: Bearer <token>`
- **Required for**: All tool endpoints (memory, time, filesystem)

### Using the Authenticated Client
```python
from mcp_authenticated_client import MCPAuthenticatedClient

# Token from environment variable or file
client = MCPAuthenticatedClient()

# Or pass token directly
client = MCPAuthenticatedClient(token="your-token-here")
```

## Example Use Cases

### Knowledge Management
```python
# Create entities and relations in the knowledge graph
client.memory_create_entities([{
    "name": "Python",
    "entityType": "Programming Language", 
    "observations": ["Object-oriented", "Interpreted", "Popular for AI"]
}])

# Search and explore the graph
results = client.memory_search_nodes("programming")
```

### Time Zone Handling
```python
# Get current time in multiple zones
utc_time = client.time_get_current_time("UTC")
local_time = client.time_get_current_time("America/Los_Angeles")

# Convert meeting times
meeting_time = client.time_convert_time("America/New_York", "15:00", "Europe/London")
```

### File Operations
```python
# Explore filesystem
allowed_dirs = client.fs_list_allowed_directories()
file_tree = client.fs_directory_tree("/workspace")

# Read and write files
content = client.fs_read_text_file("/path/to/file.txt")
client.fs_write_file("/path/to/output.txt", "Hello, World!")
```

## Troubleshooting

1. **Connection Issues**: Verify the server is running at `192.168.0.7:8000`
2. **Permission Errors**: Check if filesystem operations are within allowed directories
3. **Authentication**: Add Bearer tokens if endpoints require authentication
4. **API Errors**: Check the interactive docs for correct request formats