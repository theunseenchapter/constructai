'use client';

import React, { useState, useEffect } from 'react';
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
  onRoomSelect,
  className = ""
}) => {
  const [renders, setRenders] = useState<BlenderRender[]>([]);
  const [selectedRender, setSelectedRender] = useState<BlenderRender | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mcpStatus, setMcpStatus] = useState<MCPServerStatus>({ connected: false });

  // MCP Server communication functions
  const connectToMCP = async () => {
    try {
      setIsLoading(true);
      // Simulate MCP server connection
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMcpStatus({ connected: true, version: "1.0.0" });
    } catch (error) {
      setMcpStatus({ connected: false, error: error instanceof Error ? error.message : 'Unknown error' });
    } finally {
      setIsLoading(false);
    }
  };

  const create3DScene = async () => {
    if (!mcpStatus.connected) {
      await connectToMCP();
    }

    try {
      setIsLoading(true);
      
      // For now, simulate successful scene creation
      console.log('Scene created with rooms:', rooms.length);
      
    } catch (error) {
      console.error('Error creating 3D scene:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const renderScene = async (type: 'single' | '360') => {
    if (!mcpStatus.connected) {
      await connectToMCP();
    }

    try {
      setIsLoading(true);
      
      // For now, simulate render creation with placeholder images
      const newRender: BlenderRender = {
        id: Date.now().toString(),
        url: generateMockRenderUrl(type),
        type,
        timestamp: Date.now(),
        status: 'completed'
      };

      setRenders(prev => [newRender, ...prev]);
      setSelectedRender(newRender);
      
    } catch (error) {
      console.error('Error rendering scene:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateMockRenderUrl = (type: 'single' | '360'): string => {
    // Generate a mock SVG render for demonstration
    const svg = `
      <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#F0F8FF;stop-opacity:1" />
          </linearGradient>
          <linearGradient id="floorGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#D2B48C;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#A0522D;stop-opacity:1" />
          </linearGradient>
        </defs>
        
        <!-- Background -->
        <rect width="800" height="600" fill="url(#skyGradient)"/>
        
        <!-- Floor -->
        <polygon points="50,550 750,550 700,400 100,400" fill="url(#floorGradient)"/>
        
        <!-- Walls -->
        <polygon points="100,400 700,400 700,100 100,100" fill="#F5F5DC" stroke="#D3D3D3" stroke-width="2"/>
        <polygon points="700,400 750,350 750,50 700,100" fill="#E6E6FA" stroke="#D3D3D3" stroke-width="2"/>
        
        <!-- Rooms -->
        ${rooms.map((room, index) => {
          const x = 150 + (index * 150);
          const y = 300;
          const roomColor = getRoomColor(room.type);
          
          return `
            <!-- Room ${room.name} -->
            <rect x="${x}" y="${y}" width="120" height="80" fill="${roomColor}" stroke="#333" stroke-width="1" opacity="0.8"/>
            <text x="${x + 60}" y="${y + 45}" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">${room.name}</text>
            
            <!-- Furniture -->
            ${room.type === 'bedroom' ? `
              <rect x="${x + 10}" y="${y + 10}" width="40" height="20" fill="#8B4513" opacity="0.6"/>
              <rect x="${x + 60}" y="${y + 50}" width="15" height="25" fill="#654321" opacity="0.6"/>
            ` : ''}
            ${room.type === 'kitchen' ? `
              <rect x="${x + 10}" y="${y + 10}" width="100" height="15" fill="#696969" opacity="0.6"/>
              <rect x="${x + 10}" y="${y + 50}" width="25" height="25" fill="#A9A9A9" opacity="0.6"/>
            ` : ''}
            ${room.type === 'living_room' ? `
              <rect x="${x + 20}" y="${y + 30}" width="60" height="20" fill="#DDA0DD" opacity="0.6"/>
              <rect x="${x + 30}" y="${y + 55}" width="30" height="20" fill="#8B4513" opacity="0.6"/>
            ` : ''}
          `;
        }).join('')}
        
        <!-- Lighting effects -->
        <circle cx="400" cy="50" r="30" fill="#FFD700" opacity="0.3"/>
        <circle cx="400" cy="50" r="60" fill="#FFD700" opacity="0.1"/>
        
        <!-- View type indicator -->
        <text x="20" y="30" font-family="Arial" font-size="14" fill="#333" font-weight="bold">
          ${type === '360' ? '360° View' : 'Single View'}
        </text>
        
        <!-- Building dimensions -->
        <text x="20" y="580" font-family="Arial" font-size="12" fill="#666">
          ${buildingDimensions.total_width}m × ${buildingDimensions.total_length}m × ${buildingDimensions.height}m
        </text>
      </svg>
    `;
    
    return `data:image/svg+xml;base64,${btoa(svg)}`;
  };

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
  }, [rooms, mcpStatus.connected]);

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
                <Image
                  src={selectedRender.url}
                  alt="Blender 3D Render"
                  width={800}
                  height={600}
                  className="max-w-full max-h-full object-contain mx-auto"
                  onClick={() => handleRoomClick(selectedRender.id)}
                />
                <div className="mt-2 text-sm text-gray-600">
                  {selectedRender.type === '360' ? '360° View' : 'Single View'} • 
                  {new Date(selectedRender.timestamp).toLocaleTimeString()}
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
                {renders.map((render) => (
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
