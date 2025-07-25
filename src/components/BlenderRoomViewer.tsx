'use client'

import { useState, useEffect, useCallback } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Eye, Download, RefreshCw, Camera, Layers3 } from 'lucide-react'
import { mcpClient } from '@/lib/mcp-client'
import SafeImage from '@/components/SafeImage'

interface BlenderRender {
  id: string
  url: string
  type: 'single' | '360'
  timestamp: number
  status: 'pending' | 'completed' | 'failed'
}

interface Professional3DData {
  scene_id: string
  blender_files: {
    obj_file: string
    mtl_file: string
    blend_file: string
    png_files: string[]
  }
  metadata: {
    layout_type: string
    style: string
    quality_level: string
    render_engine: string
    total_objects: number
    total_materials: number
    render_time: string
  }
  boq_data: {
    total_cost: number
    items: Array<{
      category: string
      quantity: number
      unit: string
      rate: number
      amount: number
    }>
  }
}

interface MCPServerStatus {
  connected: boolean
  version?: string
  error?: string
}

export default function BlenderRoomViewer() {
  const [renders, setRenders] = useState<BlenderRender[]>([])
  const [selectedRender, setSelectedRender] = useState<BlenderRender | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [mcpStatus, setMcpStatus] = useState<MCPServerStatus>({ connected: false })
  const [professional3D, setProfessional3D] = useState<Professional3DData | null>(null)

  const connectToMCP = useCallback(async () => {
    try {
      setIsLoading(true)
      const initialized = await mcpClient.initialize()
      setMcpStatus({ 
        connected: initialized, 
        version: initialized ? "1.0.0" : undefined,
        error: initialized ? undefined : "Failed to connect to MCP server"
      })
      return initialized
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      setMcpStatus({ connected: false, error: errorMessage })
      return false
    } finally {
      setIsLoading(false)
    }
  }, [])

  const createProfessional3D = async () => {
    if (!mcpStatus.connected) {
      const connected = await connectToMCP()
      if (!connected) return
    }

    try {
      setIsLoading(true)
      
      // Create scene with professional configuration
      const sceneConfig = {
        rooms: [
          {
            name: "Living Room",
            type: "living_room",
            dimensions: { width: 6, height: 4, length: 8 },
            position: { x: 0, y: 0, z: 0 },
            walls: [
              { start: [0, 0], end: [6, 0], height: 3.2, thickness: 0.2 },
              { start: [6, 0], end: [6, 4], height: 3.2, thickness: 0.2 },
              { start: [6, 4], end: [0, 4], height: 3.2, thickness: 0.2 },
              { start: [0, 4], end: [0, 0], height: 3.2, thickness: 0.2 }
            ],
            furniture: [
              { type: "sofa", position: [1, 2, 0], material: "leather" },
              { type: "coffee_table", position: [3, 2, 0], material: "wood" },
              { type: "tv_stand", position: [5, 0.5, 0], material: "metal" }
            ]
          }
        ],
        lighting: {
          natural: { windows: 2, intensity: 0.8 },
          artificial: { ceiling_lights: 3, lamps: 2 }
        },
        materials: {
          walls: "painted_wall",
          floor: "hardwood",
          ceiling: "white_paint"
        }
      }

      // Call MCP to create scene
      const sceneResult = await mcpClient.callTool('create_3d_scene', sceneConfig)
      
      // Render single view
      const singleRender = await mcpClient.callTool('render_scene', { 
        view_type: 'single',
        quality: 'high',
        resolution: { width: 1920, height: 1080 }
      })

      // Create professional 3D data structure
      const professional3DData: Professional3DData = {
        scene_id: sceneResult.scene_id || `scene_${Date.now()}`,
        blender_files: {
          obj_file: singleRender.files?.obj_file || '/renders/model.obj',
          mtl_file: singleRender.files?.mtl_file || '/renders/model.mtl',
          blend_file: singleRender.files?.blend_file || '/renders/scene.blend',
          png_files: singleRender.files?.png_files || ['/renders/render.png']
        },
        metadata: {
          layout_type: 'architectural_floorplan',
          style: 'professional_architecture',
          quality_level: 'detailed',
          render_engine: 'Cycles with OptiX',
          total_objects: singleRender.metadata?.total_objects || 15,
          total_materials: singleRender.metadata?.total_materials || 8,
          render_time: singleRender.metadata?.render_time || '2.5 minutes'
        },
        boq_data: {
          total_cost: 45000,
          items: [
            { category: 'Walls', quantity: 48, unit: 'sq.m', rate: 150, amount: 7200 },
            { category: 'Flooring', quantity: 24, unit: 'sq.m', rate: 200, amount: 4800 },
            { category: 'Furniture', quantity: 1, unit: 'set', rate: 25000, amount: 25000 },
            { category: 'Lighting', quantity: 5, unit: 'units', rate: 800, amount: 4000 },
            { category: 'Paint & Finish', quantity: 100, unit: 'sq.m', rate: 40, amount: 4000 }
          ]
        }
      }

      setProfessional3D(professional3DData)
      
      // Add to renders list
      const newRender: BlenderRender = {
        id: professional3DData.scene_id,
        url: professional3DData.blender_files.png_files[0],
        type: 'single',
        timestamp: Date.now(),
        status: 'completed'
      }
      
      setRenders(prev => [newRender, ...prev])
      setSelectedRender(newRender)
      
    } catch (error) {
      console.error('Error creating professional 3D scene:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const renderScene = async (type: 'single' | '360') => {
    if (!mcpStatus.connected) {
      const connected = await connectToMCP()
      if (!connected) return
    }

    try {
      setIsLoading(true)
      
      const renderResult = await mcpClient.callTool('render_scene', { 
        view_type: type,
        quality: 'high'
      })
      
      const newRender: BlenderRender = {
        id: `${Date.now()}_${type}`,
        url: renderResult.files?.png_files?.[0] || generateMockRenderUrl(type),
        type,
        timestamp: Date.now(),
        status: 'completed'
      }

      setRenders(prev => [newRender, ...prev])
      setSelectedRender(newRender)
      
    } catch (error) {
      console.error('Error rendering scene:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const generateMockRenderUrl = (type: 'single' | '360'): string => {
    const svg = `
      <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="600" fill="#f0f8ff"/>
        <text x="400" y="300" text-anchor="middle" font-size="24" fill="#333">
          ${type === '360' ? '360° View' : 'Single View'} Render
        </text>
      </svg>
    `
    return `data:image/svg+xml;base64,${btoa(svg)}`
  }

  useEffect(() => {
    connectToMCP()
  }, [connectToMCP])

  return (
    <div className="blender-room-viewer p-6 max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">🎨 Blender 3D Room Viewer</h1>
        <p className="text-gray-600">
          Create and visualize architectural spaces with professional 3D rendering
        </p>
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Badge variant={mcpStatus.connected ? "default" : "secondary"}>
            {mcpStatus.connected ? "Connected" : "Disconnected"}
          </Badge>
          {mcpStatus.error && (
            <Badge variant="destructive">Error: {mcpStatus.error}</Badge>
          )}
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={connectToMCP}
            disabled={isLoading}
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            {isLoading ? 'Connecting...' : 'Reconnect'}
          </Button>
        </div>
      </div>

      {/* Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <Card>
          <CardHeader>
            <CardTitle>Create Professional 3D Scene</CardTitle>
            <CardDescription>Generate a complete architectural visualization</CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={createProfessional3D}
              disabled={isLoading}
              className="w-full"
            >
              <Layers3 className="w-4 h-4 mr-2" />
              {isLoading ? 'Creating...' : 'Create Professional Scene'}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Render Options</CardTitle>
            <CardDescription>Generate different view types</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button 
              onClick={() => renderScene('single')}
              disabled={isLoading}
              variant="outline"
              className="w-full"
            >
              <Camera className="w-4 h-4 mr-2" />
              Single View
            </Button>
            <Button 
              onClick={() => renderScene('360')}
              disabled={isLoading}
              variant="outline"
              className="w-full"
            >
              <Eye className="w-4 h-4 mr-2" />
              360° View
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Professional 3D Results */}
      {professional3D && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Professional 3D Scene Generated</CardTitle>
            <CardDescription>Complete architectural visualization with BOQ</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Preview Images */}
              <div>
                <h3 className="font-medium mb-3">3D Renders</h3>
                <div className="grid grid-cols-2 gap-2">
                  {professional3D.blender_files.png_files.map((file, index) => (
                    <div key={index} className="relative group cursor-pointer">
                      <SafeImage
                        src={file} 
                        alt={`Render ${index + 1}`}
                        className="w-full h-32 object-cover rounded-lg border"
                        onClick={() => {
                          try {
                            const normalizedPath = file.startsWith('/') ? file : `/${file}`;
                            const fullUrl = new URL(normalizedPath, window.location.origin).href;
                            window.open(fullUrl, '_blank');
                          } catch (error) {
                            console.error('Failed to open image:', error);
                          }
                        }}
                      />
                      <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300 rounded-lg flex items-center justify-center">
                        <Eye className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      </div>
                    </div>
                  ))}
                </div>
                
                {/* Download Links */}
                <div className="flex flex-wrap gap-2 mt-4">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      try {
                        // Extract filename from path
                        const objPath = professional3D.blender_files.obj_file;
                        const filename = objPath.split('/').pop() || objPath;
                        
                        // Use the download API
                        const downloadUrl = `/api/download/${filename}`;
                        
                        // Create a temporary link for download
                        const link = document.createElement('a');
                        link.href = downloadUrl;
                        link.download = filename;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                      } catch (error) {
                        console.error('Failed to download OBJ file:', error);
                      }
                    }}
                    className="text-blue-700 border-blue-300 hover:bg-blue-50"
                  >
                    📄 Download OBJ Model
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      try {
                        const normalizedPath = professional3D.blender_files.blend_file.startsWith('/') 
                          ? professional3D.blender_files.blend_file 
                          : `/${professional3D.blender_files.blend_file}`;
                        const fullUrl = new URL(normalizedPath, window.location.origin).href;
                        window.open(fullUrl, '_blank');
                      } catch (error) {
                        console.error('Failed to open Blend file:', error);
                      }
                    }}
                    className="text-purple-700 border-purple-300 hover:bg-purple-50"
                  >
                    🔧 Download Blend File
                  </Button>
                  <Badge variant="outline" className="text-green-700 border-green-300">
                    Scene ID: {professional3D.scene_id.slice(0, 8)}...
                  </Badge>
                </div>
              </div>

              {/* BOQ Data */}
              <div>
                <h3 className="font-medium mb-3">Bill of Quantities</h3>
                <div className="space-y-2">
                  {professional3D.boq_data.items.map((item, index) => (
                    <div key={index} className="flex justify-between text-sm">
                      <span>{item.category}</span>
                      <span>${item.amount.toLocaleString()}</span>
                    </div>
                  ))}
                  <div className="border-t pt-2 font-medium">
                    <div className="flex justify-between">
                      <span>Total Cost</span>
                      <span>${professional3D.boq_data.total_cost.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Render Gallery */}
      <Card>
        <CardHeader>
          <CardTitle>Render Gallery</CardTitle>
          <CardDescription>View all generated renders</CardDescription>
        </CardHeader>
        <CardContent>
          {renders.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No renders yet. Create a scene to get started!</p>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {renders.map((render) => (
                <div 
                  key={render.id}
                  className={`relative cursor-pointer rounded-lg overflow-hidden border-2 ${
                    selectedRender?.id === render.id ? 'border-blue-500' : 'border-gray-200'
                  }`}
                  onClick={() => setSelectedRender(render)}
                >
                  <SafeImage
                    src={render.url} 
                    alt={`${render.type} render`}
                    className="w-full h-24 object-cover"
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-xs p-1">
                    {render.type === '360' ? '360°' : 'Single'}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Selected Render Display */}
      {selectedRender && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Selected Render</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative">
              <SafeImage
                src={selectedRender.url} 
                alt="Selected render"
                className="w-full max-h-96 object-contain rounded-lg"
                onClick={() => {
                  try {
                    const normalizedPath = selectedRender.url.startsWith('/') ? selectedRender.url : `/${selectedRender.url}`;
                    const fullUrl = new URL(normalizedPath, window.location.origin).href;
                    window.open(fullUrl, '_blank');
                  } catch (error) {
                    console.error('Failed to open image:', error);
                  }
                }}
              />
              <div className="absolute top-2 right-2 flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const link = document.createElement('a');
                    link.href = selectedRender.url;
                    link.download = `render_${selectedRender.type}_${selectedRender.timestamp}.png`;
                    link.click();
                  }}
                  className="bg-white/90 backdrop-blur-sm"
                >
                  📥 Download
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    try {
                      const normalizedPath = selectedRender.url.startsWith('/') ? selectedRender.url : `/${selectedRender.url}`;
                      const fullUrl = new URL(normalizedPath, window.location.origin).href;
                      window.open(fullUrl, '_blank');
                    } catch (error) {
                      console.error('Failed to open image:', error);
                    }
                  }}
                  className="bg-white/90 backdrop-blur-sm"
                >
                  🔍 View Full Size
                </Button>
              </div>
            </div>
            <div className="mt-4 text-sm text-gray-600">
              <div className="flex justify-center items-center gap-4">
                <span>Type: {selectedRender.type === '360' ? '360° View' : 'Single View'}</span>
                <span>Created: {new Date(selectedRender.timestamp).toLocaleString()}</span>
                <Badge variant="outline">{selectedRender.status}</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}