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
import math
import random
import hashlib

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
        
        print(f"BOQ Config received: {boq_config}")
        print(f"Rooms to generate: {rooms}")
        print(f"Building dimensions: {building_dims}")
        
        # Calculate dynamic layout BEFORE generating Blender script
        def calculate_optimal_layout(rooms_config, total_width, total_length):
            """Calculate truly dynamic layout pattern using multiple factors for maximum variety"""
            import random
            import hashlib
            
            # Create a unique seed from the room configuration
            room_signature = str(sorted([
                (room.get('name', ''), room.get('type', ''), room.get('area', 0))
                for room in rooms_config
            ]))
            seed = int(hashlib.md5(room_signature.encode()).hexdigest()[:8], 16)
            random.seed(seed)
            
            room_count = len(rooms_config)
            building_ratio = total_width / total_length
            total_area = sum(room.get('area', 50) for room in rooms_config)
            
            # Room type analysis
            has_living_room = any(room.get('type') == 'living_room' for room in rooms_config)
            has_kitchen = any(room.get('type') == 'kitchen' for room in rooms_config)
            bedroom_count = sum(1 for room in rooms_config if room.get('type') == 'bedroom')
            bathroom_count = sum(1 for room in rooms_config if room.get('type') == 'bathroom')
            
            # Calculate layout scores for each pattern
            layout_scores = {}
            
            # Linear layout scoring
            linear_score = 0
            if room_count <= 4: linear_score += 30
            if building_ratio > 2.0: linear_score += 40
            if building_ratio < 0.5: linear_score += 40
            linear_score += random.randint(0, 20)
            layout_scores['linear'] = linear_score
            
            # L-shaped layout scoring
            l_shaped_score = 0
            if 3 <= room_count <= 6: l_shaped_score += 35
            if 1.2 <= building_ratio <= 1.8: l_shaped_score += 30
            if has_living_room: l_shaped_score += 20
            l_shaped_score += random.randint(0, 25)
            layout_scores['l_shaped'] = l_shaped_score
            
            # Central layout scoring
            central_score = 0
            if room_count >= 3: central_score += 25
            if 0.8 <= building_ratio <= 1.2: central_score += 35
            if has_living_room: central_score += 25
            if total_area > 200: central_score += 15
            central_score += random.randint(0, 30)
            layout_scores['central'] = central_score
            
            # Split layout scoring
            split_score = 0
            if room_count >= 4: split_score += 30
            if bedroom_count >= 2: split_score += 25
            if has_kitchen and has_living_room: split_score += 20
            if building_ratio > 1.5: split_score += 20
            split_score += random.randint(0, 25)
            layout_scores['split'] = split_score
            
            # Courtyard layout scoring
            courtyard_score = 0
            if room_count >= 5: courtyard_score += 35
            if 0.9 <= building_ratio <= 1.1: courtyard_score += 30
            if total_area > 300: courtyard_score += 20
            courtyard_score += random.randint(0, 20)
            layout_scores['courtyard'] = courtyard_score
            
            # U-shaped layout scoring (new)
            u_shaped_score = 0
            if room_count >= 4: u_shaped_score += 25
            if bedroom_count >= 2: u_shaped_score += 20
            if building_ratio > 1.3: u_shaped_score += 25
            u_shaped_score += random.randint(0, 30)
            layout_scores['u_shaped'] = u_shaped_score
            
            # Cluster layout scoring (new)
            cluster_score = 0
            if room_count >= 6: cluster_score += 30
            if 0.7 <= building_ratio <= 1.3: cluster_score += 25
            if bathroom_count >= 2: cluster_score += 15
            cluster_score += random.randint(0, 35)
            layout_scores['cluster'] = cluster_score
            
            # Spiral layout scoring (new)
            spiral_score = 0
            if room_count >= 5: spiral_score += 20
            if 0.8 <= building_ratio <= 1.2: spiral_score += 30
            spiral_score += random.randint(0, 40)
            layout_scores['spiral'] = spiral_score
            
            # Choose the layout with highest score
            chosen_pattern = max(layout_scores, key=layout_scores.get)
            print(f"Layout scores: {layout_scores}")
            print(f"Selected pattern: {chosen_pattern} (score: {layout_scores[chosen_pattern]})")
            
            return chosen_pattern

        def generate_room_positions(rooms_config, total_width, total_length, layout_type):
            """Generate room positions based on layout type with maximum variety"""
            import random
            import math
            
            room_positions = []
            margin = 1.0  # Safety margin from walls
            
            # Create randomness based on room config
            room_signature = str(sorted([
                (room.get('name', ''), room.get('type', ''), room.get('area', 0))
                for room in rooms_config
            ]))
            import hashlib
            seed = int(hashlib.md5(room_signature.encode()).hexdigest()[:8], 16)
            random.seed(seed)

            if layout_type == "linear":
                # Linear arrangement with variations
                if random.choice([True, False]):
                    # Horizontal linear
                    room_width = (total_width - 2*margin) / len(rooms_config)
                    room_length = total_length - 2*margin
                    for i, room in enumerate(rooms_config):
                        x = margin + i * room_width + room_width/2
                        y = total_length/2 + random.uniform(-2, 2)  # Add slight vertical variation
                        room_positions.append({"x": x, "y": y, "width": room_width, "length": room_length})
                else:
                    # Vertical linear
                    room_width = total_width - 2*margin
                    room_length = (total_length - 2*margin) / len(rooms_config)
                    for i, room in enumerate(rooms_config):
                        x = total_width/2 + random.uniform(-2, 2)  # Add slight horizontal variation
                        y = margin + i * room_length + room_length/2
                        room_positions.append({"x": x, "y": y, "width": room_width, "length": room_length})
                    
            elif layout_type == "l_shaped":
                # L-shaped with dynamic corner placement
                corner_placement = random.choice(['bottom_left', 'bottom_right', 'top_left', 'top_right'])
                main_room_width = total_width * random.uniform(0.5, 0.7)
                main_room_length = total_length * random.uniform(0.5, 0.7)
                
                if corner_placement == 'bottom_left':
                    main_x, main_y = main_room_width/2 + margin, main_room_length/2 + margin
                elif corner_placement == 'bottom_right':
                    main_x, main_y = total_width - main_room_width/2 - margin, main_room_length/2 + margin
                elif corner_placement == 'top_left':
                    main_x, main_y = main_room_width/2 + margin, total_length - main_room_length/2 - margin
                else:  # top_right
                    main_x, main_y = total_width - main_room_width/2 - margin, total_length - main_room_length/2 - margin
                
                room_positions.append({"x": main_x, "y": main_y, "width": main_room_width, "length": main_room_length})
                
                # Remaining rooms along the L arms
                remaining_rooms = len(rooms_config) - 1
                for i in range(remaining_rooms):
                    if i < remaining_rooms // 2:
                        # First arm
                        x = main_x + main_room_width/2 + (total_width - main_x - main_room_width/2) / 2
                        y = main_y + (i - remaining_rooms//4) * main_room_length / 2
                        width = total_width - main_x - main_room_width/2 - margin
                        length = main_room_length / max(1, remaining_rooms//2)
                    else:
                        # Second arm
                        x = main_x + (i - remaining_rooms//2) * main_room_width / max(1, remaining_rooms - remaining_rooms//2)
                        y = main_y + main_room_length/2 + (total_length - main_y - main_room_length/2) / 2
                        width = main_room_width / max(1, remaining_rooms - remaining_rooms//2)
                        length = total_length - main_y - main_room_length/2 - margin
                    
                    room_positions.append({"x": x, "y": y, "width": width, "length": length})
                        
            elif layout_type == "central":
                # Central with varied positioning
                center_x, center_y = total_width/2, total_length/2
                central_room_size = min(total_width, total_length) * random.uniform(0.3, 0.5)
                
                # Central room with slight offset
                offset_x = random.uniform(-3, 3)
                offset_y = random.uniform(-3, 3)
                room_positions.append({"x": center_x + offset_x, "y": center_y + offset_y, 
                                       "width": central_room_size, "length": central_room_size})
                
                # Surrounding rooms in varied patterns
                remaining_rooms = len(rooms_config) - 1
                if remaining_rooms > 0:
                    pattern = random.choice(['circular', 'cross', 'corners'])
                    
                    if pattern == 'circular':
                        angle_step = 2 * math.pi / remaining_rooms
                        radius = central_room_size * random.uniform(0.8, 1.2)
                        for i in range(remaining_rooms):
                            angle = i * angle_step + random.uniform(-0.3, 0.3)
                            x = center_x + radius * math.cos(angle)
                            y = center_y + radius * math.sin(angle)
                            room_size = central_room_size * random.uniform(0.4, 0.7)
                            room_positions.append({"x": x, "y": y, "width": room_size, "length": room_size})
                    
                    elif pattern == 'cross':
                        positions = [
                            (center_x, center_y - central_room_size),  # North
                            (center_x + central_room_size, center_y),  # East
                            (center_x, center_y + central_room_size),  # South
                            (center_x - central_room_size, center_y)   # West
                        ]
                        for i in range(min(remaining_rooms, 4)):
                            x, y = positions[i]
                            room_size = central_room_size * random.uniform(0.5, 0.8)
                            room_positions.append({"x": x, "y": y, "width": room_size, "length": room_size})
                    
                    else:  # corners
                        corners = [
                            (margin + central_room_size/2, margin + central_room_size/2),
                            (total_width - margin - central_room_size/2, margin + central_room_size/2),
                            (total_width - margin - central_room_size/2, total_length - margin - central_room_size/2),
                            (margin + central_room_size/2, total_length - margin - central_room_size/2)
                        ]
                        for i in range(min(remaining_rooms, 4)):
                            x, y = corners[i]
                            room_size = central_room_size * random.uniform(0.4, 0.6)
                            room_positions.append({"x": x, "y": y, "width": room_size, "length": room_size})
                        
            elif layout_type == "split":
                # Split with varied orientation
                if random.choice([True, False]):
                    # Horizontal split
                    split_point = total_length * random.uniform(0.4, 0.6)
                    
                    public_rooms = [r for r in rooms_config if r.get('type') in ['living_room', 'kitchen']]
                    private_rooms = [r for r in rooms_config if r.get('type') in ['bedroom', 'bathroom']]
                    
                    if not public_rooms:
                        public_rooms = rooms_config[:len(rooms_config)//2]
                        private_rooms = rooms_config[len(rooms_config)//2:]
                    
                    # Public zone
                    if public_rooms:
                        room_width = total_width / len(public_rooms)
                        for i, room in enumerate(public_rooms):
                            x = margin + i * room_width + room_width/2
                            y = split_point/2
                            room_positions.append({"x": x, "y": y, "width": room_width, "length": split_point})
                    
                    # Private zone
                    if private_rooms:
                        room_width = total_width / len(private_rooms)
                        for i, room in enumerate(private_rooms):
                            x = margin + i * room_width + room_width/2
                            y = split_point + (total_length - split_point)/2
                            room_positions.append({"x": x, "y": y, "width": room_width, "length": total_length - split_point})
                else:
                    # Vertical split
                    split_point = total_width * random.uniform(0.4, 0.6)
                    
                    left_rooms = rooms_config[:len(rooms_config)//2]
                    right_rooms = rooms_config[len(rooms_config)//2:]
                    
                    # Left zone
                    if left_rooms:
                        room_length = total_length / len(left_rooms)
                        for i, room in enumerate(left_rooms):
                            x = split_point/2
                            y = margin + i * room_length + room_length/2
                            room_positions.append({"x": x, "y": y, "width": split_point, "length": room_length})
                    
                    # Right zone
                    if right_rooms:
                        room_length = total_length / len(right_rooms)
                        for i, room in enumerate(right_rooms):
                            x = split_point + (total_width - split_point)/2
                            y = margin + i * room_length + room_length/2
                            room_positions.append({"x": x, "y": y, "width": total_width - split_point, "length": room_length})
                        
            elif layout_type == "courtyard":
                # Courtyard with varied arrangements
                courtyard_x = total_width * random.uniform(0.3, 0.7)
                courtyard_y = total_length * random.uniform(0.3, 0.7)
                courtyard_width = min(total_width, total_length) * random.uniform(0.2, 0.4)
                courtyard_length = courtyard_width
                
                # Rooms around courtyard
                side_width = (total_width - courtyard_width) / 2
                side_length = (total_length - courtyard_length) / 2
                
                # Distribute rooms around perimeter
                perimeter_positions = []
                
                # North side
                if side_length > 5:
                    perimeter_positions.append({"x": total_width/2, "y": side_length/2, 
                                                "width": total_width, "length": side_length})
                # South side
                if side_length > 5:
                    perimeter_positions.append({"x": total_width/2, "y": total_length - side_length/2, 
                                                "width": total_width, "length": side_length})
                # East side
                if side_width > 5:
                    perimeter_positions.append({"x": total_width - side_width/2, "y": total_length/2, 
                                                "width": side_width, "length": total_length})
                # West side
                if side_width > 5:
                    perimeter_positions.append({"x": side_width/2, "y": total_length/2, 
                                                "width": side_width, "length": total_length})
                
                # Assign rooms to positions
                for i, room in enumerate(rooms_config):
                    if i < len(perimeter_positions):
                        room_positions.append(perimeter_positions[i])
                        
            elif layout_type == "u_shaped":
                # U-shaped layout
                orientation = random.choice(['horizontal', 'vertical'])
                
                if orientation == 'horizontal':
                    # Horizontal U
                    base_length = total_length * random.uniform(0.3, 0.5)
                    arm_length = (total_length - base_length) / 2
                    
                    # Base (bottom)
                    room_positions.append({"x": total_width/2, "y": base_length/2, 
                                           "width": total_width, "length": base_length})
                    
                    # Left arm
                    if len(rooms_config) > 1:
                        room_positions.append({"x": total_width * 0.25, "y": base_length + arm_length/2, 
                                               "width": total_width/2, "length": arm_length})
                    
                    # Right arm
                    if len(rooms_config) > 2:
                        room_positions.append({"x": total_width * 0.75, "y": base_length + arm_length/2, 
                                               "width": total_width/2, "length": arm_length})
                else:
                    # Vertical U
                    base_width = total_width * random.uniform(0.3, 0.5)
                    arm_width = (total_width - base_width) / 2
                    
                    # Base (left)
                    room_positions.append({"x": base_width/2, "y": total_length/2, 
                                           "width": base_width, "length": total_length})
                    
                    # Top arm
                    if len(rooms_config) > 1:
                        room_positions.append({"x": base_width + arm_width/2, "y": total_length * 0.25, 
                                               "width": arm_width, "length": total_length/2})
                    
                    # Bottom arm
                    if len(rooms_config) > 2:
                        room_positions.append({"x": base_width + arm_width/2, "y": total_length * 0.75, 
                                               "width": arm_width, "length": total_length/2})
                        
            elif layout_type == "cluster":
                # Cluster layout with random groupings
                cluster_count = random.randint(2, min(4, len(rooms_config)))
                rooms_per_cluster = len(rooms_config) // cluster_count
                
                cluster_centers = []
                for i in range(cluster_count):
                    center_x = total_width * random.uniform(0.2, 0.8)
                    center_y = total_length * random.uniform(0.2, 0.8)
                    cluster_centers.append((center_x, center_y))
                
                for i, room in enumerate(rooms_config):
                    cluster_idx = i // rooms_per_cluster
                    if cluster_idx >= len(cluster_centers):
                        cluster_idx = len(cluster_centers) - 1
                    
                    center_x, center_y = cluster_centers[cluster_idx]
                    offset_x = random.uniform(-5, 5)
                    offset_y = random.uniform(-5, 5)
                    
                    room_size = min(total_width, total_length) / (cluster_count * 2)
                    room_positions.append({"x": center_x + offset_x, "y": center_y + offset_y, 
                                           "width": room_size, "length": room_size})
                        
            elif layout_type == "spiral":
                # Spiral layout
                center_x, center_y = total_width/2, total_length/2
                angle_step = 2 * math.pi / len(rooms_config)
                
                for i, room in enumerate(rooms_config):
                    angle = i * angle_step * 1.5  # 1.5 creates the spiral effect
                    radius = (i + 1) * min(total_width, total_length) / (len(rooms_config) * 4)
                    
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                    room_size = min(total_width, total_length) / (len(rooms_config) * 1.5)
                    room_positions.append({"x": x, "y": y, "width": room_size, "length": room_size})
                    room_positions.append({"x": x, "y": y, "width": room_size, "length": room_size})
            
            # Ensure we have positions for all rooms
            while len(room_positions) < len(rooms_config):
                # Fallback to random grid layout for extra rooms
                i = len(room_positions)
                cols = math.ceil(math.sqrt(len(rooms_config)))
                rows = math.ceil(len(rooms_config) / cols)
                
                row = i // cols
                col = i % cols
                
                room_width = total_width / cols
                room_length = total_length / rows
                
                x = col * room_width + room_width/2 + random.uniform(-2, 2)
                y = row * room_length + room_length/2 + random.uniform(-2, 2)
                room_positions.append({"x": x, "y": y, "width": room_width, "length": room_length})
            
            return room_positions
        
        # Calculate layout
        total_width = building_dims['total_width']
        total_length = building_dims['total_length']
        layout_type = calculate_optimal_layout(rooms, total_width, total_length)
        room_positions = generate_room_positions(rooms, total_width, total_length, layout_type)
        
        print(f"Selected layout pattern: {layout_type} for {len(rooms)} rooms")
        for i, pos in enumerate(room_positions):
            room_name = rooms[i].get('name', f'Room_{i+1}')
            print(f"  {room_name}: {pos['width']:.1f}x{pos['length']:.1f} at ({pos['x']:.1f}, {pos['y']:.1f})")

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

# Set up GPU rendering with high quality - Force CUDA/OptiX
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences

# Force OptiX as primary choice, fallback to CUDA
cprefs.compute_device_type = 'OPTIX'
cprefs.get_devices()

# Enable all available GPU devices
gpu_devices_found = False
for device in cprefs.devices:
    if device.type in ['OPTIX', 'CUDA']:
        device.use = True
        gpu_devices_found = True
        print(f"GPU ENABLED: {{device.name}} ({{device.type}})")
    else:
        device.use = False  # Disable CPU

# If no OptiX devices found, try CUDA
if not gpu_devices_found:
    print("No OptiX devices found, trying CUDA...")
    cprefs.compute_device_type = 'CUDA'
    cprefs.get_devices()
    for device in cprefs.devices:
        if device.type == 'CUDA':
            device.use = True
            gpu_devices_found = True
            print(f"CUDA GPU ENABLED: {{device.name}}")
        else:
            device.use = False

# Force GPU rendering
scene.cycles.device = 'GPU'
if gpu_devices_found:
    print("GPU rendering enabled successfully")
else:
    print("WARNING: No GPU devices found, will use CPU")

# ULTRA HIGH QUALITY rendering settings for detailed architecture
scene.cycles.samples = 2048  # Ultra high samples for maximum detail
scene.cycles.preview_samples = 512
scene.cycles.max_bounces = 24  # More bounces for better lighting
scene.cycles.diffuse_bounces = 8
scene.cycles.glossy_bounces = 8
scene.cycles.transmission_bounces = 8
scene.cycles.volume_bounces = 4
scene.cycles.transparent_max_bounces = 12

# GPU-optimized settings for faster rendering
# Note: tile_x and tile_y are deprecated in newer Blender versions
# The GPU will automatically handle optimal tile sizes

# Enable OptiX denoising for better quality with fewer samples
scene.cycles.use_denoising = True
if cprefs.compute_device_type == 'OPTIX':
    scene.cycles.denoiser = 'OPTIX'
    print("Using OptiX denoiser for enhanced quality")
else:
    scene.cycles.denoiser = 'NLM'
    print("Using NLM denoiser")

# GPU memory optimization
scene.render.use_persistent_data = True

# 8K resolution for ultra-detailed output
scene.render.resolution_x = 7680
scene.render.resolution_y = 4320
scene.render.resolution_percentage = 100

# Color management for professional results
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'

# Ultra-detailed material creation with rich colors and textures
def create_material(name, base_color, roughness=0.5, metallic=0.0, clearcoat=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    
    # Check if IOR exists (newer Blender versions)
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.45
    
    # Add clearcoat if available
    if "Clearcoat Weight" in bsdf.inputs:
        bsdf.inputs["Clearcoat Weight"].default_value = clearcoat
    elif "Clearcoat" in bsdf.inputs:
        bsdf.inputs["Clearcoat"].default_value = clearcoat
    
    # Add noise texture for realistic variation
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs["Scale"].default_value = 5.0
    noise.inputs["Detail"].default_value = 15.0
    noise.inputs["Roughness"].default_value = 0.5
    
    # Mix noise with base color for variation
    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.location = (-200, 0)
    mix.inputs["Fac"].default_value = 0.1
    mix.inputs["Color1"].default_value = (*base_color, 1.0)
    
    # Create output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    # Link nodes
    links.new(noise.outputs["Color"], mix.inputs["Color2"])
    links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    
    return mat

# Create detailed material library with rich colors
material_lib = {{
    'oak_wood': create_material("OakWood", (0.45, 0.25, 0.12), 0.4, 0.0, 0.3),
    'walnut_wood': create_material("WalnutWood", (0.3, 0.15, 0.08), 0.35, 0.0, 0.4),
    'cherry_wood': create_material("CherryWood", (0.5, 0.2, 0.15), 0.3, 0.0, 0.5),
    'velvet_blue': create_material("VelvetBlue", (0.1, 0.2, 0.6), 0.8, 0.0, 0.2),
    'leather_brown': create_material("LeatherBrown", (0.4, 0.2, 0.1), 0.6, 0.0, 0.3),
    'silk_cream': create_material("SilkCream", (0.9, 0.87, 0.8), 0.2, 0.0, 0.8),
    'brass': create_material("Brass", (0.8, 0.6, 0.2), 0.1, 0.9, 0.8),
    'copper': create_material("Copper", (0.9, 0.4, 0.2), 0.2, 0.8, 0.6),
    'stainless_steel': create_material("StainlessSteel", (0.8, 0.8, 0.8), 0.1, 0.9, 0.9),
    'marble_white': create_material("MarbleWhite", (0.95, 0.95, 0.9), 0.05, 0.0, 0.9),
    'granite_black': create_material("GraniteBlack", (0.15, 0.15, 0.15), 0.1, 0.0, 0.8),
    'ceramic_blue': create_material("CeramicBlue", (0.2, 0.4, 0.8), 0.05, 0.0, 0.9),
    'warm_beige': create_material("WarmBeige", (0.9, 0.85, 0.7), 0.7, 0.0, 0.1),
    'sage_green': create_material("SageGreen", (0.7, 0.8, 0.6), 0.6, 0.0, 0.1),
    'terracotta': create_material("Terracotta", (0.8, 0.4, 0.3), 0.8, 0.0, 0.1),
    'clear_glass': create_material("ClearGlass", (0.9, 0.9, 0.9), 0.0, 0.0, 1.0),
    'frosted_glass': create_material("FrostedGlass", (0.9, 0.9, 0.9), 0.3, 0.0, 0.8),
    'concrete_gray': create_material("ConcreteGray", (0.6, 0.6, 0.6), 0.8, 0.0, 0.1)
}}

# Define room configurations
rooms = json.loads('{json.dumps(rooms)}')
building_dims = json.loads('{json.dumps(building_dims)}')

print(f"BLENDER DEBUG: Rooms config type: {{type(rooms)}}")
print(f"BLENDER DEBUG: Rooms config: {{rooms}}")
print(f"BLENDER DEBUG: Building dims: {{building_dims}}")
print(f"BLENDER DEBUG: Number of rooms to create: {{len(rooms)}}")

# Create a UNIFIED FLOOR PLAN with connected rooms sharing walls
# First, calculate the total building dimensions and create a unified floor
total_width = building_dims['total_width']
total_length = building_dims['total_length']
total_height = max([room.get('height', 3) for room in rooms])

print(f"Creating unified floor plan: {{total_width}}x{{total_length}}x{{total_height}}")

# Create unified foundation floor for the entire building
bpy.ops.mesh.primitive_plane_add(size=1, location=(total_width/2, total_length/2, 0))
foundation = bpy.context.active_object
foundation.name = "UnifiedFoundation"
foundation.scale = (total_width/2, total_length/2, 1)
foundation.data.materials.append(material_lib['concrete_gray'])

# Create the building's exterior walls first
wall_thickness = 0.3
wall_height = total_height * 0.5

# Exterior walls - create the building envelope
# North wall (back)
bpy.ops.mesh.primitive_cube_add(location=(total_width/2, total_length, wall_height))
north_wall = bpy.context.active_object
north_wall.name = "ExteriorWall_North"
north_wall.scale = (total_width/2, wall_thickness/2, wall_height)
north_wall.data.materials.append(material_lib['warm_beige'])

# South wall (front) 
bpy.ops.mesh.primitive_cube_add(location=(total_width/2, 0, wall_height))
south_wall = bpy.context.active_object
south_wall.name = "ExteriorWall_South"
south_wall.scale = (total_width/2, wall_thickness/2, wall_height)
south_wall.data.materials.append(material_lib['warm_beige'])

# East wall (right)
bpy.ops.mesh.primitive_cube_add(location=(total_width, total_length/2, wall_height))
east_wall = bpy.context.active_object
east_wall.name = "ExteriorWall_East"
east_wall.scale = (wall_thickness/2, total_length/2, wall_height)
east_wall.data.materials.append(material_lib['warm_beige'])

# West wall (left)
bpy.ops.mesh.primitive_cube_add(location=(0, total_length/2, wall_height))
west_wall = bpy.context.active_object
west_wall.name = "ExteriorWall_West"
west_wall.scale = (wall_thickness/2, total_length/2, wall_height)
west_wall.data.materials.append(material_lib['warm_beige'])

# Use pre-calculated room positions from main function
room_positions = {room_positions}
layout_type = "{layout_type}"
print(f"Using pre-calculated layout: {{layout_type}} with {{len(room_positions)}} positions")

# Room creation starts here
current_x = wall_thickness
current_y = wall_thickness
interior_wall_thickness = 0.2

for i, room in enumerate(rooms):
    room_name = room.get('name', f'Room_{{i+1}}')
    height = room.get('height', 3)
    room_type = room.get('type', 'bedroom')
    
    # Get dynamic position from calculated layout
    pos = room_positions[i]
    room_x = pos['x']
    room_y = pos['y'] 
    room_width = pos['width']
    room_length = pos['length']
    
    print(f"Creating {{layout_type}} room {{i+1}}: {{room_name}} ({{room_type}}) - {{room_width:.1f}}x{{room_length:.1f}} at ({{room_x:.1f}}, {{room_y:.1f}})")
    
    # Create room floor area within the unified foundation
    bpy.ops.mesh.primitive_plane_add(size=1, location=(room_x, room_y, 0.05))
    room_floor = bpy.context.active_object
    room_floor.name = f"RoomFloor_{room_name}"
    room_floor.scale = (room_width/2, room_length/2, 1)
    
    # Set room-specific floor materials
    if room_type in ['kitchen', 'bathroom']:
        room_floor.data.materials.append(material_lib['ceramic_blue'])
    elif room_type == 'living_room':
        room_floor.data.materials.append(material_lib['oak_wood'])
    elif room_type == 'bedroom':
        room_floor.data.materials.append(material_lib['walnut_wood'])
    else:
        room_floor.data.materials.append(material_lib['cherry_wood'])
    
    # Create interior walls to separate rooms (only where needed)
    interior_wall_height = height * 0.5
    
    # Check if we need walls between this room and adjacent rooms
    for room_idx, other_room in enumerate(rooms):
        if i != room_idx:
            other_pos = room_positions[room_idx]
            other_x, other_y = other_pos['x'], other_pos['y']
            other_width, other_length = other_pos['width'], other_pos['length']
            
            # Check if rooms are adjacent and need a dividing wall
            room_right = room_x + room_width/2
            room_left = room_x - room_width/2
            room_top = room_y + room_length/2
            room_bottom = room_y - room_length/2
            
            other_right = other_x + other_width/2
            other_left = other_x - other_width/2
            other_top = other_y + other_length/2
            other_bottom = other_y - other_length/2
            
            # Vertical wall between rooms
            if abs(room_right - other_left) < 0.5 and not (room_top < other_bottom or room_bottom > other_top):
                wall_x = (room_right + other_left) / 2
                wall_y = (max(room_bottom, other_bottom) + min(room_top, other_top)) / 2
                wall_length = min(room_top, other_top) - max(room_bottom, other_bottom)
                
                if wall_length > 1:  # Only create wall if significant overlap
                    bpy.ops.mesh.primitive_cube_add(location=(wall_x, wall_y, interior_wall_height))
                    wall = bpy.context.active_object
                    wall.name = f"InteriorWall_{{i}}_{{room_idx}}_V"
                    wall.scale = (interior_wall_thickness/2, wall_length/2, interior_wall_height)
                    wall.data.materials.append(material_lib['sage_green'])
                    
                    # Add doorway
                    door_y = wall_y
                    bpy.ops.mesh.primitive_cube_add(location=(wall_x, door_y, 1.1))
                    doorway = bpy.context.active_object
                    doorway.name = f"Door_{{i}}_{{room_idx}}"
                    doorway.scale = (interior_wall_thickness, 1.2, 1.1)
                    doorway.hide_render = True
                    doorway.hide_viewport = True
            
            # Horizontal wall between rooms
            elif abs(room_top - other_bottom) < 0.5 and not (room_right < other_left or room_left > other_right):
                wall_x = (max(room_left, other_left) + min(room_right, other_right)) / 2
                wall_y = (room_top + other_bottom) / 2
                wall_width = min(room_right, other_right) - max(room_left, other_left)
                
                if wall_width > 1:  # Only create wall if significant overlap
                    bpy.ops.mesh.primitive_cube_add(location=(wall_x, wall_y, interior_wall_height))
                    wall = bpy.context.active_object
                    wall.name = f"InteriorWall_{{i}}_{{room_idx}}_H"
                    wall.scale = (wall_width/2, interior_wall_thickness/2, interior_wall_height)
                    wall.data.materials.append(material_lib['sage_green'])
                    
                    # Add doorway
                    door_x = wall_x
                    bpy.ops.mesh.primitive_cube_add(location=(door_x, wall_y, 1.1))
                    doorway = bpy.context.active_object
                    doorway.name = f"Door_{{i}}_{{room_idx}}"
                    doorway.scale = (1.2, interior_wall_thickness, 1.1)
                    doorway.hide_render = True
                    doorway.hide_viewport = True
    
    # DYNAMIC furniture placement based on unified room layout
    furniture_scale = min(room_width, room_length) / 15.0  # Scale furniture to room size
    
    # Add detailed furniture based on room type with TRULY DYNAMIC sizing and positioning
    if room_type == 'bedroom':
        # Bed scaled to room size - positioned based on room dimensions
        bed_width = room_width * 0.3  # 30% of room width
        bed_length = room_length * 0.4  # 40% of room length
        bed_pos = (room_x - room_width*0.2, room_y + room_length*0.1, 0.4)
        
        # Bed frame
        bpy.ops.mesh.primitive_cube_add(location=bed_pos)
        bed_frame = bpy.context.active_object
        bed_frame.name = f"BedFrame_{{room_name}}"
        bed_frame.scale = (bed_width, bed_length, 0.3)
        
        # Mattress
        mattress_pos = (bed_pos[0], bed_pos[1], bed_pos[2] + 0.5)
        bpy.ops.mesh.primitive_cube_add(location=mattress_pos)
        mattress = bpy.context.active_object
        mattress.name = f"Mattress_{{room_name}}"
        mattress.scale = (bed_width*0.9, bed_length*0.9, 0.4)
        
        # Headboard - positioned at bed edge
        headboard_pos = (bed_pos[0], bed_pos[1] + bed_length*0.6, bed_pos[2] + 1.2)
        bpy.ops.mesh.primitive_cube_add(location=headboard_pos)
        headboard = bpy.context.active_object
        headboard.name = f"Headboard_{{room_name}}"
        headboard.scale = (bed_width, 0.3, 1.2)
        
        # Materials
        bed_frame.data.materials.append(material_lib['walnut_wood'])
        mattress.data.materials.append(material_lib['silk_cream'])
        headboard.data.materials.append(material_lib['leather_brown'])
        
        # Wardrobe scaled to room - positioned in corner
        wardrobe_width = room_width * 0.2
        wardrobe_depth = room_length * 0.15
        wardrobe_height = height * 0.8
        wardrobe_pos = (room_x + room_width*0.3, room_y + room_length*0.25, wardrobe_height*0.5)
        bpy.ops.mesh.primitive_cube_add(location=wardrobe_pos)
        wardrobe = bpy.context.active_object
        wardrobe.name = f"Wardrobe_{{room_name}}"
        wardrobe.scale = (wardrobe_width, wardrobe_depth, wardrobe_height)
        wardrobe.data.materials.append(material_lib['oak_wood'])
        
        # Bedside table - positioned relative to bed
        table_width = room_width * 0.08
        table_depth = room_length * 0.08
        table_pos = (room_x + room_width*0.25, room_y + room_length*0.15, 0.8)
        bpy.ops.mesh.primitive_cube_add(location=table_pos)
        bedside_table = bpy.context.active_object
        bedside_table.name = f"BedsideTable_{{room_name}}"
        bedside_table.scale = (table_width, table_depth, 0.8)
        
        # Table lamp - positioned on bedside table
        lamp_pos = (table_pos[0], table_pos[1], table_pos[2] + 1.2)
        bpy.ops.mesh.primitive_uv_sphere_add(location=lamp_pos, radius=0.3)
        lamp = bpy.context.active_object
        lamp.name = f"TableLamp_{{room_name}}"
        
        # Premium bedside table and lamp materials
        bedside_table.data.materials.append(material_lib['cherry_wood'])
        lamp.data.materials.append(material_lib['brass'])
        
    elif room_type == 'living_room':
        # Sofa with detailed structure - scaled to unified room
        sofa_width = room_width * 0.4  # 40% of room width
        sofa_depth = room_length * 0.2  # 20% of room depth
        sofa_pos = (room_x - room_width*0.1, room_y - room_length*0.1, 1)
        
        # Sofa body
        bpy.ops.mesh.primitive_cube_add(location=sofa_pos)
        sofa_body = bpy.context.active_object
        sofa_body.name = f"SofaBody_{{room_name}}"
        sofa_body.scale = (sofa_width, sofa_depth, 1)
        
        # Backrest - positioned at sofa edge
        backrest_pos = (sofa_pos[0], sofa_pos[1] + sofa_depth*0.7, sofa_pos[2] + 1.5)
        bpy.ops.mesh.primitive_cube_add(location=backrest_pos)
        backrest = bpy.context.active_object
        backrest.name = f"SofaBackrest_{{room_name}}"
        backrest.scale = (sofa_width, 0.5, 1.5)
        
        # Armrests - positioned at sofa sides
        armrest1_pos = (sofa_pos[0] - sofa_width*0.6, sofa_pos[1], sofa_pos[2] + 1)
        bpy.ops.mesh.primitive_cube_add(location=armrest1_pos)
        armrest1 = bpy.context.active_object
        armrest1.name = f"SofaArmrest1_{{room_name}}"
        armrest1.scale = (0.5, sofa_depth, 1)
        
        armrest2_pos = (sofa_pos[0] + sofa_width*0.6, sofa_pos[1], sofa_pos[2] + 1)
        bpy.ops.mesh.primitive_cube_add(location=armrest2_pos)
        armrest2 = bpy.context.active_object
        armrest2.name = f"SofaArmrest2_{{room_name}}"
        armrest2.scale = (0.5, sofa_depth, 1)
        
        # Luxury living room materials
        sofa_mat = material_lib['velvet_blue']
        for obj in [sofa_body, backrest, armrest1, armrest2]:
            obj.data.materials.append(sofa_mat)
        
        # Coffee table with legs - positioned in front of sofa
        table_width = room_width * 0.25
        table_depth = room_length * 0.15
        table_pos = (room_x + room_width*0.1, room_y - room_length*0.25, 0.5)
        bpy.ops.mesh.primitive_cube_add(location=table_pos)
        table_top = bpy.context.active_object
        table_top.name = f"CoffeeTableTop_{{room_name}}"
        table_top.scale = (table_width, table_depth, 0.2)
        
        # Premium coffee table material
        table_top.data.materials.append(material_lib['marble_white'])
        
        # Table legs with metallic finish - positioned at table corners
        leg_positions = [
            (table_pos[0] - table_width*0.4, table_pos[1] - table_depth*0.4, table_pos[2] - 0.8),
            (table_pos[0] + table_width*0.4, table_pos[1] - table_depth*0.4, table_pos[2] - 0.8),
            (table_pos[0] - table_width*0.4, table_pos[1] + table_depth*0.4, table_pos[2] - 0.8),
            (table_pos[0] + table_width*0.4, table_pos[1] + table_depth*0.4, table_pos[2] - 0.8)
        ]
        
        for i, leg_pos in enumerate(leg_positions):
            bpy.ops.mesh.primitive_cube_add(location=leg_pos)
            leg = bpy.context.active_object
            leg.name = f"CoffeeTableLeg{{i}}_{{room_name}}"
            leg.scale = (0.2, 0.2, 0.8)
            leg.data.materials.append(material_lib['stainless_steel'])
        
        # TV stand - positioned at opposite wall
        tv_width = room_width * 0.3
        tv_depth = room_length * 0.1
        tv_pos = (room_x + room_width*0.2, room_y + room_length*0.4, 1)
        bpy.ops.mesh.primitive_cube_add(location=tv_pos)
        tv_stand = bpy.context.active_object
        tv_stand.name = f"TVStand_{{room_name}}"
        tv_stand.scale = (tv_width, tv_depth, 1)
        
        # TV - positioned on TV stand
        tv_screen_pos = (tv_pos[0], tv_pos[1] + tv_depth*1.2, tv_pos[2] + 1.5)
        bpy.ops.mesh.primitive_cube_add(location=tv_screen_pos)
        tv_screen = bpy.context.active_object
        tv_screen.name = f"TVScreen_{{room_name}}"
        tv_screen.scale = (tv_width*0.8, 0.1, tv_width*0.5)
        
        # Premium TV and stand materials
        tv_stand.data.materials.append(material_lib['granite_black'])
        tv_screen.data.materials.append(material_lib['clear_glass'])
        
    elif room_type == 'kitchen':
        # Kitchen counter with detailed structure - scaled to unified room
        counter_width = room_width * 0.6  # 60% of room width
        counter_depth = room_length * 0.2  # 20% of room depth
        counter_pos = (room_x - room_width*0.1, room_y + room_length*0.3, 1)
        
        # Counter base
        bpy.ops.mesh.primitive_cube_add(location=counter_pos)
        counter_base = bpy.context.active_object
        counter_base.name = f"CounterBase_{{room_name}}"
        counter_base.scale = (counter_width, counter_depth, 1.5)
        
        # Counter top - scaled to counter
        top_pos = (counter_pos[0], counter_pos[1], counter_pos[2] + 1.7)
        bpy.ops.mesh.primitive_cube_add(location=top_pos)
        counter_top = bpy.context.active_object
        counter_top.name = f"CounterTop_{{room_name}}"
        counter_top.scale = (counter_width, counter_depth, 0.2)
        
        # Upper cabinets - positioned above counter
        upper_pos = (counter_pos[0], counter_pos[1] + counter_depth*0.8, counter_pos[2] + 3.5)
        bpy.ops.mesh.primitive_cube_add(location=upper_pos)
        upper_cabinet = bpy.context.active_object
        upper_cabinet.name = f"UpperCabinet_{{room_name}}"
        upper_cabinet.scale = (counter_width*0.8, counter_depth*0.6, 1.5)
        
        # Premium kitchen materials
        counter_top.data.materials.append(material_lib['marble_white'])
        counter_base.data.materials.append(material_lib['oak_wood'])
        upper_cabinet.data.materials.append(material_lib['walnut_wood'])
        
        # Refrigerator - scaled to unified room
        fridge_width = room_width * 0.1
        fridge_depth = room_length * 0.1
        fridge_height = height * 0.9
        fridge_pos = (room_x + room_width*0.25, room_y + room_length*0.3, fridge_height*0.5)
        bpy.ops.mesh.primitive_cube_add(location=fridge_pos)
        fridge = bpy.context.active_object
        fridge.name = f"Refrigerator_{{room_name}}"
        fridge.scale = (fridge_width, fridge_depth, fridge_height)
        
        # Fridge door
        door_pos = (fridge_pos[0], fridge_pos[1] - fridge_depth*1.2, fridge_pos[2])
        bpy.ops.mesh.primitive_cube_add(location=door_pos)
        door = bpy.context.active_object
        door.name = f"FridgeDoor_{{room_name}}"
        door.scale = (fridge_width*0.9, 0.1, fridge_height*0.9)
        
        # Premium refrigerator materials
        fridge.data.materials.append(material_lib['stainless_steel'])
        door.data.materials.append(material_lib['stainless_steel'])
        
        # Kitchen island - scaled to unified room
        island_width = room_width * 0.3
        island_depth = room_length * 0.2
        island_pos = (room_x + room_width*0.1, room_y - room_length*0.2, 1)
        bpy.ops.mesh.primitive_cube_add(location=island_pos)
        island = bpy.context.active_object
        island.name = f"KitchenIsland_{{room_name}}"
        island.scale = (island_width, island_depth, 1)
        
        island_mat = create_material(f"IslandMaterial_{{room_name}}", (0.7, 0.5, 0.3), 0.2)
        island.data.materials.append(island_mat)
        
    elif room_type == 'bathroom':
        # Bathroom fixtures scaled to unified room
        toilet_width = room_width * 0.15
        toilet_depth = room_length * 0.2
        toilet_pos = (room_x - room_width*0.25, room_y + room_length*0.25, 0.5)
        
        # Toilet base
        bpy.ops.mesh.primitive_cube_add(location=toilet_pos)
        toilet_base = bpy.context.active_object
        toilet_base.name = f"ToiletBase_{{room_name}}"
        toilet_base.scale = (toilet_width, toilet_depth, 0.5)
        
        # Toilet tank
        tank_pos = (toilet_pos[0], toilet_pos[1] + toilet_depth*0.6, toilet_pos[2] + 1)
        bpy.ops.mesh.primitive_cube_add(location=tank_pos)
        toilet_tank = bpy.context.active_object
        toilet_tank.name = f"ToiletTank_{{room_name}}"
        toilet_tank.scale = (toilet_width*0.8, toilet_depth*0.4, 0.8)
        
        # Sink scaled to unified room
        sink_width = room_width * 0.2
        sink_depth = room_length * 0.15
        sink_pos = (room_x + room_width*0.2, room_y + room_length*0.3, 1)
        bpy.ops.mesh.primitive_cube_add(location=sink_pos)
        sink = bpy.context.active_object
        sink.name = f"Sink_{{room_name}}"
        sink.scale = (sink_width, sink_depth, 0.2)
        
        # Sink vanity
        vanity_pos = (sink_pos[0], sink_pos[1], sink_pos[2] - 0.8)
        bpy.ops.mesh.primitive_cube_add(location=vanity_pos)
        vanity = bpy.context.active_object
        vanity.name = f"Vanity_{{room_name}}"
        vanity.scale = (sink_width*1.2, sink_depth*1.2, 1.5)
        
        # Mirror above sink
        mirror_pos = (sink_pos[0], sink_pos[1] + sink_depth*0.8, sink_pos[2] + 2)
        bpy.ops.mesh.primitive_cube_add(location=mirror_pos)
        mirror = bpy.context.active_object
        mirror.name = f"Mirror_{{room_name}}"
        mirror.scale = (sink_width*0.8, 0.1, 1.2)
        
        # Shower/bathtub scaled to unified room
        tub_width = room_width * 0.3
        tub_depth = room_length * 0.4
        tub_pos = (room_x - room_width*0.2, room_y - room_length*0.1, 0.3)
        bpy.ops.mesh.primitive_cube_add(location=tub_pos)
        bathtub = bpy.context.active_object
        bathtub.name = f"Bathtub_{{room_name}}"
        bathtub.scale = (tub_width, tub_depth, 0.6)
        
        # Premium bathroom materials
        toilet_base.data.materials.append(material_lib['ceramic_blue'])
        toilet_tank.data.materials.append(material_lib['ceramic_blue'])
        sink.data.materials.append(material_lib['marble_white'])
        vanity.data.materials.append(material_lib['walnut_wood'])
        mirror.data.materials.append(material_lib['clear_glass'])
        bathtub.data.materials.append(material_lib['ceramic_blue'])

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

# Export ultra-high-quality OBJ with materials and colors
obj_path = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}.obj'
bpy.ops.wm.obj_export(
    filepath=obj_path,
    export_selected_objects=False,
    export_materials=True,
    export_triangulated_mesh=True,
    export_smooth_groups=True,
    export_normals=True,
    export_uv=True,
    export_colors=True,
    export_pbr_extensions=True
)

print(f"Ultra-detailed OBJ exported: {{obj_path}}")
print(f"Materials included: {{len(bpy.data.materials)}} materials")
print(f"Objects included: {{len(bpy.data.objects)}} objects")

# Save blend file for reference
blend_path = r'{self.temp_dir.replace(chr(92), chr(92)+chr(92))}/boq_professional_{self.scene_id}.blend'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("PROFESSIONAL BOQ RENDERING COMPLETE")
'''
        
        # Write the script to temp file
        script_path = os.path.join(self.temp_dir, f'boq_script_{self.scene_id}.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(blender_script)
        
        try:
            # Execute Blender with the BOQ script (extended timeout for ultra-detailed rendering)
            result = subprocess.run([
                self.blender_path,
                '--background',
                '--python', script_path
            ], capture_output=True, text=True, timeout=900)  # 15 minutes for ultra-detailed rendering
            
            print(f"Blender stdout: {result.stdout}")
            if result.stderr:
                print(f"Blender stderr: {result.stderr}")
            
            # Copy files to backend directory
            backend_dir = os.path.join(os.path.dirname(__file__), 'backend', 'generated_models')
            if not os.path.exists(backend_dir):
                os.makedirs(backend_dir)
            
            generated_files = []
            
            # Check for OBJ file in temp directory first
            obj_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.obj')
            if os.path.exists(obj_path):
                dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.obj')
                shutil.copy2(obj_path, dest_path)
                generated_files.append({'type': 'obj', 'path': dest_path})
                
            # Check for MTL file in temp directory first
            mtl_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.mtl')
            if os.path.exists(mtl_path):
                dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.mtl')
                shutil.copy2(mtl_path, dest_path)
                generated_files.append({'type': 'mtl', 'path': dest_path})
                
            # Check for BLEND file in temp directory first
            blend_path = os.path.join(self.temp_dir, f'boq_professional_{self.scene_id}.blend')
            if os.path.exists(blend_path):
                dest_path = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.blend')
                shutil.copy2(blend_path, dest_path)
                generated_files.append({'type': 'blend', 'path': dest_path})
            
            # If files weren't found in temp directory, check backend directory directly
            # (sometimes Blender creates files directly in backend)
            if not generated_files:
                backend_obj = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.obj')
                backend_mtl = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.mtl')
                backend_blend = os.path.join(backend_dir, f'boq_professional_{self.scene_id}.blend')
                
                if os.path.exists(backend_obj):
                    generated_files.append({'type': 'obj', 'path': backend_obj})
                if os.path.exists(backend_mtl):
                    generated_files.append({'type': 'mtl', 'path': backend_mtl})
                if os.path.exists(backend_blend):
                    generated_files.append({'type': 'blend', 'path': backend_blend})
            
            # No PNG renders - OBJ only for ultra-detailed architecture
            
            return {
                'success': True,
                'scene_id': self.scene_id,
                'files': generated_files,
                'output': result.stdout
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Ultra-detailed BOQ rendering timeout (15 minutes)'}
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
            print(f"DEBUG: Found {len(result['files'])} files")
            for file_info in result['files']:
                print(f"DEBUG: File type: {file_info['type']}, path: {file_info['path']}")
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
