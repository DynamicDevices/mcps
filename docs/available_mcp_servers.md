# Available MCP Servers

This guide shows you the MCP servers you can add to your existing setup. Each server adds specific capabilities to your AI assistant through Open WebUI.

## Currently Configured
✅ **Memory Server** - Knowledge graph management  
✅ **Time Server** - Time zone operations  
✅ **Filesystem Server** - File operations (restricted to `/home/ajlennon/mcp-service/files`)

## Popular MCP Servers to Add

### 🌐 **Web & Data Access**

#### **Fetch Server** (Web Scraping)
```json
"fetch": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-fetch"]
}
```
**Capabilities:** Download web pages, access APIs, fetch remote content

#### **Brave Search Server**
```json
"brave-search": {
  "command": "npx", 
  "args": ["-y", "@modelcontextprotocol/server-brave-search"]
}
```
**Capabilities:** Web search, news search, image search  
**Requires:** Brave Search API key

#### **Puppeteer Server** (Browser Automation)
```json
"puppeteer": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}
```
**Capabilities:** Web scraping, screenshot capture, form automation

### 🔗 **Development & APIs**

#### **GitHub Server**
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"]
}
```
**Capabilities:** Repository management, issue tracking, code review  
**Requires:** GitHub token

#### **GitLab Server** 
```json
"gitlab": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gitlab"]
}
```
**Capabilities:** GitLab project management, merge requests, CI/CD  
**Requires:** GitLab token

#### **Postman Server**
```json
"postman": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postman"]
}
```
**Capabilities:** API testing, collection management  
**Requires:** Postman API key

### 🗄️ **Database Servers**

#### **SQLite Server**
```json
"sqlite": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
}
```
**Capabilities:** SQL queries, database management, data analysis

#### **PostgreSQL Server**
```json
"postgresql": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgresql"]
}
```
**Capabilities:** Advanced SQL operations, complex queries  
**Requires:** PostgreSQL connection string

### ☁️ **Cloud Services**

#### **Google Drive Server**
```json
"google-drive": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-google-drive"]
}
```
**Capabilities:** File management, document access, sharing  
**Requires:** Google API credentials

#### **AWS Server**
```json
"aws": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-aws"]
}
```
**Capabilities:** EC2, S3, Lambda management  
**Requires:** AWS credentials

#### **Azure Server**
```json
"azure": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-azure"]
}
```
**Capabilities:** Azure resource management, storage, analytics  
**Requires:** Azure credentials

### 💬 **Communication**

#### **Slack Server**
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"]
}
```
**Capabilities:** Send messages, read channels, manage workspaces  
**Requires:** Slack bot token

#### **Discord Server**
```json
"discord": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-discord"]
}
```
**Capabilities:** Discord bot functionality, channel management  
**Requires:** Discord bot token

### 💰 **Finance & Trading**

#### **AlphaVantage Server** (Stock Data)
```json
"alphavantage": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-alphavantage"]
}
```
**Capabilities:** Stock prices, financial data, market analysis  
**Requires:** AlphaVantage API key

#### **Stripe Server**
```json
"stripe": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-stripe"]
}
```
**Capabilities:** Payment processing, customer management  
**Requires:** Stripe API key

### 🤖 **AI Services**

#### **OpenAI Server**
```json
"openai": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-openai"]
}
```
**Capabilities:** GPT models, image generation, embeddings  
**Requires:** OpenAI API key

#### **Hugging Face Server**
```json
"huggingface": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-huggingface"]
}
```
**Capabilities:** Model inference, dataset access  
**Requires:** Hugging Face token

### 📊 **Specialized Tools**

#### **Figma Server**
```json
"figma": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-figma"]
}
```
**Capabilities:** Design file access, component extraction  
**Requires:** Figma token

#### **Auth0 Server**
```json
"auth0": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-auth0"]
}
```
**Capabilities:** User management, authentication flows  
**Requires:** Auth0 credentials

## How to Add New Servers

### 1. **Choose a Server** from the list above

### 2. **Update Server Configuration**
Edit `/home/ajlennon/mcp-service/mcp-config.json` on your server:

```json
{
  "mcpServers": {
    "memory": { ... existing ... },
    "time": { ... existing ... },
    "filesystem": { ... existing ... },
    "NEW-SERVER-NAME": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-NEW-SERVER"]
    }
  }
}
```

### 3. **Add Required Credentials** (if needed)
Some servers need API keys or tokens. Add them as environment variables:

```bash
# On your server (ollama):
export GITHUB_TOKEN="your-token-here"
export BRAVE_API_KEY="your-key-here"
# etc.
```

### 4. **Restart the MCP Proxy**
```bash
# On your server (ollama):
sudo systemctl restart mcp-proxy
# OR
pkill -f mcpo
/usr/bin/python /home/ajlennon/.local/bin/mcpo --host 0.0.0.0 --port 8000 --api-key mcp-secret-key-1754822293 --config /home/ajlennon/mcp-service/mcp-config.json
```

### 5. **Update Local Configuration**
Update your local copy in `server_config/mcp-config.json`

### 6. **Test in Open WebUI**
The new tools should appear automatically in Open WebUI's tools menu

## Recommended Next Additions

Based on your current setup, I recommend adding these first:

### **🌐 Fetch Server** (Easy to set up, no API key needed)
- Web scraping and API access
- Perfect for research and data gathering

### **📊 SQLite Server** (Local database, no external dependencies)
- Local data storage and analysis
- Great for structured data management

### **🔍 Brave Search Server** (Requires free API key)
- Web search capabilities
- Enhances research and information gathering

### **💻 GitHub Server** (If you use GitHub)
- Code repository management
- Issue tracking and project management

## Security Considerations

- **API Keys**: Store securely, never commit to git
- **Network Access**: Some servers need internet access
- **Rate Limits**: Be aware of API quotas and limits
- **Permissions**: Review what each server can access

## Advanced: Custom MCP Servers

You can also create custom MCP servers for:
- Internal company APIs
- Proprietary databases
- Custom business logic
- Specialized integrations

## Need Help?

1. **Check server documentation** for specific setup requirements
2. **Test individual servers** before adding to production
3. **Monitor logs** when adding new servers
4. **Start simple** - add one server at a time

Choose the servers that best fit your workflow and start with the simpler ones!
