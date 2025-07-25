#!/usr/bin/env python3
"""
Debug API Response
"""
import json
import requests

def debug_api_response():
    api_url = "http://localhost:3000/api/mcp/blender-bridge"
    
    payload = {
        "tool": "generate_3d_model",
        "arguments": {
            "rooms": [
                {"name": "Living Room", "type": "living", "area": 35, "width": 6, "length": 5, "height": 3},
                {"name": "Kitchen", "type": "kitchen", "area": 20, "width": 4, "length": 4, "height": 3}
            ],
            "building_dimensions": {"total_width": 25, "total_length": 20, "height": 3},
            "enhanced_features": {"furniture": True, "lighting": True},
            "architectural_style": "modern"
        }
    }
    
    response = requests.post(api_url, json=payload, timeout=300)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    debug_api_response()
