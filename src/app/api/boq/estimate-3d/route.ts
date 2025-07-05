import { NextRequest, NextResponse } from 'next/server'

interface BOQSpecs {
  building_type: string
  total_area: number
  floors: number
  rooms: number
  bathrooms: number
  flooring_type: string
  wall_finish: string
  ceiling_type: string
  electrical_fixtures: string
  plumbing_fixtures: string
  hvac_system: string
  door_window_type: string
  roofing_type: string
  exterior_finish: string
  structural_system: string
  foundation_type: string
  insulation_type: string
  security_system: string
  smart_home_features: string
  sustainability_features: string
  additional_features: string[]
}

interface BOQ3DResponse {
  boq_id: string
  project_specs: BOQSpecs
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
        position: { x: number; y: number; z: number }
      }>
    }
  }
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const specs: BOQSpecs = await request.json()
    
    // Generate mock BOQ data based on specs
    const baseCostPerSqft = 200 // Base cost per square foot
    const totalCost = specs.total_area * baseCostPerSqft
    
    // Generate room configuration based on specs
    const roomsConfig = []
    
    // Calculate room dimensions based on total area
    const avgRoomArea = specs.total_area / specs.rooms
    const roomDimension = Math.sqrt(avgRoomArea)
    
    for (let i = 0; i < specs.rooms; i++) {
      const roomTypes = ['living_room', 'bedroom', 'kitchen', 'dining_room']
      const roomType = i === 0 ? 'living_room' : roomTypes[i % roomTypes.length]
      
      roomsConfig.push({
        name: `${roomType}_${i + 1}`,
        room_type: roomType,
        width: roomDimension,
        length: roomDimension,
        height: 10,
        position: { x: i * roomDimension, y: 0, z: 0 }
      })
    }
    
    // Add bathrooms
    for (let i = 0; i < specs.bathrooms; i++) {
      roomsConfig.push({
        name: `bathroom_${i + 1}`,
        room_type: 'bathroom',
        width: 8,
        length: 8,
        height: 10,
        position: { x: i * 8, y: roomDimension, z: 0 }
      })
    }
    
    // Generate sample BOQ items
    const sampleItems = [
      {
        category: 'Materials',
        item: 'Cement',
        quantity: specs.total_area * 0.02,
        unit: 'bags',
        rate: 400,
        amount: specs.total_area * 0.02 * 400
      },
      {
        category: 'Materials',
        item: 'Steel',
        quantity: specs.total_area * 0.05,
        unit: 'kg',
        rate: 60,
        amount: specs.total_area * 0.05 * 60
      },
      {
        category: 'Materials',
        item: 'Bricks',
        quantity: specs.total_area * 0.5,
        unit: 'nos',
        rate: 8,
        amount: specs.total_area * 0.5 * 8
      },
      {
        category: 'Labor',
        item: 'Construction Labor',
        quantity: specs.total_area * 0.1,
        unit: 'days',
        rate: 500,
        amount: specs.total_area * 0.1 * 500
      }
    ]
    
    const response: BOQ3DResponse = {
      boq_id: `BOQ-${Date.now()}`,
      project_specs: specs,
      total_cost: totalCost,
      material_cost: totalCost * 0.4,
      labor_cost: totalCost * 0.3,
      items: sampleItems,
      cost_breakdown: {
        material_cost: totalCost * 0.4,
        labor_cost: totalCost * 0.3,
        overhead_cost: totalCost * 0.15,
        total_cost: totalCost,
        cost_per_sqft: baseCostPerSqft
      },
      room_3d_data: {
        visualization_data: {
          rooms: roomsConfig
        }
      }
    }
    
    return NextResponse.json(response)
    
  } catch (error) {
    console.error('❌ BOQ API error:', error)
    return NextResponse.json({
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}
