import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
  request: NextRequest,
  { params }: { params: { filename: string } }
) {
  try {
    const filename = params.filename
    
    // Try multiple possible locations for the file
    const possiblePaths = [
      path.join(process.cwd(), 'public', 'renders', filename),
      path.join(process.cwd(), 'backend', 'generated_models', filename),
      path.join(process.cwd(), 'public', 'renders', `model_${filename}`),
    ]
    
    let filePath = ''
    let fileExists = false
    
    for (const possiblePath of possiblePaths) {
      if (fs.existsSync(possiblePath)) {
        filePath = possiblePath
        fileExists = true
        break
      }
    }
    
    if (!fileExists) {
      console.error(`File not found: ${filename}`)
      console.error('Searched paths:', possiblePaths)
      return new NextResponse('3D Model file not found', { status: 404 })
    }

    // Get file stats
    const stats = fs.statSync(filePath)
    const fileBuffer = fs.readFileSync(filePath)
    
    // Determine content type based on file extension
    const ext = path.extname(filename).toLowerCase()
    let contentType = 'application/octet-stream'
    
    switch (ext) {
      case '.obj':
        contentType = 'model/obj'
        break
      case '.mtl':
        contentType = 'text/plain'
        break
      case '.ply':
        contentType = 'application/ply'
        break
      case '.gltf':
        contentType = 'model/gltf+json'
        break
      case '.glb':
        contentType = 'model/gltf-binary'
        break
      case '.blend':
        contentType = 'application/x-blender'
        break
      default:
        contentType = 'application/octet-stream'
    }

    // Return file with proper headers for download
    return new NextResponse(fileBuffer, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Content-Length': stats.size.toString(),
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    })
  } catch (error) {
    console.error('Error serving 3D model file:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
}
