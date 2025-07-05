from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import uuid
from datetime import datetime
import math
import json
import os
import logging

# Import dynamic pricing system (optional)
try:
    from core.pricing import DynamicPricingSystem, get_dynamic_material_rates
    from core.database import get_sync_db
    DYNAMIC_PRICING_AVAILABLE = True
except ImportError:
    DYNAMIC_PRICING_AVAILABLE = False
    DynamicPricingSystem = None
    get_dynamic_material_rates = None
    get_sync_db = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Static material rates for fallback when dynamic pricing is unavailable
STATIC_MATERIAL_RATES = {
    "cement": {"rate": 420, "unit": "bag", "weight_kg": 50},
    "steel": {"rate": 68000, "unit": "ton", "weight_kg": 1000},
    "bricks": {"rate": 9.5, "unit": "piece", "weight_kg": 3},
    "sand": {"rate": 1800, "unit": "cft", "weight_kg": 35},
    "aggregate": {"rate": 2200, "unit": "cft", "weight_kg": 40},
    "concrete_m25": {"rate": 6200, "unit": "cum", "weight_kg": 2400},
    "rcc_slab": {"rate": 6800, "unit": "sqm", "weight_kg": 375},
    "brick_wall": {"rate": 480, "unit": "sqm", "weight_kg": 400},
    "plaster": {"rate": 195, "unit": "sqm", "weight_kg": 25},
    "tiles": {"rate": 850, "unit": "sqm", "weight_kg": 20},
    "paint": {"rate": 140, "unit": "sqm", "weight_kg": 2},
    "electrical": {"rate": 16500, "unit": "room", "weight_kg": 50},
    "plumbing": {"rate": 13500, "unit": "room", "weight_kg": 80},
    "door_standard": {"rate": 9200, "unit": "piece", "weight_kg": 45},
    "door_premium": {"rate": 18000, "unit": "piece", "weight_kg": 50},
    "window_standard": {"rate": 5500, "unit": "piece", "weight_kg": 25},
    "window_premium": {"rate": 8800, "unit": "piece", "weight_kg": 30},
    "door_frame": {"rate": 2800, "unit": "piece", "weight_kg": 15},
    "window_frame": {"rate": 2000, "unit": "piece", "weight_kg": 10}
}

def get_current_material_rates() -> Dict[str, Dict[str, Any]]:
    """Get current material rates - dynamic if available, static as fallback"""
    if not DYNAMIC_PRICING_AVAILABLE:
        logger.info("Dynamic pricing not available, using static rates")
        return STATIC_MATERIAL_RATES
        
    try:
        # Try to get dynamic rates if database is available
        db = get_sync_db()
        if db:
            pricing_system = DynamicPricingSystem(db)
            dynamic_rates = get_dynamic_material_rates(pricing_system)
            logger.info("Using dynamic pricing system for BOQ calculation")
            return dynamic_rates
    except Exception as e:
        logger.warning(f"Dynamic pricing unavailable, falling back to static rates: {str(e)}")
    
    logger.info("Using static pricing for BOQ calculation")
    return STATIC_MATERIAL_RATES

# Labor rates (per unit in INR)
LABOR_RATES = {
    "mason": {"rate": 800, "unit": "day"},
    "helper": {"rate": 500, "unit": "day"},
    "electrician": {"rate": 1000, "unit": "day"},
    "plumber": {"rate": 900, "unit": "day"},
    "painter": {"rate": 600, "unit": "day"},
    "carpenter": {"rate": 850, "unit": "day"}
}

# Legacy support - keep original ProjectSpecs for backward compatibility
class ProjectSpecs(BaseModel):
    total_area: float  # in sqft
    num_rooms: int
    num_bathrooms: int
    num_floors: int = 1
    construction_type: str = "residential"  # residential, commercial, industrial
    quality_grade: str = "standard"  # basic, standard, premium
    location: str = "urban"  # urban, suburban, rural

class BOQResponse(BaseModel):
    boq_id: str
    project_specs: Dict[str, Any]
    total_cost: float
    material_cost: float
    labor_cost: float
    items: List[Dict[str, Any]]
    cost_breakdown: Dict[str, float]
    created_at: str

# Enhanced project specifications with 3D details
class Enhanced3DProjectSpecs(BaseModel):
    # Basic specs
    total_area: float  # in sqft
    num_bedrooms: int
    num_living_rooms: int
    num_kitchens: int
    num_bathrooms: int
    num_floors: int = 1
    construction_type: str = "residential"
    quality_grade: str = "standard"
    location: str = "urban"
    
    # 3D Room specifications
    room_height: float = 10  # in feet
    wall_thickness: float = 0.5  # in feet
    
    # Doors and Windows per room type
    doors_per_bedroom: int = 1
    doors_per_living_room: int = 1
    doors_per_kitchen: int = 1
    doors_per_bathroom: int = 1
    doors_per_dining_room: int = 1
    doors_per_study_room: int = 1
    doors_per_guest_room: int = 1
    doors_per_utility_room: int = 1
    doors_per_store_room: int = 1
    windows_per_bedroom: int = 2
    windows_per_living_room: int = 3
    windows_per_kitchen: int = 1
    windows_per_bathroom: int = 1
    windows_per_dining_room: int = 2
    windows_per_study_room: int = 2
    windows_per_guest_room: int = 2
    windows_per_utility_room: int = 1
    windows_per_store_room: int = 0
    main_door_type: str = "premium"  # standard, premium
    interior_door_type: str = "standard"
    window_type: str = "standard"
    
    # Room layout preferences
    room_layout: str = "rectangular"  # rectangular, square, custom
    include_balcony: bool = False
    balcony_area: float = 0  # in sqft
    
    # Additional room types
    num_dining_rooms: int = 0
    num_study_rooms: int = 0
    num_utility_rooms: int = 0
    num_guest_rooms: int = 0
    num_store_rooms: int = 0
    
    # Additional features
    ceiling_type: str = "false"  # false, pop, wooden
    flooring_type: str = "tiles"  # tiles, marble, wood, vitrified

class Room3DSpec(BaseModel):
    name: str
    width: float  # in feet
    length: float  # in feet
    height: float  # in feet
    doors: List[Dict[str, Any]] = []
    windows: List[Dict[str, Any]] = []
    room_type: str = "bedroom"  # bedroom, bathroom, kitchen, living

class BOQ3DResponse(BaseModel):
    boq_id: str
    project_specs: Enhanced3DProjectSpecs
    total_cost: float
    material_cost: float
    labor_cost: float
    items: List[Dict[str, Any]]
    cost_breakdown: Dict[str, float]
    room_3d_data: Dict[str, Any]  # 3D room geometry and materials
    model_file_path: str  # Path to generated 3D model
    created_at: str

def generate_3d_room_layout(specs: Enhanced3DProjectSpecs) -> Dict[str, Any]:
    """Generate realistic 3D room layout based on specifications"""
    
    # Calculate total number of rooms for area allocation
    total_rooms = (specs.num_bedrooms + specs.num_living_rooms + specs.num_kitchens + 
                   specs.num_bathrooms + specs.num_dining_rooms + specs.num_study_rooms + 
                   specs.num_guest_rooms + specs.num_utility_rooms + specs.num_store_rooms)
    
    # Realistic area allocation for residential buildings
    if specs.construction_type == "residential":
        if total_rooms <= 4:  # Small apartment
            area_allocation = {
                "bedroom": 0.25,      # 25% per bedroom
                "living_room": 0.30,  # 30% per living room  
                "kitchen": 0.15,      # 15% per kitchen
                "bathroom": 0.12,     # 12% per bathroom
                "dining_room": 0.18,  # 18% per dining room
                "study_room": 0.15,   # 15% per study room
                "guest_room": 0.20,   # 20% per guest room
                "utility_room": 0.10, # 10% per utility room
                "store_room": 0.08,   # 8% per store room
                "circulation": 0.15   # 15% for corridors, balcony, etc.
            }
        elif total_rooms <= 8:  # Medium house
            area_allocation = {
                "bedroom": 0.20,      # 20% per bedroom
                "living_room": 0.25,  # 25% per living room
                "kitchen": 0.12,      # 12% per kitchen
                "bathroom": 0.08,     # 8% per bathroom
                "dining_room": 0.15,  # 15% per dining room
                "study_room": 0.12,   # 12% per study room
                "guest_room": 0.18,   # 18% per guest room
                "utility_room": 0.08, # 8% per utility room
                "store_room": 0.06,   # 6% per store room
                "circulation": 0.12   # 12% for corridors, balcony, etc.
            }
        else:  # Large house
            area_allocation = {
                "bedroom": 0.15,      # 15% per bedroom
                "living_room": 0.20,  # 20% per living room
                "kitchen": 0.08,      # 8% per kitchen
                "bathroom": 0.05,     # 5% per bathroom
                "dining_room": 0.12,  # 12% per dining room
                "study_room": 0.10,   # 10% per study room
                "guest_room": 0.15,   # 15% per guest room
                "utility_room": 0.06, # 6% per utility room
                "store_room": 0.04,   # 4% per store room
                "circulation": 0.10   # 10% for corridors, balcony, etc.
            }
    else:  # Commercial
        area_allocation = {
            "office": 0.70,
            "meeting_room": 0.15,
            "bathroom": 0.05,
            "circulation": 0.10
        }
    
    rooms = []
    total_doors = 0
    total_windows = 0
    
    # Calculate realistic building dimensions
    building_ratio = 1.4  # Length to width ratio
    total_area_sqft = specs.total_area
    building_width = math.sqrt(total_area_sqft / building_ratio)
    building_length = total_area_sqft / building_width
    
    # Generate rooms based on user specifications
    current_x = 0
    current_y = 0
    
    # Helper function to generate room
    def generate_room(room_type: str, count: int, doors_per_room: int, windows_per_room: int, area_pct: float):
        nonlocal current_x, current_y, total_doors, total_windows
        
        for i in range(count):
            # Calculate room area and dimensions
            room_area = total_area_sqft * area_pct
            
            # Standard room dimensions based on type
            if room_type == "bedroom":
                base_width = 12 if i == 0 else 10  # Master bedroom larger
                room_name = "Master Bedroom" if i == 0 else f"Bedroom {i+1}"
            elif room_type == "living_room":
                base_width = 16
                room_name = "Living Room" if count == 1 else f"Living Room {i+1}"
            elif room_type == "kitchen":
                base_width = 8
                room_name = "Kitchen" if count == 1 else f"Kitchen {i+1}"
            elif room_type == "bathroom":
                base_width = 6
                room_name = "Master Bathroom" if i == 0 else f"Bathroom {i+1}"
            elif room_type == "dining_room":
                base_width = 12
                room_name = "Dining Room" if count == 1 else f"Dining Room {i+1}"
            elif room_type == "study_room":
                base_width = 10
                room_name = "Study Room" if count == 1 else f"Study Room {i+1}"
            elif room_type == "guest_room":
                base_width = 10
                room_name = "Guest Room" if count == 1 else f"Guest Room {i+1}"
            elif room_type == "utility_room":
                base_width = 6
                room_name = "Utility Room" if count == 1 else f"Utility Room {i+1}"
            elif room_type == "store_room":
                base_width = 6
                room_name = "Store Room" if count == 1 else f"Store Room {i+1}"
            else:
                base_width = 10
                room_name = f"{room_type.title()} {i+1}"
            
            room_length = room_area / base_width
            
            # Generate doors
            doors = []
            for j in range(doors_per_room):
                door_type = specs.main_door_type if (room_type == "living_room" and j == 0) else specs.interior_door_type
                door_width = 4 if door_type == "premium" else 3
                door_width = 2.5 if room_type == "bathroom" else door_width
                
                doors.append({
                    "type": door_type,
                    "width": door_width,
                    "height": 7 if room_type == "bathroom" else 8,
                    "position": {"wall": "front", "offset": base_width / 2 + j * 2}
                })
            
            # Generate windows
            windows = []
            for j in range(windows_per_room):
                window_width = 4 if room_type in ["living_room", "bedroom"] else 3
                window_width = 2 if room_type == "bathroom" else window_width
                
                windows.append({
                    "type": specs.window_type,
                    "width": window_width,
                    "height": 4 if room_type != "bathroom" else 2,
                    "position": {"wall": "side" if j % 2 == 0 else "back", "offset": 2 + j * 4}
                })
            
            total_doors += len(doors)
            total_windows += len(windows)
            
            # Add room to list
            rooms.append({
                "name": room_name,
                "width": base_width,
                "length": room_length,
                "height": specs.room_height,
                "doors": doors,
                "windows": windows,
                "room_type": room_type,
                "area": room_area,
                "position": {"x": current_x, "y": current_y}
            })
            
            # Update position for next room
            current_x += base_width
            if current_x > building_width:
                current_x = 0
                current_y += room_length
    
    # Generate all room types based on user specifications
    if specs.construction_type == "residential":
        # Generate bedrooms
        if specs.num_bedrooms > 0:
            generate_room("bedroom", specs.num_bedrooms, specs.doors_per_bedroom, specs.windows_per_bedroom, area_allocation["bedroom"])
        
        # Generate living rooms
        if specs.num_living_rooms > 0:
            generate_room("living_room", specs.num_living_rooms, specs.doors_per_living_room, specs.windows_per_living_room, area_allocation["living_room"])
        
        # Generate kitchens
        if specs.num_kitchens > 0:
            generate_room("kitchen", specs.num_kitchens, specs.doors_per_kitchen, specs.windows_per_kitchen, area_allocation["kitchen"])
        
        # Generate bathrooms
        if specs.num_bathrooms > 0:
            generate_room("bathroom", specs.num_bathrooms, specs.doors_per_bathroom, specs.windows_per_bathroom, area_allocation["bathroom"])
        
        # Generate dining rooms
        if specs.num_dining_rooms > 0:
            generate_room("dining_room", specs.num_dining_rooms, specs.doors_per_dining_room, specs.windows_per_dining_room, area_allocation["dining_room"])
        
        # Generate study rooms
        if specs.num_study_rooms > 0:
            generate_room("study_room", specs.num_study_rooms, specs.doors_per_study_room, specs.windows_per_study_room, area_allocation["study_room"])
        
        # Generate guest rooms
        if specs.num_guest_rooms > 0:
            generate_room("guest_room", specs.num_guest_rooms, specs.doors_per_guest_room, specs.windows_per_guest_room, area_allocation["guest_room"])
        
        # Generate utility rooms
        if specs.num_utility_rooms > 0:
            generate_room("utility_room", specs.num_utility_rooms, specs.doors_per_utility_room, specs.windows_per_utility_room, area_allocation["utility_room"])
        
        # Generate store rooms
        if specs.num_store_rooms > 0:
            generate_room("store_room", specs.num_store_rooms, specs.doors_per_store_room, specs.windows_per_store_room, area_allocation["store_room"])
    
    # Add balcony if specified
    if specs.include_balcony and specs.balcony_area > 0:
        balcony_width = min(building_width * 0.8, 12)  # Max 12 feet wide
        balcony_length = specs.balcony_area / balcony_width
        
        rooms.append({
            "name": "Balcony",
            "width": balcony_width,
            "length": balcony_length,
            "height": specs.room_height,
            "doors": [{
                "type": "glass_door",
                "width": 6, "height": 8,
                "position": {"wall": "back", "offset": balcony_width / 2}
            }],
            "windows": [],  # Balcony is open
            "room_type": "balcony",
            "area": specs.balcony_area,
            "position": {"x": 0, "y": -balcony_length}
        })
        total_doors += 1
    
    # Total doors and windows are already calculated in the generate_room function
    
    return {
        "rooms": rooms,
        "total_doors": total_doors,
        "total_windows": total_windows,
        "building_dimensions": {
            "total_width": building_width,
            "total_length": building_length,
            "height": specs.room_height * specs.num_floors
        },
        "room_breakdown": {
            "bedrooms": specs.num_bedrooms,
            "living_rooms": specs.num_living_rooms,
            "kitchens": specs.num_kitchens,
            "bathrooms": specs.num_bathrooms,
            "dining_rooms": specs.num_dining_rooms,
            "study_rooms": specs.num_study_rooms,
            "guest_rooms": specs.num_guest_rooms,
            "utility_rooms": specs.num_utility_rooms,
            "store_rooms": specs.num_store_rooms,
            "total_spaces": len(rooms)
        }
    }

def generate_3d_model_file(room_layout: Dict[str, Any], specs: Enhanced3DProjectSpecs) -> str:
    """Generate detailed 3D OBJ model file with proper interior geometry"""
    
    model_id = str(uuid.uuid4())
    obj_filename = f"{model_id}.obj"
    mtl_filename = f"{model_id}.mtl"
    
    obj_file_path = f"generated_models/{obj_filename}"
    mtl_file_path = f"generated_models/{mtl_filename}"
    
    # Create directories if they don't exist
    os.makedirs("generated_models", exist_ok=True)
    
    # Generate MTL file (Material Template Library)
    mtl_content = [
        "# Material file for 3D room model\n",
        "# Generated by ConstructAI\n\n",
        "newmtl floor_material\n",
        "Ka 0.8 0.7 0.6\n",  # Ambient color (light brown)
        "Kd 0.9 0.8 0.7\n",  # Diffuse color (beige)
        "Ks 0.1 0.1 0.1\n",  # Specular color
        "Ns 10.0\n\n",       # Specular exponent
        
        "newmtl wall_material\n",
        "Ka 0.9 0.9 0.9\n",   # Light gray
        "Kd 0.95 0.95 0.95\n",
        "Ks 0.1 0.1 0.1\n",
        "Ns 5.0\n\n",
        
        "newmtl door_material\n",
        "Ka 0.6 0.4 0.2\n",   # Brown
        "Kd 0.8 0.5 0.3\n",
        "Ks 0.2 0.2 0.2\n",
        "Ns 20.0\n\n",
        
        "newmtl window_material\n",
        "Ka 0.7 0.9 1.0\n",   # Light blue (glass)
        "Kd 0.8 0.95 1.0\n",
        "Ks 0.9 0.9 0.9\n",
        "Ns 100.0\n\n",
        
        "newmtl furniture_material\n",
        "Ka 0.5 0.3 0.2\n",   # Dark brown
        "Kd 0.7 0.5 0.4\n",
        "Ks 0.3 0.3 0.3\n",
        "Ns 15.0\n\n",
        
        "newmtl fixture_material\n",
        "Ka 0.9 0.9 0.9\n",   # White
        "Kd 0.95 0.95 0.95\n",
        "Ks 0.5 0.5 0.5\n",
        "Ns 50.0\n\n"
    ]
    
    with open(mtl_file_path, 'w') as f:
        f.writelines(mtl_content)
    
    # Generate OBJ file with proper room geometry
    obj_content = [
        "# 3D Room Model with Interior Details\n",
        f"# Generated by ConstructAI for {specs.construction_type} project\n",
        f"# Total area: {specs.total_area} sqft\n",
        f"# Bedrooms: {specs.num_bedrooms}, Bathrooms: {specs.num_bathrooms}\n",
        f"mtllib {mtl_filename}\n\n"
    ]
    
    vertex_count = 0
    wall_thickness = 0.5  # Wall thickness in feet
    
    def add_box(obj_content, vertex_count, x, y, z, width, depth, height, material_name):
        """Helper function to add a box (furniture/fixture) to OBJ"""
        obj_content.append(f"# Box: {material_name}\n")
        obj_content.append(f"usemtl {material_name}\n")
        
        # 8 vertices of a box
        vertices = [
            [x, y, z],                      # 0: bottom-front-left
            [x + width, y, z],              # 1: bottom-front-right
            [x + width, y + depth, z],      # 2: bottom-back-right
            [x, y + depth, z],              # 3: bottom-back-left
            [x, y, z + height],             # 4: top-front-left
            [x + width, y, z + height],     # 5: top-front-right
            [x + width, y + depth, z + height], # 6: top-back-right
            [x, y + depth, z + height]      # 7: top-back-left
        ]
        
        for vertex in vertices:
            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        
        base_idx = vertex_count + 1
        
        # 6 faces of the box
        faces = [
            [base_idx, base_idx+1, base_idx+2, base_idx+3],      # Bottom
            [base_idx+7, base_idx+6, base_idx+5, base_idx+4],    # Top
            [base_idx, base_idx+4, base_idx+5, base_idx+1],      # Front
            [base_idx+2, base_idx+6, base_idx+7, base_idx+3],    # Back
            [base_idx+1, base_idx+5, base_idx+6, base_idx+2],    # Right
            [base_idx+3, base_idx+7, base_idx+4, base_idx]       # Left
        ]
        
        for face in faces:
            obj_content.append(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")
        
        return vertex_count + 8
    
    def add_wall_with_opening(obj_content, vertex_count, start_x, start_y, end_x, end_y, height, opening_start, opening_width, opening_height, opening_sill=0):
        """Add a wall with door/window opening"""
        obj_content.append("usemtl wall_material\n")
        
        wall_length = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5
        wall_direction_x = (end_x - start_x) / wall_length
        wall_direction_y = (end_y - start_y) / wall_length
        
        current_vertex_count = vertex_count
        
        # Wall segment before opening
        if opening_start > 0:
            seg_end_x = start_x + wall_direction_x * opening_start
            seg_end_y = start_y + wall_direction_y * opening_start
            
            vertices = [
                [start_x, start_y, 0],
                [seg_end_x, seg_end_y, 0],
                [seg_end_x, seg_end_y, height],
                [start_x, start_y, height]
            ]
            
            for vertex in vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = current_vertex_count + 1
            obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
            current_vertex_count += 4
        
        # Wall segment above opening (lintel)
        if opening_height < height:
            lintel_start_x = start_x + wall_direction_x * opening_start
            lintel_start_y = start_y + wall_direction_y * opening_start
            lintel_end_x = start_x + wall_direction_x * (opening_start + opening_width)
            lintel_end_y = start_y + wall_direction_y * (opening_start + opening_width)
            
            vertices = [
                [lintel_start_x, lintel_start_y, opening_height + opening_sill],
                [lintel_end_x, lintel_end_y, opening_height + opening_sill],
                [lintel_end_x, lintel_end_y, height],
                [lintel_start_x, lintel_start_y, height]
            ]
            
            for vertex in vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = current_vertex_count + 1
            obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
            current_vertex_count += 4
        
        # Wall segments beside opening (sill for windows)
        if opening_sill > 0:
            sill_start_x = start_x + wall_direction_x * opening_start
            sill_start_y = start_y + wall_direction_y * opening_start
            sill_end_x = start_x + wall_direction_x * (opening_start + opening_width)
            sill_end_y = start_y + wall_direction_y * (opening_start + opening_width)
            
            vertices = [
                [sill_start_x, sill_start_y, 0],
                [sill_end_x, sill_end_y, 0],
                [sill_end_x, sill_end_y, opening_sill],
                [sill_start_x, sill_start_y, opening_sill]
            ]
            
            for vertex in vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = current_vertex_count + 1
            obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
            current_vertex_count += 4
        
        # Wall segment after opening
        opening_end = opening_start + opening_width
        if opening_end < wall_length:
            seg_start_x = start_x + wall_direction_x * opening_end
            seg_start_y = start_y + wall_direction_y * opening_end
            
            vertices = [
                [seg_start_x, seg_start_y, 0],
                [end_x, end_y, 0],
                [end_x, end_y, height],
                [seg_start_x, seg_start_y, height]
            ]
            
            for vertex in vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = current_vertex_count + 1
            obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
            current_vertex_count += 4
        
        return current_vertex_count
    
    # Generate each room with proper geometry
    current_x_offset = 0
    current_y_offset = 0
    
    for room_idx, room in enumerate(room_layout["rooms"]):
        obj_content.append(f"# ======= ROOM: {room['name']} =======\n")
        obj_content.append(f"# Area: {room['area']:.1f} sqft\n\n")
        
        # Room dimensions and position
        width = room["width"]
        length = room["length"] 
        height = room["height"]
        
        # Use realistic room positioning from layout
        x_offset = room.get("position", {}).get("x", current_x_offset)
        y_offset = room.get("position", {}).get("y", current_y_offset)
        
        # Update position for next room (fallback if no position specified)
        if "position" not in room:
            if room_idx % 2 == 0:  # Even rooms go to the right
                current_x_offset += width + 2  # 2 feet gap between rooms
            else:  # Odd rooms go down and reset x
                current_x_offset = 0
                current_y_offset += length + 2
        
        # === FLOOR ===
        obj_content.append(f"# Floor for {room['name']}\n")
        obj_content.append("usemtl floor_material\n")
        
        floor_vertices = [
            [x_offset, y_offset, 0],
            [x_offset + width, y_offset, 0],
            [x_offset + width, y_offset + length, 0],
            [x_offset, y_offset + length, 0]
        ]
        
        for vertex in floor_vertices:
            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        
        base_idx = vertex_count + 1
        obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
        vertex_count += 4
        
        # === CEILING ===
        obj_content.append(f"# Ceiling for {room['name']}\n")
        obj_content.append("usemtl wall_material\n")
        
        ceiling_vertices = [
            [x_offset, y_offset, height],
            [x_offset + width, y_offset, height],
            [x_offset + width, y_offset + length, height],
            [x_offset, y_offset + length, height]
        ]
        
        for vertex in ceiling_vertices:
            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        
        base_idx = vertex_count + 1
        obj_content.append(f"f {base_idx+3} {base_idx+2} {base_idx+1} {base_idx}\n")  # Reverse for correct normal
        vertex_count += 4
        
        # === WALLS WITH OPENINGS ===
        obj_content.append(f"# Walls with openings for {room['name']}\n")
        
        # Define walls
        walls = [
            {"name": "front", "start": [x_offset, y_offset], "end": [x_offset + width, y_offset]},
            {"name": "right", "start": [x_offset + width, y_offset], "end": [x_offset + width, y_offset + length]},
            {"name": "back", "start": [x_offset + width, y_offset + length], "end": [x_offset, y_offset + length]},
            {"name": "left", "start": [x_offset, y_offset + length], "end": [x_offset, y_offset]}
        ]
        
        for wall in walls:
            wall_name = wall["name"]
            start = wall["start"]
            end = wall["end"]
            
            # Find doors and windows on this wall
            doors_on_wall = [d for d in room["doors"] if d["position"]["wall"] == wall_name]
            windows_on_wall = [w for w in room["windows"] if w["position"]["wall"] == wall_name]
            
            obj_content.append(f"# {wall_name.title()} wall\n")
            
            if not doors_on_wall and not windows_on_wall:
                # Solid wall
                obj_content.append("usemtl wall_material\n")
                wall_vertices = [
                    start + [0],
                    end + [0],
                    end + [height],
                    start + [height]
                ]
                
                for vertex in wall_vertices:
                    obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
                
                base_idx = vertex_count + 1
                obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
                vertex_count += 4
            else:
                # Wall with openings
                for door in doors_on_wall:
                    vertex_count = add_wall_with_opening(
                        obj_content, vertex_count,
                        start[0], start[1], end[0], end[1], height,
                        door["position"]["offset"], door["width"], door["height"], 0
                    )
                    
                    # Add door frame (simplified)
                    obj_content.append("# Door frame\n")
                    door_x = start[0] + (end[0] - start[0]) * (door["position"]["offset"] / width)
                    door_y = start[1] + (end[1] - start[1]) * (door["position"]["offset"] / width)
                    vertex_count = add_box(obj_content, vertex_count, door_x - 0.1, door_y - 0.1, 0, door["width"] + 0.2, 0.2, door["height"], "door_material")
                
                for window in windows_on_wall:
                    vertex_count = add_wall_with_opening(
                        obj_content, vertex_count,
                        start[0], start[1], end[0], end[1], height,
                        window["position"]["offset"], window["width"], window["height"], 3
                    )
                    
                    # Add window frame (simplified)
                    obj_content.append("# Window frame\n")
                    window_x = start[0] + (end[0] - start[0]) * (window["position"]["offset"] / width)
                    window_y = start[1] + (end[1] - start[1]) * (window["position"]["offset"] / width)
                    vertex_count = add_box(obj_content, vertex_count, window_x - 0.1, window_y - 0.1, 3, window["width"] + 0.2, 0.2, window["height"], "window_material")
        
        # === INTERIOR FURNITURE ===
        if room["room_type"] == "bathroom":
            obj_content.append(f"# Bathroom fixtures for {room['name']}\n")
            
            # Toilet
            vertex_count = add_box(obj_content, vertex_count, x_offset + 1, y_offset + 1, 0, 1.5, 2, 1.5, "fixture_material")
            
            # Sink/vanity
            vertex_count = add_box(obj_content, vertex_count, x_offset + width - 2.5, y_offset + 1, 0, 2, 1.5, 2.5, "fixture_material")
            
            # Shower area (if space allows)
            if width > 6 and length > 6:
                # Shower base
                vertex_count = add_box(obj_content, vertex_count, x_offset + 1, y_offset + length - 3, 0, 3, 3, 0.1, "floor_material")
                # Shower walls (3 sides)
                vertex_count = add_box(obj_content, vertex_count, x_offset + 1, y_offset + length - 3, 0, 0.1, 3, 6, "fixture_material")  # Side wall
                vertex_count = add_box(obj_content, vertex_count, x_offset + 3.9, y_offset + length - 3, 0, 0.1, 3, 6, "fixture_material")  # Other side
                vertex_count = add_box(obj_content, vertex_count, x_offset + 1, y_offset + length - 3, 0, 3, 0.1, 6, "fixture_material")  # Back wall
        
        elif room["room_type"] == "bedroom":
            obj_content.append(f"# Bedroom furniture for {room['name']}\n")
            
            # Bed (centered)
            bed_x = x_offset + width/2 - 3
            bed_y = y_offset + length/2 - 2
            vertex_count = add_box(obj_content, vertex_count, bed_x, bed_y, 0, 6, 4, 1.5, "furniture_material")
            
            # Wardrobe (along one wall)
            if width > 8:
                vertex_count = add_box(obj_content, vertex_count, x_offset + 0.5, y_offset + 0.5, 0, 2, 6, 7, "furniture_material")
            
            # Side table
            vertex_count = add_box(obj_content, vertex_count, bed_x + 6.5, bed_y + 1, 0, 1.5, 1.5, 1.5, "furniture_material")
            
            # Study table (if space allows)
            if width > 10:
                vertex_count = add_box(obj_content, vertex_count, x_offset + width - 4, y_offset + 0.5, 0, 3, 2, 2.5, "furniture_material")
                # Chair
                vertex_count = add_box(obj_content, vertex_count, x_offset + width - 2.5, y_offset + 2.5, 0, 1.5, 1.5, 3, "furniture_material")
    
    # Write OBJ file
    with open(obj_file_path, 'w') as f:
        f.writelines(obj_content)
    
    print(f"✅ Generated detailed 3D model with interior: {obj_filename}")
    print(f"   - Model contains {vertex_count} vertices")
    print(f"   - Includes walls, doors, windows, and furniture")
    print(f"   - Material file: {mtl_filename}")
    return obj_filename
    """Generate detailed OBJ file for the 3D room model with interior details"""
    
    model_id = str(uuid.uuid4())
    model_filename = f"boq_room_{model_id}.obj"
    model_path = f"generated_models/{model_filename}"
    
    vertices = []
    faces = []
    vertex_count = 0
    
    # Generate detailed OBJ content with interior
    obj_content = ["# ConstructAI Generated Detailed Room Model\n"]
    obj_content.append(f"# BOQ Project: {specs.construction_type} - {specs.total_area} sqft\n")
    obj_content.append(f"# Generated on: {datetime.now().isoformat()}\n")
    obj_content.append(f"# Bedrooms: {specs.num_bedrooms}, Bathrooms: {specs.num_bathrooms}\n")
    obj_content.append(f"# Quality: {specs.quality_grade}, Doors: {room_layout['total_doors']}, Windows: {room_layout['total_windows']}\n\n")
    
    # Material definitions
    obj_content.append("# Material definitions\n")
    obj_content.append("mtllib room_materials.mtl\n\n")
    
    current_x_offset = 0
    current_y_offset = 0
    
    for room_idx, room in enumerate(room_layout["rooms"]):
        obj_content.append(f"# === {room['name']} ===\n")
        obj_content.append(f"g {room['name'].replace(' ', '_')}\n")
        
        width = room["width"]
        length = room["length"] 
        height = room["height"]
        wall_thickness = specs.wall_thickness
        
        # Room positioning (arrange rooms side by side)
        x_offset = current_x_offset
        y_offset = current_y_offset
        
        # Update offset for next room
        if room_idx % 2 == 0:  # Even rooms go to the right
            current_x_offset += width + 2  # 2 feet gap between rooms
        else:  # Odd rooms go down and reset x
            current_x_offset = 0
            current_y_offset += length + 2
        
        # === FLOOR ===
        obj_content.append(f"# Floor for {room['name']}\n")
        obj_content.append("usemtl floor_material\n")
        
        floor_vertices = [
            [x_offset, y_offset, 0],
            [x_offset + width, y_offset, 0],
            [x_offset + width, y_offset + length, 0],
            [x_offset, y_offset + length, 0]
        ]
        
        for vertex in floor_vertices:
            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        
        # Floor face
        base_idx = vertex_count + 1
        obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
        vertex_count += 4
        
        # === CEILING ===
        obj_content.append(f"# Ceiling for {room['name']}\n")
        obj_content.append("usemtl ceiling_material\n")
        
        ceiling_vertices = [
            [x_offset, y_offset, height],
            [x_offset + width, y_offset, height],
            [x_offset + width, y_offset + length, height],
            [x_offset, y_offset + length, height]
        ]
        
        for vertex in ceiling_vertices:
            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        
        # Ceiling face
        base_idx = vertex_count + 1
        obj_content.append(f"f {base_idx+3} {base_idx+2} {base_idx+1} {base_idx}\n")  # Reversed for correct normal
        vertex_count += 4
        
        # === WALLS ===
        obj_content.append(f"# Walls for {room['name']}\n")
        obj_content.append("usemtl wall_material\n")
        
        # Wall coordinates
        walls_info = [
            {"name": "front", "start": [x_offset, y_offset], "end": [x_offset + width, y_offset]},
            {"name": "right", "start": [x_offset + width, y_offset], "end": [x_offset + width, y_offset + length]},
            {"name": "back", "start": [x_offset + width, y_offset + length], "end": [x_offset, y_offset + length]},
            {"name": "left", "start": [x_offset, y_offset + length], "end": [x_offset, y_offset]}
        ]
        
        for wall_info in walls_info:
            wall_name = wall_info["name"]
            start = wall_info["start"]
            end = wall_info["end"]
            
            # Check if this wall has doors or windows
            doors_on_wall = [d for d in room["doors"] if d["position"]["wall"] == wall_name]
            windows_on_wall = [w for w in room["windows"] if w["position"]["wall"] == wall_name]
            
            obj_content.append(f"# {wall_name.title()} wall\n")
            
            if not doors_on_wall and not windows_on_wall:
                # Solid wall
                wall_vertices = [
                    start + [0],
                    end + [0],
                    end + [height],
                    start + [height]
                ]
                
                for vertex in wall_vertices:
                    obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
                
                base_idx = vertex_count + 1
                obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
                vertex_count += 4
            else:
                # Wall with openings - create segments
                obj_content.append(f"# Wall segments with openings\n")
                
                # Create wall segments around doors and windows
                wall_length = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
                
                # For simplicity, create wall with openings marked
                segments = []
                current_pos = 0
                
                # Add door openings
                for door in doors_on_wall:
                    door_pos = door["position"]["offset"]
                    door_width = door["width"]
                    door_height = door["height"]
                    
                    # Segment before door
                    if door_pos > current_pos:
                        segments.append({
                            "start": current_pos,
                            "end": door_pos,
                            "type": "wall",
                            "height": height
                        })
                    
                    # Door opening
                    segments.append({
                        "start": door_pos,
                        "end": door_pos + door_width,
                        "type": "door",
                        "height": door_height
                    })
                    
                    current_pos = door_pos + door_width
                
                # Add window openings
                for window in windows_on_wall:
                    window_pos = window["position"]["offset"]
                    window_width = window["width"]
                    window_height = window["height"]
                    
                    segments.append({
                        "start": window_pos,
                        "end": window_pos + window_width,
                        "type": "window",
                        "height": window_height,
                        "sill_height": 3  # 3 feet from floor
                    })
                
                # Segment after last opening
                if current_pos < wall_length:
                    segments.append({
                        "start": current_pos,
                        "end": wall_length,
                        "type": "wall",
                        "height": height
                    })
                
                # Generate geometry for each segment
                for segment in segments:
                    if segment["type"] == "wall":
                        # Calculate position along wall
                        ratio_start = segment["start"] / wall_length
                        ratio_end = segment["end"] / wall_length
                        
                        seg_start = [
                            start[0] + (end[0] - start[0]) * ratio_start,
                            start[1] + (end[1] - start[1]) * ratio_start
                        ]
                        seg_end = [
                            start[0] + (end[0] - start[0]) * ratio_end,
                            start[1] + (end[1] - start[1]) * ratio_end
                        ]
                        
                        wall_vertices = [
                            seg_start + [0],
                            seg_end + [0],
                            seg_end + [segment["height"]],
                            seg_start + [segment["height"]]
                        ]
                        
                        for vertex in wall_vertices:
                            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
                        
                        base_idx = vertex_count + 1
                        obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
                        vertex_count += 4
                    
                    elif segment["type"] == "window":
                        # Create window frame
                        obj_content.append("usemtl window_material\n")
                        
                        ratio_start = segment["start"] / wall_length
                        ratio_end = segment["end"] / wall_length
                        sill_height = segment.get("sill_height", 3)
                        window_height = segment["height"]
                        
                        seg_start = [
                            start[0] + (end[0] - start[0]) * ratio_start,
                            start[1] + (end[1] - start[1]) * ratio_start
                        ]
                        seg_end = [
                            start[0] + (end[0] - start[0]) * ratio_end,
                            start[1] + (end[1] - start[1]) * ratio_end
                        ]
                        
                        # Window opening
                        window_vertices = [
                            seg_start + [sill_height],
                            seg_end + [sill_height],
                            seg_end + [sill_height + window_height],
                            seg_start + [sill_height + window_height]
                        ]
                        
                        for vertex in window_vertices:
                            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
                        
                        base_idx = vertex_count + 1
                        obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
                        vertex_count += 4
                        
                        obj_content.append("usemtl wall_material\n")  # Reset to wall material
                    
                    elif segment["type"] == "door":
                        # Create door frame
                        obj_content.append("usemtl door_material\n")
                        
                        ratio_start = segment["start"] / wall_length
                        ratio_end = segment["end"] / wall_length
                        door_height = segment["height"]
                        
                        seg_start = [
                            start[0] + (end[0] - start[0]) * ratio_start,
                            start[1] + (end[1] - start[1]) * ratio_start
                        ]
                        seg_end = [
                            start[0] + (end[0] - start[0]) * ratio_end,
                            start[1] + (end[1] - start[1]) * ratio_end
                        ]
                        
                        # Door frame (simplified)
                        door_vertices = [
                            seg_start + [0],
                            seg_end + [0],
                            seg_end + [door_height],
                            seg_start + [door_height]
                        ]
                        
                        for vertex in door_vertices:
                            obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
                        
                        base_idx = vertex_count + 1
                        obj_content.append(f"f {base_idx} {base_idx+1} {base_idx+2} {base_idx+3}\n")
                        vertex_count += 4
                        
                        obj_content.append("usemtl wall_material\n")  # Reset to wall material
        
        # === INTERIOR FEATURES ===
        if room["room_type"] == "bathroom":
            obj_content.append(f"# Bathroom fixtures for {room['name']}\n")
            obj_content.append("usemtl fixture_material\n")
            
            # Add toilet (simplified box)
            toilet_x = x_offset + 1
            toilet_y = y_offset + 1
            toilet_w = 1.5
            toilet_d = 2
            toilet_h = 1.5
            
            toilet_vertices = [
                # Bottom
                [toilet_x, toilet_y, 0],
                [toilet_x + toilet_w, toilet_y, 0],
                [toilet_x + toilet_w, toilet_y + toilet_d, 0],
                [toilet_x, toilet_y + toilet_d, 0],
                # Top
                [toilet_x, toilet_y, toilet_h],
                [toilet_x + toilet_w, toilet_y, toilet_h],
                [toilet_x + toilet_w, toilet_y + toilet_d, toilet_h],
                [toilet_x, toilet_y + toilet_d, toilet_h]
            ]
            
            for vertex in toilet_vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = vertex_count + 1
            # Create toilet box faces
            toilet_faces = [
                [base_idx, base_idx+1, base_idx+2, base_idx+3],  # Bottom
                [base_idx+7, base_idx+6, base_idx+5, base_idx+4],  # Top
                [base_idx, base_idx+4, base_idx+5, base_idx+1],  # Front
                [base_idx+1, base_idx+5, base_idx+6, base_idx+2],  # Right
                [base_idx+2, base_idx+6, base_idx+7, base_idx+3],  # Back
                [base_idx+3, base_idx+7, base_idx+4, base_idx]   # Left
            ]
            
            for face in toilet_faces:
                obj_content.append(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")
            vertex_count += 8
            
            # Add sink
            sink_x = x_offset + width - 2.5
            sink_y = y_offset + 1
            sink_w = 2
            sink_d = 1.5
            sink_h = 2.5
            
            sink_vertices = [
                # Bottom
                [sink_x, sink_y, 0],
                [sink_x + sink_w, sink_y, 0],
                [sink_x + sink_w, sink_y + sink_d, 0],
                [sink_x, sink_y + sink_d, 0],
                # Top
                [sink_x, sink_y, sink_h],
                [sink_x + sink_w, sink_y, sink_h],
                [sink_x + sink_w, sink_y + sink_d, sink_h],
                [sink_x, sink_y + sink_d, sink_h]
            ]
            
            for vertex in sink_vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = vertex_count + 1
            for face in toilet_faces:  # Reuse same face structure
                face_adjusted = [f + 8 for f in face]  # Adjust indices
                obj_content.append(f"f {face_adjusted[0]} {face_adjusted[1]} {face_adjusted[2]} {face_adjusted[3]}\n")
            vertex_count += 8
        
        elif room["room_type"] == "bedroom":
            obj_content.append(f"# Bedroom furniture for {room['name']}\n")
            obj_content.append("usemtl furniture_material\n")
            
            # Add bed (simplified)
            bed_x = x_offset + width/2 - 3
            bed_y = y_offset + length/2 - 2
            bed_w = 6
            bed_d = 4
            bed_h = 1.5
            
            bed_vertices = [
                # Bottom
                [bed_x, bed_y, 0],
                [bed_x + bed_w, bed_y, 0],
                [bed_x + bed_w, bed_y + bed_d, 0],
                [bed_x, bed_y + bed_d, 0],
                # Top
                [bed_x, bed_y, bed_h],
                [bed_x + bed_w, bed_y, bed_h],
                [bed_x + bed_w, bed_y + bed_d, bed_h],
                [bed_x, bed_y + bed_d, bed_h]
            ]
            
            for vertex in bed_vertices:
                obj_content.append(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
            
            base_idx = vertex_count + 1
            bed_faces = [
                [base_idx, base_idx+1, base_idx+2, base_idx+3],  # Bottom
                [base_idx+7, base_idx+6, base_idx+5, base_idx+4],  # Top
                [base_idx, base_idx+4, base_idx+5, base_idx+1],  # Front
                [base_idx+1, base_idx+5, base_idx+6, base_idx+2],  # Right
                [base_idx+2, base_idx+6, base_idx+7, base_idx+3],  # Back
                [base_idx+3, base_idx+7, base_idx+4, base_idx]   # Left
            ]
            
            for face in bed_faces:
                obj_content.append(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")
            vertex_count += 8
        
        obj_content.append("\n")
    
    # Write OBJ file
    os.makedirs("generated_models", exist_ok=True)
    
    with open(model_path, "w") as f:
        f.writelines(obj_content)
    
    # Also create a basic MTL file for materials
    mtl_path = model_path.replace('.obj', '.mtl')
    mtl_content = [
        "# ConstructAI Materials\n",
        "newmtl wall_material\n",
        "Kd 0.8 0.8 0.8\n",
        "Ka 0.2 0.2 0.2\n\n",
        "newmtl floor_material\n",
        "Kd 0.7 0.5 0.3\n",
        "Ka 0.1 0.1 0.1\n\n",
        "newmtl ceiling_material\n",
        "Kd 0.9 0.9 0.9\n",
        "Ka 0.3 0.3 0.3\n\n",
        "newmtl door_material\n",
        "Kd 0.6 0.3 0.1\n",
        "Ka 0.1 0.1 0.1\n\n",
        "newmtl window_material\n",
        "Kd 0.5 0.7 0.9\n",
        "Ka 0.1 0.1 0.1\n\n",
        "newmtl fixture_material\n",
        "Kd 0.9 0.9 0.9\n",
        "Ka 0.2 0.2 0.2\n\n",
        "newmtl furniture_material\n",
        "Kd 0.5 0.3 0.2\n",
        "Ka 0.1 0.1 0.1\n\n"
    ]
    
    with open(mtl_path, "w") as f:
        f.writelines(mtl_content)
    
    return model_filename  # Return just the filename, not the full path

def calculate_enhanced_construction_quantities(specs: Enhanced3DProjectSpecs, room_layout: Dict[str, Any]) -> Dict[str, float]:
    """Calculate construction quantities including doors and windows"""
    
    quantities = {}
    area_sqm = specs.total_area * 0.092903  # Convert sqft to sqm
    
    # Calculate wall area (including doors and windows)
    total_wall_area = 0
    for room in room_layout["rooms"]:
        perimeter = 2 * (room["width"] + room["length"])
        wall_area = perimeter * room["height"]
        
        # Subtract door and window areas
        for door in room["doors"]:
            wall_area -= door["width"] * door["height"]
        for window in room["windows"]:
            wall_area -= window["width"] * window["height"]
            
        total_wall_area += wall_area
    
    # Basic materials (existing logic)
    quantities["cement"] = area_sqm * 8 * specs.num_floors  # bags
    quantities["steel"] = area_sqm * 0.05 * specs.num_floors  # tons
    quantities["bricks"] = total_wall_area * 12  # pieces
    quantities["sand"] = area_sqm * 0.5 * specs.num_floors  # cft
    quantities["aggregate"] = area_sqm * 0.8 * specs.num_floors  # cft
    quantities["rcc_slab"] = area_sqm * specs.num_floors
    quantities["brick_wall"] = total_wall_area
    quantities["plaster"] = total_wall_area * 2 + area_sqm * specs.num_floors
    quantities["tiles"] = area_sqm * specs.num_floors
    quantities["paint"] = quantities["plaster"]
    
    # Calculate electrical and plumbing requirements based on actual room counts
    total_rooms = (specs.num_bedrooms + specs.num_living_rooms + specs.num_kitchens + 
                   specs.num_dining_rooms + specs.num_study_rooms + specs.num_guest_rooms + 
                   specs.num_utility_rooms + specs.num_store_rooms)
    
    quantities["electrical"] = total_rooms + specs.num_bathrooms
    quantities["plumbing"] = specs.num_bathrooms + specs.num_kitchens + specs.num_utility_rooms
    
    # Doors and windows
    main_doors = 1
    room_doors = room_layout["total_doors"] - main_doors
    total_windows = room_layout["total_windows"]
    
    if specs.main_door_type == "premium":
        quantities["door_premium"] = main_doors
    else:
        quantities["door_standard"] = main_doors
        
    quantities["door_standard"] = quantities.get("door_standard", 0) + room_doors
    
    if specs.window_type == "premium":
        quantities["window_premium"] = total_windows
    else:
        quantities["window_standard"] = total_windows
    
    quantities["door_frame"] = room_layout["total_doors"]
    quantities["window_frame"] = total_windows
    
    return quantities

def calculate_construction_quantities(specs: ProjectSpecs) -> Dict[str, float]:
    """Calculate material quantities based on project specifications"""
    
    area_sqft = specs.total_area
    area_sqm = area_sqft * 0.092903  # Convert sqft to sqm
    
    # Quality multipliers
    quality_multipliers = {
        "basic": 0.8,
        "standard": 1.0,
        "premium": 1.4
    }
    quality_factor = quality_multipliers.get(specs.quality_grade, 1.0)
    
    # Location multipliers
    location_multipliers = {
        "rural": 0.85,
        "suburban": 1.0,
        "urban": 1.15
    }
    location_factor = location_multipliers.get(specs.location, 1.0)
    
    # Basic quantity calculations
    quantities = {}
    
    # Concrete and foundation
    foundation_volume = area_sqm * 0.15  # 150mm thick foundation
    quantities["concrete_m25"] = foundation_volume * specs.num_floors
    
    # Steel requirement (typical 80-120 kg per sqm for RCC)
    steel_per_sqm = 100 if specs.construction_type == "commercial" else 80
    quantities["steel"] = (area_sqm * steel_per_sqm * specs.num_floors) / 1000  # Convert to tons
    
    # Cement calculation (1 bag per 2.5 sqm typically)
    quantities["cement"] = area_sqm * 0.4 * specs.num_floors
    
    # Bricks for walls (assuming 4.5 inch walls)
    wall_area = area_sqm * 0.6 * specs.num_floors  # 60% of floor area as wall area
    quantities["bricks"] = wall_area * 55  # 55 bricks per sqm
    
    # Sand and aggregate
    quantities["sand"] = area_sqm * 0.5 * specs.num_floors  # cft
    quantities["aggregate"] = area_sqm * 0.8 * specs.num_floors  # cft
    
    # RCC slab
    quantities["rcc_slab"] = area_sqm * specs.num_floors
    
    # Walls
    quantities["brick_wall"] = wall_area
    
    # Plaster (both sides of walls + ceiling)
    quantities["plaster"] = wall_area * 2 + area_sqm * specs.num_floors
    
    # Flooring tiles
    quantities["tiles"] = area_sqm * specs.num_floors
    
    # Paint (walls + ceiling)
    quantities["paint"] = quantities["plaster"]
    
    # Electrical and plumbing per room
    # Calculate total rooms for electrical requirements
    total_rooms = (specs.num_bedrooms + specs.num_living_rooms + specs.num_kitchens + 
                   specs.num_dining_rooms + specs.num_study_rooms + specs.num_guest_rooms + 
                   specs.num_utility_rooms + specs.num_store_rooms)
    quantities["electrical"] = total_rooms + specs.num_bathrooms
    quantities["plumbing"] = specs.num_bathrooms
    
    # Apply quality and location factors
    for item in quantities:
        quantities[item] *= quality_factor * location_factor
    
    return quantities

def calculate_enhanced_labor_requirements(specs: Enhanced3DProjectSpecs, quantities: Dict[str, float]) -> Dict[str, float]:
    """Calculate labor requirements based on Enhanced3DProjectSpecs"""
    
    labor_days = {}
    
    # Mason work
    mason_work_sqm = quantities.get("brick_wall", 0) + quantities.get("plaster", 0)
    labor_days["mason"] = mason_work_sqm * 0.1  # 0.1 days per sqm
    
    # Helper (1 helper per mason)
    labor_days["helper"] = labor_days["mason"]
    
    # Electrician
    labor_days["electrician"] = quantities.get("electrical", 0) * 2  # 2 days per room
    
    # Plumber
    labor_days["plumber"] = quantities.get("plumbing", 0) * 1.5  # 1.5 days per bathroom/kitchen
    
    # Painter
    labor_days["painter"] = quantities.get("paint", 0) * 0.05  # 0.05 days per sqm
    
    # Carpenter (for doors, windows, etc.)
    total_rooms = (specs.num_bedrooms + specs.num_living_rooms + specs.num_kitchens + 
                   specs.num_dining_rooms + specs.num_study_rooms + specs.num_guest_rooms + 
                   specs.num_utility_rooms + specs.num_store_rooms)
    labor_days["carpenter"] = total_rooms * 1.5  # 1.5 days per room
    
    return labor_days

def calculate_labor_requirements(specs: ProjectSpecs, quantities: Dict[str, float]) -> Dict[str, float]:
    """Calculate labor requirements based on quantities"""
    
    labor_days = {}
    
    # Mason work
    mason_work_sqm = quantities.get("brick_wall", 0) + quantities.get("plaster", 0)
    labor_days["mason"] = mason_work_sqm * 0.1  # 0.1 days per sqm
    
    # Helper (1 helper per mason)
    labor_days["helper"] = labor_days["mason"]
    
    # Electrician
    labor_days["electrician"] = quantities.get("electrical", 0) * 2  # 2 days per room
    
    # Plumber
    labor_days["plumber"] = quantities.get("plumbing", 0) * 1.5  # 1.5 days per bathroom
    
    # Painter
    labor_days["painter"] = quantities.get("paint", 0) * 0.05  # 0.05 days per sqm
    
    # Carpenter (for doors, windows, etc.)
    # Calculate total rooms for carpenter work
    total_rooms = (specs.num_bedrooms + specs.num_living_rooms + specs.num_kitchens + 
                   specs.num_dining_rooms + specs.num_study_rooms + specs.num_guest_rooms + 
                   specs.num_utility_rooms + specs.num_store_rooms)
    labor_days["carpenter"] = total_rooms * 1.5  # 1.5 days per room
    
    return labor_days

@router.post("/estimate", response_model=BOQResponse, summary="Calculate real BOQ and cost estimation")
async def calculate_boq(specs: ProjectSpecs):
    """Calculate detailed Bill of Quantities and cost estimation based on project specifications"""
    
    try:
        print(f"📊 Calculating BOQ for {specs.total_area} sqft {specs.construction_type} project")
        
        # Calculate material quantities
        quantities = calculate_construction_quantities(specs)
        
        # Calculate labor requirements
        labor_days = calculate_labor_requirements(specs, quantities)
        
        # Get current material rates (dynamic or static fallback)
        current_rates = get_current_material_rates()
        
        # Calculate costs
        material_items = []
        total_material_cost = 0
        
        for material, quantity in quantities.items():
            if material in current_rates:
                rate_info = current_rates[material]
                item_cost = quantity * rate_info["rate"]
                total_material_cost += item_cost
                
                material_items.append({
                    "category": "Material",
                    "item": material.replace("_", " ").title(),
                    "quantity": round(quantity, 2),
                    "unit": rate_info["unit"],
                    "rate": rate_info["rate"],
                    "amount": round(item_cost, 2)
                })
        
        # Calculate labor costs
        labor_items = []
        total_labor_cost = 0
        
        for labor_type, days in labor_days.items():
            if labor_type in LABOR_RATES:
                rate_info = LABOR_RATES[labor_type]
                item_cost = days * rate_info["rate"]
                total_labor_cost += item_cost
                
                labor_items.append({
                    "category": "Labor",
                    "item": labor_type.replace("_", " ").title(),
                    "quantity": round(days, 1),
                    "unit": rate_info["unit"],
                    "rate": rate_info["rate"],
                    "amount": round(item_cost, 2)
                })
        
        # Calculate timeline
        max_labor_days = max(labor_days.values()) if labor_days else 30
        timeline_days = int(max_labor_days * 1.3)  # Add 30% buffer
        
        # Combine all items
        all_items = material_items + labor_items
        
        # Add overhead and profit (15% of material + labor)
        subtotal = total_material_cost + total_labor_cost
        overhead = subtotal * 0.15
        
        all_items.append({
            "category": "Overhead",
            "item": "Contractor Overhead & Profit",
            "quantity": 1,
            "unit": "lump sum",
            "rate": round(overhead, 2),
            "amount": round(overhead, 2)
        })
        
        total_cost = subtotal + overhead
        
        boq_id = str(uuid.uuid4())
        
        result = BOQResponse(
            boq_id=boq_id,
            project_specs=specs,
            material_cost=round(total_material_cost, 2),
            labor_cost=round(total_labor_cost, 2),
            total_cost=round(total_cost, 2),
            items=all_items,
            timeline_days=timeline_days,
            generated_at=datetime.now().isoformat()
        )
        
        print(f"✅ BOQ calculated: ₹{total_cost:,.2f} for {timeline_days} days")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BOQ calculation failed: {str(e)}")

@router.post("/quick-estimate", summary="Quick cost estimation")
async def quick_estimate(area_sqft: float, construction_type: str = "residential"):
    """Quick cost estimation based on area and type"""
    
    # Quick estimation rates per sqft
    rates_per_sqft = {
        "residential": {"basic": 1200, "standard": 1800, "premium": 2800},
        "commercial": {"basic": 1500, "standard": 2200, "premium": 3500},
        "industrial": {"basic": 1000, "standard": 1500, "premium": 2200}
    }
    
    type_rates = rates_per_sqft.get(construction_type, rates_per_sqft["residential"])
    
    estimates = {}
    for grade, rate in type_rates.items():
        estimates[grade] = {
            "cost_per_sqft": rate,
            "total_cost": area_sqft * rate,
            "timeline_months": math.ceil(area_sqft / 500)  # Rough estimate
        }
    
    return {
        "area_sqft": area_sqft,
        "construction_type": construction_type,
        "estimates": estimates,
        "currency": "INR",
        "note": "These are rough estimates. Use detailed BOQ for accurate costing."
    }

@router.get("/{boq_id}", summary="Get BOQ details")
async def get_boq(boq_id: str):
    """Get BOQ details by ID"""
    return {"boq_id": boq_id, "message": "BOQ details endpoint working"}

@router.get("/", summary="List all BOQs")
async def list_boqs():
    """List all BOQ calculations"""
    return {"boqs": [], "message": "BOQ list endpoint working"}

@router.post("/export/{boq_id}", summary="Export BOQ to PDF/Excel")
async def export_boq(boq_id: str, format: str = "pdf"):
    """Export BOQ to PDF or Excel format"""
    return {
        "boq_id": boq_id,
        "format": format,
        "download_url": f"/files/boq_{boq_id}.{format}",
        "message": "BOQ export ready"
    }

@router.post("/estimate-3d", response_model=BOQ3DResponse, summary="Calculate BOQ with 3D Room Generation")
async def calculate_boq_with_3d(specs: Enhanced3DProjectSpecs):
    """Calculate detailed BOQ with 3D room visualization"""
    
    try:
        print(f"🏗️ Generating 3D BOQ for {specs.total_area} sqft {specs.construction_type} project")
        print(f"📊 Specs: {specs.num_bedrooms} bedrooms, {specs.num_living_rooms} living rooms, {specs.num_kitchens} kitchens, {specs.num_bathrooms} bathrooms, {specs.quality_grade} quality")
        
        # Generate 3D room layout
        print("🔄 Generating 3D room layout...")
        room_layout = generate_3d_room_layout(specs)
        print(f"✅ Room layout generated: {len(room_layout.get('rooms', []))} rooms")
        
        # Calculate material quantities (enhanced)
        print("🔄 Calculating material quantities...")
        quantities = calculate_enhanced_construction_quantities(specs, room_layout)
        print(f"✅ Quantities calculated: {len(quantities)} materials")
        
        # Calculate labor requirements  
        print("🔄 Calculating labor requirements...")
        labor_days = calculate_enhanced_labor_requirements(specs, quantities)
        print(f"✅ Labor calculated: {len(labor_days)} labor types")
        
        # Get current material rates (dynamic or static fallback)
        print("🔄 Getting material rates...")
        current_rates = get_current_material_rates()
        print(f"✅ Material rates obtained: {len(current_rates)} materials")
        
        # Calculate costs
        material_items = []
        total_material_cost = 0
        
        print("🔄 Calculating material costs...")
        for material, quantity in quantities.items():
            if material in current_rates:
                rate_info = current_rates[material]
                item_cost = quantity * rate_info["rate"]
                total_material_cost += item_cost
                
                material_items.append({
                    "category": "Material",
                    "item": material.replace("_", " ").title(),
                    "quantity": round(quantity, 2),
                    "unit": rate_info["unit"],
                    "rate": rate_info["rate"],
                    "amount": round(item_cost, 2)
                })
        
        print(f"✅ Material costs calculated: ₹{total_material_cost:,.2f}")
        
        # Calculate labor costs
        labor_items = []
        total_labor_cost = 0
        
        print("🔄 Calculating labor costs...")
        for labor_type, days in labor_days.items():
            if labor_type in LABOR_RATES:
                rate_info = LABOR_RATES[labor_type]
                item_cost = days * rate_info["rate"]
                total_labor_cost += item_cost
                
                labor_items.append({
                    "category": "Labor",
                    "item": labor_type.replace("_", " ").title(),
                    "quantity": round(days, 1),
                    "unit": rate_info["unit"],
                    "rate": rate_info["rate"],
                    "amount": round(item_cost, 2)
                })
        
        print(f"✅ Labor costs calculated: ₹{total_labor_cost:,.2f}")
        
        # Generate 3D model file
        print("🔄 Generating 3D model file...")
        model_file_path = generate_3d_model_file(room_layout, specs)
        print(f"✅ 3D model generated: {model_file_path}")
        
        # Combine all items
        all_items = material_items + labor_items
        
        # Add overhead costs (10% of material + labor)
        overhead_cost = (total_material_cost + total_labor_cost) * 0.1
        all_items.append({
            "category": "Overhead",
            "item": "Project Management & Misc",
            "quantity": 1,
            "unit": "lump sum",
            "rate": overhead_cost,
            "amount": overhead_cost
        })
        
        total_cost = total_material_cost + total_labor_cost + overhead_cost
        
        # Prepare cost breakdown
        cost_breakdown = {
            "material_cost": round(total_material_cost, 2),
            "labor_cost": round(total_labor_cost, 2),
            "overhead_cost": round(overhead_cost, 2),
            "total_cost": round(total_cost, 2),
            "cost_per_sqft": round(total_cost / specs.total_area, 2)
        }
        
        # Enhanced room data for 3D visualization
        room_3d_data = {
            "room_layout": room_layout,
            "material_quantities": quantities,
            "visualization_data": {
                "rooms": room_layout["rooms"],
                "building_dimensions": room_layout["building_dimensions"],
                "total_doors": room_layout["total_doors"],
                "total_windows": room_layout["total_windows"],
                "wall_material": "brick" if specs.quality_grade == "standard" else "concrete",
                "flooring_material": specs.flooring_type,
                "ceiling_material": specs.ceiling_type
            }
        }
        
        boq_id = str(uuid.uuid4())
        
        result = BOQ3DResponse(
            boq_id=boq_id,
            project_specs=specs,
            total_cost=round(total_cost, 2),
            material_cost=round(total_material_cost, 2),
            labor_cost=round(total_labor_cost, 2),
            items=all_items,
            cost_breakdown=cost_breakdown,
            room_3d_data=room_3d_data,
            model_file_path=model_file_path,
            created_at=datetime.now().isoformat()
        )
        
        print(f"✅ 3D BOQ calculated successfully. Total cost: ₹{total_cost:,.2f}")
        print(f"📁 3D Model saved: {model_file_path}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error calculating 3D BOQ: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"BOQ calculation failed: {str(e)}"
        )

@router.get("/download-model/{model_filename}")
async def download_3d_model(model_filename: str):
    """Download the generated 3D model file"""
    try:
        # Security check: only allow OBJ files and prevent directory traversal
        if not model_filename.endswith('.obj') or '..' in model_filename or '/' in model_filename or '\\' in model_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename"
            )
        
        file_path = f"generated_models/{model_filename}"
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model file not found"
            )
        
        return FileResponse(
            path=file_path,
            filename=model_filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        print(f"❌ Error serving model file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to serve model file: {str(e)}"
        )
