#!/usr/bin/env python3
"""
Simple test to verify the BOQ renderer is working correctly
"""

import subprocess
import sys
import json

# Create a simple test config
test_config = {
    "rooms": [
        {"name": "Living Room", "type": "living_room", "area": 120},
        {"name": "Kitchen", "type": "kitchen", "area": 60}
    ],
    "building_dimensions": {"total_width": 20, "total_length": 15, "height": 8},
    "quality": "high"
}

# Save test config
with open('simple_test_config.json', 'w') as f:
    json.dump(test_config, f, indent=2)

print("🧪 Testing BOQ renderer with simple config...")
print(f"Config: {test_config}")

# Test the renderer
try:
    result = subprocess.run([
        sys.executable, "boq_renderer.py", "simple_test_config.json"
    ], capture_output=True, text=True)
    
    print(f"Return code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    print(f"STDERR:\n{result.stderr}")
    
    if result.returncode == 0:
        print("✅ SUCCESS: BOQ renderer completed without errors!")
    else:
        print("❌ FAILED: BOQ renderer failed")
        
except Exception as e:
    print(f"❌ Exception: {e}")
