#!/usr/bin/env python3
"""
Fixed Material Renderer - Simplified version with Blender 4.4 compatibility
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

class FixedMaterialRenderer:
    """Simple fixed renderer with Blender 4.4 compatibility"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_fixed_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        self.layout_generator = AdvancedLayoutGenerator()
    
    def render_simple_scene(self, boq_config):
        """Render a simple 3D scene with basic materials"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 40, "total_length": 30, "height": 12})
        
        print(f"Creating simple scene: {self.scene_id}")
        print(f"Rooms to generate: {len(rooms)}")
        print(f"Building dimensions: {building_dims}")
        
        # Generate layout
        layout_positions = self.layout_generator.generate_layout(rooms, building_dims)
        
        # Create simple Blender script
        blender_script = f'''
import bpy
import bmesh
import math
from mathutils import Vector

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

scene = bpy.context.scene

# GPU setup
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
cprefs.compute_device_type = 'OPTIX'
cprefs.get_devices()

print("Configuring GPU...")
for i, device in enumerate(cprefs.devices):
    if device.type in ['OPTIX', 'CUDA']:
        device.use = True
        print(f"ENABLED GPU {{i}}: {{device.name}} ({{device.type}})")
    else:
        device.use = False

scene.cycles.device = 'GPU'
scene.cycles.samples = 256
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Simple material creation function
def create_simple_material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat

# Create basic materials
materials = {{
    'floor': create_simple_material("Floor", (0.6, 0.4, 0.2), 0.3),
    'wall': create_simple_material("Wall", (0.9, 0.9, 0.9), 0.8),
    'ceiling': create_simple_material("Ceiling", (0.95, 0.95, 0.95), 0.9),
    'furniture': create_simple_material("Furniture", (0.5, 0.3, 0.2), 0.4),
}}

# Create rooms
layout_positions = {json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

for room_data in layout_positions:
    room = room_data['room']
    x = room_data['x']
    y = room_data['y']
    width = room_data['width']
    length = room_data['length']
    height = room.get('height', 3.0)
    
    print(f"Creating room: {{room['name']}} at ({{x}}, {{y}})")
    
    # Floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room['name']}}"
    floor.scale = (width/2, length/2, 1)
    floor.data.materials.append(materials['floor'])
    
    # Ceiling
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, height))
    ceiling = bpy.context.active_object
    ceiling.name = f"Ceiling_{{room['name']}}"
    ceiling.scale = (width/2, length/2, 1)
    ceiling.data.materials.append(materials['ceiling'])
    
    # Walls
    wall_positions = [
        (x - width/2, y, height/2, 0.1, length, height),  # Left wall
        (x + width/2, y, height/2, 0.1, length, height),  # Right wall
        (x, y - length/2, height/2, width, 0.1, height),  # Front wall
        (x, y + length/2, height/2, width, 0.1, height),  # Back wall
    ]
    
    for i, (wx, wy, wz, w_width, w_length, w_height) in enumerate(wall_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz))
        wall = bpy.context.active_object
        wall.name = f"Wall_{{room['name']}}_{{i}}"
        wall.scale = (w_width, w_length, w_height/2)
        wall.data.materials.append(materials['wall'])
    
    # Simple furniture
    if room.get('type') == 'living':
        # Sofa
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.4))
        sofa = bpy.context.active_object
        sofa.name = f"Sofa_{{room['name']}}"
        sofa.scale = (1.5, 0.8, 0.8)
        sofa.data.materials.append(materials['furniture'])
    elif room.get('type') == 'bedroom':
        # Bed
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.3))
        bed = bpy.context.active_object
        bed.name = f"Bed_{{room['name']}}"
        bed.scale = (2.0, 1.5, 0.6)
        bed.data.materials.append(materials['furniture'])

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
sun = bpy.context.active_object
sun.data.energy = 5

# Add camera
bpy.ops.object.camera_add(location=(20, -20, 15))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)
scene.camera = camera

# Set output path
output_dir = "{self.temp_dir.replace(chr(92), '/')}"
blend_file = f"{{output_dir}}/simple_scene_{self.scene_id}.blend"
obj_file = f"{{output_dir}}/simple_scene_{self.scene_id}.obj"
render_file = f"{{output_dir}}/simple_scene_{self.scene_id}.png"

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=blend_file)
print(f"BLEND_FILE: {{blend_file}}")

# Export OBJ
bpy.ops.wm.obj_export(filepath=obj_file, check_existing=False, export_selected_objects=False)
print(f"OBJ_FILE: {{obj_file}}")

# Render
scene.render.filepath = render_file
bpy.ops.render.render(write_still=True)
print(f"RENDER_PNG: {{render_file}}")

print(f"SCENE_ID: {self.scene_id}")
print(f"LAYOUT_TYPE: simple")
print(f"STYLE: modern")
print(f"QUALITY_LEVEL: basic")
print("SUCCESS: Scene created successfully")
'''
        
        # Write script
        script_path = os.path.join(self.temp_dir, f'simple_scene_{self.scene_id}.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        print(f"Simple Blender script written to: {script_path}")
        
        # Run Blender
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ Simple scene created successfully")
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
        print("Usage: python fixed_material_renderer.py <config_file>")
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
    
    renderer = FixedMaterialRenderer()
    output = renderer.render_simple_scene(config)
    print(output)

if __name__ == "__main__":
    main()
