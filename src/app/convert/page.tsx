'use client'

import { useState, useRef } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Upload, FileImage, Layers3, Download, Eye, Zap, Cpu, Image as ImageIcon } from 'lucide-react'
import { constructAI } from '@/lib/api'
import NeRFViewer from '@/components/NeRFViewer'

interface NeRFData {
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
    scene_bounds: {
      min: [number, number, number]
      max: [number, number, number]
    }
  }
}

interface Convert3DResult {
  blueprint_id: string
  dimensions: {
    width: number
    height: number
    area: number
  }
  rooms: Array<{
    name: string
    area: number
    type: string
  }>
  walls: Array<{
    start: [number, number]
    end: [number, number]
    height: number
  }>
  model_3d_url: string
  nerf_3d?: NeRFData
}

export default function Convert2DTo3DPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState('')
  const [result, setResult] = useState<Convert3DResult | null>(null)
  const [processingMethod, setProcessingMethod] = useState<'traditional' | 'nerf' | 'hybrid'>('hybrid')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setResult(null)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    handleFileSelect(file)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const processImage = async () => {
    if (!selectedFile) return

    setProcessing(true)
    setProgress(0)
    setResult(null)

    try {
      // Step 1: Traditional 2D → 3D Processing
      setCurrentStep('Analyzing blueprint structure...')
      setProgress(20)
      
      const traditional3D = await constructAI.convert2DTo3D(selectedFile) as Convert3DResult
      
      setCurrentStep('Extracting room layouts...')
      setProgress(40)
      
      if (processingMethod === 'traditional') {
        setProgress(100)
        setCurrentStep('Conversion complete!')
        setResult(traditional3D)
        return
      }

      // Step 2: NeRF Processing (if enabled)
      if (processingMethod === 'nerf' || processingMethod === 'hybrid') {
        setCurrentStep('Generating NeRF 3D model...')
        setProgress(60)

        // Convert traditional result to NeRF input format
        const nerfRequest = await fetch('/api/nerf/generate-3d', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            rooms: traditional3D.rooms || [],
            building_dimensions: {
              total_width: traditional3D.dimensions?.width || 20,
              total_length: traditional3D.dimensions?.height || 20,
              height: 3
            },
            quality_level: 'high',
            training_iterations: 10000
          })
        })

        if (nerfRequest.ok) {
          const nerfResult = await nerfRequest.json()
          setCurrentStep('NeRF training complete!')
          setProgress(90)
          
          // Combine traditional and NeRF results
          const combinedResult: Convert3DResult = {
            ...traditional3D,
            nerf_3d: nerfResult.nerf_3d
          }
          setResult(combinedResult)
        } else {
          // Fallback to traditional result if NeRF fails
          setResult(traditional3D)
        }
      }

      setProgress(100)
      setCurrentStep('Processing complete!')
      
    } catch (error) {
      console.error('Processing error:', error)
      setCurrentStep('Processing failed')
    } finally {
      setProcessing(false)
    }
  }

  const downloadModel = (url: string, filename: string) => {
    try {
      // If the URL is already a full URL, use it directly
      // Otherwise, extract filename and use the download API
      let downloadUrl = url;
      
      if (!url.startsWith('http') && !url.startsWith('/api/download/')) {
        // Extract filename from path/URL
        const extractedFilename = url.split('/').pop() || filename;
        downloadUrl = `/api/download/${extractedFilename}`;
      }
      
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Download failed:', error);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            <Layers3 className="inline-block w-10 h-10 mr-3 text-blue-600" />
            2D → 3D Converter
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Transform your blueprints, floor plans, and architectural drawings into detailed 3D models using AI and NeRF technology
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Upload Blueprint
              </CardTitle>
              <CardDescription>
                Support for JPG, PNG, PDF blueprints and floor plans
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* File Upload Area */}
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer ${
                  isDragging
                    ? 'border-blue-400 bg-blue-50'
                    : selectedFile
                    ? 'border-green-400 bg-green-50'
                    : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*,.pdf"
                  className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                />
                
                {selectedFile ? (
                  <div className="space-y-2">
                    <FileImage className="w-12 h-12 mx-auto text-green-600" />
                    <p className="font-medium text-green-800">{selectedFile.name}</p>
                    <p className="text-sm text-green-600">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <ImageIcon className="w-12 h-12 mx-auto text-gray-400" />
                    <p className="text-lg font-medium text-gray-700">
                      Drop your blueprint here
                    </p>
                    <p className="text-sm text-gray-500">
                      or click to browse files
                    </p>
                  </div>
                )}
              </div>

              {/* Processing Method Selection */}
              <div className="space-y-3">
                <h4 className="font-medium text-gray-900">Processing Method</h4>
                <div className="grid grid-cols-1 gap-2">
                  <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      name="method"
                      value="hybrid"
                      checked={processingMethod === 'hybrid'}
                      onChange={(e) => setProcessingMethod(e.target.value as 'traditional' | 'nerf' | 'hybrid')}
                      className="text-blue-600"
                    />
                    <div className="flex items-center gap-2">
                      <Zap className="w-4 h-4 text-blue-600" />
                      <span className="font-medium">Hybrid (Recommended)</span>
                    </div>
                    <Badge variant="outline" className="ml-auto">Best Quality</Badge>
                  </label>
                  
                  <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      name="method"
                      value="nerf"
                      checked={processingMethod === 'nerf'}
                      onChange={(e) => setProcessingMethod(e.target.value as 'traditional' | 'nerf' | 'hybrid')}
                      className="text-blue-600"
                    />
                    <div className="flex items-center gap-2">
                      <Cpu className="w-4 h-4 text-purple-600" />
                      <span className="font-medium">NeRF Only</span>
                    </div>
                    <Badge variant="outline" className="ml-auto">Photorealistic</Badge>
                  </label>
                  
                  <label className="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      name="method"
                      value="traditional"
                      checked={processingMethod === 'traditional'}
                      onChange={(e) => setProcessingMethod(e.target.value as 'traditional' | 'nerf' | 'hybrid')}
                      className="text-blue-600"
                    />
                    <div className="flex items-center gap-2">
                      <Layers3 className="w-4 h-4 text-green-600" />
                      <span className="font-medium">Traditional</span>
                    </div>
                    <Badge variant="outline" className="ml-auto">Fast</Badge>
                  </label>
                </div>
              </div>

              {/* Process Button */}
              <Button
                onClick={processImage}
                disabled={!selectedFile || processing}
                className="w-full"
                size="lg"
              >
                {processing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Layers3 className="w-4 h-4 mr-2" />
                    Convert to 3D
                  </>
                )}
              </Button>

              {/* Progress */}
              {processing && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">{currentStep}</span>
                    <span className="text-blue-600">{progress}%</span>
                  </div>
                  <Progress value={progress} className="w-full" />
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="w-5 h-5" />
                3D Model Results
              </CardTitle>
              <CardDescription>
                View and download your generated 3D model
              </CardDescription>
            </CardHeader>
            <CardContent>
              {result ? (
                <div className="space-y-6">
                  {/* Project Stats */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">
                        {result.rooms?.length || 0}
                      </div>
                      <div className="text-sm text-blue-800">Rooms</div>
                    </div>
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">
                        {result.dimensions?.area || 0}
                      </div>
                      <div className="text-sm text-green-800">m²</div>
                    </div>
                  </div>

                  {/* NeRF Viewer (if available) */}
                  {result.nerf_3d && (
                    <div className="space-y-3">
                      <h4 className="font-medium text-gray-900">NeRF 3D Model</h4>
                      <NeRFViewer
                        nerfData={result.nerf_3d}
                        className="w-full h-64 rounded-lg"
                      />
                    </div>
                  )}

                  {/* Room List */}
                  {result.rooms && result.rooms.length > 0 && (
                    <div className="space-y-3">
                      <h4 className="font-medium text-gray-900">Detected Rooms</h4>
                      <div className="space-y-2">
                        {result.rooms.map((room, index) => (
                          <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                            <span className="font-medium">{room.name}</span>
                            <div className="text-sm text-gray-600">
                              {room.area}m² • {room.type}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Download Options */}
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-900">Download Options</h4>
                    <div className="grid grid-cols-1 gap-2">
                      <Button
                        variant="outline"
                        onClick={() => downloadModel(result.model_3d_url, `model_${result.blueprint_id}.obj`)}
                        className="w-full justify-start"
                      >
                        <Download className="w-4 h-4 mr-2" />
                        Download OBJ Model
                      </Button>
                      
                      {result.nerf_3d?.model_files?.ply_file && (
                        <Button
                          variant="outline"
                          onClick={() => result.nerf_3d?.model_files?.ply_file && downloadModel(result.nerf_3d.model_files.ply_file, `nerf_${result.blueprint_id}.ply`)}
                          className="w-full justify-start"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download NeRF Mesh (PLY)
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <Layers3 className="w-16 h-16 mx-auto mb-4 opacity-30" />
                  <p>Upload a blueprint to see 3D conversion results</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Features Section */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center space-y-2">
                <Layers3 className="w-8 h-8 mx-auto text-blue-600" />
                <h3 className="font-semibold">Traditional 3D</h3>
                <p className="text-sm text-gray-600">
                  Fast geometric reconstruction from blueprints
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center space-y-2">
                <Zap className="w-8 h-8 mx-auto text-purple-600" />
                <h3 className="font-semibold">NeRF Technology</h3>
                <p className="text-sm text-gray-600">
                  Photorealistic 3D reconstruction using Neural Radiance Fields
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center space-y-2">
                <Download className="w-8 h-8 mx-auto text-green-600" />
                <h3 className="font-semibold">Multiple Formats</h3>
                <p className="text-sm text-gray-600">
                  Export as OBJ, PLY, GLTF for use in any 3D software
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
