#!/usr/bin/env python3
"""
Startup script for the Blender MCP Server
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import the MCP server
from mcp_servers.blender_server import main

if __name__ == "__main__":
    print("Starting Blender MCP Server...")
    print(f"Backend directory: {backend_dir}")
    print(f"Python path: {sys.path}")
    
    # Check if Blender is available
    blender_path = os.environ.get('BLENDER_PATH', 'blender')
    print(f"Blender path: {blender_path}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down Blender MCP Server...")
    except Exception as e:
        print(f"Error starting MCP server: {e}")
        sys.exit(1)
