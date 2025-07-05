import { NextRequest, NextResponse } from 'next/server';
import { mcpClient } from '@/lib/mcp-client';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { server_url, server_name } = body;

    console.log(`Connecting to MCP server: ${server_name} at ${server_url}`);
    
    // Check MCP server status
    const status = await mcpClient.getServerStatus();
    
    if (status.connected) {
      return NextResponse.json({
        success: true,
        connected: true,
        server_name,
        server_url,
        version: status.version,
        message: "Connected to Blender MCP Server"
      });
    } else {
      throw new Error(status.error || 'Failed to connect');
    }

  } catch (error) {
    console.error('MCP connection error:', error);
    return NextResponse.json(
      { 
        success: false,
        connected: false,
        error: 'Failed to connect to MCP server',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
