# MCP Server Configuration Management

This directory contains tools and documentation for managing the MCP server configuration.

## Files

### Configuration Files
- **`mcp-config.json`** - Local copy of the server configuration
- **`server_notes.md`** - Detailed documentation of the server setup

### Management Tools
- **`sync_config.py`** - Tool to sync configuration from remote server
- **`README.md`** - This documentation file

## Server Setup Summary

### Current Configuration
- **Host**: `ajlennon@ollama` (192.168.0.7:8000)
- **Service**: MCP Proxy (`mcpo`) exposing 3 MCP servers via REST API
- **Authentication**: Bearer token (`mcp-secret-key-1754822293`)

### Active MCP Servers
1. **Memory Server** - Knowledge graph management (Node.js/npx)
2. **Time Server** - Timezone operations (Python/uvx)  
3. **Filesystem Server** - File operations in `/home/ajlennon/mcp-files` (Node.js/npx)

## Usage

### Sync Configuration from Remote
```bash
python3 server_config/sync_config.py sync
```

### List Current Servers
```bash
python3 server_config/sync_config.py list
```

### Check Service Status
```bash
python3 server_config/sync_config.py status
```

## Adding New MCP Servers

### 1. Update Remote Configuration
SSH to the server and edit the configuration:
```bash
ssh ajlennon@ollama
nano /home/ajlennon/mcp-service/mcp-config.json
```

Add your new server:
```json
{
  "mcpServers": {
    "memory": { ... },
    "time": { ... },
    "filesystem": { ... },
    "new-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-package"]
    }
  }
}
```

### 2. Restart MCP Service
Restart the mcpo service to load the new configuration:
```bash
# Stop the service (method depends on how it's managed)
sudo systemctl restart mcp-proxy
# or kill and restart the process
```

### 3. Sync Local Configuration
Update your local copy:
```bash
python3 server_config/sync_config.py sync
```

### 4. Update Client (if needed)
If the new server provides novel functionality, you may need to add new methods to the Python client in `src/mcp_authenticated_client.py`.

### 5. Test Integration
Verify the new server is working:
```bash
# Check service status
python3 server_config/sync_config.py status

# Test client functionality
python3 src/mcp_authenticated_client.py <new-command>
```

## Configuration Management

### Remote Server Details
- **Config Path**: `/home/ajlennon/mcp-service/mcp-config.json`
- **Service Command**: 
  ```bash
  /usr/bin/python /home/ajlennon/.local/bin/mcpo \
    --host 0.0.0.0 --port 8000 \
    --api-key mcp-secret-key-1754822293 \
    --config /home/ajlennon/mcp-service/mcp-config.json
  ```

### Local Management
- Keep local configuration synchronized with remote
- Document changes in `server_notes.md`
- Update client code when new servers are added
- Test functionality after configuration changes

## Troubleshooting

### Configuration Sync Issues
- Verify SSH access to `ajlennon@ollama`
- Check remote file permissions
- Ensure JSON syntax is valid

### Service Issues
- Check if mcpo process is running: `ps aux | grep mcpo`
- Verify service accessibility: `curl http://192.168.0.7:8000/docs`
- Check server logs for error messages

### Client Issues
- Verify API token is still valid
- Check network connectivity to 192.168.0.7:8000
- Test with basic endpoints first (time server)

## Security Notes

- The API key (`mcp-secret-key-1754822293`) is stored in the local token file
- Configuration files don't contain sensitive data
- Remote server restricts filesystem access to `/home/ajlennon/mcp-files`
- Service runs on internal network (no external SSL/TLS required)