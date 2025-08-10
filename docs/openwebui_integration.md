# Configuring Open WebUI with MCP Tools

This guide shows you how to integrate your MCP OpenAPI Proxy server with Open WebUI to access Time, Memory, and Filesystem tools directly in your chat interface.

## Prerequisites

- Open WebUI version 0.6+ (MCP support was added in v0.6)
- Your MCP server running at `http://192.168.0.7:8000`
- API key: `mcp-secret-key-1754822293`

## Overview

Open WebUI integrates with MCP servers through OpenAPI endpoints. Since your server is already an MCP-to-OpenAPI proxy, it's perfectly compatible with Open WebUI's new MCP support.

## Step-by-Step Configuration

⚠️ **IMPORTANT**: MCP tools in Open WebUI must be configured with **individual paths to each service**. You cannot combine multiple MCP services into a single tool configuration. Each service (Time, Memory, Filesystem) needs to be configured separately if you want granular control, or use the proxy URL that exposes all services through a single endpoint.

### 1. Access Open WebUI Admin Settings

1. Log into Open WebUI as an administrator
2. Navigate to **Settings** → **Admin Panel** → **Tools**
3. Look for the **OpenAPI Servers** or **MCP Servers** section

### 2. Add Your MCP Server

You have two configuration options:

#### Option A: Single Proxy Configuration (Recommended)
Configure one server that provides access to all tools:

**Server Configuration:**
- **Name**: `MCP Tools (Time, Memory, Filesystem)`
- **URL**: `http://192.168.0.7:8000`
- **API Key**: `mcp-secret-key-1754822293`
- **Authentication**: Bearer Token

**Detailed Settings:**
```json
{
  "name": "MCP Tools",
  "url": "http://192.168.0.7:8000",
  "headers": {
    "Authorization": "Bearer mcp-secret-key-1754822293",
    "Content-Type": "application/json"
  },
  "enabled": true
}
```

#### Option B: Individual Service Configuration
If you need granular control, configure each service separately:

**Time Service:**
```json
{
  "name": "MCP Time Tools",
  "url": "http://192.168.0.7:8000/time",
  "headers": {
    "Authorization": "Bearer mcp-secret-key-1754822293",
    "Content-Type": "application/json"
  },
  "enabled": true
}
```

**Memory Service:**
```json
{
  "name": "MCP Memory Tools", 
  "url": "http://192.168.0.7:8000/memory",
  "headers": {
    "Authorization": "Bearer mcp-secret-key-1754822293",
    "Content-Type": "application/json"
  },
  "enabled": true
}
```

**Filesystem Service:**
```json
{
  "name": "MCP Filesystem Tools",
  "url": "http://192.168.0.7:8000/filesystem", 
  "headers": {
    "Authorization": "Bearer mcp-secret-key-1754822293",
    "Content-Type": "application/json"
  },
  "enabled": true
}
```

### 3. Test the Connection

1. Save the configuration
2. Open WebUI should automatically validate the connection
3. You should see a green checkmark if successful
4. If there's a red error, check:
   - Network connectivity to `192.168.0.7:8000`
   - API key is correct
   - Server is running

### 4. Verify Available Tools

Once connected, you should see the following tools available in Open WebUI:

**Time Server Tools:**
- `get_current_time` - Get current time in any timezone
- `convert_time` - Convert time between timezones

**Memory Server Tools:**
- `create_entities` - Create knowledge graph entities
- `create_relations` - Create relationships between entities
- `add_observations` - Add observations to entities
- `read_graph` - Read the entire knowledge graph
- `search_nodes` - Search the knowledge graph
- `open_nodes` - Retrieve specific entities
- `delete_entities` - Remove entities
- `delete_relations` - Remove relationships

**Filesystem Server Tools:**
- `list_allowed_directories` - Show accessible directories
- `read_text_file` - Read file contents
- `write_file` - Create or update files
- `list_directory` - List directory contents
- `create_directory` - Create directories
- `search_files` - Find files by pattern
- `get_file_info` - Get file metadata
- `directory_tree` - Get directory structure

## Using MCP Tools in Open WebUI

### Basic Usage

1. Start a new chat in Open WebUI
2. Look for a tools icon (🔧) in the chat interface
3. Click it to see available MCP tools
4. Select tools to enable for your conversation

### Example Prompts

**Time Operations:**
```
What time is it in Tokyo right now?
Convert 3 PM UTC to New York time.
Show me the current time in London, Tokyo, and San Francisco.
```

**Knowledge Management:**
```
Create an entity called "Project Alpha" with type "Software Project".
Search my knowledge graph for anything related to "AI".
Show me all entities in my knowledge graph.
```

**File Operations:**
```
List all files in /home/ajlennon/mcp-service/files
Read the contents of /home/ajlennon/mcp-service/files/README.md
Create a new file called /home/ajlennon/mcp-service/files/notes.txt with my meeting notes
```

⚠️ **IMPORTANT**: Always use **full paths** when working with filesystem tools. The filesystem server only allows access to `/home/ajlennon/mcp-service/files/` and will block any attempts to access parent directories.

## Advanced Configuration

### Custom Headers

If you need additional headers or custom authentication:

```json
{
  "name": "MCP Tools",
  "url": "http://192.168.0.7:8000",
  "headers": {
    "Authorization": "Bearer mcp-secret-key-1754822293",
    "Content-Type": "application/json",
    "User-Agent": "OpenWebUI-MCP-Client",
    "X-Custom-Header": "value"
  }
}
```

### Network Considerations

If Open WebUI and your MCP server are on different networks:

1. **Same Network**: Use `http://192.168.0.7:8000` (current setup)
2. **Different Networks**: May need to expose the MCP server publicly or use VPN
3. **Docker Deployments**: Use appropriate container networking

### SSL/HTTPS Setup

For production deployments, consider adding SSL:

1. Set up SSL certificate on your MCP server
2. Update URL to `https://your-domain.com:8000`
3. Ensure certificate is valid and trusted

## Troubleshooting

### Common Issues

**Connection Errors:**
- Verify MCP server is running: `curl http://192.168.0.7:8000/docs`
- Check network connectivity from Open WebUI server
- Verify API key is correct

**Authentication Failures:**
- Confirm API key: `mcp-secret-key-1754822293`
- Check Bearer token format in headers
- Test with curl: `curl -H "Authorization: Bearer mcp-secret-key-1754822293" http://192.168.0.7:8000/time/get_current_time`

**Tools Not Appearing:**
- Refresh Open WebUI page
- Check server logs for errors
- Verify OpenAPI spec is accessible: `http://192.168.0.7:8000/openapi.json`

**Tool Execution Errors:**
- Check MCP server logs
- Verify tool parameters are correct
- Test tools directly via Swagger UI: `http://192.168.0.7:8000/docs`

### Network Debugging

Test connectivity from Open WebUI server:
```bash
# Basic connectivity
curl -I http://192.168.0.7:8000

# API authentication
curl -H "Authorization: Bearer mcp-secret-key-1754822293" \
     http://192.168.0.7:8000/time/get_current_time \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"timezone": "UTC"}'
```

## Security Considerations

### API Key Management

- Store API key securely in Open WebUI configuration
- Consider rotating the API key periodically
- Monitor access logs on your MCP server

### Network Security

- Use HTTPS in production environments
- Restrict network access to MCP server if possible
- Consider VPN or private network setup for sensitive data

### File Access Security

- Filesystem server is restricted to `/home/ajlennon/mcp-files`
- Review file permissions and access controls
- Monitor file operations through server logs

## Benefits of Open WebUI + MCP Integration

### Enhanced Productivity

- **Unified Interface**: Access all tools from one chat interface
- **Natural Language**: Use conversational prompts instead of API calls
- **Context Aware**: Tools work together in conversation context

### Powerful Workflows

```
User: "Check my knowledge graph for any entities related to 'time zones', 
      then get the current time in all mentioned locations."

AI: [Uses search_nodes to find timezone entities, then get_current_time for each]
```

### Team Collaboration

- Multiple users can access the same MCP tools
- Shared knowledge graph for team information
- Collaborative file management through filesystem tools

## Next Steps

1. **Configure Open WebUI** with your MCP server
2. **Test basic functionality** with simple time queries
3. **Explore knowledge management** by creating entities and relations
4. **Set up file workflows** for document management
5. **Train your team** on using MCP tools through Open WebUI

Your MCP server is production-ready and will provide powerful AI-assisted capabilities directly through Open WebUI's intuitive chat interface!