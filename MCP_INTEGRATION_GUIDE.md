# ConstructAI Blender MCP Integration Guide

## 🚀 Complete Setup Instructions

### 1. Prerequisites Verification
```bash
# Ensure you have these installed:
- Blender (latest version)
- Python 3.8+
- Node.js 18+
- VS Code with GitHub Copilot
```

### 2. MCP Server Configuration ✅
The MCP server is already configured in `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "constructai-blender": {
      "command": "python",
      "args": ["d:/constructai/backend/start_mcp_server.py"],
      "cwd": "d:/constructai",
      "env": {
        "BLENDER_PATH": "blender",
        "PYTHONPATH": "d:/constructai/backend",
        "MCP_SERVER_NAME": "blender-3d-server"
      }
    }
  }
}
```

### 3. How to Use the Integration

#### Option A: Using GitHub Copilot Chat
1. Open VS Code in the `d:\constructai` folder
2. Open GitHub Copilot Chat (Ctrl+Shift+I)
3. Ask Copilot to create 3D scenes:

```
@constructai-blender Create a modern living room with:
- 6m x 8m dimensions
- Modern furniture (sofa, coffee table, TV stand)
- Proper lighting
- Render both single view and 360° panorama
```

#### Option B: Using the Web Interface
1. Start the development server:
```bash
cd d:\constructai
npm run dev
```

2. Open your browser to: `http://localhost:3001`

3. Navigate to available pages:
   - **BOQ Calculator**: `http://localhost:3001/boq`
   - **Modern Living Room Demo**: `http://localhost:3001/demo/modern-living-room`
   - **Admin Dashboard**: `http://localhost:3001/admin/pricing`

#### Option C: Using the API Directly
```javascript
// Create a 3D scene
const response = await fetch('/api/mcp/create-scene', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    rooms: [
      {
        name: "Living Room",
        type: "living_room",
        width: 6,
        length: 8,
        height: 3.2
      }
    ],
    building_dimensions: {
      total_width: 6,
      total_length: 8,
      height: 3.2
    }
  })
});

// Render the scene
const renderResponse = await fetch('/api/mcp/render-scene', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    view_type: '360' // or 'single'
  })
});
```

### 4. Available MCP Tools

The Blender MCP server provides these tools:

1. **`create_3d_scene`** - Creates complete room layouts
2. **`render_scene`** - Generates high-quality renders
3. **`add_furniture`** - Adds specific furniture pieces
4. **`set_materials`** - Applies materials and textures
5. **`configure_lighting`** - Sets up realistic lighting
6. **`export_model`** - Exports 3D models (OBJ, FBX, GLTF)

### 5. GitHub Copilot Integration Examples

#### Create a Modern Kitchen
```
@constructai-blender Create a modern kitchen scene:
- 4m x 3m kitchen
- Include cabinets, island, appliances
- White and wood finish
- Natural lighting from window
- Render top view and perspective view
```

#### Generate Building Layout
```
@constructai-blender Design a 2-bedroom apartment:
- 1000 sq ft total area
- Master bedroom with ensuite
- Open living/kitchen area
- Balcony access
- Modern minimalist style
- Generate floor plan and 3D visualization
```

#### Create Construction BOQ
```
@constructai-blender Calculate BOQ for:
- 3-bedroom house
- 1500 sq ft
- Standard quality materials
- Include doors, windows, flooring
- Generate 3D preview and cost breakdown
```

### 6. Testing the Integration

#### Quick Test Commands:
```bash
# 1. Test MCP server directly
cd d:\constructai\backend
python start_mcp_server.py

# 2. Test web interface
cd d:\constructai
npm run dev

# 3. Test API endpoints
curl -X POST http://localhost:3001/api/mcp/connect
```

#### Expected Outputs:
- ✅ MCP server starts on port 9876
- ✅ Web interface loads on port 3001
- ✅ API endpoints respond with status
- ✅ Copilot can call MCP tools

### 7. Troubleshooting

#### Common Issues:

**MCP Server Not Starting:**
```bash
# Check Python path
python --version
# Check Blender installation
blender --version
# Install MCP dependencies
pip install mcp
```

**Port Conflicts:**
```bash
# Kill processes on port 3000/3001
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

**VS Code Copilot Issues:**
```bash
# Reload VS Code window
Ctrl+Shift+P > "Developer: Reload Window"
# Check MCP server status in VS Code output panel
```

### 8. Next Steps

1. **Test Basic Functionality**: Try the modern living room demo
2. **Create Your First Scene**: Use Copilot to generate a custom room
3. **Explore BOQ Features**: Calculate costs for your projects
4. **Customize Materials**: Add your own textures and finishes
5. **Export Models**: Download 3D models for other tools

### 9. File Structure Overview

```
d:\constructai\
├── .vscode/settings.json          # MCP configuration
├── backend/
│   ├── start_mcp_server.py        # MCP server startup
│   └── mcp_servers/
│       └── blender_server.py      # Main MCP server
├── src/
│   ├── components/
│   │   ├── BlenderRoomViewer.tsx  # 3D viewer component
│   │   ├── Enhanced3DBOQ.tsx      # BOQ calculator
│   │   └── ModernLivingRoomDemo.tsx # Demo component
│   ├── app/
│   │   ├── boq/page.tsx          # BOQ page
│   │   └── demo/modern-living-room/page.tsx # Demo page
│   └── lib/mcp-client.ts         # MCP client
└── package.json                  # Dependencies
```

### 10. Ready to Go! 🎉

Your ConstructAI Blender MCP integration is complete and ready for:
- ✅ GitHub Copilot integration
- ✅ 3D architectural visualization
- ✅ BOQ calculation and cost estimation
- ✅ Modern web interface
- ✅ MCP server communication
- ✅ Blender automation

**Start using it now:**
1. Run `npm run dev` in the terminal
2. Open http://localhost:3001/demo/modern-living-room
3. Click "Create Modern Living Room" to test
4. Use GitHub Copilot chat with `@constructai-blender` commands

Happy building! 🏗️✨
