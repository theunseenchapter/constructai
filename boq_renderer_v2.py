#!/usr/bin/env python3
"""
Professional BOQ Renderer for ConstructAI - High Quality Version
"""
import subprocess
import os
import tempfile
import uuid
import json
import shutil

class BOQRenderer:
    """Professional BOQ-based 3D scene renderer with detailed furniture and materials"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_boq_')
        self.blender_path = 'D:\\blender\\blender.exe'
        self.scene_id = None
        
    def render_boq_scene(self, boq_config):
        """Render a professional 3D scene based on BOQ data"""
        
        self.scene_id = str(uuid.uuid4())
        
        # Get room configuration
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 30, "total_length": 30, "height": 10})
        
        # Professional Blender script for BOQ-based rendering
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

# Professional material creation
def create_material(name, base_color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat

# Define room configurations
rooms_config = {json.dumps(rooms)}
building_dims = {json.dumps(building_dims)}

# Create rooms with professional detail
for i, room in enumerate(rooms_config):
    room_name = room.get('name', f'Room_{{i+1}}')
    width = room.get('width', 12)
    length = room.get('length', 12)
    height = room.get('height', 10)
    position = room.get('position', {{"x": i*18, "y": 0, "z": 0}})
    room_type = room.get('type', 'bedroom')
    
    # Create room structure
    # Floor with detailed material
    bpy.ops.mesh.primitive_plane_add(size=max(width, length), location=(position['x'], position['y'], position['z']))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room_name}}"
    
    # Professional floor material based on room type
    if room_type == 'kitchen' or room_type == 'bathroom':
        floor_mat = create_material(f"TileFloor_{{room_name}}", (0.85, 0.85, 0.9), 0.1)
    else:
        floor_mat = create_material(f"WoodFloor_{{room_name}}", (0.42, 0.26, 0.15), 0.3)
    
    floor.data.materials.append(floor_mat)
    
    # Create walls with proper thickness and height
    wall_thickness = 0.3
    wall_height = height / 2
    
    # Back wall
    bpy.ops.mesh.primitive_cube_add(location=(position['x'], position['y'] + length/2, position['z'] + wall_height))
    back_wall = bpy.context.active_object
    back_wall.name = f"BackWall_{{room_name}}"
    back_wall.scale = (width/2, wall_thickness/2, wall_height)
    
    # Left wall
    bpy.ops.mesh.primitive_cube_add(location=(position['x'] - width/2, position['y'], position['z'] + wall_height))
    left_wall = bpy.context.active_object
    left_wall.name = f"LeftWall_{{room_name}}"
    left_wall.scale = (wall_thickness/2, length/2, wall_height)
    
    # Right wall
    bpy.ops.mesh.primitive_cube_add(location=(position['x'] + width/2, position['y'], position['z'] + wall_height))
    right_wall = bpy.context.active_object
    right_wall.name = f"RightWall_{{room_name}}"
    right_wall.scale = (wall_thickness/2, length/2, wall_height)
    
    # Front wall (partial for entrance)
    bpy.ops.mesh.primitive_cube_add(location=(position['x'], position['y'] - length/2, position['z'] + wall_height))
    front_wall = bpy.context.active_object
    front_wall.name = f"FrontWall_{{room_name}}"
    front_wall.scale = (width/4, wall_thickness/2, wall_height)
    
    # Wall material
    wall_mat = create_material(f"WallMaterial_{{room_name}}", (0.92, 0.92, 0.88), 0.8)
    for wall in [back_wall, left_wall, right_wall, front_wall]:
        wall.data.materials.append(wall_mat)
    
    # Add detailed furniture based on room type
    if room_type == 'bedroom':
        # Bed with frame and mattress
        bed_pos = (position['x'] - width/4, position['y'] + length/4, position['z'] + 0.5)
        
        # Bed frame
        bpy.ops.mesh.primitive_cube_add(location=bed_pos)
        bed_frame = bpy.context.active_object
        bed_frame.name = f"BedFrame_{{room_name}}"
        bed_frame.scale = (2.5, 4, 0.3)
        
        # Mattress
        mattress_pos = (bed_pos[0], bed_pos[1], bed_pos[2] + 0.5)
        bpy.ops.mesh.primitive_cube_add(location=mattress_pos)
        mattress = bpy.context.active_object
        mattress.name = f"Mattress_{{room_name}}"
        mattress.scale = (2.3, 3.8, 0.4)
        
        # Headboard
        headboard_pos = (bed_pos[0], bed_pos[1] + 2.2, bed_pos[2] + 1.5)
        bpy.ops.mesh.primitive_cube_add(location=headboard_pos)
        headboard = bpy.context.active_object
        headboard.name = f"Headboard_{{room_name}}"
        headboard.scale = (2.5, 0.3, 1.2)
        
        # Bed materials
        bed_mat = create_material(f"BedMaterial_{{room_name}}", (0.4, 0.2, 0.1), 0.2)
        mattress_mat = create_material(f"MattressMaterial_{{room_name}}", (0.9, 0.9, 0.95), 0.7)
        
        bed_frame.data.materials.append(bed_mat)
        mattress.data.materials.append(mattress_mat)
        headboard.data.materials.append(bed_mat)
        
        # Wardrobe
        wardrobe_pos = (position['x'] + width/3, position['y'] + length/3, position['z'] + 2)
        bpy.ops.mesh.primitive_cube_add(location=wardrobe_pos)
        wardrobe = bpy.context.active_object
        wardrobe.name = f"Wardrobe_{{room_name}}"
        wardrobe.scale = (2, 1, 4)
        
        # Wardrobe doors
        door1_pos = (wardrobe_pos[0] - 0.5, wardrobe_pos[1] - 1.1, wardrobe_pos[2])
        bpy.ops.mesh.primitive_cube_add(location=door1_pos)
        door1 = bpy.context.active_object
        door1.name = f"WardrobeDoor1_{{room_name}}"
        door1.scale = (0.9, 0.1, 3.8)
        
        door2_pos = (wardrobe_pos[0] + 0.5, wardrobe_pos[1] - 1.1, wardrobe_pos[2])
        bpy.ops.mesh.primitive_cube_add(location=door2_pos)
        door2 = bpy.context.active_object
        door2.name = f"WardrobeDoor2_{{room_name}}"
        door2.scale = (0.9, 0.1, 3.8)
        
        # Wardrobe material
        wardrobe_mat = create_material(f"WardrobeMaterial_{{room_name}}", (0.3, 0.15, 0.1), 0.1)
        for obj in [wardrobe, door1, door2]:
            obj.data.materials.append(wardrobe_mat)
        
        # Bedside table
        table_pos = (position['x'] + width/4, position['y'] + length/4, position['z'] + 0.8)
        bpy.ops.mesh.primitive_cube_add(location=table_pos)
        bedside_table = bpy.context.active_object
        bedside_table.name = f"BedsideTable_{{room_name}}"
        bedside_table.scale = (0.8, 0.8, 0.8)
        
        # Table lamp
        lamp_pos = (table_pos[0], table_pos[1], table_pos[2] + 1.2)
        bpy.ops.mesh.primitive_uv_sphere_add(location=lamp_pos, radius=0.3)
        lamp = bpy.context.active_object
        lamp.name = f"TableLamp_{{room_name}}"
        
        table_mat = create_material(f"TableMaterial_{{room_name}}", (0.3, 0.15, 0.1), 0.2)
        lamp_mat = create_material(f"LampMaterial_{{room_name}}", (0.9, 0.9, 0.7), 0.1)
        
        bedside_table.data.materials.append(table_mat)
        lamp.data.materials.append(lamp_mat)
        
    elif room_type == 'living_room':
        # Sofa with detailed structure
        sofa_pos = (position['x'], position['y'], position['z'] + 1)
        
        # Sofa body
        bpy.ops.mesh.primitive_cube_add(location=sofa_pos)
        sofa_body = bpy.context.active_object
        sofa_body.name = f"SofaBody_{{room_name}}"
        sofa_body.scale = (4, 2, 1)
        
        # Backrest
        backrest_pos = (sofa_pos[0], sofa_pos[1] + 1.5, sofa_pos[2] + 1.5)
        bpy.ops.mesh.primitive_cube_add(location=backrest_pos)
        backrest = bpy.context.active_object
        backrest.name = f"SofaBackrest_{{room_name}}"
        backrest.scale = (4, 0.5, 1.5)
        
        # Armrests
        armrest1_pos = (sofa_pos[0] - 3.5, sofa_pos[1], sofa_pos[2] + 1)
        bpy.ops.mesh.primitive_cube_add(location=armrest1_pos)
        armrest1 = bpy.context.active_object
        armrest1.name = f"SofaArmrest1_{{room_name}}"
        armrest1.scale = (0.5, 2, 1)
        
        armrest2_pos = (sofa_pos[0] + 3.5, sofa_pos[1], sofa_pos[2] + 1)
        bpy.ops.mesh.primitive_cube_add(location=armrest2_pos)
        armrest2 = bpy.context.active_object
        armrest2.name = f"SofaArmrest2_{{room_name}}"
        armrest2.scale = (0.5, 2, 1)
        
        # Sofa material
        sofa_mat = create_material(f"SofaMaterial_{{room_name}}", (0.7, 0.5, 0.3), 0.7)
        for obj in [sofa_body, backrest, armrest1, armrest2]:
            obj.data.materials.append(sofa_mat)
        
        # Coffee table with legs
        table_pos = (position['x'], position['y'] - 3, position['z'] + 0.5)
        bpy.ops.mesh.primitive_cube_add(location=table_pos)
        table_top = bpy.context.active_object
        table_top.name = f"CoffeeTableTop_{{room_name}}"
        table_top.scale = (3, 1.5, 0.2)
        
        # Table legs
        leg_positions = [
            (table_pos[0] - 2.5, table_pos[1] - 1, table_pos[2] - 0.8),
            (table_pos[0] + 2.5, table_pos[1] - 1, table_pos[2] - 0.8),
            (table_pos[0] - 2.5, table_pos[1] + 1, table_pos[2] - 0.8),
            (table_pos[0] + 2.5, table_pos[1] + 1, table_pos[2] - 0.8)
        ]
        
        for i, leg_pos in enumerate(leg_positions):
            bpy.ops.mesh.primitive_cube_add(location=leg_pos)
            leg = bpy.context.active_object
            leg.name = f"CoffeeTableLeg{{i}}_{{room_name}}"
            leg.scale = (0.2, 0.2, 0.8)
        
        # Table material
        table_mat = create_material(f"CoffeeTableMaterial_{{room_name}}", (0.5, 0.3, 0.2), 0.2)
        table_top.data.materials.append(table_mat)
        
        # TV stand
        tv_pos = (position['x'], position['y'] + length/2 - 1, position['z'] + 1)
        bpy.ops.mesh.primitive_cube_add(location=tv_pos)
        tv_stand = bpy.context.active_object
        tv_stand.name = f"TVStand_{{room_name}}"
        tv_stand.scale = (2, 0.8, 1)
        
        # TV
        tv_screen_pos = (tv_pos[0], tv_pos[1] + 0.9, tv_pos[2] + 1.5)
        bpy.ops.mesh.primitive_cube_add(location=tv_screen_pos)
        tv_screen = bpy.context.active_object
        tv_screen.name = f"TVScreen_{{room_name}}"
        tv_screen.scale = (1.8, 0.1, 1.2)
        
        tv_mat = create_material(f"TVMaterial_{{room_name}}", (0.1, 0.1, 0.1), 0.1)
        tv_stand.data.materials.append(tv_mat)
        tv_screen.data.materials.append(tv_mat)
        
    elif room_type == 'kitchen':
        # Kitchen counter with detailed structure
        counter_pos = (position['x'] - width/3, position['y'] + length/3, position['z'] + 1)
        
        # Counter base
        bpy.ops.mesh.primitive_cube_add(location=counter_pos)
        counter_base = bpy.context.active_object
        counter_base.name = f"CounterBase_{{room_name}}"
        counter_base.scale = (3, 1.5, 1.5)
        
        # Counter top
        top_pos = (counter_pos[0], counter_pos[1], counter_pos[2] + 1.7)
        bpy.ops.mesh.primitive_cube_add(location=top_pos)
        counter_top = bpy.context.active_object
        counter_top.name = f"CounterTop_{{room_name}}"
        counter_top.scale = (3.2, 1.7, 0.2)
        
        # Upper cabinets
        upper_pos = (counter_pos[0], counter_pos[1] + 1.2, counter_pos[2] + 3.5)
        bpy.ops.mesh.primitive_cube_add(location=upper_pos)
        upper_cabinet = bpy.context.active_object
        upper_cabinet.name = f"UpperCabinet_{{room_name}}"
        upper_cabinet.scale = (3, 0.8, 1.5)
        
        # Kitchen materials
        counter_mat = create_material(f"CounterMaterial_{{room_name}}", (0.8, 0.8, 0.8), 0.1)
        cabinet_mat = create_material(f"CabinetMaterial_{{room_name}}", (0.6, 0.4, 0.2), 0.3)
        
        counter_top.data.materials.append(counter_mat)
        counter_base.data.materials.append(cabinet_mat)
        upper_cabinet.data.materials.append(cabinet_mat)
        
        # Refrigerator
        fridge_pos = (position['x'] + width/3, position['y'] + length/3, position['z'] + 1.8)
        bpy.ops.mesh.primitive_cube_add(location=fridge_pos)
        fridge = bpy.context.active_object
        fridge.name = f"Refrigerator_{{room_name}}"
        fridge.scale = (1.2, 1.2, 3.5)
        
        # Fridge door
        door_pos = (fridge_pos[0], fridge_pos[1] - 1.3, fridge_pos[2])
        bpy.ops.mesh.primitive_cube_add(location=door_pos)
        door = bpy.context.active_object
        door.name = f"FridgeDoor_{{room_name}}"
        door.scale = (1.1, 0.1, 3.4)
        
        # Fridge materials
        fridge_mat = create_material(f"FridgeMaterial_{{room_name}}", (0.95, 0.95, 0.95), 0.1, 0.8)
        fridge.data.materials.append(fridge_mat)
        door.data.materials.append(fridge_mat)
        
        # Kitchen island
        island_pos = (position['x'], position['y'] - length/4, position['z'] + 1)
        bpy.ops.mesh.primitive_cube_add(location=island_pos)
        island = bpy.context.active_object
        island.name = f"KitchenIsland_{{room_name}}"
        island.scale = (2, 1, 1)
        
        island_mat = create_material(f"IslandMaterial_{{room_name}}", (0.7, 0.5, 0.3), 0.2)
        island.data.materials.append(island_mat)

# Professional lighting setup
# Main sun light
bpy.ops.object.light_add(type='SUN', location=(20, 20, 30))
sun = bpy.context.active_object
sun.data.energy = 5.0
sun.data.color = (1, 0.95, 0.8)
sun.rotation_euler = (0.8, 0, 0.5)

# Key area light
bpy.ops.object.light_add(type='AREA', location=(10, -10, 20))
area_light = bpy.context.active_object
area_light.data.energy = 200
area_light.data.size = 8
area_light.data.color = (1, 1, 1)

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-10, 10, 15))
fill_light = bpy.context.active_object
fill_light.data.energy = 100
fill_light.data.size = 6
fill_light.data.color = (0.9, 0.9, 1)

# Professional camera setup
building_center_x = building_dims['total_width'] / 2
building_center_y = building_dims['total_length'] / 2

# Hero camera position
bpy.ops.object.camera_add(location=(building_center_x + 25, building_center_y - 20, 15))
camera = bpy.context.active_object
camera.data.lens = 35
camera.data.dof.use_dof = True
camera.data.dof.aperture_fstop = 2.8

# Point camera at building center
direction = mathutils.Vector((building_center_x, building_center_y, 5)) - mathutils.Vector(camera.location)
camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
scene.camera = camera

# Render settings
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# Hero shot
scene.render.filepath = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}_hero.png'
bpy.ops.render.render(write_still=True)

# Detail shot
camera.location = (building_center_x + 15, building_center_y - 10, 10)
direction = mathutils.Vector((building_center_x, building_center_y, 3)) - mathutils.Vector(camera.location)
camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
scene.render.filepath = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}_detail.png'
bpy.ops.render.render(write_still=True)

# Plan view
camera.location = (building_center_x, building_center_y, 40)
camera.rotation_euler = (0, 0, 0)
scene.render.filepath = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}_plan.png'
bpy.ops.render.render(write_still=True)

# Export high-quality OBJ
obj_path = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}.obj'
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True
)

# Save blend file
blend_path = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}.blend'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("PROFESSIONAL BOQ RENDERING COMPLETE")
'''
        
        # Write the script to temp file
        script_path = os.path.join(self.temp_dir, f'boq_script_{self.scene_id}.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        try:
            # Execute Blender with the BOQ script
            result = subprocess.run([
                self.blender_path,
                '--background',
                '--python', script_path
            ], capture_output=True, text=True, timeout=300)
            
            print(f"Blender stdout: {result.stdout}")
            if result.stderr:
                print(f"Blender stderr: {result.stderr}")
            
            # Copy files to backend directory
            backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'generated_models')
            if not os.path.exists(backend_dir):
                os.makedirs(backend_dir)
            
            generated_files = []
            
            # Check for OBJ file
            obj_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.obj')
            if os.path.exists(obj_path):
                dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.obj')
                shutil.copy2(obj_path, dest_path)
                generated_files.append({'type': 'obj', 'path': dest_path})
                
            # Check for MTL file
            mtl_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.mtl')
            if os.path.exists(mtl_path):
                dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.mtl')
                shutil.copy2(mtl_path, dest_path)
                generated_files.append({'type': 'mtl', 'path': dest_path})
                
            # Check for BLEND file
            blend_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.blend')
            if os.path.exists(blend_path):
                dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.blend')
                shutil.copy2(blend_path, dest_path)
                generated_files.append({'type': 'blend', 'path': dest_path})
            
            # Check for rendered images
            for view_type in ['hero', 'detail', 'plan']:
                img_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}_{view_type}.png')
                if os.path.exists(img_path):
                    dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}_{view_type}.png')
                    shutil.copy2(img_path, dest_path)
                    generated_files.append({'type': 'render', 'subtype': view_type, 'path': dest_path})
            
            return {
                'success': True,
                'scene_id': self.scene_id,
                'files': generated_files,
                'output': result.stdout
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'BOQ rendering timeout (5 minutes)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    """Command line interface for API integration"""
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
                if file_type == 'RENDER':
                    print(f"RENDER_PNG: {file_info['path']}")
                else:
                    print(f"{file_type}_FILE: {file_info['path']}")
        else:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
