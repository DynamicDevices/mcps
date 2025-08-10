# Function Calling Models for Open WebUI

## Models That Actually Support Function Calling

Based on testing and research, here are models that work with Open WebUI's MCP integration:

### ✅ **Recommended for GTX 1080 Ti (11GB VRAM)**

#### **1. Hermes 3 Models** (Best Overall)
```bash
# Install the latest Hermes models with native function calling
ollama pull hermes3:8b     # ~4.7GB - Best choice
ollama pull hermes3:3b     # ~2.0GB - Lightweight option
```

**Why Hermes 3:**
- ✅ **Latest generation** with improved function calling
- ✅ **Native tool support** - no special fine-tuning needed
- ✅ **Fits comfortably** on GTX 1080 Ti
- ✅ **128K context** for complex conversations

#### **2. Hermes 2 Pro Function Calling Specialist**
```bash
# Install models specifically trained for function calling
ollama pull adrienbrault/nous-hermes2pro:Q4_0-tools    # ~3.5GB
ollama pull adrienbrault/nous-hermes2pro:Q4_0          # ~3.5GB
```

**Why Hermes 2 Pro:**
- ✅ **Specifically trained** for function calling
- ✅ **Proven to work** with Open WebUI tools integration
- ✅ **Lightweight** - fits easily on GTX 1080 Ti

#### **3. CodeLlama Function Calling**
```bash
ollama pull codellama:7b-instruct-q4_K_M    # ~4GB
```

#### **4. Alternative Models** (If Above Don't Work)
```bash
# Standard Hermes 2 models (older but reliable)
ollama pull nous-hermes2:10.7b    # ~6.1GB
```

### **4. Alternative: Use Fireworks/Together AI Models**

If local models don't work, you can configure Open WebUI to use cloud models that definitely support function calling:

#### **Fireworks AI (Pay-per-use)**
- **Model**: `accounts/fireworks/models/llama-v3p1-8b-instruct`
- **Function calling**: ✅ Native support
- **Cost**: ~$0.20/1M tokens

#### **Together AI**
- **Model**: `meta-llama/Llama-3.1-8B-Instruct-Turbo`
- **Function calling**: ✅ Native support
- **Cost**: ~$0.18/1M tokens

## Open WebUI Configuration

### **For Local Models:**
1. **Download a function-calling model**:
   ```bash
   ollama pull hermes3:8b
   # OR for lighter option:
   ollama pull adrienbrault/nous-hermes2pro:Q4_0-tools
   ```

2. **Switch to the new model** in Open WebUI

3. **Look for tools icon** (🔧) in chat interface

4. **Enable the MCP tools** you want to use

### **For Cloud Models:**
1. **Go to Settings → Models → Add Model**
2. **Add API configuration** for Fireworks/Together
3. **Select the function-calling model**
4. **Test with tools**

## Testing Function Calling

### **Test Prompt:**
```
I need you to use available tools to help me. 
Please use the get_current_time tool to tell me what time it is now.
```

### **Expected Response:**
The model should either:
- **Call the tool directly** and return the time
- **Show tool usage** in the UI with results
- **Indicate it's using external tools**

### **Wrong Response (What You're Getting):**
```
I don't have a "get_current_time" tool available...
```

## Troubleshooting Steps

### **1. Verify Tools Are Configured**
- Settings → Admin Panel → Tools → OpenAPI Servers
- Check that your MCP server shows as "Connected"
- URL: `http://192.168.0.7:8000`
- API Key: `mcp-secret-key-1754822293`

### **2. Check Open WebUI Version**
- Settings → About → Version
- **Minimum required**: v0.6.0+
- **Recommended**: v0.7.0+

### **3. Try Different Models**
If your current model doesn't work, try these in order:
1. `hermes3:8b` (best overall)
2. `adrienbrault/nous-hermes2pro:Q4_0-tools` (function calling specialist)
3. `codellama:7b-instruct-q4_K_M` (alternative)
4. Cloud model via Fireworks/Together

### **4. Browser Debugging**
- **Open Developer Tools** (F12)
- **Go to Network tab**
- **Try asking for time**
- **Look for requests** to `192.168.0.7:8000`

## Memory Usage Estimates

| Model | Quantization | Memory | Function Calling |
|-------|-------------|--------|------------------|
| Hermes 3 8B | default | ~4.7GB | ✅ Excellent |
| Hermes 3 3B | default | ~2.0GB | ✅ Good |
| Hermes 2 Pro Tools | Q4_0 | ~3.5GB | ✅ Excellent |
| CodeLlama 7B | Q4_K_M | ~4GB | ✅ Good |
| Nous Hermes 2 10.7B | default | ~6.1GB | ⚠️ Limited |
| Standard Llama 3.1 8B | Q4_K_M | ~5GB | ❌ Poor |

## Alternative: Direct MCP Python Client

If Open WebUI continues to have issues, you can always use the Python client directly:

```bash
# Get current time using your working MCP server
python3 src/mcp_authenticated_client.py time_now

# This will return something like:
# Current UTC time: 2025-08-10T12:08:35+00:00
```

This proves your MCP setup works - it's just a matter of getting Open WebUI to use it properly.