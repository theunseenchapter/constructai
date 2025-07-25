#!/usr/bin/env python3
"""
Improved Connected Floor Plan Renderer - Creates detailed connected home layouts
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

class ImprovedConnectedRenderer:
    """Creates improved connected floor plans with better detail and materials"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_improved_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
    
    def render_connected_floor_plan(self, boq_config):
        """Render an improved connected floor plan"""
        
        # Use configured scene_id if available, otherwise generate one
        output_config = boq_config.get('output', {})
        self.scene_id = output_config.get('scene_id', str(uuid.uuid4()))
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 20, "total_length": 20, "height": 8})
        
        print(f"Creating improved connected floor plan: {self.scene_id}")
        print(f"Rooms: {len(rooms)}")
        
        # Create improved Blender script
        blender_script = f"""import bpy
import bmesh
from mathutils import Vector
import math

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# Create materials with proper color handling
def create_simple_material(name, color_rgb):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create principled BSDF node
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (color_rgb[0], color_rgb[1], color_rgb[2], 1.0)
    principled.inputs['Roughness'].default_value = 0.5
    
    # Create output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# Create room-specific materials
materials = {{
    'living': create_simple_material('Living_Material', (0.8, 0.52, 0.25)),  # Sandy brown
    'kitchen': create_simple_material('Kitchen_Material', (0.9, 0.9, 0.98)),  # Lavender
    'bedroom': create_simple_material('Bedroom_Material', (0.85, 0.65, 0.13)),  # Goldenrod
    'bathroom': create_simple_material('Bathroom_Material', (0.53, 0.81, 0.92)),  # Sky blue
    'dining': create_simple_material('Dining_Material', (0.82, 0.71, 0.55)),  # Tan
    'utility': create_simple_material('Utility_Material', (0.5, 0.5, 0.5)),  # Gray
    'wall': create_simple_material('Wall_Material', (0.96, 0.96, 0.96)),  # White smoke
    'door': create_simple_material('Door_Material', (0.63, 0.32, 0.18)),  # Sienna
    'window': create_simple_material('Window_Material', (0.53, 0.81, 0.98)),  # Light blue
    'furniture': create_simple_material('Furniture_Material', (0.55, 0.27, 0.07)),  # Saddle brown
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
foundation.data.materials.append(materials['wall'])

# Calculate room layout
total_rooms = len(room_data)
rooms_per_row = 3
grid_width = building_width - 4
grid_length = building_length - 4
cell_width = grid_width / rooms_per_row
cell_length = grid_length / math.ceil(total_rooms / rooms_per_row)

# Create detailed room layout
for i, room in enumerate(room_data):
    room_name = room.get('name', f'Room_{{i}}').replace(' ', '_')
    room_type = room.get('type', 'bedroom').lower()
    
    # Calculate grid position
    row = i // rooms_per_row
    col = i % rooms_per_row
    
    # Calculate room position
    room_x = -building_width/2 + 2 + (col + 0.5) * cell_width
    room_y = -building_length/2 + 2 + (row + 0.5) * cell_length
    room_width = min(cell_width * 0.9, room.get('width', 8))
    room_length = min(cell_length * 0.9, room.get('length', 8))
    room_height = building_height * 0.8
    
    # Create floor
    bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y, 0.05))
    floor = bpy.context.active_object
    floor.scale = (room_width/2, room_length/2, 0.05)
    floor.name = f"Floor_{{room_name}}"
    
    # Assign material based on room type
    if room_type in materials:
        floor.data.materials.append(materials[room_type])
    else:
        floor.data.materials.append(materials['living'])
    
    # Create walls
    wall_height = room_height/2
    wall_thickness = 0.15
    
    # Front wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y + room_length/2, wall_height))
    wall = bpy.context.active_object
    wall.scale = (room_width/2, wall_thickness, wall_height)
    wall.name = f"Wall_Front_{{room_name}}"
    wall.data.materials.append(materials['wall'])
    
    # Back wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y - room_length/2, wall_height))
    wall = bpy.context.active_object
    wall.scale = (room_width/2, wall_thickness, wall_height)
    wall.name = f"Wall_Back_{{room_name}}"
    wall.data.materials.append(materials['wall'])
    
    # Left wall (with door opening if not first in row)
    if col > 0:
        # Create wall with door opening
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/2, room_y + room_length/4, wall_height))
        wall = bpy.context.active_object
        wall.scale = (wall_thickness, room_length/4, wall_height)
        wall.name = f"Wall_Left_Top_{{room_name}}"
        wall.data.materials.append(materials['wall'])
        
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/2, room_y - room_length/4, wall_height))
        wall = bpy.context.active_object
        wall.scale = (wall_thickness, room_length/4, wall_height)
        wall.name = f"Wall_Left_Bottom_{{room_name}}"
        wall.data.materials.append(materials['wall'])
        
        # Add door
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/2, room_y, 0.8))
        door = bpy.context.active_object
        door.scale = (0.05, 0.4, 0.8)
        door.name = f"Door_Left_{{room_name}}"
        door.data.materials.append(materials['door'])
    else:
        # Full wall
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/2, room_y, wall_height))
        wall = bpy.context.active_object
        wall.scale = (wall_thickness, room_length/2, wall_height)
        wall.name = f"Wall_Left_{{room_name}}"
        wall.data.materials.append(materials['wall'])
    
    # Right wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x + room_width/2, room_y, wall_height))
    wall = bpy.context.active_object
    wall.scale = (wall_thickness, room_length/2, wall_height)
    wall.name = f"Wall_Right_{{room_name}}"
    wall.data.materials.append(materials['wall'])
    
    # Add furniture based on room type
    furniture_height = 0.4
    
    if room_type == 'living':
        # Sofa
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/3, room_y, furniture_height/2))
        furniture = bpy.context.active_object
        furniture.scale = (room_width/4, 0.4, furniture_height/2)
        furniture.name = f"Sofa_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y, 0.2))
        furniture = bpy.context.active_object
        furniture.scale = (0.6, 0.3, 0.2)
        furniture.name = f"Table_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y, furniture_height/2))
        furniture = bpy.context.active_object
        furniture.scale = (room_width/3, 0.5, furniture_height/2)
        furniture.name = f"Island_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Counter
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/3, room_y + room_length/3, furniture_height/2))
        furniture = bpy.context.active_object
        furniture.scale = (room_width/4, 0.3, furniture_height/2)
        furniture.name = f"Counter_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
    elif room_type == 'bedroom':
        # Bed
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y, 0.3))
        furniture = bpy.context.active_object
        furniture.scale = (room_width/3, room_length/3, 0.3)
        furniture.name = f"Bed_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Dresser
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x + room_width/3, room_y, furniture_height/2))
        furniture = bpy.context.active_object
        furniture.scale = (0.3, 0.25, furniture_height/2)
        furniture.name = f"Dresser_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
    elif room_type == 'bathroom':
        # Toilet
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x - room_width/3, room_y + room_length/3, 0.2))
        furniture = bpy.context.active_object
        furniture.scale = (0.15, 0.25, 0.2)
        furniture.name = f"Toilet_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Sink
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x + room_width/3, room_y + room_length/3, furniture_height/2))
        furniture = bpy.context.active_object
        furniture.scale = (0.25, 0.15, 0.05)
        furniture.name = f"Sink_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])
        
        # Bathtub
        bpy.ops.mesh.primitive_cube_add(size=2, location=(room_x, room_y - room_length/3, 0.25))
        furniture = bpy.context.active_object
        furniture.scale = (room_width/3, 0.3, 0.25)
        furniture.name = f"Bathtub_{{room_name}}"
        furniture.data.materials.append(materials['furniture'])

# Add connecting hallway
hallway_width = 2
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.05))
hallway = bpy.context.active_object
hallway.scale = (building_width/2, hallway_width/2, 0.05)
hallway.name = "Main_Hallway"
hallway.data.materials.append(materials['living'])

# Add lighting
light_data = bpy.data.lights.new(name="Sun", type='SUN')
light_data.energy = 5
light_object = bpy.data.objects.new(name="Sun", object_data=light_data)
bpy.context.collection.objects.link(light_object)
light_object.location = (building_width, building_length, building_height * 2)
light_object.rotation_euler = (0.785, 0, 0.785)

# Add area light for better illumination
area_light = bpy.data.lights.new(name="Area", type='AREA')
area_light.energy = 100
area_light.size = 15
area_object = bpy.data.objects.new(name="Area", object_data=area_light)
bpy.context.collection.objects.link(area_object)
area_object.location = (0, 0, building_height * 1.5)

# Position camera for good view
bpy.ops.object.camera_add(location=(building_width*0.7, -building_length*0.7, building_height*0.7))
camera = bpy.context.active_object
camera.rotation_euler = (1.0, 0, 0.785)
scene.camera = camera

# Configure render settings
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True

# Export files
output_dir = "{self.temp_dir.replace(chr(92), '/')}"
blend_file = output_dir + "/improved_floor_plan_{self.scene_id}.blend"
obj_file = output_dir + "/improved_floor_plan_{self.scene_id}.obj"
mtl_file = output_dir + "/improved_floor_plan_{self.scene_id}.mtl"
render_file = output_dir + "/improved_floor_plan_{self.scene_id}.png"

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=blend_file)
print("BLEND_FILE: " + blend_file)

# Export OBJ with materials
try:
    bpy.ops.wm.obj_export(
        filepath=obj_file,
        check_existing=False,
        export_selected_objects=False,
        export_materials=True,
        export_material_groups=True,
        export_vertex_groups=False,
        export_smooth_groups=False
    )
    print("OBJ_FILE: " + obj_file)
    print("MTL_FILE: " + mtl_file)
except:
    try:
        bpy.ops.export_scene.obj(
            filepath=obj_file,
            check_existing=False,
            use_selection=False,
            use_materials=True,
            use_mesh_modifiers=True
        )
        print("OBJ_FILE: " + obj_file)
        print("MTL_FILE: " + mtl_file)
    except Exception as e:
        print("OBJ export failed: " + str(e))

# Render preview image
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
        
        # Copy files to public directory with cache-busting
        public_renders = 'public/renders'
        os.makedirs(public_renders, exist_ok=True)
        
        cache_buster = f"?v={int(uuid.uuid4().int % 1e10)}"
        
        if 'obj_file' in result:
            src_obj = result['obj_file']
            dst_obj = os.path.join(public_renders, os.path.basename(src_obj))
            if os.path.exists(src_obj):
                shutil.copy2(src_obj, dst_obj)
                result['obj_file'] = f"/renders/{os.path.basename(src_obj)}{cache_buster}"
        
        if 'mtl_file' in result:
            src_mtl = result['mtl_file']
            dst_mtl = os.path.join(public_renders, os.path.basename(src_mtl))
            if os.path.exists(src_mtl):
                shutil.copy2(src_mtl, dst_mtl)
                result['mtl_file'] = f"/renders/{os.path.basename(src_mtl)}{cache_buster}"
        
        if 'blend_file' in result:
            src_blend = result['blend_file']
            dst_blend = os.path.join(public_renders, os.path.basename(src_blend))
            if os.path.exists(src_blend):
                shutil.copy2(src_blend, dst_blend)
                result['blend_file'] = f"/renders/{os.path.basename(src_blend)}{cache_buster}"
        
        if 'render_file' in result:
            src_render = result['render_file']
            dst_render = os.path.join(public_renders, os.path.basename(src_render))
            if os.path.exists(src_render):
                shutil.copy2(src_render, dst_render)
                result['render_file'] = f"/renders/{os.path.basename(src_render)}{cache_buster}"
        
        result['success'] = 'obj_file' in result and 'mtl_file' in result
        return result
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

def main():
    """Main function - can be called with config file or run test"""
    import sys
    
    if len(sys.argv) > 1:
        # Called with config file from API
        config_file = sys.argv[1]
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        renderer = ImprovedConnectedRenderer()
        try:
            result = renderer.render_connected_floor_plan(config)
            print(f"Render result: {result}")
            return result
        finally:
            renderer.cleanup()
    else:
        # Test mode
        renderer = ImprovedConnectedRenderer()
        
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
