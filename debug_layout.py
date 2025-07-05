#!/usr/bin/env python3
"""
Simple test to debug the layout issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boq_renderer import BOQRenderer

def simple_test():
    print("Testing simple 2-room layout...")
    
    config = {
        "rooms": [
            {"name": "Living Room", "type": "living_room", "width": 20, "length": 15, "height": 3.5},
            {"name": "Kitchen", "type": "kitchen", "width": 15, "length": 12, "height": 3.2}
        ],
        "building_dimensions": {"total_width": 40, "total_length": 20, "height": 10}
    }
    
    renderer = BOQRenderer()
    
    try:
        result = renderer.render_boq_scene(config)
        print(f"Result: {result.get('success', False)}")
        if not result.get('success'):
            print(f"Error details: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    simple_test()
