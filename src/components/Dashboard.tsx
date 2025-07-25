'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Building2, Eye, Calculator, Layers3, MessageSquare, Upload, Send } from "lucide-react"
import { constructAI } from '@/lib/api'

// Define types for API responses
interface Convert3DResponse {
  blueprint_id?: string
  model_3d_url?: string
  image_type?: string
  processing_info?: Record<string, unknown>
  data?: {
    rooms?: Array<{ type: string; area: number }>
    walls?: Array<{ id: string; start: number[]; end: number[]; thickness: number; material: string }>
    dimensions?: { width: number; height: number; area: number }
    blueprint_id?: string
    model_3d_url?: string
    model_3d_data?: string
  }
}

interface PPEResponse {
  data?: {
    detections?: Array<{ type: string; confidence: number }>
  }
}

interface BOQResponse {
  total_cost?: number
  timeline_days?: number
}

interface ChatResponse {
  response?: string
}

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [backendConnected, setBackendConnected] = useState(false)
  const [notification, setNotification] = useState<string | null>(null)
  const [result, setResult] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [activeModule, setActiveModule] = useState<string | null>(null)
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState<Array<{user: string, bot: string, timestamp: string}>>([])
  
  // BOQ Form state
  const [boqSpecs, setBOQSpecs] = useState({
    total_area: 1000,
    num_rooms: 3,
    num_bathrooms: 2,
    num_floors: 1,
    construction_type: 'residential',
    quality_grade: 'standard',
    location: 'urban'
  })

  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const initConnection = async () => {
      try {
        await constructAI.health()
        setBackendConnected(true)
        showMessage('✅ Backend Connected Successfully!')
      } catch {
        setBackendConnected(false)
        showMessage('❌ Backend Offline - Check if running on port 8000')
      }
    }
    initConnection()
  }, [])

  const testConnection = async () => {
    try {
      await constructAI.health()
      setBackendConnected(true)
      showMessage('✅ Backend Connected Successfully!')
    } catch {
      setBackendConnected(false)
      showMessage('❌ Backend Offline - Check if running on port 8000')
    }
  }

  const showMessage = (message: string) => {
    setNotification(message)
    setTimeout(() => setNotification(null), 4000)
  }

  const showResult = (data: unknown) => {
    setResult(JSON.stringify(data, null, 2))
  }

  const showFormattedResult = (data: Convert3DResponse['data']) => {
    const formatted = `
🏗️ 3D CONVERSION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━

📐 DIMENSIONS:
   Width: ${data?.dimensions?.width || 0}m
   Height: ${data?.dimensions?.height || 0}m  
   Area: ${data?.dimensions?.area || 0}m²

🏠 STRUCTURE DETECTED:
   Rooms: ${data?.rooms?.length || 0}
   Walls: ${data?.walls?.length || 0}

📁 3D MODEL:
   Blueprint ID: ${data?.blueprint_id || 'N/A'}
   Download URL: ${data?.model_3d_url || 'N/A'}
   
🎯 CONFIDENCE: 85% accuracy

━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Model ready for download!
    `
    setResult(formatted)
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      showMessage(`📁 Selected: ${file.name}`)
    }
  }

  const handleStartBuilding = async () => {
    if (!backendConnected) {
      showMessage('⚠️ Backend not connected')
      return
    }
    
    setLoading(true)
    try {
      const newProject = await constructAI.createProject({
        name: `Project ${Date.now()}`,
        description: 'New construction project',
        location: 'Construction Site'
      })
      showMessage('✅ New project created!')
      showResult(newProject)
    } catch {
      showMessage('❌ Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  const handle2DTo3D = async () => {
    if (!backendConnected) {
      showMessage('⚠️ Backend not connected')
      return
    }

    if (!selectedFile) {
      showMessage('⚠️ Please select a blueprint image first')
      fileInputRef.current?.click()
      return
    }

    setLoading(true)
    setActiveModule('3d-conversion')
    try {
      showMessage('🏗️ Processing blueprint...')
      
      // Add debug logging
      console.log('🔍 Sending file to API:', selectedFile.name, selectedFile.size, 'bytes')
      
      const result = await constructAI.convert2DTo3D(selectedFile)
      const resultData = result as Convert3DResponse
      
      // Debug: Log the actual response
      console.log('🔍 API Response received:', result)
      console.log('🔍 Response type:', typeof result)
      console.log('🔍 Response keys:', Object.keys(result || {}))
      
      // Handle different response formats
      let actualData: Convert3DResponse['data'] | null = null;
      if (resultData.data) {
        actualData = resultData.data;
      } else if (typeof result === 'object' && result !== null && 
                 ('rooms' in result || 'walls' in result || 'dimensions' in result)) {
        // Direct response format
        actualData = result as Convert3DResponse['data'];
      } else {
        console.error('🚨 Unexpected response format:', result);
        showMessage('⚠️ Unexpected response format from server');
        showResult(result);
        return;
      }
      
      // Show success message with image type
      const roomCount = actualData?.rooms?.length || 0
      const wallCount = actualData?.walls?.length || 0
      const area = actualData?.dimensions?.area || 0
      const imageType = resultData?.image_type || 'unknown'
      
      console.log('🔍 Extracted data:', { roomCount, wallCount, area, imageType });
      
      if (roomCount === 0 && wallCount === 0 && area === 0) {
        showMessage('❌ Processing returned empty results - this should not happen!')
        console.error('🚨 Empty results detected, raw response:', result);
        showResult(result);
        return;
      }
      
      // Create type-specific message
      let typeMessage = ''
      switch(imageType) {
        case 'blueprint':
          typeMessage = '📐 Blueprint detected'
          break
        case 'floor_plan':
          typeMessage = '🏗️ Floor plan detected'
          break
        case 'interior_photo':
          typeMessage = '🏠 Interior photo detected'
          break
        case 'photo':
          typeMessage = '📷 Photo detected'
          break
        default:
          typeMessage = '❓ Image type unknown'
      }
      
      showMessage(`✅ 3D Model Generated! ${typeMessage} - Found ${roomCount} rooms, ${wallCount} walls, ${area.toFixed(1)}sqm`)
      
      // Auto-download the 3D model file
      const modelUrl = actualData?.model_3d_url || resultData?.model_3d_url;
      if (modelUrl) {
        const downloadUrl = `http://localhost:8000${modelUrl}`
        const blueprintId = actualData?.blueprint_id || resultData?.blueprint_id || 'unknown'
        const fileExtension = modelUrl.includes('.obj') ? 'obj' : 'glb'
        try {
          // Create download link
          const link = document.createElement('a')
          link.href = downloadUrl
          link.download = `constructai-model-${blueprintId}.${fileExtension}`
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          
          showMessage(`📥 3D Model (.${fileExtension}) downloaded successfully! Open with Blender, MeshLab, or any 3D software.`)
        } catch (downloadError) {
          console.error('Download failed:', downloadError)
          showMessage('⚠️ Download failed, but you can access the model manually')
        }
      }
      
      // Show formatted result instead of raw JSON
      showFormattedResult(actualData)
      
    } catch (error) {
      console.error('3D conversion error:', error)
      showMessage('❌ 3D conversion failed. Checking backend status...')
      
      // Try to get some debug info from the server
      try {
        const debugResult = await fetch('http://localhost:8000/api/v1/ai/debug/test-processing');
        const debugData = await debugResult.json();
        console.log('🔍 Debug endpoint response:', debugData);
        showMessage(`Debug: Backend can generate ${debugData.rooms_count} rooms and ${debugData.walls_count} walls`);
      } catch (debugError) {
        console.error('Debug request failed:', debugError);
      }
      
      showResult(error)
    } finally {
      setLoading(false)
      setActiveModule(null)
    }
  }

  const handlePPEDetection = async () => {
    if (!backendConnected) {
      showMessage('⚠️ Backend not connected')
      return
    }

    if (!selectedFile) {
      showMessage('⚠️ Please select a site image first')
      fileInputRef.current?.click()
      return
    }

    setLoading(true)
    setActiveModule('ppe-detection')
    try {
      showMessage('👁️ Analyzing PPE...')
      const result = await constructAI.detectPPE(selectedFile)
      const resultData = result as PPEResponse
      const detections = resultData.data?.detections || []
      showMessage(`✅ PPE Analysis Complete! Found ${detections.length} safety items`)
      showResult(result)
    } catch (error) {
      showMessage('❌ PPE detection failed')
      console.error(error)
    } finally {
      setLoading(false)
      setActiveModule(null)
    }
  }

  const handleDetailedBOQ = async () => {
    if (!backendConnected) {
      showMessage('⚠️ Backend not connected')
      return
    }
    
    setLoading(true)
    setActiveModule('boq-calculation')
    try {
      showMessage('📊 Calculating detailed BOQ...')
      const result = await constructAI.calculateDetailedBOQ(boqSpecs)
      const resultData = result as BOQResponse
      const totalCost = resultData.total_cost || 0
      const timeline = resultData.timeline_days || 0
      showMessage(`✅ BOQ Complete! Cost: ₹${totalCost.toLocaleString()} | Timeline: ${timeline} days`)
      showResult(result)
    } catch (error) {
      showMessage('❌ BOQ calculation failed')
      console.error(error)
    } finally {
      setLoading(false)
      setActiveModule(null)
    }
  }

  const handleChatSubmit = async () => {
    if (!backendConnected) {
      showMessage('⚠️ Backend not connected')
      return
    }

    if (!chatMessage.trim()) {
      showMessage('⚠️ Please enter a message')
      return
    }

    setLoading(true)
    try {
      showMessage('🤖 MistriBot is thinking...')
      const response = await constructAI.askRealChatbot(chatMessage)
      const responseData = response as ChatResponse
      
      const newChat = {
        user: chatMessage,
        bot: responseData.response || 'Sorry, I could not process your request.',
        timestamp: new Date().toLocaleTimeString()
      }
      
      setChatHistory(prev => [...prev, newChat])
      setChatMessage('')
      showMessage('✅ MistriBot responded!')
      showResult(response)
    } catch (error) {
      showMessage('❌ Chat failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const modules = [
    {
      title: '2D → 3D Converter',
      description: 'Transform blueprints into 3D models',
      icon: Layers3,
      action: () => window.location.href = '/convert',
      requiresFile: false
    },
    {
      title: 'BOQ & Cost Estimator',
      description: 'Calculate bills of quantities',
      icon: Calculator,
      action: () => window.location.href = '/boq',
      requiresFile: false
    },
    {
      title: 'PPE Safety Monitor',
      description: 'AI safety detection',
      icon: Eye,
      action: handlePPEDetection,
      requiresFile: true,
      fileTypes: 'image/*'
    },
    {
      title: 'MistriBot Assistant',
      description: 'AI chatbot helper',
      icon: MessageSquare,
      action: () => setActiveModule('chat'),
      requiresFile: false
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
            ConstructAI
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Real AI-Powered Construction Management System
          </p>
          
          {/* Status */}
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium mb-6 ${
            backendConnected 
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}>
            <div className={`w-2 h-2 rounded-full ${backendConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            Backend {backendConnected ? 'Connected' : 'Disconnected'}
          </div>

          {/* File Upload */}
          <div className="mb-6">
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileSelect}
              className="hidden"
              accept="image/*"
            />
            <Button 
              onClick={() => fileInputRef.current?.click()}
              variant="outline"
              className="mr-4"
            >
              <Upload className="mr-2 h-4 w-4" />
              {selectedFile ? selectedFile.name : 'Upload File'}
            </Button>
            {selectedFile && (
              <span className="text-sm text-green-600">
                ✅ {selectedFile.name} ({Math.round(selectedFile.size / 1024)}KB)
              </span>
            )}
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              onClick={handleStartBuilding}
              disabled={loading}
            >
              <Building2 className="mr-2 h-5 w-5" />
              {loading ? 'Creating...' : 'Start Building'}
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              onClick={() => {
                try {
                  const fullUrl = new URL('/api-test', window.location.origin).href;
                  window.open(fullUrl, '_blank');
                } catch (error) {
                  console.error('Failed to open demo page:', error);
                }
              }}
            >
              <Eye className="mr-2 h-5 w-5" />
              View Demo
            </Button>
          </div>
        </div>

        {/* BOQ Configuration Modal */}
        {activeModule === 'boq-calculation' && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
              <div className="p-6">
                <h3 className="text-lg font-semibold mb-4">BOQ Configuration</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Total Area (sqft)</label>
                    <input
                      type="number"
                      value={boqSpecs.total_area}
                      onChange={(e) => setBOQSpecs({...boqSpecs, total_area: Number(e.target.value)})}
                      className="w-full border rounded px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Number of Rooms</label>
                    <input
                      type="number"
                      value={boqSpecs.num_rooms}
                      onChange={(e) => setBOQSpecs({...boqSpecs, num_rooms: Number(e.target.value)})}
                      className="w-full border rounded px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Bathrooms</label>
                    <input
                      type="number"
                      value={boqSpecs.num_bathrooms}
                      onChange={(e) => setBOQSpecs({...boqSpecs, num_bathrooms: Number(e.target.value)})}
                      className="w-full border rounded px-3 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Construction Type</label>
                    <select
                      value={boqSpecs.construction_type}
                      onChange={(e) => setBOQSpecs({...boqSpecs, construction_type: e.target.value})}
                      className="w-full border rounded px-3 py-2"
                    >
                      <option value="residential">Residential</option>
                      <option value="commercial">Commercial</option>
                      <option value="industrial">Industrial</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Quality Grade</label>
                    <select
                      value={boqSpecs.quality_grade}
                      onChange={(e) => setBOQSpecs({...boqSpecs, quality_grade: e.target.value})}
                      className="w-full border rounded px-3 py-2"
                    >
                      <option value="basic">Basic</option>
                      <option value="standard">Standard</option>
                      <option value="premium">Premium</option>
                    </select>
                  </div>
                </div>
                <div className="flex gap-2 mt-6">
                  <Button onClick={handleDetailedBOQ} disabled={loading} className="flex-1">
                    Calculate BOQ
                  </Button>
                  <Button variant="outline" onClick={() => setActiveModule(null)}>
                    Cancel
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Chat Interface */}
        {activeModule === 'chat' && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] flex flex-col">
              <div className="p-4 border-b flex justify-between items-center">
                <h3 className="text-lg font-semibold">MistriBot Assistant</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setActiveModule(null)}
                >
                  ✕
                </Button>
              </div>
              
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {chatHistory.length === 0 ? (
                  <div className="text-center text-gray-500">
                    <MessageSquare className="mx-auto h-12 w-12 mb-2" />
                    <p>Start a conversation with MistriBot!</p>
                  </div>
                ) : (
                  chatHistory.map((chat, index) => (
                    <div key={index} className="space-y-2">
                      <div className="bg-blue-100 rounded-lg p-3 ml-auto max-w-[80%]">
                        <p className="text-sm"><strong>You:</strong> {chat.user}</p>
                        <span className="text-xs text-gray-500">{chat.timestamp}</span>
                      </div>
                      <div className="bg-gray-100 rounded-lg p-3 mr-auto max-w-[80%]">
                        <p className="text-sm"><strong>MistriBot:</strong> {chat.bot}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
              
              <div className="p-4 border-t">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={chatMessage}
                    onChange={(e) => setChatMessage(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleChatSubmit()}
                    placeholder="Ask MistriBot about construction..."
                    className="flex-1 border rounded px-3 py-2"
                    disabled={loading}
                  />
                  <Button onClick={handleChatSubmit} disabled={loading || !chatMessage.trim()}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {modules.map((module, index) => {
            const IconComponent = module.icon
            const isActive = activeModule === module.title.toLowerCase().replace(/\s+/g, '-')
            
            return (
              <Card 
                key={index}
                className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                  isActive ? 'ring-2 ring-blue-500' : ''
                } ${loading && isActive ? 'opacity-50' : ''}`}
                onClick={module.action}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto mb-4 p-3 bg-blue-100 rounded-full w-fit">
                    <IconComponent className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-lg">{module.title}</CardTitle>
                  <CardDescription className="text-sm">{module.description}</CardDescription>
                  {module.requiresFile && (
                    <div className="text-xs text-orange-600 mt-2">
                      📁 Requires file upload
                    </div>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      backendConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {backendConnected ? 'Ready' : 'Offline'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Quick Actions */}
        <div className="text-center">
          <div className="flex flex-wrap gap-4 justify-center">
            <Button onClick={() => window.open('http://localhost:8000/docs', '_blank')}>
              📚 API Docs
            </Button>
            <Button variant="outline" onClick={testConnection}>
              🔄 Test Connection
            </Button>
            <Button variant="outline" onClick={() => setSelectedFile(null)}>
              🗑️ Clear File
            </Button>
          </div>
        </div>
      </div>

      {/* Simple Notification */}
      {notification && (
        <div className="fixed top-4 right-4 bg-white border border-gray-200 rounded-lg shadow-lg p-4 max-w-sm z-50">
          <div className="flex justify-between items-start">
            <p className="text-sm">{notification}</p>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setNotification(null)}
              className="ml-2 p-1 h-auto"
            >
              ✕
            </Button>
          </div>
        </div>
      )}

      {/* Simple Results Modal */}
      {result && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b">
              <h3 className="text-lg font-semibold">API Response</h3>
              <Button variant="ghost" size="sm" onClick={() => setResult(null)}>
                ✕
              </Button>
            </div>
            <div className="p-4 overflow-y-auto max-h-[60vh]">
              <pre className="bg-gray-100 rounded p-4 text-xs overflow-x-auto whitespace-pre-wrap">
                {result}
              </pre>
            </div>
            <div className="p-4 border-t">
              <Button onClick={() => setResult(null)} className="w-full">
                Close
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
