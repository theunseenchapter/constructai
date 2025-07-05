import { NextRequest, NextResponse } from 'next/server';
import { mcpClient } from '@/lib/mcp-client';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { rooms, building_dimensions } = body;

    console.log('Creating 3D scene with MCP:', { rooms: rooms.length, building_dimensions });

    // Call the MCP server
    const result = await mcpClient.callTool('create_3d_scene', {
      rooms,
      building_dimensions
    });

    return NextResponse.json({
      success: true,
      message: 'Scene created successfully with Blender MCP',
      scene_id: Date.now().toString(),
      rooms_processed: rooms.length,
      building_dimensions,
      mcp_result: result,
      server: 'blender-mcp-9876'
    });

  } catch (error) {
    console.error('MCP create-scene error:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to create scene via MCP',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
