'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Eye, RotateCcw, Camera, Loader2 } from 'lucide-react';
import Image from 'next/image';

// Interface definitions to match Enhanced3DBOQ requirements
interface RoomData {
  id: string;
  name: string;
  type: string;
  area: number;
  width: number;
  height: number;
  length: number;
  position: { x: number; y: number; z: number };
  materials?: Array<{
    type: string;
    area: number;
    cost: number;
    finish: string;
  }>;
  fixtures?: Array<{
    type: string;
    quantity: number;
    cost: number;
    position: { x: number; y: number; z: number };
  }>;
}

interface BuildingDimensions {
  total_width: number;
  total_length: number;
  height: number;
}

interface BlenderRoomViewerProps {
  rooms: RoomData[];
  buildingDimensions: BuildingDimensions;
  professional3D?: {
    scene_id: string;
    quality: string;
    renderer: string;
    samples: number;
    resolution: string;
    blender_files: {
      scene_id: string;
      obj_file: string;
      mtl_file: string;
      blend_file: string;
      renders: string[];
      file_paths: {
        obj: string;
        mtl: string;
        blend: string;
        renders: string[];
      };
    };
  };
  onRoomSelect?: (roomId: string) => void;
  className?: string;
}

interface BlenderRender {
  id: string;
  url: string;
  type: 'single' | '360';
  timestamp: number;
  status: 'pending' | 'completed' | 'failed';
}

interface MCPServerStatus {
  connected: boolean;
  error?: string;
  version?: string;
}

const BlenderRoomViewer: React.FC<BlenderRoomViewerProps> = ({
  rooms,
  buildingDimensions,
  professional3D,
  onRoomSelect,
  className = ""
}) => {
  const [renders, setRenders] = useState<BlenderRender[]>([]);
  const [selectedRender, setSelectedRender] = useState<BlenderRender | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mcpStatus, setMcpStatus] = useState<MCPServerStatus>({ connected: false });
  const [showProfessional3D, setShowProfessional3D] = useState(false);

  // Check if professional 3D data is available
  const hasProfessional3D = professional3D && professional3D.blender_files?.renders?.length > 0;

  useEffect(() => {
    console.log('🎨 Professional 3D data received:', professional3D);
    if (hasProfessional3D) {
      setShowProfessional3D(true);
    }
  }, [professional3D, hasProfessional3D]);

  // MCP Server communication functions
  const connectToMCP = async () => {
    try {
      setIsLoading(true);
      // Connect to actual MCP server on port 9876
      const response = await fetch('/api/mcp/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          server_url: 'http://localhost:9876',
          server_name: 'blender-3d-server'
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        setMcpStatus({ connected: true, version: result.version || "1.0.0" });
      } else {
        throw new Error(`Failed to connect: ${response.statusText}`);
      }
    } catch (error) {
      setMcpStatus({ connected: false, error: error instanceof Error ? error.message : 'Connection failed' });
    } finally {
      setIsLoading(false);
    }
  };

  const create3DScene = useCallback(async () => {
    if (!mcpStatus.connected) {
      await connectToMCP();
    }

    try {
      setIsLoading(true);
      
      // Call actual MCP server to create 3D scene
      const response = await fetch('/api/mcp/create-scene', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rooms,
          building_dimensions: buildingDimensions
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Scene created successfully:', result);
      } else {
        throw new Error(`Scene creation failed: ${response.statusText}`);
      }
      
    } catch (error) {
      console.error('Error creating 3D scene:', error);
    } finally {
      setIsLoading(false);
    }
  }, [mcpStatus.connected, rooms, buildingDimensions]);

  const renderScene = useCallback(async (type: 'single' | '360') => {
    if (!rooms.length) return;
    
    setIsLoading(true);
    
    try {
      console.log(`🎨 Creating ${type} render...`);
      
      // Transform room data for professional BOQ rendering
      const professionalConfig = {
        scene_type: "architectural_visualization",
        quality: "professional",
        detail_level: "ultra_high",
        style: "modern_luxury",
        render_quality: "production",
        rooms: rooms.map(room => ({
          name: room.name,
          type: room.type,
          width: room.width,
          length: room.length,
          height: room.height,
          position: room.position,
          style: "modern_contemporary",
          materials: {
            floor: "premium_hardwood",
            walls: "luxury_paint",
            ceiling: "modern_false_ceiling"
          },
          furniture_quality: "luxury",
          lighting_setup: "professional"
        })),
        building_dimensions: buildingDimensions,
        lighting: {
          type: "cinematic",
          golden_hour: true,
          ambient_intensity: 0.8,
          key_light_strength: 3.0
        },
        materials: {
          quality: "pbr_advanced",
          detail_level: "ultra_high",
          textures: "4k"
        },
        camera: {
          type: type === '360' ? 'panoramic' : 'architectural',
          lens: 35,
          dof: true,
          fstop: 5.6
        },
        render_settings: {
          samples: type === '360' ? 512 : 256,
          resolution: type === '360' ? [3840, 2160] : [2560, 1440],
          denoising: true,
          output_format: "png"
        }
      };
      
      // Call the professional Blender API
      const response = await fetch('/api/mcp/blender-bridge', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tool: 'generate_3d_model',
          arguments: professionalConfig
        })
      });
      
      if (!response.ok) {
        throw new Error(`Professional render failed: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success && result.result) {
        const newRenders: BlenderRender[] = [];
        
        // Add each render to the renders array
        for (const renderUrl of result.result.renders) {
          const render: BlenderRender = {
            id: `${result.result.scene_id}_${type}_${Date.now()}`,
            url: renderUrl,
            type: type,
            timestamp: Date.now(),
            status: 'completed'
          };
          newRenders.push(render);
        }
        
        // Update renders state
        setRenders(prev => [...prev, ...newRenders]);
        
        // Select the first new render
        if (newRenders.length > 0) {
          setSelectedRender(newRenders[0]);
        }
        
        console.log(`✅ ${type} render completed with ${newRenders.length} images`);
        
      } else {
        throw new Error(result.error || 'Professional render failed');
      }
      
    } catch (error) {
      console.error('❌ Professional render error:', error);
      alert(`Professional render failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  }, [rooms, buildingDimensions]);

  const getRoomColor = (roomType: string): string => {
    const colors: Record<string, string> = {
      'bedroom': '#FFE4E1',
      'kitchen': '#F0FFF0',
      'living_room': '#F0F8FF',
      'bathroom': '#E0FFFF',
      'dining_room': '#FFF8DC',
      'study_room': '#F5F5DC',
      'guest_room': '#FFF0F5',
      'utility_room': '#F8F8FF',
      'store_room': '#FFFACD'
    };
    return colors[roomType] || '#FFFFFF';
  };

  const handleRoomClick = (roomId: string) => {
    if (onRoomSelect) {
      onRoomSelect(roomId);
    }
  };

  // Auto-create scene when rooms change
  useEffect(() => {
    if (rooms.length > 0 && !mcpStatus.connected) {
      create3DScene();
    }
  }, [rooms, mcpStatus.connected, create3DScene]);

  return (
    <div className={`blender-room-viewer ${className}`}>
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Camera className="w-5 h-5" />
            Blender 3D Visualization
          </CardTitle>
          <CardDescription>
            High-quality architectural renders using Blender
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Professional 3D Models Section */}
          {hasProfessional3D && showProfessional3D && (
            <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
              <h3 className="text-lg font-semibold text-blue-900 mb-3 flex items-center gap-2">
                <Camera className="w-5 h-5" />
                Professional 3D Models ({professional3D?.quality || 'High Quality'})
              </h3>
              <div className="text-sm text-blue-700 mb-4">
                Generated with {professional3D?.renderer || 'Blender Cycles'} • {professional3D?.samples || 512} samples • {professional3D?.resolution || '3840x2160'}
              </div>
              
              {/* Render Gallery */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                {professional3D?.blender_files?.renders?.map((renderPath, index) => (
                  <div key={index} className="relative group">
                    <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden">
                      <Image
                        src={renderPath}
                        alt={`Professional 3D Render ${index + 1}`}
                        width={400}
                        height={300}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        onLoad={() => console.log(`✅ Professional render loaded: ${renderPath}`)}
                        onError={() => console.error(`❌ Failed to load render: ${renderPath}`)}
                      />
                    </div>
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300 rounded-lg flex items-center justify-center">
                      <Eye className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Download Links */}
              <div className="flex flex-wrap gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    if (professional3D?.blender_files?.obj_file) {
                      window.open(professional3D.blender_files.obj_file, '_blank');
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
                    if (professional3D?.blender_files?.blend_file) {
                      window.open(professional3D.blender_files.blend_file, '_blank');
                    }
                  }}
                  className="text-purple-700 border-purple-300 hover:bg-purple-50"
                >
                  🔧 Download Blend File
                </Button>
                <Badge variant="outline" className="text-green-700 border-green-300">
                  Scene ID: {professional3D?.scene_id?.slice(0, 8)}...
                </Badge>
              </div>
            </div>
          )}

          {/* Status Bar */}
          <div className="flex items-center justify-between mb-4">
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
                onClick={() => renderScene('single')}
                disabled={isLoading}
              >
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Eye className="w-4 h-4" />}
                Single View
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => renderScene('360')}
                disabled={isLoading}
              >
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RotateCcw className="w-4 h-4" />}
                360° View
              </Button>
            </div>
          </div>

          {/* Main Render Display */}
          <div className="border rounded-lg p-4 mb-4 bg-gray-50">
            {selectedRender ? (
              <div className="text-center">
                <div className="relative">
                  <Image
                    src={selectedRender.url}
                    alt="Blender 3D Render"
                    width={800}
                    height={600}
                    className="max-w-full max-h-full object-contain mx-auto rounded-lg shadow-md"
                    onClick={() => handleRoomClick(selectedRender.id)}
                  />
                  {/* Download and View Controls */}
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
                      onClick={() => window.open(selectedRender.url, '_blank')}
                      className="bg-white/90 backdrop-blur-sm"
                    >
                      🔍 View Full Size
                    </Button>
                  </div>
                </div>
                <div className="mt-4 text-sm text-gray-600">
                  <div className="flex justify-center items-center gap-4">
                    <span>
                      {selectedRender.type === '360' ? '360° View' : 'Single View'} • 
                      {new Date(selectedRender.timestamp).toLocaleTimeString()}
                    </span>
                    <Badge variant="outline" className="text-xs">
                      {selectedRender.status}
                    </Badge>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Camera className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No renders available</p>
                <p className="text-sm">Click a render button to generate visualization</p>
              </div>
            )}
          </div>

          {/* Render History */}
          {renders.length > 0 && (
            <div>
              <h4 className="font-medium mb-2">Render History</h4>
              <div className="flex gap-2 overflow-x-auto pb-2">
                {renders.map((render: BlenderRender) => (
                  <div
                    key={render.id}
                    className={`flex-shrink-0 border rounded p-2 cursor-pointer transition-all ${
                      selectedRender?.id === render.id 
                        ? 'border-blue-500 bg-blue-50' 
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setSelectedRender(render)}
                  >
                    <Image
                      src={render.url}
                      alt={`Render ${render.type}`}
                      width={100}
                      height={75}
                      className="object-cover rounded"
                    />
                    <div className="mt-1 text-xs text-center">
                      <Badge variant="outline" className="text-xs">
                        {render.type === '360' ? '360°' : 'Single'}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Room Info */}
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-medium mb-2">Building Information</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Rooms:</span> {rooms.length}
              </div>
              <div>
                <span className="font-medium">Dimensions:</span> {buildingDimensions.total_width}m × {buildingDimensions.total_length}m
              </div>
              <div>
                <span className="font-medium">Height:</span> {buildingDimensions.height}m
              </div>
              <div>
                <span className="font-medium">Total Area:</span> {(buildingDimensions.total_width * buildingDimensions.total_length).toFixed(1)}m²
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default BlenderRoomViewer;
