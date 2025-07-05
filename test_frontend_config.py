#!/usr/bin/env python3
"""
Test script that mimics what the frontend does
"""
import time
import json
from boq_renderer import BOQRenderer

# Configuration that matches what the frontend sends
frontend_config = {
    "scene_type": "architectural_visualization",
    "quality": "professional",
    "detail_level": "ultra_high",
    "style": "modern_luxury",
    "render_quality": "production",
    "rooms": [
        {
            "name": "living_room",
            "type": "living_room",
            "width": 20,
            "length": 15,
            "height": 3,
            "position": {"x": 0, "y": 0, "z": 0},
            "materials": {
                "floor": "hardwood",
                "walls": "painted",
                "ceiling": "standard"
            },
            "features": ["windows", "lighting", "furniture"]
        }
    ],
    "building_dimensions": {
        "total_width": 25,
        "total_length": 20,
        "height": 3
    },
    "force_fresh": True,
    "timestamp": int(time.time() * 1000)
}

print("🚀 Testing BOQ renderer with frontend config...")
print("📊 Config:", json.dumps(frontend_config, indent=2))

# Create renderer and test
renderer = BOQRenderer()
print("🔧 Calling renderer with rooms:", frontend_config.get('rooms', []))
print("🔧 Building dimensions:", frontend_config.get('building_dimensions', {}))
result = renderer.render_boq_scene(frontend_config)

print("\n✨ RESULT:")
print(json.dumps(result, indent=2))

if result.get('success'):
    print(f"\n✅ SUCCESS! Generated {len(result.get('files', []))} files")
    for file_info in result.get('files', []):
        print(f"  - {file_info['type']}: {file_info['path']}")
        
    # Test what the command line script would output
    print(f"\n🔤 Command line output format:")
    print(f"SCENE_ID: {result['scene_id']}")
    for file_info in result['files']:
        file_type = file_info['type'].upper()
        if file_type == 'RENDER':
            print(f"RENDER_PNG: {file_info['path']}")
        else:
            print(f"{file_type}_FILE: {file_info['path']}")
else:
    print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
