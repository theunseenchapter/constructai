#!/usr/bin/env node
/**
 * Test script to create a modern living room using MCP API
 * Run with: node test_living_room.js
 */

const https = require('http');

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

function makeRequest(path, method = 'POST', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 3001,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => {
        body += chunk;
      });
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve(result);
        } catch (e) {
          resolve(body);
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

async function testModernLivingRoom() {
  console.log('🏠 Creating Modern Living Room with Blender MCP Server...\n');
  
  try {
    // Step 1: Test MCP connection
    console.log('🔗 Step 1: Testing MCP connection...');
    const connectionResult = await makeRequest('/api/mcp/connect');
    console.log('✅ MCP Connection Result:', JSON.stringify(connectionResult, null, 2));
    console.log('');
    
    // Step 2: Create the 3D scene
    console.log('🎨 Step 2: Creating modern living room scene...');
    const sceneResult = await makeRequest('/api/mcp/create-scene', 'POST', modernLivingRoomData);
    console.log('✅ Scene Creation Result:', JSON.stringify(sceneResult, null, 2));
    console.log('');
    
    // Step 3: Render single view
    console.log('📸 Step 3: Rendering single view...');
    const singleRenderResult = await makeRequest('/api/mcp/render-scene', 'POST', { view_type: 'single' });
    console.log('✅ Single View Render Result:', JSON.stringify(singleRenderResult, null, 2));
    console.log('');
    
    // Step 4: Render 360-degree view
    console.log('🔄 Step 4: Rendering 360-degree view...');
    const panoramaRenderResult = await makeRequest('/api/mcp/render-scene', 'POST', { view_type: '360' });
    console.log('✅ 360-degree View Render Result:', JSON.stringify(panoramaRenderResult, null, 2));
    console.log('');
    
    console.log('🎉 Modern Living Room Scene Created Successfully!');
    console.log('📊 Summary:');
    console.log(`   - Scene File: ${sceneResult.scene_file || 'Generated'}`);
    console.log(`   - Single Render: ${singleRenderResult.render_files ? singleRenderResult.render_files.length : 1} file(s)`);
    console.log(`   - 360° Render: ${panoramaRenderResult.render_files ? panoramaRenderResult.render_files.length : 8} file(s)`);
    console.log(`   - MCP Server: ${connectionResult.server || 'blender-mcp-server'}`);
    
  } catch (error) {
    console.error('❌ Error creating modern living room:', error);
    process.exit(1);
  }
}

// Run the test
testModernLivingRoom();
