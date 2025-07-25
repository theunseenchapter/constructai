#!/usr/bin/env python3
"""
Professional Home Renderer with Interior Details and Realistic Architecture
Creates detailed, realistic homes with proper proportions, interiors, and materials
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

class ProfessionalHomeRenderer:
    """Professional home renderer with detailed interiors and realistic architecture"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_professional_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        self.layout_generator = AdvancedLayoutGenerator()
    
    def render_professional_home(self, boq_config):
        """Render a professional, detailed home with interiors"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 40, "total_length": 30, "height": 12})
        enhanced_features = boq_config.get('enhanced_features', {})
        architectural_style = boq_config.get('architectural_style', 'modern')
        quality_level = boq_config.get('quality_level', 'professional')
        
        print(f"Creating professional home: {self.scene_id}")
        print(f"Rooms to generate: {len(rooms)}")
        print(f"Building dimensions: {building_dims}")
        print(f"Architectural style: {architectural_style}")
        print(f"Quality level: {quality_level}")
        
        # Generate advanced layout
        layout_positions = self.layout_generator.generate_layout(rooms, building_dims)
        
        # Create professional Blender script with detailed interiors
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

print("Configuring GPU for professional rendering...")
for i, device in enumerate(cprefs.devices):
    if device.type in ['OPTIX', 'CUDA']:
        device.use = True
        print(f"ENABLED GPU {{i}}: {{device.name}} ({{device.type}})")
    else:
        device.use = False

scene.cycles.device = 'GPU'
scene.cycles.samples = 512  # High quality
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'
scene.render.resolution_x = 2048
scene.render.resolution_y = 1536

# Professional material creation
def create_realistic_material(name, base_color, roughness=0.5, metallic=0.0, normal_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    
    # Add texture variation
    if normal_strength > 0:
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.inputs["Scale"].default_value = 15.0
        
        bump = nodes.new(type='ShaderNodeBump')
        bump.inputs["Strength"].default_value = normal_strength
        
        mat.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
        mat.node_tree.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat

# Create realistic materials
materials = {{
    'exterior_wall': create_realistic_material("Exterior Wall", (0.85, 0.80, 0.75), 0.7, 0.0, 0.5),
    'interior_wall': create_realistic_material("Interior Wall", (0.95, 0.93, 0.90), 0.8, 0.0, 0.1),
    'hardwood_floor': create_realistic_material("Hardwood Floor", (0.55, 0.35, 0.20), 0.3, 0.0, 0.6),
    'tile_floor': create_realistic_material("Tile Floor", (0.90, 0.88, 0.85), 0.1, 0.0, 0.3),
    'carpet': create_realistic_material("Carpet", (0.65, 0.60, 0.55), 0.9, 0.0, 0.8),
    'ceiling': create_realistic_material("Ceiling", (0.98, 0.98, 0.98), 0.6, 0.0, 0.1),
    'roof': create_realistic_material("Roof", (0.35, 0.25, 0.20), 0.4, 0.0, 0.7),
    'window_frame': create_realistic_material("Window Frame", (0.95, 0.95, 0.95), 0.2, 0.0, 0.0),
    'door_wood': create_realistic_material("Door Wood", (0.45, 0.30, 0.20), 0.3, 0.0, 0.4),
    'furniture_wood': create_realistic_material("Furniture Wood", (0.50, 0.30, 0.15), 0.25, 0.0, 0.3),
    'furniture_fabric': create_realistic_material("Furniture Fabric", (0.40, 0.50, 0.70), 0.8, 0.0, 0.6),
    'countertop': create_realistic_material("Countertop", (0.25, 0.25, 0.30), 0.1, 0.0, 0.2),
    'appliance': create_realistic_material("Appliance", (0.85, 0.85, 0.85), 0.15, 0.8, 0.0),
}}

# Glass material for windows
glass_mat = bpy.data.materials.new(name="Glass")
glass_mat.use_nodes = True
glass_nodes = glass_mat.node_tree.nodes
glass_nodes.clear()
glass_bsdf = glass_nodes.new(type='ShaderNodeBsdfPrincipled')
glass_bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.98, 1.0)
glass_bsdf.inputs["Roughness"].default_value = 0.0
glass_bsdf.inputs["Metallic"].default_value = 0.0
if "Transmission" in glass_bsdf.inputs:
    glass_bsdf.inputs["Transmission"].default_value = 0.95
glass_bsdf.inputs["IOR"].default_value = 1.45
glass_output = glass_nodes.new(type='ShaderNodeOutputMaterial')
glass_mat.node_tree.links.new(glass_bsdf.outputs["BSDF"], glass_output.inputs["Surface"])
materials['glass'] = glass_mat

def create_window(x, y, z, width, height, wall_thickness):
    """Create a realistic window with frame and glass"""
    # Window frame
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    frame = bpy.context.active_object
    frame.name = "WindowFrame"
    frame.scale = (width + 0.2, wall_thickness + 0.1, height + 0.2)
    frame.data.materials.append(materials['window_frame'])
    
    # Glass pane
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    glass = bpy.context.active_object
    glass.name = "WindowGlass"
    glass.scale = (width - 0.1, wall_thickness * 0.3, height - 0.1)
    glass.data.materials.append(materials['glass'])
    
    return [frame, glass]

def create_door(x, y, z, width, height, wall_thickness):
    """Create a realistic door"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    door = bpy.context.active_object
    door.name = "Door"
    door.scale = (width, wall_thickness * 0.5, height)
    door.data.materials.append(materials['door_wood'])
    
    # Door handle
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x + width * 0.4, y, z - height * 0.1))
    handle = bpy.context.active_object
    handle.name = "DoorHandle"
    handle.data.materials.append(materials['appliance'])
    
    return [door, handle]

def create_kitchen_furniture(room_x, room_y, room_width, room_length, room_height):
    """Create detailed kitchen furniture"""
    furniture = []
    
    # Kitchen cabinets along one wall
    cabinet_height = 0.9
    cabinet_depth = 0.6
    num_cabinets = int(room_width / 1.5)
    
    for i in range(num_cabinets):
        cabinet_x = room_x - room_width/2 + (i + 0.5) * (room_width / num_cabinets)
        cabinet_y = room_y - room_length/2 + cabinet_depth/2
        
        # Lower cabinet
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cabinet_x, cabinet_y, cabinet_height/2))
        cabinet = bpy.context.active_object
        cabinet.name = f"KitchenCabinet_{{i}}"
        cabinet.scale = (room_width / num_cabinets - 0.1, cabinet_depth, cabinet_height)
        cabinet.data.materials.append(materials['furniture_wood'])
        furniture.append(cabinet)
        
        # Countertop
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cabinet_x, cabinet_y, cabinet_height + 0.05))
        counter = bpy.context.active_object
        counter.name = f"Countertop_{{i}}"
        counter.scale = (room_width / num_cabinets - 0.05, cabinet_depth + 0.1, 0.1)
        counter.data.materials.append(materials['countertop'])
        furniture.append(counter)
        
        # Upper cabinet
        bpy.ops.mesh.primitive_cube_add(size=1, location=(cabinet_x, cabinet_y, cabinet_height + 1.5))
        upper_cabinet = bpy.context.active_object
        upper_cabinet.name = f"UpperCabinet_{{i}}"
        upper_cabinet.scale = (room_width / num_cabinets - 0.1, cabinet_depth * 0.7, 0.8)
        upper_cabinet.data.materials.append(materials['furniture_wood'])
        furniture.append(upper_cabinet)
    
    # Kitchen island
    if room_width > 4 and room_length > 4:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y, cabinet_height/2))
        island = bpy.context.active_object
        island.name = "KitchenIsland"
        island.scale = (2.5, 1.2, cabinet_height)
        island.data.materials.append(materials['furniture_wood'])
        furniture.append(island)
        
        # Island countertop
        bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y, cabinet_height + 0.05))
        island_counter = bpy.context.active_object
        island_counter.name = "IslandCountertop"
        island_counter.scale = (2.6, 1.3, 0.1)
        island_counter.data.materials.append(materials['countertop'])
        furniture.append(island_counter)
    
    # Refrigerator
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x + room_width/2 - 0.4, room_y - room_length/2 + 0.4, 1.0))
    fridge = bpy.context.active_object
    fridge.name = "Refrigerator"
    fridge.scale = (0.7, 0.7, 2.0)
    fridge.data.materials.append(materials['appliance'])
    furniture.append(fridge)
    
    return furniture

def create_living_room_furniture(room_x, room_y, room_width, room_length, room_height):
    """Create detailed living room furniture"""
    furniture = []
    
    # Sofa
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y - room_length/4, 0.4))
    sofa = bpy.context.active_object
    sofa.name = "Sofa"
    sofa.scale = (2.5, 1.0, 0.8)
    sofa.data.materials.append(materials['furniture_fabric'])
    furniture.append(sofa)
    
    # Coffee table
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y + room_length/6, 0.25))
    coffee_table = bpy.context.active_object
    coffee_table.name = "CoffeeTable"
    coffee_table.scale = (1.5, 0.8, 0.5)
    coffee_table.data.materials.append(materials['furniture_wood'])
    furniture.append(coffee_table)
    
    # TV stand
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y + room_length/2 - 0.3, 0.3))
    tv_stand = bpy.context.active_object
    tv_stand.name = "TVStand"
    tv_stand.scale = (2.0, 0.5, 0.6)
    tv_stand.data.materials.append(materials['furniture_wood'])
    furniture.append(tv_stand)
    
    # TV
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y + room_length/2 - 0.15, 0.8))
    tv = bpy.context.active_object
    tv.name = "TV"
    tv.scale = (1.8, 0.1, 1.0)
    tv.data.materials.append(materials['appliance'])
    furniture.append(tv)
    
    # Armchairs
    for i, pos in enumerate([(-room_width/3, -room_length/4), (room_width/3, -room_length/4)]):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x + pos[0], room_y + pos[1], 0.4))
        chair = bpy.context.active_object
        chair.name = f"Armchair_{{i}}"
        chair.scale = (1.0, 1.0, 0.8)
        chair.data.materials.append(materials['furniture_fabric'])
        furniture.append(chair)
    
    return furniture

def create_bedroom_furniture(room_x, room_y, room_width, room_length, room_height):
    """Create detailed bedroom furniture"""
    furniture = []
    
    # Bed
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y - room_length/4, 0.3))
    bed = bpy.context.active_object
    bed.name = "Bed"
    bed.scale = (2.0, 2.2, 0.6)
    bed.data.materials.append(materials['furniture_fabric'])
    furniture.append(bed)
    
    # Headboard
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y - room_length/4 - 1.2, 0.8))
    headboard = bpy.context.active_object
    headboard.name = "Headboard"
    headboard.scale = (2.2, 0.2, 1.6)
    headboard.data.materials.append(materials['furniture_wood'])
    furniture.append(headboard)
    
    # Nightstands
    for i, side in enumerate([-1.3, 1.3]):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x + side, room_y - room_length/4, 0.3))
        nightstand = bpy.context.active_object
        nightstand.name = f"Nightstand_{{i}}"
        nightstand.scale = (0.6, 0.5, 0.6)
        nightstand.data.materials.append(materials['furniture_wood'])
        furniture.append(nightstand)
    
    # Dresser
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x + room_width/2 - 0.4, room_y + room_length/3, 0.4))
    dresser = bpy.context.active_object
    dresser.name = "Dresser"
    dresser.scale = (0.8, 1.5, 0.8)
    dresser.data.materials.append(materials['furniture_wood'])
    furniture.append(dresser)
    
    # Wardrobe
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x - room_width/2 + 0.5, room_y + room_length/3, 1.0))
    wardrobe = bpy.context.active_object
    wardrobe.name = "Wardrobe"
    wardrobe.scale = (1.0, 0.6, 2.0)
    wardrobe.data.materials.append(materials['furniture_wood'])
    furniture.append(wardrobe)
    
    return furniture

def create_bathroom_furniture(room_x, room_y, room_width, room_length, room_height):
    """Create detailed bathroom fixtures"""
    furniture = []
    
    # Toilet
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x + room_width/3, room_y + room_length/3, 0.2))
    toilet = bpy.context.active_object
    toilet.name = "Toilet"
    toilet.scale = (0.4, 0.7, 0.4)
    toilet.data.materials.append(materials['appliance'])
    furniture.append(toilet)
    
    # Sink with vanity
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x - room_width/3, room_y + room_length/3, 0.4))
    vanity = bpy.context.active_object
    vanity.name = "Vanity"
    vanity.scale = (1.2, 0.6, 0.8)
    vanity.data.materials.append(materials['furniture_wood'])
    furniture.append(vanity)
    
    # Sink
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x - room_width/3, room_y + room_length/3, 0.82))
    sink = bpy.context.active_object
    sink.name = "Sink"
    sink.scale = (0.6, 0.4, 0.15)
    sink.data.materials.append(materials['appliance'])
    furniture.append(sink)
    
    # Bathtub
    bpy.ops.mesh.primitive_cube_add(size=1, location=(room_x, room_y - room_length/3, 0.3))
    bathtub = bpy.context.active_object
    bathtub.name = "Bathtub"
    bathtub.scale = (1.8, 0.8, 0.6)
    bathtub.data.materials.append(materials['appliance'])
    furniture.append(bathtub)
    
    return furniture

# Create rooms with interiors
layout_positions = {json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

for room_data in layout_positions:
    room = room_data['room']
    x = room_data['x']
    y = room_data['y']
    width = room_data['width']
    length = room_data['length']
    height = room.get('height', 3.0)
    room_type = room.get('type', 'general')
    
    print(f"Creating detailed room: {{room['name']}} ({{room_type}}) at ({{x}}, {{y}})")
    
    # Determine floor material based on room type
    if room_type in ['kitchen', 'bathroom']:
        floor_material = materials['tile_floor']
    elif room_type in ['bedroom', 'living']:
        floor_material = materials['hardwood_floor'] if random.random() > 0.3 else materials['carpet']
    else:
        floor_material = materials['hardwood_floor']
    
    # Floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room['name']}}"
    floor.scale = (width/2, length/2, 1)
    floor.data.materials.append(floor_material)
    
    # Ceiling
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, height))
    ceiling = bpy.context.active_object
    ceiling.name = f"Ceiling_{{room['name']}}"
    ceiling.scale = (width/2, length/2, 1)
    ceiling.data.materials.append(materials['ceiling'])
    
    # Walls with proper thickness
    wall_thickness = 0.2
    wall_height = height
    
    # Create walls with openings for doors and windows
    wall_positions = [
        (x - width/2, y, wall_height/2, wall_thickness, length, wall_height, 'left'),
        (x + width/2, y, wall_height/2, wall_thickness, length, wall_height, 'right'),
        (x, y - length/2, wall_height/2, width, wall_thickness, wall_height, 'front'),
        (x, y + length/2, wall_height/2, width, wall_thickness, wall_height, 'back'),
    ]
    
    for i, (wx, wy, wz, w_width, w_length, w_height, wall_side) in enumerate(wall_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz))
        wall = bpy.context.active_object
        wall.name = f"Wall_{{room['name']}}_{{wall_side}}"
        wall.scale = (w_width, w_length, w_height/2)
        wall.data.materials.append(materials['interior_wall'])
        
        # Add windows to exterior walls (randomly)
        if wall_side in ['front', 'back'] and random.random() > 0.5:
            window_x = wx + random.uniform(-w_width/3, w_width/3)
            window_y = wy
            window_z = wz + wall_height/4
            windows = create_window(window_x, window_y, window_z, 1.2, 1.5, wall_thickness)
    
    # Add doors between rooms (simplified for now)
    if room_type != 'bathroom':  # Main rooms get doors
        door_x = x + width/2
        door_y = y
        door_z = height/2
        doors = create_door(door_x, door_y, door_z, 0.9, 2.1, wall_thickness)
    
    # Add furniture based on room type
    furniture = []
    if room_type == 'kitchen':
        furniture = create_kitchen_furniture(x, y, width, length, height)
    elif room_type == 'living':
        furniture = create_living_room_furniture(x, y, width, length, height)
    elif room_type == 'bedroom':
        furniture = create_bedroom_furniture(x, y, width, length, height)
    elif room_type == 'bathroom':
        furniture = create_bathroom_furniture(x, y, width, length, height)

# Add exterior walls and roof
building_width = {building_dims['total_width']}
building_length = {building_dims['total_length']}
building_height = {building_dims['height']}

# Exterior walls
exterior_wall_thickness = 0.3
exterior_positions = [
    (-building_width/2, 0, building_height/2, exterior_wall_thickness, building_length + exterior_wall_thickness, building_height),
    (building_width/2, 0, building_height/2, exterior_wall_thickness, building_length + exterior_wall_thickness, building_height),
    (0, -building_length/2, building_height/2, building_width + exterior_wall_thickness, exterior_wall_thickness, building_height),
    (0, building_length/2, building_height/2, building_width + exterior_wall_thickness, exterior_wall_thickness, building_height),
]

for i, (x, y, z, w, l, h) in enumerate(exterior_positions):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    ext_wall = bpy.context.active_object
    ext_wall.name = f"ExteriorWall_{{i}}"
    ext_wall.scale = (w, l, h/2)
    ext_wall.data.materials.append(materials['exterior_wall'])

# Roof
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, building_height + 0.2))
roof = bpy.context.active_object
roof.name = "Roof"
roof.scale = (building_width + 1, building_length + 1, 0.4)
roof.data.materials.append(materials['roof'])

# Professional lighting setup
# Sun light
bpy.ops.object.light_add(type='SUN', location=(20, -20, 30))
sun = bpy.context.active_object
sun.name = "SunLight"
sun.data.energy = 3.0
sun.rotation_euler = (0.785, 0, 0.785)

# Area lights for interior
interior_lights = [
    (0, 0, building_height - 0.5, 200),  # Main ceiling light
    (-building_width/4, -building_length/4, building_height - 0.5, 100),  # Room light 1
    (building_width/4, building_length/4, building_height - 0.5, 100),   # Room light 2
]

for i, (lx, ly, lz, energy) in enumerate(interior_lights):
    bpy.ops.object.light_add(type='AREA', location=(lx, ly, lz))
    area_light = bpy.context.active_object
    area_light.name = f"InteriorLight_{{i}}"
    area_light.data.energy = energy
    area_light.data.size = 2.0

# Professional camera setup
bpy.ops.object.camera_add(location=(building_width * 0.8, -building_length * 0.8, building_height * 0.6))
camera = bpy.context.active_object
camera.name = "MainCamera"
camera.rotation_euler = (1.0, 0, 0.785)
scene.camera = camera

# Enable depth of field for cinematic look
camera.data.dof.use_dof = True
camera.data.dof.aperture_fstop = 2.8
camera.data.lens = 35

# Set output paths
output_dir = "{self.temp_dir.replace(chr(92), '/')}"
blend_file = f"{{output_dir}}/professional_home_{self.scene_id}.blend"
obj_file = f"{{output_dir}}/professional_home_{self.scene_id}.obj"
render_file = f"{{output_dir}}/professional_home_{self.scene_id}.png"

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=blend_file)
print(f"BLEND_FILE: {{blend_file}}")

# Export OBJ with materials
bpy.ops.wm.obj_export(filepath=obj_file, check_existing=False, export_selected_objects=False, export_materials=True)
print(f"OBJ_FILE: {{obj_file}}")

# Render high-quality image
scene.render.filepath = render_file
bpy.ops.render.render(write_still=True)
print(f"RENDER_PNG: {{render_file}}")

print(f"SCENE_ID: {self.scene_id}")
print(f"LAYOUT_TYPE: professional")
print(f"STYLE: {architectural_style}")
print(f"QUALITY_LEVEL: professional")
print("SUCCESS: Professional home created successfully")
'''
        
        # Write script
        script_path = os.path.join(self.temp_dir, f'professional_home_{self.scene_id}.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        print(f"Professional Blender script written to: {script_path}")
        
        # Run Blender
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print("✅ Professional home created successfully")
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
        print("Usage: python professional_home_renderer.py <config_file>")
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
    
    renderer = ProfessionalHomeRenderer()
    output = renderer.render_professional_home(config)
    print(output)

if __name__ == "__main__":
    main()
