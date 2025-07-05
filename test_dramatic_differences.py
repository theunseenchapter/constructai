#!/usr/bin/env python3
"""
Test with dramatically different room configurations
"""
import time
import json
from boq_renderer import BOQRenderer

# Test 1: Tiny bathroom
tiny_config = {
    "rooms": [
        {
            "name": "tiny_bathroom",
            "type": "bathroom", 
            "width": 5,
            "length": 4,
            "height": 2.5,
            "position": {"x": 0, "y": 0, "z": 0}
        }
    ],
    "building_dimensions": {"total_width": 5, "total_length": 4, "height": 2.5}
}

# Test 2: Huge living room  
huge_config = {
    "rooms": [
        {
            "name": "massive_living_room",
            "type": "living_room",
            "width": 40,
            "length": 30, 
            "height": 5,
            "position": {"x": 0, "y": 0, "z": 0}
        }
    ],
    "building_dimensions": {"total_width": 40, "total_length": 30, "height": 5}
}

# Test 3: Complex multi-room house
complex_config = {
    "rooms": [
        {
            "name": "kitchen",
            "type": "kitchen",
            "width": 12,
            "length": 8,
            "height": 3,
            "position": {"x": 0, "y": 0, "z": 0}
        },
        {
            "name": "living_room", 
            "type": "living_room",
            "width": 20,
            "length": 15,
            "height": 3,
            "position": {"x": 15, "y": 0, "z": 0}
        },
        {
            "name": "bedroom",
            "type": "bedroom", 
            "width": 14,
            "length": 12,
            "height": 3,
            "position": {"x": 0, "y": 20, "z": 0}
        },
        {
            "name": "bathroom",
            "type": "bathroom",
            "width": 6,
            "length": 8,
            "height": 3,
            "position": {"x": 35, "y": 5, "z": 0}
        }
    ],
    "building_dimensions": {"total_width": 45, "total_length": 35, "height": 3}
}

renderer = BOQRenderer()

print("🚿 TINY BATHROOM (5x4)...")
tiny_result = renderer.render_boq_scene(tiny_config)
print(f"Tiny: {tiny_result.get('scene_id', 'FAILED')} - {len(tiny_result.get('files', []))} files")

print("\n🏰 HUGE LIVING ROOM (40x30)...")
huge_result = renderer.render_boq_scene(huge_config)  
print(f"Huge: {huge_result.get('scene_id', 'FAILED')} - {len(huge_result.get('files', []))} files")

print("\n🏠 COMPLEX HOUSE (4 rooms)...")
complex_result = renderer.render_boq_scene(complex_config)
print(f"Complex: {complex_result.get('scene_id', 'FAILED')} - {len(complex_result.get('files', []))} files")
