# Blender MCP Server Integration

This document describes the integration of Blender with the ConstructAI system using the Model Context Protocol (MCP).

## Overview

The Blender MCP Server provides high-quality 3D architectural visualization for ConstructAI. It replaces the previous Three.js and Babylon.js implementations with a server-side Blender rendering solution.

## Components

### Backend Components

1. **MCP Server** (`backend/mcp_servers/blender_server.py`)
   - Handles 3D scene creation using Blender's Python API
   - Provides tools for scene rendering and image generation
   - Supports both single view and 360° panoramic renders

2. **API Routes** (`src/app/api/mcp/`)
   - `create-scene/route.ts`: Creates 3D scenes from room data
   - `render-scene/route.ts`: Renders scenes with different view types

3. **Startup Scripts**
   - `start_mcp_server.py`: Python startup script
   - `start-mcp-server.ps1`: PowerShell script for Windows

### Frontend Components

1. **BlenderRoomViewer** (`src/components/BlenderRoomViewer.tsx`)
   - React component for displaying Blender renders
   - Supports single view and 360° panoramic viewing
   - Manages render history and user interactions

2. **Enhanced3DBOQ** (`src/components/Enhanced3DBOQ.tsx`)
   - Main integration point for the 3D viewer
   - Updated to use BlenderRoomViewer instead of Three.js/Babylon.js

## Setup

### Prerequisites

1. **Blender Installation**
   - Install Blender 3.0 or higher
   - Ensure Blender is accessible from command line (`blender` command)
   - Set `BLENDER_PATH` environment variable if needed

2. **Python Environment**
   - Install MCP package: `pip install mcp`
   - All dependencies are listed in `backend/requirements.txt`

### Installation

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start MCP Server**
   ```bash
   cd backend
   python start_mcp_server.py
   ```
   
   Or on Windows:
   ```powershell
   cd backend
   .\start-mcp-server.ps1
   ```

3. **Start Frontend**
   ```bash
   npm run dev
   ```

## Features

### 3D Scene Creation
- Automatic room layout generation from building specifications
- Support for different room types (bedroom, kitchen, living room, etc.)
- Furniture placement based on room type
- Realistic materials and textures

### Rendering Capabilities
- **Single View**: Standard perspective render
- **360° View**: Multiple angle captures for panoramic viewing
- High-quality PBR (Physically Based Rendering) materials
- Realistic lighting with sun and area lights

### User Interface
- Real-time render status and progress
- Render history with thumbnail previews
- Interactive render viewing
- Building information display

## MCP Tools

The server provides the following MCP tools:

1. **create_3d_scene**
   - Creates a Blender scene from room data
   - Input: rooms array, building dimensions
   - Output: scene file path

2. **render_scene**
   - Renders the current scene
   - Input: view type (single/360)
   - Output: rendered image file paths

3. **get_render_image**
   - Retrieves rendered image as base64
   - Input: render file path
   - Output: base64 encoded image

## Configuration

### Environment Variables

- `BLENDER_PATH`: Path to Blender executable (default: "blender")
- `MCP_SERVER_PORT`: Port for MCP server (default: auto-assigned)
- `TEMP_DIR`: Directory for temporary files (default: system temp)

### Blender Settings

The server automatically configures Blender with:
- Cycles rendering engine
- High-quality render settings (1920x1080)
- PBR materials with realistic properties
- Proper lighting setup

## Troubleshooting

### Common Issues

1. **Blender Not Found**
   - Ensure Blender is installed and in PATH
   - Set BLENDER_PATH environment variable

2. **MCP Connection Failed**
   - Check if MCP server is running
   - Verify port configuration
   - Check firewall settings

3. **Render Quality Issues**
   - Adjust render settings in blender_server.py
   - Modify material properties
   - Update lighting configuration

### Debug Mode

Enable debug logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Optimization

### Render Optimization
- Use appropriate render resolution for preview vs final
- Implement render caching for repeated requests
- Consider GPU acceleration for faster rendering

### Memory Management
- Clean up temporary files after rendering
- Limit concurrent render operations
- Monitor system resources

## Future Enhancements

- [ ] Real-time preview updates
- [ ] Custom material libraries
- [ ] Animation support
- [ ] VR/AR rendering modes
- [ ] Cloud rendering integration
- [ ] Batch processing capabilities

## API Reference

See the MCP server code for detailed API documentation and tool schemas.
