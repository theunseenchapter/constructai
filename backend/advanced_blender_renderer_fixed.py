#!/usr/bin/env python3
"""
Advanced Blender Renderer for ConstructAI - FIXED VERSION
Professional 3D architectural visualization using Blender
"""

import subprocess
import tempfile
import json
import os
import sys
import uuid


class AdvancedBlenderRenderer:
    """Professional Blender renderer for high-quality 3D architectural visualization"""
    
    def __init__(self, blender_path="blender"):
        self.blender_path = blender_path
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_blender_')
        self.scene_id = None
        
    def generate_3d_model(self, model_config: dict) -> dict:
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

# Set up professional render settings with GPU acceleration
scene.render.engine = 'CYCLES'

# GPU setup with error handling
try:
    prefs = bpy.context.preferences
    cprefs = prefs.addons['cycles'].preferences
    
    # Set compute device to CUDA or OptiX
    if hasattr(cprefs, 'compute_device_type'):
        cprefs.compute_device_type = 'OPTIX'
    
    # Enable GPU devices
    if hasattr(cprefs, 'get_devices'):
        cprefs.get_devices()
        for device in cprefs.devices:
            if device.type in ['OPTIX', 'CUDA']:
                device.use = True
                print(f"🚀 GPU ENABLED: {{device.name}} ({{device.type}})")
    
    # Set scene to use GPU
    scene.cycles.device = 'GPU'
    print("✅ GPU rendering enabled")
except Exception as e:
    print(f"⚠️ GPU setup failed, using CPU: {{e}}")
    scene.cycles.device = 'CPU'

# High quality settings
scene.cycles.samples = 512  # Balanced quality/speed
scene.render.resolution_x = 2560
scene.render.resolution_y = 1440
scene.render.resolution_percentage = 100

# Quality features
scene.cycles.use_denoising = True
if hasattr(scene.cycles, 'denoiser'):
    scene.cycles.denoiser = 'OPTIX' if scene.cycles.device == 'GPU' else 'OPENIMAGEDENOISE'
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

# Material creation function
def create_advanced_material(name, base_color, roughness=0.5, metallic=0.0):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    
    # Create principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    # Output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return material

# Room creation function
def create_room_with_details(room_data):
    room_name = room_data.get('name', 'Room')
    room_type = room_data.get('type', 'living_room')
    width = room_data.get('width', 6)
    length = room_data.get('length', 8)
    height = room_data.get('height', 3)
    
    # Create floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor_" + room_name
    floor.scale = (width, length, 1)
    
    # Floor material
    floor_material = create_advanced_material(
        "Hardwood_Floor_" + room_name,
        (0.4, 0.25, 0.15),  # Rich wood brown
        roughness=0.2,
        metallic=0.0
    )
    floor.data.materials.append(floor_material)
    
    # Create walls
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
    
    # Wall material
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

# Furniture creation
def create_furniture(room_data):
    room_type = room_data.get('type', 'living_room')
    width = room_data.get('width', 6)
    length = room_data.get('length', 8)
    
    if room_type == 'living_room':
        # Sofa
        bpy.ops.mesh.primitive_cube_add(location=(0, -length/4, 0.4))
        sofa = bpy.context.active_object
        sofa.name = "Sofa"
        sofa.scale = (2.5, 1.2, 0.4)
        
        # Fabric material
        fabric_material = create_advanced_material(
            "Sofa_Fabric",
            (0.2, 0.4, 0.6),  # Blue fabric
            roughness=0.8,
            metallic=0.0
        )
        sofa.data.materials.append(fabric_material)
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.3))
        table = bpy.context.active_object
        table.name = "Coffee_Table"
        table.scale = (1.5, 0.8, 0.05)
        
        # Glass material
        glass_material = create_advanced_material(
            "Glass_Top",
            (0.9, 0.95, 1.0),  # Clear glass
            roughness=0.0,
            metallic=0.0
        )
        table.data.materials.append(glass_material)

# Lighting setup
def setup_lighting():
    # Remove default light
    if 'Light' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Light'], do_unlink=True)
    
    # Main window light
    bpy.ops.object.light_add(type='AREA', location=(0, -6, 2))
    window_light = bpy.context.active_object
    window_light.name = "Window_Light"
    window_light.data.energy = 50.0
    window_light.data.size = 4.0
    window_light.data.color = (1.0, 0.95, 0.9)  # Warm daylight
    window_light.rotation_euler = (1.2, 0, 0)
    
    # Ceiling light
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.8))
    ceiling_light = bpy.context.active_object
    ceiling_light.name = "Ceiling_Light"
    ceiling_light.data.energy = 20.0
    ceiling_light.data.size = 3.0
    ceiling_light.data.color = (1.0, 0.98, 0.95)
    ceiling_light.rotation_euler = (3.14159, 0, 0)

# Camera setup
def setup_camera():
    # Remove default camera
    if 'Camera' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Camera'], do_unlink=True)
    
    # Create new camera
    bpy.ops.object.camera_add(location=(-4, -4, 2))
    camera = bpy.context.active_object
    camera.name = "InteriorCamera"
    camera.rotation_euler = (1.0, 0, -0.785)  # 45-degree angle
    
    # Camera settings
    camera.data.lens = 24  # Wide angle
    camera.data.sensor_width = 36
    camera.data.clip_start = 0.1
    camera.data.clip_end = 100
    
    # Set as active camera
    bpy.context.scene.camera = camera

# Create rooms if specified
if 'rooms' in model_config:
    for room_data in model_config['rooms']:
        create_room_with_details(room_data)
        create_furniture(room_data)

# Set up lighting and camera
setup_lighting()
setup_camera()

# Export files
output_dir = "{temp_dir}"
scene_name = "professional_model_{scene_id}"

# Save .blend file
blend_file = os.path.join(output_dir, scene_name + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_file)

# Export OBJ
obj_file = os.path.join(output_dir, scene_name + ".obj")
try:
    bpy.ops.wm.obj_export(
        filepath=obj_file,
        export_materials=True,
        export_smooth_groups=True,
        export_normals=True,
        export_uv=True
    )
except:
    # Fallback for older Blender versions
    bpy.ops.export_scene.obj(
        filepath=obj_file,
        use_materials=True,
        use_smooth_groups=True,
        use_normals=True,
        use_uvs=True
    )

# Export GLB
glb_file = os.path.join(output_dir, scene_name + ".glb")
try:
    bpy.ops.export_scene.gltf(
        filepath=glb_file,
        export_format='GLB',
        export_materials='EXPORT'
    )
except Exception as e:
    print(f"GLB export failed: {{e}}")

# Render images
rendered_files = []
camera = bpy.context.scene.camera

render_positions = [
    ("main", (-4, -4, 2), (1.0, 0, -0.785)),
    ("detail", (-3, -5, 1.8), (0.9, 0, -0.6)),
    ("wide", (-6, -3, 2.5), (1.1, 0, -1.0))
]

for name, location, rotation in render_positions:
    camera.location = location
    camera.rotation_euler = rotation
    
    render_file = os.path.join(output_dir, f"{{scene_name}}_{{name}}.png")
    bpy.context.scene.render.filepath = render_file
    bpy.ops.render.render(write_still=True)
    rendered_files.append(render_file)

# Output result
result = {{
    "success": True,
    "scene_id": "{scene_id}",
    "files": [blend_file, obj_file, glb_file] + rendered_files,
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
        
        try:
            # Execute Blender with the script
            result = subprocess.run([
                self.blender_path,
                '--background',
                '--python-expr', blender_script
            ], capture_output=True, text=True, timeout=600)
            
            # Parse the result
            stdout_lines = result.stdout.split('\n')
            capturing = False
            result_lines = []
            
            for line in stdout_lines:
                if 'BLENDER_RESULT_START' in line:
                    capturing = True
                    continue
                elif 'BLENDER_RESULT_END' in line:
                    break
                elif capturing:
                    result_lines.append(line)
            
            if result_lines:
                try:
                    result_json = json.loads('\n'.join(result_lines))
                    return result_json
                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "error": f"JSON decode error: {str(e)}",
                        "raw_output": '\n'.join(result_lines)
                    }
            
            return {
                "success": False,
                "error": f"No valid result found. stderr: {result.stderr}",
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
        print("Usage: python advanced_blender_renderer_fixed.py <tool> [args_json]")
        sys.exit(1)
    
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    if tool == "create_3d_scene":
        result = advanced_renderer.generate_3d_model(args)
        print(json.dumps(result))
    else:
        print(json.dumps({"success": False, "error": f"Unknown tool: {tool}"}))


if __name__ == "__main__":
    main()
