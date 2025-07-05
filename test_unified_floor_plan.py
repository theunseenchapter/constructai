#!/usr/bin/env python3
"""
Test script for the new unified floor plan generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boq_renderer import BOQRenderer
import json

def test_unified_floor_plan():
    print("Testing unified floor plan generation...")
    
    # Create a test configuration with multiple rooms
    test_config = {
        "rooms": [
            {
                "name": "Living Room",
                "type": "living_room",
                "width": 20,
                "length": 15,
                "height": 3.5
            },
            {
                "name": "Kitchen",
                "type": "kitchen", 
                "width": 15,
                "length": 12,
                "height": 3.2
            },
            {
                "name": "Master Bedroom",
                "type": "bedroom",
                "width": 18,
                "length": 14,
                "height": 3.0
            },
            {
                "name": "Bathroom",
                "type": "bathroom",
                "width": 8,
                "length": 10,
                "height": 2.8
            }
        ]
    }
    
    print(f"Test config: {json.dumps(test_config, indent=2)}")
    
    # Initialize renderer
    renderer = BOQRenderer()
    
    # Generate unified floor plan
    print("Generating unified floor plan...")
    result = renderer.render_boq_scene(test_config)
    
    print(f"Generation result: {result}")
    
    if result.get('success'):
        print("✓ Unified floor plan generated successfully!")
        print(f"  Files created: {result.get('files', {})}")
        
        # Check if files exist
        files = result.get('files', [])
        if isinstance(files, list):
            print(f"  Files list: {files}")
            for file_info in files:
                if isinstance(file_info, dict):
                    file_type = file_info.get('type', 'unknown')
                    file_path = file_info.get('path', '')
                    if file_path and os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        print(f"  {file_type}: {file_path} ({file_size} bytes)")
                    else:
                        print(f"  {file_type}: MISSING - {file_path}")
                else:
                    # Handle old format where file_info is just a path string
                    if file_info and os.path.exists(file_info):
                        file_size = os.path.getsize(file_info)
                        print(f"  File: {file_info} ({file_size} bytes)")
                    else:
                        print(f"  File: MISSING - {file_info}")
        elif isinstance(files, dict):
            for file_type, file_path in files.items():
                if file_path and os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"  {file_type}: {file_path} ({file_size} bytes)")
                else:
                    print(f"  {file_type}: MISSING - {file_path}")
    else:
        print("✗ Failed to generate unified floor plan")
        print(f"Error: {result.get('error', 'Unknown error')}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_unified_floor_plan()
    if success:
        print("\n🎉 Unified floor plan test completed successfully!")
    else:
        print("\n❌ Unified floor plan test failed!")
        sys.exit(1)
