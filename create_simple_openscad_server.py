#!/usr/bin/env python3
"""
Simple OpenSCAD MCP Server
Creates a working OpenSCAD server compatible with current MCP SDK
"""

import asyncio
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Any, Dict

from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent


# Create the server instance
server = Server("openscad-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available OpenSCAD tools."""
    return [
        Tool(
            name="render_openscad",
            description="Render OpenSCAD code to PNG image",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "OpenSCAD code to render"
                    },
                    "width": {
                        "type": "integer", 
                        "description": "Image width (default: 512)",
                        "default": 512
                    },
                    "height": {
                        "type": "integer",
                        "description": "Image height (default: 512)", 
                        "default": 512
                    }
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="generate_stl",
            description="Generate STL file from OpenSCAD code",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "OpenSCAD code to convert to STL"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Output filename (without extension)",
                        "default": "model"
                    }
                },
                "required": ["code"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "render_openscad":
        return await render_openscad_code(
            arguments["code"],
            arguments.get("width", 512),
            arguments.get("height", 512)
        )
    
    elif name == "generate_stl":
        return await generate_stl_file(
            arguments["code"],
            arguments.get("filename", "model")
        )
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def render_openscad_code(code: str, width: int = 512, height: int = 512) -> list[TextContent]:
    """Render OpenSCAD code to PNG image."""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write OpenSCAD code to temporary file
            scad_file = Path(temp_dir) / "model.scad"
            png_file = Path(temp_dir) / "model.png"
            
            with open(scad_file, 'w') as f:
                f.write(code)
            
            # Run OpenSCAD to render image (headless mode via environment)
            cmd = [
                "openscad",
                "--render",
                "--imgsize", f"{width},{height}",
                "-o", str(png_file),
                str(scad_file)
            ]
            
            # Set environment for headless operation
            env = os.environ.copy()
            env['DISPLAY'] = ':99'  # Virtual display
            env['QT_QPA_PLATFORM'] = 'offscreen'
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,
                env=env
            )
            
            if result.returncode != 0:
                return [TextContent(
                    type="text",
                    text=f"❌ OpenSCAD rendering failed:\n{result.stderr}"
                )]
            
            if png_file.exists():
                # Copy to persistent location
                output_dir = Path("/home/ajlennon/mcp-service/files")
                output_dir.mkdir(exist_ok=True)
                
                output_file = output_dir / f"openscad_render_{width}x{height}.png"
                import shutil
                shutil.copy2(png_file, output_file)
                
                return [TextContent(
                    type="text",
                    text=f"✅ OpenSCAD code rendered successfully!\n📁 Output: {output_file}\n📐 Size: {width}x{height}"
                )]
            else:
                return [TextContent(
                    type="text", 
                    text="❌ Rendering completed but no output file was generated"
                )]
                
    except subprocess.TimeoutExpired:
        return [TextContent(
            type="text",
            text="❌ OpenSCAD rendering timed out (30 seconds)"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error during rendering: {str(e)}"
        )]


async def generate_stl_file(code: str, filename: str = "model") -> list[TextContent]:
    """Generate STL file from OpenSCAD code."""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write OpenSCAD code to temporary file
            scad_file = Path(temp_dir) / "model.scad"
            stl_file = Path(temp_dir) / "model.stl"
            
            with open(scad_file, 'w') as f:
                f.write(code)
            
            # Run OpenSCAD to generate STL (headless mode via environment)
            cmd = [
                "openscad",
                "--export-format=binstl",
                "-o", str(stl_file),
                str(scad_file)
            ]
            
            # Set environment for headless operation
            env = os.environ.copy()
            env['DISPLAY'] = ':99'  # Virtual display
            env['QT_QPA_PLATFORM'] = 'offscreen'
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                env=env
            )
            
            if result.returncode != 0:
                return [TextContent(
                    type="text",
                    text=f"❌ STL generation failed:\n{result.stderr}"
                )]
            
            if stl_file.exists():
                # Copy to persistent location
                output_dir = Path("/home/ajlennon/mcp-service/files")
                output_dir.mkdir(exist_ok=True)
                
                output_file = output_dir / f"{filename}.stl"
                import shutil
                shutil.copy2(stl_file, output_file)
                
                file_size = output_file.stat().st_size
                return [TextContent(
                    type="text",
                    text=f"✅ STL file generated successfully!\n📁 Output: {output_file}\n📏 Size: {file_size:,} bytes"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ STL generation completed but no output file was generated"
                )]
                
    except subprocess.TimeoutExpired:
        return [TextContent(
            type="text",
            text="❌ STL generation timed out (60 seconds)"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error during STL generation: {str(e)}"
        )]



async def main():
    """Run the OpenSCAD MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
