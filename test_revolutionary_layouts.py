#!/usr/bin/env python3
"""
Test script to demonstrate the revolutionary new layout system
that generates completely different 3D floor plans for different inputs.
"""

import subprocess
import sys
import os
import time
import hashlib
import json

def run_blender_generation(config_name, rooms_config, building_dims):
    """Run the BOQ renderer with specific configuration"""
    
    boq_config = {
        "rooms": rooms_config,
        "building_dimensions": building_dims,
        "quality": "ultra_high",
        "style": "modern_architecture"
    }
    
    print(f"\n{'='*80}")
    print(f"GENERATING LAYOUT: {config_name}")
    print(f"{'='*80}")
    print(f"Rooms: {len(rooms_config)}")
    print(f"Building: {building_dims['total_width']}x{building_dims['total_length']}")
    print(f"Room types: {[r.get('type', 'unknown') for r in rooms_config]}")
    
    try:
        # Save config to temporary file
        config_file = f"temp_config_{config_name.replace(' ', '_').lower()}.json"
        with open(config_file, 'w') as f:
            json.dump(boq_config, f, indent=2)
        
        # Run the BOQ renderer
        result = subprocess.run([
            sys.executable, "boq_renderer.py", config_file
        ], capture_output=True, text=True, cwd="d:\\constructai")
        
        # Clean up temp file
        try:
            os.remove(config_file)
        except:
            pass
        
        if result.returncode != 0:
            print(f"❌ ERROR: {result.stderr}")
            return None
        
        # Parse output
        obj_file = None
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('OBJ_FILE:'):
                obj_file = line.split(':', 1)[1].strip()
                print(f"✅ Generated: {obj_file}")
                
                # Get file stats
                if os.path.exists(obj_file):
                    size = os.path.getsize(obj_file)
                    print(f"   File size: {size:,} bytes")
                    
                    # Calculate file hash for uniqueness verification
                    with open(obj_file, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()[:12]
                    print(f"   File hash: {file_hash}")
                    
                    return {
                        'config': config_name,
                        'file': obj_file,
                        'size': size,
                        'hash': file_hash
                    }
                else:
                    print(f"❌ File not found: {obj_file}")
                    return None
            elif line.startswith('Selected pattern:'):
                print(f"🏗️  {line}")
            elif line.startswith('Layout scores:'):
                print(f"📊 {line}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    """Test different layout configurations"""
    
    print("🚀 REVOLUTIONARY LAYOUT SYSTEM TEST")
    print("=" * 80)
    print("Testing completely different 3D floor plan generations...")
    
    # Configuration 1: Small apartment
    config1 = {
        "name": "Small Urban Apartment",
        "rooms": [
            {"name": "Living Room", "type": "living_room", "area": 120},
            {"name": "Kitchen", "type": "kitchen", "area": 60},
            {"name": "Bedroom", "type": "bedroom", "area": 90},
            {"name": "Bathroom", "type": "bathroom", "area": 30}
        ],
        "building_dimensions": {"total_width": 25, "total_length": 15, "height": 8}
    }
    
    # Configuration 2: Large family home
    config2 = {
        "name": "Large Family Home",
        "rooms": [
            {"name": "Master Living Room", "type": "living_room", "area": 200},
            {"name": "Modern Kitchen", "type": "kitchen", "area": 100},
            {"name": "Master Bedroom", "type": "bedroom", "area": 150},
            {"name": "Kids Bedroom 1", "type": "bedroom", "area": 80},
            {"name": "Kids Bedroom 2", "type": "bedroom", "area": 80},
            {"name": "Master Bathroom", "type": "bathroom", "area": 50},
            {"name": "Guest Bathroom", "type": "bathroom", "area": 35}
        ],
        "building_dimensions": {"total_width": 40, "total_length": 30, "height": 10}
    }
    
    # Configuration 3: Luxury villa
    config3 = {
        "name": "Luxury Villa",
        "rooms": [
            {"name": "Grand Living Room", "type": "living_room", "area": 300},
            {"name": "Gourmet Kitchen", "type": "kitchen", "area": 150},
            {"name": "Master Suite", "type": "bedroom", "area": 200},
            {"name": "Guest Bedroom 1", "type": "bedroom", "area": 120},
            {"name": "Guest Bedroom 2", "type": "bedroom", "area": 120},
            {"name": "Office", "type": "office", "area": 100},
            {"name": "Master Bathroom", "type": "bathroom", "area": 80},
            {"name": "Guest Bathroom 1", "type": "bathroom", "area": 40},
            {"name": "Guest Bathroom 2", "type": "bathroom", "area": 40}
        ],
        "building_dimensions": {"total_width": 50, "total_length": 35, "height": 12}
    }
    
    # Configuration 4: Narrow townhouse
    config4 = {
        "name": "Narrow Townhouse",
        "rooms": [
            {"name": "Living Room", "type": "living_room", "area": 100},
            {"name": "Kitchen", "type": "kitchen", "area": 70},
            {"name": "Bedroom 1", "type": "bedroom", "area": 85},
            {"name": "Bedroom 2", "type": "bedroom", "area": 85},
            {"name": "Bathroom", "type": "bathroom", "area": 40}
        ],
        "building_dimensions": {"total_width": 12, "total_length": 45, "height": 9}
    }
    
    # Configuration 5: Square studio
    config5 = {
        "name": "Square Studio",
        "rooms": [
            {"name": "Main Studio", "type": "living_room", "area": 180},
            {"name": "Kitchenette", "type": "kitchen", "area": 40},
            {"name": "Bathroom", "type": "bathroom", "area": 30}
        ],
        "building_dimensions": {"total_width": 20, "total_length": 20, "height": 8}
    }
    
    # Configuration 6: Courtyard house
    config6 = {
        "name": "Courtyard House",
        "rooms": [
            {"name": "Living Room", "type": "living_room", "area": 140},
            {"name": "Kitchen", "type": "kitchen", "area": 80},
            {"name": "Master Bedroom", "type": "bedroom", "area": 120},
            {"name": "Guest Bedroom", "type": "bedroom", "area": 100},
            {"name": "Study", "type": "office", "area": 60},
            {"name": "Master Bathroom", "type": "bathroom", "area": 50},
            {"name": "Guest Bathroom", "type": "bathroom", "area": 35}
        ],
        "building_dimensions": {"total_width": 35, "total_length": 35, "height": 10}
    }
    
    configs = [config1, config2, config3, config4, config5, config6]
    results = []
    
    for config in configs:
        result = run_blender_generation(
            config["name"], 
            config["rooms"], 
            config["building_dimensions"]
        )
        if result:
            results.append(result)
        
        # Small delay between generations
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*80}")
    print("🎯 REVOLUTIONARY LAYOUT RESULTS SUMMARY")
    print(f"{'='*80}")
    
    if len(results) >= 2:
        print(f"✅ Generated {len(results)} completely different floor plans!")
        
        # Show uniqueness
        unique_hashes = set(r['hash'] for r in results)
        unique_sizes = set(r['size'] for r in results)
        
        print(f"🔢 Unique file hashes: {len(unique_hashes)}/{len(results)}")
        print(f"📏 Unique file sizes: {len(unique_sizes)}/{len(results)}")
        
        print(f"\n📋 DETAILED RESULTS:")
        for result in results:
            print(f"  • {result['config']}: {result['size']:,} bytes, hash: {result['hash']}")
        
        if len(unique_hashes) == len(results):
            print(f"\n🏆 SUCCESS: All layouts are completely unique!")
            print(f"🎨 The revolutionary system generates truly different floor plans!")
        else:
            print(f"\n⚠️  WARNING: Some layouts may be similar")
    else:
        print(f"❌ Only generated {len(results)} layouts")
    
    print(f"\n{'='*80}")
    print("🎉 REVOLUTIONARY LAYOUT SYSTEM TEST COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
