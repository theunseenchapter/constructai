import React, { useRef, useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Download, Eye, RotateCcw, ZoomIn, ZoomOut, Camera, Play, Pause } from 'lucide-react'

interface NeRFViewerProps {
  nerfData: {
    nerf_id: string
    model_files: {
      obj_file?: string
      ply_file?: string
      gltf_file?: string
      texture_files: string[]
      novel_views: string[]
    }
    metadata: {
      training_time: number
      iteration_count: number
      reconstruction_quality: number
      scene_bounds: { min: [number, number, number]; max: [number, number, number] }
    }
  }
  className?: string
}

export default function NeRFViewer({ nerfData, className = '' }: NeRFViewerProps) {
  const viewerRef = useRef<HTMLDivElement>(null)
  const [currentView, setCurrentView] = useState(0)
  const [isPlayingAnimation, setIsPlayingAnimation] = useState(false)
  const [loadingProgress, setLoadingProgress] = useState(0)
  const [viewerInitialized, setViewerInitialized] = useState(false)

  const createMockNeRFViewer = React.useCallback(() => {
    if (!viewerRef.current) return

    // Create a canvas element for the NeRF viewer
    const canvas = document.createElement('canvas')
    canvas.width = viewerRef.current.clientWidth
    canvas.height = viewerRef.current.clientHeight
    canvas.style.width = '100%'
    canvas.style.height = '100%'
    canvas.style.background = 'linear-gradient(45deg, #1a1a1a, #2a2a2a)'
    
    // Add some mock 3D content text
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.fillStyle = '#ffffff'
      ctx.font = '16px Arial'
      ctx.textAlign = 'center'
      ctx.fillText('NeRF 3D Model Viewer', canvas.width / 2, canvas.height / 2 - 40)
      ctx.fillText(`Quality: ${(nerfData.metadata.reconstruction_quality * 100).toFixed(1)}%`, canvas.width / 2, canvas.height / 2)
      ctx.fillText(`Iterations: ${nerfData.metadata.iteration_count.toLocaleString()}`, canvas.width / 2, canvas.height / 2 + 20)
      ctx.fillText('Interactive NeRF rendering would appear here', canvas.width / 2, canvas.height / 2 + 60)
    }

    viewerRef.current.innerHTML = ''
    viewerRef.current.appendChild(canvas)
  }, [nerfData.metadata.reconstruction_quality, nerfData.metadata.iteration_count])

  // Initialize NeRF viewer when component mounts
  useEffect(() => {
    const initializeNeRFViewer = async () => {
      if (!viewerRef.current) return

      console.log('🎯 Initializing NeRF viewer for:', nerfData.nerf_id)
      
      // Simulate loading progress
      for (let i = 0; i <= 100; i += 10) {
        setLoadingProgress(i)
        await new Promise(resolve => setTimeout(resolve, 100))
      }

      // In a real implementation, this would load Three.js and set up NeRF rendering
      // For now, we'll create a mock 3D viewer
      createMockNeRFViewer()
      setViewerInitialized(true)
    }

    initializeNeRFViewer()
  }, [nerfData.nerf_id, createMockNeRFViewer])

  const cycleNovelViews = () => {
    if (nerfData.model_files.novel_views.length === 0) return
    
    setIsPlayingAnimation(true)
    const interval = setInterval(() => {
      setCurrentView(prev => {
        const next = (prev + 1) % nerfData.model_files.novel_views.length
        if (next === 0) {
          clearInterval(interval)
          setIsPlayingAnimation(false)
        }
        return next
      })
    }, 800) // Change view every 800ms
  }

  const resetCamera = () => {
    // In real implementation, this would reset the Three.js camera
    createMockNeRFViewer()
  }

  const downloadModel = (fileType: 'obj' | 'ply' | 'gltf') => {
    const fileMap = {
      obj: nerfData.model_files.obj_file,
      ply: nerfData.model_files.ply_file,
      gltf: nerfData.model_files.gltf_file
    }
    
    const filePath = fileMap[fileType]
    if (filePath) {
      const link = document.createElement('a')
      link.href = filePath.startsWith('/') ? filePath : `/${filePath}`
      link.download = `nerf_model_${nerfData.nerf_id}.${fileType}`
      link.click()
    }
  }

  const downloadTextures = () => {
    nerfData.model_files.texture_files.forEach((textureFile: string, index: number) => {
      const link = document.createElement('a')
      link.href = textureFile.startsWith('/') ? textureFile : `/${textureFile}`
      link.download = `nerf_texture_${index + 1}_${nerfData.nerf_id}.png`
      link.click()
    })
  }

  const qualityColor = nerfData.metadata.reconstruction_quality > 0.9 ? 'bg-green-500' :
                      nerfData.metadata.reconstruction_quality > 0.8 ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <Card className={`w-full ${className}`}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Camera className="w-5 h-5" />
            NeRF 3D Model
            <Badge variant="secondary">Neural Radiance Fields</Badge>
          </CardTitle>
          <div className="flex items-center gap-2">
            <Badge className={qualityColor}>
              {(nerfData.metadata.reconstruction_quality * 100).toFixed(1)}% Quality
            </Badge>
            <Badge variant="outline">
              {(nerfData.metadata.training_time / 1000).toFixed(1)}s Training
            </Badge>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* NeRF Viewer Container */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ height: '400px' }}>
          {!viewerInitialized && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-900">
              <div className="text-white mb-4">Loading NeRF Model...</div>
              <Progress value={loadingProgress} className="w-64" />
              <div className="text-sm text-gray-400 mt-2">{loadingProgress}%</div>
            </div>
          )}
          
          <div ref={viewerRef} className="w-full h-full" />
          
          {/* Viewer Controls Overlay */}
          {viewerInitialized && (
            <div className="absolute bottom-4 left-4 right-4 flex justify-between items-center">
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={resetCamera}
                  className="bg-black/50 text-white hover:bg-black/70"
                >
                  <RotateCcw className="w-4 h-4" />
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  className="bg-black/50 text-white hover:bg-black/70"
                >
                  <ZoomIn className="w-4 h-4" />
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  className="bg-black/50 text-white hover:bg-black/70"
                >
                  <ZoomOut className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="text-xs text-white bg-black/50 px-2 py-1 rounded">
                NeRF ID: {nerfData.nerf_id}
              </div>
            </div>
          )}
        </div>

        {/* Novel Views */}
        {nerfData.model_files.novel_views.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="font-medium">Novel Views ({nerfData.model_files.novel_views.length})</h4>
              <Button
                size="sm"
                variant="outline"
                onClick={cycleNovelViews}
                disabled={isPlayingAnimation}
                className="flex items-center gap-2"
              >
                {isPlayingAnimation ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                {isPlayingAnimation ? 'Playing...' : 'Cycle Views'}
              </Button>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {nerfData.model_files.novel_views.map((view: string, index: number) => (
                <Button
                  key={index}
                  variant={currentView === index ? "default" : "outline"}
                  size="sm"
                  onClick={() => setCurrentView(index)}
                  className="h-20 flex flex-col items-center justify-center text-xs"
                >
                  <Eye className="w-4 h-4 mb-1" />
                  View {index + 1}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Download Options */}
        <div className="space-y-3">
          <h4 className="font-medium">Download NeRF Assets</h4>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {nerfData.model_files.obj_file && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => downloadModel('obj')}
                className="flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                OBJ Model
              </Button>
            )}
            
            {nerfData.model_files.ply_file && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => downloadModel('ply')}
                className="flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                PLY Model
              </Button>
            )}
            
            {nerfData.model_files.gltf_file && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => downloadModel('gltf')}
                className="flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                GLTF Model
              </Button>
            )}
            
            {nerfData.model_files.texture_files.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={downloadTextures}
                className="flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Textures ({nerfData.model_files.texture_files.length})
              </Button>
            )}
          </div>
        </div>

        {/* NeRF Metadata */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
          <div className="text-center">
            <div className="text-sm text-gray-600">Iterations</div>
            <div className="font-semibold">{nerfData.metadata.iteration_count.toLocaleString()}</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-600">Training Time</div>
            <div className="font-semibold">{(nerfData.metadata.training_time / 1000).toFixed(1)}s</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-600">Quality Score</div>
            <div className="font-semibold">{(nerfData.metadata.reconstruction_quality * 100).toFixed(1)}%</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-600">Scene Size</div>
            <div className="font-semibold text-xs">
              {nerfData.metadata.scene_bounds.max[0] - nerfData.metadata.scene_bounds.min[0]}×
              {nerfData.metadata.scene_bounds.max[2] - nerfData.metadata.scene_bounds.min[2]}×
              {nerfData.metadata.scene_bounds.max[1]}m
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
