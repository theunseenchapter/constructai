#!/usr/bin/env python3
"""
Test with different room configurations to see if it generates different scenes
"""
import time
import json
from boq_renderer import BOQRenderer

# Test 1: Kitchen scene
kitchen_config = {
    "scene_type": "architectural_visualization",
    "quality": "professional", 
    "rooms": [
        {
            "name": "modern_kitchen",
            "type": "kitchen",
            "width": 15,
            "length": 12,
            "height": 3,
            "position": {"x": 0, "y": 0, "z": 0}
        }
    ],
    "building_dimensions": {
        "total_width": 15,
        "total_length": 12,
        "height": 3
    },
    "timestamp": int(time.time() * 1000)
}

# Test 2: Bedroom scene
bedroom_config = {
    "scene_type": "architectural_visualization", 
    "quality": "professional",
    "rooms": [
        {
            "name": "master_bedroom",
            "type": "bedroom",
            "width": 18,
            "length": 16,
            "height": 3,
            "position": {"x": 0, "y": 0, "z": 0}
        }
    ],
    "building_dimensions": {
        "total_width": 18,
        "total_length": 16,
        "height": 3
    },
    "timestamp": int(time.time() * 1000)
}

# Test 3: Multi-room scene
multi_room_config = {
    "scene_type": "architectural_visualization",
    "quality": "professional",
    "rooms": [
        {
            "name": "living_room",
            "type": "living_room", 
            "width": 20,
            "length": 15,
            "height": 3,
            "position": {"x": 0, "y": 0, "z": 0}
        },
        {
            "name": "kitchen",
            "type": "kitchen",
            "width": 12,
            "length": 10,
            "height": 3,
            "position": {"x": 25, "y": 0, "z": 0}
        }
    ],
    "building_dimensions": {
        "total_width": 40,
        "total_length": 20,
        "height": 3
    },
    "timestamp": int(time.time() * 1000)
}

renderer = BOQRenderer()

print("🍳 TESTING KITCHEN SCENE...")
kitchen_result = renderer.render_boq_scene(kitchen_config)
print(f"Kitchen Scene ID: {kitchen_result.get('scene_id', 'FAILED')}")
print(f"Kitchen Files: {len(kitchen_result.get('files', []))}")

print("\n🛏️ TESTING BEDROOM SCENE...")
bedroom_result = renderer.render_boq_scene(bedroom_config)
print(f"Bedroom Scene ID: {bedroom_result.get('scene_id', 'FAILED')}")
print(f"Bedroom Files: {len(bedroom_result.get('files', []))}")

print("\n🏠 TESTING MULTI-ROOM SCENE...")
multi_result = renderer.render_boq_scene(multi_room_config)
print(f"Multi-room Scene ID: {multi_result.get('scene_id', 'FAILED')}")
print(f"Multi-room Files: {len(multi_result.get('files', []))}")

# Compare scene IDs
print(f"\n🔍 COMPARISON:")
print(f"Kitchen ID: {kitchen_result.get('scene_id', 'FAILED')}")
print(f"Bedroom ID: {bedroom_result.get('scene_id', 'FAILED')}")
print(f"Multi-room ID: {multi_result.get('scene_id', 'FAILED')}")

if len(set([kitchen_result.get('scene_id'), bedroom_result.get('scene_id'), multi_result.get('scene_id')])) == 3:
    print("✅ All scenes have different IDs - Dynamic generation working!")
else:
    print("❌ Scene IDs are not unique - Dynamic generation NOT working!")
