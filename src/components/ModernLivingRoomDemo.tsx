/**
 * Modern Living Room Demo Component
 * Demonstrates 3D scene creation with Blender MCP server
 */

'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { mcpClient } from '../lib/mcp-client';

interface SceneData {
  success: boolean;
  scene_file?: string;
  message: string;
}

interface RenderData {
  single?: {
    render_files?: string[];
    success: boolean;
    message: string;
  };
  panorama?: {
    render_files?: string[];
    success: boolean;
    message: string;
  };
}

interface ModernLivingRoomDemoProps {
  onSceneCreated?: (sceneData: SceneData) => void;
  onRenderComplete?: (renderData: RenderData) => void;
}

const modernLivingRoomConfig = {
  scene_type: "interior_design",
  quality: "ultra_high",
  detail_level: "maximum",
  style: "modern_luxury",
  rooms: [
    {
      name: "Modern Living Room",
      type: "living_room",
      width: 6,
      length: 8,
      height: 3.2,
      style: "modern_contemporary",
      furniture: [
        {
          type: "sectional_sofa",
          position: { x: 2, y: 1, z: 0 },
          rotation: { x: 0, y: 45, z: 0 },
          dimensions: { width: 2.8, depth: 1.8, height: 0.8 },
          color: "#2C3E50",
          material: "premium_leather",
          details: {
            cushions: 5,
            style: "L_shaped",
            tufting: true,
            chrome_legs: true
          }
        },
        {
          type: "coffee_table",
          position: { x: 3, y: 2.5, z: 0 },
          dimensions: { width: 1.2, depth: 0.6, height: 0.4 },
          color: "#8B4513",
          material: "walnut_wood",
          details: {
            glass_top: true,
            storage_shelf: true,
            rounded_corners: true,
            finish: "matte_lacquer"
          }
        },
        {
          type: "tv_console",
          position: { x: 5.5, y: 4, z: 0 },
          dimensions: { width: 1.8, depth: 0.4, height: 0.5 },
          color: "#FFFFFF",
          material: "high_gloss_lacquer",
          details: {
            floating_mount: true,
            led_backlighting: true,
            cable_management: true,
            walnut_accents: true
          }
        },
        {
          type: "floor_lamp",
          position: { x: 1, y: 1, z: 0 },
          dimensions: { width: 0.3, depth: 0.3, height: 1.8 },
          color: "#C0C0C0",
          material: "brushed_steel",
          details: {
            style: "arc_lamp",
            marble_base: true,
            dimmer_switch: true,
            led_bulb: true
          }
        },
        {
          type: "bookshelf",
          position: { x: 0.5, y: 6, z: 0 },
          dimensions: { width: 1.2, depth: 0.3, height: 2.2 },
          color: "#8B4513",
          material: "solid_walnut",
          details: {
            floating_design: true,
            adjustable_shelves: 5,
            invisible_brackets: true,
            books_and_decor: true
          }
        },
        {
          type: "accent_chair",
          position: { x: 4.5, y: 1.5, z: 0 },
          rotation: { x: 0, y: -30, z: 0 },
          dimensions: { width: 0.8, depth: 0.8, height: 1.1 },
          color: "#E74C3C",
          material: "velvet_fabric",
          details: {
            style: "mid_century_modern",
            swivel_base: true,
            brass_legs: true,
            ergonomic_design: true
          }
        }
      ],
      lighting: {
        natural: {
          windows: [
            {
              position: { x: 0, y: 4, z: 2 },
              width: 2.5,
              height: 1.8,
              style: "floor_to_ceiling",
              frame: "black_aluminum",
              glass: "double_pane"
            }
          ]
        },
        artificial: [
          {
            type: "pendant_lights",
            position: { x: 3, y: 4, z: 2.8 },
            count: 3,
            style: "geometric_modern",
            material: "brass_and_glass",
            brightness: 0.8
          },
          {
            type: "recessed_lighting",
            count: 6,
            spacing: "even_grid",
            dimmer: true,
            color_temperature: 3000,
            brightness: 0.6
          },
          {
            type: "ambient_lighting",
            color: "#FFF8DC",
            brightness: 0.3,
            source: "led_strips"
          }
        ]
      },
      materials: {
        floor: {
          type: "engineered_hardwood",
          wood_type: "white_oak",
          color: "#D4B896",
          texture: "wide_plank",
          finish: "natural_oil",
          pattern: "straight_lay"
        },
        walls: {
          type: "premium_paint",
          color: "#F8F9FA",
          finish: "eggshell",
          accent_wall: {
            color: "#2C3E50",
            position: "north",
            texture: "smooth_matte"
          }
        },
        ceiling: {
          type: "drywall",
          color: "#FFFFFF",
          finish: "smooth",
          crown_molding: true,
          recessed_lights: true
        }
      },
      decor: [
        {
          type: "area_rug",
          position: { x: 3, y: 3, z: 0.01 },
          dimensions: { width: 2.5, depth: 3.0 },
          pattern: "geometric_modern",
          colors: ["#34495E", "#ECF0F1", "#95A5A6"]
        },
        {
          type: "throw_pillows",
          count: 4,
          colors: ["#E74C3C", "#F39C12", "#ECF0F1", "#34495E"],
          materials: ["velvet", "linen", "faux_fur"]
        },
        {
          type: "wall_art",
          style: "abstract_modern",
          size: "large",
          frame: "black_metal"
        },
        {
          type: "plants",
          items: ["fiddle_leaf_fig", "snake_plant", "monstera"]
        }
      ]
    }
  ],
  building_dimensions: {
    total_width: 6,
    total_length: 8,
    height: 3.2,
    style: "modern_luxury"
  },
  render_settings: {
    quality: "ultra_high",
    lighting: "realistic_pbr",
    shadows: "raytraced",
    resolution: { width: 1920, height: 1080 },
    samples: 512
  },
  export_settings: {
    format: "obj_with_mtl",
    include_materials: true,
    mesh_quality: "high",
    scale: "real_world_meters"
  }
};

// Simplified configuration for better MCP server compatibility
const simplifiedLivingRoomConfig = {
  scene_type: "living_room",
  style: "modern",
  dimensions: { width: 6, length: 8, height: 3.2 },
  furniture: [
    {
      type: "sofa",
      position: [2, 1, 0],
      size: "large",
      material: "leather",
      color: "#2C3E50"
    },
    {
      type: "coffee_table", 
      position: [3, 2.5, 0],
      material: "wood",
      color: "#8B4513"
    },
    {
      type: "tv_unit",
      position: [5.5, 4, 0], 
      material: "modern",
      color: "#FFFFFF"
    },
    {
      type: "chair",
      position: [4.5, 1.5, 0],
      material: "fabric", 
      color: "#E74C3C"
    }
  ],
  walls: {
    material: "paint",
    color: "#F8F9FA",
    accent: "#2C3E50"
  },
  floor: {
    material: "hardwood",
    color: "#D4B896" 
  },
  lighting: "modern",
  quality: "high"
};

export default function ModernLivingRoomDemo({ onSceneCreated, onRenderComplete }: ModernLivingRoomDemoProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [isRendering, setIsRendering] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [sceneData, setSceneData] = useState<SceneData | null>(null);
  const [renderData, setRenderData] = useState<RenderData | null>(null);
  const [mcpStatus, setMcpStatus] = useState<string>('Not Connected');
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const checkMCPStatus = useCallback(async () => {
    try {
      const status = await mcpClient.getServerStatus();
      setMcpStatus(status.connected ? 'Connected' : 'Disconnected');
      addLog(`MCP Server Status: ${status.connected ? 'Connected' : 'Disconnected'}`);
    } catch (error) {
      setMcpStatus('Error');
      addLog(`MCP Status Error: ${error}`);
    }
  }, []);

  useEffect(() => {
    // Check MCP server status on mount
    checkMCPStatus();
  }, [checkMCPStatus]);

  const createModernLivingRoom = async () => {
    setIsCreating(true);
    addLog('🏠 Starting Modern Living Room Creation...');
    addLog(`📋 Scene Config: ${JSON.stringify(modernLivingRoomConfig).substring(0, 200)}...`);
    
    try {
      // Initialize MCP client
      addLog('🔗 Initializing MCP Client...');
      const initialized = await mcpClient.initialize();
      if (!initialized) {
        throw new Error('Failed to initialize MCP client');
      }
      addLog('✅ MCP Client Initialized');
      
      // Create the scene with detailed configuration
      addLog('🎨 Creating High-Quality 3D Scene...');
      addLog('📝 Sending detailed furniture specifications...');
      addLog('🎯 Quality: Ultra-High, Style: Modern Luxury');
      
      const sceneResult = await mcpClient.callTool('create_3d_scene', modernLivingRoomConfig);
      const typedSceneResult = sceneResult as SceneData;
      
      addLog(`🔍 Scene Result: ${JSON.stringify(typedSceneResult).substring(0, 300)}...`);
      addLog(`📁 Scene File: ${typedSceneResult.scene_file || 'Not specified'}`);
      
      setSceneData(typedSceneResult);
      addLog('✅ High-Quality Scene Created Successfully');
      
      if (onSceneCreated) {
        onSceneCreated(typedSceneResult);
      }
      
      // Render the scene
      await renderScene();
      
    } catch (error) {
      addLog(`❌ Error: ${error}`);
      console.error('Error creating modern living room:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const renderScene = async () => {
    if (!sceneData) {
      addLog('❌ No scene data available for rendering');
      return;
    }

    setIsRendering(true);
    addLog('📸 Starting Scene Rendering...');
    
    try {
      // Render single view
      addLog('📸 Rendering Single View...');
      const singleRender = await mcpClient.callTool('render_scene', { view_type: 'single' });
      addLog(`🔍 Single render result: ${JSON.stringify(singleRender).substring(0, 200)}...`);
      
      // Render 360-degree view
      addLog('🔄 Rendering 360-degree View...');
      const panoramaRender = await mcpClient.callTool('render_scene', { view_type: '360' });
      addLog(`🔍 Panorama render result: ${JSON.stringify(panoramaRender).substring(0, 200)}...`);
      
      const renderResult: RenderData = {
        single: singleRender as SceneData,
        panorama: panoramaRender as SceneData
      };
      
      setRenderData(renderResult);
      addLog('✅ All Renders Complete');
      
      if (onRenderComplete) {
        onRenderComplete(renderResult);
      }
      
    } catch (error) {
      addLog(`❌ Render Error: ${error}`);
      console.error('Error rendering scene:', error);
    } finally {
      setIsRendering(false);
    }
  };

  const downloadRenders = async () => {
    if (!sceneData) {
      addLog('❌ No scene data available for download');
      return;
    }

    setIsDownloading(true);
    addLog('💾 Starting 3D model downloads...');

    try {
      // Copy 3D model files to D:\constructai\downloads folder
      addLog('📁 Copying 3D models to D:\\constructai\\downloads...');
      const response = await fetch('/api/renders/download', { method: 'POST' });
      const data = await response.json();
      
      addLog(`📊 API Response: Found ${data.files?.length || 0} model files`);
      
      if (data.success && data.files && data.files.length > 0) {
        addLog(`📥 Found ${data.files.length} 3D model files to download`);
        addLog(`📂 Files saved to: ${data.downloadsPath}`);
        
        // Show the model files that were copied
        for (const file of data.files) {
          addLog(`✅ Copied ${file.type.toUpperCase()} file: ${file.originalName} → ${file.name}`);
        }
        
        addLog(`🎉 Download complete! ${data.files.length} 3D model files saved to D:\\constructai\\downloads`);
        addLog(`📂 Open folder: D:\\constructai\\downloads to view your 3D models`);
        addLog(`🔧 Import .obj files directly into Blender to view your scene!`);
      } else {
        addLog('❌ No 3D model files found. Create a scene first!');
        addLog('🔍 Make sure the scene creation completed successfully.');
      }
    } catch (error) {
      addLog(`❌ Download failed: ${error}`);
      console.error('Error downloading 3D models:', error);
    } finally {
      setIsDownloading(false);
    }
  };

  const createSimplifiedRoom = async () => {
    setIsCreating(true);
    addLog('🏠 Creating Simplified High-Quality Room...');
    addLog('🔧 Using optimized configuration for better results');
    
    try {
      // Initialize MCP client
      addLog('🔗 Initializing MCP Client...');
      const initialized = await mcpClient.initialize();
      if (!initialized) {
        throw new Error('Failed to initialize MCP client');
      }
      addLog('✅ MCP Client Initialized');
      
      // Create the scene with simplified but effective config
      addLog('🎨 Creating Optimized 3D Scene...');
      const sceneResult = await mcpClient.callTool('create_3d_scene', simplifiedLivingRoomConfig);
      const typedSceneResult = sceneResult as SceneData;
      
      addLog(`🔍 Scene Result: ${JSON.stringify(typedSceneResult).substring(0, 300)}...`);
      addLog(`📁 Scene File: ${typedSceneResult.scene_file || 'Not specified'}`);
      
      setSceneData(typedSceneResult);
      addLog('✅ Optimized Scene Created Successfully');
      
      if (onSceneCreated) {
        onSceneCreated(typedSceneResult);
      }
      
      // Render the scene
      await renderScene();
      
    } catch (error) {
      addLog(`❌ Error: ${error}`);
      console.error('Error creating simplified living room:', error);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="modern-living-room-demo p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">🏠 Modern Living Room - Blender MCP Demo</h1>
        <p className="text-gray-600 mb-4">
          This demo creates a modern living room using the Blender MCP server integration with GitHub Copilot.
        </p>
        
        <div className="mb-4">
          <span className="font-semibold">MCP Server Status: </span>
          <span className={`px-2 py-1 rounded text-sm ${
            mcpStatus === 'Connected' ? 'bg-green-100 text-green-800' :
            mcpStatus === 'Disconnected' ? 'bg-red-100 text-red-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {mcpStatus}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Control Panel */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Control Panel</h2>
          
          <div className="space-y-4">
            <button
              onClick={createModernLivingRoom}
              disabled={isCreating}
              className={`w-full py-3 px-4 rounded-lg font-medium ${
                isCreating 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              {isCreating ? '🔄 Creating Scene...' : '🎨 Create Detailed Room'}
            </button>

            <button
              onClick={createSimplifiedRoom}
              disabled={isCreating}
              className={`w-full py-3 px-4 rounded-lg font-medium ${
                isCreating 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-orange-600 hover:bg-orange-700 text-white'
              }`}
            >
              {isCreating ? '🔄 Creating Scene...' : '🔧 Create Optimized Room'}
            </button>

            <button
              onClick={renderScene}
              disabled={isRendering || !sceneData}
              className={`w-full py-3 px-4 rounded-lg font-medium ${
                isRendering || !sceneData
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {isRendering ? '🔄 Rendering...' : '📸 Render Scene'}
            </button>

            <button
              onClick={checkMCPStatus}
              className="w-full py-2 px-4 rounded-lg font-medium bg-gray-200 hover:bg-gray-300 text-gray-800"
            >
              🔄 Check MCP Status
            </button>

            <button
              onClick={downloadRenders}
              disabled={isDownloading || !sceneData}
              className={`w-full py-3 px-4 rounded-lg font-medium ${
                isDownloading || !sceneData
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-purple-600 hover:bg-purple-700 text-white'
              }`}
            >
              {isDownloading ? '🔄 Downloading 3D Models...' : '� Download 3D Models (.obj)'}
            </button>

            <button
              onClick={createSimplifiedRoom}
              disabled={isCreating}
              className={`w-full py-3 px-4 rounded-lg font-medium ${
                isCreating 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-orange-600 hover:bg-orange-700 text-white'
              }`}
            >
              {isCreating ? '🔄 Creating Simplified Room...' : '🏡 Create Simplified Room'}
            </button>
          </div>
        </div>

        {/* Scene Configuration */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Scene Configuration</h2>
          
          <div className="text-sm text-gray-600 space-y-2">
            <div><strong>Room Type:</strong> Modern Living Room</div>
            <div><strong>Dimensions:</strong> 6m × 8m × 3.2m</div>
            <div><strong>Style:</strong> Modern Minimalist</div>
            <div><strong>Furniture:</strong> 6 pieces</div>
            <div><strong>Lighting:</strong> Natural + Artificial</div>
            <div><strong>Materials:</strong> Hardwood, Paint, Fabric</div>
          </div>
          
          <div className="mt-4">
            <h3 className="font-medium mb-2">Furniture List:</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Sectional Sofa (Leather)</li>
              <li>• Coffee Table (Wood)</li>
              <li>• TV Stand (Metal)</li>
              <li>• Floor Lamp (Modern)</li>
              <li>• Bookshelf (Wood)</li>
              <li>• Accent Chair (Fabric)</li>
            </ul>
          </div>

          <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="font-medium mb-1 text-blue-800">� 3D Models Location:</h3>
            <p className="text-xs text-blue-600">D:\constructai\downloads</p>
            <p className="text-xs text-blue-500 mt-1">Import .obj files into Blender</p>
          </div>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Results</h2>
          
          {sceneData && (
            <div className="mb-4">
              <h3 className="font-medium text-green-600 mb-2">✅ Scene Created</h3>
              <div className="text-sm text-gray-600">
                <div>Scene File: {sceneData.scene_file || 'Generated'}</div>
                <div>Status: {sceneData.success ? 'Success' : 'Failed'}</div>
                <div>Message: {sceneData.message}</div>
              </div>
            </div>
          )}

          {renderData && (
            <div className="mb-4">
              <h3 className="font-medium text-blue-600 mb-2">✅ Renders Complete</h3>
              <div className="text-sm text-gray-600">
                <div>Single View: {renderData.single?.render_files?.length || 1} file(s)</div>
                <div>360° View: {renderData.panorama?.render_files?.length || 8} file(s)</div>
              </div>
            </div>
          )}
        </div>

        {/* Logs */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Activity Log</h2>
          <div className="h-64 overflow-y-auto bg-gray-50 rounded p-3">
            {logs.length === 0 ? (
              <div className="text-gray-500 text-sm">No activity yet...</div>
            ) : (
              <div className="space-y-1">
                {logs.map((log, index) => (
                  <div key={index} className="text-xs text-gray-700 font-mono">
                    {log}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
