// Type definitions for ConstructAI frontend components

export interface Enhanced3DProjectSpecs {
  total_area: number;
  num_bedrooms: number;
  num_living_rooms: number;
  num_kitchens: number;
  num_bathrooms: number;
  num_floors: number;
  construction_type: string;
  quality_grade: string;
  location: string;
  room_height: number;
  wall_thickness: number;
  doors_per_bedroom: number;
  doors_per_living_room: number;
  doors_per_kitchen: number;
  doors_per_bathroom: number;
  windows_per_bedroom: number;
  windows_per_living_room: number;
  windows_per_kitchen: number;
  windows_per_bathroom: number;
  main_door_type: string;
  interior_door_type: string;
  window_type: string;
  room_layout: string;
  include_balcony: boolean;
  balcony_area: number;
  num_dining_rooms: number;
  num_study_rooms: number;
  num_utility_rooms: number;
  num_guest_rooms: number;
  num_store_rooms: number;
  ceiling_type: string;
  flooring_type: string;
}

export interface BOQItem {
  item: string;
  quantity: number;
  unit: string;
  rate: number;
  amount: number;
}

export interface BlenderFiles {
  obj: string;
  mtl: string;
  blend_file: string;
  renders: string[];
}

export interface Professional3D {
  scene_id: string;
  quality: string;
  renderer: string;
  samples: number;
  resolution: string;
  obj_url?: string;
  mtl_url?: string;
  blender_files: BlenderFiles;
}

export interface RoomData {
  id?: string;
  name: string;
  room_type?: string;
  type?: string;
  width: number;
  length: number;
  height: number;
  area?: number;
  position?: {
    x: number;
    y: number;
    z?: number;
  };
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

export interface BuildingDimensions {
  total_width: number;
  total_length: number;
  height: number;
}

export interface VisualizationData {
  rooms: RoomData[];
  building_dimensions?: BuildingDimensions;
}

export interface Room3DData {
  visualization_data: VisualizationData;
}

export interface BOQResult {
  total_cost: number;
  items: BOQItem[];
  professional_3d?: Professional3D;
  room_3d_data?: Room3DData;
}

export interface EnhancedFeatures {
  furniture: boolean;
  landscaping: boolean;
  premiumMaterials: boolean;
  interiorDetails: boolean;
  lighting: boolean;
  textures: boolean;
}

// ThreeJS Viewer Props
export interface ThreeJSViewerProps {
  objUrl?: string;
  mtlUrl?: string;
  width?: number;
  height?: number;
  onModelLoad?: () => void;
  onModelError?: (error: Error) => void;
  className?: string;
}

// Simple Viewer Props
export interface SimpleViewerProps {
  rooms: RoomData[];
  buildingDimensions: BuildingDimensions;
  onRoomSelect?: (roomId: string) => void;
  className?: string;
}
