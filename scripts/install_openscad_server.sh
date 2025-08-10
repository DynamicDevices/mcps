#!/bin/bash
# OpenSCAD MCP Server Installation Script
# Run this on your MCP server (192.168.0.7)

set -e  # Exit on any error

echo "🔧 Installing OpenSCAD MCP Server"
echo "=================================="
echo "ℹ️  This installer will reuse your existing Stable Diffusion WebUI"
echo "   virtual environment to save space and avoid conflicts."

# Check if running on the correct server
if [ "$(hostname)" != "ollama" ]; then
    echo "⚠️  This script should be run on the ollama server (192.168.0.7)"
    echo "   Run: ssh ajlennon@192.168.0.7"
    echo "   Then: bash install_openscad_server.sh"
    exit 1
fi

# Step 1: Install OpenSCAD
echo ""
echo "📦 Step 1: Installing OpenSCAD..."
if ! command -v openscad &> /dev/null; then
    echo "   Installing OpenSCAD via apt..."
    sudo apt-get update
    sudo apt-get install -y openscad
    echo "   ✅ OpenSCAD installed"
else
    echo "   ✅ OpenSCAD already installed"
fi

# Verify OpenSCAD installation
OPENSCAD_VERSION=$(openscad --version 2>&1 | head -n 1)
echo "   📋 OpenSCAD version: $OPENSCAD_VERSION"

# Step 2: Set up directory structure
echo ""
echo "📁 Step 2: Setting up directories..."
cd /home/ajlennon/mcp-service

# Clone the repository if it doesn't exist
if [ ! -d "OpenSCAD-MCP-Server" ]; then
    echo "   Cloning OpenSCAD MCP Server repository..."
    git clone https://github.com/jhacksman/OpenSCAD-MCP-Server.git
    echo "   ✅ Repository cloned"
else
    echo "   ✅ Repository already exists"
fi

cd OpenSCAD-MCP-Server

# Step 3: Use existing Stable Diffusion virtual environment
echo ""
echo "🐍 Step 3: Using Stable Diffusion virtual environment..."
STABLE_DIFFUSION_VENV="/home/ajlennon/stable-diffusion-webui/venv"

if [ -d "$STABLE_DIFFUSION_VENV" ]; then
    echo "   ✅ Found Stable Diffusion virtual environment"
    echo "   📂 Location: $STABLE_DIFFUSION_VENV"
    
    # Create symbolic link to the existing venv
    if [ ! -L "venv" ] && [ ! -d "venv" ]; then
        ln -s "$STABLE_DIFFUSION_VENV" venv
        echo "   🔗 Created symbolic link to existing venv"
    else
        echo "   ✅ Virtual environment link already exists"
    fi
else
    echo "   ⚠️  Stable Diffusion venv not found at $STABLE_DIFFUSION_VENV"
    echo "   Creating new virtual environment as fallback..."
    python3 -m venv venv
    echo "   ✅ New virtual environment created"
fi

# Activate virtual environment and install dependencies
echo "   Installing Python dependencies..."
source venv/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "   ✅ Dependencies installed"
else
    echo "   ⚠️  No requirements.txt found, installing basic dependencies..."
    pip install fastapi uvicorn python-multipart aiofiles
    echo "   ✅ Basic dependencies installed"
fi

# Step 4: Test the installation
echo ""
echo "🧪 Step 4: Testing installation..."

# Test OpenSCAD
echo "   Testing OpenSCAD..."
echo 'cube([10, 10, 10]);' > test_cube.scad
if openscad --render test_cube.scad -o test_cube.png 2>/dev/null; then
    echo "   ✅ OpenSCAD rendering test passed"
    rm -f test_cube.scad test_cube.png
else
    echo "   ⚠️  OpenSCAD rendering test failed, but installation may still work"
    rm -f test_cube.scad test_cube.png
fi

# Test Python server (basic syntax check)
echo "   Testing Python server..."
if [ -f "src/main.py" ]; then
    if python src/main.py --help &>/dev/null; then
        echo "   ✅ Python server test passed"
    else
        echo "   ⚠️  Python server test failed, check dependencies"
    fi
else
    echo "   ⚠️  src/main.py not found, manual setup may be required"
fi

# Step 5: Create configuration
echo ""
echo "⚙️  Step 5: Configuration instructions..."
echo ""
echo "🎯 Next steps to complete the setup:"
echo ""
echo "1. 📝 Update your MCP configuration:"
echo "   nano /home/ajlennon/mcp-service/mcp-config.json"
echo ""
echo "   Add this server block:"
echo '   "openscad": {'
echo '     "command": "/home/ajlennon/stable-diffusion-webui/venv/bin/python",'
echo '     "args": ["/home/ajlennon/mcp-service/OpenSCAD-MCP-Server/src/main.py"],'
echo '     "env": {'
echo '       "VIRTUAL_ENV": "/home/ajlennon/stable-diffusion-webui/venv"'
echo '     }'
echo '   }'
echo ""
echo "2. 🔄 Restart the MCP proxy:"
echo "   sudo systemctl restart mcp-proxy"
echo ""
echo "3. 🧪 Test the integration:"
echo "   Check if openscad endpoints appear in http://192.168.0.7:8000/docs"
echo ""
echo "4. 🎨 Try in Open WebUI:"
echo '   "Create an OpenSCAD model of a cube and render it as an image"'
echo ""

# Step 6: Optional API keys setup
echo "🔑 Optional: API Keys for Advanced Features"
echo ""
echo "For AI-generated 3D models, create a .env file:"
echo "   nano /home/ajlennon/mcp-service/OpenSCAD-MCP-Server/.env"
echo ""
echo "Add these lines (get keys from respective services):"
echo "   GEMINI_API_KEY=your-gemini-api-key"
echo "   VENICE_API_KEY=your-venice-api-key"
echo ""
echo "Note: Basic OpenSCAD rendering works without API keys!"
echo ""

echo "✅ OpenSCAD MCP Server installation completed!"
echo ""
echo "📚 For detailed documentation, see:"
echo "   docs/setup_openscad_server.md"
echo ""
echo "🚀 Happy 3D modeling!"
