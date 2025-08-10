# Setting Up OpenSCAD MCP Server

This guide shows you how to add 3D modeling and CAD capabilities to your MCP setup using the OpenSCAD MCP server.

## What You'll Get

The OpenSCAD MCP server provides:
- **3D Model Generation** from text descriptions
- **OpenSCAD Code Rendering** to images and STL files  
- **Parametric 3D Modeling** capabilities
- **Multi-view Reconstruction** (optional with CUDA)
- **Integration with AI models** for automated 3D design

## Prerequisites

### 1. System Requirements
- **Python 3.8+** (already have this)
- **OpenSCAD binary** installed on your server
- **Git** for repository cloning
- **Optional**: CUDA-capable GPU for advanced features

### 2. Install OpenSCAD on Your Server

**On Ubuntu/Debian (your ollama server):**
```bash
# Connect to your server
ssh ajlennon@192.168.0.7

# Install OpenSCAD
sudo apt-get update
sudo apt-get install openscad

# Verify installation
openscad --version
```

**Alternative methods:**
- **Snap**: `sudo snap install openscad`
- **Manual**: Download from [openscad.org](https://openscad.org/downloads.html)

## Installation Steps

### 1. Clone the OpenSCAD MCP Server

```bash
# On your server (192.168.0.7)
ssh ajlennon@192.168.0.7

# Navigate to your MCP directory
cd /home/ajlennon/mcp-service

# Clone the repository
git clone https://github.com/jhacksman/OpenSCAD-MCP-Server.git
cd OpenSCAD-MCP-Server
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)

Some features require API keys. Create a `.env` file:

```bash
# Create environment file
nano .env

# Add these lines (optional for basic OpenSCAD rendering):
GEMINI_API_KEY=your-gemini-api-key  # For AI-generated models
VENICE_API_KEY=your-venice-api-key  # Alternative AI service
REMOTE_CUDA_MVS_API_KEY=your-key    # For remote 3D reconstruction
```

**Note**: For basic OpenSCAD code rendering, these API keys are **optional**.

### 4. Test the Installation

```bash
# Test OpenSCAD directly
openscad --version

# Test the MCP server
python src/main.py --help
```

### 5. Add to MCP Configuration

Update your MCP configuration to include the OpenSCAD server:

```bash
# Edit your MCP config
nano /home/ajlennon/mcp-service/mcp-config.json
```

Add this server configuration:

```json
{
  "mcpServers": {
    "memory": { ... existing ... },
    "time": { ... existing ... },
    "filesystem": { ... existing ... },
    "fetch": { ... existing ... },
    "openscad": {
      "command": "python",
      "args": ["/home/ajlennon/mcp-service/OpenSCAD-MCP-Server/src/main.py"],
      "env": {
        "VIRTUAL_ENV": "/home/ajlennon/mcp-service/OpenSCAD-MCP-Server/venv"
      }
    }
  }
}
```

### 6. Restart MCP Proxy

```bash
# Restart the MCP proxy service
sudo systemctl restart mcp-proxy

# OR restart manually:
pkill -f mcpo
/usr/bin/python /home/ajlennon/.local/bin/mcpo --host 0.0.0.0 --port 8000 --api-key mcp-secret-key-1754822293 --config /home/ajlennon/mcp-service/mcp-config.json
```

## Testing the OpenSCAD Server

### 1. Basic OpenSCAD Code Rendering

```bash
# Test with curl
curl -X POST "http://192.168.0.7:8000/openscad/render" \
  -H "Authorization: Bearer mcp-secret-key-1754822293" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "cube([10, 10, 10]);",
    "output_format": "png"
  }'
```

### 2. Generate STL File

```bash
curl -X POST "http://192.168.0.7:8000/openscad/generate_stl" \
  -H "Authorization: Bearer mcp-secret-key-1754822293" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "difference() { cube([20, 20, 20]); sphere(10); }",
    "filename": "hollow_cube.stl"
  }'
```

## Using in Open WebUI

Once set up, you can ask your AI assistant to:

### 📐 **3D Modeling Examples**

```
"Create an OpenSCAD model of a gear with 20 teeth and render it as an image"

"Generate OpenSCAD code for a phone case and export it as an STL file"

"Design a parametric bracket in OpenSCAD with adjustable dimensions"

"Create a complex 3D printed part with holes and mounting points"
```

### 🔧 **CAD Operations**

```
"Modify this OpenSCAD code to make the object 50% larger"

"Create a hollow version of this solid 3D model"

"Generate technical drawings from this OpenSCAD model"

"Optimize this design for 3D printing"
```

## Features and Capabilities

### ✅ **Basic Features**
- OpenSCAD code execution and rendering
- PNG/JPEG image generation from 3D models
- STL file export for 3D printing
- Parametric model generation
- Code validation and error reporting

### 🚀 **Advanced Features** (with API keys)
- AI-generated 3D models from text descriptions
- Multi-view 3D reconstruction
- Automatic parametric design
- Style transfer for 3D models

### 🔧 **Technical Specs**
- **Input Formats**: OpenSCAD code (.scad), text descriptions
- **Output Formats**: PNG, JPEG, STL, SCAD
- **Rendering Engine**: OpenSCAD native renderer
- **Max Model Complexity**: Limited by server resources

## Troubleshooting

### Common Issues

**❌ "OpenSCAD not found"**
```bash
# Check if OpenSCAD is installed
which openscad
sudo apt-get install openscad
```

**❌ "Permission denied"**
```bash
# Make sure scripts are executable
chmod +x /home/ajlennon/mcp-service/OpenSCAD-MCP-Server/src/main.py
```

**❌ "Module not found"**
```bash
# Activate virtual environment
cd /home/ajlennon/mcp-service/OpenSCAD-MCP-Server
source venv/bin/activate
pip install -r requirements.txt
```

**❌ "Rendering failed"**
- Check OpenSCAD code syntax
- Verify server has sufficient memory
- Check OpenSCAD error logs

### Performance Tips

1. **Optimize Models**: Keep complexity reasonable for web rendering
2. **Resource Limits**: Set timeout limits for complex renders
3. **Caching**: Enable result caching for repeated operations
4. **Parallel Processing**: Use multiple workers for batch operations

## Security Considerations

⚠️ **Important Security Notes:**

1. **Code Execution**: OpenSCAD executes arbitrary code - restrict access
2. **File System**: Limit output directory permissions
3. **Resource Limits**: Set memory and CPU limits to prevent DoS
4. **Input Validation**: Validate all OpenSCAD code before execution

## Next Steps

### Recommended Workflow
1. **Start Simple**: Test basic cube and sphere generation
2. **Learn OpenSCAD**: Familiarize yourself with OpenSCAD syntax
3. **Create Templates**: Build reusable parametric designs
4. **Integrate AI**: Use AI models to generate complex designs
5. **3D Print**: Export STL files for physical prototyping

### Advanced Setup
- **GPU Acceleration**: Configure CUDA for faster rendering
- **Distributed Processing**: Set up multiple render nodes
- **Custom Libraries**: Add specialized OpenSCAD libraries
- **API Integration**: Connect to CAD/CAM systems

## Resources

- **OpenSCAD Documentation**: [openscad.org/documentation](https://openscad.org/documentation.html)
- **MCP Server Repository**: [GitHub - jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server)
- **OpenSCAD Cheat Sheet**: [OpenSCAD Quick Reference](https://openscad.org/cheatsheet/)
- **3D Printing Guidelines**: STL export best practices

Your AI assistant can now help you with professional 3D modeling and CAD operations! 🎯
