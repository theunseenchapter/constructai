import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    const publicDir = path.join(process.cwd(), 'public', 'renders')
    const backendDir = path.join(process.cwd(), 'generated_models')
    
    const allFiles: Array<{
      name: string
      size: number
      modified: string
      type: 'obj' | 'ply' | 'other'
      location: string
    }> = []
    
    // Check public directory
    try {
      if (fs.existsSync(publicDir)) {
        const publicFiles = fs.readdirSync(publicDir)
        for (const filename of publicFiles) {
          const filePath = path.join(publicDir, filename)
          const stats = fs.statSync(filePath)
          if (stats.isFile()) {
            const ext = path.extname(filename).toLowerCase()
            allFiles.push({
              name: filename,
              size: stats.size,
              modified: stats.mtime.toISOString(),
              type: ext === '.obj' ? 'obj' : ext === '.ply' ? 'ply' : 'other',
              location: 'public'
            })
          }
        }
      }
    } catch (err) {
      console.error('Error reading public directory:', err)
    }
    
    // Check backend directory
    try {
      if (fs.existsSync(backendDir)) {
        const backendFiles = fs.readdirSync(backendDir)
        for (const filename of backendFiles) {
          const filePath = path.join(backendDir, filename)
          const stats = fs.statSync(filePath)
          if (stats.isFile()) {
            // Only add if not already in public (avoid duplicates)
            const alreadyExists = allFiles.some(f => f.name === filename)
            if (!alreadyExists) {
              const ext = path.extname(filename).toLowerCase()
              allFiles.push({
                name: filename,
                size: stats.size,
                modified: stats.mtime.toISOString(),
                type: ext === '.obj' ? 'obj' : ext === '.ply' ? 'ply' : 'other',
                location: 'backend'
              })
            }
          }
        }
      }
    } catch (err) {
      console.error('Error reading backend directory:', err)
    }
    
    // Sort by modification date (newest first)
    allFiles.sort((a, b) => new Date(b.modified).getTime() - new Date(a.modified).getTime())
    
    const response = {
      success: true,
      files: allFiles,
      count: allFiles.length,
      directories: {
        public: publicDir,
        backend: backendDir
      },
      timestamp: new Date().toISOString()
    }
    
    console.log(`📁 File list request: ${allFiles.length} files found`)
    
    return NextResponse.json(response)
    
  } catch (error) {
    console.error('❌ Error listing files:', error)
    
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to list files',
        details: error instanceof Error ? error.message : 'Unknown error',
        files: [],
        count: 0
      },
      { status: 500 }
    )
  }
}
