#!/usr/bin/env python3
"""
Test the API endpoint directly to see what it returns
"""
import requests
import json

# Test configuration
test_config = {
    "tool": "generate_3d_model",
    "arguments": {
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
}

# Test the API endpoint
url = "http://localhost:3000/api/mcp/blender-bridge"

print("Testing API endpoint...")
try:
    response = requests.post(url, json=test_config, timeout=180)
    
    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    
    if response.status_code == 200:
        result = response.json()
        print("API Response:")
        print(json.dumps(result, indent=2))
        
        if result.get('success'):
            print("\n✅ API call successful!")
            print(f"Scene ID: {result.get('result', {}).get('scene_id', 'unknown')}")
            print(f"OBJ file: {result.get('result', {}).get('obj_file', 'None')}")
            print(f"MTL file: {result.get('result', {}).get('mtl_file', 'None')}")
            print(f"BLEND file: {result.get('result', {}).get('blend_file', 'None')}")
            print(f"Renders: {result.get('result', {}).get('renders', [])}")
        else:
            print(f"\n❌ API call failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
