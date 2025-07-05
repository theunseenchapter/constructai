# ConstructAI - GitHub Copilot MCP Integration

This project integrates with GitHub Copilot in VS Code through the Model Context Protocol (MCP) to provide AI-powered 3D architectural visualization using Blender.

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   pip install -r backend/requirements.txt
   ```

2. **Start the Development Server**
   ```bash
   npm run dev
   ```

3. **Start the MCP Server**
   ```bash
   cd backend
   python start_mcp_server.py
   ```

4. **Use with GitHub Copilot**
   - Open VS Code with this workspace
   - GitHub Copilot will automatically detect the MCP server
   - Ask Copilot to create 3D scenes: "Create a 3D architectural scene with a living room"

## MCP Server Configuration

The MCP server is configured in `.vscode/settings.json`:

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

## Available MCP Tools

- `create_3d_scene`: Creates a 3D scene from room data
- `render_scene`: Renders the current scene (single or 360° view)

## Architecture

- **Frontend**: Next.js 14 PWA with TypeScript
- **Backend**: FastAPI with MCP server integration
- **3D Engine**: Blender (via MCP)
- **AI Integration**: GitHub Copilot + MCP protocol

## Usage Examples

### In GitHub Copilot Chat:

```
@workspace Create a 3D scene with a modern living room using the Blender MCP server
```

```
@workspace Render a 360-degree view of the current scene
```

### In the Web Interface:

The frontend provides a `BlenderRoomViewer` component that communicates with the MCP server through API routes.

## Development

- **Frontend**: `src/components/BlenderRoomViewer.tsx`
- **MCP Client**: `src/lib/mcp-client.ts`
- **MCP Server**: `backend/mcp_servers/blender_server.py`
- **API Routes**: `src/app/api/mcp/`

## Documentation

- [MCP GitHub Copilot Integration Guide](./MCP_GITHUB_COPILOT_INTEGRATION.md)
- [Cleanup Summary](./CLEANUP_SUMMARY.md)

## Features

✅ GitHub Copilot MCP integration
✅ Blender-based 3D rendering
✅ TypeScript type safety
✅ Real-time 3D scene generation
✅ API-based MCP communication
✅ VS Code workspace configuration
