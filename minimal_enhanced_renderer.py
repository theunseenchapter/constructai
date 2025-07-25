#!/usr/bin/env python3
"""
Minimal Enhanced BOQ Renderer - bypass problematic imports
"""
import subprocess
import os
import tempfile
import uuid
import json
import shutil
import math
import random

class MinimalEnhancedRenderer:
    """Minimal enhanced renderer"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_minimal_')
        # Try multiple common Blender paths
        possible_blender_paths = [
            'D:\\blender\\blender.exe',
            'C:\\Program Files\\Blender Foundation\\Blender 4.4\\blender.exe',
            'C:\\Program Files\\Blender Foundation\\Blender 4.3\\blender.exe',
            'C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe',
            'blender'  # System PATH
        ]
        
        self.blender_path = None
        for path in possible_blender_paths:
            if path == 'blender' or os.path.exists(path):
                self.blender_path = path
                break
        
        if not self.blender_path:
            self.blender_path = 'blender'  # fallback
            
        self.scene_id = None
    
    def generate_simple_layout(self, rooms, building_dims):
        """Generate a simple grid layout without advanced layout generator"""
        layout_positions = []
        
        total_width = building_dims.get('total_width', 30)
        total_length = building_dims.get('total_length', 30)
        
        # Simple grid layout
        cols = math.ceil(math.sqrt(len(rooms)))
        rows = math.ceil(len(rooms) / cols)
        
        cell_width = total_width / cols
        cell_length = total_length / rows
        
        for i, room in enumerate(rooms):
            row = i // cols
            col = i % cols
            
            x = col * cell_width + cell_width / 2
            y = row * cell_length + cell_length / 2
            
            # Use room dimensions if available, otherwise fit to cell
            width = min(room.get('width', cell_width * 0.8), cell_width * 0.9)
            length = min(room.get('length', cell_length * 0.8), cell_length * 0.9)
            height = room.get('height', 3)
            
            layout_positions.append({
                'room': room,
                'x': x,
                'y': y,
                'width': width,
                'length': length,
                'height': height,
                'architectural_features': {
                    'style': 'modern',
                    'pattern': 'grid'
                }
            })
        
        return layout_positions
    
    def render_enhanced_boq_scene(self, boq_config):
        """Render an enhanced 3D scene"""
        
        self.scene_id = str(uuid.uuid4())
        
        rooms = boq_config.get('rooms', [])
        building_dims = boq_config.get('building_dimensions', {"total_width": 30, "total_length": 30, "height": 12})
        enhanced_features = boq_config.get('enhanced_features', {})
        architectural_style = boq_config.get('architectural_style', 'modern')
        quality_level = boq_config.get('quality_level', 'professional')
        
        print(f"Creating minimal enhanced BOQ scene: {self.scene_id}")
        print(f"Rooms to generate: {len(rooms)}")
        print(f"Building dimensions: {building_dims}")
        print(f"Enhanced features: {enhanced_features}")
        print(f"Using Blender: {self.blender_path}")
        
        # Generate simple layout
        layout_positions = self.generate_simple_layout(rooms, building_dims)
        
        print(f"Generated simple layout with {len(layout_positions)} rooms")
        
        # Create enhanced Blender script
        layout_json_str = json.dumps(layout_positions).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        enhanced_features_str = json.dumps(enhanced_features).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        
        blender_script = f'''
import bpy
import bmesh
import math

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

scene = bpy.context.scene

# Simple material creation
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    return mat

# Simple materials
materials = {{
    'floor': create_material("Floor", (0.7, 0.7, 0.7)),
    'wall': create_material("Wall", (0.9, 0.9, 0.9)),
    'roof': create_material("Roof", (0.5, 0.3, 0.2))
}}

# Layout data
layout_positions = {layout_json_str}
building_dims = {building_dims}
total_width = {building_dims['total_width']}
total_length = {building_dims['total_length']}
total_height = {building_dims.get('height', 12)}

# Create foundation
bpy.ops.mesh.primitive_plane_add(size=1, location=(total_width/2, total_length/2, 0))
foundation = bpy.context.active_object
foundation.name = "Foundation"
foundation.scale = (total_width/2, total_length/2, 1)
foundation.data.materials.append(materials['floor'])

# Create rooms
room_count = 0
for pos in layout_positions:
    room = pos['room']
    x, y = pos['x'], pos['y']
    width, length, height = pos['width'], pos['length'], pos['height']
    
    # Create room floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 0.1))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room['name']}}"
    floor.scale = (width/2, length/2, 1)
    floor.data.materials.append(materials['floor'])
    
    # Create room walls
    wall_height = height / 2
    wall_thickness = 0.1
    
    # Four walls
    walls = [
        ("North", (x, y + length/2, wall_height), (width/2, wall_thickness/2, wall_height/2)),
        ("South", (x, y - length/2, wall_height), (width/2, wall_thickness/2, wall_height/2)),
        ("East", (x + width/2, y, wall_height), (wall_thickness/2, length/2, wall_height/2)),
        ("West", (x - width/2, y, wall_height), (wall_thickness/2, length/2, wall_height/2))
    ]
    
    for wall_name, location, scale in walls:
        bpy.ops.mesh.primitive_cube_add(location=location)
        wall = bpy.context.active_object
        wall.name = f"{{wall_name}}Wall_{{room['name']}}"
        wall.scale = scale
        wall.data.materials.append(materials['wall'])
    
    room_count += 1

print(f"Created {{room_count}} rooms")

# Export OBJ
bpy.ops.wm.obj_export(
    filepath="{os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.obj').replace(os.sep, '/')}",
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_colors=True
)

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath="{os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.blend').replace(os.sep, '/')}")

print("MINIMAL ENHANCED BOQ RENDERING COMPLETE")
print(f"Scene ID: {self.scene_id}")
print(f"Objects: {{len(bpy.data.objects)}}")
print(f"Materials: {{len(bpy.data.materials)}}")
'''
        
        script_path = os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.py')
        
        try:
            # Write the Blender script
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(blender_script)
            
            print(f"Enhanced Blender script written to: {script_path}")
            
            # Run Blender
            command = [self.blender_path, '--background', '--python', script_path]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            
            if result.stderr:
                print("Blender warnings:", result.stderr)
            
            print("Blender render output:", result.stdout)
            
            if result.returncode != 0:
                raise Exception(f"Blender execution failed with return code {result.returncode}")
            
            # Copy files to backend directory
            backend_dir = os.path.join(os.getcwd(), 'backend', 'generated_models')
            os.makedirs(backend_dir, exist_ok=True)
            
            obj_src = os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.obj')
            mtl_src = os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.mtl')
            blend_src = os.path.join(self.temp_dir, f'enhanced_boq_{self.scene_id}.blend')
            
            copied_files = []
            
            if os.path.exists(obj_src):
                obj_dst = os.path.join(backend_dir, f'enhanced_boq_{self.scene_id}.obj')
                shutil.copy2(obj_src, obj_dst)
                copied_files.append(f"OBJ_FILE: {obj_dst}")
                print(f"OBJ_FILE: {obj_dst}")
            
            if os.path.exists(mtl_src):
                mtl_dst = os.path.join(backend_dir, f'enhanced_boq_{self.scene_id}.mtl')
                shutil.copy2(mtl_src, mtl_dst)
                copied_files.append(f"MTL_FILE: {mtl_dst}")
                print(f"MTL_FILE: {mtl_dst}")
            
            if os.path.exists(blend_src):
                blend_dst = os.path.join(backend_dir, f'enhanced_boq_{self.scene_id}.blend')
                shutil.copy2(blend_src, blend_dst)
                copied_files.append(f"BLEND_FILE: {blend_dst}")
                print(f"BLEND_FILE: {blend_dst}")
            
            print(f"ENHANCED_SCENE_ID: {self.scene_id}")
            print(f"LAYOUT_TYPE: grid")
            print(f"STYLE: {architectural_style}")
            print(f"QUALITY_LEVEL: {quality_level}")
            print(f"ENHANCED_FEATURES: {enhanced_features}")
            
            return {
                'scene_id': self.scene_id,
                'files_copied': len(copied_files)
            }
            
        except subprocess.TimeoutExpired:
            raise Exception("Blender execution timed out")
        except Exception as e:
            print(f"Error in render_enhanced_boq_scene: {e}")
            raise
        finally:
            # Clean up temp directory
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python minimal_enhanced_renderer.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        sys.exit(1)
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        renderer = MinimalEnhancedRenderer()
        result = renderer.render_enhanced_boq_scene(config)
        
        print(f"Minimal renderer completed: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
