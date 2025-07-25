import bpy
import bmesh
import json
import sys
import os
import time
from mathutils import Vector
import math

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color, roughness=0.5, metallic=0.0):
    """Create a material with given properties"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # Clear default nodes
    mat.node_tree.nodes.clear()
    
    # Add principled BSDF
    bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    # Add output
    output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_wall(name, start_pos, end_pos, height=3.0, thickness=0.2):
    """Create a wall between two points"""
    # Calculate wall dimensions
    length = (Vector(end_pos) - Vector(start_pos)).length
    center = Vector(start_pos) + (Vector(end_pos) - Vector(start_pos)) / 2
    
    # Create wall mesh
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    wall = bpy.context.active_object
    wall.name = name
    
    # Scale to wall dimensions
    wall.scale = (length, thickness, height)
    
    # Rotate if needed
    direction = Vector(end_pos) - Vector(start_pos)
    if abs(direction.x) > abs(direction.y):
        # Horizontal wall
        pass
    else:
        # Vertical wall
        wall.rotation_euler = (0, 0, math.pi / 2)
    
    return wall

def create_floor(name, room_bounds, height=0.1):
    """Create a floor for a room"""
    min_x, max_x, min_y, max_y = room_bounds
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    depth = max_y - min_y
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, -height/2))
    floor = bpy.context.active_object
    floor.name = name
    floor.scale = (width, depth, height)
    
    return floor

def create_ceiling(name, room_bounds, room_height=3.0, thickness=0.1):
    """Create a ceiling for a room"""
    min_x, max_x, min_y, max_y = room_bounds
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    depth = max_y - min_y
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, room_height + thickness/2))
    ceiling = bpy.context.active_object
    ceiling.name = name
    ceiling.scale = (width, depth, thickness)
    
    return ceiling

def create_door(name, position, width=0.9, height=2.1, thickness=0.05):
    """Create a door"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    door = bpy.context.active_object
    door.name = name
    door.scale = (width, thickness, height)
    
    # Move door to proper height
    door.location.z = height / 2
    
    return door

def create_window(name, position, width=1.2, height=1.0, thickness=0.05):
    """Create a window"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    window = bpy.context.active_object
    window.name = name
    window.scale = (width, thickness, height)
    
    # Move window to proper height
    window.location.z = 1.5  # Window height from floor
    
    return window

def create_simple_furniture(room_type, room_bounds, room_height=3.0):
    """Create simple furniture for different room types"""
    furniture = []
    min_x, max_x, min_y, max_y = room_bounds
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    
    if room_type == "living_room":
        # Sofa
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y - 1, 0.4))
        sofa = bpy.context.active_object
        sofa.name = f"{room_type}_sofa"
        sofa.scale = (2.0, 0.8, 0.8)
        furniture.append(sofa)
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y + 0.5, 0.2))
        table = bpy.context.active_object
        table.name = f"{room_type}_table"
        table.scale = (1.2, 0.6, 0.4)
        furniture.append(table)
        
    elif room_type == "bedroom":
        # Bed
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.3))
        bed = bpy.context.active_object
        bed.name = f"{room_type}_bed"
        bed.scale = (2.0, 1.5, 0.6)
        furniture.append(bed)
        
        # Nightstand
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x + 1.2, center_y, 0.3))
        nightstand = bpy.context.active_object
        nightstand.name = f"{room_type}_nightstand"
        nightstand.scale = (0.5, 0.5, 0.6)
        furniture.append(nightstand)
        
    elif room_type == "kitchen":
        # Counter
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x - 1, center_y, 0.45))
        counter = bpy.context.active_object
        counter.name = f"{room_type}_counter"
        counter.scale = (3.0, 0.6, 0.9)
        furniture.append(counter)
        
        # Island
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x + 0.5, center_y, 0.45))
        island = bpy.context.active_object
        island.name = f"{room_type}_island"
        island.scale = (1.5, 1.0, 0.9)
        furniture.append(island)
        
    elif room_type == "bathroom":
        # Vanity
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x - 0.5, center_y, 0.4))
        vanity = bpy.context.active_object
        vanity.name = f"{room_type}_vanity"
        vanity.scale = (1.2, 0.5, 0.8)
        furniture.append(vanity)
        
        # Toilet
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x + 0.5, center_y, 0.2))
        toilet = bpy.context.active_object
        toilet.name = f"{room_type}_toilet"
        toilet.scale = (0.6, 0.4, 0.4)
        furniture.append(toilet)
    
    return furniture

def create_realistic_house(config):
    """Create a realistic house with proper room geometry"""
    clear_scene()
    
    # Create materials with vibrant colors
    materials = {
        'wall': create_material('Wall', (0.95, 0.95, 0.90), 0.8),  # Light cream walls
        'floor_wood': create_material('Wood_Floor', (0.7, 0.4, 0.2), 0.3),  # Rich brown wood
        'floor_tile': create_material('Tile_Floor', (0.9, 0.9, 0.95), 0.1),  # Light blue-gray tile
        'ceiling': create_material('Ceiling', (0.98, 0.98, 0.98), 0.9),  # White ceiling
        'door': create_material('Door', (0.5, 0.3, 0.1), 0.2),  # Dark brown door
        'window': create_material('Window', (0.6, 0.8, 1.0), 0.0),  # Light blue window
        'sofa': create_material('Sofa', (0.2, 0.4, 0.8), 0.8),  # Blue sofa
        'bed': create_material('Bed', (0.8, 0.2, 0.3), 0.6),  # Red bed
        'table': create_material('Table', (0.4, 0.2, 0.1), 0.2),  # Dark wood table
        'counter': create_material('Counter', (0.8, 0.8, 0.9), 0.1),  # Light gray counter
        'vanity': create_material('Vanity', (0.6, 0.5, 0.4), 0.3),  # Beige vanity
        'toilet': create_material('Toilet', (0.95, 0.95, 0.95), 0.1),  # White toilet
        'nightstand': create_material('Nightstand', (0.5, 0.3, 0.2), 0.3),  # Brown nightstand
        'carpet': create_material('Carpet', (0.7, 0.3, 0.3), 0.9),  # Red carpet
        'island': create_material('Island', (0.4, 0.4, 0.5), 0.1)  # Gray island
    }
    
    all_objects = []
    room_height = 3.0
    
    # Process each room
    current_x = 0
    current_y = 0
    room_spacing = 0.5  # Space between rooms
    
    for i, room in enumerate(config.get('rooms', [])):
        room_name = room.get('name', 'room')
        room_type = room.get('type', 'living_room')
        
        # Extract dimensions directly from room config
        width = room.get('width', 4)
        length = room.get('length', room.get('height', 4))  # 'height' in config is actually length
        room_height = room.get('height', 3)
        
        # Calculate position for this room
        if i == 0:
            x, y = 0, 0
        elif i == 1:
            x, y = current_x + width + room_spacing, 0
        elif i == 2:
            x, y = 0, current_y + length + room_spacing
        else:
            x, y = current_x + width + room_spacing, current_y + length + room_spacing
        
        # Update current position for next room
        current_x = x
        current_y = y
        
        room_bounds = (x, x + width, y, y + length)
        
        # Create room structure
        # Floor
        if room_type == 'bedroom':
            floor_material = 'carpet'
        elif room_type in ['kitchen', 'bathroom']:
            floor_material = 'floor_tile'
        else:
            floor_material = 'floor_wood'
        
        floor = create_floor(f"{room_name}_floor", room_bounds)
        floor.data.materials.append(materials[floor_material])
        all_objects.append(floor)
        
        # Ceiling
        ceiling = create_ceiling(f"{room_name}_ceiling", room_bounds, room_height)
        ceiling.data.materials.append(materials['ceiling'])
        all_objects.append(ceiling)
        
        # Walls
        wall_positions = [
            ((x, y, 0), (x + width, y, 0)),  # Front wall
            ((x + width, y, 0), (x + width, y + length, 0)),  # Right wall
            ((x + width, y + length, 0), (x, y + length, 0)),  # Back wall
            ((x, y + length, 0), (x, y, 0))  # Left wall
        ]
        
        for i, (start, end) in enumerate(wall_positions):
            wall = create_wall(f"{room_name}_wall_{i}", start, end, room_height)
            wall.data.materials.append(materials['wall'])
            all_objects.append(wall)
        
        # Add door (remove from front wall)
        door_pos = (x + width/2, y - 0.1, 0)
        door = create_door(f"{room_name}_door", door_pos)
        door.data.materials.append(materials['door'])
        all_objects.append(door)
        
        # Add window (on right wall)
        window_pos = (x + width + 0.1, y + length/2, 0)
        window = create_window(f"{room_name}_window", window_pos)
        window.data.materials.append(materials['window'])
        all_objects.append(window)
        
        # Add furniture
        furniture = create_simple_furniture(room_type, room_bounds, room_height)
        for item in furniture:
            item_type = item.name.split('_')[-1]
            if item_type in materials:
                item.data.materials.append(materials[item_type])
            all_objects.append(item)
    
    # Set up lighting
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    
    # Add area light for interior
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.5))
    area_light = bpy.context.active_object
    area_light.data.energy = 50.0
    area_light.data.size = 5.0
    
    # Set up camera
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    return all_objects

def main():
    if len(sys.argv) < 2:
        print("Usage: blender --background --python realistic_room_renderer.py -- <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[-1]
    
    # Load configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Create the house
    objects = create_realistic_house(config)
    
    # Generate output paths
    scene_id = f"realistic_house_{int(time.time())}"
    output_dir = os.path.abspath("public/renders")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up file paths
    obj_file = os.path.join(output_dir, f"{scene_id}.obj")
    mtl_file = os.path.join(output_dir, f"{scene_id}.mtl")
    blend_file = os.path.join(output_dir, f"{scene_id}.blend")
    png_file = os.path.join(output_dir, f"{scene_id}.png")
    
    # Export OBJ with materials
    try:
        # Make sure all objects are selected for export
        bpy.ops.object.select_all(action='SELECT')
        
        # Export with enhanced material settings
        bpy.ops.wm.obj_export(
            filepath=obj_file,
            export_materials=True,
            export_material_groups=True,
            export_uv=True,
            export_normals=True,
            export_colors=True,
            export_triangulated_mesh=True,
            export_smooth_groups=True
        )
        print(f"OBJ exported successfully: {obj_file}")
    except AttributeError:
        # Fallback for older Blender versions
        try:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.export_scene.obj(
                filepath=obj_file,
                use_materials=True,
                use_uvs=True,
                use_normals=True,
                use_triangles=True,
                use_smooth_groups=True,
                use_vertex_groups=True
            )
            print(f"OBJ exported successfully (fallback): {obj_file}")
        except Exception as e:
            print(f"Warning: Could not export OBJ file: {e}")
            obj_file = ""
            mtl_file = ""
    
    # Save blend file
    bpy.ops.wm.save_as_mainfile(filepath=blend_file)
    
    # Render preview image
    bpy.context.scene.render.filepath = png_file
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.ops.render.render(write_still=True)
    
    # Output results for API parsing
    print("=== BLENDER RENDERER OUTPUT ===")
    print(f"SCENE_ID: {scene_id}")
    print(f"OBJ_FILE: {obj_file}")
    print(f"MTL_FILE: {mtl_file}")
    print(f"BLEND_FILE: {blend_file}")
    print(f"PNG_FILE: {png_file}")
    print(f"OBJECTS_COUNT: {len(objects)}")
    print("RENDER_COMPLETE: True")
    print("=== END BLENDER RENDERER OUTPUT ===")
    
    # Also print file existence status
    print(f"OBJ file exists: {os.path.exists(obj_file)}")
    print(f"MTL file exists: {os.path.exists(mtl_file)}")
    print(f"BLEND file exists: {os.path.exists(blend_file)}")
    print(f"PNG file exists: {os.path.exists(png_file)}")

if __name__ == "__main__":
    main()
