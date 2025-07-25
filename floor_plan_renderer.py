#!/usr/bin/env python3
"""
Floor Plan Renderer - Creates 3D floor plans with interior details
Open top-down view without ceilings, colorful materials, architectural style
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

from advanced_layout_generator import AdvancedLayoutGenerator

class FloorPlanRenderer:
    """3D Floor Plan Renderer with interior details and colorful materials"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_floorplan_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        self.layout_generator = AdvancedLayoutGenerator()
    
    def render_floor_plan(self, boq_config):
        """Render a 3D floor plan with interior details and no ceiling"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 40, "total_length": 30, "height": 12})
        enhanced_features = boq_config.get('enhanced_features', {})
        architectural_style = boq_config.get('architectural_style', 'modern')
        quality_level = boq_config.get('quality_level', 'professional')
        
        print(f"Creating 3D floor plan: {self.scene_id}")
        print(f"Rooms to generate: {len(rooms)}")
        print(f"Building dimensions: {building_dims}")
        print(f"Style: {architectural_style}")
        
        # Generate advanced layout
        layout_positions = self.layout_generator.generate_layout(rooms, building_dims)
        
        # Create floor plan Blender script
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

# GPU setup for high-quality rendering
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
cprefs.compute_device_type = 'OPTIX'
cprefs.get_devices()

print("Configuring GPU for floor plan rendering...")
for i, device in enumerate(cprefs.devices):
    if device.type in ['OPTIX', 'CUDA']:
        device.use = True
        print(f"ENABLED GPU {{i}}: {{device.name}} ({{device.type}})")
    else:
        device.use = False

scene.cycles.device = 'GPU'
scene.cycles.samples = 128  # Good quality for floor plans
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Colorful floor plan materials
def create_floor_plan_material(name, base_color, roughness=0.8, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission > 0:
        bsdf.inputs["Emission"].default_value = (*base_color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat

# Create colorful architectural materials
materials = {{
    'living_room_floor': create_floor_plan_material("Living Room Floor", (0.8, 0.6, 0.4)),  # Warm wood
    'kitchen_floor': create_floor_plan_material("Kitchen Floor", (0.9, 0.9, 0.85)),  # Light tile
    'bedroom_floor': create_floor_plan_material("Bedroom Floor", (0.7, 0.5, 0.3)),  # Dark wood
    'bathroom_floor': create_floor_plan_material("Bathroom Floor", (0.85, 0.9, 0.95)),  # Light blue tile
    'exterior_wall': create_floor_plan_material("Exterior Wall", (0.6, 0.6, 0.6)),  # Gray
    'interior_wall': create_floor_plan_material("Interior Wall", (0.95, 0.95, 0.95)),  # White
    'kitchen_cabinet': create_floor_plan_material("Kitchen Cabinet", (0.4, 0.2, 0.1)),  # Dark wood
    'kitchen_counter': create_floor_plan_material("Kitchen Counter", (0.2, 0.2, 0.25)),  # Dark granite
    'bathroom_fixture': create_floor_plan_material("Bathroom Fixture", (1.0, 1.0, 1.0)),  # White
    'bedroom_furniture': create_floor_plan_material("Bedroom Furniture", (0.5, 0.3, 0.2)),  # Medium wood
    'living_furniture': create_floor_plan_material("Living Furniture", (0.3, 0.4, 0.6)),  # Blue fabric
    'door': create_floor_plan_material("Door", (0.6, 0.4, 0.2)),  # Wood door
    'window': create_floor_plan_material("Window", (0.8, 0.9, 1.0)),  # Light blue glass
}}

def create_floor_plan_furniture(room_type, x, y, width, length, height):
    """Create simplified furniture for floor plan view"""
    furniture = []
    
    if room_type == 'kitchen':
        # Kitchen cabinets along walls
        cabinet_positions = [
            (x - width/2 + 0.3, y - length/2 + 0.3, 0.45, width - 0.6, 0.6, 0.9),  # Lower cabinets
            (x - width/2 + 0.3, y + length/2 - 0.3, 0.45, width - 0.6, 0.6, 0.9),  # Upper cabinets
        ]
        
        for i, (cx, cy, cz, cw, cl, ch) in enumerate(cabinet_positions):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
            cabinet = bpy.context.active_object
            cabinet.name = f"KitchenCabinet_{{i}}"
            cabinet.scale = (cw, cl, ch)
            cabinet.data.materials.append(materials['kitchen_cabinet'])
            furniture.append(cabinet)
        
        # Kitchen island
        if width > 4 and length > 4:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.45))
            island = bpy.context.active_object
            island.name = "KitchenIsland"
            island.scale = (2.0, 1.0, 0.9)
            island.data.materials.append(materials['kitchen_counter'])
            furniture.append(island)
    
    elif room_type == 'living':
        # Living room furniture
        furniture_items = [
            (x, y - length/4, 0.4, 2.2, 0.8, 0.8, 'living_furniture'),  # Sofa
            (x, y + length/4, 0.25, 1.2, 0.6, 0.5, 'living_furniture'),  # Coffee table
            (x - width/3, y - length/3, 0.4, 0.8, 0.8, 0.8, 'living_furniture'),  # Chair 1
            (x + width/3, y - length/3, 0.4, 0.8, 0.8, 0.8, 'living_furniture'),  # Chair 2
        ]
        
        for i, (fx, fy, fz, fw, fl, fh, mat_name) in enumerate(furniture_items):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(fx, fy, fz))
            furn = bpy.context.active_object
            furn.name = f"LivingFurniture_{{i}}"
            furn.scale = (fw, fl, fh)
            furn.data.materials.append(materials[mat_name])
            furniture.append(furn)
    
    elif room_type == 'bedroom':
        # Bedroom furniture
        furniture_items = [
            (x, y - length/4, 0.3, 2.0, 1.8, 0.6, 'bedroom_furniture'),  # Bed
            (x - width/2 + 0.5, y + length/3, 0.4, 0.8, 0.6, 0.8, 'bedroom_furniture'),  # Dresser
            (x + width/2 - 0.5, y + length/3, 1.0, 0.8, 0.6, 2.0, 'bedroom_furniture'),  # Wardrobe
        ]
        
        for i, (fx, fy, fz, fw, fl, fh, mat_name) in enumerate(furniture_items):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(fx, fy, fz))
            furn = bpy.context.active_object
            furn.name = f"BedroomFurniture_{{i}}"
            furn.scale = (fw, fl, fh)
            furn.data.materials.append(materials[mat_name])
            furniture.append(furn)
    
    elif room_type == 'bathroom':
        # Bathroom fixtures
        fixtures = [
            (x - width/3, y + length/3, 0.4, 0.6, 0.4, 0.8, 'bathroom_fixture'),  # Toilet
            (x + width/3, y + length/3, 0.4, 0.8, 0.5, 0.8, 'bathroom_fixture'),  # Sink
            (x, y - length/3, 0.3, 1.6, 0.7, 0.6, 'bathroom_fixture'),  # Bathtub
        ]
        
        for i, (fx, fy, fz, fw, fl, fh, mat_name) in enumerate(fixtures):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(fx, fy, fz))
            fixture = bpy.context.active_object
            fixture.name = f"BathroomFixture_{{i}}"
            fixture.scale = (fw, fl, fh)
            fixture.data.materials.append(materials[mat_name])
            furniture.append(fixture)
    
    return furniture

# Create floor plan layout
layout_positions = {json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

print(f"Creating floor plan with {{len(layout_positions)}} rooms...")

for room_data in layout_positions:
    room = room_data['room']
    x = room_data['x']
    y = room_data['y']
    width = room_data['width']
    length = room_data['length']
    height = room.get('height', 3.0)
    room_type = room.get('type', 'general')
    
    print(f"Creating room: {{room['name']}} ({{room_type}}) at ({{x}}, {{y}})")
    
    # Choose floor material based on room type
    if room_type == 'kitchen':
        floor_material = materials['kitchen_floor']
    elif room_type == 'living':
        floor_material = materials['living_room_floor']
    elif room_type == 'bedroom':
        floor_material = materials['bedroom_floor']
    elif room_type == 'bathroom':
        floor_material = materials['bathroom_floor']
    else:
        floor_material = materials['living_room_floor']
    
    # Create colorful floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room['name']}}"
    floor.scale = (width/2, length/2, 1)
    floor.data.materials.append(floor_material)
    
    # NO CEILING - this is the key difference for floor plan view
    
    # Create walls (lower height for floor plan view)
    wall_thickness = 0.2
    wall_height = 2.5  # Lower walls for better top-down view
    
    wall_positions = [
        (x - width/2, y, wall_height/2, wall_thickness, length, wall_height),  # Left wall
        (x + width/2, y, wall_height/2, wall_thickness, length, wall_height),  # Right wall
        (x, y - length/2, wall_height/2, width, wall_thickness, wall_height),  # Front wall
        (x, y + length/2, wall_height/2, width, wall_thickness, wall_height),  # Back wall
    ]
    
    for i, (wx, wy, wz, w_width, w_length, w_height) in enumerate(wall_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz))
        wall = bpy.context.active_object
        wall.name = f"Wall_{{room['name']}}_{{i}}"
        wall.scale = (w_width, w_length, w_height/2)
        wall.data.materials.append(materials['interior_wall'])
    
    # Add doors and windows
    # Door opening (create a gap in one wall)
    if room_type != 'bathroom':
        door_x = x + width/2 - 0.5
        door_y = y
        door_z = wall_height/2
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(door_x, door_y, door_z))
        door = bpy.context.active_object
        door.name = f"Door_{{room['name']}}"
        door.scale = (0.1, 0.9, 2.0)
        door.data.materials.append(materials['door'])
    
    # Add windows
    window_x = x
    window_y = y + length/2 - 0.1
    window_z = wall_height * 0.6
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(window_x, window_y, window_z))
    window = bpy.context.active_object
    window.name = f"Window_{{room['name']}}"
    window.scale = (1.2, 0.1, 0.8)
    window.data.materials.append(materials['window'])
    
    # Add furniture
    furniture = create_floor_plan_furniture(room_type, x, y, width, length, height)

# Add exterior walls
building_width = {building_dims['total_width']}
building_length = {building_dims['total_length']}
building_height = 3.0  # Lower for floor plan view

exterior_wall_thickness = 0.3
exterior_positions = [
    (-building_width/2, 0, building_height/2, exterior_wall_thickness, building_length, building_height),
    (building_width/2, 0, building_height/2, exterior_wall_thickness, building_length, building_height),
    (0, -building_length/2, building_height/2, building_width, exterior_wall_thickness, building_height),
    (0, building_length/2, building_height/2, building_width, exterior_wall_thickness, building_height),
]

for i, (x, y, z, w, l, h) in enumerate(exterior_positions):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    ext_wall = bpy.context.active_object
    ext_wall.name = f"ExteriorWall_{{i}}"
    ext_wall.scale = (w, l, h/2)
    ext_wall.data.materials.append(materials['exterior_wall'])

# Floor plan optimized lighting
# Bright top-down lighting
bpy.ops.object.light_add(type='SUN', location=(0, 0, 50))
sun = bpy.context.active_object
sun.name = "TopDownLight"
sun.data.energy = 5.0
sun.rotation_euler = (0, 0, 0)  # Direct top-down

# Additional area lights for even illumination
area_lights = [
    (0, 0, 20, 500),  # Main top light
    (-building_width/2, 0, 15, 200),  # Left side
    (building_width/2, 0, 15, 200),   # Right side
    (0, -building_length/2, 15, 200), # Front
    (0, building_length/2, 15, 200),  # Back
]

for i, (lx, ly, lz, energy) in enumerate(area_lights):
    bpy.ops.object.light_add(type='AREA', location=(lx, ly, lz))
    area_light = bpy.context.active_object
    area_light.name = f"AreaLight_{{i}}"
    area_light.data.energy = energy
    area_light.data.size = 5.0
    area_light.rotation_euler = (0, 0, 0)

# Floor plan camera - isometric top-down view
camera_distance = max(building_width, building_length) * 0.8
bpy.ops.object.camera_add(location=(camera_distance, -camera_distance, camera_distance))
camera = bpy.context.active_object
camera.name = "FloorPlanCamera"
camera.rotation_euler = (1.0, 0, 0.785)  # 45-degree isometric view
scene.camera = camera

# Set camera to orthographic for architectural view
camera.data.type = 'ORTHO'
camera.data.ortho_scale = max(building_width, building_length) * 1.2

# Set output paths
output_dir = "{self.temp_dir.replace(chr(92), '/')}"
blend_file = f"{{output_dir}}/floor_plan_{self.scene_id}.blend"
obj_file = f"{{output_dir}}/floor_plan_{self.scene_id}.obj"
render_file = f"{{output_dir}}/floor_plan_{self.scene_id}.png"

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=blend_file)
print(f"BLEND_FILE: {{blend_file}}")

# Export OBJ with materials using legacy exporter for better MTL support
try:
    # Try new exporter first
    bpy.ops.wm.obj_export(filepath=obj_file, check_existing=False, export_selected_objects=False, export_materials=True)
    print(f"OBJ_FILE: {{obj_file}}")
    
    # Check if MTL was created
    mtl_file = obj_file.replace('.obj', '.mtl')
    if not bpy.path.exists(mtl_file):
        print(f"MTL file not created by new exporter, trying legacy exporter...")
        # Try legacy exporter
        bpy.ops.export_scene.obj(filepath=obj_file, check_existing=False, use_selection=False, use_materials=True)
        print(f"OBJ_FILE (legacy): {{obj_file}}")
        if bpy.path.exists(mtl_file):
            print(f"MTL_FILE: {{mtl_file}}")
    else:
        print(f"MTL_FILE: {{mtl_file}}")
        
except Exception as e:
    print(f"Export error: {{e}}")
    # Fallback to legacy exporter
    bpy.ops.export_scene.obj(filepath=obj_file, check_existing=False, use_selection=False, use_materials=True)
    print(f"OBJ_FILE (fallback): {{obj_file}}")
    mtl_file = obj_file.replace('.obj', '.mtl')
    if bpy.path.exists(mtl_file):
        print(f"MTL_FILE: {{mtl_file}}")

# Render floor plan
scene.render.filepath = render_file
bpy.ops.render.render(write_still=True)
print(f"RENDER_PNG: {{render_file}}")

print(f"SCENE_ID: {self.scene_id}")
print(f"LAYOUT_TYPE: floor_plan")
print(f"STYLE: {architectural_style}")
print(f"QUALITY_LEVEL: architectural")
print("SUCCESS: 3D floor plan created successfully")
'''
        
        # Write script
        script_path = os.path.join(self.temp_dir, f'floor_plan_{self.scene_id}.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        print(f"Floor plan Blender script written to: {script_path}")
        
        # Run Blender
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print("✅ 3D floor plan created successfully")
                print("Blender render output:")
                print(result.stdout)
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
        print("Usage: python floor_plan_renderer.py <config_file>")
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
    
    renderer = FloorPlanRenderer()
    output = renderer.render_floor_plan(config)
    print(output)

if __name__ == "__main__":
    main()
