import { NextRequest, NextResponse } from 'next/server';
import { mcpClient } from '@/lib/mcp-client';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { view_type } = body;

    console.log('Rendering scene via MCP with view type:', view_type);

    // Call the MCP server
    const result = await mcpClient.callTool('render_scene', {
      view_type
    });

    const renderResult = result as { render_files: string[] };
    
    return NextResponse.json({
      success: true,
      message: 'Scene rendered successfully with Blender MCP',
      render_id: Date.now().toString(),
      view_type,
      render_files: renderResult.render_files,
      mcp_result: result,
      server: 'blender-mcp-9876'
    });

  } catch (error) {
    console.error('MCP render-scene error:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to render scene via MCP',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
