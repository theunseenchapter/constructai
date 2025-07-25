#!/usr/bin/env python3
"""
Enhanced Connected Floor Plan Renderer - Creates detailed, colorful connected home layouts
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

class DetailedConnectedRenderer:
    """Creates detailed connected floor plans with proper room layouts"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_detailed_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
    
    def render_connected_floor_plan(self, boq_config):
        """Render a detailed connected floor plan"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 20, "total_length": 20, "height": 8})
        
        print(f"Creating detailed connected floor plan: {self.scene_id}")
        print(f"Rooms: {len(rooms)}")
        
        # Create detailed Blender script
        blender_script = f"""import bpy
import bmesh
from mathutils import Vector
import math

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# Create materials
def create_material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create principled BSDF node
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = color + (1.0,)
    principled.inputs['Roughness'].default_value = roughness
    principled.inputs['Metallic'].default_value = metallic
    
    # Create output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# Create room-specific materials
materials = {{
    'living': create_material('Living_Material', (0.8, 0.52, 0.25)),  # Sandy brown
    'kitchen': create_material('Kitchen_Material', (0.9, 0.9, 0.98)),  # Lavender
    'bedroom': create_material('Bedroom_Material', (0.85, 0.65, 0.13)),  # Goldenrod
    'bathroom': create_material('Bathroom_Material', (0.53, 0.81, 0.92)),  # Sky blue
    'dining': create_material('Dining_Material', (0.82, 0.71, 0.55)),  # Tan
    'utility': create_material('Utility_Material', (0.5, 0.5, 0.5)),  # Gray
    'wall': create_material('Wall_Material', (0.96, 0.96, 0.96)),  # White smoke
    'door': create_material('Door_Material', (0.63, 0.32, 0.18)),  # Sienna
    'window': create_material('Window_Material', (0.53, 0.81, 0.98, 0.6)),  # Light blue glass
    'furniture': create_material('Furniture_Material', (0.55, 0.27, 0.07)),  # Saddle brown
}}

# Room data
room_data = {rooms}
building_width = {building_dims['total_width']}
building_length = {building_dims['total_length']}
building_height = {building_dims['height']}

# Create foundation
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -0.1))
foundation = bpy.context.active_object
foundation.scale = (building_width/2, building_length/2, 0.1)
foundation.name = "Foundation"

# Create detailed room layout
room_positions = []
current_x = -building_width/2 + 2
current_y = -building_length/2 + 2
row_height = 0
rooms_per_row = 3

for i, room in enumerate(room_data):
    room_name = room.get('name', f'Room_{{i}}')
    room_type = room.get('type', 'bedroom').lower()
    room_width = room.get('width', 8)
    room_length = room.get('length', 8)
    room_height = room.get('height', 10)
    
    # Calculate position
    if i > 0 and i % rooms_per_row == 0:
        current_x = -building_width/2 + 2
        current_y += row_height + 2
        row_height = 0
    
    room_x = current_x + room_width/2
    room_y = current_y + room_length/2
    room_positions.append((room_x, room_y, room_width, room_length, room_type, room_name))
    
    # Update positions
    current_x += room_width + 1
    row_height = max(row_height, room_length)

# Create rooms
for i, (x, y, width, length, room_type, name) in enumerate(room_positions):
    # Create floor
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y, 0.05))
    floor = bpy.context.active_object
    floor.scale = (width/2, length/2, 0.05)
    floor.name = f"Floor_{{name}}"
    
    # Assign material
    if room_type in materials:
        floor.data.materials.append(materials[room_type])
    else:
        floor.data.materials.append(materials['living'])
    
    # Create walls
    wall_height = building_height/2
    wall_thickness = 0.1
    
    # Front wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y + length/2, wall_height))
    wall = bpy.context.active_object
    wall.scale = (width/2, wall_thickness, wall_height)
    wall.name = f"Wall_Front_{{name}}"
    wall.data.materials.append(materials['wall'])
    
    # Back wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y - length/2, wall_height))
    wall = bpy.context.active_object
    wall.scale = (width/2, wall_thickness, wall_height)
    wall.name = f"Wall_Back_{{name}}"
    wall.data.materials.append(materials['wall'])
    
    # Left wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x - width/2, y, wall_height))
    wall = bpy.context.active_object
    wall.scale = (wall_thickness, length/2, wall_height)
    wall.name = f"Wall_Left_{{name}}"
    wall.data.materials.append(materials['wall'])
    
    # Right wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x + width/2, y, wall_height))
    wall = bpy.context.active_object
    wall.scale = (wall_thickness, length/2, wall_height)
    wall.name = f"Wall_Right_{{name}}"
    wall.data.materials.append(materials['wall'])
    
    # Add simple furniture based on room type
    if room_type == 'living':
        # Sofa
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x - width/4, y, 0.3))
        furniture = bpy.context.active_object
        furniture.scale = (width/4, 0.4, 0.3)
        furniture.name = f"Sofa_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y, 0.15))
        furniture = bpy.context.active_object
        furniture.scale = (0.8, 0.4, 0.15)
        furniture.name = f"Table_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y, 0.4))
        furniture = bpy.context.active_object
        furniture.scale = (width/3, 0.6, 0.4)
        furniture.name = f"Island_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Cabinets
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x - width/3, y + length/3, 0.4))
        furniture = bpy.context.active_object
        furniture.scale = (width/4, 0.3, 0.4)
        furniture.name = f"Cabinets_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
    elif room_type == 'bedroom':
        # Bed
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y, 0.25))
        furniture = bpy.context.active_object
        furniture.scale = (width/3, length/3, 0.25)
        furniture.name = f"Bed_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Dresser
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x + width/3, y, 0.4))
        furniture = bpy.context.active_object
        furniture.scale = (0.4, 0.3, 0.4)
        furniture.name = f"Dresser_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
    elif room_type == 'bathroom':
        # Toilet
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x - width/4, y + length/4, 0.2))
        furniture = bpy.context.active_object
        furniture.scale = (0.2, 0.3, 0.2)
        furniture.name = f"Toilet_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Sink
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x + width/4, y + length/4, 0.4))
        furniture = bpy.context.active_object
        furniture.scale = (0.3, 0.2, 0.05)
        furniture.name = f"Sink_{{name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Bathtub
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y - length/4, 0.2))
        furniture = bpy.context.active_object
        furniture.scale = (width/3, 0.4, 0.2)
        furniture.name = f"Bathtub_{{name}}"
        furniture.data.materials.append(materials['furniture'])
    
    # Add doors (openings in walls)
    if i < len(room_positions) - 1:
        # Create door opening by scaling down wall section
        door_x = x + width/2
        door_y = y
        bpy.ops.mesh.primitive_cube_add(size=2, location=(door_x, door_y, 1))
        door = bpy.context.active_object
        door.scale = (0.05, 0.4, 1)
        door.name = f"Door_{{name}}"
        door.data.materials.append(materials['door'])

# Add connecting hallway
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.05))
hallway = bpy.context.active_object
hallway.scale = (building_width/2, 1, 0.05)
hallway.name = "Hallway"
hallway.data.materials.append(materials['living'])

# Add lighting
light_data = bpy.data.lights.new(name="MainLight", type='SUN')
light_data.energy = 3
light_object = bpy.data.objects.new(name="MainLight", object_data=light_data)
bpy.context.collection.objects.link(light_object)
light_object.location = (10, 10, 20)
light_object.rotation_euler = (0.785, 0, 0.785)

# Add area light
area_light = bpy.data.lights.new(name="AreaLight", type='AREA')
area_light.energy = 50
area_light.size = 10
area_object = bpy.data.objects.new(name="AreaLight", object_data=area_light)
bpy.context.collection.objects.link(area_object)
area_object.location = (0, 0, 15)

# Add camera
bpy.ops.object.camera_add(location=(building_width*0.8, -building_length*0.8, building_height*0.8))
camera = bpy.context.active_object
camera.rotation_euler = (0.8, 0, 0.8)
scene.camera = camera

# Configure render settings
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = True

# Export files
output_dir = "{self.temp_dir.replace(chr(92), '/')}"
blend_file = output_dir + "/detailed_floor_plan_{self.scene_id}.blend"
obj_file = output_dir + "/detailed_floor_plan_{self.scene_id}.obj"
mtl_file = output_dir + "/detailed_floor_plan_{self.scene_id}.mtl"
render_file = output_dir + "/detailed_floor_plan_{self.scene_id}.png"

# Save files
bpy.ops.wm.save_as_mainfile(filepath=blend_file)
print("BLEND_FILE: " + blend_file)

# Export OBJ with materials
try:
    # Try new Blender 4.x export
    bpy.ops.wm.obj_export(
        filepath=obj_file,
        check_existing=False,
        export_selected_objects=False,
        export_materials=True,
        export_material_groups=True,
        export_vertex_groups=False,
        export_smooth_groups=False,
        smooth_group_bitflags=False
    )
    print("OBJ_FILE: " + obj_file)
    print("MTL_FILE: " + mtl_file)
except:
    try:
        # Fallback to old export
        bpy.ops.export_scene.obj(
            filepath=obj_file,
            check_existing=False,
            use_selection=False,
            use_materials=True,
            use_mesh_modifiers=True,
            use_smooth_groups=False,
            use_vertex_groups=False
        )
        print("OBJ_FILE: " + obj_file)
        print("MTL_FILE: " + mtl_file)
    except Exception as e:
        print("OBJ export failed: " + str(e))

# Render image
try:
    scene.render.filepath = render_file
    bpy.ops.render.render(write_still=True)
    print("RENDER_FILE: " + render_file)
except Exception as e:
    print("Render failed: " + str(e))

print("SCENE_ID: {self.scene_id}")
"""

        # Write script to file
        script_path = os.path.join(self.temp_dir, f"render_script_{self.scene_id}.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(blender_script)
        
        # Run Blender
        cmd = [
            self.blender_path,
            '--background',
            '--python', script_path,
            '--',
            '--verbose'
        ]
        
        print(f"Running Blender: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=self.temp_dir
            )
            
            print("STDOUT:")
            print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
            
            return self.parse_output(result.stdout)
            
        except subprocess.TimeoutExpired:
            print("Blender process timed out")
            return None
        except Exception as e:
            print(f"Error running Blender: {e}")
            return None
    
    def parse_output(self, output):
        """Parse Blender output to extract file paths"""
        result = {
            'scene_id': self.scene_id,
            'success': False
        }
        
        lines = output.split('\n')
        for line in lines:
            if 'SCENE_ID:' in line:
                result['scene_id'] = line.split('SCENE_ID:')[1].strip()
            elif 'BLEND_FILE:' in line:
                result['blend_file'] = line.split('BLEND_FILE:')[1].strip()
            elif 'OBJ_FILE:' in line:
                result['obj_file'] = line.split('OBJ_FILE:')[1].strip()
            elif 'MTL_FILE:' in line:
                result['mtl_file'] = line.split('MTL_FILE:')[1].strip()
            elif 'RENDER_FILE:' in line:
                result['render_file'] = line.split('RENDER_FILE:')[1].strip()
        
        # Copy files to public directory
        public_renders = 'public/renders'
        os.makedirs(public_renders, exist_ok=True)
        
        if 'obj_file' in result:
            src_obj = result['obj_file']
            dst_obj = os.path.join(public_renders, os.path.basename(src_obj))
            if os.path.exists(src_obj):
                shutil.copy2(src_obj, dst_obj)
                result['obj_file'] = f"/renders/{os.path.basename(src_obj)}"
        
        if 'mtl_file' in result:
            src_mtl = result['mtl_file']
            dst_mtl = os.path.join(public_renders, os.path.basename(src_mtl))
            if os.path.exists(src_mtl):
                shutil.copy2(src_mtl, dst_mtl)
                result['mtl_file'] = f"/renders/{os.path.basename(src_mtl)}"
        
        if 'blend_file' in result:
            src_blend = result['blend_file']
            dst_blend = os.path.join(public_renders, os.path.basename(src_blend))
            if os.path.exists(src_blend):
                shutil.copy2(src_blend, dst_blend)
                result['blend_file'] = f"/renders/{os.path.basename(src_blend)}"
        
        if 'render_file' in result:
            src_render = result['render_file']
            dst_render = os.path.join(public_renders, os.path.basename(src_render))
            if os.path.exists(src_render):
                shutil.copy2(src_render, dst_render)
                result['render_file'] = f"/renders/{os.path.basename(src_render)}"
        
        result['success'] = 'obj_file' in result and 'mtl_file' in result
        return result
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

def main():
    """Test the renderer"""
    renderer = DetailedConnectedRenderer()
    
    # Test configuration
    test_config = {
        "rooms": [
            {"name": "Living Room", "type": "living", "width": 16, "length": 12, "height": 10},
            {"name": "Kitchen", "type": "kitchen", "width": 12, "length": 10, "height": 10},
            {"name": "Master Bedroom", "type": "bedroom", "width": 14, "length": 12, "height": 10},
            {"name": "Bedroom 2", "type": "bedroom", "width": 12, "length": 10, "height": 10},
            {"name": "Bedroom 3", "type": "bedroom", "width": 10, "length": 10, "height": 10},
            {"name": "Bathroom 1", "type": "bathroom", "width": 8, "length": 8, "height": 10},
            {"name": "Bathroom 2", "type": "bathroom", "width": 6, "length": 8, "height": 10},
            {"name": "Dining Room", "type": "dining", "width": 12, "length": 10, "height": 10},
            {"name": "Utility Room", "type": "utility", "width": 8, "length": 6, "height": 10}
        ],
        "building_dimensions": {
            "total_width": 40,
            "total_length": 30,
            "height": 12
        }
    }
    
    try:
        result = renderer.render_connected_floor_plan(test_config)
        print(f"Render result: {result}")
        return result
    finally:
        renderer.cleanup()

if __name__ == "__main__":
    main()
