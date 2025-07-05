import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';
import os from 'os';

export async function POST() {
  try {
    // Get list of recent render files and copy them to public directory
    const tempDir = os.tmpdir();
    const publicRendersDir = path.join(process.cwd(), 'public', 'renders');
    
    // Ensure public/renders directory exists
    try {
      await fs.mkdir(publicRendersDir, { recursive: true });
    } catch (error) {
      console.warn('Could not create public renders directory:', error);
    }

    const constructaiDirs = await fs.readdir(tempDir);
    const blenderDirs = constructaiDirs.filter(dir => dir.startsWith('constructai_blender_'));
    
    const renderFiles = [];
    
    for (const dir of blenderDirs.slice(-10)) { // Get last 10 directories
      const dirPath = path.join(tempDir, dir);
      try {
        const files = await fs.readdir(dirPath);
        const pngFiles = files.filter(file => file.endsWith('.png'));
        
        for (const file of pngFiles) {
          const sourcePath = path.join(dirPath, file);
          const stats = await fs.stat(sourcePath);
          
          // Create unique filename with timestamp
          const timestamp = stats.birthtime.getTime();
          const uniqueFileName = `${timestamp}_${file}`;
          const publicPath = path.join(publicRendersDir, uniqueFileName);
          
          // Copy file to public directory if it doesn't exist
          try {
            await fs.access(publicPath);
          } catch {
            // File doesn't exist in public, copy it
            try {
              await fs.copyFile(sourcePath, publicPath);
            } catch (copyError) {
              console.warn(`Could not copy file ${file}:`, copyError);
              continue;
            }
          }
          
          renderFiles.push({
            name: file,
            path: sourcePath,
            publicPath: `/renders/${uniqueFileName}`,
            size: stats.size,
            created: stats.birthtime,
            url: `/renders/${uniqueFileName}`
          });
        }
      } catch (error) {
        console.warn(`Could not read directory ${dir}:`, error);
      }
    }

    // Sort by creation time, newest first
    renderFiles.sort((a, b) => b.created.getTime() - a.created.getTime());

    return NextResponse.json({ 
      renders: renderFiles,
      message: `Found ${renderFiles.length} render files`
    });
  } catch (error) {
    console.error('Error copying render files:', error);
    return NextResponse.json({ error: 'Failed to process files' }, { status: 500 });
  }
}
