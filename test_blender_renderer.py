#!/usr/bin/env python3
"""
Test script for the advanced Blender renderer
"""
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from advanced_blender_renderer import AdvancedBlenderRenderer

def test_renderer():
    """Test the advanced Blender renderer"""
    print("🧪 Testing Advanced Blender Renderer...")
    
    # Create renderer
    renderer = AdvancedBlenderRenderer()
    
    # Test configuration
    test_config = {
        "rooms": [
            {
                "name": "Living Room",
                "type": "living_room",
                "width": 6,
                "length": 8,
                "height": 3,
                "position": {"x": 0, "y": 0}
            },
            {
                "name": "Kitchen",
                "type": "kitchen",
                "width": 4,
                "length": 6,
                "height": 3,
                "position": {"x": 6, "y": 0}
            }
        ],
        "building_dimensions": {
            "total_width": 12,
            "total_length": 8,
            "height": 3
        },
        "quality": "professional"
    }
    
    print("🎨 Testing generate_3d_model...")
    try:
        result = renderer.generate_3d_model(test_config)
        print("✅ Test completed!")
        print(f"🎯 Result: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print("🎉 SUCCESS: Professional 3D model generated!")
            if result.get('files'):
                print(f"📁 Generated files: {len(result['files'])}")
                for file in result['files']:
                    print(f"  - {os.path.basename(file)}")
        else:
            print("❌ FAILED: 3D model generation failed")
            if result.get('error'):
                print(f"Error: {result['error']}")
                
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_renderer()
