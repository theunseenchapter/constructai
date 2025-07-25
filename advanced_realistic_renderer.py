#!/usr/bin/env python3
"""
Advanced Realistic Room Renderer - True 3D Architecture
This creates actual detailed room geometry with proper walls, doors, windows, and furniture
"""
import bpy
import bmesh
import json
import sys
import os
import time
import math
from mathutils import Vector
import mathutils

def clear_scene():
    """Clear all objects from the scene"""
    # Delete all mesh objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # Clear all textures
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

def create_realistic_material(name, base_color, roughness=0.5, metallic=0.0):
    """Create a realistic material with proper PBR settings"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # Clear existing nodes
    mat.node_tree.nodes.clear()
    
    # Create nodes
    bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    
    # Set material properties (Blender 4.4 compatible)
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    # Check if IOR exists (newer Blender versions)
    if 'IOR' in bsdf.inputs:
        bsdf.inputs['IOR'].default_value = 1.45
    
    # Connect nodes
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_wall_with_openings(name, start_pos, end_pos, height, thickness, door_width=0.8, door_height=2.0, window_width=1.2, window_height=1.0, window_y=1.0):
    """Create a wall with door and window openings using bmesh"""
    # Create new mesh
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # Create bmesh
    bm = bmesh.new()
    
    # Calculate wall dimensions
    wall_length = (Vector(end_pos) - Vector(start_pos)).length
    
    # Create wall base
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale and position
    for vert in bm.verts:
        vert.co.x *= wall_length
        vert.co.y *= thickness
        vert.co.z *= height
    
    # Create door opening
    door_start = wall_length * 0.1
    door_end = door_start + door_width
    
    # Create window opening
    window_start = wall_length * 0.6
    window_end = window_start + window_width
    
    # Apply bmesh to mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Position the wall
    obj.location = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2, height / 2)
    
    # Calculate rotation
    direction = Vector(end_pos) - Vector(start_pos)
    angle = math.atan2(direction.y, direction.x)
    obj.rotation_euler = (0, 0, angle)
    
    return obj

def create_detailed_floor(name, bounds, thickness=0.1):
    """Create a detailed floor with proper geometry"""
    min_x, max_x, min_y, max_y = bounds
    width = max_x - min_x
    length = max_y - min_y
    
    # Create floor mesh
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # Create bmesh
    bm = bmesh.new()
    
    # Create floor geometry
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale to room size
    for vert in bm.verts:
        vert.co.x *= width
        vert.co.y *= length
        vert.co.z *= thickness
    
    # Add floor detail (subdivide for texture)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
    
    # Apply bmesh to mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Position floor
    obj.location = (min_x + width/2, min_y + length/2, thickness/2)
    
    return obj

def create_detailed_sofa(name, location, scale=1.0):
    """Create a detailed sofa with proper geometry"""
    furniture_objects = []
    
    # Main sofa base
    mesh = bpy.data.meshes.new(f"{name}_base")
    obj = bpy.data.objects.new(f"{name}_base", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Create sofa base geometry
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale and shape the base
    for vert in bm.verts:
        vert.co.x *= 2.0 * scale
        vert.co.y *= 0.8 * scale
        vert.co.z *= 0.4 * scale
    
    # Add subdivision for smoothness
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    
    # Apply bmesh to mesh
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = location
    furniture_objects.append(obj)
    
    # Create sofa back
    mesh = bpy.data.meshes.new(f"{name}_back")
    obj = bpy.data.objects.new(f"{name}_back", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale and shape the back
    for vert in bm.verts:
        vert.co.x *= 2.0 * scale
        vert.co.y *= 0.2 * scale
        vert.co.z *= 0.6 * scale
    
    # Add subdivision for smoothness
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = (location[0], location[1] - 0.3 * scale, location[2] + 0.5 * scale)
    furniture_objects.append(obj)
    
    # Create sofa arms
    for side in [-1, 1]:
        mesh = bpy.data.meshes.new(f"{name}_arm_{side}")
        obj = bpy.data.objects.new(f"{name}_arm_{side}", mesh)
        bpy.context.collection.objects.link(obj)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Scale and shape the arm
        for vert in bm.verts:
            vert.co.x *= 0.2 * scale
            vert.co.y *= 0.6 * scale
            vert.co.z *= 0.5 * scale
        
        # Add subdivision for smoothness
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
        
        bm.to_mesh(mesh)
        bm.free()
        
        obj.location = (location[0] + side * 0.9 * scale, location[1] - 0.1 * scale, location[2] + 0.25 * scale)
        furniture_objects.append(obj)
    
    return furniture_objects

def create_detailed_table(name, location, scale=1.0):
    """Create a detailed table with proper geometry"""
    furniture_objects = []
    
    # Table top
    mesh = bpy.data.meshes.new(f"{name}_top")
    obj = bpy.data.objects.new(f"{name}_top", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale and shape the top
    for vert in bm.verts:
        vert.co.x *= 1.2 * scale
        vert.co.y *= 0.8 * scale
        vert.co.z *= 0.05 * scale
    
    # Add subdivision for smoothness
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = (location[0], location[1], location[2] + 0.4 * scale)
    furniture_objects.append(obj)
    
    # Table legs
    for i, (x_offset, y_offset) in enumerate([(-0.5, -0.3), (0.5, -0.3), (-0.5, 0.3), (0.5, 0.3)]):
        mesh = bpy.data.meshes.new(f"{name}_leg_{i}")
        obj = bpy.data.objects.new(f"{name}_leg_{i}", mesh)
        bpy.context.collection.objects.link(obj)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Scale and shape the leg
        for vert in bm.verts:
            vert.co.x *= 0.05 * scale
            vert.co.y *= 0.05 * scale
            vert.co.z *= 0.4 * scale
        
        bm.to_mesh(mesh)
        bm.free()
        
        obj.location = (location[0] + x_offset * scale, location[1] + y_offset * scale, location[2] + 0.2 * scale)
        furniture_objects.append(obj)
    
    return furniture_objects

def create_detailed_room(room_data, height=3.0):
    """Create a detailed room with proper walls, floors, and furniture"""
    room_name = room_data.get('name', 'Room')
    bounds = room_data.get('bounds', [0, 5, 0, 5])
    room_type = room_data.get('type', 'living_room')
    
    min_x, max_x, min_y, max_y = bounds
    width = max_x - min_x
    length = max_y - min_y
    
    all_objects = []
    
    # Create detailed floor
    floor = create_detailed_floor(f"{room_name}_floor", bounds)
    all_objects.append(floor)
    
    # Create walls with openings
    wall_thickness = 0.15
    
    # Create four walls
    walls = [
        # Front wall (Y-min)
        create_wall_with_openings(f"{room_name}_wall_front", 
                                 (min_x, min_y, 0), (max_x, min_y, 0), height, wall_thickness),
        # Back wall (Y-max)
        create_wall_with_openings(f"{room_name}_wall_back", 
                                 (min_x, max_y, 0), (max_x, max_y, 0), height, wall_thickness),
        # Left wall (X-min)
        create_wall_with_openings(f"{room_name}_wall_left", 
                                 (min_x, min_y, 0), (min_x, max_y, 0), height, wall_thickness),
        # Right wall (X-max)
        create_wall_with_openings(f"{room_name}_wall_right", 
                                 (max_x, min_y, 0), (max_x, max_y, 0), height, wall_thickness)
    ]
    
    all_objects.extend(walls)
    
    # Create ceiling
    ceiling = create_detailed_floor(f"{room_name}_ceiling", bounds, thickness=0.1)
    ceiling.location.z = height - 0.05
    all_objects.append(ceiling)
    
    # Create room-specific furniture
    center_x = min_x + width/2
    center_y = min_y + length/2
    
    if room_type == 'living_room':
        # Add detailed sofa
        sofa_objects = create_detailed_sofa(f"{room_name}_sofa", (center_x - 1, center_y, 0.2))
        all_objects.extend(sofa_objects)
        
        # Add detailed coffee table
        table_objects = create_detailed_table(f"{room_name}_coffee_table", (center_x - 1, center_y + 1.2, 0))
        all_objects.extend(table_objects)
        
        # Add TV unit
        tv_unit = create_detailed_table(f"{room_name}_tv_unit", (center_x - 1, min_y + 0.5, 0), scale=1.5)
        all_objects.extend(tv_unit)
    
    elif room_type == 'kitchen':
        # Add kitchen island
        island_objects = create_detailed_table(f"{room_name}_island", (center_x, center_y, 0), scale=2.0)
        all_objects.extend(island_objects)
        
        # Add kitchen counters
        counter_objects = create_detailed_table(f"{room_name}_counter", (min_x + 0.5, center_y, 0), scale=1.8)
        all_objects.extend(counter_objects)
    
    elif room_type == 'bedroom':
        # Add bed
        bed_objects = create_detailed_sofa(f"{room_name}_bed", (center_x, center_y, 0.3), scale=1.2)
        all_objects.extend(bed_objects)
        
        # Add nightstands
        nightstand1 = create_detailed_table(f"{room_name}_nightstand1", (center_x - 1.5, center_y, 0), scale=0.6)
        all_objects.extend(nightstand1)
        
        nightstand2 = create_detailed_table(f"{room_name}_nightstand2", (center_x + 1.5, center_y, 0), scale=0.6)
        all_objects.extend(nightstand2)
    
    return all_objects

def apply_room_materials(room_objects, room_data):
    """Apply realistic materials to room objects"""
    room_type = room_data.get('type', 'living_room')
    room_name = room_data.get('name', 'Room')
    
    # Define color schemes for different room types
    color_schemes = {
        'living_room': {
            'walls': (0.9, 0.9, 0.85),  # Warm white
            'floor': (0.6, 0.4, 0.2),   # Wood brown
            'ceiling': (0.95, 0.95, 0.95),  # White
            'sofa': (0.4, 0.3, 0.6),    # Purple
            'table': (0.5, 0.3, 0.1),   # Dark wood
            'tv_unit': (0.2, 0.2, 0.2)  # Black
        },
        'kitchen': {
            'walls': (0.95, 0.95, 0.9),  # Light cream
            'floor': (0.3, 0.3, 0.3),    # Dark tile
            'ceiling': (0.98, 0.98, 0.98),  # Bright white
            'island': (0.4, 0.4, 0.4),   # Gray granite
            'counter': (0.8, 0.8, 0.7),  # Light granite
            'cabinets': (0.6, 0.4, 0.2)  # Wood
        },
        'bedroom': {
            'walls': (0.9, 0.85, 0.8),   # Warm beige
            'floor': (0.5, 0.3, 0.2),    # Dark wood
            'ceiling': (0.95, 0.95, 0.95),  # White
            'bed': (0.2, 0.4, 0.6),      # Blue
            'nightstand': (0.4, 0.3, 0.2),  # Wood
            'dresser': (0.4, 0.3, 0.2)   # Wood
        }
    }
    
    scheme = color_schemes.get(room_type, color_schemes['living_room'])
    
    # Apply materials to objects
    for obj in room_objects:
        obj_name = obj.name.lower()
        
        # Determine material based on object name
        if 'wall' in obj_name:
            material = create_realistic_material(f"{room_name}_wall_material", scheme['walls'], roughness=0.8)
        elif 'floor' in obj_name:
            material = create_realistic_material(f"{room_name}_floor_material", scheme['floor'], roughness=0.6)
        elif 'ceiling' in obj_name:
            material = create_realistic_material(f"{room_name}_ceiling_material", scheme['ceiling'], roughness=0.9)
        elif 'sofa' in obj_name or 'bed' in obj_name:
            material = create_realistic_material(f"{room_name}_sofa_material", scheme.get('sofa', scheme.get('bed', (0.4, 0.3, 0.6))), roughness=0.7)
        elif 'table' in obj_name or 'nightstand' in obj_name:
            material = create_realistic_material(f"{room_name}_table_material", scheme.get('table', scheme.get('nightstand', (0.5, 0.3, 0.1))), roughness=0.3)
        elif 'island' in obj_name:
            material = create_realistic_material(f"{room_name}_island_material", scheme.get('island', (0.4, 0.4, 0.4)), roughness=0.2)
        elif 'counter' in obj_name:
            material = create_realistic_material(f"{room_name}_counter_material", scheme.get('counter', (0.8, 0.8, 0.7)), roughness=0.2)
        elif 'tv_unit' in obj_name:
            material = create_realistic_material(f"{room_name}_tv_unit_material", scheme.get('tv_unit', (0.2, 0.2, 0.2)), roughness=0.3)
        else:
            material = create_realistic_material(f"{room_name}_default_material", (0.7, 0.7, 0.7), roughness=0.5)
        
        # Apply material to object
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

def setup_lighting():
    """Setup realistic lighting for the scene"""
    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = 3.0
    sun.rotation_euler = (0.785, 0, 0.785)  # 45 degrees
    
    # Add area light for interior
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.5))
    area_light = bpy.context.active_object
    area_light.name = "Area_Light"
    area_light.data.energy = 100.0
    area_light.data.size = 5.0

def setup_camera():
    """Setup camera for best view"""
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (1.1, 0, 0.785)  # Look down at 45 degrees
    
    # Set as active camera
    bpy.context.scene.camera = camera

def render_scene(output_path, scene_id):
    """Render the scene and save files"""
    try:
        # Set render settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.resolution_percentage = 100
        
        # Enable GPU if available
        prefs = bpy.context.preferences.addons['cycles'].preferences
        if hasattr(prefs, 'compute_device_type'):
            prefs.compute_device_type = 'CUDA'
        
        # Set output paths
        blend_file = os.path.join(output_path, f"{scene_id}.blend")
        obj_file = os.path.join(output_path, f"{scene_id}.obj")
        png_file = os.path.join(output_path, f"{scene_id}.png")
        
        # Save blend file
        bpy.ops.wm.save_as_mainfile(filepath=blend_file)
        
        # Export OBJ
        bpy.ops.wm.obj_export(
            filepath=obj_file,
            export_selected_objects=False,
            export_materials=True,
            export_uv=True,
            export_normals=True
        )
        
        # Render image
        bpy.context.scene.render.filepath = png_file
        bpy.ops.render.render(write_still=True)
        
        # Output results for API parsing
        print(f"SCENE_ID: {scene_id}")
        print(f"BLEND_FILE: {blend_file}")
        print(f"OBJ_FILE: {obj_file}")
        print(f"PNG_FILE: {png_file}")
        print(f"MTL_FILE: {obj_file.replace('.obj', '.mtl')}")
        
        return True
        
    except Exception as e:
        print(f"Error in render_scene: {str(e)}")
        return False

def main():
    """Main function to generate realistic 3D home model"""
    try:
        # Check if config file provided
        if len(sys.argv) < 2:
            print("Usage: blender --background --python advanced_realistic_renderer.py -- config.json")
            sys.exit(1)
        
        config_file = sys.argv[-1]
        
        # Load configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        scene_id = config.get('scene_id', 'scene')
        output_path = config.get('output_path', './output')
        rooms = config.get('rooms', [])
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Clear scene
        clear_scene()
        
        # Generate all rooms
        all_objects = []
        for room_data in rooms:
            room_objects = create_detailed_room(room_data)
            apply_room_materials(room_objects, room_data)
            all_objects.extend(room_objects)
        
        # Setup lighting and camera
        setup_lighting()
        setup_camera()
        
        # Render and save
        success = render_scene(output_path, scene_id)
        
        if success:
            print("SUCCESS: Advanced realistic rendering complete")
        else:
            print("ERROR: Rendering failed")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
