import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';
import os from 'os';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const filePath = searchParams.get('path');

    if (!filePath) {
      return NextResponse.json({ error: 'File path required' }, { status: 400 });
    }

    // Security check - only allow files from temp directories we created
    if (!filePath.includes('constructai_blender_')) {
      return NextResponse.json({ error: 'Invalid file path' }, { status: 403 });
    }

    // Check if file exists
    try {
      await fs.access(filePath);
    } catch {
      return NextResponse.json({ error: 'File not found' }, { status: 404 });
    }

    // Read and serve the file
    const fileBuffer = await fs.readFile(filePath);
    const fileName = path.basename(filePath);

    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': 'image/png',
        'Content-Disposition': `inline; filename="${fileName}"`,
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  } catch (error) {
    console.error('Error serving render file:', error);
    return NextResponse.json({ error: 'Failed to serve file' }, { status: 500 });
  }
}

export async function POST() {
  try {
    // Get list of recent render files
    const tempDir = os.tmpdir();
    const constructaiDirs = await fs.readdir(tempDir);
    const blenderDirs = constructaiDirs.filter(dir => dir.startsWith('constructai_blender_'));
    
    const renderFiles = [];
    
    for (const dir of blenderDirs.slice(-5)) { // Get last 5 directories
      const dirPath = path.join(tempDir, dir);
      try {
        const files = await fs.readdir(dirPath);
        const pngFiles = files.filter(file => file.endsWith('.png'));
        
        for (const file of pngFiles) {
          const filePath = path.join(dirPath, file);
          const stats = await fs.stat(filePath);
          renderFiles.push({
            name: file,
            path: filePath,
            size: stats.size,
            created: stats.birthtime,
            url: `/api/renders?path=${encodeURIComponent(filePath)}`
          });
        }
      } catch (error) {
        console.warn(`Could not read directory ${dir}:`, error);
      }
    }

    // Sort by creation time, newest first
    renderFiles.sort((a, b) => b.created.getTime() - a.created.getTime());

    return NextResponse.json({ renders: renderFiles });
  } catch (error) {
    console.error('Error listing render files:', error);
    return NextResponse.json({ error: 'Failed to list files' }, { status: 500 });
  }
}
