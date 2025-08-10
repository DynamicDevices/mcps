# Troubleshooting Open WebUI MCP Integration

## Common Issue: Tools Not Being Used

If your model responds like a standard LLM without using the MCP tools (like saying "I don't have real-time access"), here are the solutions:

### 1. Check Tool Visibility in Chat

**Look for the Tools Icon:**
- In the chat interface, look for a tools/plugin icon (🔧 or similar)
- It should appear near the message input box
- Click it to see if your MCP tools are listed

**If No Tools Icon Appears:**
- The server connection failed
- Check the configuration in Admin → Tools → OpenAPI Servers
- Verify the server shows as "Connected" or has a green status

### 2. Enable Tools for the Conversation

**Method 1: Tool Selection**
1. Click the tools icon (🔧) in the chat interface
2. You should see categories like:
   - **Time Server** (get_current_time, convert_time)
   - **Memory Server** (create_entities, search_nodes, etc.)
   - **Filesystem Server** (read_file, list_directory, etc.)
3. **Enable/select the tools** you want to use
4. Try your question again

**Method 2: Explicit Tool Request**
Instead of "What time is it now?", try:
```
Use the get_current_time tool to tell me what time it is now in UTC.
```

### 3. Check Open WebUI Configuration

**Verify Server Settings:**
1. Go to **Settings** → **Admin Panel** → **Tools**
2. Find your MCP server entry
3. Check that it shows:
   - ✅ **Status**: Connected/Active
   - ✅ **URL**: `http://192.168.0.7:8000`
   - ✅ **Authentication**: Working

**Common Configuration Issues:**

**Wrong URL Format:**
```bash
# Wrong - missing http://
192.168.0.7:8000

# Correct
http://192.168.0.7:8000
```

**Authentication Problems:**
```json
// Wrong - missing Bearer prefix
"Authorization": "mcp-secret-key-1754822293"

// Correct
"Authorization": "Bearer mcp-secret-key-1754822293"
```

**⚠️ Service Path Configuration:**
- **IMPORTANT**: MCP tools must be configured with individual paths to each service
- You cannot combine multiple MCP services into a single tool configuration
- Choose one approach:
  
  **Option A - Single Proxy (Recommended):**
  ```
  URL: http://192.168.0.7:8000
  ```
  
  **Option B - Individual Services:**
  ```
  Time Service:       http://192.168.0.7:8000/time
  Memory Service:     http://192.168.0.7:8000/memory
  Filesystem Service: http://192.168.0.7:8000/filesystem
  ```

### 4. Model Selection Issues

**Check Your Model:**
- Some models work better with tools than others
- Try with a different model (GPT-4, Claude, etc.)
- Make sure the model supports function calling

**Model-Specific Settings:**
- Look for "Tools" or "Function Calling" settings in the model configuration
- Ensure tools are enabled for the selected model

### 5. Network Connectivity Issues

**Test from Open WebUI Server:**
If Open WebUI is running on a different machine than your MCP server:

```bash
# Test from the Open WebUI server machine
curl -H "Authorization: Bearer mcp-secret-key-1754822293" \
     http://192.168.0.7:8000/time/get_current_time \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"timezone": "UTC"}'
```

**Docker Network Issues:**
If Open WebUI is in Docker, it might not be able to reach `192.168.0.7:8000`:
- Use the host machine's IP instead of localhost
- Consider using `host.docker.internal` on some Docker setups
- Check Docker network configuration

### 6. Open WebUI Version Check

**Ensure Correct Version:**
- MCP support requires **Open WebUI v0.6+**
- Check: Settings → About → Version
- Update if necessary

### 7. Browser/Cache Issues

**Clear Cache:**
1. Hard refresh the Open WebUI page (Ctrl+F5)
2. Clear browser cache
3. Try in an incognito/private window
4. Check browser console for JavaScript errors

### 8. Configuration File Method

If the UI configuration isn't working, try direct configuration:

**For Docker Deployments:**
Add environment variables:
```yaml
environment:
  - OPENAPI_SERVERS='[{"name":"MCP Tools","url":"http://192.168.0.7:8000","headers":{"Authorization":"Bearer mcp-secret-key-1754822293"}}]'
```

**For Manual Deployments:**
Check if there's a configuration file you can edit directly.

### 9. Debug Steps

**Step 1: Verify Connection in UI**
1. Go to Admin → Tools → OpenAPI Servers
2. Edit your MCP server entry
3. Save it again (this forces a connection test)
4. Look for error messages

**Step 2: Check Browser Network Tab**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try asking for time again
4. Look for failed requests to your MCP server

**Step 3: Test with Curl**
```bash
# Test OpenAPI spec access
curl http://192.168.0.7:8000/openapi.json

# Test authenticated tool call
curl -H "Authorization: Bearer mcp-secret-key-1754822293" \
     http://192.168.0.7:8000/time/get_current_time \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"timezone": "UTC"}'
```

### 10. Alternative Configuration

**Try Different URL Formats:**
```
http://192.168.0.7:8000           # Base URL
http://192.168.0.7:8000/          # With trailing slash
http://192.168.0.7:8000/api       # Different path
```

**Try Without Custom Headers:**
Sometimes simpler is better:
```json
{
  "name": "MCP Tools",
  "url": "http://192.168.0.7:8000",
  "headers": {
    "Authorization": "Bearer mcp-secret-key-1754822293"
  }
}
```

## Quick Fix Checklist

- [ ] Tools icon (🔧) visible in chat?
- [ ] Tools enabled/selected for conversation?
- [ ] Server shows "Connected" status?
- [ ] Correct URL: `http://192.168.0.7:8000`?
- [ ] Correct API key: `mcp-secret-key-1754822293`?
- [ ] Open WebUI version 0.6+?
- [ ] Tried hard refresh (Ctrl+F5)?
- [ ] Network connectivity working?
- [ ] Tried explicit tool request?

## Test Prompts

Once configured properly, try these specific prompts:

```
Use the time tools to tell me what time it is now in UTC.

Use the get_current_time tool to show me the current time in Tokyo.

Use the memory tools to create an entity called "Test Entity".

Use the filesystem tools to list my allowed directories.
```

## Still Not Working?

If none of the above works:

1. **Check Open WebUI logs** for error messages
2. **Check your MCP server logs** on the `ollama` machine
3. **Try a different model** in Open WebUI
4. **Consider using the Python client directly** as a workaround
5. **Contact Open WebUI support** with your configuration details

## Workaround: Direct Python Client

While debugging, you can still use the MCP tools directly:

```bash
# Get current time
python3 src/mcp_authenticated_client.py time_now

# Get time in specific timezone  
python3 src/mcp_authenticated_client.py time_now "Asia/Tokyo"

# Convert time
python3 src/mcp_authenticated_client.py time_convert "15:00" "UTC" "America/New_York"
```

This ensures your MCP server is working while you fix the Open WebUI integration.