# MCP OpenAPI Proxy Client

A comprehensive Python client for connecting to MCP (Model Context Protocol) OpenAPI Proxy servers.

## Overview

This project provides tools and utilities to connect to and interact with MCP OpenAPI Proxy servers that expose MCP tools as REST API endpoints. It includes authenticated clients, testing utilities, and configuration templates.

## Features

- **🔐 Secure Authentication**: Bearer token authentication with multiple configuration options
- **⏰ Time Operations**: Current time retrieval and timezone conversions
- **🧠 Knowledge Graph**: Create and manage entities, relations, and observations
- **📁 Filesystem Operations**: Secure file reading, writing, and directory management
- **🧪 Comprehensive Testing**: Full test suite with authentication
- **📚 Documentation**: Complete setup guides and API documentation

## Quick Start

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Set Up Authentication
```bash
# Option A: Environment variable (recommended)
export MCP_API_TOKEN="your-api-token"

# Option B: Token file
echo "your-api-token" > mcp_token.txt

# Option C: Interactive setup
python3 examples/setup_auth.py
```

### 3. Test Connection
```bash
python3 src/mcp_authenticated_client.py time_now
```

## Project Structure

```
mcps/
├── src/                          # Main source code
│   ├── mcp_authenticated_client.py    # Full-featured authenticated client
│   └── mcp_proxy_client.py           # Basic client (no auth)
├── tests/                        # Test files
│   ├── test_mcp_tools.py             # Comprehensive tool tests
│   ├── test_mcp_connection.py        # Basic connection tests
│   └── auth_helper.py                # Authentication discovery
├── config/                       # Configuration templates
│   ├── auth_config_template.json     # Authentication template
│   ├── claude_desktop_config.json    # Claude Desktop config
│   ├── cline_mcp_settings.json       # VS Code/Cline config
│   └── mcp_client_config.json        # Generic MCP client config
├── server_config/                # Server configuration management
│   ├── mcp-config.json               # Local copy of server config
│   ├── server_notes.md               # Server setup documentation
│   ├── sync_config.py                # Configuration sync tool
│   └── README.md                     # Server management guide
├── examples/                     # Example scripts
│   └── setup_auth.py                 # Interactive auth setup
├── docs/                         # Documentation
│   ├── README.md                     # Detailed usage guide
│   ├── SETUP_COMPLETE.md             # Complete setup documentation
│   └── SUCCESS_SUMMARY.md            # Success summary with examples
└── .gitignore                    # Git ignore file (excludes tokens)
```

## Authentication

This client supports multiple authentication methods:

1. **Environment Variable** (Recommended)
   ```bash
   export MCP_API_TOKEN="your-token"
   ```

2. **Token File**
   ```bash
   echo "your-token" > mcp_token.txt
   ```

3. **Configuration File**
   Edit `config/auth_config_template.json` with your token

4. **Direct Parameter**
   ```python
   client = MCPAuthenticatedClient(token="your-token")
   ```

## Usage Examples

### Command Line Interface
```bash
# Time operations
python3 src/mcp_authenticated_client.py time_now "Europe/London"
python3 src/mcp_authenticated_client.py time_convert "15:00" "UTC" "Asia/Tokyo"

# Filesystem operations
python3 src/mcp_authenticated_client.py fs_list_dirs
python3 src/mcp_authenticated_client.py fs_list "/allowed/directory"

# Memory operations
python3 src/mcp_authenticated_client.py memory_graph
python3 src/mcp_authenticated_client.py memory_search "technology"
```

### Python Integration
```python
from src.mcp_authenticated_client import MCPAuthenticatedClient

client = MCPAuthenticatedClient()

# Time operations
time_nyc = client.time_get_current_time("America/New_York")
conversion = client.time_convert_time("UTC", "14:30", "Asia/Tokyo")

# Memory operations
graph = client.memory_read_graph()
client.memory_create_entities([{
    "name": "Python",
    "entityType": "Programming Language",
    "observations": ["Object-oriented", "Popular for AI"]
}])

# Filesystem operations
directories = client.fs_list_allowed_directories()
content = client.fs_read_text_file("/path/to/file.txt")
```

## Adding More MCP Servers

Your setup currently includes **Memory**, **Time**, and **Filesystem** servers. You can add many more:

### 🚀 **Quick Server Addition**
```bash
# List available servers
python3 scripts/add_mcp_server.py list

# Add a new server (example: web scraping)
python3 scripts/add_mcp_server.py fetch

# Add GitHub integration  
python3 scripts/add_mcp_server.py github
```

### 📋 **Popular Server Options**
- **🌐 Web & APIs**: `fetch`, `brave-search`, `puppeteer`
- **💻 Development**: `github`, `gitlab`, `postman`  
- **🗄️ Databases**: `sqlite`, `postgresql`
- **☁️ Cloud**: `google-drive`, `aws`, `azure`
- **💬 Communication**: `slack`, `discord`
- **💰 Finance**: `alphavantage`, `stripe`

See `docs/available_mcp_servers.md` for complete list and setup instructions.

## Server Configuration Management

### Sync Configuration from Remote Server
```bash
python3 server_config/sync_config.py sync    # Sync from remote
python3 server_config/sync_config.py list    # List current servers
python3 server_config/sync_config.py status  # Check service status
```

### Server Details
- **Host**: `ajlennon@ollama` (192.168.0.7:8000)
- **Active Servers**: Memory, Time, Filesystem (3 servers)
- **Configuration**: `/home/ajlennon/mcp-service/mcp-config.json`
- **Service**: MCP Proxy (`mcpo`) with REST API exposure

## Testing

Run the comprehensive test suite:
```bash
python3 tests/test_mcp_tools.py
```

Test specific components:
```bash
python3 tests/test_mcp_connection.py     # Basic connectivity
python3 tests/auth_helper.py             # Authentication discovery
```

## Configuration

Template configuration files are provided in the `config/` directory for various MCP clients:

- **Claude Desktop**: `config/claude_desktop_config.json`
- **VS Code/Cline**: `config/cline_mcp_settings.json`
- **Generic**: `config/mcp_client_config.json`

## Security

- **Token Protection**: All sensitive tokens are excluded from git via `.gitignore`
- **Multiple Auth Methods**: Flexible authentication options for different environments
- **Secure Defaults**: Environment variables recommended for production use

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- `docs/README.md` - Detailed usage guide
- `docs/SETUP_COMPLETE.md` - Complete setup instructions
- `docs/SUCCESS_SUMMARY.md` - Success summary with examples

## Requirements

- Python 3.6+
- `requests` library
- MCP OpenAPI Proxy server with Bearer token authentication

## License

This project is provided as-is for connecting to MCP OpenAPI Proxy servers.

## Contributing

This is a client implementation for a specific MCP OpenAPI Proxy server. Contributions welcome for additional features and improvements.