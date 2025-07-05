/**
 * Modern Living Room 3D Scene Creation Test
 * Using Blender MCP Server through GitHub Copilot integration
 */

import { mcpClient } from './src/lib/mcp-client';

// Modern living room configuration
const modernLivingRoomData = {
  rooms: [
    {
      name: "Modern Living Room",
      type: "living_room",
      width: 6,
      length: 8,
      height: 3.2,
      style: "modern",
      furniture: [
        {
          type: "sectional_sofa",
          position: { x: 2, y: 1, z: 0 },
          color: "#2C3E50",
          material: "leather"
        },
        {
          type: "coffee_table",
          position: { x: 3, y: 2.5, z: 0 },
          color: "#8B4513",
          material: "wood"
        },
        {
          type: "tv_stand",
          position: { x: 5.5, y: 4, z: 0 },
          color: "#1C1C1C",
          material: "metal"
        },
        {
          type: "floor_lamp",
          position: { x: 1, y: 1, z: 0 },
          color: "#FFFFFF",
          material: "modern"
        },
        {
          type: "bookshelf",
          position: { x: 0.5, y: 6, z: 0 },
          color: "#8B4513",
          material: "wood"
        },
        {
          type: "accent_chair",
          position: { x: 4.5, y: 1.5, z: 0 },
          color: "#34495E",
          material: "fabric"
        }
      ],
      lighting: {
        natural: {
          windows: [
            {
              position: { x: 0, y: 4, z: 2 },
              width: 2,
              height: 1.5
            }
          ]
        },
        artificial: [
          {
            type: "ceiling_light",
            position: { x: 3, y: 4, z: 3 },
            brightness: 0.8
          },
          {
            type: "ambient_lighting",
            color: "#FFF8DC",
            brightness: 0.3
          }
        ]
      },
      materials: {
        floor: {
          type: "hardwood",
          color: "#8B4513",
          texture: "oak"
        },
        walls: {
          type: "paint",
          color: "#F5F5F5",
          accent_wall: {
            color: "#2C3E50",
            position: "north"
          }
        },
        ceiling: {
          type: "paint",
          color: "#FFFFFF"
        }
      }
    }
  ],
  building_dimensions: {
    total_width: 6,
    total_length: 8,
    height: 3.2,
    style: "modern_minimalist"
  }
};

async function createModernLivingRoom() {
  console.log('🏠 Creating Modern Living Room Scene...');
  
  try {
    // Initialize MCP client
    const initialized = await mcpClient.initialize();
    if (!initialized) {
      throw new Error('Failed to initialize MCP client');
    }
    
    console.log('✅ MCP Client initialized successfully');
    
    // Create the 3D scene
    console.log('🎨 Creating 3D scene with modern living room...');
    const sceneResult = await mcpClient.callTool('create_3d_scene', modernLivingRoomData);
    
    console.log('✅ Scene created successfully:', sceneResult);
    
    // Render the scene in single view
    console.log('📸 Rendering scene (single view)...');
    const singleRender = await mcpClient.callTool('render_scene', { 
      view_type: 'single' 
    });
    
    console.log('✅ Single view rendered:', singleRender);
    
    // Render the scene in 360-degree view
    console.log('🔄 Rendering scene (360-degree view)...');
    const panoramaRender = await mcpClient.callTool('render_scene', { 
      view_type: '360' 
    });
    
    console.log('✅ 360-degree view rendered:', panoramaRender);
    
    return {
      scene: sceneResult,
      renders: {
        single: singleRender,
        panorama: panoramaRender
      }
    };
    
  } catch (error) {
    console.error('❌ Error creating modern living room:', error);
    throw error;
  }
}

// Execute the scene creation
createModernLivingRoom()
  .then(result => {
    console.log('🎉 Modern Living Room Scene Created Successfully!');
    console.log('Scene Data:', JSON.stringify(result, null, 2));
  })
  .catch(error => {
    console.error('Failed to create scene:', error);
  });

export { createModernLivingRoom, modernLivingRoomData };
