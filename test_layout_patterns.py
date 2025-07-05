#!/usr/bin/env python3
"""
Test script to demonstrate different dynamic layout patterns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boq_renderer import BOQRenderer
import json

def test_layout_patterns():
    """Test different layout patterns to show variety"""
    
    print("🏗️  Testing Dynamic Layout Patterns")
    print("=" * 50)
    
    # Test different configurations to trigger different layouts
    test_configs = [
        {
            "name": "Linear Layout (2 rooms)",
            "config": {
                "rooms": [
                    {"name": "Living Room", "type": "living_room", "width": 20, "length": 15, "height": 3.5},
                    {"name": "Kitchen", "type": "kitchen", "width": 15, "length": 12, "height": 3.2}
                ],
                "building_dimensions": {"total_width": 40, "total_length": 20, "height": 10}
            }
        },
        {
            "name": "L-Shaped Layout (3 rooms)",
            "config": {
                "rooms": [
                    {"name": "Living Room", "type": "living_room", "width": 25, "length": 20, "height": 3.5},
                    {"name": "Kitchen", "type": "kitchen", "width": 15, "length": 12, "height": 3.2},
                    {"name": "Bedroom", "type": "bedroom", "width": 18, "length": 14, "height": 3.0}
                ],
                "building_dimensions": {"total_width": 35, "total_length": 35, "height": 10}
            }
        },
        {
            "name": "Central Layout (4 rooms)",
            "config": {
                "rooms": [
                    {"name": "Living Room", "type": "living_room", "width": 25, "length": 20, "height": 3.5},
                    {"name": "Kitchen", "type": "kitchen", "width": 15, "length": 12, "height": 3.2},
                    {"name": "Master Bedroom", "type": "bedroom", "width": 18, "length": 14, "height": 3.0},
                    {"name": "Bathroom", "type": "bathroom", "width": 8, "length": 10, "height": 2.8}
                ],
                "building_dimensions": {"total_width": 30, "total_length": 30, "height": 10}
            }
        },
        {
            "name": "Split Zone Layout (4 rooms)",
            "config": {
                "rooms": [
                    {"name": "Living Room", "type": "living_room", "width": 25, "length": 20, "height": 3.5},
                    {"name": "Kitchen", "type": "kitchen", "width": 15, "length": 12, "height": 3.2},
                    {"name": "Master Bedroom", "type": "bedroom", "width": 18, "length": 14, "height": 3.0},
                    {"name": "Bathroom", "type": "bathroom", "width": 8, "length": 10, "height": 2.8}
                ],
                "building_dimensions": {"total_width": 45, "total_length": 25, "height": 10}
            }
        },
        {
            "name": "Courtyard Layout (5 rooms)",
            "config": {
                "rooms": [
                    {"name": "Living Room", "type": "living_room", "width": 25, "length": 20, "height": 3.5},
                    {"name": "Kitchen", "type": "kitchen", "width": 15, "length": 12, "height": 3.2},
                    {"name": "Master Bedroom", "type": "bedroom", "width": 18, "length": 14, "height": 3.0},
                    {"name": "Guest Bedroom", "type": "bedroom", "width": 16, "length": 12, "height": 3.0},
                    {"name": "Bathroom", "type": "bathroom", "width": 8, "length": 10, "height": 2.8}
                ],
                "building_dimensions": {"total_width": 40, "total_length": 40, "height": 10}
            }
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_configs):
        print(f"\n🏠 Test {i+1}: {test_case['name']}")
        print(f"   Building: {test_case['config']['building_dimensions']['total_width']}x{test_case['config']['building_dimensions']['total_length']}")
        print(f"   Rooms: {len(test_case['config']['rooms'])}")
        
        # Initialize renderer
        renderer = BOQRenderer()
        
        # Generate layout
        try:
            result = renderer.render_boq_scene(test_case['config'])
            
            if result.get('success'):
                files = result.get('files', [])
                if files:
                    obj_file = next((f for f in files if f.get('type') == 'obj'), None)
                    if obj_file and os.path.exists(obj_file['path']):
                        file_size = os.path.getsize(obj_file['path'])
                        print(f"   ✅ Generated: {obj_file['path']} ({file_size:,} bytes)")
                        results.append({
                            "name": test_case['name'],
                            "file": obj_file['path'],
                            "size": file_size,
                            "success": True
                        })
                    else:
                        print(f"   ❌ File not found")
                        results.append({"name": test_case['name'], "success": False})
                else:
                    print(f"   ❌ No files generated")
                    results.append({"name": test_case['name'], "success": False})
            else:
                print(f"   ❌ Generation failed: {result.get('error', 'Unknown error')}")
                results.append({"name": test_case['name'], "success": False})
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results.append({"name": test_case['name'], "success": False, "error": str(e)})
    
    # Summary
    print("\n📊 RESULTS SUMMARY:")
    print("=" * 50)
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]
    
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print("\n🎯 File Size Comparison (shows layout variety):")
        for result in successful:
            print(f"   {result['name']}: {result['size']:,} bytes")
    
    if failed:
        print("\n❌ Failed Tests:")
        for result in failed:
            print(f"   {result['name']}: {result.get('error', 'Unknown error')}")
    
    return len(successful) == len(results)

if __name__ == "__main__":
    success = test_layout_patterns()
    if success:
        print("\n🎉 All layout patterns generated successfully!")
        print("Each layout should be visually different!")
    else:
        print("\n⚠️  Some layout patterns failed.")
    
    print("\n💡 Next: Check the generated OBJ files in Blender to see the different layouts!")
