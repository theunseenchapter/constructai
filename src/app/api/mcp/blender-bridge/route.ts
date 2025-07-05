import { NextRequest, NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'
import path from 'path'
import fs from 'fs'

const execAsync = promisify(exec)

interface BlenderRequest {
  tool: string
  arguments: Record<string, unknown>
}

interface BlenderResponse {
  success: boolean
  result?: {
    scene_id: string
    obj_file: string
    mtl_file: string
    blend_file: string
    renders: string[]
    file_paths: {
      obj: string
      mtl: string
      blend: string
      renders: string[]
    }
  }
  error?: string
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body: BlenderRequest = await request.json()
    
    if (body.tool !== 'generate_3d_model') {
      return NextResponse.json({
        success: false,
        error: 'Unsupported tool'
      }, { status: 400 })
    }
    
    console.log('🎨 Starting professional Blender 3D generation...')
    console.log('📊 BOQ Configuration:', JSON.stringify(body.arguments, null, 2))
    
    // Call the BOQRenderer Python script
    const pythonScript = path.join(process.cwd(), 'boq_renderer.py')
    const timestamp = Date.now()
    const configPath = path.join(process.cwd(), `temp_boq_config_${timestamp}.json`)
    
    console.log('🔧 Working directory:', process.cwd())
    console.log('🐍 Python script path:', pythonScript)
    console.log('📄 Config file path:', configPath)
    
    // Write the config to a temporary file with timestamp
    fs.writeFileSync(configPath, JSON.stringify(body.arguments, null, 2))
    console.log('📝 Config written to:', configPath)
    
    try {
      // Run the BOQRenderer with force fresh generation
      const command = `python "${pythonScript}" "${configPath}"`
      console.log('⚡ Running command:', command)
      console.log('⏰ Timestamp:', timestamp)
      
      const { stdout, stderr } = await execAsync(command, { 
        cwd: process.cwd(),
        timeout: 120000 // 2 minutes timeout
      })
      
      if (stderr) {
        console.warn('⚠️ Blender stderr:', stderr)
      }
      
      console.log('✨ Blender stdout:', stdout)
      
      // Parse the output to get file paths
      let scene_id = ''
      let obj_file = ''
      let mtl_file = ''
      let blend_file = ''
      const renders: string[] = []
      
      // Parse the stdout for file paths
      const lines = stdout.split('\n')
      for (const line of lines) {
        if (line.includes('SCENE_ID:')) {
          scene_id = line.split('SCENE_ID:')[1]?.trim() || ''
        } else if (line.includes('OBJ_FILE:')) {
          obj_file = line.split('OBJ_FILE:')[1]?.trim() || ''
        } else if (line.includes('MTL_FILE:')) {
          mtl_file = line.split('MTL_FILE:')[1]?.trim() || ''
        } else if (line.includes('BLEND_FILE:')) {
          blend_file = line.split('BLEND_FILE:')[1]?.trim() || ''
        } else if (line.includes('RENDER_PNG:')) {
          const renderPath = line.split('RENDER_PNG:')[1]?.trim()
          if (renderPath) {
            renders.push(renderPath)
          }
        }
      }
      
      console.log('📄 Parsed files:', { scene_id, obj_file, mtl_file, blend_file, renders })
      
      // Copy files to public directory for access (with cache-busting)
      const publicDir = path.join(process.cwd(), 'public', 'renders')
      if (!fs.existsSync(publicDir)) {
        fs.mkdirSync(publicDir, { recursive: true })
      }
      
      const copiedFiles = {
        obj: '',
        mtl: '',
        blend: '',
        renders: [] as string[]
      }
      
      // Copy OBJ file
      if (obj_file && fs.existsSync(obj_file)) {
        const objFileName = path.basename(obj_file)
        const objDestPath = path.join(publicDir, objFileName)
        fs.copyFileSync(obj_file, objDestPath)
        copiedFiles.obj = `/renders/${objFileName}?v=${timestamp}`
        console.log('📄 Copied OBJ file:', copiedFiles.obj)
      } else {
        console.log('⚠️ OBJ file not found:', obj_file)
      }
      
      // Copy MTL file
      if (mtl_file && fs.existsSync(mtl_file)) {
        const mtlFileName = path.basename(mtl_file)
        const mtlDestPath = path.join(publicDir, mtlFileName)
        fs.copyFileSync(mtl_file, mtlDestPath)
        copiedFiles.mtl = `/renders/${mtlFileName}?v=${timestamp}`
        console.log('🎨 Copied MTL file:', copiedFiles.mtl)
      } else {
        console.log('⚠️ MTL file not found:', mtl_file)
      }
      
      // Copy BLEND file
      if (blend_file && fs.existsSync(blend_file)) {
        const blendFileName = path.basename(blend_file)
        const blendDestPath = path.join(publicDir, blendFileName)
        fs.copyFileSync(blend_file, blendDestPath)
        copiedFiles.blend = `/renders/${blendFileName}?v=${timestamp}`
        console.log('🔧 Copied BLEND file:', copiedFiles.blend)
      } else {
        console.log('⚠️ BLEND file not found:', blend_file)
      }
      
      // Copy render PNG files
      for (const renderFile of renders) {
        if (fs.existsSync(renderFile)) {
          const renderFileName = path.basename(renderFile)
          const renderDestPath = path.join(publicDir, renderFileName)
          fs.copyFileSync(renderFile, renderDestPath)
          copiedFiles.renders.push(`/renders/${renderFileName}?v=${timestamp}`)
          console.log('🖼️ Copied render file:', `/renders/${renderFileName}?v=${timestamp}`)
        } else {
          console.log('⚠️ Render file not found:', renderFile)
        }
      }
      
      // Clean up temp config file
      if (fs.existsSync(configPath)) {
        fs.unlinkSync(configPath)
      }
      
      const response: BlenderResponse = {
        success: true,
        result: {
          scene_id: scene_id || 'unknown',
          obj_file: copiedFiles.obj,
          mtl_file: copiedFiles.mtl,
          blend_file: copiedFiles.blend,
          renders: copiedFiles.renders,
          file_paths: copiedFiles
        }
      }
      
      console.log('✅ Professional Blender 3D generation completed:', response.result)
      console.log('🔍 API Response structure:', JSON.stringify(response, null, 2))
      return NextResponse.json(response)
      
    } catch (error) {
      console.error('❌ Blender rendering failed:', error)
      
      // Clean up temp config file
      if (fs.existsSync(configPath)) {
        fs.unlinkSync(configPath)
      }
      
      return NextResponse.json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }, { status: 500 })
    }
    
  } catch (error) {
    console.error('❌ API request failed:', error)
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Invalid request'
    }, { status: 400 })
  }
}
