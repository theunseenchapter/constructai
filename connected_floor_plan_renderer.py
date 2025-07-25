#!/usr/bin/env python3
"""
Connected Floor Plan Renderer - Creates proper connected home layouts
"""
import subprocess
import os
import tempfile
import uuid
import json
import shutil
import math
import random

# Force NVIDIA GPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['BLENDER_CUDA_DEVICE'] = '0'
os.environ['NVIDIA_VISIBLE_DEVICES'] = '0'

class ConnectedFloorPlanRenderer:
    """Creates connected, realistic floor plans with proper room layouts"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_connected_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
    
    def create_connected_layout(self, rooms, building_dims):
        """Create a connected floor plan layout"""
        
        # Standard room dimensions for realistic layouts
        room_configs = {
            'living': {'width': 6, 'length': 5, 'priority': 1},
            'kitchen': {'width': 4, 'length': 4, 'priority': 2},
            'bedroom': {'width': 4, 'length': 3.5, 'priority': 3},
            'bathroom': {'width': 2.5, 'length': 2, 'priority': 4},
            'dining': {'width': 4, 'length': 3, 'priority': 2},
            'office': {'width': 3, 'length': 3, 'priority': 4},
        }
        
        # Create a grid-based layout
        grid_size = 1.0  # 1 meter grid
        building_width = building_dims['total_width']
        building_length = building_dims['total_length']
        
        # Calculate grid dimensions
        grid_width = int(building_width / grid_size)
        grid_length = int(building_length / grid_size)
        
        # Create connected room layout
        layout = []
        
        # Start with main rooms and place them connected
        main_rooms = [r for r in rooms if r.get('type') in ['living', 'kitchen']]
        bedrooms = [r for r in rooms if r.get('type') == 'bedroom']
        bathrooms = [r for r in rooms if r.get('type') == 'bathroom']
        
        current_x = -building_width/2 + 3
        current_y = -building_length/2 + 3
        
        # Place living room first (main room)
        if main_rooms:
            living_room = main_rooms[0]
            room_width = room_configs.get(living_room['type'], {}).get('width', 5)
            room_length = room_configs.get(living_room['type'], {}).get('length', 4)
            
            layout.append({
                'room': living_room,
                'x': current_x,
                'y': current_y,
                'width': room_width,
                'length': room_length,
                'height': 3.0
            })
            
            current_x += room_width + 0.5  # Move to next position
        
        # Place kitchen next to living room
        kitchen_rooms = [r for r in rooms if r.get('type') == 'kitchen']
        if kitchen_rooms:
            kitchen = kitchen_rooms[0]
            room_width = room_configs.get('kitchen', {}).get('width', 4)
            room_length = room_configs.get('kitchen', {}).get('length', 4)
            
            layout.append({
                'room': kitchen,
                'x': current_x,
                'y': current_y,
                'width': room_width,
                'length': room_length,
                'height': 3.0
            })
            
            current_y += room_length + 0.5  # Move to next row
        
        # Place bedrooms in a row
        current_x = -building_width/2 + 3
        for bedroom in bedrooms:
            room_width = room_configs.get('bedroom', {}).get('width', 4)
            room_length = room_configs.get('bedroom', {}).get('length', 3.5)
            
            layout.append({
                'room': bedroom,
                'x': current_x,
                'y': current_y,
                'width': room_width,
                'length': room_length,
                'height': 3.0
            })
            
            current_x += room_width + 0.5
        
        # Place bathrooms
        current_y += 4
        current_x = -building_width/2 + 3
        for bathroom in bathrooms:
            room_width = room_configs.get('bathroom', {}).get('width', 2.5)
            room_length = room_configs.get('bathroom', {}).get('length', 2)
            
            layout.append({
                'room': bathroom,
                'x': current_x,
                'y': current_y,
                'width': room_width,
                'length': room_length,
                'height': 3.0
            })
            
            current_x += room_width + 1
        
        return layout
    
    def render_connected_floor_plan(self, boq_config):
        """Render a connected floor plan with proper room connections"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 40, "total_length": 30, "height": 12})
        architectural_style = boq_config.get('architectural_style', 'modern')
        
        print(f"Creating connected floor plan: {self.scene_id}")
        print(f"Rooms: {len(rooms)}")
        print(f"Style: {architectural_style}")
        
        # Create proper connected layout
        layout_positions = self.create_connected_layout(rooms, building_dims)
        
        # Create Blender script for connected floor plan
        blender_script = f'''
import bpy
import bmesh
import math
import random
from mathutils import Vector

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

scene = bpy.context.scene

# GPU setup
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.samples = 128
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Create beautiful floor plan materials
def create_material(name, color, roughness=0.8):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat

# Beautiful room materials
materials = {
    'living_floor': create_material("Living Floor", (0.8, 0.6, 0.4)),  # Warm wood
    'kitchen_floor': create_material("Kitchen Floor", (0.9, 0.9, 0.85)),  # Light tile
    'bedroom_floor': create_material("Bedroom Floor", (0.7, 0.5, 0.3)),  # Dark wood
    'bathroom_floor': create_material("Bathroom Floor", (0.85, 0.9, 0.95)),  # Light blue
    'wall': create_material("Wall", (0.95, 0.95, 0.95)),  # White walls
    'exterior_wall': create_material("Exterior Wall", (0.6, 0.6, 0.6)),  # Gray exterior
    'furniture': create_material("Furniture", (0.5, 0.3, 0.2)),  # Brown furniture
    'cabinet': create_material("Cabinet", (0.4, 0.2, 0.1)),  # Dark wood
    'counter': create_material("Counter", (0.2, 0.2, 0.25)),  # Dark counter
    'fixture': create_material("Fixture", (1.0, 1.0, 1.0)),  # White fixtures
    'door': create_material("Door", (0.6, 0.4, 0.2)),  # Wood door
}

# Create the complete house structure first
building_width = {building_dims['total_width']}
building_length = {building_dims['total_length']}

# Create main foundation/floor
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.05))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (building_width/2, building_length/2, 1)
foundation.data.materials.append(materials['wall'])

# Create exterior walls as one connected structure
wall_height = 2.5
wall_thickness = 0.3

# Create exterior walls
exterior_positions = [
    (-building_width/2, 0, wall_height/2, wall_thickness, building_length, wall_height),  # Left
    (building_width/2, 0, wall_height/2, wall_thickness, building_length, wall_height),   # Right
    (0, -building_length/2, wall_height/2, building_width, wall_thickness, wall_height), # Front
    (0, building_length/2, wall_height/2, building_width, wall_thickness, wall_height),  # Back
]

for i, (x, y, z, w, l, h) in enumerate(exterior_positions):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    wall = bpy.context.active_object
    wall.name = f"ExteriorWall_{{i}}"
    wall.scale = (w, l, h/2)
    wall.data.materials.append(materials['exterior_wall'])

# Create rooms with proper connections
layout_data = {json.dumps(layout_positions)}

print(f"Creating {{len(layout_data)}} connected rooms...")

# Track room boundaries for wall creation
room_boundaries = []

for room_data in layout_data:
    room = room_data['room']
    x = room_data['x']
    y = room_data['y'] 
    width = room_data['width']
    length = room_data['length']
    height = room_data.get('height', 3.0)
    room_type = room.get('type', 'general')
    
    print(f"Creating room: {{room['name']}} at ({{x}}, {{y}}) - {{width}}x{{length}}")
    
    # Store room boundary
    room_boundaries.append({{
        'x': x, 'y': y, 'width': width, 'length': length, 
        'type': room_type, 'name': room['name']
    }})
    
    # Create room floor with proper material
    floor_material = materials['living_floor']
    if room_type == 'kitchen':
        floor_material = materials['kitchen_floor']
    elif room_type == 'bedroom':
        floor_material = materials['bedroom_floor']
    elif room_type == 'bathroom':
        floor_material = materials['bathroom_floor']
    
    # Room floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room['name']}}"
    floor.scale = (width/2, length/2, 1)
    floor.data.materials.append(floor_material)
    
    # Create interior walls for room separation
    interior_wall_thickness = 0.2
    interior_wall_height = 2.4
    
    # Create walls around room (will be optimized later)
    wall_positions = [
        (x - width/2, y, interior_wall_height/2, interior_wall_thickness, length, interior_wall_height),
        (x + width/2, y, interior_wall_height/2, interior_wall_thickness, length, interior_wall_height),
        (x, y - length/2, interior_wall_height/2, width, interior_wall_thickness, interior_wall_height),
        (x, y + length/2, interior_wall_height/2, width, interior_wall_thickness, interior_wall_height),
    ]
    
    for i, (wx, wy, wz, w_width, w_length, w_height) in enumerate(wall_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz))
        wall = bpy.context.active_object
        wall.name = f"Wall_{{room['name']}}_{{i}}"
        wall.scale = (w_width, w_length, w_height/2)
        wall.data.materials.append(materials['wall'])
    
    # Add simple furniture based on room type
    if room_type == 'living':
        # Sofa
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y - length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "Sofa"
        sofa.scale = (2.0, 0.8, 0.8)
        sofa.data.materials.append(materials['furniture'])
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y + length/4, 0.25))
        table = bpy.context.active_object
        table.name = "CoffeeTable"
        table.scale = (1.2, 0.6, 0.5)
        table.data.materials.append(materials['furniture'])
        
    elif room_type == 'kitchen':
        # Kitchen counter
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x - width/3, y, 0.45))
        counter = bpy.context.active_object
        counter.name = "KitchenCounter"
        counter.scale = (width/3, 0.6, 0.9)
        counter.data.materials.append(materials['cabinet'])
        
        # Countertop
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x - width/3, y, 0.9))
        countertop = bpy.context.active_object
        countertop.name = "Countertop"
        countertop.scale = (width/3 + 0.1, 0.65, 0.05)
        countertop.data.materials.append(materials['counter'])
        
    elif room_type == 'bedroom':
        # Bed
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.3))
        bed = bpy.context.active_object
        bed.name = "Bed"
        bed.scale = (1.8, 2.0, 0.6)
        bed.data.materials.append(materials['furniture'])
        
    elif room_type == 'bathroom':
        # Toilet
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x - width/3, y, 0.2))
        toilet = bpy.context.active_object
        toilet.name = "Toilet"
        toilet.scale = (0.4, 0.6, 0.4)
        toilet.data.materials.append(materials['fixture'])
        
        # Sink
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + width/3, y, 0.4))
        sink = bpy.context.active_object
        sink.name = "Sink"
        sink.scale = (0.6, 0.4, 0.8)
        sink.data.materials.append(materials['fixture'])

# Add doors between rooms
door_height = 2.0
door_width = 0.9

# Create a few strategic doors
door_positions = [
    (0, -5, door_height/2, 0.1, door_width, door_height),  # Main entrance
]

for i, (dx, dy, dz, dw, dl, dh) in enumerate(door_positions):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(dx, dy, dz))
    door = bpy.context.active_object
    door.name = f"Door_{{i}}"
    door.scale = (dw, dl, dh/2)
    door.data.materials.append(materials['door'])

# Professional lighting
bpy.ops.object.light_add(type='SUN', location=(0, 0, 20))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 5.0
sun.rotation_euler = (0, 0, 0)

# Area lights for interior
area_lights = [
    (0, 0, 15, 300),  # Main light
    (-10, -10, 10, 150),  # Corner light
    (10, 10, 10, 150),   # Corner light
]

for i, (lx, ly, lz, energy) in enumerate(area_lights):
    bpy.ops.object.light_add(type='AREA', location=(lx, ly, lz))
    light = bpy.context.active_object
    light.name = f"AreaLight_{{i}}"
    light.data.energy = energy
    light.data.size = 3.0

# Perfect isometric camera
camera_distance = max(building_width, building_length) * 0.7
bpy.ops.object.camera_add(location=(camera_distance, -camera_distance, camera_distance))
camera = bpy.context.active_object
camera.name = "IsometricCamera"
camera.rotation_euler = (1.0, 0, 0.785)
scene.camera = camera

# Set camera to orthographic
camera.data.type = 'ORTHO'
camera.data.ortho_scale = max(building_width, building_length) * 1.1

# Export files
output_dir = "{self.temp_dir.replace(chr(92), '/')}"
blend_file = f"{{output_dir}}/connected_floor_plan_{self.scene_id}.blend"
obj_file = f"{{output_dir}}/connected_floor_plan_{self.scene_id}.obj"
render_file = f"{{output_dir}}/connected_floor_plan_{self.scene_id}.png"

# Save files
bpy.ops.wm.save_as_mainfile(filepath=blend_file)
print(f"BLEND_FILE: {{blend_file}}")

# Export OBJ with error handling
try:
    # Try newer OBJ export first
    bpy.ops.wm.obj_export(filepath=obj_file, check_existing=False, export_selected_objects=False, export_materials=True)
    print(f"OBJ_FILE: {{obj_file}}")
except:
    try:
        # Fallback to legacy export
        bpy.ops.export_scene.obj(filepath=obj_file, check_existing=False, use_selection=False, use_materials=True)
        print(f"OBJ_FILE: {{obj_file}}")
    except Exception as e:
        print(f"OBJ export failed: {{e}}")

# Check if MTL file was created
mtl_file = obj_file.replace('.obj', '.mtl')
import os
if os.path.exists(mtl_file):
    print(f"MTL_FILE: {{mtl_file}}")
else:
    print("MTL_FILE: Not created")

# Render image
scene.render.filepath = render_file
bpy.ops.render.render(write_still=True)
print(f"RENDER_PNG: {{render_file}}")

print(f"SCENE_ID: {self.scene_id}")
print("LAYOUT_TYPE: connected_floor_plan") 
print("STYLE: modern")
print("QUALITY_LEVEL: architectural")
print("SUCCESS: Connected floor plan created")
'''
        
        # Write and execute script
        script_path = os.path.join(self.temp_dir, f'connected_floor_plan_{self.scene_id}.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        print(f"Script written to: {script_path}")
        
        # Run Blender
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print("✅ Connected floor plan created successfully")
                print("Blender output:")
                print(result.stdout)
                
                # Copy files to public directory
                public_dir = os.path.join(os.getcwd(), 'public', 'renders')
                if not os.path.exists(public_dir):
                    os.makedirs(public_dir, exist_ok=True)
                
                # Copy generated files
                temp_files = [
                    f'connected_floor_plan_{self.scene_id}.blend',
                    f'connected_floor_plan_{self.scene_id}.obj',
                    f'connected_floor_plan_{self.scene_id}.mtl',
                    f'connected_floor_plan_{self.scene_id}.png'
                ]
                
                for filename in temp_files:
                    src_path = os.path.join(self.temp_dir, filename)
                    if os.path.exists(src_path):
                        dst_path = os.path.join(public_dir, filename)
                        shutil.copy2(src_path, dst_path)
                        print(f"✅ Copied {filename} to public/renders/")
                    else:
                        print(f"⚠️ File not found: {filename}")
                
                return result.stdout
            else:
                print(f"❌ Blender error: {result.stderr}")
                return f"Error: {result.stderr}"
        
        except subprocess.TimeoutExpired:
            return "Error: Blender timeout"
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python connected_floor_plan_renderer.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file: {config_file}")
        sys.exit(1)
    
    renderer = ConnectedFloorPlanRenderer()
    output = renderer.render_connected_floor_plan(config)
    print(output)

if __name__ == "__main__":
    main()
