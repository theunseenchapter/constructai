import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';
import os from 'os';

export async function POST() {
  try {
    const tempDir = os.tmpdir();
    const results = {
      tempDir,
      searchResults: [] as Array<{name: string, path: string, size: number, lastModified: Date, isFile: boolean}>,
      allTempContents: [] as Array<{directory: string, path: string, files: string[], lastModified: Date}>
    };

    // Search all temp directories
    try {
      const tempContents = await fs.readdir(tempDir);
      
      // Find all constructai directories
      const constructaiDirs = tempContents.filter(dir => 
        dir.includes('constructai') || dir.includes('blender')
      );

      for (const dir of constructaiDirs) {
        const dirPath = path.join(tempDir, dir);
        try {
          const stats = await fs.stat(dirPath);
          if (stats.isDirectory()) {
            const files = await fs.readdir(dirPath);
            results.allTempContents.push({
              directory: dir,
              path: dirPath,
              files,
              lastModified: stats.mtime
            });
          }
        } catch (error) {
          console.warn(`Could not read directory ${dir}:`, error);
        }
      }

      // Also check for any recent files in temp
      const recentFiles = [];
      for (const item of tempContents) {
        try {
          const itemPath = path.join(tempDir, item);
          const stats = await fs.stat(itemPath);
          if (!stats.isDirectory() && 
              (item.endsWith('.png') || item.endsWith('.jpg') || item.endsWith('.jpeg') || item.endsWith('.blend'))) {
            recentFiles.push({
              name: item,
              path: itemPath,
              size: stats.size,
              lastModified: stats.mtime,
              isFile: stats.isFile()
            });
          }
        } catch {
          // Skip files we can't access
        }
      }
      
      results.searchResults = recentFiles;

    } catch (error) {
      console.error('Error reading temp directory:', error);
    }

    return NextResponse.json({
      success: true,
      results
    });
  } catch (error) {
    console.error('Error in debug endpoint:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Debug failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
