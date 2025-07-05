#!/usr/bin/env python3
"""
Blender MCP Server for ConstructAI
Provides 3D architectural visualization using Blender's Python API
"""

import asyncio
import json
import sys
import os
import tempfile
import subprocess
import base64
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types

# Add Blender's Python modules to path if available
BLENDER_PATH = os.environ.get('BLENDER_PATH', 'blender')

server = Server("blender-3d-server")

class BlenderRenderer:
    """Handles Blender operations for 3D room visualization"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='constructai_blender_')
        self.scene_file = None
        
    def create_room_scene(self, rooms_data: List[Dict], building_dimensions: Dict) -> str:
        """Create a Blender scene with rooms and furniture"""
        
        # Blender Python script for scene creation
        blender_script = f'''
import bpy
import bmesh
from mathutils import Vector
import json
import os

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Room data
rooms_data = {json.dumps(rooms_data)}
building_dimensions = {json.dumps(building_dimensions)}

# Materials setup
def create_pbr_material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.node_tree.clear()
    
    # Add principled BSDF
    bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Set material properties
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    return mat

# Create materials
materials = {{
    'drywall': create_pbr_material('Drywall', (0.96, 0.96, 0.96), 0.8, 0.0),
    'hardwood': create_pbr_material('Hardwood', (0.55, 0.27, 0.07), 0.2, 0.0),
    'tile': create_pbr_material('Tile', (1.0, 1.0, 1.0), 0.1, 0.0),
    'ceiling': create_pbr_material('Ceiling', (1.0, 1.0, 1.0), 0.6, 0.0),
    'wood': create_pbr_material('Wood', (0.55, 0.27, 0.07), 0.3, 0.0),
    'fabric': create_pbr_material('Fabric', (0.25, 0.41, 0.88), 0.8, 0.0),
    'metal': create_pbr_material('Metal', (0.53, 0.53, 0.53), 0.2, 0.8),
}}

def create_room_geometry(room):
    """Create room walls, floor, and ceiling"""
    room_objects = []
    
    # Floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(room['position']['x'], room['position']['z'], room['position']['y']))
    floor = bpy.context.active_object
    floor.name = f"Floor_{{room['name']}}"
    floor.scale = (room['width'], room['length'], 1)
    floor.data.materials.append(materials['hardwood'])
    room_objects.append(floor)
    
    # Ceiling
    bpy.ops.mesh.primitive_plane_add(size=1, location=(room['position']['x'], room['position']['z'], room['position']['y'] + room['height']))
    ceiling = bpy.context.active_object
    ceiling.name = f"Ceiling_{{room['name']}}"
    ceiling.scale = (room['width'], room['length'], 1)
    ceiling.data.materials.append(materials['ceiling'])
    room_objects.append(ceiling)
    
    # Walls
    wall_thickness = 0.1
    
    # Front wall
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(room['position']['x'], room['position']['z'] + room['length']/2, room['position']['y'] + room['height']/2)
    )
    front_wall = bpy.context.active_object
    front_wall.name = f"FrontWall_{{room['name']}}"
    front_wall.scale = (room['width'], wall_thickness, room['height'])
    front_wall.data.materials.append(materials['drywall'])
    room_objects.append(front_wall)
    
    # Back wall
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(room['position']['x'], room['position']['z'] - room['length']/2, room['position']['y'] + room['height']/2)
    )
    back_wall = bpy.context.active_object
    back_wall.name = f"BackWall_{{room['name']}}"
    back_wall.scale = (room['width'], wall_thickness, room['height'])
    back_wall.data.materials.append(materials['drywall'])
    room_objects.append(back_wall)
    
    # Left wall
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(room['position']['x'] - room['width']/2, room['position']['z'], room['position']['y'] + room['height']/2)
    )
    left_wall = bpy.context.active_object
    left_wall.name = f"LeftWall_{{room['name']}}"
    left_wall.scale = (wall_thickness, room['length'], room['height'])
    left_wall.data.materials.append(materials['drywall'])
    room_objects.append(left_wall)
    
    # Right wall
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(room['position']['x'] + room['width']/2, room['position']['z'], room['position']['y'] + room['height']/2)
    )
    right_wall = bpy.context.active_object
    right_wall.name = f"RightWall_{{room['name']}}"
    right_wall.scale = (wall_thickness, room['length'], room['height'])
    right_wall.data.materials.append(materials['drywall'])
    room_objects.append(right_wall)
    
    return room_objects

def create_furniture(room):
    """Create furniture based on room type"""
    furniture = []
    room_type = room['type'].lower()
    
    if room_type == 'bedroom':
        # Bed
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'], room['position']['z'] - 1, room['position']['y'] + 0.3)
        )
        bed = bpy.context.active_object
        bed.name = f"Bed_{{room['name']}}"
        bed.scale = (2, 1.5, 0.6)
        bed.data.materials.append(materials['fabric'])
        furniture.append(bed)
        
        # Nightstand
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'] + 1.5, room['position']['z'] - 1, room['position']['y'] + 0.3)
        )
        nightstand = bpy.context.active_object
        nightstand.name = f"Nightstand_{{room['name']}}"
        nightstand.scale = (0.5, 0.4, 0.6)
        nightstand.data.materials.append(materials['wood'])
        furniture.append(nightstand)
    
    elif room_type == 'living room':
        # Sofa
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'], room['position']['z'], room['position']['y'] + 0.4)
        )
        sofa = bpy.context.active_object
        sofa.name = f"Sofa_{{room['name']}}"
        sofa.scale = (2.5, 1, 0.8)
        sofa.data.materials.append(materials['fabric'])
        furniture.append(sofa)
        
        # Coffee table
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'], room['position']['z'] + 1.5, room['position']['y'] + 0.2)
        )
        table = bpy.context.active_object
        table.name = f"CoffeeTable_{{room['name']}}"
        table.scale = (1.2, 0.8, 0.4)
        table.data.materials.append(materials['wood'])
        furniture.append(table)
    
    elif room_type == 'kitchen':
        # Kitchen island
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'], room['position']['z'], room['position']['y'] + 0.45)
        )
        island = bpy.context.active_object
        island.name = f"KitchenIsland_{{room['name']}}"
        island.scale = (2, 1, 0.9)
        island.data.materials.append(materials['wood'])
        furniture.append(island)
    
    elif room_type == 'bathroom':
        # Toilet
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'] + 1, room['position']['z'] + 1, room['position']['y'] + 0.2)
        )
        toilet = bpy.context.active_object
        toilet.name = f"Toilet_{{room['name']}}"
        toilet.scale = (0.4, 0.7, 0.4)
        toilet.data.materials.append(materials['tile'])
        furniture.append(toilet)
        
        # Sink
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(room['position']['x'] - 1, room['position']['z'] + 1, room['position']['y'] + 0.4)
        )
        sink = bpy.context.active_object
        sink.name = f"Sink_{{room['name']}}"
        sink.scale = (0.6, 0.4, 0.8)
        sink.data.materials.append(materials['tile'])
        furniture.append(sink)
    
    return furniture

# Create rooms and furniture
for room in rooms_data:
    room_objects = create_room_geometry(room)
    furniture = create_furniture(room)

# Setup lighting
# Add sun light
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
sun = bpy.context.active_object
sun.data.energy = 5
sun.data.angle = 0.1

# Add area lights for interior
bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
area_light = bpy.context.active_object
area_light.data.energy = 50
area_light.data.size = 5

# Setup camera
bpy.ops.object.camera_add(location=(15, -15, 10))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera

# Set render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = '{os.path.join(self.temp_dir, "render.png")}'

# Save the scene
blend_path = '{os.path.join(self.temp_dir, "scene.blend")}'
obj_path = '{os.path.join(self.temp_dir, "scene.obj")}'

bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# Export OBJ file for download
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_uv=True,
    export_normals=True,
    export_materials=True,
    export_triangulated_mesh=False,
    export_curves_as_nurbs=False
)

print("Scene created and exported successfully!")
print(f"Blend file: {{blend_path}}")
print(f"OBJ file: {{obj_path}}")
'''
        
        # Write the script to a temporary file
        script_path = os.path.join(self.temp_dir, 'create_scene.py')
        with open(script_path, 'w') as f:
            f.write(blender_script)
        
        # Run Blender with the script
        cmd = [
            BLENDER_PATH,
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                self.scene_file = os.path.join(self.temp_dir, "scene.blend")
                return "Scene created successfully"
            else:
                return f"Error creating scene: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Timeout: Blender took too long to create the scene"
        except FileNotFoundError:
            return "Error: Blender not found. Please install Blender and set BLENDER_PATH environment variable"
    
    def render_scene(self) -> str:
        """Render the current scene"""
        if not self.scene_file or not os.path.exists(self.scene_file):
            return "No scene file available to render"
        
        render_script = f'''
import bpy

# Open the scene
bpy.ops.wm.open_mainfile(filepath='{self.scene_file}')

# Render the scene
bpy.ops.render.render(write_still=True)

print("Render completed!")
'''
        
        script_path = os.path.join(self.temp_dir, 'render_scene.py')
        with open(script_path, 'w') as f:
            f.write(render_script)
        
        cmd = [
            BLENDER_PATH,
            '--background',
            '--python', script_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                render_path = os.path.join(self.temp_dir, "render.png")
                if os.path.exists(render_path):
                    return render_path
                else:
                    return "Render completed but file not found"
            else:
                return f"Error rendering: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Timeout: Rendering took too long"
    
    def create_360_view(self) -> List[str]:
        """Create multiple camera angles for 360-degree view"""
        if not self.scene_file or not os.path.exists(self.scene_file):
            return ["No scene file available for 360 view"]
        
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        render_paths = []
        
        for i, angle in enumerate(angles):
            render_script = f'''
import bpy
import math

# Open the scene
bpy.ops.wm.open_mainfile(filepath='{self.scene_file}')

# Get camera and rotate it
camera = bpy.context.scene.camera
if camera:
    # Set camera position in a circle around the scene
    radius = 20
    angle_rad = math.radians({angle})
    camera.location.x = radius * math.cos(angle_rad)
    camera.location.y = radius * math.sin(angle_rad)
    camera.location.z = 10
    
    # Point camera at origin
    camera.rotation_euler = (math.radians(60), 0, angle_rad + math.radians(90))

# Set output filename
bpy.context.scene.render.filepath = '{os.path.join(self.temp_dir, f"render_360_{angle:03d}.png")}'

# Render
bpy.ops.render.render(write_still=True)

print("Render {i+1}/8 completed!")
'''
            
            script_path = os.path.join(self.temp_dir, f'render_360_{angle}.py')
            with open(script_path, 'w') as f:
                f.write(render_script)
            
            cmd = [
                BLENDER_PATH,
                '--background',
                '--python', script_path
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                if result.returncode == 0:
                    render_path = os.path.join(self.temp_dir, f"render_360_{angle:03d}.png")
                    if os.path.exists(render_path):
                        render_paths.append(render_path)
            except subprocess.TimeoutExpired:
                render_paths.append(f"Timeout for angle {angle}")
        
        return render_paths

# Global renderer instance
renderer = BlenderRenderer()

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available 3D visualization resources"""
    return [
        Resource(
            uri="blender://room-viewer",
            name="3D Room Viewer",
            description="Blender-based 3D architectural visualization",
            mimeType="application/json"
        ),
        Resource(
            uri="blender://renders",
            name="Rendered Images",
            description="Generated 3D room renderings",
            mimeType="image/png"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read 3D visualization resources"""
    if uri == "blender://room-viewer":
        return json.dumps({
            "status": "ready",
            "renderer": "Blender",
            "capabilities": [
                "PBR Materials",
                "Realistic Lighting",
                "Furniture Generation",
                "360° Views",
                "High-Quality Rendering"
            ]
        })
    elif uri == "blender://renders":
        render_dir = renderer.temp_dir
        renders = []
        if os.path.exists(render_dir):
            for file in os.listdir(render_dir):
                if file.endswith('.png'):
                    renders.append(os.path.join(render_dir, file))
        return json.dumps({"renders": renders})
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available Blender tools"""
    return [
        Tool(
            name="create_3d_scene",
            description="Create a 3D scene with rooms and furniture using Blender",
            inputSchema={
                "type": "object",
                "properties": {
                    "rooms": {
                        "type": "array",
                        "description": "List of room data",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "width": {"type": "number"},
                                "height": {"type": "number"},
                                "length": {"type": "number"},
                                "area": {"type": "number"},
                                "position": {
                                    "type": "object",
                                    "properties": {
                                        "x": {"type": "number"},
                                        "y": {"type": "number"},
                                        "z": {"type": "number"}
                                    }
                                }
                            }
                        }
                    },
                    "building_dimensions": {
                        "type": "object",
                        "properties": {
                            "total_width": {"type": "number"},
                            "total_length": {"type": "number"},
                            "height": {"type": "number"}
                        }
                    }
                },
                "required": ["rooms", "building_dimensions"]
            }
        ),
        Tool(
            name="render_scene",
            description="Render the current 3D scene to an image",
            inputSchema={
                "type": "object",
                "properties": {
                    "quality": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
                    }
                }
            }
        ),
        Tool(
            name="create_360_view",
            description="Create a 360-degree view of the scene with multiple camera angles",
            inputSchema={
                "type": "object",
                "properties": {
                    "angles": {
                        "type": "number",
                        "description": "Number of angles (default: 8)",
                        "default": 8
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls"""
    if name == "create_3d_scene":
        rooms = arguments.get("rooms", [])
        building_dimensions = arguments.get("building_dimensions", {})
        
        result = renderer.create_room_scene(rooms, building_dimensions)
        
        return [TextContent(
            type="text",
            text=f"3D Scene Creation Result: {result}"
        )]
    
    elif name == "render_scene":
        quality = arguments.get("quality", "medium")
        
        result = renderer.render_scene()
        
        if result.endswith('.png') and os.path.exists(result):
            # Read image file and return as base64
            with open(result, 'rb') as f:
                image_data = f.read()
            
            return [
                TextContent(
                    type="text", 
                    text="Scene rendered successfully!"
                ),
                ImageContent(
                    type="image",
                    data=image_data,
                    mimeType="image/png"
                )
            ]
        else:
            return [TextContent(
                type="text",
                text=f"Render failed: {result}"
            )]
    
    elif name == "create_360_view":
        render_paths = renderer.create_360_view()
        
        results = [TextContent(
            type="text",
            text=f"Generated {len([p for p in render_paths if p.endswith('.png')])} 360° views"
        )]
        
        # Add rendered images
        for path in render_paths:
            if path.endswith('.png') and os.path.exists(path):
                with open(path, 'rb') as f:
                    image_data = f.read()
                results.append(ImageContent(
                    type="image",
                    data=image_data,
                    mimeType="image/png"
                ))
        
        return results
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Run the Blender MCP server"""
    # Initialize the server for GitHub Copilot integration
    import mcp.server.stdio
    from mcp.server.stdio import stdio_server
    
    # Set up logging for debugging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Blender MCP Server for GitHub Copilot integration...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        raise
