#!/usr/bin/env python3
"""
Test script to verify door and window calculations
"""
import requests
import json

def test_door_window_calculation():
    """Test the door and window calculation"""
    
    # Test data - 1 room with 1 door per room and 2 windows per room
    test_specs = {
        "total_area": 500,
        "num_rooms": 1,
        "num_bathrooms": 2,
        "num_floors": 1,
        "construction_type": "residential",
        "quality_grade": "standard",
        "location": "urban",
        "room_height": 10,
        "wall_thickness": 0.5,
        "doors_per_room": 1,      # 1 door per bedroom
        "windows_per_room": 2,    # 2 windows per bedroom
        "main_door_type": "premium",
        "room_door_type": "standard",
        "window_type": "standard",
        "room_layout": "rectangular",
        "include_balcony": False,
        "balcony_area": 0,
        "ceiling_type": "false",
        "flooring_type": "tiles"
    }
    
    try:
        print("🧪 Testing door and window calculation...")
        print(f"Input: {test_specs['num_rooms']} room(s)")
        print(f"Doors per room: {test_specs['doors_per_room']}")
        print(f"Windows per room: {test_specs['windows_per_room']}")
        print()
        
        # Make API call
        response = requests.post(
            'http://localhost:8000/api/v1/boq/estimate-3d',
            json=test_specs,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            room_data = result['room_3d_data']['visualization_data']
            rooms = room_data.get('rooms', [])
            
            print("🚪 Door and Window Analysis:")
            print(f"Total doors: {room_data.get('total_doors', 0)}")
            print(f"Total windows: {room_data.get('total_windows', 0)}")
            print()
            
            # Expected calculation:
            # Bedroom doors: 1 room × 1 door = 1 door
            # Common area doors: 1 living room + 1 kitchen + 2 bathrooms = 4 doors
            # Total doors: 1 + 4 = 5 doors
            
            # Bedroom windows: 1 room × 2 windows = 2 windows
            # Common area windows: 3 living room + 1 kitchen + 2 bathrooms = 6 windows
            # Total windows: 2 + 6 = 8 windows
            
            expected_doors = (test_specs['doors_per_room'] * test_specs['num_rooms']) + 1 + 1 + test_specs['num_bathrooms']
            expected_windows = (test_specs['windows_per_room'] * test_specs['num_rooms']) + 3 + 1 + test_specs['num_bathrooms']
            
            print(f"Expected doors: {expected_doors}")
            print(f"Expected windows: {expected_windows}")
            print(f"Door calculation: {'✅ CORRECT' if room_data.get('total_doors', 0) == expected_doors else '❌ WRONG'}")
            print(f"Window calculation: {'✅ CORRECT' if room_data.get('total_windows', 0) == expected_windows else '❌ WRONG'}")
            
            print()
            print("📋 Detailed breakdown:")
            for room in rooms:
                doors = len(room.get('doors', []))
                windows = len(room.get('windows', []))
                print(f"  - {room['name']}: {doors} door(s), {windows} window(s)")
            
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_door_window_calculation()
