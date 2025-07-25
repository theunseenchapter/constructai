import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

interface BOQ3DResponse {
  boq_id: string
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  project_specs: any
  total_cost: number
  material_cost: number
  labor_cost: number
  items: Array<{
    category: string
    item: string
    quantity: number
    unit: string
    rate: number
    amount: number
  }>
  cost_breakdown: {
    material_cost: number
    labor_cost: number
    overhead_cost: number
    enhanced_features_cost?: number
    total_cost: number
    cost_per_sqft: number
  }
  room_3d_data: {
    visualization_data: {
      rooms: Array<{
        name: string
        room_type: string
        width: number
        length: number
        height: number
        area: number
        position: { x: number; y: number; z: number }
      }>
      building_dimensions: {
        total_width: number
        total_length: number
        height: number
      }
      total_doors: number
      total_windows: number
    }
  }
  model_file_path: string
  created_at: string
  config_file: string
  scene_id: string
  professional_3d?: {
    scene_id: string
    quality: string
    renderer: string
    samples: number
    resolution: string
    blender_files: {
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

// Helper function to generate mock room images for NeRF training
function generateMockRoomImages(roomsConfig: Array<{
  name: string
  room_type: string
  width: number
  length: number
  height: number
  area: number
  position: { x: number; y: number }
}>): string[] {
  const images: string[] = []
  
  // Generate image URLs based on room configuration
  roomsConfig.forEach((room, index) => {
    // In a real implementation, these would be actual photos taken of the rooms
    // For now, we generate mock image paths that would represent different views of each room
    images.push(`mock_images/room_${index + 1}_view_1.jpg`)
    images.push(`mock_images/room_${index + 1}_view_2.jpg`)
    images.push(`mock_images/room_${index + 1}_view_3.jpg`)
  })
  
  // Add overview shots
  images.push(`mock_images/house_exterior_1.jpg`)
  images.push(`mock_images/house_exterior_2.jpg`)
  images.push(`mock_images/house_interior_overview.jpg`)
  
  return images
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const specs: Record<string, any> = await request.json()
    console.log('🔍 Received specs:', specs)
    
    // Generate mock BOQ data based on specs
    // Will calculate enhanced BOQ after room configuration
    
    // Generate room configuration based on user's actual room specifications
    const roomsConfig: Array<{
      name: string
      room_type: string
      width: number
      length: number
      height: number
      area: number
      position: { x: number; y: number }
    }> = []
    
    // Use user's actual room specifications - generate rooms based on counts
    const userRooms = Array.isArray(specs.rooms) ? specs.rooms : []
    
    // If no rooms array provided, generate based on room counts
    if (userRooms.length === 0) {
      const totalArea = specs.total_area || 1000
      const totalRooms = (specs.rooms || specs.num_bedrooms || 0) + (specs.num_living_rooms || 0) + 
                        (specs.num_kitchens || 0) + (specs.num_bathrooms || 0) + 
                        (specs.num_dining_rooms || 0) + (specs.num_study_rooms || 0) + 
                        (specs.num_utility_rooms || 0) + (specs.num_guest_rooms || 0) + 
                        (specs.num_store_rooms || 0)
      
      // Calculate dynamic area per room based on room type ratios
      const baseAreaPerRoom = totalRooms > 0 ? totalArea * 0.8 / totalRooms : 100 // 80% of total area for rooms, 20% for circulation
      
      // Generate default rooms if just a number was provided
      if (typeof specs.rooms === 'number') {
        for (let i = 0; i < specs.rooms; i++) {
          userRooms.push({
            name: `Room ${i + 1}`,
            area: Math.round(baseAreaPerRoom)
          })
        }
      }
      
      // Generate bedrooms
      for (let i = 0; i < (specs.num_bedrooms || 0); i++) {
        userRooms.push({
          name: `Bedroom ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 1.2) // Bedrooms get 20% more area
        })
      }
      
      // Generate living rooms
      for (let i = 0; i < (specs.num_living_rooms || 0); i++) {
        userRooms.push({
          name: `Living Room ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 1.4) // Living rooms get 40% more area
        })
      }
      
      // Generate kitchens
      for (let i = 0; i < (specs.num_kitchens || 0); i++) {
        userRooms.push({
          name: `Kitchen ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 0.8) // Kitchens are typically smaller
        })
      }
      
      // Generate bathrooms
      for (let i = 0; i < (specs.num_bathrooms || 0); i++) {
        userRooms.push({
          name: `Bathroom ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 0.4) // Bathrooms are much smaller
        })
      }
      
      // Generate dining rooms
      for (let i = 0; i < (specs.num_dining_rooms || 0); i++) {
        userRooms.push({
          name: `Dining Room ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 1.0) // Standard area
        })
      }
      
      // Generate study rooms
      for (let i = 0; i < (specs.num_study_rooms || 0); i++) {
        userRooms.push({
          name: `Study Room ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 0.7) // Smaller than bedrooms
        })
      }
      
      // Generate utility rooms
      for (let i = 0; i < (specs.num_utility_rooms || 0); i++) {
        userRooms.push({
          name: `Utility Room ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 0.5) // Small utility areas
        })
      }
      
      // Generate guest rooms
      for (let i = 0; i < (specs.num_guest_rooms || 0); i++) {
        userRooms.push({
          name: `Guest Room ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 1.1) // Similar to bedrooms
        })
      }
      
      // Generate store rooms
      for (let i = 0; i < (specs.num_store_rooms || 0); i++) {
        userRooms.push({
          name: `Store Room ${i + 1}`,
          area: Math.round(baseAreaPerRoom * 0.3) // Very small storage areas
        })
      }
    }
    
    console.log('🏠 Generated rooms:', userRooms)
    
    let currentX = 0
    let currentY = 0
    const maxRowWidth = 30
    
    // Function to normalize room names to room types
    const getRoomType = (roomName: string): string => {
      const name = roomName.toLowerCase()
      if (name.includes('living') || name.includes('lounge') || name.includes('family')) return 'living_room'
      if (name.includes('bedroom') || name.includes('bed')) return 'bedroom'
      if (name.includes('kitchen') || name.includes('cook')) return 'kitchen'
      if (name.includes('bathroom') || name.includes('bath') || name.includes('toilet')) return 'bathroom'
      if (name.includes('dining') || name.includes('eat')) return 'dining_room'
      if (name.includes('study') || name.includes('office') || name.includes('work')) return 'study_room'
      if (name.includes('guest')) return 'guest_room'
      if (name.includes('utility') || name.includes('laundry')) return 'utility_room'
      if (name.includes('store') || name.includes('storage')) return 'store_room'
      return 'bedroom' // Default fallback
    }
    
    // Generate room configurations based on user input
    userRooms.forEach((room: { name: string; area: number }) => {
      const roomType = getRoomType(room.name)
      const roomArea = room.area || 100 // Minimum reasonable room size if not specified
      const roomDimension = Math.sqrt(roomArea)
      
      // Calculate room dimensions based on type and area
      let width = roomDimension
      let length = roomDimension
      const height = specs.room_height || 2.5
      
      // Adjust dimensions based on room type
      switch (roomType) {
        case 'living_room':
          width = roomDimension * 1.2
          length = roomDimension * 1.2
          break
        case 'kitchen':
          width = roomDimension * 0.8
          length = roomDimension * 1.2
          break
        case 'bathroom':
          width = Math.min(roomDimension, 4)
          length = Math.min(roomDimension, 4)
          break
        case 'bedroom':
          width = roomDimension
          length = roomDimension * 1.1
          break
        case 'study_room':
          width = roomDimension * 0.9
          length = roomDimension * 0.9
          break
        default:
          width = roomDimension
          length = roomDimension
      }
      
      // Position rooms in a grid layout
      if (currentX + width > maxRowWidth) {
        currentX = 0
        currentY += length + 1 // Add some spacing between rows
      }
      
      roomsConfig.push({
        name: room.name,
        room_type: roomType,
        width: width,
        length: length,
        height: height,
        area: roomArea,
        position: { x: currentX, y: currentY }
      })
      
      currentX += width + 1 // Add some spacing between rooms
    })
    
    // Calculate building dimensions based on actual room positions
    const buildingDimensions = {
      total_width: Math.max(...roomsConfig.map(r => r.position.x + r.width), 30),
      total_length: Math.max(...roomsConfig.map(r => r.position.y + r.length), 30),
      height: Math.max(...roomsConfig.map(r => r.height), 10) + 2
    }
    
    // Calculate total doors and windows
    const totalDoorsCalculated = roomsConfig.reduce((total, room) => {
      if (room.room_type === 'bedroom') return total + (specs.doors_per_bedroom || 1)
      if (room.room_type === 'living_room') return total + (specs.doors_per_living_room || 1)
      if (room.room_type === 'kitchen') return total + (specs.doors_per_kitchen || 1)
      if (room.room_type === 'bathroom') return total + (specs.doors_per_bathroom || 1)
      return total + 1
    }, 0)
    
    const totalWindowsCalculated = roomsConfig.reduce((total, room) => {
      if (room.room_type === 'bedroom') return total + (specs.windows_per_bedroom || 2)
      if (room.room_type === 'living_room') return total + (specs.windows_per_living_room || 3)
      if (room.room_type === 'kitchen') return total + (specs.windows_per_kitchen || 1)
      if (room.room_type === 'bathroom') return total + (specs.windows_per_bathroom || 1)
      return total + 1
    }, 0)
    
    // Enhanced BOQ calculation function
    const calculateEnhancedBOQ = (specsData: typeof specs, totalArea: number) => {
      interface BOQItem {
        category: string
        item: string
        quantity: number
        unit: string
        rate: number
        amount: number
      }
      
      const items: BOQItem[] = []
      
      // Quality grade multipliers
      const qualityMultipliers = {
        'basic': 1.0,
        'standard': 1.3,
        'premium': 1.8,
        'luxury': 2.5
      }
      
      // Construction type multipliers
      const constructionMultipliers = {
        'RCC': 1.0,
        'Steel': 1.4,
        'Brick': 0.8,
        'Wood': 1.2
      }
      
      const qualityMultiplier = qualityMultipliers[specsData.quality_grade as keyof typeof qualityMultipliers] || 1.3
      const constructionMultiplier = constructionMultipliers[specsData.construction_type as keyof typeof constructionMultipliers] || 1.0
      const baseMultiplier = qualityMultiplier * constructionMultiplier
      
      // 1. Foundation and Structure
      const cementBags = Math.round(totalArea * 0.8 * baseMultiplier)
      const steelKg = Math.round(totalArea * 0.6 * baseMultiplier)
      const aggregateCubicFt = Math.round(totalArea * 0.4 * baseMultiplier)
      
      items.push(
        {
          category: 'Structure',
          item: 'Cement (OPC 53 Grade)',
          quantity: cementBags,
          unit: 'bags',
          rate: specsData.quality_grade === 'luxury' ? 550 : specsData.quality_grade === 'premium' ? 480 : 400,
          amount: 0
        },
        {
          category: 'Structure',
          item: 'Steel TMT Bars',
          quantity: steelKg,
          unit: 'kg',
          rate: specsData.quality_grade === 'luxury' ? 85 : specsData.quality_grade === 'premium' ? 75 : 60,
          amount: 0
        },
        {
          category: 'Structure',
          item: 'Coarse Aggregate',
          quantity: aggregateCubicFt,
          unit: 'cubic ft',
          rate: specsData.quality_grade === 'premium' ? 180 : 150,
          amount: 0
        }
      )
      
      // 2. Masonry and Walls
      const brickCount = Math.round(totalArea * 12 * baseMultiplier)
      const sandCubicFt = Math.round(totalArea * 0.3 * baseMultiplier)
      
      items.push(
        {
          category: 'Masonry',
          item: specsData.quality_grade === 'luxury' ? 'AAC Blocks' : 'Red Clay Bricks',
          quantity: brickCount,
          unit: 'nos',
          rate: specsData.quality_grade === 'luxury' ? 15 : specsData.quality_grade === 'premium' ? 12 : 8,
          amount: 0
        },
        {
          category: 'Masonry',
          item: 'Fine Sand',
          quantity: sandCubicFt,
          unit: 'cubic ft',
          rate: 120,
          amount: 0
        }
      )
      
      // 3. Flooring based on specifications
      const flooringRate = specsData.flooring_type === 'marble' ? 2500 :
                          specsData.flooring_type === 'granite' ? 1800 :
                          specsData.flooring_type === 'tiles' ? 800 :
                          specsData.flooring_type === 'wooden' ? 1500 : 600
      
      items.push({
        category: 'Flooring',
        item: specsData.flooring_type ? 
              `${specsData.flooring_type.charAt(0).toUpperCase() + specsData.flooring_type.slice(1)} Flooring` : 
              'Ceramic Tiles',
        quantity: totalArea,
        unit: 'sqft',
        rate: flooringRate * qualityMultiplier,
        amount: 0
      })
      
      // 4. Doors and Windows calculation
      const totalDoors = (specsData.num_bedrooms * (specsData.doors_per_bedroom || 2)) +
                        (specsData.num_living_rooms * (specsData.doors_per_living_room || 1)) +
                        (specsData.num_kitchens * (specsData.doors_per_kitchen || 1)) +
                        (specsData.num_bathrooms * (specsData.doors_per_bathroom || 1)) + 1 // Main door
      
      const totalWindows = (specsData.num_bedrooms * (specsData.windows_per_bedroom || 2)) +
                          (specsData.num_living_rooms * (specsData.windows_per_living_room || 3)) +
                          (specsData.num_kitchens * (specsData.windows_per_kitchen || 2)) +
                          (specsData.num_bathrooms * (specsData.windows_per_bathroom || 1))
      
      const doorRate = specsData.main_door_type === 'wooden' ? 25000 :
                      specsData.main_door_type === 'steel' ? 15000 :
                      specsData.interior_door_type === 'wooden' ? 12000 : 8000
      
      const windowRate = specsData.window_type === 'upvc' ? 8000 :
                        specsData.window_type === 'aluminum' ? 6000 : 4000
      
      if (totalDoors > 0) {
        items.push({
          category: 'Doors & Windows',
          item: `${specsData.main_door_type || 'Standard'} Doors`,
          quantity: totalDoors,
          unit: 'nos',
          rate: doorRate * qualityMultiplier,
          amount: 0
        })
      }
      
      if (totalWindows > 0) {
        items.push({
          category: 'Doors & Windows',
          item: `${specsData.window_type || 'Standard'} Windows`,
          quantity: totalWindows,
          unit: 'nos',
          rate: windowRate * qualityMultiplier,
          amount: 0
        })
      }
      
      // 5. Electrical and Plumbing
      items.push(
        {
          category: 'Electrical',
          item: 'Electrical Fittings & Wiring',
          quantity: totalArea,
          unit: 'sqft',
          rate: specsData.quality_grade === 'luxury' ? 250 : specsData.quality_grade === 'premium' ? 180 : 120,
          amount: 0
        },
        {
          category: 'Plumbing',
          item: 'Plumbing & Sanitary Fittings',
          quantity: specsData.num_bathrooms + specsData.num_kitchens,
          unit: 'set',
          rate: specsData.quality_grade === 'luxury' ? 45000 : specsData.quality_grade === 'premium' ? 30000 : 20000,
          amount: 0
        }
      )
      
      // 6. Painting and Finishing
      const paintArea = totalArea * 3 // Walls + ceiling
      items.push({
        category: 'Finishing',
        item: specsData.quality_grade === 'luxury' ? 'Premium Paint & Texture' : 'Interior Paint',
        quantity: paintArea,
        unit: 'sqft',
        rate: specsData.quality_grade === 'luxury' ? 85 : specsData.quality_grade === 'premium' ? 65 : 45,
        amount: 0
      })
      
      // 7. Labor costs
      const laborDays = Math.round(totalArea * 0.15 * baseMultiplier)
      items.push({
        category: 'Labor',
        item: 'Skilled Construction Labor',
        quantity: laborDays,
        unit: 'days',
        rate: specsData.quality_grade === 'luxury' ? 800 : specsData.quality_grade === 'premium' ? 650 : 500,
        amount: 0
      })
      
      // Calculate amounts
      items.forEach(item => {
        item.amount = item.quantity * item.rate
      })
      
      return items
    }
    
    // Calculate enhanced BOQ items
    const enhancedBOQItems = calculateEnhancedBOQ(specs, specs.total_area)
    
    // Calculate totals from enhanced BOQ
    const materialCost = enhancedBOQItems
      .filter(item => ['Structure', 'Masonry', 'Flooring', 'Doors & Windows', 'Electrical', 'Plumbing', 'Finishing'].includes(item.category))
      .reduce((sum, item) => sum + item.amount, 0)
    
    const laborCost = enhancedBOQItems
      .filter(item => item.category === 'Labor')
      .reduce((sum, item) => sum + item.amount, 0)
    
    const overheadCost = Math.round((materialCost + laborCost) * 0.15) // 15% overhead
    
    // Add enhanced features costs
    let enhancedFeaturesCost = 0
    if (specs.enhanced_features) {
      if (specs.enhanced_features.furniture) enhancedFeaturesCost += specs.total_area * 300
      if (specs.enhanced_features.landscaping) enhancedFeaturesCost += specs.total_area * 150
      if (specs.enhanced_features.premiumMaterials) enhancedFeaturesCost += (materialCost + laborCost) * 0.2
      if (specs.enhanced_features.interiorDetails) enhancedFeaturesCost += specs.total_area * 200
      if (specs.enhanced_features.lighting) enhancedFeaturesCost += specs.total_area * 100
      if (specs.enhanced_features.textures) enhancedFeaturesCost += specs.total_area * 80
    }
    
    const totalCost = materialCost + laborCost + overheadCost + enhancedFeaturesCost
    const baseCostPerSqft = Math.round(totalCost / specs.total_area)
    
    // Generate configuration file for Blender renderer
    const blenderConfig = {
      house: {
        rooms: roomsConfig.map(room => ({
          name: room.name,
          type: room.room_type,
          dimensions: [room.width, room.length, room.height],
          location: [room.position.x, room.position.y, 0]
        }))
      }
    }
    
    // Save configuration file
    const configFileName = `boq_config_${Date.now()}.json`
    const configFilePath = path.join(process.cwd(), configFileName)
    fs.writeFileSync(configFilePath, JSON.stringify(blenderConfig, null, 2))
      console.log('🔧 Calling Blender bridge API...')

    // Call Blender bridge API to generate 3D model
    let blenderResponse = null
    let nerfResponse = null
    
    try {
      const blenderRequest = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/api/mcp/blender-bridge`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tool: 'generate_3d_model',
          arguments: {
            config_file: configFilePath,
            enhanced_features: {
              furniture: true,
              lighting: true,
              landscaping: true,
              interiorDetails: true,
              professionalMaterials: true,
              highQualityRendering: true
            },
            architectural_style: 'modern',
            quality_level: 'professional',
            render_settings: {
              resolution: '1920x1080',
              samples: 256,
              denoising: true,
              gpu_acceleration: true,
              camera_angles: ['hero', 'aerial', 'detail']
            }
          }
        })
      })
      
      if (blenderRequest.ok) {
        blenderResponse = await blenderRequest.json()
        console.log('✅ Blender bridge response:', blenderResponse)
      } else {
        const errorText = await blenderRequest.text()
        console.error('❌ Blender bridge error:', errorText)
        console.error('❌ Blender bridge status:', blenderRequest.status)
      }
    } catch (blenderError) {
      console.error('❌ Blender bridge request failed:', blenderError)
    }

    // 🧠 NEW: Generate NeRF-based 3D model for photorealistic reconstruction
    console.log('🎯 Generating NeRF 3D model from room specifications...')
    
    try {
      // Generate mock 2D views for NeRF training (in real implementation, these would be actual room photos)
      const mockRoomImages = generateMockRoomImages(roomsConfig)
      
      const nerfRequest = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/api/nerf/generate-3d`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          images: mockRoomImages,
          room_specifications: {
            room_type: 'multi_room_house',
            dimensions: {
              width: buildingDimensions.total_width,
              length: buildingDimensions.total_length,
              height: buildingDimensions.height
            }
          },
          rendering_options: {
            quality: specs.quality_grade === 'luxury' ? 'ultra' : 
                    specs.quality_grade === 'premium' ? 'high' : 'medium',
            output_format: 'obj',
            texture_resolution: specs.quality_grade === 'luxury' ? 2048 : 1024,
            novel_view_count: 8
          }
        })
      })

      if (nerfRequest.ok) {
        nerfResponse = await nerfRequest.json()
        console.log('✅ NeRF 3D generation complete:', nerfResponse)
      } else {
        const errorText = await nerfRequest.text()
        console.error('❌ NeRF generation error:', errorText)
      }
    } catch (nerfError) {
      console.error('❌ NeRF generation failed:', nerfError)
    }
    
    const response: BOQ3DResponse = {
      boq_id: `BOQ-${Date.now()}`,
      project_specs: specs,
      total_cost: totalCost,
      material_cost: materialCost,
      labor_cost: laborCost,
      items: enhancedBOQItems,
      cost_breakdown: {
        material_cost: materialCost,
        labor_cost: laborCost,
        overhead_cost: overheadCost,
        enhanced_features_cost: enhancedFeaturesCost,
        total_cost: totalCost,
        cost_per_sqft: baseCostPerSqft
      },
      room_3d_data: {
        visualization_data: {
          rooms: roomsConfig.map(room => ({
            name: room.name,
            room_type: room.room_type,
            width: room.width,
            length: room.length,
            height: room.height,
            area: room.area,
            position: { x: room.position.x, y: room.position.y, z: 0 }
          })),
          building_dimensions: buildingDimensions,
          total_doors: totalDoorsCalculated,
          total_windows: totalWindowsCalculated
        }
      },
      model_file_path: `model_${Date.now()}.obj`,
      created_at: new Date().toISOString(),
      config_file: configFilePath,
      scene_id: `scene_${Date.now()}`,
      // Add professional_3d data if Blender bridge succeeded
      ...(blenderResponse && blenderResponse.success && {
        professional_3d: {
          scene_id: blenderResponse.data.scene_id,
          quality: 'professional',
          renderer: 'blender_cycles',
          samples: 256,
          resolution: '1920x1080',
          status: 'completed',
          obj_url: blenderResponse.data.files.obj_file,
          mtl_url: blenderResponse.data.files.mtl_file,
          blend_url: blenderResponse.data.files.blend_file,
          preview_url: blenderResponse.data.files.preview_image || null,
          blender_files: {
            obj: blenderResponse.data.files.obj_file,
            mtl: blenderResponse.data.files.mtl_file,
            blend_file: blenderResponse.data.files.blend_file,
            renders: blenderResponse.data.files.preview_image ? [blenderResponse.data.files.preview_image] : []
          }
        }
      }),
      // Add NeRF 3D data if NeRF generation succeeded
      ...(nerfResponse && nerfResponse.success && {
        nerf_3d: {
          nerf_id: nerfResponse.nerf_id,
          model_files: nerfResponse.model_files,
          metadata: nerfResponse.metadata
        }
      })
    }
    
    console.log('✅ Generated BOQ response:', JSON.stringify(response, null, 2))
    console.log('🏠 Rooms config:', roomsConfig)
    console.log('🏗️ Building dimensions:', buildingDimensions)
    return NextResponse.json(response)
    
  } catch (error) {
    console.error('❌ BOQ API error:', error)
    
    // Clean up config file if it exists
    try {
      const configFileName = `boq_config_${Date.now()}.json`
      const configFilePath = path.join(process.cwd(), configFileName)
      if (fs.existsSync(configFilePath)) {
        fs.unlinkSync(configFilePath)
      }
    } catch (cleanupError) {
      console.warn('⚠️ Could not clean up config file:', cleanupError)
    }
    
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
      details: error instanceof Error ? error.stack : undefined
    }, { status: 500 })
  }
}
