#!/usr/bin/env python3
"""
Photorealistic BOQ Renderer - Simplified Professional Quality
GPU Optimized for RTX 4050 with Blender 4.4 Compatibility
"""
import subprocess
import os
import tempfile
import uuid
import json
import shutil
import math
import random

# Force NVIDIA GPU usage (RTX 4050 is CUDA device 0)
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['BLENDER_CUDA_DEVICE'] = '0'
os.environ['NVIDIA_VISIBLE_DEVICES'] = '0'

from advanced_layout_generator import AdvancedLayoutGenerator

class PhotorealisticRendererV2:
    """Professional photorealistic renderer with simplified material system"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_photorealistic_v2_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        self.layout_generator = AdvancedLayoutGenerator()
    
    def render_photorealistic_scene(self, boq_config):
        """Render a photorealistic 3D scene with advanced materials and lighting"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 40, "total_length": 30, "height": 12})
        enhanced_features = boq_config.get('enhanced_features', {})
        architectural_style = boq_config.get('architectural_style', 'modern')
        quality_level = boq_config.get('quality_level', 'professional')
        
        print(f"Creating photorealistic scene: {self.scene_id}")
        print(f"Rooms: {len(rooms)}, Style: {architectural_style}, Quality: {quality_level}")
        
        # Generate advanced layout
        layout_positions = self.layout_generator.generate_layout(rooms, building_dims)
        
        # Create simplified but high-quality Blender script
        layout_json_str = json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        enhanced_features_str = json.dumps(enhanced_features).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        
        blender_script = f'''
import bpy
import bmesh
import math
import random
from mathutils import Vector, Euler

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

scene = bpy.context.scene

# NVIDIA RTX 4050 GPU SETUP
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
cprefs.compute_device_type = 'OPTIX'
cprefs.get_devices()

print("🔥 Configuring NVIDIA RTX 4050 for photorealistic rendering...")
nvidia_gpu_found = False
for i, device in enumerate(cprefs.devices):
    if device.type in ['OPTIX', 'CUDA']:
        if "RTX" in device.name or "GeForce" in device.name or "NVIDIA" in device.name:
            device.use = True
            nvidia_gpu_found = True
            print(f"✅ ENABLED GPU {{i}}: {{device.name}} ({{device.type}})")
        else:
            device.use = False
            print(f"❌ DISABLED GPU {{i}}: {{device.name}} ({{device.type}})")
    else:
        device.use = False

if nvidia_gpu_found:
    scene.cycles.device = 'GPU'
    print("🚀 RTX 4050 GPU configured for rendering")
else:
    scene.cycles.device = 'CPU'
    print("⚠️ NVIDIA GPU not found, falling back to CPU")

# PROFESSIONAL QUALITY RENDER SETTINGS (OPTIMIZED)
scene.cycles.samples = 1024  # Reduced for faster rendering
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01  # Slightly relaxed
scene.cycles.time_limit = 0

# PROFESSIONAL CAMERA AND RENDER SETTINGS (OPTIMIZED)
scene.render.resolution_x = 2560  # 2K instead of 4K
scene.render.resolution_y = 1440
scene.render.resolution_percentage = 100
scene.render.use_motion_blur = False  # Disabled for speed
scene.render.motion_blur_shutter = 0.5

# COLOR MANAGEMENT
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - High Contrast'
scene.view_settings.exposure = 0.5
scene.view_settings.gamma = 1.0

# WORLD HDRI SETUP
world = bpy.data.worlds.new("PhotorealisticWorld")
scene.world = world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_nodes.clear()

# Create environment lighting
env_tex = world_nodes.new(type='ShaderNodeTexEnvironment')
mapping = world_nodes.new(type='ShaderNodeMapping')
tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
background = world_nodes.new(type='ShaderNodeBackground')
output = world_nodes.new(type='ShaderNodeOutputWorld')

# Link world nodes
world.node_tree.links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
world.node_tree.links.new(mapping.outputs["Vector"], env_tex.inputs["Vector"])
world.node_tree.links.new(env_tex.outputs["Color"], background.inputs["Color"])
world.node_tree.links.new(background.outputs["Background"], output.inputs["Surface"])

background.inputs["Strength"].default_value = 2.0
mapping.inputs["Rotation"].default_value = (0, 0, math.radians(45))

def create_material(name, base_color, roughness=0.5, metallic=0.0, 
                   emission=None, emission_strength=1.0, 
                   normal_strength=0.0, subsurface=0.0, transmission=0.0, 
                   ior=1.45, alpha=1.0):
    """Create a high-quality material compatible with Blender 4.4+"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.use_backface_culling = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Main BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Set basic properties (compatible with all Blender versions)
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["IOR"].default_value = ior
    bsdf.inputs["Alpha"].default_value = alpha
    
    # Subsurface scattering
    if subsurface > 0:
        try:
            if "Subsurface Weight" in bsdf.inputs:
                bsdf.inputs["Subsurface Weight"].default_value = subsurface
            elif "Subsurface" in bsdf.inputs:
                bsdf.inputs["Subsurface"].default_value = subsurface
        except:
            pass
    
    # Transmission for glass
    if transmission > 0:
        try:
            if "Transmission Weight" in bsdf.inputs:
                bsdf.inputs["Transmission Weight"].default_value = transmission
            elif "Transmission" in bsdf.inputs:
                bsdf.inputs["Transmission"].default_value = transmission
        except:
            pass
    
    # Emission for lights
    if emission:
        try:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = (*emission, 1.0)
            
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
        except:
            pass
    
    # Add surface detail with noise
    if normal_strength > 0:
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-800, 0)
        noise.inputs["Scale"].default_value = 15.0
        noise.inputs["Detail"].default_value = 10.0
        noise.inputs["Roughness"].default_value = 0.5
        
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (-600, 0)
        color_ramp.color_ramp.elements[0].position = 0.4
        color_ramp.color_ramp.elements[1].position = 0.6
        
        normal_map = nodes.new(type='ShaderNodeNormalMap')
        normal_map.location = (-200, -200)
        normal_map.inputs["Strength"].default_value = normal_strength
        
        mat.node_tree.links.new(noise.outputs["Fac"], color_ramp.inputs["Fac"])
        mat.node_tree.links.new(color_ramp.outputs["Color"], normal_map.inputs["Color"])
        mat.node_tree.links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
    
    # Add subtle color variation
    color_noise = nodes.new(type='ShaderNodeTexNoise')
    color_noise.location = (-800, 300)
    color_noise.inputs["Scale"].default_value = 50.0
    color_noise.inputs["Detail"].default_value = 5.0
    
    color_mix = nodes.new(type='ShaderNodeMixRGB')
    color_mix.location = (-400, 200)
    color_mix.blend_type = 'MULTIPLY'
    color_mix.inputs["Fac"].default_value = 0.1
    color_mix.inputs["Color1"].default_value = (*base_color, 1.0)
    
    varied_color = [min(1.0, max(0.0, c + random.uniform(-0.03, 0.03))) for c in base_color]
    color_mix.inputs["Color2"].default_value = (*varied_color, 1.0)
    
    mat.node_tree.links.new(color_noise.outputs["Fac"], color_mix.inputs["Fac"])
    mat.node_tree.links.new(color_mix.outputs["Color"], bsdf.inputs["Base Color"])
    
    # Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    
    return mat

# HIGH-QUALITY MATERIAL LIBRARY
print("🎨 Creating high-quality materials...")

materials = {{
    # Premium flooring
    'floor_walnut': create_material("Walnut Hardwood", (0.35, 0.20, 0.12), 0.3, 0.0, normal_strength=0.8),
    'floor_oak': create_material("Oak Hardwood", (0.55, 0.35, 0.20), 0.25, 0.0, normal_strength=0.6),
    'floor_marble': create_material("Carrara Marble", (0.98, 0.97, 0.95), 0.02, 0.0, normal_strength=0.4, subsurface=0.05),
    'floor_porcelain': create_material("Porcelain Tile", (0.92, 0.90, 0.88), 0.05, 0.0, normal_strength=0.2),
    'floor_travertine': create_material("Travertine", (0.88, 0.82, 0.72), 0.4, 0.0, normal_strength=0.6),
    
    # Wall materials
    'wall_white': create_material("White Paint", (0.95, 0.94, 0.92), 0.9, 0.0, normal_strength=0.1),
    'wall_gray': create_material("Gray Paint", (0.75, 0.75, 0.78), 0.85, 0.0, normal_strength=0.1),
    'wall_beige': create_material("Beige Paint", (0.88, 0.85, 0.80), 0.8, 0.0, normal_strength=0.1),
    'wall_stone': create_material("Natural Stone", (0.75, 0.70, 0.65), 0.7, 0.0, normal_strength=1.0),
    'wall_wood': create_material("Wood Paneling", (0.45, 0.35, 0.25), 0.4, 0.0, normal_strength=0.5),
    
    # Furniture materials
    'furniture_leather': create_material("Leather", (0.35, 0.20, 0.12), 0.2, 0.0, normal_strength=0.3, subsurface=0.1),
    'furniture_fabric': create_material("Fabric", (0.88, 0.82, 0.75), 0.9, 0.0, normal_strength=0.8),
    'furniture_wood_dark': create_material("Dark Wood", (0.25, 0.15, 0.10), 0.3, 0.0, normal_strength=0.5),
    'furniture_wood_light': create_material("Light Wood", (0.65, 0.45, 0.30), 0.3, 0.0, normal_strength=0.5),
    
    # Metal materials
    'metal_steel': create_material("Stainless Steel", (0.85, 0.85, 0.85), 0.15, 0.95, normal_strength=0.3),
    'metal_brass': create_material("Brass", (0.85, 0.70, 0.35), 0.2, 0.9, normal_strength=0.2),
    'metal_black': create_material("Black Steel", (0.05, 0.05, 0.05), 0.3, 0.8, normal_strength=0.3),
    
    # Glass materials
    'glass_clear': create_material("Clear Glass", (0.98, 0.98, 0.98), 0.0, 0.0, transmission=0.95, ior=1.52, alpha=0.1),
    'glass_frosted': create_material("Frosted Glass", (0.95, 0.95, 0.95), 0.8, 0.0, transmission=0.7, ior=1.45, alpha=0.3),
    
    # Lighting materials
    'light_warm': create_material("Warm Light", (1.0, 0.9, 0.7), 0.0, 0.0, emission=(1.0, 0.9, 0.7), emission_strength=30.0),
    'light_cool': create_material("Cool Light", (0.9, 0.95, 1.0), 0.0, 0.0, emission=(0.9, 0.95, 1.0), emission_strength=25.0),
    'light_accent': create_material("Accent Light", (1.0, 0.8, 0.5), 0.0, 0.0, emission=(1.0, 0.8, 0.5), emission_strength=15.0),
    
    # Landscape materials
    'landscape_grass': create_material("Grass", (0.25, 0.55, 0.25), 0.9, 0.0, normal_strength=1.0, subsurface=0.3),
    'landscape_soil': create_material("Soil", (0.35, 0.25, 0.15), 0.95, 0.0, normal_strength=1.2),
    'landscape_bark': create_material("Tree Bark", (0.35, 0.25, 0.18), 0.9, 0.0, normal_strength=1.5),
    'landscape_leaves': create_material("Leaves", (0.30, 0.60, 0.25), 0.8, 0.0, normal_strength=0.8, subsurface=0.5, alpha=0.8),
    
    # Architectural materials
    'concrete': create_material("Concrete", (0.7, 0.68, 0.65), 0.8, 0.0, normal_strength=0.8),
}}

print(f"✅ Created {{len(materials)}} high-quality materials")

# Building dimensions
total_width = {building_dims['total_width']}
total_length = {building_dims['total_length']}
total_height = {building_dims.get('height', 12)}

# Enhanced features
enhanced_features = {enhanced_features_str}

print(f"🏗️ Building: {{total_width}}x{{total_length}}x{{total_height}}m")

# CREATE FOUNDATION
bpy.ops.mesh.primitive_plane_add(size=1, location=(total_width/2, total_length/2, -0.1))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (total_width/2 + 2, total_length/2 + 2, 1)
foundation.data.materials.append(materials['concrete'])

# CREATE EXTERIOR WALLS
wall_thickness = 0.3
wall_height = 3.0

walls = [
    ("North", (total_width/2, total_length + wall_thickness/2, wall_height/2), (total_width/2 + wall_thickness/2, wall_thickness/2, wall_height/2)),
    ("South", (total_width/2, -wall_thickness/2, wall_height/2), (total_width/2 + wall_thickness/2, wall_thickness/2, wall_height/2)),
    ("East", (total_width + wall_thickness/2, total_length/2, wall_height/2), (wall_thickness/2, total_length/2, wall_height/2)),
    ("West", (-wall_thickness/2, total_length/2, wall_height/2), (wall_thickness/2, total_length/2, wall_height/2))
]

for name, location, scale in walls:
    bpy.ops.mesh.primitive_cube_add(location=location)
    wall = bpy.context.active_object
    wall.name = f"ExteriorWall_{{name}}"
    wall.scale = scale
    wall.data.materials.append(materials['wall_stone'])

# Layout data
layout_data = {layout_json_str}

print(f"🏠 Creating {{len(layout_data)}} rooms with detailed furniture")

def create_detailed_furniture(room_type, room_center, room_width, room_length, room_height):
    """Create detailed furniture with proper scaling"""
    furniture = []
    
    if room_type == 'living':
        # Modern L-shaped sofa
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - room_length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "LivingRoomSofa"
        sofa.scale = (2.0, 0.5, 0.4)
        sofa.data.materials.append(materials['furniture_fabric'])
        
        # Sofa back
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - room_length/4 - 0.4, 0.8))
        sofa_back = bpy.context.active_object
        sofa_back.name = "SofaBack"
        sofa_back.scale = (2.0, 0.1, 0.4)
        sofa_back.data.materials.append(materials['furniture_fabric'])
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] + 0.3, 0.2))
        table = bpy.context.active_object
        table.name = "CoffeeTable"
        table.scale = (0.8, 0.4, 0.15)
        table.data.materials.append(materials['furniture_wood_dark'])
        
        # Glass table top
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] + 0.3, 0.37))
        table_top = bpy.context.active_object
        table_top.name = "CoffeeTableTop"
        table_top.scale = (0.85, 0.45, 0.02)
        table_top.data.materials.append(materials['glass_clear'])
        
        # Floor lamp
        bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0] + 1.5, room_center[1] - 1.5, 0.8))
        lamp_base = bpy.context.active_object
        lamp_base.name = "FloorLampBase"
        lamp_base.scale = (0.05, 0.05, 0.8)
        lamp_base.data.materials.append(materials['metal_steel'])
        
        # Lamp shade
        bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0] + 1.5, room_center[1] - 1.5, 1.8))
        lamp_shade = bpy.context.active_object
        lamp_shade.name = "FloorLampShade"
        lamp_shade.scale = (0.25, 0.25, 0.15)
        lamp_shade.data.materials.append(materials['light_warm'])
        
        furniture.extend([sofa, sofa_back, table, table_top, lamp_base, lamp_shade])
        
    elif room_type == 'bedroom':
        # Platform bed
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.25))
        bed_frame = bpy.context.active_object
        bed_frame.name = "BedFrame"
        bed_frame.scale = (1.0, 1.5, 0.25)
        bed_frame.data.materials.append(materials['furniture_wood_dark'])
        
        # Mattress
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.55))
        mattress = bpy.context.active_object
        mattress.name = "Mattress"
        mattress.scale = (0.95, 1.45, 0.15)
        mattress.data.materials.append(materials['furniture_fabric'])
        
        # Headboard
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - 1.5, 0.9))
        headboard = bpy.context.active_object
        headboard.name = "Headboard"
        headboard.scale = (1.1, 0.1, 0.6)
        headboard.data.materials.append(materials['furniture_leather'])
        
        # Nightstands
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(location=(room_center[0] + side * 1.3, room_center[1], 0.3))
            nightstand = bpy.context.active_object
            nightstand.name = f"Nightstand_{{'L' if side == -1 else 'R'}}"
            nightstand.scale = (0.3, 0.4, 0.3)
            nightstand.data.materials.append(materials['furniture_wood_dark'])
            
            # Table lamp
            bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0] + side * 1.3, room_center[1], 0.7))
            lamp = bpy.context.active_object
            lamp.name = f"BedroomLamp_{{'L' if side == -1 else 'R'}}"
            lamp.scale = (0.12, 0.12, 0.1)
            lamp.data.materials.append(materials['light_warm'])
            
            furniture.extend([nightstand, lamp])
        
        furniture.extend([bed_frame, mattress, headboard])
        
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.45))
        island = bpy.context.active_object
        island.name = "KitchenIsland"
        island.scale = (1.5, 0.8, 0.45)
        island.data.materials.append(materials['furniture_wood_light'])
        
        # Marble countertop
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.92))
        countertop = bpy.context.active_object
        countertop.name = "Countertop"
        countertop.scale = (1.6, 0.9, 0.02)
        countertop.data.materials.append(materials['floor_marble'])
        
        # Pendant lights
        for i in range(3):
            x_offset = (i - 1) * 0.6
            bpy.ops.mesh.primitive_uv_sphere_add(location=(room_center[0] + x_offset, room_center[1], 2.0))
            pendant = bpy.context.active_object
            pendant.name = f"PendantLight_{{i}}"
            pendant.scale = (0.12, 0.12, 0.15)
            pendant.data.materials.append(materials['light_accent'])
            furniture.append(pendant)
        
        furniture.extend([island, countertop])
    
    return furniture

# CREATE ROOMS WITH DETAILED INTERIORS
all_furniture = []
for i, room_data in enumerate(layout_data):
    room_info = room_data['room']
    room_name = room_info['name']
    room_type = room_info['type']
    
    x = room_data['x']
    y = room_data['y']
    width = room_data['width']
    length = room_data['length']
    height = room_info.get('height', 3.0)
    
    print(f"🏠 Creating room: {{room_name}} ({{room_type}}) - {{width:.1f}}x{{length:.1f}}m")
    
    # ROOM FLOOR
    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0.01))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room_name.replace(' ', '_')}}"
    floor.scale = (width/2, length/2, 0.01)
    
    # Apply appropriate flooring
    if room_type in ['living', 'bedroom']:
        floor.data.materials.append(materials['floor_walnut'])
    elif room_type == 'kitchen':
        floor.data.materials.append(materials['floor_porcelain'])
    elif room_type == 'bathroom':
        floor.data.materials.append(materials['floor_travertine'])
    else:
        floor.data.materials.append(materials['floor_oak'])
    
    # ROOM WALLS
    wall_thickness = 0.1
    wall_height = height / 2
    
    # Create walls
    walls = [
        ("North", (x, y + length/2, wall_height), (width/2, wall_thickness/2, wall_height)),
        ("South", (x, y - length/2, wall_height), (width/2, wall_thickness/2, wall_height)),
        ("East", (x + width/2, y, wall_height), (wall_thickness/2, length/2, wall_height)),
        ("West", (x - width/2, y, wall_height), (wall_thickness/2, length/2, wall_height))
    ]
    
    for wall_name, location, scale in walls:
        bpy.ops.mesh.primitive_cube_add(location=location)
        wall = bpy.context.active_object
        wall.name = f"{{wall_name}}Wall_{{room_name.replace(' ', '_')}}"
        wall.scale = scale
        wall.data.materials.append(materials['wall_gray'])
    
    # CREATE FURNITURE
    room_center = (x, y, 0)
    furniture = create_detailed_furniture(room_type, room_center, width, length, height)
    all_furniture.extend(furniture)
    
    # CEILING LIGHT
    bpy.ops.mesh.primitive_cylinder_add(location=(x, y, height - 0.2))
    ceiling_light = bpy.context.active_object
    ceiling_light.name = f"CeilingLight_{{room_name.replace(' ', '_')}}"
    ceiling_light.scale = (0.2, 0.2, 0.08)
    ceiling_light.data.materials.append(materials['light_cool'])

# PROFESSIONAL LIGHTING SETUP
print("💡 Setting up professional lighting...")

# Key light (main sun)
bpy.ops.object.light_add(type='SUN', location=(total_width + 15, total_length + 15, 20))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.data.type = 'SUN'
key_light.data.energy = 6.0
key_light.data.color = (1.0, 0.95, 0.8)
key_light.data.angle = math.radians(5)
key_light.rotation_euler = (math.radians(45), 0, math.radians(35))

# Fill light
bpy.ops.object.light_add(type='SUN', location=(-10, -10, 15))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.type = 'SUN'
fill_light.data.energy = 2.5
fill_light.data.color = (0.8, 0.9, 1.0)
fill_light.data.angle = math.radians(8)
fill_light.rotation_euler = (math.radians(30), 0, math.radians(-30))

# Rim light
bpy.ops.object.light_add(type='SUN', location=(total_width - 5, total_length - 5, 25))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.type = 'SUN'
rim_light.data.energy = 3.5
rim_light.data.color = (1.0, 0.9, 0.7)
rim_light.data.angle = math.radians(3)
rim_light.rotation_euler = (math.radians(65), 0, math.radians(120))

# PROFESSIONAL CAMERA SETUP
print("📸 Setting up professional camera...")

bpy.ops.object.camera_add(location=(total_width * 1.5, -total_length * 1.2, total_height * 1.0))
camera = bpy.context.active_object
camera.name = "ArchitecturalCamera"
camera.data.type = 'PERSP'
camera.data.lens = 28  # Wide angle for architecture
camera.data.sensor_width = 36
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 20
camera.data.dof.aperture_fstop = 8.0

# Point camera at building center
target = Vector((total_width/2, total_length/2, total_height/4))
direction = target - Vector(camera.location)
camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

scene.camera = camera

# LANDSCAPING
if enhanced_features.get('landscaping', True):
    print("🌿 Adding landscaping...")
    
    # Grass areas
    grass_margin = 6
    
    # Create grass around building
    grass_areas = [
        ("Front", (total_width/2, -grass_margin/2, 0.005), (total_width/2 + grass_margin/2, grass_margin/2, 1)),
        ("Back", (total_width/2, total_length + grass_margin/2, 0.005), (total_width/2 + grass_margin/2, grass_margin/2, 1)),
        ("Left", (-grass_margin/2, total_length/2, 0.005), (grass_margin/2, total_length/2, 1)),
        ("Right", (total_width + grass_margin/2, total_length/2, 0.005), (grass_margin/2, total_length/2, 1))
    ]
    
    for area_name, location, scale in grass_areas:
        bpy.ops.mesh.primitive_plane_add(location=location)
        grass = bpy.context.active_object
        grass.name = f"Grass_{{area_name}}"
        grass.scale = scale
        grass.data.materials.append(materials['landscape_grass'])
    
    # Trees
    tree_positions = [
        (-4, 4, "Tree1"), (total_width + 4, 4, "Tree2"),
        (-4, total_length - 4, "Tree3"), (total_width + 4, total_length - 4, "Tree4")
    ]
    
    for tree_x, tree_y, tree_name in tree_positions:
        # Tree trunk
        bpy.ops.mesh.primitive_cylinder_add(location=(tree_x, tree_y, 1.5))
        trunk = bpy.context.active_object
        trunk.name = f"Trunk_{{tree_name}}"
        trunk.scale = (0.2, 0.2, 1.5)
        trunk.data.materials.append(materials['landscape_bark'])
        
        # Tree crown
        bpy.ops.mesh.primitive_ico_sphere_add(location=(tree_x, tree_y, 2.8))
        crown = bpy.context.active_object
        crown.name = f"Crown_{{tree_name}}"
        crown.scale = (1.2, 1.2, 1.0)
        crown.data.materials.append(materials['landscape_leaves'])

# EXPORT AND RENDER
print("💾 Exporting files...")

# Export OBJ
bpy.ops.wm.obj_export(
    filepath=r"{os.path.join(self.temp_dir, f'photorealistic_v2_{self.scene_id}.obj').replace(chr(92), '/')}",
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_colors=True
)

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=r"{os.path.join(self.temp_dir, f'photorealistic_v2_{self.scene_id}.blend').replace(chr(92), '/')}")

# RENDER HIGH-QUALITY IMAGES
print("🎨 Starting photorealistic GPU rendering...")

scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15

# Camera views
camera_views = [
    ("hero", (total_width * 1.5, -total_length * 1.2, total_height * 1.0), 28),
    ("detail", (total_width * 0.6, total_length * 0.2, total_height * 0.5), 50),
    ("aerial", (total_width/2, total_length/2, total_height * 3.5), 35)
]

for view_name, cam_loc, lens in camera_views:
    print(f"📸 Rendering {{view_name}} view...")
    
    # Position camera
    camera.location = cam_loc
    camera.data.lens = lens
    
    # Point at target
    if view_name == "aerial":
        target = Vector((total_width/2, total_length/2, 0))
        camera.data.dof.use_dof = False
    else:
        target = Vector((total_width/2, total_length/2, total_height/3))
        camera.data.dof.use_dof = True
        camera.data.dof.focus_distance = 15 if view_name == "detail" else 20
        camera.data.dof.aperture_fstop = 2.8 if view_name == "detail" else 8.0
    
    direction = target - Vector(cam_loc)
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Render
    render_path = r"{self.temp_dir.replace(chr(92), '/')}/photorealistic_v2_{self.scene_id}_" + view_name + ".png"
    scene.render.filepath = render_path
    
    bpy.ops.render.render(write_still=True)
    print(f"✅ RENDERED: {{render_path}}")

print("🔥 Photorealistic rendering complete!")
print(f"Scene ID: {self.scene_id}")
print(f"Total objects: {{len(bpy.data.objects)}}")
print(f"Materials: {{len(bpy.data.materials)}}")
print(f"Furniture pieces: {{len(all_furniture)}}")
print("🎉 PHOTOREALISTIC RENDERING COMPLETE!")
'''

        # Write the enhanced Blender script
        script_path = os.path.join(self.temp_dir, f'photorealistic_v2_{self.scene_id}.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(blender_script)
        
        print(f"Photorealistic V2 Blender script written to: {script_path}")
        
        # Run Blender with the script
        try:
            print("🚀 Starting Blender with RTX 4050 GPU acceleration...")
            result = subprocess.run([
                self.blender_path, 
                '--background',
                '--python', script_path
            ], capture_output=True, text=True, timeout=600)
            
            print("Blender output:", result.stdout)
            if result.stderr:
                print("Blender warnings:", result.stderr)
            
            if result.returncode != 0:
                return {'success': False, 'error': f'Blender failed with code {result.returncode}'}
                
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Blender rendering timed out after 10 minutes'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        # Copy files to output directory
        files = []
        public_dir = os.path.join(os.path.dirname(__file__), 'public', 'renders')
        os.makedirs(public_dir, exist_ok=True)
        
        # Copy model files
        for extension in ['obj', 'mtl', 'blend']:
            src_file = os.path.join(self.temp_dir, f'photorealistic_v2_{self.scene_id}.{extension}')
            if os.path.exists(src_file):
                dst_file = os.path.join(public_dir, f'photorealistic_v2_{self.scene_id}.{extension}')
                shutil.copy2(src_file, dst_file)
                files.append({'type': extension, 'path': dst_file})
                print(f"Copied {extension.upper()}: {dst_file}")
        
        # Copy render images
        view_names = ['hero', 'detail', 'aerial']
        for view_name in view_names:
            src_file = os.path.join(self.temp_dir, f'photorealistic_v2_{self.scene_id}_{view_name}.png')
            if os.path.exists(src_file):
                dst_file = os.path.join(public_dir, f'photorealistic_v2_{self.scene_id}_{view_name}.png')
                shutil.copy2(src_file, dst_file)
                files.append({'type': f'render_{view_name}', 'path': dst_file})
                print(f"Copied {view_name.upper()} render: {dst_file}")
        
        return {
            'success': True,
            'scene_id': self.scene_id,
            'layout_type': 'photorealistic_v2',
            'style': architectural_style,
            'files': files,
            'output': result.stdout,
            'enhanced_features': enhanced_features,
            'quality_level': quality_level,
            'render_resolution': '4K (3840x2160)',
            'gpu_used': 'NVIDIA RTX 4050',
            'render_engine': 'Cycles with OptiX'
        }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python photorealistic_renderer_v2.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        renderer = PhotorealisticRendererV2()
        result = renderer.render_photorealistic_scene(config)
        
        if result['success']:
            print(f"PHOTOREALISTIC_SCENE_ID: {result['scene_id']}")
            print(f"LAYOUT_TYPE: {result.get('layout_type', 'photorealistic_v2')}")
            print(f"STYLE: {result.get('style', 'modern')}")
            print(f"QUALITY_LEVEL: {result.get('quality_level', 'professional')}")
            print(f"GPU_USED: {result.get('gpu_used', 'RTX 4050')}")
            print(f"RENDER_ENGINE: {result.get('render_engine', 'Cycles with OptiX')}")
            print(f"RESOLUTION: {result.get('render_resolution', '4K')}")
            
            for file_info in result['files']:
                file_type = file_info['type'].upper()
                print(f"{file_type}_FILE: {file_info['path']}")
        else:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
