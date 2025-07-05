import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

export async function POST() {
  try {
    const publicRendersDir = path.join(process.cwd(), 'public', 'renders');
    
    // Ensure public/renders directory exists
    await fs.mkdir(publicRendersDir, { recursive: true });

    // Create some test render files (SVG images that look like architectural renders)
    const testRenders = [
      {
        name: 'modern_living_room_single.png',
        content: createMockRenderSVG('Modern Living Room - Single View', 'living_room')
      },
      {
        name: 'modern_living_room_360.png', 
        content: createMockRenderSVG('Modern Living Room - 360° View', 'living_room_360')
      },
      {
        name: 'kitchen_design.png',
        content: createMockRenderSVG('Kitchen Design', 'kitchen')
      }
    ];

    const createdFiles = [];

    for (const render of testRenders) {
      const filePath = path.join(publicRendersDir, render.name);
      
      // Only create if doesn't exist
      try {
        await fs.access(filePath);
      } catch {
        await fs.writeFile(filePath, render.content);
        const stats = await fs.stat(filePath);
        createdFiles.push({
          name: render.name,
          path: filePath,
          publicPath: `/renders/${render.name}`,
          size: stats.size,
          created: stats.birthtime,
          url: `/renders/${render.name}`
        });
      }
    }

    return NextResponse.json({ 
      message: `Created ${createdFiles.length} test renders`,
      renders: createdFiles
    });
  } catch (error) {
    console.error('Error creating test renders:', error);
    return NextResponse.json({ error: 'Failed to create test renders' }, { status: 500 });
  }
}

function createMockRenderSVG(title: string, type: string): string {
  const roomColors = {
    living_room: '#F0F8FF',
    living_room_360: '#E6E6FA', 
    kitchen: '#F0FFF0'
  };

  const bgColor = roomColors[type as keyof typeof roomColors] || '#F5F5F5';

  return `<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bgGradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" style="stop-color:${bgColor};stop-opacity:1" />
        <stop offset="100%" style="stop-color:#FFFFFF;stop-opacity:1" />
      </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="800" height="600" fill="url(#bgGradient)"/>
    
    <!-- Title -->
    <text x="400" y="40" text-anchor="middle" font-family="Arial" font-size="24" font-weight="bold" fill="#333">
      ${title}
    </text>
    
    <!-- Main Room -->
    <rect x="100" y="100" width="600" height="400" fill="${bgColor}" stroke="#333" stroke-width="2" opacity="0.8"/>
    
    <!-- Furniture based on room type -->
    ${type === 'living_room' ? `
      <!-- Sofa -->
      <rect x="150" y="350" width="200" height="80" fill="#8B4513" rx="10"/>
      <!-- Coffee Table -->
      <rect x="200" y="300" width="100" height="40" fill="#654321" rx="5"/>
      <!-- TV -->
      <rect x="500" y="150" width="150" height="100" fill="#000" rx="5"/>
    ` : ''}
    
    ${type === 'kitchen' ? `
      <!-- Kitchen Island -->
      <rect x="300" y="250" width="200" height="100" fill="#D2691E" rx="5"/>
      <!-- Cabinets -->
      <rect x="150" y="150" width="500" height="50" fill="#8B4513" rx="3"/>
      <!-- Appliances -->
      <rect x="200" y="200" width="60" height="60" fill="#C0C0C0" rx="5"/>
      <rect x="300" y="200" width="60" height="60" fill="#C0C0C0" rx="5"/>
    ` : ''}
    
    ${type === 'living_room_360' ? `
      <!-- 360 View Indicator -->
      <circle cx="400" cy="300" r="150" fill="none" stroke="#4169E1" stroke-width="3" stroke-dasharray="10,5"/>
      <text x="400" y="305" text-anchor="middle" font-family="Arial" font-size="16" fill="#4169E1">360° VIEW</text>
      <!-- Multiple furniture views -->
      <rect x="150" y="350" width="200" height="80" fill="#8B4513" rx="10" opacity="0.7"/>
      <rect x="450" y="350" width="200" height="80" fill="#8B4513" rx="10" opacity="0.7"/>
    ` : ''}
    
    <!-- Floor pattern -->
    <pattern id="floorPattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <rect width="20" height="20" fill="#DEB887"/>
      <rect width="19" height="19" fill="#D2B48C"/>
    </pattern>
    <rect x="100" y="480" width="600" height="20" fill="url(#floorPattern)"/>
    
    <!-- Timestamp -->
    <text x="750" y="580" text-anchor="end" font-family="Arial" font-size="12" fill="#666">
      Generated: ${new Date().toLocaleString()}
    </text>
  </svg>`;
}
