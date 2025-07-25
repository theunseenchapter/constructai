import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(
  request: NextRequest,
  { params }: { params: { filename: string } }
) {
  try {
    const { filename } = await params
    
    // Try multiple possible locations for the file
    const possiblePaths = [
      path.join(process.cwd(), 'public', 'renders', filename),
      path.join(process.cwd(), 'backend', 'generated_models', filename),
      path.join(process.cwd(), 'public', 'renders', `model_${filename}`),
      // Also try without the model_ prefix
      path.join(process.cwd(), 'public', 'renders', filename.replace('model_', '')),
      // Try moving from backend to public if it exists there
      path.join(process.cwd(), 'backend', 'generated_models', filename.replace('model_', '')),
    ]
    
    let filePath = ''
    let fileExists = false
    
    console.log(`🔍 Searching for file: ${filename}`)
    
    for (const possiblePath of possiblePaths) {
      console.log(`📁 Checking: ${possiblePath}`)
      if (fs.existsSync(possiblePath)) {
        filePath = possiblePath
        fileExists = true
        console.log(`✅ Found file at: ${possiblePath}`)
        break
      }
    }
    
    if (!fileExists) {
      console.error(`❌ File not found: ${filename}`)
      console.error('🔍 Searched paths:', possiblePaths)
      
      // Try to find similar files for helpful suggestions
      const publicDir = path.join(process.cwd(), 'public', 'renders')
      let suggestions: string[] = []
      
      try {
        const allFiles = fs.readdirSync(publicDir)
        const nerfFiles = allFiles.filter(f => f.startsWith('nerf_')).slice(-5) // Last 5 NeRF files
        suggestions = nerfFiles
      } catch (e) {
        console.error('Could not read public directory:', e)
      }
      
      return new NextResponse(
        `<!DOCTYPE html>
<html>
<head>
    <title>3D Model Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .error { color: #e74c3c; }
        .suggestion { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .code { background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 5px; font-family: monospace; }
        .file-link { display: block; padding: 8px; margin: 5px 0; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        .file-link:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="error">🚫 3D Model File Not Found</h1>
        <p>The requested file <strong>"${filename}"</strong> could not be found on the server.</p>
        
        <div class="suggestion">
            <h3>🔍 What happened?</h3>
            <ul>
                <li>The file may still be generating (try refreshing in a few seconds)</li>
                <li>The file may have been moved or deleted</li>
                <li>There might be a typo in the filename</li>
                <li>Browser cache might be showing an old link</li>
            </ul>
        </div>
        
        ${suggestions.length > 0 ? `
        <div class="suggestion">
            <h3>📁 Recent NeRF Models Available:</h3>
            <p>Try downloading one of these recently generated models:</p>
            ${suggestions.map(file => `<a href="/api/download/${file}" class="file-link">📦 ${file}</a>`).join('')}
        </div>
        ` : ''}
        
        <div class="suggestion">
            <h3>💡 Solutions:</h3>
            <ol>
                <li><strong>Refresh and retry:</strong> The file might still be generating</li>
                <li><strong>Generate a new model:</strong> <a href="/test-living-room.html">Go to the test page</a></li>
                <li><strong>Check the main app:</strong> <a href="/">Browse available models</a></li>
            </ol>
        </div>
        
        <div class="suggestion">
            <h3>🛠️ For Developers:</h3>
            <div class="code">
Searched paths:
${possiblePaths.map(p => `• ${p.replace(process.cwd(), '')}`).join('\n')}

File ID: ${filename}
Timestamp: ${new Date().toISOString()}
Recent files found: ${suggestions.length}
            </div>
        </div>
        
        <p><a href="javascript:history.back()">← Go Back</a> | <a href="/">🏠 Home</a> | <a href="/test-living-room.html">🧪 Test NeRF</a></p>
    </div>
</body>
</html>`,
        { 
          status: 404,
          headers: {
            'Content-Type': 'text/html',
          }
        }
      )
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
      case '.blend':
        contentType = 'application/x-blender'
        break
      case '.png':
        contentType = 'image/png'
        break
      case '.jpg':
      case '.jpeg':
        contentType = 'image/jpeg'
        break
      default:
        contentType = 'application/octet-stream'
    }

    // Return file with proper headers
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
    console.error('Error serving file:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
}
