#!/usr/bin/env python3
"""
Test script to verify BOQ calculation fixes
"""
import requests
import json

def test_boq_calculation():
    """Test the BOQ calculation with 1 room input"""
    
    # Test data - 1 room should generate 1 bedroom + living room + kitchen
    test_specs = {
        "total_area": 500,
        "num_rooms": 1,  # This should create 1 BEDROOM
        "num_bathrooms": 2,
        "num_floors": 1,
        "construction_type": "residential",
        "quality_grade": "standard",
        "location": "urban",
        "room_height": 10,
        "wall_thickness": 0.5,
        "doors_per_room": 1,
        "windows_per_room": 2,
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
        print("🧪 Testing BOQ calculation with 1 room...")
        print(f"Input: {test_specs['num_rooms']} room(s), {test_specs['num_bathrooms']} bathroom(s)")
        print(f"Total area: {test_specs['total_area']} sqft")
        print()
        
        # Make API call
        response = requests.post(
            'http://localhost:8000/api/v1/boq/estimate-3d',
            json=test_specs,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ BOQ calculation successful!")
            print(f"Total cost: ₹{result['total_cost']:,.2f}")
            print()
            
            # Check room layout
            room_data = result['room_3d_data']['visualization_data']
            rooms = room_data.get('rooms', [])
            
            print("🏠 Generated room layout:")
            print(f"Total spaces: {len(rooms)}")
            print(f"Doors: {room_data.get('total_doors', 0)}")
            print(f"Windows: {room_data.get('total_windows', 0)}")
            print()
            
            print("📋 Room breakdown:")
            bedroom_count = 0
            for room in rooms:
                room_type = room.get('room_type', 'unknown')
                if room_type == 'bedroom':
                    bedroom_count += 1
                print(f"  - {room['name']}: {room['width']:.1f} × {room['length']:.1f} ft ({room['area']:.0f} sqft)")
            
            print()
            print(f"✅ Verification:")
            print(f"  - Input bedrooms: {test_specs['num_rooms']}")
            print(f"  - Generated bedrooms: {bedroom_count}")
            print(f"  - Match: {'✅ YES' if bedroom_count == test_specs['num_rooms'] else '❌ NO'}")
            
            # Check for essential rooms
            room_types = [room.get('room_type', '') for room in rooms]
            has_living = 'living_room' in room_types
            has_kitchen = 'kitchen' in room_types
            has_bathroom = 'bathroom' in room_types
            
            print(f"  - Has living room: {'✅ YES' if has_living else '❌ NO'}")
            print(f"  - Has kitchen: {'✅ YES' if has_kitchen else '❌ NO'}")
            print(f"  - Has bathroom: {'✅ YES' if has_bathroom else '❌ NO'}")
            
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_boq_calculation()
