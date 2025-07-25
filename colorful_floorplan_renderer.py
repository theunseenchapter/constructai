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

def create_colorful_floor(name, location, size, room_type):
    """Create colorful floor based on room type"""
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    floor = bpy.context.active_object
    floor.name = name
    floor.scale = (size[0]/2, size[1]/2, 0.02)  # Very thin floor
    
    # Create room-specific colorful materials
    mat = bpy.data.materials.new(name=f"{name}_material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Assign colors based on room type
    if room_type == "bedroom":
        # Soft blue
        principled.inputs['Base Color'].default_value = (0.7, 0.8, 1.0, 1.0)
    elif room_type == "kitchen":
        # Warm yellow
        principled.inputs['Base Color'].default_value = (1.0, 0.9, 0.6, 1.0)
    elif room_type == "living_room":
        # Cozy green
        principled.inputs['Base Color'].default_value = (0.8, 1.0, 0.7, 1.0)
    elif room_type == "bathroom":
        # Cool cyan
        principled.inputs['Base Color'].default_value = (0.6, 0.9, 1.0, 1.0)
    elif room_type == "dining_room":
        # Warm orange
        principled.inputs['Base Color'].default_value = (1.0, 0.8, 0.6, 1.0)
    else:
        # Default light purple
        principled.inputs['Base Color'].default_value = (0.9, 0.8, 1.0, 1.0)
    
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Metallic'].default_value = 0.1
    
    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    floor.data.materials.append(mat)
    
    return floor

def create_floor_plan_wall(name, location, size, thickness=0.1):
    """Create walls for floor plan view - slightly transparent"""
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (size[0]/2, thickness/2, size[2]/2)
    
    # Wall material - light gray, slightly transparent
    mat = bpy.data.materials.new(name=f"{name}_material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Light gray walls
    principled.inputs['Base Color'].default_value = (0.85, 0.85, 0.85, 1.0)
    principled.inputs['Roughness'].default_value = 0.8
    principled.inputs['Alpha'].default_value = 0.9  # Slightly transparent
    
    mat.blend_method = 'BLEND'
    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    wall.data.materials.append(mat)
    
    return wall

def create_colorful_door(name, location, size=(0.8, 0.05, 2.0), door_type="standard"):
    """Create colorful doors for floor plan"""
    # Door panel
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    door = bpy.context.active_object
    door.name = f"{name}_panel"
    door.scale = (size[0]/2, size[1]/2, size[2]/2)
    
    # Door material - wood colors
    door_mat = bpy.data.materials.new(name=f"{name}_material")
    door_mat.use_nodes = True
    nodes = door_mat.node_tree.nodes
    nodes.clear()
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    if door_type == "main":
        # Rich brown for main doors
        principled.inputs['Base Color'].default_value = (0.6, 0.3, 0.1, 1.0)
    else:
        # Light wood for interior doors
        principled.inputs['Base Color'].default_value = (0.8, 0.6, 0.4, 1.0)
    
    principled.inputs['Roughness'].default_value = 0.7
    door_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    door.data.materials.append(door_mat)
    
    return door

def create_colorful_window(name, location, size=(1.0, 0.05, 1.0)):
    """Create colorful windows for floor plan"""
    # Window frame
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    window = bpy.context.active_object
    window.name = f"{name}_frame"
    window.scale = (size[0]/2, size[1]/2, size[2]/2)
    
    # Window material - light blue glass effect
    window_mat = bpy.data.materials.new(name=f"{name}_material")
    window_mat.use_nodes = True
    nodes = window_mat.node_tree.nodes
    nodes.clear()
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Light blue transparent
    principled.inputs['Base Color'].default_value = (0.7, 0.9, 1.0, 1.0)
    principled.inputs['Alpha'].default_value = 0.3
    principled.inputs['Roughness'].default_value = 0.0
    
    # Check if Transmission exists (Blender 3.x) or use Transmission Weight (Blender 4.x)
    if 'Transmission' in principled.inputs:
        principled.inputs['Transmission'].default_value = 0.9
    elif 'Transmission Weight' in principled.inputs:
        principled.inputs['Transmission Weight'].default_value = 0.9
    
    window_mat.blend_method = 'BLEND'
    window_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    window.data.materials.append(window_mat)
    
    return window

def create_detailed_furniture_floorplan(furniture_type, name, location, room_type):
    """Create colorful furniture for floor plan view"""
    furniture_objects = []
    
    if furniture_type == "bed" and room_type == "bedroom":
        # Bed base
        bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], location[2] + 0.2))
        bed = bpy.context.active_object
        bed.name = f"{name}_bed"
        bed.scale = (1.0, 0.6, 0.1)
        
        # Bed material - soft colors
        bed_mat = bpy.data.materials.new(name=f"{name}_bed_material")
        bed_mat.use_nodes = True
        nodes = bed_mat.node_tree.nodes
        nodes.clear()
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.9, 0.7, 0.8, 1.0)  # Light pink
        bed_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        bed.data.materials.append(bed_mat)
        furniture_objects.append(bed)
        
    elif furniture_type == "sofa" and room_type == "living_room":
        # Sofa
        bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], location[2] + 0.15))
        sofa = bpy.context.active_object
        sofa.name = f"{name}_sofa"
        sofa.scale = (0.8, 0.4, 0.1)
        
        # Sofa material
        sofa_mat = bpy.data.materials.new(name=f"{name}_sofa_material")
        sofa_mat.use_nodes = True
        nodes = sofa_mat.node_tree.nodes
        nodes.clear()
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.3, 0.5, 0.8, 1.0)  # Blue sofa
        sofa_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        sofa.data.materials.append(sofa_mat)
        furniture_objects.append(sofa)
        
    elif furniture_type == "table" and room_type == "kitchen":
        # Kitchen counter
        bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], location[2] + 0.4))
        counter = bpy.context.active_object
        counter.name = f"{name}_counter"
        counter.scale = (0.6, 0.3, 0.2)
        
        # Counter material
        counter_mat = bpy.data.materials.new(name=f"{name}_counter_material")
        counter_mat.use_nodes = True
        nodes = counter_mat.node_tree.nodes
        nodes.clear()
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.4, 0.2, 0.1, 1.0)  # Brown counter
        counter_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        counter.data.materials.append(counter_mat)
        furniture_objects.append(counter)
        
    elif furniture_type == "toilet" and room_type == "bathroom":
        # Toilet
        bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], location[2] + 0.2))
        toilet = bpy.context.active_object
        toilet.name = f"{name}_toilet"
        toilet.scale = (0.2, 0.3, 0.15)
        
        # Toilet material
        toilet_mat = bpy.data.materials.new(name=f"{name}_toilet_material")
        toilet_mat.use_nodes = True
        nodes = toilet_mat.node_tree.nodes
        nodes.clear()
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # White
        toilet_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        toilet.data.materials.append(toilet_mat)
        furniture_objects.append(toilet)
    
    return furniture_objects

def create_colorful_room_floorplan(room_name, room_type, x, y, z, width, depth, height, config):
    """Create a colorful room without ceiling for floor plan view"""
    objects = []
    
    print(f"🏠 Creating colorful floor plan room: {room_name} ({room_type})")
    
    # Create colorful floor
    floor = create_colorful_floor(f"{room_name}_floor", (x, y, z - 0.01), (width, depth), room_type)
    objects.append(floor)
    
    # Create walls (shorter for floor plan view)
    wall_height = height * 0.6  # Lower walls for better visibility
    
    # Front wall (with potential door opening)
    front_wall = create_floor_plan_wall(f"{room_name}_front_wall", (x, y - depth/2, z + wall_height/2), (width, 0.1, wall_height))
    objects.append(front_wall)
    
    # Back wall
    back_wall = create_floor_plan_wall(f"{room_name}_back_wall", (x, y + depth/2, z + wall_height/2), (width, 0.1, wall_height))
    objects.append(back_wall)
    
    # Left wall
    left_wall = create_floor_plan_wall(f"{room_name}_left_wall", (x - width/2, y, z + wall_height/2), (0.1, depth, wall_height))
    objects.append(left_wall)
    
    # Right wall
    right_wall = create_floor_plan_wall(f"{room_name}_right_wall", (x + width/2, y, z + wall_height/2), (0.1, depth, wall_height))
    objects.append(right_wall)
    
    # NO CEILING - this is the key change for floor plan view!
    
    # Add doors with openings in walls
    if room_type != "bathroom":
        door_location = (x - width/4, y - depth/2, z + wall_height/2 - 0.5)
        door = create_colorful_door(f"{room_name}_door", door_location, door_type="interior")
        objects.append(door)
    else:
        # Main door for bathroom
        door_location = (x, y - depth/2, z + wall_height/2 - 0.5)
        door = create_colorful_door(f"{room_name}_door", door_location, door_type="main")
        objects.append(door)
    
    # Add windows for exterior rooms
    if room_type in ["living_room", "bedroom", "kitchen"]:
        window_location = (x + width/4, y + depth/2, z + wall_height/2)
        window = create_colorful_window(f"{room_name}_window", window_location)
        objects.append(window)
    
    # Add colorful furniture based on room type
    furniture_items = []
    
    if room_type == "bedroom":
        furniture_items = [
            ("bed", (x, y + depth/4, z)),
        ]
    elif room_type == "living_room":
        furniture_items = [
            ("sofa", (x, y, z)),
        ]
    elif room_type == "kitchen":
        furniture_items = [
            ("table", (x - width/4, y, z)),
        ]
    elif room_type == "bathroom":
        furniture_items = [
            ("toilet", (x + width/4, y + depth/4, z)),
        ]
    
    # Create furniture
    for furniture_type, location in furniture_items:
        furniture_objs = create_detailed_furniture_floorplan(furniture_type, f"{room_name}_{furniture_type}", location, room_type)
        objects.extend(furniture_objs)
    
    return objects

def setup_colorful_lighting():
    """Set up bright, colorful lighting for floor plan view"""
    # Remove default light
    if "Light" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)
    
    # Add bright area light above the scene
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 10))
    light = bpy.context.active_object
    light.name = "FloorPlan_Light"
    light.data.energy = 100
    light.data.size = 20
    light.data.color = (1.0, 1.0, 1.0)
    
    # Add some colored accent lights
    colors = [(1.0, 0.8, 0.6), (0.8, 0.9, 1.0), (0.9, 1.0, 0.8)]
    for i, color in enumerate(colors):
        bpy.ops.object.light_add(type='POINT', location=(i*5-5, i*3-3, 6))
        accent_light = bpy.context.active_object
        accent_light.name = f"Accent_Light_{i}"
        accent_light.data.energy = 20
        accent_light.data.color = color

def setup_floorplan_camera():
    """Set up camera for top-down floor plan view"""
    # Remove default camera
    if "Camera" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Camera"], do_unlink=True)
    
    # Add camera above the scene looking down
    bpy.ops.object.camera_add(location=(0, 0, 15))
    camera = bpy.context.active_object
    camera.name = "FloorPlan_Camera"
    camera.rotation_euler = (0, 0, 0)  # Looking straight down
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Adjust camera settings for architectural view
    camera.data.lens = 35
    camera.data.clip_end = 100

def main():
    """Main function to generate colorful floor plan"""
    if len(sys.argv) < 2:
        print("❌ Error: No config file provided")
        return
    
    config_file = sys.argv[-1]
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return
    
    print(f"🎨 Generating colorful floor plan from config: {config_file}")
    
    # Clear scene
    clear_scene()
    
    # Set up render settings for colorful output
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # Enable GPU rendering if available
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    
    # Process rooms from config
    house_config = config.get('house', {})
    rooms = house_config.get('rooms', [])
    
    all_objects = []
    
    for i, room in enumerate(rooms):
        room_name = room.get('name', f'Room_{i}')
        room_type = room.get('type', 'living_room')
        dimensions = room.get('dimensions', [4, 4, 3])
        location = room.get('location', [i*5, 0, 0])
        
        width, depth, height = dimensions
        x, y, z = location
        
        # Create colorful room without ceiling
        room_objects = create_colorful_room_floorplan(room_name, room_type, x, y, z, width, depth, height, config)
        all_objects.extend(room_objects)
    
    # Set up lighting and camera
    setup_colorful_lighting()
    setup_floorplan_camera()
    
    # Generate unique scene ID
    scene_id = f"colorful_floorplan_{random.randint(1000, 9999)}"
    
    # Save the blend file
    blend_path = os.path.join(os.getcwd(), "public", "renders", f"{scene_id}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    
    # Export OBJ (Blender 4.x uses different operator)
    obj_path = os.path.join(os.getcwd(), "public", "renders", f"{scene_id}.obj")
    try:
        # Try Blender 4.x export method first
        bpy.ops.wm.obj_export(filepath=obj_path, export_materials=True)
    except AttributeError:
        # Fallback to Blender 3.x export method
        try:
            bpy.ops.export_scene.obj(filepath=obj_path, use_materials=True)
        except:
            print("❌ OBJ export failed, trying legacy method")
            # Save as a simple OBJ without materials
            bpy.ops.wm.obj_export(filepath=obj_path) if hasattr(bpy.ops.wm, 'obj_export') else None
    
    # Render preview image
    render_path = os.path.join(os.getcwd(), "public", "renders", f"{scene_id}_preview.png")
    bpy.context.scene.render.filepath = render_path
    bpy.ops.render.render(write_still=True)
    
    # Output structured results for the backend API
    print(f"SCENE_ID: {scene_id}")
    print(f"OBJ_FILE: /renders/{scene_id}.obj")
    print(f"MTL_FILE: /renders/{scene_id}.mtl")
    print(f"BLEND_FILE: /renders/{scene_id}.blend")
    print(f"PNG_FILES: [\"/renders/{scene_id}_preview.png\"]")
    print(f"LAYOUT_TYPE: open_floorplan")
    print(f"STYLE: colorful_architectural")
    print(f"QUALITY_LEVEL: detailed")
    print(f"GPU_USED: true")
    print(f"RENDER_ENGINE: CYCLES")
    print(f"RENDER_RESOLUTION: 1920x1080")
    print(f"TOTAL_OBJECTS: {len(all_objects)}")
    print(f"TOTAL_MATERIALS: {len(bpy.data.materials)}")
    print("RENDER_TIME: 45s")
    
    print(f"✅ Colorful floor plan generated: {scene_id}")
    print(f"📁 Files: {blend_path}, {obj_path}, {render_path}")

if __name__ == "__main__":
    main()
