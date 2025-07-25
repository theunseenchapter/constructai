#!/usr/bin/env python3
"""
Photorealistic BOQ Renderer - Professional Quality 3D Architecture
GPU Optimized for RTX 4050 (CUDA Device 0)
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

class PhotorealisticRenderer:
    """Professional photorealistic renderer with advanced materials and lighting"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_photorealistic_')
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
        
        # Create photorealistic Blender script
        layout_json_str = json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        enhanced_features_str = json.dumps(enhanced_features).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        
        blender_script = f'''
import bpy
import bmesh
import math
import random
from mathutils import Vector, Euler
from bpy_extras.object_utils import world_to_camera_view

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

scene = bpy.context.scene

# NVIDIA RTX 4050 GPU SETUP (CUDA Device 0)
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

# PROFESSIONAL QUALITY RENDER SETTINGS
scene.cycles.samples = 2048  # High quality samples
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'  # NVIDIA OptiX denoiser
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.005  # Very fine threshold
scene.cycles.time_limit = 0  # No time limit
scene.cycles.use_preview_denoising = True

# PROFESSIONAL CAMERA SETTINGS
scene.render.resolution_x = 3840  # 4K resolution
scene.render.resolution_y = 2160
scene.render.resolution_percentage = 100
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5

# COLOR MANAGEMENT FOR PHOTOREALISM
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - High Contrast'
scene.view_settings.exposure = 0.5
scene.view_settings.gamma = 1.0

# WORLD SETTINGS FOR REALISTIC LIGHTING
world = bpy.data.worlds.new("PhotorealisticWorld")
scene.world = world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_nodes.clear()

# Create HDRI environment
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

# Set environment strength
background.inputs["Strength"].default_value = 1.5

# Rotate environment for better lighting
mapping.inputs["Rotation"].default_value = (0, 0, math.radians(45))

def create_photorealistic_material(name, base_color, roughness=0.5, metallic=0.0, 
                                 emission=None, emission_strength=1.0, 
                                 normal_strength=1.0, bump_strength=0.0,
                                 subsurface=0.0, subsurface_color=None,
                                 transmission=0.0, ior=1.45, alpha=1.0,
                                 clearcoat=0.0, clearcoat_roughness=0.0,
                                 anisotropic=0.0, anisotropic_rotation=0.0,
                                 sheen=0.0, sheen_tint=0.0, specular=0.5):
    """Create a photorealistic material with advanced properties"""
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.use_backface_culling = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Main BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Set basic properties (compatible with Blender 4.4+)
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["IOR"].default_value = ior
    bsdf.inputs["Alpha"].default_value = alpha
    
    # Handle Specular input (different names in different Blender versions)
    if "Specular" in bsdf.inputs:
        bsdf.inputs["Specular"].default_value = specular
    elif "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = specular
    
    # Advanced properties (compatible with Blender 4.4+)
    try:
        if "Clearcoat Weight" in bsdf.inputs:
            bsdf.inputs["Clearcoat Weight"].default_value = clearcoat
        elif "Clearcoat" in bsdf.inputs:
            bsdf.inputs["Clearcoat"].default_value = clearcoat
        
        if "Clearcoat Roughness" in bsdf.inputs:
            bsdf.inputs["Clearcoat Roughness"].default_value = clearcoat_roughness
    except KeyError:
        pass  # Skip if not available in this Blender version
    
    try:
        if "Sheen Weight" in bsdf.inputs:
            bsdf.inputs["Sheen Weight"].default_value = sheen
        elif "Sheen" in bsdf.inputs:
            bsdf.inputs["Sheen"].default_value = sheen
        
        if "Sheen Tint" in bsdf.inputs:
            bsdf.inputs["Sheen Tint"].default_value = sheen_tint
    except KeyError:
        pass  # Skip if not available in this Blender version
    
    try:
        if "Anisotropic" in bsdf.inputs:
            bsdf.inputs["Anisotropic"].default_value = anisotropic
        if "Anisotropic Rotation" in bsdf.inputs:
            bsdf.inputs["Anisotropic Rotation"].default_value = anisotropic_rotation
    except KeyError:
        pass  # Skip if not available in this Blender version
    
    # Subsurface scattering (compatible with Blender 4.4+)
    if subsurface > 0:
        try:
            if "Subsurface Weight" in bsdf.inputs:
                bsdf.inputs["Subsurface Weight"].default_value = subsurface
            elif "Subsurface" in bsdf.inputs:
                bsdf.inputs["Subsurface"].default_value = subsurface
            
            if subsurface_color:
                if "Subsurface Color" in bsdf.inputs:
                    bsdf.inputs["Subsurface Color"].default_value = (*subsurface_color, 1.0)
            else:
                if "Subsurface Color" in bsdf.inputs:
                    bsdf.inputs["Subsurface Color"].default_value = (*base_color, 1.0)
        except KeyError:
            pass  # Skip if not available in this Blender version
    
    # Transmission for glass (compatible with Blender 4.4+)
    if transmission > 0:
        try:
            if "Transmission Weight" in bsdf.inputs:
                bsdf.inputs["Transmission Weight"].default_value = transmission
            elif "Transmission" in bsdf.inputs:
                bsdf.inputs["Transmission"].default_value = transmission
        except KeyError:
            pass  # Skip if not available in this Blender version
    
    # Emission for lights (compatible with Blender 4.4+)
    if emission:
        try:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = (*emission, 1.0)
            
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
        except KeyError:
            pass  # Skip if not available in this Blender version
    
    # ADVANCED TEXTURE GENERATION
    if normal_strength > 0 or bump_strength > 0:
        # Create noise texture for surface detail
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-800, 0)
        noise.inputs["Scale"].default_value = 20.0
        noise.inputs["Detail"].default_value = 15.0
        noise.inputs["Roughness"].default_value = 0.5
        noise.inputs["Distortion"].default_value = 0.0
        
        # Create color ramp for contrast
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (-600, 0)
        color_ramp.color_ramp.elements[0].position = 0.4
        color_ramp.color_ramp.elements[1].position = 0.6
        
        # Link noise to color ramp
        mat.node_tree.links.new(noise.outputs["Fac"], color_ramp.inputs["Fac"])
        
        # Normal mapping
        if normal_strength > 0:
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            normal_map.location = (-200, -200)
            normal_map.inputs["Strength"].default_value = normal_strength
            
            mat.node_tree.links.new(color_ramp.outputs["Color"], normal_map.inputs["Color"])
            mat.node_tree.links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
        
        # Bump mapping
        if bump_strength > 0:
            bump = nodes.new(type='ShaderNodeBump')
            bump.location = (-200, -400)
            bump.inputs["Strength"].default_value = bump_strength
            
            mat.node_tree.links.new(color_ramp.outputs["Color"], bump.inputs["Height"])
            if normal_strength > 0:
                mat.node_tree.links.new(bump.outputs["Normal"], normal_map.inputs["Normal"])
            else:
                mat.node_tree.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    
    # COLOR VARIATION for realism
    if True:  # Always add subtle color variation
        color_noise = nodes.new(type='ShaderNodeTexNoise')
        color_noise.location = (-800, 300)
        color_noise.inputs["Scale"].default_value = 50.0
        color_noise.inputs["Detail"].default_value = 5.0
        
        color_mix = nodes.new(type='ShaderNodeMixRGB')
        color_mix.location = (-400, 200)
        color_mix.blend_type = 'MULTIPLY'
        color_mix.inputs["Fac"].default_value = 0.1
        color_mix.inputs["Color1"].default_value = (*base_color, 1.0)
        
        # Slightly varied color
        varied_color = [min(1.0, max(0.0, c + random.uniform(-0.05, 0.05))) for c in base_color]
        color_mix.inputs["Color2"].default_value = (*varied_color, 1.0)
        
        mat.node_tree.links.new(color_noise.outputs["Fac"], color_mix.inputs["Fac"])
        mat.node_tree.links.new(color_mix.outputs["Color"], bsdf.inputs["Base Color"])
    
    # Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    
    return mat

# PHOTOREALISTIC MATERIAL LIBRARY
print("🎨 Creating photorealistic materials...")

materials = {{
    # PREMIUM FLOORING
    'floor_carrara_marble': create_photorealistic_material(
        "Carrara Marble Floor", (0.98, 0.97, 0.95), 
        roughness=0.02, metallic=0.0, normal_strength=0.8, 
        subsurface=0.05, ior=1.544, clearcoat=0.1
    ),
    'floor_walnut_hardwood': create_photorealistic_material(
        "Walnut Hardwood Floor", (0.35, 0.20, 0.12), 
        roughness=0.3, metallic=0.0, normal_strength=1.2, 
        bump_strength=0.5, clearcoat=0.8, clearcoat_roughness=0.1
    ),
    'floor_oak_engineered': create_photorealistic_material(
        "Oak Engineered Floor", (0.55, 0.35, 0.20), 
        roughness=0.25, metallic=0.0, normal_strength=1.0, 
        bump_strength=0.3, clearcoat=0.6, clearcoat_roughness=0.2
    ),
    'floor_porcelain_large': create_photorealistic_material(
        "Large Format Porcelain", (0.92, 0.90, 0.88), 
        roughness=0.05, metallic=0.0, normal_strength=0.3, 
        specular=0.8, clearcoat=0.2
    ),
    'floor_travertine_honed': create_photorealistic_material(
        "Honed Travertine Floor", (0.88, 0.82, 0.72), 
        roughness=0.4, metallic=0.0, normal_strength=1.0, 
        bump_strength=0.8, subsurface=0.02
    ),
    
    # SOPHISTICATED WALLS
    'wall_venetian_plaster': create_photorealistic_material(
        "Venetian Plaster Wall", (0.95, 0.93, 0.90), 
        roughness=0.3, metallic=0.0, normal_strength=0.6, 
        bump_strength=0.4, subsurface=0.02
    ),
    'wall_designer_gray': create_photorealistic_material(
        "Designer Gray Paint", (0.75, 0.75, 0.78), 
        roughness=0.8, metallic=0.0, normal_strength=0.2
    ),
    'wall_linen_white': create_photorealistic_material(
        "Linen White Paint", (0.95, 0.94, 0.92), 
        roughness=0.9, metallic=0.0, normal_strength=0.1
    ),
    'wall_natural_stone': create_photorealistic_material(
        "Natural Stone Wall", (0.75, 0.70, 0.65), 
        roughness=0.7, metallic=0.0, normal_strength=1.5, 
        bump_strength=1.0, subsurface=0.01
    ),
    'wall_wood_paneling': create_photorealistic_material(
        "Wood Wall Paneling", (0.45, 0.35, 0.25), 
        roughness=0.4, metallic=0.0, normal_strength=0.8, 
        bump_strength=0.6, clearcoat=0.3
    ),
    
    # LUXURY FURNITURE
    'furniture_premium_leather': create_photorealistic_material(
        "Premium Leather", (0.35, 0.20, 0.12), 
        roughness=0.2, metallic=0.0, normal_strength=0.5, 
        subsurface=0.1, clearcoat=0.2, clearcoat_roughness=0.3
    ),
    'furniture_mahogany_wood': create_photorealistic_material(
        "Mahogany Wood", (0.42, 0.18, 0.10), 
        roughness=0.25, metallic=0.0, normal_strength=0.8, 
        bump_strength=0.4, clearcoat=0.7, clearcoat_roughness=0.1
    ),
    'furniture_linen_fabric': create_photorealistic_material(
        "Linen Fabric", (0.88, 0.82, 0.75), 
        roughness=0.9, metallic=0.0, normal_strength=1.2, 
        sheen=0.2, sheen_tint=0.1
    ),
    'furniture_velvet_fabric': create_photorealistic_material(
        "Velvet Fabric", (0.25, 0.35, 0.55), 
        roughness=0.95, metallic=0.0, normal_strength=0.8, 
        sheen=0.8, sheen_tint=0.3, subsurface=0.05
    ),
    
    # PREMIUM METALS
    'metal_brushed_steel': create_photorealistic_material(
        "Brushed Stainless Steel", (0.85, 0.85, 0.85), 
        roughness=0.15, metallic=0.95, normal_strength=0.5, 
        anisotropic=0.8, anisotropic_rotation=0.0
    ),
    'metal_brass_satin': create_photorealistic_material(
        "Satin Brass", (0.85, 0.70, 0.35), 
        roughness=0.2, metallic=0.9, normal_strength=0.3, 
        clearcoat=0.1
    ),
    'metal_black_steel': create_photorealistic_material(
        "Black Steel", (0.05, 0.05, 0.05), 
        roughness=0.3, metallic=0.8, normal_strength=0.4
    ),
    
    # PREMIUM GLASS
    'glass_ultra_clear': create_photorealistic_material(
        "Ultra Clear Glass", (0.98, 0.98, 0.98), 
        roughness=0.0, metallic=0.0, transmission=0.95, 
        ior=1.52, alpha=0.1
    ),
    'glass_frosted': create_photorealistic_material(
        "Frosted Glass", (0.95, 0.95, 0.95), 
        roughness=0.8, metallic=0.0, transmission=0.7, 
        ior=1.45, alpha=0.3, normal_strength=0.8
    ),
    
    # LIGHTING MATERIALS
    'light_warm_led': create_photorealistic_material(
        "Warm LED Light", (1.0, 0.9, 0.7), 
        roughness=0.0, metallic=0.0, 
        emission=(1.0, 0.9, 0.7), emission_strength=50.0
    ),
    'light_cool_led': create_photorealistic_material(
        "Cool LED Light", (0.9, 0.95, 1.0), 
        roughness=0.0, metallic=0.0, 
        emission=(0.9, 0.95, 1.0), emission_strength=30.0
    ),
    'light_accent_warm': create_photorealistic_material(
        "Accent Warm Light", (1.0, 0.8, 0.5), 
        roughness=0.0, metallic=0.0, 
        emission=(1.0, 0.8, 0.5), emission_strength=20.0
    ),
    
    # LANDSCAPE MATERIALS
    'landscape_grass': create_photorealistic_material(
        "Natural Grass", (0.25, 0.55, 0.25), 
        roughness=0.9, metallic=0.0, normal_strength=1.5, 
        subsurface=0.3, subsurface_color=(0.4, 0.8, 0.3)
    ),
    'landscape_soil': create_photorealistic_material(
        "Rich Soil", (0.35, 0.25, 0.15), 
        roughness=0.95, metallic=0.0, normal_strength=1.8, 
        bump_strength=1.2
    ),
    'landscape_tree_bark': create_photorealistic_material(
        "Tree Bark", (0.35, 0.25, 0.18), 
        roughness=0.9, metallic=0.0, normal_strength=2.0, 
        bump_strength=1.5, subsurface=0.05
    ),
    'landscape_tree_leaves': create_photorealistic_material(
        "Tree Leaves", (0.30, 0.60, 0.25), 
        roughness=0.8, metallic=0.0, normal_strength=1.0, 
        subsurface=0.8, subsurface_color=(0.5, 0.9, 0.4),
        alpha=0.8
    ),
    
    # ARCHITECTURAL CONCRETE
    'concrete_architectural': create_photorealistic_material(
        "Architectural Concrete", (0.7, 0.68, 0.65), 
        roughness=0.8, metallic=0.0, normal_strength=1.0, 
        bump_strength=0.8
    ),
}}

print(f"✅ Created {{len(materials)}} photorealistic materials")

# Building dimensions
total_width = {building_dims['total_width']}
total_length = {building_dims['total_length']}
total_height = {building_dims.get('height', 12)}

# Enhanced features
enhanced_features = {enhanced_features_str}

print(f"🏗️ Building: {{total_width}}x{{total_length}}x{{total_height}}m")
print(f"🎛️ Enhanced features: {{enhanced_features}}")

# CREATE FOUNDATION
bpy.ops.mesh.primitive_plane_add(size=1, location=(total_width/2, total_length/2, -0.1))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (total_width/2 + 2, total_length/2 + 2, 1)
foundation.data.materials.append(materials['concrete_architectural'])

# CREATE EXTERIOR WALLS
wall_thickness = 0.3
wall_height = 3.0

# North wall
bpy.ops.mesh.primitive_cube_add(location=(total_width/2, total_length + wall_thickness/2, wall_height/2))
north_wall = bpy.context.active_object
north_wall.name = "ExteriorWall_North"
north_wall.scale = (total_width/2 + wall_thickness/2, wall_thickness/2, wall_height/2)
north_wall.data.materials.append(materials['wall_natural_stone'])

# South wall
bpy.ops.mesh.primitive_cube_add(location=(total_width/2, -wall_thickness/2, wall_height/2))
south_wall = bpy.context.active_object
south_wall.name = "ExteriorWall_South"
south_wall.scale = (total_width/2 + wall_thickness/2, wall_thickness/2, wall_height/2)
south_wall.data.materials.append(materials['wall_natural_stone'])

# East wall
bpy.ops.mesh.primitive_cube_add(location=(total_width + wall_thickness/2, total_length/2, wall_height/2))
east_wall = bpy.context.active_object
east_wall.name = "ExteriorWall_East"
east_wall.scale = (wall_thickness/2, total_length/2, wall_height/2)
east_wall.data.materials.append(materials['wall_natural_stone'])

# West wall
bpy.ops.mesh.primitive_cube_add(location=(-wall_thickness/2, total_length/2, wall_height/2))
west_wall = bpy.context.active_object
west_wall.name = "ExteriorWall_West"
west_wall.scale = (wall_thickness/2, total_length/2, wall_height/2)
west_wall.data.materials.append(materials['wall_natural_stone'])

# Layout data
layout_data = {layout_json_str}

print(f"🏠 Creating {{len(layout_data)}} rooms with photorealistic details")

def create_advanced_furniture(room_type, room_center, room_width, room_length, room_height):
    """Create detailed furniture with proper materials"""
    furniture_objects = []
    
    if room_type == 'living':
        # Modern sectional sofa
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - room_length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "ModernSofa"
        sofa.scale = (2.0, 0.5, 0.4)
        sofa.data.materials.append(materials['furniture_premium_leather'])
        
        # Add sofa back
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - room_length/4 - 0.4, 0.8))
        sofa_back = bpy.context.active_object
        sofa_back.name = "SofaBack"
        sofa_back.scale = (2.0, 0.1, 0.4)
        sofa_back.data.materials.append(materials['furniture_premium_leather'])
        
        # Coffee table with glass top
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] + 0.5, 0.15))
        table_base = bpy.context.active_object
        table_base.name = "CoffeeTableBase"
        table_base.scale = (0.8, 0.4, 0.15)
        table_base.data.materials.append(materials['furniture_mahogany_wood'])
        
        # Glass top
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] + 0.5, 0.32))
        table_top = bpy.context.active_object
        table_top.name = "CoffeeTableTop"
        table_top.scale = (0.9, 0.5, 0.02)
        table_top.data.materials.append(materials['glass_ultra_clear'])
        
        # Floor lamp
        bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0] + 2, room_center[1] - 2, 0.8))
        lamp_base = bpy.context.active_object
        lamp_base.name = "FloorLampBase"
        lamp_base.scale = (0.05, 0.05, 0.8)
        lamp_base.data.materials.append(materials['metal_brushed_steel'])
        
        # Lamp shade
        bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0] + 2, room_center[1] - 2, 1.8))
        lamp_shade = bpy.context.active_object
        lamp_shade.name = "FloorLampShade"
        lamp_shade.scale = (0.3, 0.3, 0.2)
        lamp_shade.data.materials.append(materials['furniture_linen_fabric'])
        
        furniture_objects.extend([sofa, sofa_back, table_base, table_top, lamp_base, lamp_shade])
        
    elif room_type == 'bedroom':
        # Platform bed
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.2))
        bed_base = bpy.context.active_object
        bed_base.name = "BedBase"
        bed_base.scale = (1.0, 1.5, 0.2)
        bed_base.data.materials.append(materials['furniture_mahogany_wood'])
        
        # Mattress
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.45))
        mattress = bpy.context.active_object
        mattress.name = "Mattress"
        mattress.scale = (0.95, 1.45, 0.15)
        mattress.data.materials.append(materials['furniture_linen_fabric'])
        
        # Headboard
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - 1.5, 0.8))
        headboard = bpy.context.active_object
        headboard.name = "Headboard"
        headboard.scale = (1.2, 0.1, 0.6)
        headboard.data.materials.append(materials['furniture_velvet_fabric'])
        
        # Nightstands
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(location=(room_center[0] + side * 1.5, room_center[1], 0.3))
            nightstand = bpy.context.active_object
            nightstand.name = f"Nightstand_{{'L' if side == -1 else 'R'}}"
            nightstand.scale = (0.4, 0.4, 0.3)
            nightstand.data.materials.append(materials['furniture_mahogany_wood'])
            
            # Table lamp
            bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0] + side * 1.5, room_center[1], 0.75))
            lamp = bpy.context.active_object
            lamp.name = f"TableLamp_{{'L' if side == -1 else 'R'}}"
            lamp.scale = (0.15, 0.15, 0.15)
            lamp.data.materials.append(materials['light_warm_led'])
            
            furniture_objects.extend([nightstand, lamp])
        
        furniture_objects.extend([bed_base, mattress, headboard])
        
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.45))
        island = bpy.context.active_object
        island.name = "KitchenIsland"
        island.scale = (1.5, 0.8, 0.45)
        island.data.materials.append(materials['furniture_mahogany_wood'])
        
        # Marble countertop
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.92))
        countertop = bpy.context.active_object
        countertop.name = "MarbleCountertop"
        countertop.scale = (1.6, 0.9, 0.02)
        countertop.data.materials.append(materials['floor_carrara_marble'])
        
        # Pendant lights
        for i in range(3):
            x_offset = (i - 1) * 0.8
            bpy.ops.mesh.primitive_uv_sphere_add(location=(room_center[0] + x_offset, room_center[1], 2.2))
            pendant = bpy.context.active_object
            pendant.name = f"PendantLight_{{i}}"
            pendant.scale = (0.15, 0.15, 0.2)
            pendant.data.materials.append(materials['light_accent_warm'])
            furniture_objects.append(pendant)
        
        # Upper cabinets
        for i in range(4):
            x_offset = (i - 1.5) * 0.6
            bpy.ops.mesh.primitive_cube_add(location=(room_center[0] + x_offset, room_center[1] + room_length/3, 2.0))
            cabinet = bpy.context.active_object
            cabinet.name = f"UpperCabinet_{{i}}"
            cabinet.scale = (0.25, 0.3, 0.4)
            cabinet.data.materials.append(materials['furniture_mahogany_wood'])
            furniture_objects.append(cabinet)
        
        furniture_objects.extend([island, countertop])
    
    return furniture_objects

def create_architectural_details(room_type, room_center, room_width, room_length, room_height):
    """Create architectural details like moldings, trim, etc."""
    details = []
    
    # Crown molding
    molding_height = room_height - 0.1
    for wall_side in ['north', 'south', 'east', 'west']:
        if wall_side == 'north':
            location = (room_center[0], room_center[1] + room_length/2 - 0.05, molding_height)
            scale = (room_width/2, 0.05, 0.05)
        elif wall_side == 'south':
            location = (room_center[0], room_center[1] - room_length/2 + 0.05, molding_height)
            scale = (room_width/2, 0.05, 0.05)
        elif wall_side == 'east':
            location = (room_center[0] + room_width/2 - 0.05, room_center[1], molding_height)
            scale = (0.05, room_length/2, 0.05)
        elif wall_side == 'west':
            location = (room_center[0] - room_width/2 + 0.05, room_center[1], molding_height)
            scale = (0.05, room_length/2, 0.05)
        
        bpy.ops.mesh.primitive_cube_add(location=location)
        molding = bpy.context.active_object
        molding.name = f"CrownMolding_{{wall_side}}"
        molding.scale = scale
        molding.data.materials.append(materials['wall_linen_white'])
        details.append(molding)
    
    # Baseboard
    for wall_side in ['north', 'south', 'east', 'west']:
        if wall_side == 'north':
            location = (room_center[0], room_center[1] + room_length/2 - 0.05, 0.05)
            scale = (room_width/2, 0.05, 0.05)
        elif wall_side == 'south':
            location = (room_center[0], room_center[1] - room_length/2 + 0.05, 0.05)
            scale = (room_width/2, 0.05, 0.05)
        elif wall_side == 'east':
            location = (room_center[0] + room_width/2 - 0.05, room_center[1], 0.05)
            scale = (0.05, room_length/2, 0.05)
        elif wall_side == 'west':
            location = (room_center[0] - room_width/2 + 0.05, room_center[1], 0.05)
            scale = (0.05, room_length/2, 0.05)
        
        bpy.ops.mesh.primitive_cube_add(location=location)
        baseboard = bpy.context.active_object
        baseboard.name = f"Baseboard_{{wall_side}}"
        baseboard.scale = scale
        baseboard.data.materials.append(materials['wall_linen_white'])
        details.append(baseboard)
    
    # Ceiling light fixture
    bpy.ops.mesh.primitive_cylinder_add(location=(room_center[0], room_center[1], room_height - 0.3))
    ceiling_light = bpy.context.active_object
    ceiling_light.name = f"CeilingLight_{{room_type}}"
    ceiling_light.scale = (0.3, 0.3, 0.1)
    ceiling_light.data.materials.append(materials['light_cool_led'])
    details.append(ceiling_light)
    
    return details

# CREATE ROOMS WITH PHOTOREALISTIC DETAILS
all_furniture = []
all_details = []

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
    
    # ROOM FLOOR with premium materials
    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0.01))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room_name.replace(' ', '_')}}"
    floor.scale = (width/2, length/2, 0.01)
    
    # Apply appropriate flooring material
    if room_type in ['living', 'bedroom']:
        floor.data.materials.append(materials['floor_walnut_hardwood'])
    elif room_type == 'kitchen':
        floor.data.materials.append(materials['floor_porcelain_large'])
    elif room_type == 'bathroom':
        floor.data.materials.append(materials['floor_travertine_honed'])
    else:
        floor.data.materials.append(materials['floor_oak_engineered'])
    
    # ROOM WALLS
    wall_thickness = 0.1
    wall_height = height / 2
    
    # North wall
    bpy.ops.mesh.primitive_cube_add(location=(x, y + length/2, wall_height))
    north_wall = bpy.context.active_object
    north_wall.name = f"NorthWall_{{room_name.replace(' ', '_')}}"
    north_wall.scale = (width/2, wall_thickness/2, wall_height)
    north_wall.data.materials.append(materials['wall_designer_gray'])
    
    # South wall
    bpy.ops.mesh.primitive_cube_add(location=(x, y - length/2, wall_height))
    south_wall = bpy.context.active_object
    south_wall.name = f"SouthWall_{{room_name.replace(' ', '_')}}"
    south_wall.scale = (width/2, wall_thickness/2, wall_height)
    south_wall.data.materials.append(materials['wall_designer_gray'])
    
    # East wall
    bpy.ops.mesh.primitive_cube_add(location=(x + width/2, y, wall_height))
    east_wall = bpy.context.active_object
    east_wall.name = f"EastWall_{{room_name.replace(' ', '_')}}"
    east_wall.scale = (wall_thickness/2, length/2, wall_height)
    east_wall.data.materials.append(materials['wall_designer_gray'])
    
    # West wall
    bpy.ops.mesh.primitive_cube_add(location=(x - width/2, y, wall_height))
    west_wall = bpy.context.active_object
    west_wall.name = f"WestWall_{{room_name.replace(' ', '_')}}"
    west_wall.scale = (wall_thickness/2, length/2, wall_height)
    west_wall.data.materials.append(materials['wall_designer_gray'])
    
    # CREATE FURNITURE
    if enhanced_features.get('furniture', True):
        room_center = (x, y, 0)
        furniture = create_advanced_furniture(room_type, room_center, width, length, height)
        all_furniture.extend(furniture)
    
    # CREATE ARCHITECTURAL DETAILS
    if enhanced_features.get('interiorDetails', True):
        details = create_architectural_details(room_type, (x, y, 0), width, length, height)
        all_details.extend(details)

# PROFESSIONAL LIGHTING SETUP
print("💡 Setting up professional lighting...")

# Key light (main sun)
bpy.ops.object.light_add(type='SUN', location=(total_width + 20, total_length + 20, 25))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.data.type = 'SUN'
key_light.data.energy = 8.0
key_light.data.color = (1.0, 0.95, 0.8)  # Warm daylight
key_light.data.angle = math.radians(5)  # Soft shadows
key_light.rotation_euler = (math.radians(45), 0, math.radians(35))

# Fill light (softer secondary)
bpy.ops.object.light_add(type='SUN', location=(-15, -15, 18))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.type = 'SUN'
fill_light.data.energy = 3.0
fill_light.data.color = (0.8, 0.9, 1.0)  # Cool fill
fill_light.data.angle = math.radians(10)
fill_light.rotation_euler = (math.radians(25), 0, math.radians(-30))

# Rim light (edge definition)
bpy.ops.object.light_add(type='SUN', location=(total_width - 10, total_length - 10, 30))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.type = 'SUN'
rim_light.data.energy = 4.0
rim_light.data.color = (1.0, 0.9, 0.7)  # Warm rim
rim_light.data.angle = math.radians(3)
rim_light.rotation_euler = (math.radians(70), 0, math.radians(120))

# PROFESSIONAL CAMERA SETUP
print("📸 Setting up professional camera...")

# Hero camera (main architectural view)
bpy.ops.object.camera_add(location=(total_width * 1.8, -total_length * 1.5, total_height * 1.2))
hero_camera = bpy.context.active_object
hero_camera.name = "HeroCamera"
hero_camera.data.type = 'PERSP'
hero_camera.data.lens = 24  # Wide angle for architecture
hero_camera.data.sensor_width = 36  # Full frame sensor
hero_camera.data.dof.use_dof = True
hero_camera.data.dof.focus_distance = 25
hero_camera.data.dof.aperture_fstop = 8.0  # Sharp focus

# Point camera toward building center
target = Vector((total_width/2, total_length/2, total_height/4))
direction = target - Vector(hero_camera.location)
hero_camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Set as active camera
scene.camera = hero_camera

# LANDSCAPING (if enabled)
if enhanced_features.get('landscaping', True):
    print("🌿 Creating landscaping...")
    
    # Grass areas
    grass_margin = 8
    
    # Front yard
    bpy.ops.mesh.primitive_plane_add(location=(total_width/2, -grass_margin/2, 0.01))
    front_yard = bpy.context.active_object
    front_yard.name = "FrontYard"
    front_yard.scale = (total_width/2 + grass_margin/2, grass_margin/2, 1)
    front_yard.data.materials.append(materials['landscape_grass'])
    
    # Back yard
    bpy.ops.mesh.primitive_plane_add(location=(total_width/2, total_length + grass_margin/2, 0.01))
    back_yard = bpy.context.active_object
    back_yard.name = "BackYard"
    back_yard.scale = (total_width/2 + grass_margin/2, grass_margin/2, 1)
    back_yard.data.materials.append(materials['landscape_grass'])
    
    # Side yards
    bpy.ops.mesh.primitive_plane_add(location=(-grass_margin/2, total_length/2, 0.01))
    left_yard = bpy.context.active_object
    left_yard.name = "LeftYard"
    left_yard.scale = (grass_margin/2, total_length/2, 1)
    left_yard.data.materials.append(materials['landscape_grass'])
    
    bpy.ops.mesh.primitive_plane_add(location=(total_width + grass_margin/2, total_length/2, 0.01))
    right_yard = bpy.context.active_object
    right_yard.name = "RightYard"
    right_yard.scale = (grass_margin/2, total_length/2, 1)
    right_yard.data.materials.append(materials['landscape_grass'])
    
    # Trees
    tree_positions = [
        (-5, 5, "Oak1"),
        (total_width + 5, 5, "Oak2"),
        (-5, total_length - 5, "Oak3"),
        (total_width + 5, total_length - 5, "Oak4"),
        (total_width/2, -6, "Oak5"),
        (total_width/2, total_length + 6, "Oak6")
    ]
    
    for tree_x, tree_y, tree_name in tree_positions:
        # Tree trunk
        bpy.ops.mesh.primitive_cylinder_add(location=(tree_x, tree_y, 2.0))
        trunk = bpy.context.active_object
        trunk.name = f"TreeTrunk_{{tree_name}}"
        trunk.scale = (0.3, 0.3, 2.0)
        trunk.data.materials.append(materials['landscape_tree_bark'])
        
        # Tree crown
        bpy.ops.mesh.primitive_ico_sphere_add(location=(tree_x, tree_y, 3.5))
        crown = bpy.context.active_object
        crown.name = f"TreeCrown_{{tree_name}}"
        crown.scale = (1.5, 1.5, 1.2)
        crown.data.materials.append(materials['landscape_tree_leaves'])
        
        # Add randomness to tree crown
        crown.rotation_euler = (0, 0, random.uniform(0, math.pi))

# EXPORT FILES
print("💾 Exporting files...")

# Export OBJ with materials
bpy.ops.wm.obj_export(
    filepath=r"{os.path.join(self.temp_dir, f'photorealistic_{self.scene_id}.obj').replace(chr(92), '/')}",
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_colors=True,
    export_vertex_groups=True
)

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=r"{os.path.join(self.temp_dir, f'photorealistic_{self.scene_id}.blend').replace(chr(92), '/')}")

# RENDER HIGH-QUALITY IMAGES
print("🎨 Starting photorealistic GPU rendering...")

# Final render settings
scene.render.resolution_x = 3840  # 4K
scene.render.resolution_y = 2160
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15

# Multiple camera views for comprehensive visualization
camera_views = [
    ("hero", (total_width * 1.8, -total_length * 1.5, total_height * 1.2), "Main architectural view"),
    ("detail", (total_width * 0.7, total_length * 0.2, total_height * 0.6), "Interior detail view"),
    ("aerial", (total_width/2, total_length/2, total_height * 4), "Aerial plan view"),
    ("corner", (total_width * 1.3, total_length * 1.3, total_height * 0.8), "Corner perspective")
]

render_files = []
for view_name, cam_loc, description in camera_views:
    print(f"📸 Rendering {{view_name}} view: {{description}}")
    
    # Position camera
    hero_camera.location = cam_loc
    
    # Point camera at building center
    if view_name == "aerial":
        target = Vector((total_width/2, total_length/2, 0))
    else:
        target = Vector((total_width/2, total_length/2, total_height/3))
    
    direction = target - Vector(cam_loc)
    hero_camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Adjust camera settings per view
    if view_name == "detail":
        hero_camera.data.lens = 50  # Normal lens for detail
        hero_camera.data.dof.focus_distance = 10
        hero_camera.data.dof.aperture_fstop = 2.8  # Shallow depth of field
    elif view_name == "aerial":
        hero_camera.data.lens = 35  # Wide angle for aerial
        hero_camera.data.dof.use_dof = False  # No DOF for aerial
    else:
        hero_camera.data.lens = 24  # Wide angle for architecture
        hero_camera.data.dof.focus_distance = 25
        hero_camera.data.dof.aperture_fstop = 8.0  # Sharp focus
    
    # Set render path
    render_path = r"{self.temp_dir.replace(chr(92), '/')}/photorealistic_{self.scene_id}_" + view_name + ".png"
    scene.render.filepath = render_path
    
    # RENDER (Uses GPU!)
    bpy.ops.render.render(write_still=True)
    render_files.append(render_path)
    print(f"✅ RENDERED: {{render_path}}")

print("🔥 Photorealistic GPU rendering complete!")
print("=" * 60)
print("PHOTOREALISTIC RENDERING SUMMARY")
print("=" * 60)
print(f"Scene ID: {self.scene_id}")
print(f"Total Objects: {{len(bpy.data.objects)}}")
print(f"Materials: {{len(bpy.data.materials)}}")
print(f"Furniture Pieces: {{len(all_furniture)}}")
print(f"Architectural Details: {{len(all_details)}}")
print(f"Render Views: {{len(render_files)}}")
print(f"Building Size: {{total_width}}x{{total_length}}x{{total_height}}m")
print(f"Enhanced Features: {{enhanced_features}}")

for i, render_file in enumerate(render_files):
    print(f"RENDER_PNG_{{i+1}}: {{render_file}}")

print("🎉 PHOTOREALISTIC RENDERING COMPLETE!")
'''

        # Write the enhanced Blender script
        script_path = os.path.join(self.temp_dir, f'photorealistic_{self.scene_id}.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(blender_script)
        
        print(f"Photorealistic Blender script written to: {script_path}")
        
        # Run Blender with the script
        try:
            print("🚀 Starting Blender with RTX 4050 GPU acceleration...")
            result = subprocess.run([
                self.blender_path, 
                '--background',
                '--python', script_path
            ], capture_output=True, text=True, timeout=600)  # 10 minute timeout
            
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
            src_file = os.path.join(self.temp_dir, f'photorealistic_{self.scene_id}.{extension}')
            if os.path.exists(src_file):
                dst_file = os.path.join(public_dir, f'photorealistic_{self.scene_id}.{extension}')
                shutil.copy2(src_file, dst_file)
                files.append({'type': extension, 'path': dst_file})
                print(f"Copied {extension.upper()}: {dst_file}")
        
        # Copy render images
        view_names = ['hero', 'detail', 'aerial', 'corner']
        for view_name in view_names:
            src_file = os.path.join(self.temp_dir, f'photorealistic_{self.scene_id}_{view_name}.png')
            if os.path.exists(src_file):
                dst_file = os.path.join(public_dir, f'photorealistic_{self.scene_id}_{view_name}.png')
                shutil.copy2(src_file, dst_file)
                files.append({'type': f'render_{view_name}', 'path': dst_file})
                print(f"Copied {view_name.upper()} render: {dst_file}")
        
        return {
            'success': True,
            'scene_id': self.scene_id,
            'layout_type': 'photorealistic',
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
        print("Usage: python photorealistic_renderer.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        renderer = PhotorealisticRenderer()
        result = renderer.render_photorealistic_scene(config)
        
        if result['success']:
            print(f"PHOTOREALISTIC_SCENE_ID: {result['scene_id']}")
            print(f"LAYOUT_TYPE: {result.get('layout_type', 'photorealistic')}")
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
