import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

export async function POST() {
  try {
    // Copy 3D model files to D:\constructai\downloads folder
    const modelsDir = path.join(process.cwd(), 'backend', 'generated_models');
    const downloadsDir = path.join('D:', 'constructai', 'downloads');
    
    console.log('Models directory:', modelsDir);
    console.log('Downloads directory:', downloadsDir);
    
    // Ensure downloads directory exists
    try {
      await fs.mkdir(downloadsDir, { recursive: true });
    } catch (error) {
      console.warn('Could not create downloads directory:', error);
    }

    // Get all model files (.obj, .mtl)
    const copiedFiles = [];
    
    try {
      const files = await fs.readdir(modelsDir);
      console.log('Found files in models directory:', files);
      
      const modelFiles = files.filter(file => 
        file.endsWith('.obj') || file.endsWith('.mtl') || file.endsWith('.blend')
      );
      
      console.log('Model files to copy:', modelFiles);
      
      for (const file of modelFiles) {
        const sourcePath = path.join(modelsDir, file);
        try {
          const stats = await fs.stat(sourcePath);
          
          // Create unique filename with timestamp
          const timestamp = stats.birthtime.getTime();
          const fileExt = path.extname(file);
          const baseName = path.basename(file, fileExt);
          const uniqueFileName = `${timestamp}_${baseName}${fileExt}`;
          const downloadPath = path.join(downloadsDir, uniqueFileName);
          
          // Copy file to downloads directory
          await fs.copyFile(sourcePath, downloadPath);
          
          copiedFiles.push({
            name: uniqueFileName,
            originalName: file,
            path: downloadPath,
            size: stats.size,
            type: fileExt.substring(1), // Remove the dot
            created: stats.birthtime.toISOString()
          });
          
          console.log(`Copied ${file} to ${uniqueFileName}`);
        } catch (copyError) {
          console.warn(`Could not copy file ${file}:`, copyError);
          continue;
        }
      }
      
    } catch (error) {
      console.warn('Could not read models directory:', error);
    }

    // Sort by creation time (newest first)
    copiedFiles.sort((a, b) => new Date(b.created).getTime() - new Date(a.created).getTime());

    console.log(`Total model files copied: ${copiedFiles.length}`);

    return NextResponse.json({
      success: true,
      message: `Copied ${copiedFiles.length} 3D model files to downloads folder`,
      files: copiedFiles,
      downloadsPath: downloadsDir,
      modelTypes: ['obj', 'mtl', 'blend']
    });
  } catch (error) {
    console.error('Error copying 3D models to downloads:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to copy 3D models to downloads folder',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
