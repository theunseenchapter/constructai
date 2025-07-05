# ConstructAI 🏗️

> AI-Powered Construction Management System with Blender 3D Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-15.3.4-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![MCP Integration](https://img.shields.io/badge/MCP-Integrated-green)](https://modelcontextprotocol.io/)

## 🚀 Features

### 🎨 3D Architectural Visualization
- **Blender MCP Integration** - Seamless 3D scene creation through GitHub Copilot
- **Real-time Rendering** - High-quality architectural renders
- **360° Panoramic Views** - Immersive visualization experience
- **Multiple Export Formats** - OBJ, FBX, GLTF support

### 💰 Bill of Quantities (BOQ) Calculator
- **Intelligent Cost Estimation** - AI-powered pricing analysis
- **Material Database** - Comprehensive construction materials
- **Real-time Pricing** - Dynamic market rate integration
- **3D Preview Integration** - Visual BOQ with 3D models

### 🤖 GitHub Copilot Integration
- **Natural Language Commands** - Create 3D scenes through chat
- **MCP Server Protocol** - Direct Blender automation
- **Intelligent Suggestions** - AI-powered design recommendations
- **Code Generation** - Automatic component creation

## 🏃‍♂️ Quick Start

### Prerequisites
- **Blender** (latest version)
- **Node.js** 18+ 
- **Python** 3.8+
- **VS Code** with GitHub Copilot

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/constructai.git
cd constructai
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm run dev
```

4. **Open in VS Code**
```bash
code .
```

### 🎯 Usage

#### Web Interface
- **BOQ Calculator**: http://localhost:3001/boq
- **3D Demo**: http://localhost:3001/demo/modern-living-room
- **Admin Panel**: http://localhost:3001/admin/pricing

#### GitHub Copilot Commands
```
@constructai-blender Create a modern living room with sectional sofa and coffee table

@constructai-blender Generate BOQ for 3-bedroom house, 1500 sq ft

@constructai-blender Design kitchen layout with island and modern appliances
```

## 🏗️ Architecture

### Frontend (Next.js 15)
- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **Progressive Web App** support

### Backend (FastAPI)
- **Python FastAPI** microservices
- **PostgreSQL** database
- **MinIO** object storage
- **MCP Server Protocol**

### AI/ML Integration
- **Blender Python API** automation
- **Computer Vision** for progress tracking
- **Natural Language Processing** for chat commands
- **3D Model Generation** and optimization

## 📁 Project Structure

```
constructai/
├── 🌐 src/                     # Frontend source
│   ├── 📱 app/                 # Next.js app router
│   ├── 🧩 components/          # React components
│   │   ├── BlenderRoomViewer.tsx
│   │   ├── Enhanced3DBOQ.tsx
│   │   └── ModernLivingRoomDemo.tsx
│   └── 📚 lib/                 # Utilities
├── 🐍 backend/                 # Python backend
│   ├── mcp_servers/            # MCP server implementation
│   ├── api/                    # FastAPI routes
│   └── core/                   # Business logic
├── 🗄️ database/               # Database schemas
├── 🚢 deploy/                  # Deployment configs
└── 📖 docs/                    # Documentation
```

## 🎮 Demo Scenarios

### 1. Modern Living Room Creation
```bash
# Open the demo page
http://localhost:3001/demo/modern-living-room

# Click "Create Modern Living Room"
# Watch as Blender MCP creates and renders the scene
```

### 2. BOQ Calculation with 3D Preview
```bash
# Navigate to BOQ calculator
http://localhost:3001/boq

# Enter project specifications
# Generate cost estimate with 3D visualization
```

### 3. GitHub Copilot Integration
```bash
# Open VS Code in project folder
# Start Copilot Chat (Ctrl+Shift+I)
# Use @constructai-blender commands
```

## 🔧 Configuration

### MCP Server Setup
The MCP server is configured in `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "constructai-blender": {
      "command": "python",
      "args": ["d:/constructai/backend/start_mcp_server.py"],
      "cwd": "d:/constructai"
    }
  }
}
```

### Environment Variables
Create `.env.local`:

```env
NEXTAUTH_SECRET=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/constructai
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
```

## 🧪 Testing

```bash
# Run tests
npm test

# Type checking
npm run type-check

# Linting
npm run lint

# Build
npm run build
```

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production
```bash
npm run build
npm start
```

### Docker
```bash
docker-compose up -d
```

## 📚 Documentation

- **[MCP Integration Guide](./MCP_INTEGRATION_GUIDE.md)** - Complete setup instructions
- **[API Documentation](./docs/api.md)** - Backend API reference
- **[Component Guide](./docs/components.md)** - Frontend components
- **[Deployment Guide](./docs/deployment.md)** - Production deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Blender Foundation** - For the amazing 3D creation suite
- **GitHub Copilot** - For AI-powered development assistance
- **Model Context Protocol** - For enabling AI tool integration
- **Next.js Team** - For the excellent React framework

## 📞 Support

- 📧 Email: support@constructai.com
- 💬 Discord: [ConstructAI Community](https://discord.gg/constructai)
- 📝 Issues: [GitHub Issues](https://github.com/yourusername/constructai/issues)

---

<div align="center">
  <p>Built with ❤️ for the construction industry</p>
  <p>🏗️ ConstructAI - Revolutionizing Construction with AI 🏗️</p>
</div>
