'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ThreeJSViewer from "./ThreeJSViewer"
import NeRFViewer from "./NeRFViewer"
import { 
  Building2, 
  Calculator, 
  Download, 
  Layers3, 
  Zap, 
  CheckCircle,
  AlertCircle,
  Loader2,
  Sparkles,
  Palette,
  Home,
  TreePine,
  Sofa,
  Monitor,
  Star,
  Wand2
} from "lucide-react"

// Interface definitions
interface Enhanced3DProjectSpecs {
  total_area: number
  num_bedrooms: number
  num_living_rooms: number
  num_kitchens: number
  num_bathrooms: number
  num_floors: number
  construction_type: string
  quality_grade: string
  location: string
  room_height: number
  wall_thickness: number
  doors_per_bedroom: number
  doors_per_living_room: number
  doors_per_kitchen: number
  doors_per_bathroom: number
  windows_per_bedroom: number
  windows_per_living_room: number
  windows_per_kitchen: number
  windows_per_bathroom: number
  main_door_type: string
  interior_door_type: string
  window_type: string
  room_layout: string
  include_balcony: boolean
  balcony_area: number
  num_dining_rooms: number
  num_study_rooms: number
  num_utility_rooms: number
  num_guest_rooms: number
  num_store_rooms: number
  ceiling_type: string
  flooring_type: string
}

interface VisualizationData {
  rooms: Array<{
    name: string
    width: number
    length: number
    height: number
    area: number
    room_type?: string
    position?: { x: number; y: number }
  }>
  total_area: number
  estimated_cost: number
  blender_files?: {
    scene_id: string
    obj_file: string
    mtl_file: string
    blend_file: string
    renders: string[]
  }
}

interface BOQResult {
  total_cost: number
  items: Array<{
    item: string
    quantity: number
    unit: string
    rate: number
    amount: number
  }>
  room_3d_data?: {
    visualization_data: VisualizationData
  }
  professional_3d?: {
    scene_id: string
    quality: string
    renderer: string
    samples: number
    resolution: string
    status?: string
    obj_url?: string
    mtl_url?: string
    blend_url?: string
    preview_url?: string
    blender_files?: {
      obj: string
      mtl: string
      blend_file: string
      renders: string[]
    }
  }
  nerf_3d?: {
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
}

export default function Enhanced3DBOQ() {
  // State management
  const [specs, setSpecs] = useState<Enhanced3DProjectSpecs>({
    total_area: 0,
    num_bedrooms: 0,
    num_living_rooms: 0,
    num_kitchens: 0,
    num_bathrooms: 0,
    num_floors: 1,
    construction_type: '',
    quality_grade: '',
    location: '',
    room_height: 0,
    wall_thickness: 0,
    doors_per_bedroom: 0,
    doors_per_living_room: 0,
    doors_per_kitchen: 0,
    doors_per_bathroom: 0,
    windows_per_bedroom: 0,
    windows_per_living_room: 0,
    windows_per_kitchen: 0,
    windows_per_bathroom: 0,
    main_door_type: '',
    interior_door_type: '',
    window_type: '',
    room_layout: '',
    include_balcony: false,
    balcony_area: 0,
    num_dining_rooms: 0,
    num_study_rooms: 0,
    num_utility_rooms: 0,
    num_guest_rooms: 0,
    num_store_rooms: 0,
    ceiling_type: '',
    flooring_type: ''
  })

  // Enhanced 3D Features State
  const [enhancedFeatures, setEnhancedFeatures] = useState({
    furniture: true,
    landscaping: true,
    premiumMaterials: true,
    interiorDetails: true,
    lighting: true,
    textures: true
  })

  const [architecturalStyle, setArchitecturalStyle] = useState('modern')
  const [qualityLevel, setQualityLevel] = useState('professional')
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [showAlert, setShowAlert] = useState(false)
  const [alertMessage, setAlertMessage] = useState('')
  const [alertType, setAlertType] = useState<'success' | 'error'>('success')
  const [currentStep, setCurrentStep] = useState('initializing')
  const [result, setResult] = useState<BOQResult | null>(null)
  const [blenderProcessing, setBlenderProcessing] = useState(false)
  const [activeTab, setActiveTab] = useState('generator')

  // Test with a recent generated model
  useEffect(() => {
    // For testing, set a dummy result with a recent model
    // Test data (commented out)
    /*
    const testResult = {
      total_cost: 240000,
      items: [
        { item: 'Cement', quantity: 24, unit: 'bags', rate: 400, amount: 9600 },
        { item: 'Steel', quantity: 60, unit: 'kg', rate: 60, amount: 3600 },
      ],
      professional_3d: {
        scene_id: 'architectural_detailed_1752083732496',
        quality: 'professional',
        renderer: 'blender_cycles',
        samples: 512,
        resolution: '3840x2160',
        obj_url: '/renders/architectural_detailed_1752083732496.obj',
        mtl_url: '/renders/architectural_detailed_1752083732496.mtl',
        blender_files: {
          obj: 'renders/architectural_detailed_1752083732496.obj',
          mtl: 'renders/architectural_detailed_1752083732496.mtl',
          blend_file: 'renders/architectural_detailed_1752083732496.blend',
          renders: ['renders/architectural_detailed_1752083732496.png']
        }
      }
    }
    
    // Uncomment next line to test with real data
    // setResult(testResult)
    */
  }, [])

  const showNotification = (message: string, type: 'success' | 'error') => {
    setAlertMessage(message)
    setAlertType(type)
    setShowAlert(true)
    setTimeout(() => setShowAlert(false), 5000)
  }

  const generateRandomVariations = () => {
    // Add random variations to prevent identical layouts
    const variations = {
      colorScheme: ['warm', 'cool', 'neutral', 'vibrant'][Math.floor(Math.random() * 4)],
      furnitureStyle: ['modern', 'classic', 'minimalist', 'eclectic'][Math.floor(Math.random() * 4)],
      lightingVariation: Math.random() > 0.5 ? 'bright' : 'ambient',
      materialTexture: Math.random() > 0.5 ? 'smooth' : 'textured',
      roomArrangement: Math.random() > 0.5 ? 'symmetrical' : 'asymmetrical'
    }
    return variations
  }

  const generateModel = async () => {
    // Validate required fields
    if (!specs.total_area || specs.total_area <= 0) {
      showNotification('Please enter a valid total area', 'error')
      return
    }
    
    if (!specs.construction_type) {
      showNotification('Please select a construction type', 'error')
      return
    }
    
    if (!specs.quality_grade) {
      showNotification('Please select a quality grade', 'error')
      return
    }
    
    if (!specs.room_layout) {
      showNotification('Please select a room layout', 'error')
      return
    }
    
    const totalRooms = (specs.num_bedrooms || 0) + (specs.num_living_rooms || 0) + 
                      (specs.num_kitchens || 0) + (specs.num_bathrooms || 0)
    
    if (totalRooms === 0) {
      showNotification('Please add at least one room (bedroom, living room, kitchen, or bathroom)', 'error')
      return
    }
    
    setIsGenerating(true)
    setProgress(0)
    setCurrentStep('initializing')
    
    try {
      // Step 1: Initialize
      setProgress(10)
      setCurrentStep('Initializing professional 3D generation...')
      console.log('🏗️ Generating BOQ with professional 3D visualization...')
      
      // Generate random variations for unique designs
      const variations = generateRandomVariations()
      console.log('🎨 Design variations:', variations)
      
      // Step 2: Generate BOQ data from backend
      setProgress(20)
      setCurrentStep('Analyzing room specifications...')
      const boqResponse = await fetch('/api/boq/estimate-3d', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...specs,
          architectural_style: architecturalStyle,
          quality_level: qualityLevel,
          enhanced_features: enhancedFeatures
        }),
      })

      if (!boqResponse.ok) {
        throw new Error(`BOQ API error! status: ${boqResponse.status}`)
      }

      const boqData: BOQResult = await boqResponse.json()
      console.log('💰 BOQ Data received:', boqData)
      console.log('🔍 Professional 3D data:', boqData.professional_3d)
      console.log('🔍 Blender files:', boqData.professional_3d?.blender_files)
      
      // Check if professional_3d data is already included in BOQ response
      if (boqData.professional_3d && boqData.professional_3d.blender_files) {
        console.log('✅ Professional 3D data already included in BOQ response')
        console.log('🔍 Full professional_3d object:', JSON.stringify(boqData.professional_3d, null, 2))
        console.log('🔍 Blender files object:', JSON.stringify(boqData.professional_3d.blender_files, null, 2))
        setProgress(100)
        setCurrentStep('Generation complete!')
        setResult(boqData)
        console.log('🔍 Result state set to:', JSON.stringify(boqData, null, 2))
        showNotification('3D model generated successfully!', 'success')
        
        // Auto-switch to Results tab
        setTimeout(() => {
          setActiveTab('results')
        }, 1000)
        return
      }
      
      // Step 3: Generate professional 3D visualization using advanced Blender renderer
      if (boqData.room_3d_data?.visualization_data?.rooms) {
        setBlenderProcessing(true)
        setProgress(30)
        setCurrentStep('Generating intelligent layout...')
        
        // Calculate building dimensions from room data
        const rooms = boqData.room_3d_data.visualization_data.rooms
        const maxX = Math.max(...rooms.map((r) => (r.position?.x || 0) + r.width))
        const maxZ = Math.max(...rooms.map((r) => (r.position?.y || 0) + r.length))
        const maxHeight = Math.max(...rooms.map((r) => r.height))
        
        const buildingDimensions = {
          total_width: Math.max(maxX, 30),
          total_length: Math.max(maxZ, 30),
          height: maxHeight + 2
        }
        
        const professionalSceneConfig = {
          rooms: rooms.map((room) => ({
            name: room.name,
            type: room.room_type || 'bedroom',
            width: room.width,
            length: room.length,
            height: room.height,
            area: room.width * room.length,
            // Add detailed room specifications
            features: {
              furniture: enhancedFeatures.furniture,
              lighting: enhancedFeatures.lighting,
              flooring: specs.flooring_type || 'tiles',
              walls: specs.construction_type || 'RCC',
              ceiling: specs.ceiling_type || 'false_ceiling',
              doors: room.room_type === 'bedroom' ? specs.doors_per_bedroom : 
                     room.room_type === 'living_room' ? specs.doors_per_living_room :
                     room.room_type === 'kitchen' ? specs.doors_per_kitchen :
                     room.room_type === 'bathroom' ? specs.doors_per_bathroom : 1,
              windows: room.room_type === 'bedroom' ? specs.windows_per_bedroom : 
                       room.room_type === 'living_room' ? specs.windows_per_living_room :
                       room.room_type === 'kitchen' ? specs.windows_per_kitchen :
                       room.room_type === 'bathroom' ? specs.windows_per_bathroom : 1,
              door_type: room.room_type === 'bedroom' || room.room_type === 'living_room' ? 
                        specs.interior_door_type : specs.main_door_type,
              window_type: specs.window_type
            },
            // Add materials and colors based on quality and style
            materials: {
              quality: qualityLevel,
              style: architecturalStyle,
              premium_materials: enhancedFeatures.premiumMaterials,
              textures: enhancedFeatures.textures
            }
          })),
          building_dimensions: buildingDimensions,
          architectural_style: architecturalStyle,
          quality_level: qualityLevel,
          room_layout: specs.room_layout,
          construction_specifications: {
            construction_type: specs.construction_type,
            quality_grade: specs.quality_grade,
            wall_thickness: specs.wall_thickness,
            room_height: specs.room_height,
            flooring_type: specs.flooring_type,
            ceiling_type: specs.ceiling_type,
            main_door_type: specs.main_door_type,
            interior_door_type: specs.interior_door_type,
            window_type: specs.window_type,
            location: specs.location
          },
          enhanced_features: enhancedFeatures,
          interior_design: {
            furniture_style: variations.furnitureStyle,
            color_scheme: variations.colorScheme,
            lighting_variation: variations.lightingVariation,
            material_texture: variations.materialTexture,
            room_arrangement: variations.roomArrangement,
            include_details: enhancedFeatures.interiorDetails,
            landscaping: enhancedFeatures.landscaping
          },
          lighting: {
            ambient_intensity: 0.3,
            sun_strength: 5.0,
            area_lights: [
              { position: [10, -10, 20], power: 200 },
              { position: [-10, 10, 15], power: 100 }
            ]
          },
          camera: {
            lens: 35,
            dof_enabled: true,
            fstop: 2.8
          },
          render_settings: {
            samples: 512,
            resolution: [2560, 1440],
            denoising: true,
            output_format: "png"
          }
        }
        
        // Call the professional Blender MCP bridge
        setProgress(50)
        setCurrentStep('Generating professional 3D model...')
        const blenderResponse = await fetch('/api/mcp/blender-bridge', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            tool: 'generate_3d_model',
            arguments: professionalSceneConfig
          })
        })
        
        if (blenderResponse.ok) {
          const blenderResult = await blenderResponse.json()
          console.log('🎨 Blender result:', blenderResult)
          
          if (blenderResult.success) {
            setProgress(90)
            setCurrentStep('Finalizing 3D model...')
            
            // Update the result with 3D data
            const newResult = {
              ...boqData,
              professional_3d: {
                scene_id: blenderResult.data?.scene_id,
                quality: "professional",
                renderer: "blender_cycles",
                samples: 512,
                resolution: "3840x2160",
                obj_url: blenderResult.data?.files?.obj,
                mtl_url: blenderResult.data?.files?.mtl,
                blender_files: {
                  obj: blenderResult.data?.files?.obj,
                  mtl: blenderResult.data?.files?.mtl,
                  blend_file: blenderResult.data?.files?.blend,
                  renders: blenderResult.data?.files?.renders || []
                }
              }
            }
            
            console.log('🔍 Setting result state:', newResult)
            setResult(newResult)
            
            setProgress(100)
            setCurrentStep('Generation complete!')
            showNotification('3D model generated successfully!', 'success')
            
            // Auto-switch to Results tab
            setTimeout(() => {
              setActiveTab('results')
            }, 1000)
          } else {
            throw new Error(blenderResult.error || 'Failed to generate 3D model')
          }
        } else {
          const errorText = await blenderResponse.text()
          console.error('Blender API error response:', errorText)
          throw new Error(`Blender API error! status: ${blenderResponse.status}, response: ${errorText}`)
        }
      } else {
        // Fallback: Create basic room configuration from specs if room data is missing
        console.warn('⚠️ Room data missing from BOQ response, creating fallback configuration')
        
        // Create fallback room configuration
        const fallbackRooms = [
          { name: 'Living Room', type: 'living_room', width: 6, length: 5, height: 3.2, area: 30 },
          { name: 'Kitchen', type: 'kitchen', width: 4, length: 4, height: 3.2, area: 16 },
          { name: 'Bedroom', type: 'bedroom', width: 5, length: 4, height: 3.2, area: 20 },
          { name: 'Bathroom', type: 'bathroom', width: 3, length: 3, height: 3.2, area: 9 }
        ]
        
        const fallbackConfig = {
          rooms: fallbackRooms,
          building_dimensions: {
            total_width: 15,
            total_length: 12,
            height: 3.2
          },
          architectural_style: architecturalStyle,
          quality_level: qualityLevel,
          enhanced_features: enhancedFeatures
        }
        
        setBlenderProcessing(true)
        setProgress(50)
        setCurrentStep('Generating 3D model with fallback configuration...')
        
        const blenderResponse = await fetch('/api/mcp/blender-bridge', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            tool: 'generate_3d_model',
            arguments: fallbackConfig
          })
        })
        
        if (blenderResponse.ok) {
          const blenderResult = await blenderResponse.json()
          console.log('🎨 Blender result (fallback):', blenderResult)
          
          if (blenderResult.success) {
            setProgress(90)
            setCurrentStep('Finalizing 3D model...')
            
            // Update the result with 3D data
            const newResult = {
              ...boqData,
              professional_3d: {
                scene_id: blenderResult.data?.scene_id,
                quality: "professional",
                renderer: "blender_cycles",
                samples: 512,
                resolution: "3840x2160",
                obj_url: blenderResult.data?.files?.obj,
                mtl_url: blenderResult.data?.files?.mtl,
                blender_files: {
                  obj: blenderResult.data?.files?.obj,
                  mtl: blenderResult.data?.files?.mtl,
                  blend_file: blenderResult.data?.files?.blend,
                  renders: blenderResult.data?.files?.renders || []
                }
              }
            }
            
            setResult(newResult)
            setProgress(100)
            setCurrentStep('Generation complete!')
            showNotification('3D model generated successfully with fallback configuration!', 'success')
            
            // Auto-switch to Results tab
            setTimeout(() => {
              setActiveTab('results')
            }, 1000)
          } else {
            throw new Error(blenderResult.error || 'Failed to generate 3D model')
          }
        } else {
          const errorText = await blenderResponse.text()
          console.error('Blender API error response (fallback):', errorText)
          throw new Error(`Blender API error! status: ${blenderResponse.status}, response: ${errorText}`)
        }
      }
      
      // Non-3D fallback case
      if (!boqData.room_3d_data?.visualization_data?.rooms && !blenderProcessing) {
        // Just save the BOQ data without 3D
        setResult(boqData)
        setProgress(100)
        setCurrentStep('BOQ generation complete!')
        showNotification('BOQ generated successfully!', 'success')
        
        // Auto-switch to Results tab
        setTimeout(() => {
          setActiveTab('results')
        }, 1000)
      }
    } catch (error) {
      console.error('Generation error:', error)
      showNotification(`Generation failed: ${error}`, 'error')
    } finally {
      setIsGenerating(false)
      setBlenderProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            ConstructAI Professional 3D BOQ Generator
          </h1>
          <p className="text-gray-600 text-lg">
            Generate detailed construction costs with ultra-realistic 3D architectural visualizations
          </p>
          <div className="flex justify-center items-center gap-4 mt-4">
            <Badge variant="outline" className="bg-white">
              <Sparkles className="w-4 h-4 mr-2" />
              AI-Powered
            </Badge>
            <Badge variant="outline" className="bg-white">
              <Layers3 className="w-4 h-4 mr-2" />
              3D Visualization
            </Badge>
            <Badge variant="outline" className="bg-white">
              <Zap className="w-4 h-4 mr-2" />
              GPU Accelerated
            </Badge>
            {result && (
              <Badge variant="outline" className="bg-green-50 border-green-200">
                <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                Generated
              </Badge>
            )}
            {isGenerating && (
              <Badge variant="outline" className="bg-blue-50 border-blue-200">
                <Loader2 className="w-4 h-4 mr-2 text-blue-600 animate-spin" />
                Processing...
              </Badge>
            )}
          </div>
        </div>

        {/* Alert System */}
        {showAlert && (
          <Alert className={`mb-6 ${alertType === 'success' ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'}`}>
            {alertType === 'success' ? (
              <CheckCircle className="h-4 w-4 text-green-600" />
            ) : (
              <AlertCircle className="h-4 w-4 text-red-600" />
            )}
            <AlertDescription className={alertType === 'success' ? 'text-green-800' : 'text-red-800'}>
              {alertMessage}
            </AlertDescription>
          </Alert>
        )}

        {/* Progress Bar */}
        {(isGenerating || blenderProcessing) && (
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                {blenderProcessing ? 'Rendering professional 3D model...' : currentStep}
              </span>
              <span className="text-sm text-gray-500">{progress}%</span>
            </div>
            <Progress value={progress} className="w-full" />
            {blenderProcessing && (
              <div className="flex items-center justify-center mt-2">
                <Sparkles className="w-4 h-4 text-purple-600 animate-pulse mr-2" />
                <span className="text-sm text-purple-600">GPU-accelerated rendering in progress...</span>
              </div>
            )}
          </div>
        )}

        {/* Debug Info */}
        {result && (
          <div className="mb-4 p-4 bg-gray-100 rounded-lg text-xs">
            <p><strong>Result Data:</strong></p>
            <p>Scene ID: {result.professional_3d?.scene_id || 'N/A'}</p>
            <p>OBJ File: {result.professional_3d?.blender_files?.obj || 'N/A'}</p>
            <p>MTL File: {result.professional_3d?.blender_files?.mtl || 'N/A'}</p>
            <p>Has professional_3d: {result.professional_3d ? 'Yes' : 'No'}</p>
            <p>Has blender_files: {result.professional_3d?.blender_files ? 'Yes' : 'No'}</p>
            <p><strong>Debug - Raw Values:</strong></p>
            <p>blender_files type: {typeof result.professional_3d?.blender_files}</p>
            <p>obj property: &quot;{result.professional_3d?.blender_files?.obj || 'UNDEFINED'}&quot;</p>
            <p>mtl property: &quot;{result.professional_3d?.blender_files?.mtl || 'UNDEFINED'}&quot;</p>
            <details className="mt-2">
              <summary className="cursor-pointer text-blue-600">Full Result Object</summary>
              <pre className="mt-2 p-2 bg-white rounded text-xs overflow-auto max-h-40">
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>
            <details className="mt-2">
              <summary className="cursor-pointer text-blue-600">Professional 3D Object Only</summary>
              <pre className="mt-2 p-2 bg-white rounded text-xs overflow-auto max-h-40">
                {JSON.stringify(result.professional_3d, null, 2)}
              </pre>
            </details>
          </div>
        )}

        {/* Main Tabbed Interface */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="generator" className="flex items-center gap-2">
              <Building2 className="w-4 h-4" />
              3D Generator
            </TabsTrigger>
            <TabsTrigger value="features" className="flex items-center gap-2">
              <Star className="w-4 h-4" />
              Enhanced Features
            </TabsTrigger>
            <TabsTrigger value="results" className="flex items-center gap-2" disabled={!result}>
              <Calculator className="w-4 h-4" />
              BOQ Results
            </TabsTrigger>
            <TabsTrigger value="viewer" className="flex items-center gap-2" disabled={!result}>
              <Monitor className="w-4 h-4" />
              3D Viewer
            </TabsTrigger>
          </TabsList>

          {/* Generator Tab */}
          <TabsContent value="generator">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Building2 className="w-5 h-5" />
                  Project Specifications
                </CardTitle>
                <CardDescription>
                  Configure your construction project parameters for accurate BOQ generation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Basic Project Info */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Home className="w-4 h-4" />
                      Basic Information
                    </h3>
                    
                    <div>
                      <Label htmlFor="total_area">Total Area (sq ft) *</Label>
                      <Input
                        id="total_area"
                        type="number"
                        placeholder="e.g. 1200"
                        value={specs.total_area || ''}
                        onChange={(e) => setSpecs(prev => ({ ...prev, total_area: parseInt(e.target.value) || 0 }))}
                        className="mt-1"
                        required
                      />
                    </div>

                    <div>
                      <Label htmlFor="construction_type">Construction Type *</Label>
                      <Select value={specs.construction_type} onValueChange={(value) => setSpecs(prev => ({ ...prev, construction_type: value }))}>
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Select construction type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="RCC">RCC (Reinforced Concrete)</SelectItem>
                          <SelectItem value="Steel">Steel Frame</SelectItem>
                          <SelectItem value="Brick">Brick Masonry</SelectItem>
                          <SelectItem value="Wood">Wood Frame</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="quality_grade">Quality Grade *</Label>
                      <Select value={specs.quality_grade} onValueChange={(value) => setSpecs(prev => ({ ...prev, quality_grade: value }))}>
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Select quality grade" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="basic">Basic</SelectItem>
                          <SelectItem value="standard">Standard</SelectItem>
                          <SelectItem value="premium">Premium</SelectItem>
                          <SelectItem value="luxury">Luxury</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="room_layout">Room Layout *</Label>
                      <Select value={specs.room_layout} onValueChange={(value) => setSpecs(prev => ({ ...prev, room_layout: value }))}>
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Select room layout style" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="traditional">Traditional</SelectItem>
                          <SelectItem value="modern">Modern</SelectItem>
                          <SelectItem value="open_concept">Open Concept</SelectItem>
                          <SelectItem value="minimalist">Minimalist</SelectItem>
                          <SelectItem value="colonial">Colonial</SelectItem>
                          <SelectItem value="contemporary">Contemporary</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Room Configuration */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Room Configuration</h3>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="num_bedrooms">Bedrooms</Label>
                        <Input
                          id="num_bedrooms"
                          type="number"
                          min="0"
                          placeholder="e.g. 3"
                          value={specs.num_bedrooms || ''}
                          onChange={(e) => setSpecs(prev => ({ ...prev, num_bedrooms: parseInt(e.target.value) || 0 }))}
                          className="mt-1"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="num_bathrooms">Bathrooms</Label>
                        <Input
                          id="num_bathrooms"
                          type="number"
                          min="0"
                          placeholder="e.g. 2"
                          value={specs.num_bathrooms || ''}
                          onChange={(e) => setSpecs(prev => ({ ...prev, num_bathrooms: parseInt(e.target.value) || 0 }))}
                          className="mt-1"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="num_living_rooms">Living Rooms</Label>
                        <Input
                          id="num_living_rooms"
                          type="number"
                          min="0"
                          placeholder="e.g. 1"
                          value={specs.num_living_rooms || ''}
                          onChange={(e) => setSpecs(prev => ({ ...prev, num_living_rooms: parseInt(e.target.value) || 0 }))}
                          className="mt-1"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="num_kitchens">Kitchens</Label>
                        <Input
                          id="num_kitchens"
                          type="number"
                          min="0"
                          placeholder="e.g. 1"
                          value={specs.num_kitchens || ''}
                          onChange={(e) => setSpecs(prev => ({ ...prev, num_kitchens: parseInt(e.target.value) || 0 }))}
                          className="mt-1"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-8 pt-6 border-t border-gray-200 bg-gray-50 -mx-6 px-6 py-4 rounded-b-lg">
                  <Button 
                    onClick={generateModel}
                    disabled={isGenerating}
                    className="w-full h-12 text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all duration-200"
                  >
                    {isGenerating ? (
                      <>
                        <Loader2 className="w-5 h-5 mr-3 animate-spin" />
                        Generating 3D Model...
                      </>
                    ) : (
                      <>
                        <Calculator className="w-5 h-5 mr-3" />
                        Generate 3D Model & BOQ
                      </>
                    )}
                  </Button>
                  <p className="text-center text-sm text-gray-600 mt-2">
                    Click to generate professional 3D visualization with enhanced features
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Enhanced Features Tab */}
          <TabsContent value="features">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Star className="w-5 h-5" />
                  Enhanced Features
                </CardTitle>
                <CardDescription>
                  Professional 3D visualization features and settings
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* Enhanced Features Toggles */}
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Wand2 className="w-4 h-4" />
                      3D Enhancement Features
                    </h3>
                    
                    <div className="space-y-4">
                      <div className="flex items-center space-x-3">
                        <Checkbox
                          id="furniture"
                          checked={enhancedFeatures.furniture}
                          onCheckedChange={(checked) => 
                            setEnhancedFeatures(prev => ({ ...prev, furniture: checked as boolean }))
                          }
                        />
                        <div className="flex items-center gap-2">
                          <Sofa className="w-4 h-4 text-blue-600" />
                          <Label htmlFor="furniture" className="text-sm font-medium">
                            Furniture & Fixtures
                          </Label>
                        </div>
                      </div>
                      <p className="text-xs text-gray-500 ml-6">
                        Add sofas, tables, beds, chairs, and lighting fixtures
                      </p>

                      <div className="flex items-center space-x-3">
                        <Checkbox
                          id="landscaping"
                          checked={enhancedFeatures.landscaping}
                          onCheckedChange={(checked) => 
                            setEnhancedFeatures(prev => ({ ...prev, landscaping: checked as boolean }))
                          }
                        />
                        <div className="flex items-center gap-2">
                          <TreePine className="w-4 h-4 text-green-600" />
                          <Label htmlFor="landscaping" className="text-sm font-medium">
                            Landscaping & Gardens
                          </Label>
                        </div>
                      </div>
                      <p className="text-xs text-gray-500 ml-6">
                        Include trees, shrubs, outdoor furniture, and garden elements
                      </p>

                      <div className="flex items-center space-x-3">
                        <Checkbox
                          id="premiumMaterials"
                          checked={enhancedFeatures.premiumMaterials}
                          onCheckedChange={(checked) => 
                            setEnhancedFeatures(prev => ({ ...prev, premiumMaterials: checked as boolean }))
                          }
                        />
                        <div className="flex items-center gap-2">
                          <Palette className="w-4 h-4 text-purple-600" />
                          <Label htmlFor="premiumMaterials" className="text-sm font-medium">
                            Premium Materials
                          </Label>
                        </div>
                      </div>
                      <p className="text-xs text-gray-500 ml-6">
                        Hardwood, marble, granite, and luxury finishes
                      </p>

                      <div className="flex items-center space-x-3">
                        <Checkbox
                          id="interiorDetails"
                          checked={enhancedFeatures.interiorDetails}
                          onCheckedChange={(checked) => 
                            setEnhancedFeatures(prev => ({ ...prev, interiorDetails: checked as boolean }))
                          }
                        />
                        <div className="flex items-center gap-2">
                          <Home className="w-4 h-4 text-orange-600" />
                          <Label htmlFor="interiorDetails" className="text-sm font-medium">
                            Interior Details
                          </Label>
                        </div>
                      </div>
                      <p className="text-xs text-gray-500 ml-6">
                        Crown molding, baseboards, and architectural features
                      </p>

                      <div className="flex items-center space-x-3">
                        <Checkbox
                          id="lighting"
                          checked={enhancedFeatures.lighting}
                          onCheckedChange={(checked) => 
                            setEnhancedFeatures(prev => ({ ...prev, lighting: checked as boolean }))
                          }
                        />
                        <div className="flex items-center gap-2">
                          <Zap className="w-4 h-4 text-yellow-600" />
                          <Label htmlFor="lighting" className="text-sm font-medium">
                            Professional Lighting
                          </Label>
                        </div>
                      </div>
                      <p className="text-xs text-gray-500 ml-6">
                        3-point lighting system with GPU acceleration
                      </p>

                      <div className="flex items-center space-x-3">
                        <Checkbox
                          id="textures"
                          checked={enhancedFeatures.textures}
                          onCheckedChange={(checked) => 
                            setEnhancedFeatures(prev => ({ ...prev, textures: checked as boolean }))
                          }
                        />
                        <div className="flex items-center gap-2">
                          <Layers3 className="w-4 h-4 text-indigo-600" />
                          <Label htmlFor="textures" className="text-sm font-medium">
                            High-Quality Textures
                          </Label>
                        </div>
                      </div>
                      <p className="text-xs text-gray-500 ml-6">
                        Realistic materials with procedural textures
                      </p>
                    </div>
                  </div>

                  {/* Style and Quality Settings */}
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Star className="w-4 h-4" />
                      Style & Quality Settings
                    </h3>
                    
                    <div className="space-y-4">
                      <div>
                        <Label htmlFor="architectural_style">Architectural Style</Label>
                        <Select value={architecturalStyle} onValueChange={setArchitecturalStyle}>
                          <SelectTrigger className="mt-1">
                            <SelectValue placeholder="Select architectural style" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="modern">Modern</SelectItem>
                            <SelectItem value="contemporary">Contemporary</SelectItem>
                            <SelectItem value="traditional">Traditional</SelectItem>
                            <SelectItem value="minimalist">Minimalist</SelectItem>
                            <SelectItem value="luxury_villa">Luxury Villa</SelectItem>
                            <SelectItem value="industrial">Industrial</SelectItem>
                            <SelectItem value="scandinavian">Scandinavian</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label htmlFor="quality_level">Rendering Quality</Label>
                        <Select value={qualityLevel} onValueChange={setQualityLevel}>
                          <SelectTrigger className="mt-1">
                            <SelectValue placeholder="Select quality level" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="standard">Standard Quality</SelectItem>
                            <SelectItem value="professional">Professional Quality</SelectItem>
                            <SelectItem value="ultra">Ultra High Quality</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-medium mb-2">Feature Summary</h4>
                        <div className="text-sm text-gray-600 space-y-1">
                          <p>• Style: {architecturalStyle.replace('_', ' ')}</p>
                          <p>• Quality: {qualityLevel}</p>
                          <p>• Active Features: {Object.values(enhancedFeatures).filter(Boolean).length}/6</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 pt-6 border-t">
                  <Button 
                    onClick={() => showNotification('Enhanced features updated successfully!', 'success')}
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                  >
                    <Star className="w-4 h-4 mr-2" />
                    Update Enhanced Features
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Results Tab */}
          <TabsContent value="results">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* BOQ Summary */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Calculator className="w-5 h-5" />
                    BOQ Summary
                  </CardTitle>
                  <CardDescription>
                    Detailed cost breakdown and project specifications
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {result && (
                    <div className="space-y-6">
                      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border border-blue-200">
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">
                          Total Cost: ₹{result.total_cost?.toLocaleString() || 'N/A'}
                        </h3>
                        <p className="text-gray-600">
                          Professional 3D visualization included
                        </p>
                      </div>
                      
                      <div className="space-y-3">
                        <h4 className="font-semibold text-gray-900">Project Details</h4>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-gray-500">Total Area</p>
                            <p className="font-medium">{specs.total_area} sq ft</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Construction Type</p>
                            <p className="font-medium">{specs.construction_type}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Quality Grade</p>
                            <p className="font-medium">{specs.quality_grade}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Architectural Style</p>
                            <p className="font-medium">{architecturalStyle}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <h4 className="font-semibold text-gray-900">Room Configuration</h4>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-gray-500">Bedrooms</p>
                            <p className="font-medium">{specs.num_bedrooms}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Bathrooms</p>
                            <p className="font-medium">{specs.num_bathrooms}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Living Rooms</p>
                            <p className="font-medium">{specs.num_living_rooms}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Kitchens</p>
                            <p className="font-medium">{specs.num_kitchens}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        <h4 className="font-semibold text-gray-900">Enhanced Features</h4>
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(enhancedFeatures).map(([key, enabled]) => (
                            <Badge 
                              key={key} 
                              variant={enabled ? "default" : "secondary"}
                              className={enabled ? "bg-green-100 text-green-800" : ""}
                            >
                              {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="pt-4 border-t">
                        <Button 
                          onClick={() => {
                            const boqData = {
                              project_specs: specs,
                              enhanced_features: enhancedFeatures,
                              architectural_style: architecturalStyle,
                              quality_level: qualityLevel,
                              total_cost: result.total_cost,
                              items: result.items,
                              generated_at: new Date().toISOString()
                            }
                            
                            const blob = new Blob([JSON.stringify(boqData, null, 2)], { type: 'application/json' })
                            const url = URL.createObjectURL(blob)
                            const a = document.createElement('a')
                            a.href = url
                            a.download = `BOQ_${new Date().toISOString().split('T')[0]}.json`
                            a.click()
                            URL.revokeObjectURL(url)
                          }}
                          className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download BOQ Report
                        </Button>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Detailed Items */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Layers3 className="w-5 h-5" />
                    Detailed Items
                  </CardTitle>
                  <CardDescription>
                    Itemized breakdown of construction materials and labor
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {result?.items && (
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                      {result.items.map((item, index) => (
                        <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <div className="flex-1">
                            <div className="font-medium text-gray-900">{item.item}</div>
                            <div className="text-sm text-gray-500">
                              {item.quantity} {item.unit} @ ₹{item.rate?.toLocaleString()}
                            </div>
                          </div>
                          <div className="font-semibold text-gray-900">
                            ₹{item.amount?.toLocaleString()}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 3D Viewer Tab */}
          <TabsContent value="viewer">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Monitor className="w-5 h-5" />
                  3D Model Viewer
                </CardTitle>
                <CardDescription>
                  Real-time preview of your generated 3D architectural model
                </CardDescription>
              </CardHeader>
              <CardContent>
                {result?.professional_3d?.blender_files?.obj ? (
                  <div className="space-y-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium mb-2">Model Information</h4>
                      <div className="text-sm text-gray-600 space-y-1">
                        <p>• Scene ID: {result.professional_3d.scene_id}</p>
                        <p>• Quality: {result.professional_3d.quality}</p>
                        <p>• Renderer: {result.professional_3d.renderer}</p>
                        <p>• Samples: {result.professional_3d.samples}</p>
                      </div>
                    </div>
                    
                    <div className="border rounded-lg overflow-hidden">
                      <ThreeJSViewer
                        objUrl={result.professional_3d.blender_files?.obj}
                        mtlUrl={result.professional_3d.blender_files?.mtl}
                        width={800}
                        height={600}
                        onModelLoad={() => console.log('✅ Enhanced3DBOQ: 3D model loaded successfully')}
                        onModelError={(error) => console.error('❌ Enhanced3DBOQ: 3D viewer error:', error)}
                      />
                    </div>
                    
                    {result.professional_3d.blender_files.renders && result.professional_3d.blender_files.renders.length > 0 && (
                      <div className="space-y-2">
                        <h4 className="font-medium">Rendered Views</h4>
                        <div className="grid grid-cols-1 gap-2">
                          {result.professional_3d.blender_files.renders
                            .filter((render) => render && typeof render === 'string' && render.trim() !== '')
                            .map((render, index) => (
                                <Button
                                  key={index}
                                  variant="outline"
                                  size="sm"
                                  onClick={() => {
                                    try {
                                      // Create download link for the render
                                      const normalizedPath = render.startsWith('/') ? render : `/${render}`;
                                      const link = document.createElement('a');
                                      link.href = normalizedPath;
                                      link.download = `render_${index + 1}_${Date.now()}.png`;
                                      link.click();
                                    } catch (error) {
                                      console.error('Failed to download render:', error);
                                    }
                                  }}
                                  className="w-full justify-start"
                                >
                                  <Download className="w-4 h-4 mr-2" />
                                  Download Render {index + 1}
                                </Button>
                            ))}
                        </div>
                      </div>
                    )}
                    
                    <div className="flex gap-2">
                      <Button 
                        onClick={async () => {
                          if (result.professional_3d?.blender_files?.obj) {
                            try {
                              // Extract filename from path
                              const objPath = result.professional_3d.blender_files.obj;
                              const filename = objPath.split('/').pop() || objPath;
                              
                              // Use the download API
                              const downloadUrl = `/api/download/${filename}`;
                              
                              // Check if file exists first
                              const response = await fetch(downloadUrl, { method: 'HEAD' });
                              if (!response.ok) {
                                alert(`❌ File not found: ${filename}\n\nThe 3D model may not have been generated properly. Try regenerating the model.`);
                                return;
                              }
                              
                              // Create a temporary link for download
                              const link = document.createElement('a');
                              link.href = downloadUrl;
                              link.download = filename;
                              document.body.appendChild(link);
                              link.click();
                              document.body.removeChild(link);
                            } catch (error) {
                              console.error('Failed to download OBJ file:', error);
                              alert('❌ Download failed. The file may not exist or there was a network error.');
                            }
                          }
                        }}
                        className="flex-1"
                      >
                        <Download className="w-4 h-4 mr-2" />
                        Download OBJ
                      </Button>
                      <Button 
                        onClick={() => {
                          if (result.professional_3d?.blender_files?.mtl) {
                            try {
                              // Extract filename from path
                              const mtlPath = result.professional_3d.blender_files.mtl;
                              const filename = mtlPath.split('/').pop() || mtlPath;
                              
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
                              console.error('Failed to download MTL file:', error);
                            }
                          }
                        }}
                        className="flex-1"
                      >
                        <Download className="w-4 h-4 mr-2" />
                        Download MTL
                      </Button>
                    </div>
                  </div>
                ) : result?.nerf_3d ? (
                  <div className="space-y-4">
                    <NeRFViewer 
                      nerfData={result.nerf_3d}
                      className="w-full"
                    />
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <Monitor className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No 3D Model Available</h3>
                    <p className="text-gray-500 mb-4">
                      {result ? 'Generate a 3D model to view it here' : 'Generate a project first to view 3D models'}
                    </p>
                    {!result && (
                      <Button 
                        onClick={() => setActiveTab('generator')}
                        className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                      >
                        <Building2 className="w-4 h-4 mr-2" />
                        Go to Generator
                      </Button>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
        
        {/* Floating Action Button - Always visible */}
        {activeTab === 'generator' && !result && (
          <div className="fixed bottom-8 right-8 z-50">
            <Button
              onClick={generateModel}
              disabled={isGenerating}
              className="h-16 w-16 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-110"
            >
              {isGenerating ? (
                <Loader2 className="w-8 h-8 animate-spin" />
              ) : (
                <Calculator className="w-8 h-8" />
              )}
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
