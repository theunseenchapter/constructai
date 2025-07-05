#!/usr/bin/env python3
"""
Simple test to create a basic interior scene and render it
"""
import subprocess
import os
import json
import tempfile

def create_simple_interior():
    """Create a simple interior scene for testing"""
    
    temp_dir = tempfile.mkdtemp(prefix='test_interior_')
    blender_path = 'D:\\blender\\blender.exe'
    
    simple_script = f'''
import bpy
import bmesh
import mathutils
import math

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

scene = bpy.context.scene

# Set up GPU rendering
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
scene.cycles.samples = 256
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Create a simple room
# Floor
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"

# Create a simple material
mat = bpy.data.materials.new(name="FloorMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.8, 0.6, 0.4, 1.0)  # Wood color
floor.data.materials.append(mat)

# Back wall
bpy.ops.mesh.primitive_cube_add(location=(0, 5, 1.5))
wall = bpy.context.active_object
wall.name = "BackWall"
wall.scale = (5, 0.1, 1.5)

# Create wall material
wall_mat = bpy.data.materials.new(name="WallMat")
wall_mat.use_nodes = True
wall_bsdf = wall_mat.node_tree.nodes["Principled BSDF"]
wall_bsdf.inputs[0].default_value = (0.9, 0.9, 0.85, 1.0)  # Off-white
wall.data.materials.append(wall_mat)

# Add a simple cube as furniture
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.5))
furniture = bpy.context.active_object
furniture.name = "Table"
furniture.scale = (1, 2, 0.5)

# Create furniture material
furn_mat = bpy.data.materials.new(name="FurnMat")
furn_mat.use_nodes = True
furn_bsdf = furn_mat.node_tree.nodes["Principled BSDF"]
furn_bsdf.inputs[0].default_value = (0.3, 0.2, 0.1, 1.0)  # Dark wood
furniture.data.materials.append(furn_mat)

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(2, -2, 4))
sun = bpy.context.active_object
sun.data.energy = 3.0

# Position camera for interior view
bpy.ops.object.camera_add(location=(-3, -3, 1.8))
camera = bpy.context.active_object
camera.rotation_euler = (1.0, 0, -0.8)
scene.camera = camera

# Export OBJ file with minimal parameters
obj_path = "{temp_dir.replace(chr(92), '/')}/test_interior.obj"
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=True
)

print("OBJ EXPORT COMPLETE:", obj_path)
print("MTL file should be at:", obj_path.replace('.obj', '.mtl'))
'''
    
    try:
        result = subprocess.run([
            blender_path,
            '--background',
            '--python-expr', simple_script
        ], capture_output=True, text=True, timeout=120)
        
        print("Simple Interior Test Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
        # Check if OBJ file was created
        test_obj_file = os.path.join(temp_dir, 'test_interior.obj')
        test_mtl_file = os.path.join(temp_dir, 'test_interior.mtl')
        
        if os.path.exists(test_obj_file):
            print(f"✅ Test OBJ created: {test_obj_file}")
            # Copy to project
            import shutil
            shutil.copy(test_obj_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\test_simple_interior.obj')
            print("✅ Copied OBJ to project directory")
            
            if os.path.exists(test_mtl_file):
                shutil.copy(test_mtl_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\test_simple_interior.mtl')
                print("✅ Copied MTL to project directory")
            else:
                print("⚠️ MTL file not found")
        else:
            print("❌ Test OBJ not found")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    create_simple_interior()
