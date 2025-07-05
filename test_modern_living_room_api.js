/**
 * Modern Living Room API Test
 * Tests the MCP API routes for creating a 3D scene
 */

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

async function testModernLivingRoomAPI() {
  console.log('🏠 Testing Modern Living Room API...');
  
  try {
    // Test MCP connection
    console.log('🔗 Testing MCP connection...');
    const connectResponse = await fetch('http://localhost:3000/api/mcp/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!connectResponse.ok) {
      throw new Error(`Connection failed: ${connectResponse.statusText}`);
    }
    
    const connectionResult = await connectResponse.json();
    console.log('✅ MCP Connection:', connectionResult);
    
    // Create the 3D scene
    console.log('🎨 Creating 3D scene...');
    const sceneResponse = await fetch('http://localhost:3000/api/mcp/create-scene', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(modernLivingRoomData)
    });
    
    if (!sceneResponse.ok) {
      throw new Error(`Scene creation failed: ${sceneResponse.statusText}`);
    }
    
    const sceneResult = await sceneResponse.json();
    console.log('✅ Scene Created:', sceneResult);
    
    // Render single view
    console.log('📸 Rendering single view...');
    const singleRenderResponse = await fetch('http://localhost:3000/api/mcp/render-scene', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ view_type: 'single' })
    });
    
    if (!singleRenderResponse.ok) {
      throw new Error(`Single render failed: ${singleRenderResponse.statusText}`);
    }
    
    const singleRenderResult = await singleRenderResponse.json();
    console.log('✅ Single View Rendered:', singleRenderResult);
    
    // Render 360-degree view
    console.log('🔄 Rendering 360-degree view...');
    const panoramaRenderResponse = await fetch('http://localhost:3000/api/mcp/render-scene', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ view_type: '360' })
    });
    
    if (!panoramaRenderResponse.ok) {
      throw new Error(`360 render failed: ${panoramaRenderResponse.statusText}`);
    }
    
    const panoramaRenderResult = await panoramaRenderResponse.json();
    console.log('✅ 360-degree View Rendered:', panoramaRenderResult);
    
    return {
      connection: connectionResult,
      scene: sceneResult,
      renders: {
        single: singleRenderResult,
        panorama: panoramaRenderResult
      }
    };
    
  } catch (error) {
    console.error('❌ API Test Error:', error);
    throw error;
  }
}

// Export for use in browser or Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { testModernLivingRoomAPI, modernLivingRoomData };
} else if (typeof window !== 'undefined') {
  window.testModernLivingRoomAPI = testModernLivingRoomAPI;
  window.modernLivingRoomData = modernLivingRoomData;
}
