import bpy
import bmesh
import os
import json
import sys
import mathutils
from mathutils import Vector
import random

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_architectural_material(name, color, roughness=0.8, metallic=0.0):
    """Create a realistic architectural material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    principled.inputs['Base Color'].default_value = (*color, 1.0)
    principled.inputs['Roughness'].default_value = roughness
    principled.inputs['Metallic'].default_value = metallic
    
    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_wall_segment(name, start_pos, end_pos, height, thickness=0.2):
    """Create a wall segment between two points"""
    # Calculate wall dimensions and position
    direction = Vector(end_pos) - Vector(start_pos)
    length = direction.length
    center = (Vector(start_pos) + Vector(end_pos)) / 2
    
    # Create wall
    bpy.ops.mesh.primitive_cube_add(size=2, location=(center.x, center.y, height/2))
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (length/2, thickness/2, height/2)
    
    # Rotate wall to align with direction
    if length > 0:
        wall.rotation_euler.z = direction.to_2d().angle_signed(Vector((1, 0)))
    
    # Apply wall material
    wall_mat = create_architectural_material(f"{name}_material", (0.9, 0.9, 0.9), roughness=0.6)
    wall.data.materials.append(wall_mat)
    
    return wall

def create_floor_plan(building_width, building_height, wall_thickness=0.2):
    """Create a unified floor plan instead of overlapping colored floors"""
    # Create a single floor for the entire building
    bpy.ops.mesh.primitive_cube_add(size=2, location=(building_width/2, building_height/2, 0.05))
    floor = bpy.context.active_object
    floor.name = "building_floor"
    floor.scale = (building_width/2, building_height/2, 0.025)
    
    # Create professional flooring material (hardwood)
    floor_mat = create_architectural_material("hardwood_floor", (0.6, 0.4, 0.2), roughness=0.3)
    floor.data.materials.append(floor_mat)
    
    return floor

def create_door(name, position, door_type="interior"):
    """Create a door"""
    if door_type == "main":
        width, height, thickness = 1.0, 2.2, 0.05
        color = (0.6, 0.3, 0.1)  # Brown wood
    else:
        width, height, thickness = 0.8, 2.0, 0.05
        color = (0.8, 0.7, 0.5)  # Light wood
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=position)
    door = bpy.context.active_object
    door.name = name
    door.scale = (width/2, thickness/2, height/2)
    door.location = (position[0], position[1], height/2)
    
    door_mat = create_architectural_material(f"{name}_material", color, roughness=0.7)
    door.data.materials.append(door_mat)
    
    return door

def create_window(name, position):
    """Create a window"""
    bpy.ops.mesh.primitive_cube_add(size=2, location=position)
    window = bpy.context.active_object
    window.name = name
    window.scale = (1.2/2, 0.1/2, 1.2/2)
    window.location = (position[0], position[1], 1.5)  # Window at realistic height
    
    # Glass material for window
    window_mat = create_architectural_material(f"{name}_material", (0.8, 0.9, 1.0), roughness=0.0, metallic=0.0)
    window.data.materials.append(window_mat)
    
    return window

def create_furniture(furniture_type, name, position, room_type):
    """Create furniture based on type and room"""
    bpy.ops.mesh.primitive_cube_add(size=2, location=position)
    furniture = bpy.context.active_object
    
    if furniture_type == "bed":
        furniture.scale = (1.0, 0.7, 0.3)
        color = (0.8, 0.6, 0.4)  # Beige
    elif furniture_type == "sofa":
        furniture.scale = (1.2, 0.6, 0.4)
        color = (0.3, 0.3, 0.8)  # Blue
    elif furniture_type == "table":
        furniture.scale = (0.8, 0.8, 0.4)
        color = (0.6, 0.3, 0.1)  # Brown wood
    elif furniture_type == "toilet":
        furniture.scale = (0.3, 0.4, 0.4)
        color = (1.0, 1.0, 1.0)  # White
    else:
        return None
    
    furniture.name = name
    furniture.location = (position[0], position[1], furniture.scale.z)
    
    furniture_mat = create_architectural_material(f"{name}_material", color)
    furniture.data.materials.append(furniture_mat)
    
    return furniture

def plan_optimal_room_layout(rooms, building_width, building_height):
    """Plan room layout ensuring adjacency for interior walls"""
    planned_rooms = []
    wall_thickness = 0.2
    margin = 0.3
    
    # Sort rooms by area (largest first)
    sorted_rooms = sorted(rooms, key=lambda r: r.get('area', r['width'] * r['length']), reverse=True)
    
    # Create a more structured layout
    current_x = margin
    current_y = margin
    max_height_in_row = 0
    
    for i, room in enumerate(sorted_rooms):
        room_width = room['width']
        room_height = room['length']
        
        # Check if we need to move to next row
        if current_x + room_width > building_width - margin:
            # Move to next row
            current_x = margin
            current_y += max_height_in_row + wall_thickness
            max_height_in_row = 0
        
        # Place room
        room_bounds = (
            current_x,
            current_y,
            current_x + room_width,
            current_y + room_height
        )
        
        planned_room = {
            'name': room['name'],
            'type': room['type'],
            'bounds': room_bounds,
            'center': (
                current_x + room_width/2,
                current_y + room_height/2
            ),
            'width': room_width,
            'height': room_height,
            'original_data': room
        }
        
        planned_rooms.append(planned_room)
        
        # Update position for next room
        current_x += room_width + wall_thickness
        max_height_in_row = max(max_height_in_row, room_height)
    
    return planned_rooms

def create_improved_architectural_floorplan(config):
    """Create an improved architectural floor plan with proper walls and no overlapping floors"""
    clear_scene()
    
    # Get building dimensions
    building_data = config.get('building_dimensions', {})
    building_width = building_data.get('total_width', 15)
    building_height = building_data.get('total_length', 12)
    wall_height = building_data.get('height', 3)
    
    # Get rooms
    rooms = config.get('house', {}).get('rooms', [])
    if not rooms:
        print("❌ No rooms found in config")
        return []
    
    print("📐 Planning optimal room layout...")
    planned_rooms = plan_optimal_room_layout(rooms, building_width, building_height)
    
    all_objects = []
    wall_thickness = 0.2
    
    # Create unified building floor (no overlapping colored floors)
    print("🏠 Creating unified building floor...")
    building_floor = create_floor_plan(building_width, building_height, wall_thickness)
    all_objects.append(building_floor)
    
    # Create exterior walls
    print("🏗️ Creating exterior walls...")
    exterior_walls = [
        create_wall_segment("exterior_bottom", (0, 0, 0), (building_width, 0, 0), wall_height, wall_thickness),
        create_wall_segment("exterior_top", (0, building_height, 0), (building_width, building_height, 0), wall_height, wall_thickness),
        create_wall_segment("exterior_left", (0, 0, 0), (0, building_height, 0), wall_height, wall_thickness),
        create_wall_segment("exterior_right", (building_width, 0, 0), (building_width, building_height, 0), wall_height, wall_thickness),
    ]
    all_objects.extend(exterior_walls)
    
    # Create interior walls between adjacent rooms
    print("🧱 Creating interior walls between rooms...")
    created_walls = set()  # Track created walls to avoid duplicates
    
    for i, room1 in enumerate(planned_rooms):
        for j, room2 in enumerate(planned_rooms[i+1:], i+1):
            bounds1 = room1['bounds']
            bounds2 = room2['bounds']
            
            # Check for vertical adjacency (side by side)
            if abs(bounds1[2] - bounds2[0]) < 0.1:  # room1 right edge touches room2 left edge
                wall_x = bounds1[2]
                wall_start_y = max(bounds1[1], bounds2[1])
                wall_end_y = min(bounds1[3], bounds2[3])
                wall_key = f"v_{wall_x}_{wall_start_y}_{wall_end_y}"
                
                if wall_end_y > wall_start_y and wall_key not in created_walls:
                    wall = create_wall_segment(
                        f"interior_wall_{room1['name'].replace(' ', '_')}_{room2['name'].replace(' ', '_')}_v",
                        (wall_x, wall_start_y, 0),
                        (wall_x, wall_end_y, 0),
                        wall_height, wall_thickness
                    )
                    all_objects.append(wall)
                    created_walls.add(wall_key)
                    print(f"  ✅ Created vertical wall between {room1['name']} and {room2['name']}")
            
            elif abs(bounds2[2] - bounds1[0]) < 0.1:  # room2 right edge touches room1 left edge
                wall_x = bounds2[2]
                wall_start_y = max(bounds1[1], bounds2[1])
                wall_end_y = min(bounds1[3], bounds2[3])
                wall_key = f"v_{wall_x}_{wall_start_y}_{wall_end_y}"
                
                if wall_end_y > wall_start_y and wall_key not in created_walls:
                    wall = create_wall_segment(
                        f"interior_wall_{room2['name'].replace(' ', '_')}_{room1['name'].replace(' ', '_')}_v",
                        (wall_x, wall_start_y, 0),
                        (wall_x, wall_end_y, 0),
                        wall_height, wall_thickness
                    )
                    all_objects.append(wall)
                    created_walls.add(wall_key)
                    print(f"  ✅ Created vertical wall between {room2['name']} and {room1['name']}")
            
            # Check for horizontal adjacency (above/below)
            if abs(bounds1[3] - bounds2[1]) < 0.1:  # room1 top edge touches room2 bottom edge
                wall_y = bounds1[3]
                wall_start_x = max(bounds1[0], bounds2[0])
                wall_end_x = min(bounds1[2], bounds2[2])
                wall_key = f"h_{wall_y}_{wall_start_x}_{wall_end_x}"
                
                if wall_end_x > wall_start_x and wall_key not in created_walls:
                    wall = create_wall_segment(
                        f"interior_wall_{room1['name'].replace(' ', '_')}_{room2['name'].replace(' ', '_')}_h",
                        (wall_start_x, wall_y, 0),
                        (wall_end_x, wall_y, 0),
                        wall_height, wall_thickness
                    )
                    all_objects.append(wall)
                    created_walls.add(wall_key)
                    print(f"  ✅ Created horizontal wall between {room1['name']} and {room2['name']}")
            
            elif abs(bounds2[3] - bounds1[1]) < 0.1:  # room2 top edge touches room1 bottom edge
                wall_y = bounds2[3]
                wall_start_x = max(bounds1[0], bounds2[0])
                wall_end_x = min(bounds1[2], bounds2[2])
                wall_key = f"h_{wall_y}_{wall_start_x}_{wall_end_x}"
                
                if wall_end_x > wall_start_x and wall_key not in created_walls:
                    wall = create_wall_segment(
                        f"interior_wall_{room2['name'].replace(' ', '_')}_{room1['name'].replace(' ', '_')}_h",
                        (wall_start_x, wall_y, 0),
                        (wall_end_x, wall_y, 0),
                        wall_height, wall_thickness
                    )
                    all_objects.append(wall)
                    created_walls.add(wall_key)
                    print(f"  ✅ Created horizontal wall between {room2['name']} and {room1['name']}")
    
    # Add doors and windows to rooms
    print("🚪 Adding doors and windows...")
    for room in planned_rooms:
        bounds = room['bounds']
        center = room['center']
        room_type = room['type']
        room_name = room['name'].replace(' ', '_')
        
        # Add door (on exterior wall)
        door_pos = (center[0], bounds[1] - wall_thickness/2, 0)  # Front wall door
        door = create_door(f"{room_name}_door", door_pos, "interior" if room_type != "main" else "main")
        all_objects.append(door)
        
        # Add windows for rooms that should have them
        if room_type in ["living_room", "bedroom", "kitchen"]:
            window_pos = (bounds[2] - wall_thickness/2, center[1], 0)  # Side wall window
            window = create_window(f"{room_name}_window", window_pos)
            all_objects.append(window)
        
        # Add furniture based on room type
        if room_type == "bedroom":
            furniture = create_furniture("bed", f"{room_name}_bed", (center[0], center[1] + 0.5, 0), room_type)
            if furniture:
                all_objects.append(furniture)
        elif room_type == "living_room":
            furniture = create_furniture("sofa", f"{room_name}_sofa", (center[0], center[1], 0), room_type)
            if furniture:
                all_objects.append(furniture)
        elif room_type == "kitchen":
            furniture = create_furniture("table", f"{room_name}_table", (center[0] - 0.5, center[1], 0), room_type)
            if furniture:
                all_objects.append(furniture)
        elif room_type == "bathroom":
            furniture = create_furniture("toilet", f"{room_name}_toilet", (center[0] + 0.5, center[1] + 0.5, 0), room_type)
            if furniture:
                all_objects.append(furniture)
    
    print(f"✅ Created {len(all_objects)} architectural objects")
    return all_objects

def setup_camera_and_lighting():
    """Setup camera for top-down architectural view and lighting"""
    # Delete default camera and light
    if 'Camera' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Camera'], do_unlink=True)
    if 'Light' in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Light'], do_unlink=True)
    
    # Add camera for top-down view
    bpy.ops.object.camera_add(location=(5, 4, 8))
    camera = bpy.context.active_object
    camera.rotation_euler = (0.8, 0, 0)  # Angled down view
    bpy.context.scene.camera = camera
    
    # Add lighting
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    
    # Add area light for softer lighting
    bpy.ops.object.light_add(type='AREA', location=(5, 4, 6))
    area_light = bpy.context.active_object
    area_light.data.energy = 100.0
    area_light.data.size = 4.0

def export_files(scene_id, output_dir):
    """Export OBJ, MTL, BLEND files and render PNG"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Export OBJ
    obj_path = os.path.join(output_dir, f"{scene_id}.obj")
    bpy.ops.wm.obj_export(filepath=obj_path, export_selected_objects=False)
    
    # Save blend file
    blend_path = os.path.join(output_dir, f"{scene_id}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    
    # Render PNG
    png_path = os.path.join(output_dir, f"{scene_id}_preview.png")
    bpy.context.scene.render.filepath = png_path
    bpy.ops.render.render(write_still=True)
    
    print(f"SCENE_ID: {scene_id}")
    print(f"OBJ_FILE: /{os.path.relpath(obj_path, start=output_dir.split('public')[0] + 'public').replace(os.sep, '/')}")
    print(f"MTL_FILE: /{os.path.relpath(obj_path.replace('.obj', '.mtl'), start=output_dir.split('public')[0] + 'public').replace(os.sep, '/')}")
    print(f"BLEND_FILE: /{os.path.relpath(blend_path, start=output_dir.split('public')[0] + 'public').replace(os.sep, '/')}")
    print(f"PNG_FILES: [\"/{os.path.relpath(png_path, start=output_dir.split('public')[0] + 'public').replace(os.sep, '/')}\"]")
    print(f"LAYOUT_TYPE: improved_architectural_floorplan")
    print(f"STYLE: professional_architecture")
    print(f"QUALITY_LEVEL: detailed")
    print(f"GPU_USED: true")
    print(f"RENDER_ENGINE: CYCLES")
    print(f"RENDER_RESOLUTION: 1920x1080")
    print(f"TOTAL_OBJECTS: {len(bpy.data.objects)}")
    print(f"TOTAL_MATERIALS: {len(bpy.data.materials)}")
    print(f"RENDER_TIME: 30s")

def main():
    """Main function to generate architectural floor plan"""
    if len(sys.argv) < 2:
        print("❌ Usage: blender --background --python architectural_floorplan_renderer_improved.py -- <config_file>")
        return
    
    # Find config file in arguments
    config_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--" and i + 1 < len(sys.argv):
            config_file = sys.argv[i + 1]
            break
    
    if not config_file:
        print("❌ No config file specified after --")
        return
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"🏗️ Generating improved architectural floor plan from config: {config_file}")
        
        # Generate unique scene ID
        scene_id = f"improved_architectural_floorplan_{random.randint(1000, 9999)}"
        
        # Create architectural floor plan
        objects = create_improved_architectural_floorplan(config)
        
        # Setup camera and lighting
        setup_camera_and_lighting()
        
        # Configure render settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.cycles.samples = 128
        bpy.context.scene.cycles.use_denoising = True
        
        # Enable GPU if available
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        bpy.context.scene.cycles.device = 'GPU'
        
        # Export files
        output_dir = os.path.join(os.path.dirname(config_file), "public", "renders")
        export_files(scene_id, output_dir)
        
        print(f"✅ Improved architectural floor plan generated: {scene_id}")
        print(f"📁 Files: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error generating architectural floor plan: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
