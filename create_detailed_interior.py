#!/usr/bin/env python3
"""
Create a simplified but professional interior scene
"""
import subprocess
import os
import json
import tempfile

def create_detailed_interior():
    """Create a detailed interior scene"""
    
    temp_dir = tempfile.mkdtemp(prefix='detailed_interior_')
    blender_path = 'D:\\blender\\blender.exe'
    
    detailed_script = f'''
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

# Create room structure
# Floor - larger and more detailed
bpy.ops.mesh.primitive_plane_add(size=16, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"

# Wood floor material
wood_mat = bpy.data.materials.new(name="WoodFloor")
wood_mat.use_nodes = True
bsdf = wood_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.42, 0.26, 0.15, 1.0)  # Rich wood brown
bsdf.inputs["Roughness"].default_value = 0.3
floor.data.materials.append(wood_mat)

# Create 4 walls with proper architecture
# Back wall
bpy.ops.mesh.primitive_cube_add(location=(0, 8, 1.5))
back_wall = bpy.context.active_object
back_wall.name = "BackWall"
back_wall.scale = (8, 0.2, 1.5)

# Left wall
bpy.ops.mesh.primitive_cube_add(location=(-8, 0, 1.5))
left_wall = bpy.context.active_object
left_wall.name = "LeftWall"
left_wall.scale = (0.2, 8, 1.5)

# Right wall with window opening
bpy.ops.mesh.primitive_cube_add(location=(8, 0, 1.5))
right_wall = bpy.context.active_object
right_wall.name = "RightWall"
right_wall.scale = (0.2, 8, 1.5)

# Front wall (partial, for entrance)
bpy.ops.mesh.primitive_cube_add(location=(0, -8, 1.5))
front_wall = bpy.context.active_object
front_wall.name = "FrontWall"
front_wall.scale = (3, 0.2, 1.5)

# Wall material
wall_mat = bpy.data.materials.new(name="WallMaterial")
wall_mat.use_nodes = True
wall_bsdf = wall_mat.node_tree.nodes["Principled BSDF"]
wall_bsdf.inputs["Base Color"].default_value = (0.92, 0.92, 0.88, 1.0)  # Off-white
wall_bsdf.inputs["Roughness"].default_value = 0.8

for wall in [back_wall, left_wall, right_wall, front_wall]:
    wall.data.materials.append(wall_mat)

# Ceiling
bpy.ops.mesh.primitive_plane_add(size=16, location=(0, 0, 3))
ceiling = bpy.context.active_object
ceiling.name = "Ceiling"
ceiling.rotation_euler = (math.pi, 0, 0)

# Ceiling material
ceiling_mat = bpy.data.materials.new(name="CeilingMaterial")
ceiling_mat.use_nodes = True
ceil_bsdf = ceiling_mat.node_tree.nodes["Principled BSDF"]
ceil_bsdf.inputs["Base Color"].default_value = (0.98, 0.98, 0.98, 1.0)  # White
ceiling.data.materials.append(ceiling_mat)

# DETAILED FURNITURE SETUP

# Large sectional sofa
bpy.ops.mesh.primitive_cube_add(location=(-3, 2, 0.4))
sofa_main = bpy.context.active_object
sofa_main.name = "SofaMain"
sofa_main.scale = (2, 1, 0.4)

# Sofa corner piece
bpy.ops.mesh.primitive_cube_add(location=(-1, 4, 0.4))
sofa_corner = bpy.context.active_object
sofa_corner.name = "SofaCorner"
sofa_corner.scale = (1, 1, 0.4)

# Sofa back cushions
bpy.ops.mesh.primitive_cube_add(location=(-3, 2.8, 0.9))
sofa_back1 = bpy.context.active_object
sofa_back1.name = "SofaBack1"
sofa_back1.scale = (2, 0.2, 0.5)

bpy.ops.mesh.primitive_cube_add(location=(-1.2, 4, 0.9))
sofa_back2 = bpy.context.active_object
sofa_back2.name = "SofaBack2"
sofa_back2.scale = (0.2, 1, 0.5)

# Sofa material - gray fabric
sofa_mat = bpy.data.materials.new(name="SofaMaterial")
sofa_mat.use_nodes = True
sofa_bsdf = sofa_mat.node_tree.nodes["Principled BSDF"]
sofa_bsdf.inputs["Base Color"].default_value = (0.4, 0.4, 0.5, 1.0)  # Gray blue
sofa_bsdf.inputs["Roughness"].default_value = 0.9  # High roughness for fabric

for sofa_part in [sofa_main, sofa_corner, sofa_back1, sofa_back2]:
    sofa_part.data.materials.append(sofa_mat)

# Coffee table with detailed design
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.4))
table_top = bpy.context.active_object
table_top.name = "TableTop"
table_top.scale = (1.5, 1, 0.05)

# Table base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.2))
table_base = bpy.context.active_object
table_base.name = "TableBase"
table_base.scale = (1.2, 0.8, 0.2)

# Table material - dark wood
table_mat = bpy.data.materials.new(name="TableMaterial")
table_mat.use_nodes = True
table_bsdf = table_mat.node_tree.nodes["Principled BSDF"]
table_bsdf.inputs["Base Color"].default_value = (0.15, 0.1, 0.05, 1.0)  # Dark wood
table_bsdf.inputs["Roughness"].default_value = 0.2  # Low roughness for polished wood

for table_part in [table_top, table_base]:
    table_part.data.materials.append(table_mat)

# Entertainment center
bpy.ops.mesh.primitive_cube_add(location=(0, 6, 0.8))
tv_stand = bpy.context.active_object
tv_stand.name = "TVStand"
tv_stand.scale = (3, 0.4, 0.8)

# TV screen
bpy.ops.mesh.primitive_cube_add(location=(0, 6.3, 1.5))
tv_screen = bpy.context.active_object
tv_screen.name = "TVScreen"
tv_screen.scale = (2, 0.1, 1.2)

# TV material - black
tv_mat = bpy.data.materials.new(name="TVMaterial")
tv_mat.use_nodes = True
tv_bsdf = tv_mat.node_tree.nodes["Principled BSDF"]
tv_bsdf.inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1.0)  # Almost black
tv_screen.data.materials.append(tv_mat)

# TV stand material - medium wood
stand_mat = bpy.data.materials.new(name="StandMaterial")
stand_mat.use_nodes = True
stand_bsdf = stand_mat.node_tree.nodes["Principled BSDF"]
stand_bsdf.inputs["Base Color"].default_value = (0.3, 0.2, 0.1, 1.0)  # Medium wood
tv_stand.data.materials.append(stand_mat)

# Dining area
# Dining table
bpy.ops.mesh.primitive_cylinder_add(location=(4, -4, 0.75), radius=1.5, depth=0.1)
dining_table = bpy.context.active_object
dining_table.name = "DiningTable"

# Dining chairs
chair_positions = [(2.5, -4, 0.45), (5.5, -4, 0.45), (4, -2.5, 0.45), (4, -5.5, 0.45)]
for i, pos in enumerate(chair_positions):
    # Chair seat
    bpy.ops.mesh.primitive_cube_add(location=pos)
    chair_seat = bpy.context.active_object
    chair_seat.name = f"ChairSeat_{{i}}"
    chair_seat.scale = (0.4, 0.4, 0.05)
    
    # Chair back
    back_pos = (pos[0], pos[1], pos[2] + 0.4)
    bpy.ops.mesh.primitive_cube_add(location=back_pos)
    chair_back = bpy.context.active_object
    chair_back.name = f"ChairBack_{{i}}"
    chair_back.scale = (0.4, 0.05, 0.4)

# Chair material
chair_mat = bpy.data.materials.new(name="ChairMaterial")
chair_mat.use_nodes = True
chair_bsdf = chair_mat.node_tree.nodes["Principled BSDF"]
chair_bsdf.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1.0)  # Medium wood

dining_table.data.materials.append(chair_mat)

# Decorative elements
# Large plant in corner
bpy.ops.mesh.primitive_cylinder_add(location=(6, 6, 0.4), radius=0.4, depth=0.8)
plant_pot = bpy.context.active_object
plant_pot.name = "PlantPot"

# Plant leaves
bpy.ops.mesh.primitive_uv_sphere_add(location=(6, 6, 1.2), radius=0.6)
plant_leaves = bpy.context.active_object
plant_leaves.name = "PlantLeaves"
plant_leaves.scale = (1, 1, 1.8)

# Plant materials
pot_mat = bpy.data.materials.new(name="PotMaterial")
pot_mat.use_nodes = True
pot_bsdf = pot_mat.node_tree.nodes["Principled BSDF"]
pot_bsdf.inputs["Base Color"].default_value = (0.3, 0.2, 0.1, 1.0)  # Terra cotta
plant_pot.data.materials.append(pot_mat)

leaves_mat = bpy.data.materials.new(name="LeavesMaterial")
leaves_mat.use_nodes = True
leaves_bsdf = leaves_mat.node_tree.nodes["Principled BSDF"]
leaves_bsdf.inputs["Base Color"].default_value = (0.1, 0.5, 0.1, 1.0)  # Green
plant_leaves.data.materials.append(leaves_mat)

# Lighting setup for realistic interior
# Main ceiling light
bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.9))
main_light = bpy.context.active_object
main_light.name = "CeilingLight"
main_light.data.energy = 100
main_light.data.size = 3.0

# Window light (natural)
bpy.ops.object.light_add(type='SUN', location=(10, -5, 5))
window_light = bpy.context.active_object
window_light.name = "WindowLight"
window_light.data.energy = 5.0
window_light.rotation_euler = (0.3, 0, 1.8)

# Accent lighting
bpy.ops.object.light_add(type='SPOT', location=(-6, 6, 2.5))
accent_light = bpy.context.active_object
accent_light.name = "AccentLight"
accent_light.data.energy = 30
accent_light.rotation_euler = (1.2, 0, 0.8)

# Camera positioned for architectural view
bpy.ops.object.camera_add(location=(-6, -8, 2.2))
camera = bpy.context.active_object
camera.name = "ArchCamera"
camera.rotation_euler = (1.1, 0, -0.5)
scene.camera = camera

# Export detailed OBJ file
obj_path = "{temp_dir.replace(chr(92), '/')}/detailed_interior.obj"
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=True
)

print("DETAILED OBJ EXPORT COMPLETE:", obj_path)
print("MTL file at:", obj_path.replace('.obj', '.mtl'))

# Save blend file
blend_path = "{temp_dir.replace(chr(92), '/')}/detailed_interior.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("BLEND FILE SAVED:", blend_path)
'''
    
    try:
        result = subprocess.run([
            blender_path,
            '--background',
            '--python-expr', detailed_script
        ], capture_output=True, text=True, timeout=180)
        
        print("Detailed Interior Creation Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
            
        # Check and copy files
        obj_file = os.path.join(temp_dir, 'detailed_interior.obj')
        mtl_file = os.path.join(temp_dir, 'detailed_interior.mtl')
        blend_file = os.path.join(temp_dir, 'detailed_interior.blend')
        
        if os.path.exists(obj_file):
            print(f"✅ Detailed OBJ created: {obj_file}")
            import shutil
            shutil.copy(obj_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\detailed_interior.obj')
            print("✅ Copied OBJ to project directory")
            
            if os.path.exists(mtl_file):
                shutil.copy(mtl_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\detailed_interior.mtl')
                print("✅ Copied MTL to project directory")
                
            if os.path.exists(blend_file):
                shutil.copy(blend_file, 'd:\\\\constructai\\\\backend\\\\generated_models\\\\detailed_interior.blend')
                print("✅ Copied BLEND to project directory")
        else:
            print("❌ Detailed OBJ not found")
            
    except Exception as e:
        print(f"Detailed interior creation failed: {e}")

if __name__ == "__main__":
    create_detailed_interior()
