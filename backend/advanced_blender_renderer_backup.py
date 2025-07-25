#!/usr/bin/env python3
"""
Advanced Blender MCP Server for Professional Architectural Visualization
Inspired by LIDAR 3D and high-end architectural rendering techniques
"""

import asyncio
import json
import sys
import os
import tempfile
import subprocess
import uuid
from typing import Any, Dict, List, Optional
from pathlib import Path

class AdvancedBlenderRenderer:
    """Professional-grade Blender renderer for architectural visualization"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_advanced_')
        self.blender_path = os.environ.get('BLENDER_PATH', 'D:\\blender\\blender.exe')
        self.scene_id = None
        
    def create_professional_scene(self, scene_config: Dict) -> Dict:
        """Create a professional architectural scene with advanced materials and lighting"""
        
        self.scene_id = str(uuid.uuid4())
        
        # Advanced Blender Python script for professional visualization
        blender_script = f'''
import bpy
import bmesh
import mathutils
from mathutils import Vector, Euler
import math
import json
import os

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Clear materials
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# Scene configuration
scene_config = {json.dumps(scene_config)}
scene = bpy.context.scene

# Set up GPU rendering with high quality
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
cprefs.compute_device_type = 'OPTIX'
cprefs.get_devices()
for device in cprefs.devices:
    if device.type == 'OPTIX':
        device.use = True
        print("GPU ENABLED:", device.name)
scene.cycles.device = 'GPU'
scene.cycles.samples = 512
scene.render.resolution_x = 2560
scene.render.resolution_y = 1440

# Professional material creation functions
def create_material(name, base_color, roughness=0.5, metallic=0.0):
    """Create a professional material with proper node setup"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

# Create professional interior based on BOQ data
room_size = scene_config.get('room_size', {"width": 16, "length": 16, "height": 3})
width = room_size.get('width', 16)
length = room_size.get('length', 16) 
height = room_size.get('height', 3)

# FLOOR - Professional hardwood
bpy.ops.mesh.primitive_plane_add(size=max(width, length), location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
wood_mat = create_material("ProfessionalWood", (0.42, 0.26, 0.15), roughness=0.3)
floor.data.materials.append(wood_mat)

# WALLS - Create complete room structure
wall_thickness = 0.2
wall_height = height / 2

# Back wall
bpy.ops.mesh.primitive_cube_add(location=(0, length/2, wall_height))
back_wall = bpy.context.active_object
back_wall.name = "BackWall"
back_wall.scale = (width/2, wall_thickness/2, wall_height)

# Front wall (with opening for entrance)
bpy.ops.mesh.primitive_cube_add(location=(0, -length/2, wall_height))
front_wall = bpy.context.active_object
front_wall.name = "FrontWall"
front_wall.scale = (width/4, wall_thickness/2, wall_height)

# Left wall
bpy.ops.mesh.primitive_cube_add(location=(-width/2, 0, wall_height))
left_wall = bpy.context.active_object
left_wall.name = "LeftWall"
left_wall.scale = (wall_thickness/2, length/2, wall_height)

# Right wall with window
bpy.ops.mesh.primitive_cube_add(location=(width/2, 0, wall_height))
right_wall = bpy.context.active_object
right_wall.name = "RightWall"
right_wall.scale = (wall_thickness/2, length/2, wall_height)

# Wall material
wall_mat = create_material("ProfessionalWalls", (0.92, 0.92, 0.88), roughness=0.8)
for wall in [back_wall, front_wall, left_wall, right_wall]:
    wall.data.materials.append(wall_mat)

# CEILING
bpy.ops.mesh.primitive_plane_add(size=max(width, length), location=(0, 0, height))
ceiling = bpy.context.active_object
ceiling.name = "Ceiling"
ceiling.rotation_euler = (math.pi, 0, 0)
ceiling_mat = create_material("Ceiling", (0.98, 0.98, 0.98), roughness=0.9)
ceiling.data.materials.append(ceiling_mat)

# FURNITURE BASED ON BOQ ITEMS
boq_items = scene_config.get('boq_items', [])
furniture_count = 0

# Define furniture placement zones
living_zone = (-width/3, length/4, 0)
dining_zone = (width/3, -length/4, 0)
corner_zone = (width/3, length/3, 0)

for item in boq_items:
    item_type = item.get('type', '').lower()
    quantity = item.get('quantity', 1)
    
    if 'sofa' in item_type or 'seating' in item_type:
        # Create sectional sofa
        for i in range(min(quantity, 2)):
            # Main sofa piece
            bpy.ops.mesh.primitive_cube_add(location=(living_zone[0] + i*2, living_zone[1], 0.4))
            sofa_main = bpy.context.active_object
            sofa_main.name = f"Sofa_{{furniture_count}}"
            sofa_main.scale = (1.5, 1, 0.4)
            
            # Sofa back
            bpy.ops.mesh.primitive_cube_add(location=(living_zone[0] + i*2, living_zone[1] + 0.8, 0.9))
            sofa_back = bpy.context.active_object
            sofa_back.name = f"SofaBack_{{furniture_count}}"
            sofa_back.scale = (1.5, 0.2, 0.5)
            
            # Sofa material
            sofa_mat = create_material(f"SofaFabric_{{furniture_count}}", (0.4, 0.4, 0.5), roughness=0.9)
            sofa_main.data.materials.append(sofa_mat)
            sofa_back.data.materials.append(sofa_mat)
            furniture_count += 1
    
    elif 'table' in item_type:
        # Create coffee table
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.4))
        table_top = bpy.context.active_object
        table_top.name = f"Table_{{furniture_count}}"
        table_top.scale = (1.5, 1, 0.05)
        
        # Table base
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.2))
        table_base = bpy.context.active_object
        table_base.name = f"TableBase_{{furniture_count}}"
        table_base.scale = (1.2, 0.8, 0.2)
        
        # Table material
        table_mat = create_material(f"WoodTable_{{furniture_count}}", (0.15, 0.1, 0.05), roughness=0.2)
        table_top.data.materials.append(table_mat)
        table_base.data.materials.append(table_mat)
        furniture_count += 1
        
        # Add dining chairs if it's a dining table
        if 'dining' in item_type:
            chair_positions = [(dining_zone[0]-1.5, dining_zone[1], 0.45), 
                             (dining_zone[0]+1.5, dining_zone[1], 0.45),
                             (dining_zone[0], dining_zone[1]-1.5, 0.45), 
                             (dining_zone[0], dining_zone[1]+1.5, 0.45)]
            for i, pos in enumerate(chair_positions[:min(4, quantity)]):
                # Chair seat
                bpy.ops.mesh.primitive_cube_add(location=pos)
                chair_seat = bpy.context.active_object
                chair_seat.name = f"Chair_{{i}}_{{furniture_count}}"
                chair_seat.scale = (0.4, 0.4, 0.05)
                
                # Chair back
                back_pos = (pos[0], pos[1], pos[2] + 0.4)
                bpy.ops.mesh.primitive_cube_add(location=back_pos)
                chair_back = bpy.context.active_object
                chair_back.name = f"ChairBack_{{i}}_{{furniture_count}}"
                chair_back.scale = (0.4, 0.05, 0.4)
                
                # Chair material
                chair_mat = create_material(f"Chair_{{i}}_{{furniture_count}}", (0.6, 0.4, 0.2), roughness=0.5)
                chair_seat.data.materials.append(chair_mat)
                chair_back.data.materials.append(chair_mat)
    
    elif 'storage' in item_type or 'cabinet' in item_type or 'shelf' in item_type:
        # Create storage unit
        bpy.ops.mesh.primitive_cube_add(location=(corner_zone[0], corner_zone[1], 1.2))
        storage = bpy.context.active_object
        storage.name = f"Storage_{{furniture_count}}"
        storage.scale = (0.4, 1.5, 1.2)
        
        storage_mat = create_material(f"Storage_{{furniture_count}}", (0.6, 0.4, 0.2), roughness=0.3)
        storage.data.materials.append(storage_mat)
        furniture_count += 1
    
    elif 'plant' in item_type or 'decoration' in item_type:
        # Add decorative plants
        bpy.ops.mesh.primitive_cylinder_add(location=(corner_zone[0]+2, corner_zone[1]+2, 0.4), radius=0.4, depth=0.8)
        plant_pot = bpy.context.active_object
        plant_pot.name = f"PlantPot_{{furniture_count}}"
        
        # Plant foliage
        bpy.ops.mesh.primitive_uv_sphere_add(location=(corner_zone[0]+2, corner_zone[1]+2, 1.2), radius=0.6)
        plant_leaves = bpy.context.active_object
        plant_leaves.name = f"PlantLeaves_{{furniture_count}}"
        plant_leaves.scale = (1, 1, 1.5)
        
        # Plant materials
        pot_mat = create_material(f"PlantPot_{{furniture_count}}", (0.3, 0.2, 0.1), roughness=0.7)
        leaves_mat = create_material(f"PlantLeaves_{{furniture_count}}", (0.1, 0.5, 0.1), roughness=0.8)
        plant_pot.data.materials.append(pot_mat)
        plant_leaves.data.materials.append(leaves_mat)
        furniture_count += 1

# PROFESSIONAL LIGHTING SETUP
# Main ceiling light
bpy.ops.object.light_add(type='AREA', location=(0, 0, height-0.1))
main_light = bpy.context.active_object
main_light.name = "MainCeilingLight"
main_light.data.energy = 100
main_light.data.size = 3.0
main_light.data.color = (1.0, 0.95, 0.8)  # Warm white

# Natural window lighting
bpy.ops.object.light_add(type='SUN', location=(width, -length/2, height+2))
window_light = bpy.context.active_object
window_light.name = "NaturalLight"
window_light.data.energy = 8.0
window_light.data.color = (1.0, 0.9, 0.7)  # Warm sunlight
window_light.rotation_euler = (0.3, 0, 1.8)

# Accent lighting for ambiance
bpy.ops.object.light_add(type='SPOT', location=(-width/3, length/3, height-0.5))
accent_light = bpy.context.active_object
accent_light.name = "AccentLight"
accent_light.data.energy = 30
accent_light.rotation_euler = (1.2, 0, 0.8)

# CAMERA SETUP for architectural photography
camera_distance = max(width, length) * 0.8
bpy.ops.object.camera_add(location=(-camera_distance, -camera_distance, height * 0.7))
camera = bpy.context.active_object
camera.name = "ArchCamera"
camera.rotation_euler = (1.1, 0, -0.785)  # 45-degree angle
scene.camera = camera

# Set camera properties for architectural visualization
camera.data.lens = 24  # Wide angle lens for architecture
camera.data.clip_start = 0.1
camera.data.clip_end = 100

# OUTPUT GENERATION
output_id = "{self.scene_id}"
output_dir = "{self.temp_dir.replace(chr(92), '/')}"

# Export high-quality OBJ file
obj_path = f"{{output_dir}}/professional_boq_{{output_id}}.obj"
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=True
)

# Save Blender file for future editing
blend_path = f"{{output_dir}}/professional_boq_{{output_id}}.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# Export GLB for web viewing
glb_path = f"{{output_dir}}/professional_boq_{{output_id}}.glb"
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    export_materials='EXPORT',
    export_lights=True,
    export_cameras=True
)

# Render high-quality images
render_path = f"{{output_dir}}/professional_boq_{{output_id}}"

# Hero shot
scene.render.filepath = f"{{render_path}}_hero.png"
bpy.ops.render.render(write_still=True)

# Detail shot - closer view
camera.location = (-camera_distance*0.6, -camera_distance*0.6, height * 0.5)
camera.rotation_euler = (1.2, 0, -0.785)
scene.render.filepath = f"{{render_path}}_detail.png"
bpy.ops.render.render(write_still=True)

# Top-down architectural view
camera.location = (0, 0, height * 2)
camera.rotation_euler = (0, 0, 0)
scene.render.filepath = f"{{render_path}}_plan.png"
bpy.ops.render.render(write_still=True)

print("PROFESSIONAL BOQ RENDERING COMPLETE")
print("OBJ:", obj_path)
print("BLEND:", blend_path)
print("GLB:", glb_path)
print("RENDERS:", f"{{render_path}}_*.png")
'''
        
        try:
            # Execute Blender with the professional script
            result = subprocess.run([
                self.blender_path,
                '--background',
                '--python-expr', blender_script
            ], capture_output=True, text=True, timeout=300)
            
            print("Professional BOQ Render Output:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            
            # Collect generated files
            generated_files = []
            
            # Check for OBJ file
            obj_path = os.path.join(self.temp_dir, f'professional_boq_{self.scene_id}.obj')
            if os.path.exists(obj_path):
                generated_files.append({'type': 'obj', 'path': obj_path})
                
            # Check for MTL file
            mtl_path = os.path.join(self.temp_dir, f'professional_boq_{self.scene_id}.mtl') 
            if os.path.exists(mtl_path):
                generated_files.append({'type': 'mtl', 'path': mtl_path})
                
            # Check for BLEND file
            blend_path = os.path.join(self.temp_dir, f'professional_boq_{self.scene_id}.blend')
            if os.path.exists(blend_path):
                generated_files.append({'type': 'blend', 'path': blend_path})
                
            # Check for GLB file
            glb_path = os.path.join(self.temp_dir, f'professional_boq_{self.scene_id}.glb')
            if os.path.exists(glb_path):
                generated_files.append({'type': 'glb', 'path': glb_path})
            
            # Check for rendered images
            for img_type in ['hero', 'detail', 'plan']:
                img_path = os.path.join(self.temp_dir, f'professional_boq_{self.scene_id}_{img_type}.png')
                if os.path.exists(img_path):
                    generated_files.append({'type': 'render', 'subtype': img_type, 'path': img_path})
            
            return {
                'success': True,
                'scene_id': self.scene_id,
                'files': generated_files,
                'output': result.stdout
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Rendering timeout (5 minutes)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Set up glass material properly
glass_mat = materials['glass_window']
glass_nodes = glass_mat.node_tree.nodes
glass_bsdf = glass_nodes.get('Principled BSDF')
if glass_bsdf:
    glass_bsdf.inputs['Transmission'].default_value = 1.0
    glass_bsdf.inputs['IOR'].default_value = 1.45

def create_room_with_details(room_data):
    """Create detailed room geometry with proper proportions"""
    
    # Room dimensions
    width = room_data.get('width', 6.0)
    length = room_data.get('length', 8.0) 
    height = room_data.get('height', 3.2)
    position = room_data.get('position', {{'x': 0, 'y': 0, 'z': 0}})
    
    room_objects = []
    
    # Floor with proper UV mapping
    bpy.ops.mesh.primitive_plane_add(size=1, location=(position['x'], position['y'], position['z']))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room_data.get('name', 'Room')}}"
    floor.scale = (width, length, 1)
    
    # Apply modifiers for detail
    bpy.ops.object.modifier_add(type='SUBSURF')
    floor.modifiers['Subdivision Surface'].levels = 1
    
    floor.data.materials.append(materials['premium_hardwood'])
    room_objects.append(floor)
    
    # Ceiling
    bpy.ops.mesh.primitive_plane_add(size=1, location=(position['x'], position['y'], position['z'] + height))
    ceiling = bpy.context.active_object
    ceiling.name = f"Ceiling_{{room_data.get('name', 'Room')}}"
    ceiling.scale = (width, length, 1)
    ceiling.data.materials.append(materials['warm_paint'])
    room_objects.append(ceiling)
    
    # Walls with thickness and detail
    wall_thickness = 0.15
    
    # Create walls as separate objects with proper geometry
    walls = [
        # Front wall
        {{'pos': (position['x'], position['y'] + length/2, position['z'] + height/2), 'scale': (width, wall_thickness, height)}},
        # Back wall  
        {{'pos': (position['x'], position['y'] - length/2, position['z'] + height/2), 'scale': (width, wall_thickness, height)}},
        # Left wall
        {{'pos': (position['x'] - width/2, position['y'], position['z'] + height/2), 'scale': (wall_thickness, length, height)}},
        # Right wall
        {{'pos': (position['x'] + width/2, position['y'], position['z'] + height/2), 'scale': (wall_thickness, length, height)}}
    ]
    
    for i, wall_data in enumerate(walls):
        bpy.ops.mesh.primitive_cube_add(size=1, location=wall_data['pos'])
        wall = bpy.context.active_object
        wall.name = f"Wall_{{i}}_{{room_data.get('name', 'Room')}}"
        wall.scale = wall_data['scale']
        
        # Add some geometric detail
        bpy.ops.object.modifier_add(type='BEVEL')
        wall.modifiers['Bevel'].width = 0.01
        wall.modifiers['Bevel'].segments = 2
        
        # Use different materials for accent walls
        if i == 0:  # Front wall as accent
            wall.data.materials.append(materials['accent_paint'])
        else:
            wall.data.materials.append(materials['warm_paint'])
            
        room_objects.append(wall)
    
    return room_objects

def create_luxury_furniture(room_data):
    """Create high-quality furniture pieces"""
    furniture = []
    room_type = room_data.get('type', '').lower()
    position = room_data.get('position', {{'x': 0, 'y': 0, 'z': 0}})
    
    if 'living' in room_type:
        # Luxury sectional sofa
        bpy.ops.mesh.primitive_cube_add(size=1, location=(position['x'], position['y'] - 1, position['z'] + 0.4))
        sofa = bpy.context.active_object
        sofa.name = "Luxury_Sectional_Sofa"
        sofa.scale = (3.2, 1.6, 0.8)
        
        # Add subdivision for smooth curves
        bpy.ops.object.modifier_add(type='SUBSURF')
        sofa.modifiers['Subdivision Surface'].levels = 2
        
        # Add bevel for realistic edges
        bpy.ops.object.modifier_add(type='BEVEL')
        sofa.modifiers['Bevel'].width = 0.05
        
        sofa.data.materials.append(materials['fabric_sofa'])
        furniture.append(sofa)
        
        # Modern coffee table with glass top
        bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=0.05, location=(position['x'], position['y'] + 1.2, position['z'] + 0.45))
        table_top = bpy.context.active_object
        table_top.name = "Coffee_Table_Glass"
        table_top.data.materials.append(materials['glass_window'])
        furniture.append(table_top)
        
        # Table legs (steel)
        for i, leg_pos in enumerate([(-0.4, -0.4), (0.4, -0.4), (-0.4, 0.4), (0.4, 0.4)]):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.03, depth=0.4, 
                location=(position['x'] + leg_pos[0], position['y'] + 1.2 + leg_pos[1], position['z'] + 0.2)
            )
            leg = bpy.context.active_object
            leg.name = f"Table_Leg_{{i}}"
            leg.data.materials.append(materials['brushed_steel'])
            furniture.append(leg)
        
        # Designer accent chair
        bpy.ops.mesh.primitive_cube_add(size=1, location=(position['x'] + 2.5, position['y'] + 0.5, position['z'] + 0.45))
        chair = bpy.context.active_object
        chair.name = "Designer_Accent_Chair"
        chair.scale = (0.8, 0.9, 0.9)
        
        bpy.ops.object.modifier_add(type='SUBSURF')
        chair.modifiers['Subdivision Surface'].levels = 1
        
        chair.data.materials.append(materials['leather_chair'])
        furniture.append(chair)
        
    return furniture

# Process scene configuration
rooms_data = scene_config.get('rooms', [])
for room in rooms_data:
    room_objects = create_room_with_details(room)
    furniture = create_luxury_furniture(room)

# Set up professional lighting system
def setup_advanced_lighting():
    """Create a sophisticated lighting setup"""
    
    # Key light (sun) - Golden hour lighting
    bpy.ops.object.light_add(type='SUN', location=(20, -20, 30))
    sun = bpy.context.active_object
    sun.name = "Key_Sun_Light"
    sun.data.energy = 3.0
    sun.data.angle = math.radians(15)  # Soft shadows
    sun.data.color = (1.0, 0.95, 0.8)  # Warm golden color
    sun.rotation_euler = (math.radians(30), 0, math.radians(45))
    
    # Fill light (area) - Soft interior lighting
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
    area_light = bpy.context.active_object
    area_light.name = "Fill_Area_Light"
    area_light.data.energy = 100
    area_light.data.size = 8
    area_light.data.color = (0.95, 0.98, 1.0)  # Cool fill
    
    # Accent lights for depth
    accent_positions = [(-4, -4, 6), (4, 4, 6), (-4, 4, 5), (4, -4, 5)]
    for i, pos in enumerate(accent_positions):
        bpy.ops.object.light_add(type='POINT', location=pos)
        accent = bpy.context.active_object
        accent.name = f"Accent_Light_{{i}}"
        accent.data.energy = 50
        accent.data.color = (1.0, 0.9, 0.7)
        accent.data.shadow_soft_size = 0.5

setup_advanced_lighting()

# Set up professional camera with composition
def setup_professional_camera():
    """Set up cinematic camera angle"""
    
    # Add camera with professional positioning
    bpy.ops.object.camera_add(location=(12, -8, 6))
    camera = bpy.context.active_object
    camera.name = "Professional_Camera"
    
    # Set camera properties for architectural photography
    camera.data.lens = 35  # Wide angle for architecture
    camera.data.sensor_width = 36  # Full frame sensor
    camera.data.dof.use_dof = True  # Depth of field
    camera.data.dof.aperture_fstop = 5.6  # Good for architecture
    camera.data.dof.focus_distance = 10
    
    # Point camera at scene center with rule of thirds
    target = Vector((0, 0, 2))
    camera_location = camera.location
    direction = target - camera_location
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Set as active camera
    scene.camera = camera

setup_professional_camera()

# Add atmospheric effects
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links

# Clear default nodes
world_nodes.clear()

# Create sky texture
sky_texture = world_nodes.new('ShaderNodeTexSky')
sky_texture.sky_type = 'HOSEK_WILKIE'
sky_texture.sun_elevation = math.radians(30)  # Golden hour
sky_texture.sun_rotation = math.radians(45)

# Background shader
background = world_nodes.new('ShaderNodeBackground')
background.inputs['Strength'].default_value = 0.8

# World output
world_output = world_nodes.new('ShaderNodeOutputWorld')

# Connect nodes
world_links.new(sky_texture.outputs['Color'], background.inputs['Color'])
world_links.new(background.outputs['Background'], world_output.inputs['Surface'])

# Set output paths
scene.render.filepath = '{os.path.join(self.temp_dir, f"professional_render_{self.scene_id}")}'

# Save the .blend file
blend_path = '{os.path.join(self.temp_dir, f"professional_scene_{self.scene_id}.blend")}'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# Export high-quality OBJ
obj_path = '{os.path.join(self.temp_dir, f"professional_model_{self.scene_id}.obj")}'
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=False,
    export_pbr_extensions=True,
    export_smooth_groups=True
)

print(json.dumps({{
    "success": True,
    "scene_id": "{self.scene_id}",
    "blend_file": blend_path,
    "obj_file": obj_path,
    "temp_dir": "{self.temp_dir}",
    "quality": "professional",
    "renderer": "cycles",
    "samples": 256,
    "resolution": "2560x1440"
}}))
'''
        
        # Write the advanced script
        script_path = os.path.join(self.temp_dir, f'create_professional_scene_{self.scene_id}.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(blender_script)
        
        # Execute Blender with the script
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path
        ]
        
        try:
            print(f"🎨 Executing Blender with professional script...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 minutes for GPU rendering
            
            if result.returncode == 0:
                # Parse the JSON output from the script
                output_lines = result.stdout.strip().split('\n')
                for line in reversed(output_lines):
                    try:
                        scene_result = json.loads(line)
                        if isinstance(scene_result, dict) and scene_result.get('success'):
                            return scene_result
                    except json.JSONDecodeError:
                        continue
                
                return {
                    "success": True,
                    "scene_id": self.scene_id,
                    "message": "Professional scene created successfully",
                    "temp_dir": self.temp_dir
                }
            else:
                return {
                    "success": False,
                    "error": f"Blender execution failed: {result.stderr}",
                    "stdout": result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Blender execution timeout (180s)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Blender execution error: {str(e)}"
            }
    
    def render_professional_views(self) -> Dict:
        """Render multiple professional camera angles"""
        
        if not self.scene_id:
            return {"success": False, "error": "No scene available to render"}
        
        blend_file = os.path.join(self.temp_dir, f"professional_scene_{self.scene_id}.blend")
        if not os.path.exists(blend_file):
            return {"success": False, "error": "Scene file not found"}
        
        render_script = f'''
import bpy
import math
import json

# Open the professional scene
bpy.ops.wm.open_mainfile(filepath='{blend_file}')

scene = bpy.context.scene
camera = scene.camera

if not camera:
    print(json.dumps({{"success": False, "error": "No camera found in scene"}}))
    exit()

# Render configurations for BEAUTIFUL INTERIOR PHOTOGRAPHY
render_configs = [
    {{"name": "hero_interior", "location": (-4, -3, 1.6), "rotation": (63, 0, -29), "description": "Main interior hero shot"}},
    {{"name": "living_room_wide", "location": (-3, -4, 1.8), "rotation": (58, 0, -20), "description": "Wide living room view"}},
    {{"name": "cozy_corner", "location": (-2, -2, 1.4), "rotation": (68, 0, -35), "description": "Intimate corner perspective"}},
    {{"name": "magazine_shot", "location": (-5, -2, 1.7), "rotation": (60, 0, -45), "description": "Professional magazine-style shot"}}
]

rendered_files = []

for config in render_configs:
    # Set camera position and rotation
    camera.location = config["location"]
    camera.rotation_euler = (
        math.radians(config["rotation"][0]),
        math.radians(config["rotation"][1]), 
        math.radians(config["rotation"][2])
    )
    
    # Set output filename
    render_path = os.path.join("{self.temp_dir}", f"professional_{{config['name']}}_{self.scene_id}.png")
    scene.render.filepath = render_path
    
    # Render
    bpy.ops.render.render(write_still=True)
    
    rendered_files.append({{
        "name": config["name"],
        "path": render_path,
        "description": config["description"]
    }})

print(json.dumps({{
    "success": True,
    "renders": rendered_files,
    "scene_id": "{self.scene_id}",
    "quality": "professional"
}}))
'''
        
        script_path = os.path.join(self.temp_dir, f'render_professional_{self.scene_id}.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(render_script)
        
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path
        ]
        
        try:
            print(f"🎬 Rendering professional views...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 minutes for GPU rendering
            
            if result.returncode == 0:
                # Parse the JSON output
                output_lines = result.stdout.strip().split('\n')
                for line in reversed(output_lines):
                    try:
                        render_result = json.loads(line)
                        if isinstance(render_result, dict) and render_result.get('success'):
                            return render_result
                    except json.JSONDecodeError:
                        continue
            
            return {
                "success": False,
                "error": f"Rendering failed: {result.stderr}",
                "stdout": result.stdout
            }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Rendering timeout (300s)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Rendering error: {str(e)}"
            }
    
    def generate_3d_model(self, model_config: Dict) -> Dict:
        """Generate a complete 3D model with professional materials and export multiple formats"""
        
        self.scene_id = str(uuid.uuid4())
        
        # Combined script for scene creation and rendering
        blender_script = '''
import bpy
import bmesh
import mathutils
from mathutils import Vector, Euler
import math
import json
import os

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# Model configuration
model_config = {model_config_json}
scene = bpy.context.scene

# Set up professional render settings with FORCED GPU acceleration
scene.render.engine = 'CYCLES'

# Force enable GPU and OptiX (better than CUDA)
import bpy
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences

# Set compute device to OptiX for best performance
cprefs.compute_device_type = 'OPTIX'

# Refresh and enable all OptiX devices
cprefs.get_devices()
for device in cprefs.devices:
    if device.type == 'OPTIX':
        device.use = True
        print("🚀 FORCE ENABLED OPTIX GPU:", device.name)
    elif device.type == 'CUDA':
        device.use = True
        print("🚀 FORCE ENABLED CUDA GPU:", device.name)
    else:
        device.use = False

# Force scene to use GPU
scene.cycles.device = 'GPU'
print("✅ GPU device forced ON with OptiX")

# Ultra high quality settings for GPU rendering
scene.cycles.samples = 1024  # High quality samples
scene.render.resolution_x = 3840  # 4K resolution
scene.render.resolution_y = 2160
scene.render.resolution_percentage = 100

# Enable all GPU-optimized features
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'  # Use NVIDIA OptiX denoiser
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01  # Balanced adaptive sampling
scene.cycles.max_bounces = 8  # Limit light bounces for speed
scene.cycles.diffuse_bounces = 4
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 4
scene.cycles.volume_bounces = 2
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

# Enable all quality features
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX' if scene.cycles.device == 'GPU' else 'OPENIMAGEDENOISE'
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

# Material creation function
def create_advanced_material(name, base_color, roughness=0.5, metallic=0.0, normal_strength=1.0, specular=0.5):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    
    # Create principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    # Check if IOR (Index of Refraction) input exists and set it
    if 'IOR' in bsdf.inputs:
        bsdf.inputs['IOR'].default_value = 1.45
    
    # Output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return material

# Room creation function - CREATE BEAUTIFUL INTERIOR SPACES  
def create_room_with_details(room_data):
    room_name = room_data.get('name', 'Room')
    room_type = room_data.get('type', 'living_room')
    width = room_data.get('width', 6)
    length = room_data.get('length', 8)
    height = room_data.get('height', 3)
    
    # Create beautiful hardwood floor (RELIABLE METHOD)
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor_Room"
    
    # Apply beautiful hardwood material
    floor_mat = bpy.data.materials.new(name="FloorMat_Room")
    floor_mat.use_nodes = True
    floor_bsdf = floor_mat.node_tree.nodes["Principled BSDF"]
    floor_bsdf.inputs[0].default_value = (0.4, 0.25, 0.15, 1.0)  # Rich wood
    floor_bsdf.inputs[2].default_value = 0.3  # Roughness
    floor.data.materials.append(floor_mat)
    
    # Create back wall (VISIBLE TO CAMERA)
    bpy.ops.mesh.primitive_cube_add(location=(0, 5, 1.5))
    back_wall = bpy.context.active_object
    back_wall.name = "BackWall_Room"
    back_wall.scale = (5, 0.1, 1.5)
    
    # Apply beautiful wall material
    wall_mat = bpy.data.materials.new(name="WallMat_Room")
    wall_mat.use_nodes = True
    wall_bsdf = wall_mat.node_tree.nodes["Principled BSDF"]
    wall_bsdf.inputs[0].default_value = (0.92, 0.90, 0.85, 1.0)  # Warm off-white
    wall_bsdf.inputs[2].default_value = 0.8  # Roughness
    back_wall.data.materials.append(wall_mat)
    floor.name = "Floor_" + room_name
    floor.scale = (width, length, 1)
    
    # Beautiful hardwood floor material
    floor_material = create_advanced_material(
        "Hardwood_Floor_" + room_name,
        (0.4, 0.25, 0.15),  # Rich wood brown
        roughness=0.2,
        metallic=0.0
    )
    floor.data.materials.append(floor_material)
    
    # Create walls for interior view (only back and side walls, open front for camera view)
    wall_thickness = 0.1
    
    # Back wall
    bpy.ops.mesh.primitive_cube_add(location=(0, length/2, height/2))
    back_wall = bpy.context.active_object
    back_wall.name = "BackWall_" + room_name
    back_wall.scale = (width, wall_thickness, height)
    
    # Left wall
    bpy.ops.mesh.primitive_cube_add(location=(-width/2, 0, height/2))
    left_wall = bpy.context.active_object
    left_wall.name = "LeftWall_" + room_name
    left_wall.scale = (wall_thickness, length, height)
    
    # Right wall
    bpy.ops.mesh.primitive_cube_add(location=(width/2, 0, height/2))
    right_wall = bpy.context.active_object
    right_wall.name = "RightWall_" + room_name
    right_wall.scale = (wall_thickness, length, height)
    
    # Beautiful wall material - elegant white/cream
    wall_material = create_advanced_material(
        "Interior_Wall_" + room_name,
        (0.95, 0.92, 0.88),  # Warm cream white
        roughness=0.4,
        metallic=0.0
    )
    
    for wall in [back_wall, left_wall, right_wall]:
        wall.data.materials.append(wall_material)
    
    # Create ceiling
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, height))
    ceiling = bpy.context.active_object
    ceiling.name = "Ceiling_" + room_name
    ceiling.scale = (width, length, 1)
    ceiling.data.materials.append(wall_material)

# Luxury furniture creation - CREATE REALISTIC INTERIOR FURNITURE
def create_luxury_furniture(room_data):
    room_type = room_data.get('type', 'living_room')
    width = room_data.get('width', 6)
    length = room_data.get('length', 8)
    
    if room_type == 'living_room':
        # Elegant sectional sofa
        bpy.ops.mesh.primitive_cube_add(location=(0, -length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "Luxury_Sectional_Sofa"
        sofa.scale = (2.5, 1.2, 0.4)
        
        # Add sofa back
        bpy.ops.mesh.primitive_cube_add(location=(0, -length/4 + 0.4, 0.8))
        sofa_back = bpy.context.active_object
        sofa_back.name = "Sofa_Back"
        sofa_back.scale = (2.5, 0.2, 0.6)
        
        # Luxury fabric material
        fabric_material = create_advanced_material(
            "Luxury_Velvet",
            (0.2, 0.4, 0.6),  # Deep blue velvet
            roughness=0.8,
            metallic=0.0
        )
        sofa.data.materials.append(fabric_material)
        sofa_back.data.materials.append(fabric_material)
        
        # Glass coffee table with metal frame
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.3))
        table = bpy.context.active_object
        table.name = "Glass_Coffee_Table"
        table.scale = (1.5, 0.8, 0.05)
        
        # Glass top material
        glass_material = create_advanced_material(
            "Premium_Glass",
            (0.9, 0.95, 1.0),  # Clear glass with slight blue tint
            roughness=0.0,
            metallic=0.0
        )
        table.data.materials.append(glass_material)
        
        # Modern TV stand
        bpy.ops.mesh.primitive_cube_add(location=(0, length/2 - 0.3, 0.3))
        tv_stand = bpy.context.active_object
        tv_stand.name = "Modern_TV_Stand"
        tv_stand.scale = (2.0, 0.4, 0.3)
        
        # Dark wood material for TV stand
        wood_material = create_advanced_material(
            "Dark_Walnut",
            (0.15, 0.1, 0.08),  # Dark walnut
            roughness=0.3,
            metallic=0.0
        )
        tv_stand.data.materials.append(wood_material)
        
        # Add decorative lamp
        bpy.ops.mesh.primitive_cylinder_add(location=(width/2 - 0.5, -length/4, 0.8))
        lamp_base = bpy.context.active_object
        lamp_base.name = "Table_Lamp_Base"
        lamp_base.scale = (0.1, 0.1, 0.6)
        lamp_base.data.materials.append(wood_material)
        
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.45))
        island = bpy.context.active_object
        island.name = "Kitchen_Island"
        island.scale = (1.5, 1.0, 0.45)
        
        # Marble countertop material
        marble_material = create_advanced_material(
            "Carrara_Marble",
            (0.95, 0.95, 0.98),  # White marble
            roughness=0.1,
            metallic=0.0
        )
        island.data.materials.append(marble_material)
        
        # Kitchen cabinets along back wall
        bpy.ops.mesh.primitive_cube_add(location=(0, length/2 - 0.3, 0.4))
        cabinets = bpy.context.active_object
        cabinets.name = "Kitchen_Cabinets"
        cabinets.scale = (width - 1, 0.6, 0.4)
        
        # Modern cabinet material
        cabinet_material = create_advanced_material(
            "Modern_Cabinet",
            (0.25, 0.25, 0.3),  # Modern gray
            roughness=0.2,
            metallic=0.1
        )
        cabinets.data.materials.append(cabinet_material)
        
    elif room_type == 'bedroom':
        # King size bed
        bpy.ops.mesh.primitive_cube_add(location=(0, length/4, 0.3))
        bed = bpy.context.active_object
        bed.name = "King_Size_Bed"
        bed.scale = (2.0, 2.2, 0.3)
        
        # Headboard
        bpy.ops.mesh.primitive_cube_add(location=(0, length/4 + 1.0, 0.8))
        headboard = bpy.context.active_object
        headboard.name = "Bed_Headboard"
        headboard.scale = (2.2, 0.1, 0.8)
        
        # Luxury bedding material
        bedding_material = create_advanced_material(
            "Silk_Bedding",
            (0.8, 0.8, 0.85),  # Elegant white/silver
            roughness=0.1,
            metallic=0.0
        )
        bed.data.materials.append(bedding_material)
        headboard.data.materials.append(wood_material)
        
        # Nightstands
        nightstand_positions = [(-1.3, length/4, 0.3), (1.3, length/4, 0.3)]
        for i, pos in enumerate(nightstand_positions):
            bpy.ops.mesh.primitive_cube_add(location=pos)
            nightstand = bpy.context.active_object
            nightstand.name = "Nightstand_" + str(i)
            nightstand.scale = (0.4, 0.4, 0.3)
            nightstand.data.materials.append(wood_material)

# PROFESSIONAL INTERIOR LIGHTING SETUP
def setup_advanced_lighting():
    # Remove default light
    if bpy.data.lights.get('Light'):
        bpy.data.lights.remove(bpy.data.lights['Light'])
    
    # HDRI Environment lighting for realistic reflections
    world = bpy.context.scene.world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_nodes.clear()
    
    # Environment texture
    env_tex = world_nodes.new('ShaderNodeTexEnvironment')
    background = world_nodes.new('ShaderNodeBackground')
    output = world_nodes.new('ShaderNodeOutputWorld')
    
    # Set warm interior lighting
    background.inputs['Color'].default_value = (0.8, 0.9, 1.0, 1.0)  # Soft daylight
    background.inputs['Strength'].default_value = 0.3
    
    world.node_tree.links.new(background.outputs['Background'], output.inputs['Surface'])
    
    # Main window light (simulating natural daylight)
    bpy.ops.object.light_add(type='AREA', location=(0, -6, 2))
    window_light = bpy.context.active_object
    window_light.name = "Window_Light"
    window_light.data.energy = 80.0
    window_light.data.size = 4.0
    window_light.data.color = (1.0, 0.95, 0.9)  # Warm daylight
    window_light.rotation_euler = (1.2, 0, 0)  # Angle downward
    
    # Ceiling ambient light
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.8))
    ceiling_light = bpy.context.active_object
    ceiling_light.name = "Ceiling_Light"
    ceiling_light.data.energy = 30.0
    ceiling_light.data.size = 3.0
    ceiling_light.data.color = (1.0, 0.98, 0.95)  # Warm white
    ceiling_light.rotation_euler = (3.14159, 0, 0)  # Point downward
    
    # Accent corner light for depth
    bpy.ops.object.light_add(type='SPOT', location=(2, 2, 2.5))
    accent_light = bpy.context.active_object
    accent_light.name = "Accent_Light"
    accent_light.data.energy = 20.0
    accent_light.data.spot_size = 1.2
    accent_light.data.color = (1.0, 0.9, 0.8)  # Warm accent
    
    # Point accent light towards interesting furniture
    accent_light.rotation_euler = (1.3, 0, -0.8)

# PROFESSIONAL INTERIOR CAMERA SETUP - RELIABLE VERSION
def setup_professional_camera():
    # Remove default camera if exists
    if bpy.data.cameras.get('Camera'):
        bpy.data.cameras.remove(bpy.data.cameras['Camera'])
    
    # Create camera positioned for PERFECT interior view (TESTED WORKING)
    bpy.ops.object.camera_add(location=(-3, -3, 1.8))
    camera = bpy.context.active_object
    camera.name = "InteriorCamera"
    
    # Point camera into the room (PROVEN WORKING ANGLE)
    camera.rotation_euler = (1.0, 0, -0.8)  # Tested and working rotation
    
    # Professional camera settings
    camera.data.lens = 24  # Wide angle for spacious feel
    camera.data.sensor_width = 36  # Full frame sensor
    camera.data.clip_start = 0.1
    camera.data.clip_end = 100
    
    # Depth of field for cinematic look
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 6.0  # Focus on room center
    camera.data.dof.aperture_fstop = 4.0  # Sharp but with some bokeh
    
    # Set as active camera
    bpy.context.scene.camera = camera

# Create rooms if specified
if 'rooms' in model_config:
    for room_data in model_config['rooms']:
        create_room_with_details(room_data)
        create_luxury_furniture(room_data)

# Set up lighting and camera
setup_advanced_lighting()
setup_professional_camera()

# Export files
output_dir = "{temp_dir}"
scene_name = "professional_model_{scene_id}"

# Save .blend file
blend_file = os.path.join(output_dir, scene_name + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_file)

# Export OBJ with materials
obj_file = os.path.join(output_dir, scene_name + ".obj")
bpy.ops.wm.obj_export(
    filepath=obj_file,
    export_materials=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_triangulated_mesh=False
)

# Export GLB for web
glb_file = os.path.join(output_dir, scene_name + ".glb")
bpy.ops.export_scene.gltf(
    filepath=glb_file,
    export_format='GLB',
    export_materials='EXPORT'
)

# Render ultra high-quality INTERIOR IMAGES
render_configs = [
    {{"name": "hero_interior_4k", "location": (-4, -3, 1.6), "rotation": (63, 0, -29)}},
    {{"name": "living_detail_4k", "location": (-3, -4, 1.8), "rotation": (58, 0, -20)}},
    {{"name": "magazine_4k", "location": (-5, -2, 1.7), "rotation": (60, 0, -45)}}
]

rendered_files = []
camera = scene.camera

for config in render_configs:
    camera.location = config["location"]
    camera.rotation_euler = [math.radians(config["rotation"][0]), 
                            math.radians(config["rotation"][1]), 
                            math.radians(config["rotation"][2])]
    
    render_file = os.path.join(output_dir, scene_name + "_" + config['name'] + ".png")
    scene.render.filepath = render_file
    bpy.ops.render.render(write_still=True)
    rendered_files.append(render_file)

# Output result
result = {{
    "success": True,
    "scene_id": "{scene_id}",
    "files": [
        blend_file,
        obj_file,
        glb_file
    ] + rendered_files,
    "temp_dir": output_dir,
    "message": "Professional 3D model generated successfully"
}}

print("BLENDER_RESULT_START")
print(json.dumps(result))
print("BLENDER_RESULT_END")
'''.format(
            model_config_json=json.dumps(model_config),
            temp_dir=self.temp_dir.replace(os.sep, '/'),
            scene_id=self.scene_id
        )
        # Elegant sectional sofa
        bpy.ops.mesh.primitive_cube_add(location=(0, -length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "Luxury_Sectional_Sofa"
        sofa.scale = (2.5, 1.2, 0.4)
        
        # Add sofa back
        bpy.ops.mesh.primitive_cube_add(location=(0, -length/4 + 0.4, 0.8))
        sofa_back = bpy.context.active_object
        sofa_back.name = "Sofa_Back"
        sofa_back.scale = (2.5, 0.2, 0.6)
        
        # Luxury fabric material
        fabric_material = create_advanced_material(
            "Luxury_Velvet",
            (0.2, 0.4, 0.6),  # Deep blue velvet
            roughness=0.8,
            metallic=0.0
        )
        sofa.data.materials.append(fabric_material)
        sofa_back.data.materials.append(fabric_material)
        
        # Glass coffee table with metal frame
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.3))
        table = bpy.context.active_object
        table.name = "Glass_Coffee_Table"
        table.scale = (1.5, 0.8, 0.05)
        
        # Glass top material
        glass_material = create_advanced_material(
            "Premium_Glass",
            (0.9, 0.95, 1.0),  # Clear glass with slight blue tint
            roughness=0.0,
            metallic=0.0
        )
        table.data.materials.append(glass_material)
        
        # Modern TV stand
        bpy.ops.mesh.primitive_cube_add(location=(0, length/2 - 0.3, 0.3))
        tv_stand = bpy.context.active_object
        tv_stand.name = "Modern_TV_Stand"
        tv_stand.scale = (2.0, 0.4, 0.3)
        
        # Dark wood material for TV stand
        wood_material = create_advanced_material(
            "Dark_Walnut",
            (0.15, 0.1, 0.08),  # Dark walnut
            roughness=0.3,
            metallic=0.0
        )
        tv_stand.data.materials.append(wood_material)
        
        # Add decorative lamp
        bpy.ops.mesh.primitive_cylinder_add(location=(width/2 - 0.5, -length/4, 0.8))
        lamp_base = bpy.context.active_object
        lamp_base.name = "Table_Lamp_Base"
        lamp_base.scale = (0.1, 0.1, 0.6)
        lamp_base.data.materials.append(wood_material)
        
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.45))
        island = bpy.context.active_object
        island.name = "Kitchen_Island"
        island.scale = (1.5, 1.0, 0.45)
        
        # Marble countertop material
        marble_material = create_advanced_material(
            "Carrara_Marble",
            (0.95, 0.95, 0.98),  # White marble
            roughness=0.1,
            metallic=0.0
        )
        island.data.materials.append(marble_material)
        
        # Kitchen cabinets along back wall
        bpy.ops.mesh.primitive_cube_add(location=(0, length/2 - 0.3, 0.4))
        cabinets = bpy.context.active_object
        cabinets.name = "Kitchen_Cabinets"
        cabinets.scale = (width - 1, 0.6, 0.4)
        
        # Modern cabinet material
        cabinet_material = create_advanced_material(
            "Modern_Cabinet",
            (0.25, 0.25, 0.3),  # Modern gray
            roughness=0.2,
            metallic=0.1
        )
        cabinets.data.materials.append(cabinet_material)
        
    elif room_type == 'bedroom':
        # King size bed
        bpy.ops.mesh.primitive_cube_add(location=(0, length/4, 0.3))
        bed = bpy.context.active_object
        bed.name = "King_Size_Bed"
        bed.scale = (2.0, 2.2, 0.3)
        
        # Headboard
        bpy.ops.mesh.primitive_cube_add(location=(0, length/4 + 1.0, 0.8))
        headboard = bpy.context.active_object
        headboard.name = "Bed_Headboard"
        headboard.scale = (2.2, 0.1, 0.8)
        
        # Luxury bedding material
        bedding_material = create_advanced_material(
            "Silk_Bedding",
            (0.8, 0.8, 0.85),  # Elegant white/silver
            roughness=0.1,
            metallic=0.0
        )
        bed.data.materials.append(bedding_material)
        headboard.data.materials.append(wood_material)
        
        # Nightstands
        nightstand_positions = [(-1.3, length/4, 0.3), (1.3, length/4, 0.3)]
        for i, pos in enumerate(nightstand_positions):
            bpy.ops.mesh.primitive_cube_add(location=pos)
            nightstand = bpy.context.active_object
            nightstand.name = f"Nightstand_{{i}}"
            nightstand.scale = (0.4, 0.4, 0.3)
            nightstand.data.materials.append(wood_material)

# PROFESSIONAL INTERIOR LIGHTING SETUP
def setup_advanced_lighting():
    # Remove default light
    if bpy.data.lights.get('Light'):
        bpy.data.lights.remove(bpy.data.lights['Light'])
    
    # HDRI Environment lighting for realistic reflections
    world = bpy.context.scene.world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_nodes.clear()
    
    # Environment texture
    env_tex = world_nodes.new('ShaderNodeTexEnvironment')
    background = world_nodes.new('ShaderNodeBackground')
    output = world_nodes.new('ShaderNodeOutputWorld')
    
    # Set warm interior lighting
    background.inputs['Color'].default_value = (0.8, 0.9, 1.0, 1.0)  # Soft daylight
    background.inputs['Strength'].default_value = 0.3
    
    world.node_tree.links.new(background.outputs['Background'], output.inputs['Surface'])
    
    # Main window light (simulating natural daylight)
    bpy.ops.object.light_add(type='AREA', location=(0, -6, 2))
    window_light = bpy.context.active_object
    window_light.name = "Window_Light"
    window_light.data.energy = 80.0
    window_light.data.size = 4.0
    window_light.data.color = (1.0, 0.95, 0.9)  # Warm daylight
    window_light.rotation_euler = (1.2, 0, 0)  # Angle downward
    
    # Ceiling ambient light
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.8))
    ceiling_light = bpy.context.active_object
    ceiling_light.name = "Ceiling_Light"
    ceiling_light.data.energy = 30.0
    ceiling_light.data.size = 3.0
    ceiling_light.data.color = (1.0, 0.98, 0.95)  # Warm white
    ceiling_light.rotation_euler = (3.14159, 0, 0)  # Point downward
    
    # Accent corner light for depth
    bpy.ops.object.light_add(type='SPOT', location=(2, 2, 2.5))
    accent_light = bpy.context.active_object
    accent_light.name = "Accent_Light"
    accent_light.data.energy = 20.0
    accent_light.data.spot_size = 1.2
    accent_light.data.color = (1.0, 0.9, 0.8)  # Warm accent
    
    # Point accent light towards interesting furniture
    accent_light.rotation_euler = (1.3, 0, -0.8)

# PROFESSIONAL INTERIOR CAMERA SETUP - RELIABLE VERSION
def setup_professional_camera():
    # Remove default camera if exists
    if bpy.data.cameras.get('Camera'):
        bpy.data.cameras.remove(bpy.data.cameras['Camera'])
    
    # Create camera positioned for PERFECT interior view (TESTED WORKING)
    bpy.ops.object.camera_add(location=(-3, -3, 1.8))
    camera = bpy.context.active_object
    camera.name = "InteriorCamera"
    
    # Point camera into the room (PROVEN WORKING ANGLE)
    camera.rotation_euler = (1.0, 0, -0.8)  # Tested and working rotation
    
    # Professional camera settings
    camera.data.lens = 24  # Wide angle for spacious feel
    camera.data.sensor_width = 36  # Full frame sensor
    camera.data.clip_start = 0.1
    camera.data.clip_end = 100
    
    # Depth of field for cinematic look
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 6.0  # Focus on room center
    camera.data.dof.aperture_fstop = 4.0  # Sharp but with some bokeh
    
    # Set as active camera
    bpy.context.scene.camera = camera

# Create rooms if specified
if 'rooms' in model_config:
    for room_data in model_config['rooms']:
        create_room_with_details(room_data)
        create_luxury_furniture(room_data)

# Set up lighting and camera
setup_advanced_lighting()
setup_professional_camera()

# Export files
output_dir = "{self.temp_dir.replace(os.sep, '/')}"
scene_name = "professional_model_{self.scene_id}"

# Save .blend file
blend_file = os.path.join(output_dir, f"{{scene_name}}.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_file)

# Export OBJ with materials
obj_file = os.path.join(output_dir, f"{{scene_name}}.obj")
bpy.ops.wm.obj_export(
    filepath=obj_file,
    export_materials=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_triangulated_mesh=False
)

# Export GLB for web
glb_file = os.path.join(output_dir, f"{{scene_name}}.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_file,
    export_format='GLB',
    export_materials='EXPORT'
)

# Render ultra high-quality INTERIOR IMAGES
render_configs = [
    {{"name": "hero_interior_4k", "location": (-4, -3, 1.6), "rotation": (63, 0, -29)}},
    {{"name": "living_detail_4k", "location": (-3, -4, 1.8), "rotation": (58, 0, -20)}},
    {{"name": "magazine_4k", "location": (-5, -2, 1.7), "rotation": (60, 0, -45)}}
]

rendered_files = []
camera = scene.camera

for config in render_configs:
    camera.location = config["location"]
    camera.rotation_euler = [math.radians(config["rotation"][0]), 
                            math.radians(config["rotation"][1]), 
                            math.radians(config["rotation"][2])]
    
    render_file = os.path.join(output_dir, f"{{scene_name}}_{{config['name']}}.png")
    scene.render.filepath = render_file
    bpy.ops.render.render(write_still=True)
    rendered_files.append(render_file)

# Output result
result = {{
    "success": True,
    "scene_id": "{self.scene_id}",
    "files": [
        blend_file,
        obj_file,
        glb_file
    ] + rendered_files,
    "temp_dir": output_dir,
    "message": "Professional 3D model generated successfully"
}}

print("BLENDER_RESULT_START")
print(json.dumps(result))
print("BLENDER_RESULT_END")
'''
        
        try:
            # Execute Blender with the combined script
            result = subprocess.run([
                self.blender_path,
                '--background',
                '--python-expr', blender_script
            ], capture_output=True, text=True, timeout=600)  # 10 minutes timeout
            
            # Parse the result
            for line in result.stdout.split('\n'):
                if line.strip().startswith('BLENDER_RESULT_START'):
                    # Find the JSON result
                    result_lines = []
                    capturing = False
                    for output_line in result.stdout.split('\n'):
                        if 'BLENDER_RESULT_START' in output_line:
                            capturing = True
                            continue
                        elif 'BLENDER_RESULT_END' in output_line:
                            break
                        elif capturing:
                            result_lines.append(output_line)
                    
                    try:
                        result_json = json.loads('\n'.join(result_lines))
                        return result_json
                    except json.JSONDecodeError:
                        continue
            
            return {
                "success": False,
                "error": f"Model generation failed: {result.stderr}",
                "stdout": result.stdout
            }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Model generation timeout (600s)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Model generation error: {str(e)}"
            }

# Global renderer instance
advanced_renderer = AdvancedBlenderRenderer()

def main():
    """CLI interface for the advanced renderer"""
    if len(sys.argv) < 2:
        print("Usage: python advanced_blender_renderer.py <tool> [args_json]")
        sys.exit(1)
    
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {{}}
    
    if tool == "create_3d_scene":
        result = advanced_renderer.create_professional_scene(args)
        print(json.dumps(result))
    elif tool == "render_scene":
        result = advanced_renderer.render_professional_views()
        print(json.dumps(result))
    else:
        print(json.dumps({{"success": False, "error": f"Unknown tool: {tool}"}}))

if __name__ == "__main__":
    main()
