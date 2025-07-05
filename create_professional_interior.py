#!/usr/bin/env python3
"""
Create a professional, detailed interior scene for architectural visualization
"""
import subprocess
import os
import json
import tempfile

def create_professional_interior():
    """Create a detailed, professional interior scene"""
    
    temp_dir = tempfile.mkdtemp(prefix='professional_interior_')
    blender_path = 'D:\\blender\\blender.exe'
    
    professional_script = f'''
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

# Create detailed room with proper architecture
# FLOOR - Wooden parquet pattern
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"

# Create realistic wood floor material
wood_mat = bpy.data.materials.new(name="WoodFloor")
wood_mat.use_nodes = True
nodes = wood_mat.node_tree.nodes
bsdf = nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.42, 0.26, 0.15, 1.0)  # Rich wood
bsdf.inputs['Roughness'].default_value = 0.3
floor.data.materials.append(wood_mat)

# WALLS - Create 4 walls with proper thickness
# Back wall
bpy.ops.mesh.primitive_cube_add(location=(0, 6, 1.5))
back_wall = bpy.context.active_object
back_wall.name = "BackWall"
back_wall.scale = (6, 0.2, 1.5)

# Left wall  
bpy.ops.mesh.primitive_cube_add(location=(-6, 0, 1.5))
left_wall = bpy.context.active_object
left_wall.name = "LeftWall"
left_wall.scale = (0.2, 6, 1.5)

# Right wall
bpy.ops.mesh.primitive_cube_add(location=(6, 0, 1.5))
right_wall = bpy.context.active_object
right_wall.name = "RightWall"
right_wall.scale = (0.2, 6, 1.5)

# Create wall material with subtle texture
wall_mat = bpy.data.materials.new(name="WallMaterial")
wall_mat.use_nodes = True
wall_nodes = wall_mat.node_tree.nodes
wall_bsdf = wall_nodes["Principled BSDF"]
wall_bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.92, 1.0)
wall_bsdf.inputs['Roughness'].default_value = 0.8

# Apply wall material to all walls
for wall in [back_wall, left_wall, right_wall]:
    wall.data.materials.append(wall_mat)

# CEILING
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 3))
ceiling = bpy.context.active_object
ceiling.name = "Ceiling"
ceiling.rotation_euler = (math.pi, 0, 0)

# Ceiling material
ceiling_mat = bpy.data.materials.new(name="CeilingMaterial")
ceiling_mat.use_nodes = True
ceil_nodes = ceiling_mat.node_tree.nodes
ceil_bsdf = ceil_nodes["Principled BSDF"]
ceil_bsdf.inputs['Base Color'].default_value = (0.98, 0.98, 0.98, 1.0)
ceiling.data.materials.append(ceiling_mat)

# DETAILED FURNITURE

# Modern Sofa
bpy.ops.mesh.primitive_cube_add(location=(-2, 2, 0.4))
sofa_base = bpy.context.active_object
sofa_base.name = "SofaBase"
sofa_base.scale = (1.5, 0.8, 0.4)

# Sofa back
bpy.ops.mesh.primitive_cube_add(location=(-2, 2.5, 0.9))
sofa_back = bpy.context.active_object
sofa_back.name = "SofaBack"
sofa_back.scale = (1.5, 0.2, 0.5)

# Sofa material
sofa_mat = bpy.data.materials.new(name="SofaMaterial")
sofa_mat.use_nodes = True
sofa_nodes = sofa_mat.node_tree.nodes
sofa_bsdf = sofa_nodes["Principled BSDF"]
sofa_bsdf.inputs['Base Color'].default_value = (0.3, 0.4, 0.6, 1.0)  # Blue fabric
sofa_bsdf.inputs['Roughness'].default_value = 0.9

for sofa_part in [sofa_base, sofa_back]:
    sofa_part.data.materials.append(sofa_mat)

# Coffee Table
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.4))
coffee_table = bpy.context.active_object
coffee_table.name = "CoffeeTable"
coffee_table.scale = (1.2, 0.8, 0.05)

# Table legs
for i, pos in enumerate([(-1, -0.6, 0.2), (1, -0.6, 0.2), (-1, 0.6, 0.2), (1, 0.6, 0.2)]):
    bpy.ops.mesh.primitive_cylinder_add(location=pos, radius=0.05, depth=0.4)
    leg = bpy.context.active_object
    leg.name = f"TableLeg_{{i}}"

# Table material
table_mat = bpy.data.materials.new(name="TableMaterial")
table_mat.use_nodes = True
table_nodes = table_mat.node_tree.nodes
table_bsdf = table_nodes["Principled BSDF"]
table_bsdf.inputs['Base Color'].default_value = (0.15, 0.1, 0.05, 1.0)  # Dark wood
table_bsdf.inputs['Metallic'].default_value = 0.0
table_bsdf.inputs['Roughness'].default_value = 0.2

coffee_table.data.materials.append(table_mat)

# Bookshelf
bpy.ops.mesh.primitive_cube_add(location=(4, 4, 1.2))
bookshelf = bpy.context.active_object
bookshelf.name = "Bookshelf"
bookshelf.scale = (0.4, 1.5, 1.2)

# Bookshelf material
shelf_mat = bpy.data.materials.new(name="ShelfMaterial")
shelf_mat.use_nodes = True
shelf_nodes = shelf_mat.node_tree.nodes
shelf_bsdf = shelf_nodes["Principled BSDF"]
shelf_bsdf.inputs['Base Color'].default_value = (0.6, 0.4, 0.2, 1.0)  # Medium wood
bookshelf.data.materials.append(shelf_mat)

# Add books on shelf
for i in range(8):
    x_offset = 3.7 + (i % 4) * 0.15
    y_offset = 3.2 + (i // 4) * 0.6
    z_offset = 1.0 + (i // 4) * 0.4
    
    bpy.ops.mesh.primitive_cube_add(location=(x_offset, y_offset, z_offset))
    book = bpy.context.active_object
    book.name = f"Book_{{i}}"
    book.scale = (0.05, 0.3, 0.2)
    
    # Random book colors
    book_mat = bpy.data.materials.new(name=f"BookMat_{{i}}")
    book_mat.use_nodes = True
    book_nodes = book_mat.node_tree.nodes
    book_bsdf = book_nodes["Principled BSDF"]
    colors = [(0.8, 0.2, 0.2, 1.0), (0.2, 0.6, 0.2, 1.0), (0.2, 0.2, 0.8, 1.0), (0.7, 0.5, 0.2, 1.0)]
    book_bsdf.inputs['Base Color'].default_value = colors[i % 4]
    book.data.materials.append(book_mat)

# LIGHTING SETUP

# Main ceiling light
bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.8))
main_light = bpy.context.active_object
main_light.name = "MainCeilingLight"
main_light.data.energy = 50
main_light.data.size = 2.0
main_light.data.color = (1.0, 0.95, 0.8)  # Warm white

# Window light (simulate sunlight)
bpy.ops.object.light_add(type='SUN', location=(8, -8, 4))
sun_light = bpy.context.active_object
sun_light.name = "WindowSunlight"
sun_light.data.energy = 8.0
sun_light.data.color = (1.0, 0.9, 0.7)  # Warm sunlight
sun_light.rotation_euler = (0.3, 0, 2.3)

# Ambient light
bpy.ops.object.light_add(type='AREA', location=(-4, -4, 2.5))
ambient_light = bpy.context.active_object
ambient_light.name = "AmbientFill"
ambient_light.data.energy = 15
ambient_light.data.size = 3.0

# WINDOWS - Create window frame
bpy.ops.mesh.primitive_cube_add(location=(6, -2, 1.5))
window_frame = bpy.context.active_object
window_frame.name = "WindowFrame"
window_frame.scale = (0.1, 1.5, 1.2)

# Window glass
bpy.ops.mesh.primitive_plane_add(location=(5.9, -2, 1.5))
window_glass = bpy.context.active_object
window_glass.name = "WindowGlass"
window_glass.scale = (0.05, 1.4, 1.1)
window_glass.rotation_euler = (0, math.pi/2, 0)

# Glass material
glass_mat = bpy.data.materials.new(name="GlassMaterial")
glass_mat.use_nodes = True
glass_nodes = glass_mat.node_tree.nodes
glass_bsdf = glass_nodes["Principled BSDF"]
glass_bsdf.inputs['Base Color'].default_value = (0.9, 0.95, 1.0, 1.0)
glass_bsdf.inputs['Transmission'].default_value = 0.95
glass_bsdf.inputs['Roughness'].default_value = 0.0
glass_bsdf.inputs['IOR'].default_value = 1.45
window_glass.data.materials.append(glass_mat)

# Frame material
frame_mat = bpy.data.materials.new(name="FrameMaterial")
frame_mat.use_nodes = True
frame_nodes = frame_mat.node_tree.nodes
frame_bsdf = frame_nodes["Principled BSDF"]
frame_bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
window_frame.data.materials.append(frame_mat)

# DECORATIVE ELEMENTS

# Plant pot
bpy.ops.mesh.primitive_cylinder_add(location=(4, -4, 0.3), radius=0.3, depth=0.6)
plant_pot = bpy.context.active_object
plant_pot.name = "PlantPot"

# Plant leaves (simplified)
bpy.ops.mesh.primitive_icosphere_add(location=(4, -4, 0.8), radius=0.4)
plant_leaves = bpy.context.active_object
plant_leaves.name = "PlantLeaves"
plant_leaves.scale = (1, 1, 1.5)

# Plant materials
pot_mat = bpy.data.materials.new(name="PotMaterial")
pot_mat.use_nodes = True
pot_nodes = pot_mat.node_tree.nodes
pot_bsdf = pot_nodes["Principled BSDF"]
pot_bsdf.inputs['Base Color'].default_value = (0.4, 0.3, 0.2, 1.0)
plant_pot.data.materials.append(pot_mat)

leaves_mat = bpy.data.materials.new(name="LeavesMaterial")
leaves_mat.use_nodes = True
leaves_nodes = leaves_mat.node_tree.nodes
leaves_bsdf = leaves_nodes["Principled BSDF"]
leaves_bsdf.inputs['Base Color'].default_value = (0.2, 0.6, 0.2, 1.0)
plant_leaves.data.materials.append(leaves_mat)

# CAMERA SETUP for architectural photography
bpy.ops.object.camera_add(location=(-4, -5, 1.6))
camera = bpy.context.active_object
camera.name = "ArchCamera"
camera.rotation_euler = (1.15, 0, -0.6)
scene.camera = camera

# Set camera properties for architectural visualization
camera.data.lens = 24  # Wide angle lens
camera.data.clip_start = 0.1
camera.data.clip_end = 100

# Export professional OBJ file
obj_path = "{temp_dir.replace(chr(92), '/')}/professional_interior.obj"
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=True
)

print("PROFESSIONAL OBJ EXPORT COMPLETE:", obj_path)
print("MTL file should be at:", obj_path.replace('.obj', '.mtl'))

# Also save as .blend file for future editing
blend_path = "{temp_dir.replace(chr(92), '/')}/professional_interior.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("BLEND FILE SAVED:", blend_path)
'''
    
    try:
        result = subprocess.run([
            blender_path,
            '--background',
            '--python-expr', professional_script
        ], capture_output=True, text=True, timeout=180)
        
        print("Professional Interior Creation Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
        # Check if files were created
        obj_file = os.path.join(temp_dir, 'professional_interior.obj')
        mtl_file = os.path.join(temp_dir, 'professional_interior.mtl')
        blend_file = os.path.join(temp_dir, 'professional_interior.blend')
        
        if os.path.exists(obj_file):
            print(f"✅ Professional OBJ created: {obj_file}")
            # Copy to project
            import shutil
            shutil.copy(obj_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\professional_interior.obj')
            print("✅ Copied OBJ to project directory")
            
            if os.path.exists(mtl_file):
                shutil.copy(mtl_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\professional_interior.mtl')
                print("✅ Copied MTL to project directory")
                
            if os.path.exists(blend_file):
                shutil.copy(blend_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\professional_interior.blend')
                print("✅ Copied BLEND to project directory")
        else:
            print("❌ Professional OBJ not found")
            
    except Exception as e:
        print(f"Professional interior creation failed: {e}")

if __name__ == "__main__":
    create_professional_interior()
