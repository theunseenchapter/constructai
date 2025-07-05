# Perfect MCP + GitHub Copilot Integration Guide

## Prerequisites
✅ You already have:
- MCP package installed (`pip install mcp`)
- Blender MCP server created
- VS Code with GitHub Copilot extension

## Step-by-Step Setup

### 1. Configure VS Code for GitHub Copilot MCP Integration

The VS Code settings are already configured in `.vscode/settings.json` for GitHub Copilot MCP integration. The key settings are:

```json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": true,
    "markdown": true
  },
  "github.copilot.advanced": {
    "debug.overrideEngine": "claude-3-5-sonnet-20241022"
  },
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

### 2. Start Your MCP Server

```bash
cd d:\constructai\backend
python start_mcp_server.py
```

You should see:
```
Starting Blender MCP Server for GitHub Copilot integration...
Server running on stdio...
```

### 3. Test MCP Connection in VS Code

With GitHub Copilot enabled in VS Code, you can now interact with the MCP server through:

1. **VS Code Command Palette** (Ctrl+Shift+P):
   - Type "MCP" to see available MCP commands
   - Look for "constructai-blender" server

2. **GitHub Copilot Chat** (@workspace):
   Ask GitHub Copilot to help with 3D scene creation:
   ```
   @workspace Create a 3D scene with a living room using the Blender MCP server
   ```

### 4. Verify Integration

Test with these prompts in GitHub Copilot Chat:

1. **Check MCP server status:**
   ```
   Can you check if the constructai-blender MCP server is running?
   ```

2. **Create a scene:**
   ```
   Use the Blender MCP server to create a 3D scene with a bedroom and kitchen
   ```

3. **Render the scene:**
   ```
   Render the scene in 360-degree view using the Blender MCP server
   ```

## Expected Results

✅ **Working Integration:**
- GitHub Copilot can see and call your Blender MCP tools
- You get responses from your actual Blender server
- Scene creation and rendering work through GitHub Copilot
- Logs show MCP communication

✅ **In Your Frontend:**
- BlenderRoomViewer connects to MCP server
- API routes work with real MCP protocol
- Renders are generated through Blender

## Troubleshooting

### If GitHub Copilot can't find the MCP server:

1. **Check VS Code settings:**
   ```bash
   # Open VS Code settings
   Ctrl+Shift+P → "Preferences: Open Settings (JSON)"
   # Verify mcp.servers configuration
   ```

2. **Restart VS Code** after settings changes

3. **Check server logs:**
   ```bash
   cd d:\constructai\backend
   python start_mcp_server.py
   # Look for initialization messages
   ```

### If VS Code GitHub Copilot extension doesn't connect:

1. **Reload VS Code window** (Ctrl+Shift+P → "Developer: Reload Window")
2. **Check VS Code settings** are properly saved
3. **Verify GitHub Copilot extension** is installed and updated
4. **Check MCP server status** in VS Code output panel

## Advanced Configuration

### For Production:
- Add error handling in MCP server
- Implement proper Blender path detection
- Add authentication if needed
- Set up logging and monitoring

### For Development:
- Enable debug logging in MCP server
- Use development Blender builds
- Add hot-reload for MCP server changes

## Success Indicators

🟢 **Perfect Integration Achieved When:**
- GitHub Copilot shows "constructai-blender" in available servers
- MCP tools are listed and callable from GitHub Copilot
- Your frontend gets real Blender renders
- End-to-end 3D generation works seamlessly

You're now ready to have GitHub Copilot directly control your Blender 3D generation!
