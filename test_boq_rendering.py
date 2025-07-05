#!/usr/bin/env python3
"""
Test the BOQ rendering with professional interior generation
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from boq_renderer import BOQRenderer

def test_professional_boq_rendering():
    """Test the professional BOQ rendering functionality"""
    
    renderer = BOQRenderer()
    
    # Sample BOQ configuration
    scene_config = {
        'room_size': {
            'width': 12,
            'length': 10,
            'height': 3
        },
        'boq_items': [
            {
                'type': 'sofa',
                'description': 'Modern sectional sofa',
                'quantity': 1,
                'unit_price': 2500
            },
            {
                'type': 'dining table',
                'description': 'Round dining table',
                'quantity': 1,
                'unit_price': 800
            },
            {
                'type': 'storage cabinet',
                'description': 'Modern storage unit',
                'quantity': 2,
                'unit_price': 650
            },
            {
                'type': 'decorative plant',
                'description': 'Large indoor plant',
                'quantity': 3,
                'unit_price': 120
            }
        ]
    }
    
    print("🚀 Starting Professional BOQ Rendering...")
    print(f"Room Size: {scene_config['room_size']['width']}x{scene_config['room_size']['length']}x{scene_config['room_size']['height']}")
    print(f"BOQ Items: {len(scene_config['boq_items'])}")
    
    try:
        result = renderer.render_boq_scene(scene_config)
        
        if result['success']:
            print("✅ Professional BOQ rendering completed successfully!")
            print(f"Scene ID: {result['scene_id']}")
            print(f"Generated {len(result['files'])} files:")
            
            for file_info in result['files']:
                print(f"  - {file_info['type'].upper()}: {file_info['path']}")
                
            # Copy files to the main project directory
            import shutil
            project_dir = 'd:\\\\constructai\\\\backend\\\\generated_models'
            
            for file_info in result['files']:
                src_path = file_info['path']
                if os.path.exists(src_path):
                    filename = os.path.basename(src_path)
                    dest_path = os.path.join(project_dir, f"boq_{filename}")
                    shutil.copy(src_path, dest_path)
                    print(f"📁 Copied to: {dest_path}")
                    
            print("🎯 BOQ rendering integration successful!")
            return True
            
        else:
            print(f"❌ BOQ rendering failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"💥 BOQ rendering error: {e}")
        return False

if __name__ == "__main__":
    test_professional_boq_rendering()
