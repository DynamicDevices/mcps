# MCP Server Configuration Notes

## Server Details

### Host Server
- **Hostname**: `ollama` (ajlennon@ollama)
- **Service Directory**: `/home/ajlennon/mcp-service/`
- **Configuration File**: `/home/ajlennon/mcp-service/mcp-config.json`

### MCP Proxy Service
- **Binary**: `/usr/bin/python /home/ajlennon/.local/bin/mcpo`
- **Host**: `0.0.0.0` (listening on all interfaces)
- **Port**: `8000`
- **API Key**: `mcp-secret-key-1754822293`
- **Config**: `--config /home/ajlennon/mcp-service/mcp-config.json`

**Full Command Line**:
```bash
/usr/bin/python /home/ajlennon/.local/bin/mcpo \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key mcp-secret-key-1754822293 \
  --config /home/ajlennon/mcp-service/mcp-config.json
```

## Current MCP Servers

### 1. Memory Server
- **Package**: `@modelcontextprotocol/server-memory`
- **Runtime**: Node.js (npx)
- **Purpose**: Knowledge graph management (entities, relations, observations)
- **Version**: Latest from npm registry

### 2. Time Server  
- **Package**: `mcp-server-time`
- **Runtime**: Python (uvx)
- **Purpose**: Timezone operations and current time retrieval
- **Version**: Latest from PyPI

### 3. Filesystem Server
- **Package**: `@modelcontextprotocol/server-filesystem`
- **Runtime**: Node.js (npx)
- **Purpose**: Secure file operations
- **Allowed Directory**: `/home/ajlennon/mcp-files`
- **Security**: Restricted to single directory for safety

## Network Access

- **Internal IP**: `192.168.0.7:8000` (accessible from client machine)
- **External Access**: Available on all interfaces (`0.0.0.0`)
- **Protocol**: HTTP with Bearer token authentication
- **Documentation**: Available at `http://192.168.0.7:8000/docs`

## Security Model

- **Authentication**: Bearer token (`mcp-secret-key-1754822293`)
- **Authorization**: API key required for all endpoints
- **File Access**: Restricted to `/home/ajlennon/mcp-files` only
- **Network**: No SSL/TLS (internal network usage)

## MCP Proxy (mcpo) Tool

The `mcpo` tool appears to be an MCP-to-OpenAPI proxy that:
1. Reads MCP server configurations
2. Starts the configured MCP servers as child processes
3. Exposes their tools as REST API endpoints
4. Provides Swagger UI documentation
5. Handles authentication via API keys

## Adding New MCP Servers

To add new MCP servers:

1. **Update Configuration**: Modify `/home/ajlennon/mcp-service/mcp-config.json`
2. **Restart Service**: Restart the mcpo service to load new configuration
3. **Update Local Copy**: Update `server_config/mcp-config.json` in this repository
4. **Test Integration**: Verify new tools are available via client

### Example: Adding a new server
```json
{
  "mcpServers": {
    "memory": { ... },
    "time": { ... },
    "filesystem": { ... },
    "new-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-new-tool"]
    }
  }
}
```

## Maintenance Notes

- **Configuration File**: Keep local copy synchronized
- **API Key**: Store securely, exclude from git
- **Service Management**: Restart mcpo when configuration changes
- **Documentation**: New servers automatically appear in Swagger UI
- **Client Updates**: May need to add new methods to Python client

## Version Tracking

- **Initial Setup**: August 10, 2025
- **MCP Servers**: 3 servers (memory, time, filesystem)
- **API Key**: mcp-secret-key-1754822293
- **Last Updated**: August 10, 2025