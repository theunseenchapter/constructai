import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Handle requests to /renders/ for 3D model files
  if (request.nextUrl.pathname.startsWith('/renders/')) {
    const response = NextResponse.next()
    
    // Get the file extension
    const pathname = request.nextUrl.pathname
    const ext = pathname.split('.').pop()?.toLowerCase()
    
    // Set appropriate headers for 3D model files
    if (ext && ['obj', 'mtl', 'blend', 'ply', 'gltf', 'glb'].includes(ext)) {
      response.headers.set('Access-Control-Allow-Origin', '*')
      response.headers.set('Access-Control-Allow-Methods', 'GET, OPTIONS')
      response.headers.set('Cache-Control', 'public, max-age=3600')
      
      // Set content type based on extension
      switch (ext) {
        case 'obj':
          response.headers.set('Content-Type', 'model/obj')
          break
        case 'mtl':
          response.headers.set('Content-Type', 'text/plain')
          break
        case 'ply':
          response.headers.set('Content-Type', 'application/ply')
          break
        case 'gltf':
          response.headers.set('Content-Type', 'model/gltf+json')
          break
        case 'glb':
          response.headers.set('Content-Type', 'model/gltf-binary')
          break
        case 'blend':
          response.headers.set('Content-Type', 'application/x-blender')
          break
        default:
          response.headers.set('Content-Type', 'application/octet-stream')
      }
    }
    
    return response
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/renders/:path*',
  ],
}
