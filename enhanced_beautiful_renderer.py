#!/usr/bin/env python3
"""
Enhanced Beautiful BOQ Renderer with Furniture, Landscaping, and Interior Details
GPU 1 Optimized Version
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
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use NVIDIA GPU (Task Manager GPU 1)
os.environ['BLENDER_CUDA_DEVICE'] = '0'
os.environ['NVIDIA_VISIBLE_DEVICES'] = '0'

from advanced_layout_generator import AdvancedLayoutGenerator

class EnhancedBeautifulRenderer:
    """Enhanced beautiful renderer with furniture, landscaping, and interior details"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_enhanced_beautiful_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        self.layout_generator = AdvancedLayoutGenerator()
    
    def render_enhanced_boq_scene(self, boq_config):
        """Render an enhanced 3D scene with furniture, landscaping, and interior details"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 40, "total_length": 30, "height": 12})
        enhanced_features = boq_config.get('enhanced_features', {})
        architectural_style = boq_config.get('architectural_style', 'modern')
        quality_level = boq_config.get('quality_level', 'professional')
        
        print(f"Creating enhanced BOQ scene: {self.scene_id}")
        print(f"Rooms to generate: {len(rooms)}")
        print(f"Building dimensions: {building_dims}")
        print(f"Enhanced features: {enhanced_features}")
        print(f"Architectural style: {architectural_style}")
        print(f"Quality level: {quality_level}")
        
        # Generate advanced layout
        layout_positions = self.layout_generator.generate_layout(rooms, building_dims)
        
        print(f"Generated enhanced layout with {len(layout_positions)} rooms")
        for pos in layout_positions:
            room = pos['room']
            features = pos.get('architectural_features', {})
            print(f"  {room['name']}: {pos['width']:.1f}x{pos['length']:.1f} at ({pos['x']:.1f}, {pos['y']:.1f})")
            print(f"    Style: {features.get('style', 'standard')}, Pattern: {features.get('pattern', 'standard')}")
        
        # Create enhanced Blender script with furniture, landscaping, and interior details
        layout_json_str = json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        enhanced_features_str = json.dumps(enhanced_features).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        
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

# NVIDIA GPU SETUP - Force use of RTX 4050 (Task Manager GPU 1, CUDA Device 0)
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
cprefs.compute_device_type = 'OPTIX'
cprefs.get_devices()

print("Configuring NVIDIA RTX 4050 for rendering...")
nvidia_gpu_found = False
for i, device in enumerate(cprefs.devices):
    if device.type in ['OPTIX', 'CUDA']:
        # Enable NVIDIA GPU (RTX 4050)
        if "RTX 4050" in device.name or "GeForce" in device.name:
            device.use = True
            nvidia_gpu_found = True
            print(f"ENABLED GPU {{i}}: {{device.name}} ({{device.type}})")
        else:
            device.use = False
            print(f"DISABLED GPU {{i}}: {{device.name}} ({{device.type}})")
    else:
        device.use = False

if nvidia_gpu_found:
    scene.cycles.device = 'GPU'
    print("NVIDIA RTX 4050 GPU configured for rendering")
else:
    scene.cycles.device = 'CPU'
    print("WARNING: NVIDIA GPU not found, falling back to CPU")

scene.cycles.samples = 1024  # Higher quality samples
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'  # Use NVIDIA OptiX denoiser
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01

# Enhanced render settings for professional quality
scene.render.resolution_x = 2048
scene.render.resolution_y = 1536
scene.render.resolution_percentage = 100

# Enable motion blur and depth of field for cinematic quality
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5

# Ultra-premium material library with realistic textures and advanced shading
def create_advanced_material(name, base_color, roughness=0.5, metallic=0.0, emission=None, normal_strength=0.0, subsurface=0.0, transmission=0.0, ior=1.45):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["IOR"].default_value = ior
    
    # Add subsurface scattering for organic materials
    if subsurface > 0:
        if "Subsurface" in bsdf.inputs:
            bsdf.inputs["Subsurface"].default_value = subsurface
        elif "Subsurface Weight" in bsdf.inputs:
            bsdf.inputs["Subsurface Weight"].default_value = subsurface
            if "Subsurface Color" in bsdf.inputs:
                bsdf.inputs["Subsurface Color"].default_value = (*base_color, 1.0)
    
    # Add transmission for glass materials
    if transmission > 0:
        if "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        elif "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
    
    # Add procedural noise for realistic surface variation
    if normal_strength > 0:
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.inputs["Scale"].default_value = 15.0
        noise.inputs["Detail"].default_value = 10.0
        noise.inputs["Roughness"].default_value = 0.5
        
        bump = nodes.new(type='ShaderNodeBump')
        bump.inputs["Strength"].default_value = normal_strength
        
        mat.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
        mat.node_tree.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    
    # Add color variation using ColorRamp
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].color = (*base_color, 1.0)
    variation_color = [min(1.0, c * 1.2) for c in base_color]  # Slightly brighter variation
    color_ramp.color_ramp.elements[1].color = (*variation_color, 1.0)
    
    noise_color = nodes.new(type='ShaderNodeTexNoise')
    noise_color.inputs["Scale"].default_value = 25.0
    
    mat.node_tree.links.new(noise_color.outputs["Fac"], color_ramp.inputs["Fac"])
    mat.node_tree.links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])
    
    if emission:
        # Handle emission for advanced lighting
        try:
            bsdf.inputs["Emission"].default_value = (*emission, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 3.0
        except KeyError:
            try:
                bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
                bsdf.inputs["Emission Strength"].default_value = 3.0
            except KeyError:
                emission_shader = nodes.new(type='ShaderNodeEmission')
                emission_shader.inputs["Color"].default_value = (*emission, 1.0)
                emission_shader.inputs["Strength"].default_value = 3.0
                
                add_shader = nodes.new(type='ShaderNodeAddShader')
                mat.node_tree.links.new(bsdf.outputs["BSDF"], add_shader.inputs[0])
                mat.node_tree.links.new(emission_shader.outputs["Emission"], add_shader.inputs[1])
                mat.node_tree.links.new(add_shader.outputs["Shader"], output.inputs["Surface"])
                return mat
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat

# Ultra-premium material library with photorealistic quality
materials = {{
    # Luxury flooring materials
    'floor_italian_marble_carrara': create_advanced_material("Carrara Italian Marble", (0.98, 0.97, 0.95), 0.02, 0.0, None, 0.3, 0.1, 0.0, 1.55),
    'floor_nero_marquina_marble': create_advanced_material("Nero Marquina Marble", (0.08, 0.08, 0.12), 0.01, 0.0, None, 0.2, 0.05, 0.0, 1.55),
    'floor_calacatta_gold_marble': create_advanced_material("Calacatta Gold Marble", (0.95, 0.93, 0.88), 0.03, 0.0, None, 0.4, 0.08, 0.0, 1.55),
    'floor_brazilian_cherry': create_advanced_material("Brazilian Cherry Hardwood", (0.45, 0.15, 0.08), 0.25, 0.0, None, 0.5, 0.0, 0.0, 1.52),
    'floor_european_oak': create_advanced_material("European Oak", (0.55, 0.35, 0.20), 0.30, 0.0, None, 0.6, 0.0, 0.0, 1.52),
    'floor_american_walnut': create_advanced_material("American Walnut", (0.35, 0.20, 0.12), 0.20, 0.0, None, 0.4, 0.0, 0.0, 1.52),
    'floor_porcelain_modern': create_advanced_material("Modern Porcelain", (0.92, 0.90, 0.88), 0.05, 0.0, None, 0.1, 0.0, 0.0, 1.54),
    'floor_travertine_honed': create_advanced_material("Honed Travertine", (0.88, 0.82, 0.72), 0.35, 0.0, None, 0.7, 0.05, 0.0, 1.55),
    'floor_concrete_polished': create_advanced_material("Polished Concrete", (0.65, 0.62, 0.60), 0.08, 0.0, None, 0.3, 0.0, 0.0, 1.52),
    
    # Sophisticated wall materials
    'wall_venetian_plaster': create_advanced_material("Venetian Plaster", (0.95, 0.93, 0.90), 0.25, 0.0, None, 0.8, 0.02, 0.0, 1.45),
    'wall_designer_paint_pearl': create_advanced_material("Designer Pearl Paint", (0.95, 0.95, 0.93), 0.15, 0.05, None, 0.2, 0.0, 0.0, 1.45),
    'wall_designer_paint_sage': create_advanced_material("Designer Sage Paint", (0.75, 0.82, 0.70), 0.20, 0.0, None, 0.1, 0.0, 0.0, 1.45),
    'wall_natural_stone_limestone': create_advanced_material("Natural Limestone", (0.85, 0.82, 0.75), 0.45, 0.0, None, 0.8, 0.0, 0.0, 1.55),
    'wall_brick_handmade': create_advanced_material("Handmade Brick", (0.65, 0.35, 0.25), 0.65, 0.0, None, 1.0, 0.0, 0.0, 1.52),
    'wall_wood_panel_walnut': create_advanced_material("Walnut Wood Panel", (0.35, 0.22, 0.15), 0.35, 0.0, None, 0.6, 0.0, 0.0, 1.52),
    'wall_fabric_linen': create_advanced_material("Linen Wall Covering", (0.92, 0.88, 0.82), 0.85, 0.0, None, 0.9, 0.0, 0.0, 1.45),
    
    # Luxury furniture materials
    'furniture_mahogany_premium': create_advanced_material("Premium Mahogany", (0.42, 0.18, 0.10), 0.25, 0.0, None, 0.5, 0.0, 0.0, 1.52),
    'furniture_teak_aged': create_advanced_material("Aged Teak", (0.55, 0.40, 0.25), 0.30, 0.0, None, 0.6, 0.0, 0.0, 1.52),
    'furniture_maple_birds_eye': create_advanced_material("Bird's Eye Maple", (0.85, 0.75, 0.60), 0.20, 0.0, None, 0.4, 0.0, 0.0, 1.52),
    'furniture_leather_italian_brown': create_advanced_material("Italian Brown Leather", (0.35, 0.20, 0.12), 0.15, 0.0, None, 0.2, 0.15, 0.0, 1.46),
    'furniture_leather_cognac': create_advanced_material("Cognac Leather", (0.55, 0.30, 0.15), 0.18, 0.0, None, 0.3, 0.12, 0.0, 1.46),
    'furniture_fabric_cashmere': create_advanced_material("Cashmere Fabric", (0.88, 0.82, 0.75), 0.90, 0.0, None, 0.8, 0.0, 0.0, 1.45),
    'furniture_fabric_silk': create_advanced_material("Silk Fabric", (0.45, 0.52, 0.65), 0.05, 0.02, None, 0.1, 0.0, 0.0, 1.47),
    'furniture_fabric_velvet': create_advanced_material("Velvet Fabric", (0.25, 0.35, 0.55), 0.95, 0.0, None, 1.0, 0.0, 0.0, 1.45),
    
    # Premium metal finishes
    'metal_brushed_stainless': create_advanced_material("Brushed Stainless Steel", (0.85, 0.85, 0.85), 0.15, 0.95, None, 0.2, 0.0, 0.0, 2.5),
    'metal_brass_antique': create_advanced_material("Antique Brass", (0.75, 0.60, 0.35), 0.25, 0.85, None, 0.3, 0.0, 0.0, 2.3),
    'metal_copper_patina': create_advanced_material("Patina Copper", (0.45, 0.65, 0.55), 0.30, 0.80, None, 0.4, 0.0, 0.0, 2.2),
    'metal_bronze_oil_rubbed': create_advanced_material("Oil Rubbed Bronze", (0.25, 0.20, 0.15), 0.35, 0.75, None, 0.3, 0.0, 0.0, 2.4),
    'metal_titanium_brushed': create_advanced_material("Brushed Titanium", (0.70, 0.70, 0.75), 0.10, 0.90, None, 0.1, 0.0, 0.0, 2.6),
    
    # Sophisticated lighting materials
    'light_warm_led': create_advanced_material("Warm LED Light", (1.0, 0.95, 0.85), 0.0, 0.0, (1.0, 0.95, 0.85), 0.0, 0.0, 0.0, 1.0),
    'light_cool_led': create_advanced_material("Cool LED Light", (0.90, 0.95, 1.0), 0.0, 0.0, (0.90, 0.95, 1.0), 0.0, 0.0, 0.0, 1.0),
    'light_accent_amber': create_advanced_material("Amber Accent Light", (1.0, 0.75, 0.40), 0.0, 0.0, (1.0, 0.75, 0.40), 0.0, 0.0, 0.0, 1.0),
    'light_crystal_chandelier': create_advanced_material("Crystal Element", (0.98, 0.98, 0.98), 0.0, 0.0, None, 0.0, 0.0, 0.95, 1.52),
    
    # Premium glass materials
    'glass_ultra_clear': create_advanced_material("Ultra Clear Glass", (0.98, 0.98, 0.98), 0.0, 0.0, None, 0.0, 0.0, 0.95, 1.52),
    'glass_low_iron': create_advanced_material("Low Iron Glass", (0.95, 0.98, 0.95), 0.0, 0.0, None, 0.0, 0.0, 0.92, 1.52),
    'glass_frosted_luxury': create_advanced_material("Luxury Frosted Glass", (0.92, 0.92, 0.95), 0.50, 0.0, None, 0.8, 0.0, 0.60, 1.45),
    'glass_tinted_bronze': create_advanced_material("Bronze Tinted Glass", (0.75, 0.70, 0.60), 0.0, 0.0, None, 0.0, 0.0, 0.85, 1.52),
    
    # Natural landscaping materials
    'grass_premium_blend': create_advanced_material("Premium Grass Blend", (0.25, 0.55, 0.25), 0.85, 0.0, None, 0.9, 0.05, 0.0, 1.45),
    'soil_rich_loam': create_advanced_material("Rich Loam Soil", (0.35, 0.25, 0.15), 0.95, 0.0, None, 1.0, 0.0, 0.0, 1.45),
    'tree_bark_oak': create_advanced_material("Oak Tree Bark", (0.35, 0.25, 0.18), 0.85, 0.0, None, 1.2, 0.0, 0.0, 1.52),
    'tree_leaves_seasonal': create_advanced_material("Seasonal Tree Leaves", (0.30, 0.60, 0.25), 0.80, 0.0, None, 0.8, 0.08, 0.0, 1.45),
    'stone_granite_polished': create_advanced_material("Polished Granite", (0.45, 0.42, 0.40), 0.05, 0.0, None, 0.3, 0.0, 0.0, 1.55),
    'concrete_architectural': create_advanced_material("Architectural Concrete", (0.72, 0.70, 0.68), 0.25, 0.0, None, 0.4, 0.0, 0.0, 1.52),
    
    # Specialty accent materials
    'ceramic_handcrafted': create_advanced_material("Handcrafted Ceramic", (0.88, 0.85, 0.80), 0.15, 0.0, None, 0.3, 0.0, 0.0, 1.54),
    'fabric_designer_linen': create_advanced_material("Designer Linen", (0.92, 0.88, 0.82), 0.88, 0.0, None, 0.9, 0.0, 0.0, 1.45),
    'wood_reclaimed_barn': create_advanced_material("Reclaimed Barn Wood", (0.45, 0.35, 0.25), 0.70, 0.0, None, 1.0, 0.0, 0.0, 1.52),
    'stone_natural_slate': create_advanced_material("Natural Slate", (0.35, 0.38, 0.42), 0.60, 0.0, None, 0.8, 0.0, 0.0, 1.55),
}}

# Enhanced features configuration
enhanced_features = {enhanced_features_str}

# Building dimensions
total_width = {building_dims['total_width']}
total_length = {building_dims['total_length']}
total_height = {building_dims.get('height', 12)}

# Create foundation
bpy.ops.mesh.primitive_plane_add(size=1, location=(total_width/2, total_length/2, 0))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (total_width/2, total_length/2, 1)
foundation.data.materials.append(materials['floor_polished_concrete'])

# Add camera for rendering
bpy.ops.object.camera_add(location=(total_width * 1.5, -total_length * 1.2, total_height * 1.5))
camera = bpy.context.active_object
camera.name = "Camera"
bpy.context.scene.camera = camera

# Add light for rendering
bpy.ops.object.light_add(type='SUN', location=(total_width/2, total_length/2, total_height * 2))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 5.0

# Create exterior walls
wall_thickness = 0.3
wall_height = 3.0

walls = [
    ("North", (total_width/2, total_length, wall_height/2), (total_width/2, wall_thickness/2, wall_height/2)),
    ("South", (total_width/2, 0, wall_height/2), (total_width/2, wall_thickness/2, wall_height/2)),
    ("East", (total_width, total_length/2, wall_height/2), (wall_thickness/2, total_length/2, wall_height/2)),
    ("West", (0, total_length/2, wall_height/2), (wall_thickness/2, total_length/2, wall_height/2))
]

for name, location, scale in walls:
    bpy.ops.mesh.primitive_cube_add(location=location)
    wall = bpy.context.active_object
    wall.name = f"ExteriorWall_{{name}}"
    wall.scale = scale
    wall.data.materials.append(materials['wall_stone_natural'])

# Layout data
layout_data = {layout_json_str}

print(f"Creating {{len(layout_data)}} enhanced rooms with premium features")

# Function to create furniture
def create_furniture(room_type, room_center, room_width, room_length, style):
    furniture_objects = []
    
    if room_type == 'living' and enhanced_features.get('furniture', False):
        # Create sofa
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] - room_length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "Sofa"
        sofa.scale = (1.5, 0.4, 0.4)
        sofa.data.materials.append(materials['furniture_fabric_beige'])
        furniture_objects.append(sofa)
        
        # Create coffee table
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.2))
        table = bpy.context.active_object
        table.name = "CoffeeTable"
        table.scale = (0.8, 0.5, 0.2)
        table.data.materials.append(materials['furniture_wood_oak'])
        furniture_objects.append(table)
        
        # Create TV stand
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1] + room_length/3, 0.3))
        tv_stand = bpy.context.active_object
        tv_stand.name = "TVStand"
        tv_stand.scale = (1.2, 0.3, 0.3)
        tv_stand.data.materials.append(materials['furniture_wood_walnut'])
        furniture_objects.append(tv_stand)
        
    elif room_type == 'bedroom' and enhanced_features.get('furniture', False):
        # Create bed
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.3))
        bed = bpy.context.active_object
        bed.name = "Bed"
        bed.scale = (1.0, 1.5, 0.3)
        bed.data.materials.append(materials['furniture_fabric_gray'])
        furniture_objects.append(bed)
        
        # Create nightstands
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(location=(room_center[0] + side * 1.3, room_center[1], 0.25))
            nightstand = bpy.context.active_object
            nightstand.name = f"Nightstand_{{side}}"
            nightstand.scale = (0.3, 0.4, 0.25)
            nightstand.data.materials.append(materials['furniture_wood_oak'])
            furniture_objects.append(nightstand)
            
        # Create wardrobe
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0] + room_width/3, room_center[1] + room_length/3, 1.0))
        wardrobe = bpy.context.active_object
        wardrobe.name = "Wardrobe"
        wardrobe.scale = (0.6, 0.3, 1.0)
        wardrobe.data.materials.append(materials['furniture_wood_walnut'])
        furniture_objects.append(wardrobe)
        
    elif room_type == 'kitchen' and enhanced_features.get('furniture', False):
        # Create kitchen island
        bpy.ops.mesh.primitive_cube_add(location=(room_center[0], room_center[1], 0.45))
        island = bpy.context.active_object
        island.name = "KitchenIsland"
        island.scale = (1.0, 0.6, 0.45)
        island.data.materials.append(materials['floor_marble_carrara'])
        furniture_objects.append(island)
        
        # Create cabinets
        for i in range(3):
            bpy.ops.mesh.primitive_cube_add(location=(room_center[0] - room_width/3 + i*0.8, room_center[1] + room_length/3, 0.4))
            cabinet = bpy.context.active_object
            cabinet.name = f"Cabinet_{{i}}"
            cabinet.scale = (0.35, 0.3, 0.4)
            cabinet.data.materials.append(materials['furniture_wood_oak'])
            furniture_objects.append(cabinet)
    
    return furniture_objects

# Function to create interior details
def create_interior_details(room_type, room_center, room_width, room_length):
    detail_objects = []
    
    if enhanced_features.get('interiorDetails', False):
        # Create ceiling light
        bpy.ops.mesh.primitive_uv_sphere_add(location=(room_center[0], room_center[1], 2.8))
        light_fixture = bpy.context.active_object
        light_fixture.name = f"CeilingLight_{{room_type}}"
        light_fixture.scale = (0.2, 0.2, 0.1)
        light_fixture.data.materials.append(materials['light_emission_warm'])
        detail_objects.append(light_fixture)
        
        # Create baseboard
        for wall in ['north', 'south', 'east', 'west']:
            if wall == 'north':
                location = (room_center[0], room_center[1] + room_length/2, 0.1)
                scale = (room_width/2, 0.05, 0.1)
            elif wall == 'south':
                location = (room_center[0], room_center[1] - room_length/2, 0.1)
                scale = (room_width/2, 0.05, 0.1)
            elif wall == 'east':
                location = (room_center[0] + room_width/2, room_center[1], 0.1)
                scale = (0.05, room_length/2, 0.1)
            elif wall == 'west':
                location = (room_center[0] - room_width/2, room_center[1], 0.1)
                scale = (0.05, room_length/2, 0.1)
            
            bpy.ops.mesh.primitive_cube_add(location=location)
            baseboard = bpy.context.active_object
            baseboard.name = f"Baseboard_{{wall}}"
            baseboard.scale = scale
            baseboard.data.materials.append(materials['furniture_wood_oak'])
            detail_objects.append(baseboard)
    
    return detail_objects

# Function to create landscaping
def create_landscaping():
    landscaping_objects = []
    
    if enhanced_features.get('landscaping', False):
        # Create grass areas around the building
        grass_margin = 5
        
        # Front yard
        bpy.ops.mesh.primitive_plane_add(location=(total_width/2, -grass_margin/2, 0.01))
        front_yard = bpy.context.active_object
        front_yard.name = "FrontYard"
        front_yard.scale = (total_width/2 + grass_margin, grass_margin/2, 1)
        front_yard.data.materials.append(materials['grass_green'])
        landscaping_objects.append(front_yard)
        
        # Back yard
        bpy.ops.mesh.primitive_plane_add(location=(total_width/2, total_length + grass_margin/2, 0.01))
        back_yard = bpy.context.active_object
        back_yard.name = "BackYard"
        back_yard.scale = (total_width/2 + grass_margin, grass_margin/2, 1)
        back_yard.data.materials.append(materials['grass_green'])
        landscaping_objects.append(back_yard)
        
        # Create trees
        for i in range(4):
            tree_x = random.uniform(-grass_margin, total_width + grass_margin)
            tree_y = random.uniform(-grass_margin, total_length + grass_margin)
            
            # Avoid placing trees too close to building
            if not (0 <= tree_x <= total_width and 0 <= tree_y <= total_length):
                # Tree trunk
                bpy.ops.mesh.primitive_cylinder_add(location=(tree_x, tree_y, 1.5))
                trunk = bpy.context.active_object
                trunk.name = f"TreeTrunk_{{i}}"
                trunk.scale = (0.2, 0.2, 1.5)
                trunk.data.materials.append(materials['tree_bark'])
                landscaping_objects.append(trunk)
                
                # Tree foliage
                bpy.ops.mesh.primitive_uv_sphere_add(location=(tree_x, tree_y, 2.5))
                foliage = bpy.context.active_object
                foliage.name = f"TreeFoliage_{{i}}"
                foliage.scale = (1.0, 1.0, 0.8)
                foliage.data.materials.append(materials['tree_leaves'])
                landscaping_objects.append(foliage)
        
        # Create pathway
        bpy.ops.mesh.primitive_cube_add(location=(total_width/2, -2, 0.02))
        pathway = bpy.context.active_object
        pathway.name = "Pathway"
        pathway.scale = (1.0, 2, 0.02)
        pathway.data.materials.append(materials['concrete_path'])
        landscaping_objects.append(pathway)
    
    return landscaping_objects

# Create enhanced rooms with premium features
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
    rotation = room_data.get('rotation', 0)
    
    features = room_data.get('architectural_features', {{}})
    materials_config = room_data.get('materials', {{}})
    
    print(f"Creating enhanced {{room_name}} ({{room_type}}) - {{features.get('style', 'standard')}} style")
    
    # Room floor
    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0.05))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room_name.replace(' ', '_')}}"
    floor.scale = (width/2, length/2, 0.05)
    
    # Apply premium flooring material
    floor_material = materials_config.get('floor', 'hardwood_oak')
    if floor_material == 'hardwood_oak':
        floor.data.materials.append(materials['floor_hardwood_oak'])
    elif floor_material == 'marble':
        floor.data.materials.append(materials['floor_marble_carrara'])
    elif floor_material == 'ceramic':
        floor.data.materials.append(materials['floor_ceramic_modern'])
    else:
        floor.data.materials.append(materials['floor_hardwood_oak'])
    
    # Room walls
    wall_height = height / 2
    wall_thickness = 0.1
    
    # North wall
    bpy.ops.mesh.primitive_cube_add(location=(x, y + length/2, wall_height))
    north_wall = bpy.context.active_object
    north_wall.name = f"NorthWall_{{room_name.replace(' ', '_')}}"
    north_wall.scale = (width/2, wall_thickness/2, wall_height)
    north_wall.data.materials.append(materials['wall_paint_white'])
    
    # South wall
    bpy.ops.mesh.primitive_cube_add(location=(x, y - length/2, wall_height))
    south_wall = bpy.context.active_object
    south_wall.name = f"SouthWall_{{room_name.replace(' ', '_')}}"
    south_wall.scale = (width/2, wall_thickness/2, wall_height)
    south_wall.data.materials.append(materials['wall_paint_white'])
    
    # East wall
    bpy.ops.mesh.primitive_cube_add(location=(x + width/2, y, wall_height))
    east_wall = bpy.context.active_object
    east_wall.name = f"EastWall_{{room_name.replace(' ', '_')}}"
    east_wall.scale = (wall_thickness/2, length/2, wall_height)
    east_wall.data.materials.append(materials['wall_paint_white'])
    
    # West wall
    bpy.ops.mesh.primitive_cube_add(location=(x - width/2, y, wall_height))
    west_wall = bpy.context.active_object
    west_wall.name = f"WestWall_{{room_name.replace(' ', '_')}}"
    west_wall.scale = (wall_thickness/2, length/2, wall_height)
    west_wall.data.materials.append(materials['wall_paint_white'])
    
    # Create furniture for this room
    room_center = (x, y, 0)
    furniture = create_furniture(room_type, room_center, width, length, features.get('style', 'modern'))
    all_furniture.extend(furniture)
    
    # Create interior details
    details = create_interior_details(room_type, room_center, width, length)
    all_details.extend(details)

# Create landscaping
landscaping = create_landscaping()

# Enhanced lighting setup
if enhanced_features.get('lighting', False):
    # Create professional lighting
    
    # Key light (main illumination)
    bpy.ops.object.light_add(type='SUN', location=(total_width + 10, total_length + 10, 15))
    key_light = bpy.context.active_object
    key_light.name = "KeyLight"
    key_light.data.energy = 5.0
    key_light.data.color = (1.0, 0.95, 0.8)
    key_light.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Fill light (softer illumination)
    bpy.ops.object.light_add(type='SUN', location=(-10, -10, 12))
    fill_light = bpy.context.active_object
    fill_light.name = "FillLight"
    fill_light.data.energy = 2.0
    fill_light.data.color = (0.8, 0.9, 1.0)
    fill_light.rotation_euler = (math.radians(30), 0, math.radians(-45))
    
    # Rim light (edge definition)
    bpy.ops.object.light_add(type='SUN', location=(total_width - 5, total_length - 5, 20))
    rim_light = bpy.context.active_object
    rim_light.name = "RimLight"
    rim_light.data.energy = 3.0
    rim_light.data.color = (1.0, 0.9, 0.7)
    rim_light.rotation_euler = (math.radians(60), 0, math.radians(135))

# Camera setup for architectural photography
bpy.ops.object.camera_add(location=(total_width + 15, total_length + 15, 8))
camera = bpy.context.active_object
camera.name = "ArchitecturalCamera"
camera.rotation_euler = (math.radians(65), 0, math.radians(45))
camera.data.lens = 35
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 20
camera.data.dof.aperture_fstop = 5.6

# Set as active camera
scene.camera = camera

# Export settings
bpy.ops.wm.obj_export(
    filepath="{os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.obj').replace(os.sep, '/')}",
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_colors=True
)

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath="{os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.blend').replace(os.sep, '/')}")

# RENDER IMAGES WITH GPU (This will actually use the GPU)
print("🎨 Starting GPU rendering...")

# Set up rendering
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.filepath = "{os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}_render').replace(os.sep, '/')}"
scene.render.image_settings.file_format = 'PNG'

# Multiple camera angles for better visualization
camera_positions = [
    ("hero", (total_width * 1.5, -total_length * 1.2, total_height * 1.5), (total_width/2, total_length/2, total_height/3)),
    ("detail", (total_width * 0.8, total_length * 0.3, total_height * 0.8), (total_width/2, total_length/2, total_height/4)),
    ("plan", (total_width/2, total_length/2, total_height * 3), (total_width/2, total_length/2, 0))
]

render_files = []
for view_name, cam_loc, cam_target in camera_positions:
    print(f"📸 Rendering " + view_name + " view with GPU...")
    
    # Position camera
    camera = bpy.data.objects['Camera']
    camera.location = cam_loc
    
    # Point camera at target
    direction = Vector(cam_target) - Vector(cam_loc)
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Set render filename  
    render_path = r"{self.temp_dir.replace(os.sep, '/')}/enhanced_boq_{self.scene_id}_" + view_name + ".png"
    scene.render.filepath = render_path
    
    # RENDER (This actually uses the GPU!)
    bpy.ops.render.render(write_still=True)
    render_files.append(render_path)
    print("RENDER_PNG: " + render_path)

print("🔥 GPU rendering complete!")
print("ENHANCED BOQ RENDERING COMPLETE")
print(f"Scene ID: {self.scene_id}")
print(f"Objects: {{len(bpy.data.objects)}}")
print(f"Materials: {{len(bpy.data.materials)}}")
print(f"Furniture pieces: {{len(all_furniture)}}")
print(f"Interior details: {{len(all_details)}}")
print(f"Landscaping elements: {{len(landscaping)}}")
print(f"Render files: {{len(render_files)}}")
'''

        # Write the Blender script
        script_path = os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(blender_script)
        
        print(f"Enhanced Blender script written to: {script_path}")
        
        # Run Blender with the script
        try:
            result = subprocess.run([
                self.blender_path, 
                '--background',
                '--python', script_path
            ], capture_output=True, text=True, timeout=300)
            
            print("Blender render output:", result.stdout)
            if result.stderr:
                print("Blender warnings:", result.stderr)
            
            if result.returncode != 0:
                return {'success': False, 'error': f'Blender failed with code {result.returncode}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        # Copy files
        files = []
        output_dir = os.path.join(os.path.dirname(__file__), 'backend', 'generated_models')
        os.makedirs(output_dir, exist_ok=True)
        
        for extension in ['obj', 'mtl', 'blend']:
            src_file = os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.{extension}')
            if os.path.exists(src_file):
                dst_file = os.path.join(output_dir, f'enhanced_boq_{self.scene_id}.{extension}')
                shutil.copy2(src_file, dst_file)
                files.append({'type': extension, 'path': dst_file})
        
        # Get layout info from first room
        layout_type = 'enhanced'
        style = architectural_style
        if layout_positions and len(layout_positions) > 0:
            features = layout_positions[0].get('architectural_features', {})
            layout_type = features.get('pattern', 'enhanced')
            style = features.get('style', architectural_style)
        
        return {
            'success': True,
            'scene_id': self.scene_id,
            'layout_type': layout_type,
            'style': style,
            'files': files,
            'output': result.stdout,
            'enhanced_features': enhanced_features,
            'quality_level': quality_level
        }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python enhanced_beautiful_renderer.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        renderer = EnhancedBeautifulRenderer()
        result = renderer.render_enhanced_boq_scene(config)
        
        if result['success']:
            print(f"ENHANCED_SCENE_ID: {result['scene_id']}")
            print(f"LAYOUT_TYPE: {result.get('layout_type', 'enhanced')}")
            print(f"STYLE: {result.get('style', 'modern')}")
            print(f"QUALITY_LEVEL: {result.get('quality_level', 'professional')}")
            print(f"ENHANCED_FEATURES: {result.get('enhanced_features', {})}")
            for file_info in result['files']:
                file_type = file_info['type'].upper()
                print(f"{file_type}_FILE: {file_info['path']}")
        else:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
