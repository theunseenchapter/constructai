#!/usr/bin/env python3
"""
Professional BOQ Renderer for ConstructAI - Fixed Layout Version
"""
import subprocess
import os
import tempfile
import uuid
import json
import shutil
import math
import random
import hashlib

class BOQRenderer:
    """Professional BOQ-based 3D scene renderer with intelligent architectural layout"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_boq_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        
    def render_boq_scene(self, boq_config):
        """Render a professional 3D scene based on BOQ data with intelligent layout"""
        
        self.scene_id = str(uuid.uuid4())
        
        # Get room configuration
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 30, "total_length": 30, "height": 10})
        
        print(f"BOQ Config received: {boq_config}")
        print(f"Rooms to generate: {rooms}")
        print(f"Building dimensions: {building_dims}")
        
        # NEW INTELLIGENT LAYOUT ALGORITHM
        def generate_architectural_layout(rooms_config, total_width, total_length):
            """Generate intelligent architectural layout using actual room dimensions"""
            
            # Extract room dimensions
            room_dims = []
            for room in rooms_config:
                if 'width' in room and 'length' in room:
                    width = room['width']
                    length = room['length']
                else:
                    # Calculate from area if width/length not provided
                    area = room.get('area', 50)
                    if room.get('type') == 'living_room':
                        width = math.sqrt(area * 1.4)
                        length = area / width
                    elif room.get('type') == 'kitchen':
                        width = math.sqrt(area * 1.6)
                        length = area / width
                    elif room.get('type') == 'bedroom':
                        width = math.sqrt(area * 1.2)
                        length = area / width
                    elif room.get('type') == 'bathroom':
                        width = math.sqrt(area * 0.8)
                        length = area / width
                    else:
                        width = math.sqrt(area)
                        length = width
                
                room_dims.append({
                    'name': room.get('name', f'Room_{len(room_dims)+1}'),
                    'type': room.get('type', 'room'),
                    'width': width,
                    'length': length,
                    'height': room.get('height', 3.0)
                })
            
            room_summary = [(r['name'], f"{r['width']:.1f}x{r['length']:.1f}") for r in room_dims]
            print(f"Room dimensions: {room_summary}")
            
            # Calculate total area needed
            total_room_area = sum(d['width'] * d['length'] for d in room_dims)
            margin = 1.0
            available_area = (total_width - 2*margin) * (total_length - 2*margin)
            
            # Scale rooms if needed
            if total_room_area > available_area * 0.8:
                scale_factor = math.sqrt((available_area * 0.8) / total_room_area)
                for room_dim in room_dims:
                    room_dim['width'] *= scale_factor
                    room_dim['length'] *= scale_factor
                print(f"Scaled rooms by {scale_factor:.2f} to fit building")
            
            # Generate smart layout based on room types
            room_positions = []
            
            # Separate rooms by type
            living_rooms = [r for r in room_dims if r['type'] == 'living_room']
            kitchens = [r for r in room_dims if r['type'] == 'kitchen']
            bedrooms = [r for r in room_dims if r['type'] == 'bedroom']
            bathrooms = [r for r in room_dims if r['type'] == 'bathroom']
            other_rooms = [r for r in room_dims if r['type'] not in ['living_room', 'kitchen', 'bedroom', 'bathroom']]
            
            # Layout strategy: Living room first, then kitchen adjacent, bedrooms away from public areas
            current_x = margin
            current_y = margin
            max_height_in_row = 0
            
            # Place living room first (largest public space)
            if living_rooms:
                living_room = living_rooms[0]
                x = current_x + living_room['width']/2
                y = current_y + living_room['length']/2
                room_positions.append({
                    'room': living_room,
                    'x': x, 'y': y,
                    'width': living_room['width'], 'length': living_room['length']
                })
                current_x += living_room['width'] + 1.0
                max_height_in_row = max(max_height_in_row, living_room['length'])
            
            # Place kitchen adjacent to living room
            if kitchens:
                kitchen = kitchens[0]
                if current_x + kitchen['width'] < total_width - margin:
                    # Place to the right of living room
                    x = current_x + kitchen['width']/2
                    y = current_y + kitchen['length']/2
                    room_positions.append({
                        'room': kitchen,
                        'x': x, 'y': y,
                        'width': kitchen['width'], 'length': kitchen['length']
                    })
                    current_x += kitchen['width'] + 1.0
                    max_height_in_row = max(max_height_in_row, kitchen['length'])
                else:
                    # Move to next row
                    current_y += max_height_in_row + 1.0
                    current_x = margin
                    max_height_in_row = 0
                    
                    x = current_x + kitchen['width']/2
                    y = current_y + kitchen['length']/2
                    room_positions.append({
                        'room': kitchen,
                        'x': x, 'y': y,
                        'width': kitchen['width'], 'length': kitchen['length']
                    })
                    current_x += kitchen['width'] + 1.0
                    max_height_in_row = kitchen['length']
            
            # Move to next row for bedrooms
            current_y += max_height_in_row + 1.0
            current_x = margin
            max_height_in_row = 0
            
            # Place bedrooms
            for bedroom in bedrooms:
                if current_x + bedroom['width'] > total_width - margin:
                    # Move to next row
                    current_y += max_height_in_row + 1.0
                    current_x = margin
                    max_height_in_row = 0
                
                if current_y + bedroom['length'] < total_length - margin:
                    x = current_x + bedroom['width']/2
                    y = current_y + bedroom['length']/2
                    room_positions.append({
                        'room': bedroom,
                        'x': x, 'y': y,
                        'width': bedroom['width'], 'length': bedroom['length']
                    })
                    current_x += bedroom['width'] + 1.0
                    max_height_in_row = max(max_height_in_row, bedroom['length'])
            
            # Place bathrooms
            for bathroom in bathrooms:
                if current_x + bathroom['width'] > total_width - margin:
                    # Move to next row
                    current_y += max_height_in_row + 1.0
                    current_x = margin
                    max_height_in_row = 0
                
                if current_y + bathroom['length'] < total_length - margin:
                    x = current_x + bathroom['width']/2
                    y = current_y + bathroom['length']/2
                    room_positions.append({
                        'room': bathroom,
                        'x': x, 'y': y,
                        'width': bathroom['width'], 'length': bathroom['length']
                    })
                    current_x += bathroom['width'] + 1.0
                    max_height_in_row = max(max_height_in_row, bathroom['length'])
            
            # Place other rooms
            for room in other_rooms:
                if current_x + room['width'] > total_width - margin:
                    # Move to next row
                    current_y += max_height_in_row + 1.0
                    current_x = margin
                    max_height_in_row = 0
                
                if current_y + room['length'] < total_length - margin:
                    x = current_x + room['width']/2
                    y = current_y + room['length']/2
                    room_positions.append({
                        'room': room,
                        'x': x, 'y': y,
                        'width': room['width'], 'length': room['length']
                    })
                    current_x += room['width'] + 1.0
                    max_height_in_row = max(max_height_in_row, room['length'])
            
            return room_positions
        
        # Generate intelligent layout
        total_width = building_dims['total_width']
        total_length = building_dims['total_length']
        layout_positions = generate_architectural_layout(rooms, total_width, total_length)
        
        print(f"Generated architectural layout with {len(layout_positions)} rooms")
        for i, pos in enumerate(layout_positions):
            room_name = pos['room']['name']
            print(f"  {room_name}: {pos['width']:.1f}x{pos['length']:.1f} at ({pos['x']:.1f}, {pos['y']:.1f})")

        # Professional Blender script for intelligent layout
        blender_script = f'''
import bpy
import bmesh
import mathutils
import math
import json
import os

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

for device in cprefs.devices:
    if device.type in ['OPTIX', 'CUDA']:
        device.use = True
        print(f"GPU ENABLED: {{device.name}} ({{device.type}})")

scene.cycles.device = 'GPU'
scene.cycles.samples = 1024
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'

# Create materials
def create_material(name, base_color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat

# Material library
materials = {{
    'floor_wood': create_material("FloorWood", (0.45, 0.25, 0.12), 0.4),
    'wall_paint': create_material("WallPaint", (0.9, 0.87, 0.8), 0.7),
    'concrete': create_material("Concrete", (0.6, 0.6, 0.6), 0.8),
    'kitchen_counter': create_material("KitchenCounter", (0.9, 0.9, 0.9), 0.1),
    'furniture_wood': create_material("FurnitureWood", (0.3, 0.15, 0.08), 0.3),
    'fabric_blue': create_material("FabricBlue", (0.2, 0.3, 0.7), 0.8),
    'ceramic_white': create_material("CeramicWhite", (0.95, 0.95, 0.95), 0.05),
    'metal_steel': create_material("MetalSteel", (0.8, 0.8, 0.8), 0.1, 0.9)
}}

# Building dimensions
total_width = {building_dims['total_width']}
total_length = {building_dims['total_length']}
total_height = {building_dims.get('height', 10)}

# Create foundation
bpy.ops.mesh.primitive_plane_add(size=1, location=(total_width/2, total_length/2, 0))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (total_width/2, total_length/2, 1)
foundation.data.materials.append(materials['concrete'])

# Create exterior walls
wall_thickness = 0.3
wall_height = 3.0

# Exterior wall positions
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
    wall.data.materials.append(materials['wall_paint'])

# Layout data
layout_data = {json.dumps(layout_positions)}

print(f"Creating {{len(layout_data)}} rooms with intelligent layout")

# Create rooms with accurate dimensions and positions
for i, room_data in enumerate(layout_data):
    room_info = room_data['room']
    room_name = room_info['name']
    room_type = room_info['type']
    
    x = room_data['x']
    y = room_data['y']
    width = room_data['width']
    length = room_data['length']
    height = room_info.get('height', 3.0)
    
    print(f"Creating room: {{room_name}} ({{room_type}}) at {{x:.1f}}, {{y:.1f}} - {{width:.1f}}x{{length:.1f}}")
    
    # Create room floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0.05))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room_name}}"
    floor.scale = (width/2, length/2, 1)
    
    # Room-specific floor materials
    if room_type in ['kitchen', 'bathroom']:
        floor.data.materials.append(materials['ceramic_white'])
    else:
        floor.data.materials.append(materials['floor_wood'])
    
    # Create interior walls between rooms
    interior_wall_thickness = 0.15
    interior_wall_height = height * 0.8
    
    # Check for adjacent rooms and create dividing walls
    for j, other_room_data in enumerate(layout_data):
        if i >= j:  # Avoid duplicate walls
            continue
            
        other_x = other_room_data['x']
        other_y = other_room_data['y']
        other_width = other_room_data['width']
        other_length = other_room_data['length']
        
        # Check if rooms are adjacent
        room_right = x + width/2
        room_left = x - width/2
        room_top = y + length/2
        room_bottom = y - length/2
        
        other_right = other_x + other_width/2
        other_left = other_x - other_width/2
        other_top = other_y + other_length/2
        other_bottom = other_y - other_length/2
        
        # Vertical wall between rooms
        if abs(room_right - other_left) < 0.5:
            overlap_bottom = max(room_bottom, other_bottom)
            overlap_top = min(room_top, other_top)
            
            if overlap_top > overlap_bottom:
                wall_x = (room_right + other_left) / 2
                wall_y = (overlap_bottom + overlap_top) / 2
                wall_length = overlap_top - overlap_bottom
                
                bpy.ops.mesh.primitive_cube_add(location=(wall_x, wall_y, interior_wall_height/2))
                wall = bpy.context.active_object
                wall.name = f"Wall_{{room_name}}_{{other_room_data['room']['name']}}"
                wall.scale = (interior_wall_thickness/2, wall_length/2, interior_wall_height/2)
                wall.data.materials.append(materials['wall_paint'])
        
        # Horizontal wall between rooms
        elif abs(room_top - other_bottom) < 0.5:
            overlap_left = max(room_left, other_left)
            overlap_right = min(room_right, other_right)
            
            if overlap_right > overlap_left:
                wall_x = (overlap_left + overlap_right) / 2
                wall_y = (room_top + other_bottom) / 2
                wall_width = overlap_right - overlap_left
                
                bpy.ops.mesh.primitive_cube_add(location=(wall_x, wall_y, interior_wall_height/2))
                wall = bpy.context.active_object
                wall.name = f"Wall_{{room_name}}_{{other_room_data['room']['name']}}"
                wall.scale = (wall_width/2, interior_wall_thickness/2, interior_wall_height/2)
                wall.data.materials.append(materials['wall_paint'])
    
    # Add furniture based on room type
    if room_type == 'living_room':
        # Sofa
        sofa_x = x - width*0.2
        sofa_y = y - length*0.2
        bpy.ops.mesh.primitive_cube_add(location=(sofa_x, sofa_y, 0.5))
        sofa = bpy.context.active_object
        sofa.name = f"Sofa_{{room_name}}"
        sofa.scale = (width*0.3, length*0.15, 0.5)
        sofa.data.materials.append(materials['fabric_blue'])
        
        # Coffee table
        table_x = x + width*0.1
        table_y = y
        bpy.ops.mesh.primitive_cube_add(location=(table_x, table_y, 0.4))
        table = bpy.context.active_object
        table.name = f"CoffeeTable_{{room_name}}"
        table.scale = (width*0.2, length*0.15, 0.4)
        table.data.materials.append(materials['furniture_wood'])
        
    elif room_type == 'kitchen':
        # Kitchen counter
        counter_x = x + width*0.2
        counter_y = y
        bpy.ops.mesh.primitive_cube_add(location=(counter_x, counter_y, 0.9))
        counter = bpy.context.active_object
        counter.name = f"Counter_{{room_name}}"
        counter.scale = (width*0.3, length*0.15, 0.9)
        counter.data.materials.append(materials['kitchen_counter'])
        
        # Refrigerator
        fridge_x = x - width*0.3
        fridge_y = y + length*0.2
        bpy.ops.mesh.primitive_cube_add(location=(fridge_x, fridge_y, 1.0))
        fridge = bpy.context.active_object
        fridge.name = f"Fridge_{{room_name}}"
        fridge.scale = (width*0.12, length*0.12, 1.0)
        fridge.data.materials.append(materials['metal_steel'])
        
    elif room_type == 'bedroom':
        # Bed
        bed_x = x
        bed_y = y - length*0.2
        bpy.ops.mesh.primitive_cube_add(location=(bed_x, bed_y, 0.5))
        bed = bpy.context.active_object
        bed.name = f"Bed_{{room_name}}"
        bed.scale = (width*0.4, length*0.3, 0.5)
        bed.data.materials.append(materials['fabric_blue'])
        
        # Wardrobe
        wardrobe_x = x + width*0.3
        wardrobe_y = y + length*0.2
        bpy.ops.mesh.primitive_cube_add(location=(wardrobe_x, wardrobe_y, 1.2))
        wardrobe = bpy.context.active_object
        wardrobe.name = f"Wardrobe_{{room_name}}"
        wardrobe.scale = (width*0.15, length*0.15, 1.2)
        wardrobe.data.materials.append(materials['furniture_wood'])
        
    elif room_type == 'bathroom':
        # Toilet
        toilet_x = x + width*0.2
        toilet_y = y + length*0.2
        bpy.ops.mesh.primitive_cube_add(location=(toilet_x, toilet_y, 0.4))
        toilet = bpy.context.active_object
        toilet.name = f"Toilet_{{room_name}}"
        toilet.scale = (width*0.15, length*0.2, 0.4)
        toilet.data.materials.append(materials['ceramic_white'])
        
        # Sink
        sink_x = x - width*0.2
        sink_y = y - length*0.2
        bpy.ops.mesh.primitive_cube_add(location=(sink_x, sink_y, 0.8))
        sink = bpy.context.active_object
        sink.name = f"Sink_{{room_name}}"
        sink.scale = (width*0.2, length*0.15, 0.8)
        sink.data.materials.append(materials['ceramic_white'])

# Lighting
bpy.ops.object.light_add(type='SUN', location=(total_width/2, total_length/2, 20))
sun = bpy.context.active_object
sun.data.energy = 5.0
sun.rotation_euler = (0.8, 0, 0.5)

# Camera
bpy.ops.object.camera_add(location=(total_width + 10, total_length/2, 8))
camera = bpy.context.active_object
camera.data.lens = 35
camera.rotation_euler = (1.1, 0, 1.57)

# Export
obj_path = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}.obj'
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_colors=True
)

print(f"Professional layout OBJ exported: {{obj_path}}")
print(f"Materials: {{len(bpy.data.materials)}}")
print(f"Objects: {{len(bpy.data.objects)}}")

# Save blend file
blend_path = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}.blend'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("PROFESSIONAL BOQ RENDERING COMPLETE")
'''

        # Write script to temporary file
        script_path = os.path.join(self.temp_dir, f'blender_script_{self.scene_id}.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        # Execute Blender
        try:
            result = subprocess.run([
                self.blender_path, 
                '--background', 
                '--python', script_path
            ], capture_output=True, text=True, timeout=900)
            
            print(f"Blender stdout: {result.stdout}")
            if result.stderr:
                print(f"Blender stderr: {result.stderr}")
            
            if result.returncode != 0:
                return {'success': False, 'error': f'Blender failed with code {result.returncode}'}
                
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Blender rendering timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        # Find generated files
        files = []
        output_dir = os.path.join(os.path.dirname(__file__), 'backend', 'generated_models')
        os.makedirs(output_dir, exist_ok=True)
        
        for extension in ['obj', 'mtl', 'blend']:
            src_file = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.{extension}')
            if os.path.exists(src_file):
                dst_file = os.path.join(output_dir, f'boq_professional_{self.scene_id}.{extension}')
                shutil.copy2(src_file, dst_file)
                files.append({'type': extension, 'path': dst_file})
        
        return {
            'success': True,
            'scene_id': self.scene_id,
            'files': files,
            'output': result.stdout
        }

if __name__ == "__main__":
    """Command line interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python boq_renderer.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        renderer = BOQRenderer()
        result = renderer.render_boq_scene(config)
        
        if result['success']:
            print(f"SCENE_ID: {result['scene_id']}")
            for file_info in result['files']:
                file_type = file_info['type'].upper()
                print(f"{file_type}_FILE: {file_info['path']}")
        else:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
