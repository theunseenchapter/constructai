#!/usr/bin/env python3
"""
Simple test script to debug the BOQ renderer
"""

from boq_renderer import BOQRenderer
import time

# Simple test config
test_config = {
  "rooms": [
    {
      "name": "living_room",
      "type": "living_room", 
      "dimensions": {
        "width": 20,
        "length": 20,
        "height": 10
      }
    }
  ],
  "building_dimensions": {
    "total_width": 30,
    "total_length": 30,
    "height": 10
  }
}

print("Testing BOQ renderer...")

renderer = BOQRenderer()
print("Renderer created")

print("Starting rendering...")
start_time = time.time()
result = renderer.render_boq_scene(test_config)
end_time = time.time()

print(f"Rendering completed in {end_time - start_time:.2f} seconds")
print("RESULT:", result)

if result['success']:
    print("Generated files:")
    for file_info in result['files']:
        print(f"  - {file_info['type']}: {file_info['path']}")
else:
    print("ERROR:", result['error'])
