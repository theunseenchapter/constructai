#!/usr/bin/env python3
"""
Random Architecture Configuration Generator
Generates diverse, varied building configurations for photorealistic rendering
"""
import random
import json
import uuid
from typing import Dict, List, Any

class RandomArchitectureGenerator:
    """Generates completely random architectural configurations"""
    
    def __init__(self):
        # Diverse architectural styles
        self.architectural_styles = [
            'modern_minimalist', 'contemporary', 'luxury_villa', 'traditional',
            'industrial_loft', 'scandinavian', 'mediterranean', 'craftsman',
            'mid_century_modern', 'farmhouse', 'colonial', 'art_deco',
            'bauhaus', 'victorian', 'ranch', 'cape_cod'
        ]
        
        # Room types with varied characteristics
        self.room_types = [
            'living', 'bedroom', 'kitchen', 'bathroom', 'dining',
            'study', 'office', 'library', 'family_room', 'guest_room',
            'master_bedroom', 'walk_in_closet', 'pantry', 'laundry',
            'mudroom', 'sunroom', 'conservatory', 'game_room',
            'home_theater', 'gym', 'workshop', 'storage'
        ]
        
        # Flooring materials
        self.flooring_materials = [
            'hardwood_walnut', 'hardwood_oak', 'hardwood_cherry', 'hardwood_maple',
            'marble_carrara', 'marble_calacatta', 'marble_nero', 'travertine',
            'porcelain_large', 'porcelain_wood_look', 'ceramic_subway',
            'limestone', 'slate', 'concrete_polished', 'bamboo',
            'cork', 'vinyl_luxury', 'carpet_wool', 'carpet_berber'
        ]
        
        # Wall finishes
        self.wall_finishes = [
            'paint_white', 'paint_gray', 'paint_beige', 'paint_blue',
            'paint_green', 'paint_warm_white', 'wallpaper_textured',
            'wallpaper_geometric', 'wood_paneling', 'stone_natural',
            'brick_exposed', 'concrete_board', 'venetian_plaster',
            'wainscoting', 'tile_subway', 'tile_mosaic'
        ]
        
        # Building size variations
        self.building_sizes = [
            {'total_width': 12, 'total_length': 10, 'height': 3.0},  # Small
            {'total_width': 15, 'total_length': 12, 'height': 3.2},  # Medium-Small
            {'total_width': 18, 'total_length': 14, 'height': 3.0},  # Medium
            {'total_width': 22, 'total_length': 16, 'height': 3.5},  # Medium-Large
            {'total_width': 25, 'total_length': 18, 'height': 3.2},  # Large
            {'total_width': 30, 'total_length': 22, 'height': 3.8},  # Very Large
            {'total_width': 16, 'total_length': 20, 'height': 3.0},  # Long & Narrow
            {'total_width': 20, 'total_length': 15, 'height': 3.5},  # Wide & Short
        ]
        
        # Lighting scenarios
        self.lighting_scenarios = [
            'bright_daylight', 'golden_hour', 'overcast', 'dramatic_shadows',
            'warm_interior', 'cool_modern', 'accent_lighting', 'natural_soft',
            'high_contrast', 'moody_evening', 'studio_lighting', 'architectural'
        ]
        
        # Color palettes
        self.color_palettes = [
            'monochrome', 'warm_earth', 'cool_blue', 'natural_green',
            'luxury_gold', 'industrial_gray', 'scandinavian_white',
            'mediterranean_terracotta', 'modern_black_white', 'pastel_soft',
            'bold_contrast', 'jewel_tones', 'neutral_beige', 'coastal_blue'
        ]

    def generate_random_configuration(self) -> Dict[str, Any]:
        """Generate a completely random architectural configuration"""
        
        # Random building size
        building_dims = random.choice(self.building_sizes).copy()
        
        # Add some variation to the selected size
        building_dims['total_width'] += random.uniform(-2, 3)
        building_dims['total_length'] += random.uniform(-2, 3)
        building_dims['height'] += random.uniform(-0.3, 0.5)
        
        # Ensure minimum sizes
        building_dims['total_width'] = max(10, building_dims['total_width'])
        building_dims['total_length'] = max(8, building_dims['total_length'])
        building_dims['height'] = max(2.5, building_dims['height'])
        
        # Random number of rooms (2-6 rooms)
        num_rooms = random.randint(2, 6)
        
        # Generate random rooms
        rooms = []
        total_area = building_dims['total_width'] * building_dims['total_length']
        available_area = total_area * 0.85  # 85% efficiency
        
        # Always include essential rooms
        essential_rooms = ['living', 'kitchen']
        if num_rooms >= 3:
            essential_rooms.append('bedroom')
        if num_rooms >= 4:
            essential_rooms.append('bathroom')
        
        # Add random additional rooms
        additional_rooms = [r for r in self.room_types if r not in essential_rooms]
        random.shuffle(additional_rooms)
        
        all_room_types = essential_rooms + additional_rooms[:num_rooms - len(essential_rooms)]
        
        for i, room_type in enumerate(all_room_types):
            # Calculate random area for this room
            if i == 0:  # First room gets more area
                room_area = available_area * random.uniform(0.25, 0.4)
            elif i == len(all_room_types) - 1:  # Last room gets remaining area
                room_area = available_area
            else:  # Middle rooms get varied area
                room_area = available_area * random.uniform(0.15, 0.3)
                available_area -= room_area
            
            # Ensure reasonable room sizes
            room_area = max(8, min(room_area, 40))
            
            room = {
                'name': f"{room_type.replace('_', ' ').title()} {i+1}",
                'type': room_type,
                'area': round(room_area, 1),
                'height': building_dims['height'] + random.uniform(-0.2, 0.3),
                'features': {
                    'furniture': random.choice([True, True, True, False]),  # 75% chance
                    'lighting': random.choice([True, True, True, False]),   # 75% chance
                    'flooring': random.choice(self.flooring_materials),
                    'walls': random.choice(self.wall_finishes)
                }
            }
            rooms.append(room)
        
        # Random architectural style
        architectural_style = random.choice(self.architectural_styles)
        
        # Random enhanced features
        enhanced_features = {
            'furniture': random.choice([True, True, True, False]),        # 75% chance
            'lighting': random.choice([True, True, True, False]),         # 75% chance
            'landscaping': random.choice([True, True, False, False]),     # 50% chance
            'interiorDetails': random.choice([True, True, True, False]),  # 75% chance
            'professionalMaterials': True,                                # Always on
            'highQualityRendering': True                                  # Always on
        }
        
        # Random quality and render settings
        quality_levels = ['good', 'professional', 'premium', 'ultra']
        resolutions = ['HD', '2K', '4K']
        sample_counts = [512, 1024, 1536, 2048]
        
        render_settings = {
            'resolution': random.choice(resolutions),
            'samples': random.choice(sample_counts),
            'denoising': True,
            'gpu_acceleration': True,
            'camera_angles': random.choice([
                ['hero', 'detail'],
                ['hero', 'aerial'], 
                ['hero', 'detail', 'aerial'],
                ['hero', 'corner'],
                ['detail', 'aerial', 'corner']
            ]),
            'lighting_scenario': random.choice(self.lighting_scenarios),
            'color_palette': random.choice(self.color_palettes)
        }
        
        config = {
            'rooms': rooms,
            'building_dimensions': building_dims,
            'enhanced_features': enhanced_features,
            'architectural_style': architectural_style,
            'quality_level': random.choice(quality_levels),
            'render_settings': render_settings,
            'generation_id': str(uuid.uuid4()),
            'variation_seed': random.randint(1, 1000000)
        }
        
        return config

    def generate_multiple_configurations(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple random configurations"""
        configs = []
        for i in range(count):
            config = self.generate_random_configuration()
            configs.append(config)
        return configs

    def save_configuration(self, config: Dict[str, Any], filename: str = None) -> str:
        """Save configuration to file"""
        if not filename:
            filename = f"random_config_{config['generation_id'][:8]}.json"
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        return filename

if __name__ == "__main__":
    generator = RandomArchitectureGenerator()
    
    # Generate and save 5 random configurations
    configs = generator.generate_multiple_configurations(5)
    
    print("Generated Random Architectural Configurations:")
    print("=" * 50)
    
    for i, config in enumerate(configs, 1):
        filename = f"random_config_{i}.json"
        generator.save_configuration(config, filename)
        
        print(f"\nConfiguration {i}:")
        print(f"  File: {filename}")
        print(f"  Style: {config['architectural_style']}")
        print(f"  Building: {config['building_dimensions']['total_width']:.1f}x{config['building_dimensions']['total_length']:.1f}m")
        print(f"  Rooms: {len(config['rooms'])}")
        print(f"  Quality: {config['quality_level']}")
        print(f"  Resolution: {config['render_settings']['resolution']}")
        print(f"  Lighting: {config['render_settings']['lighting_scenario']}")
        print(f"  Palette: {config['render_settings']['color_palette']}")
        print(f"  Rooms: {', '.join([r['name'] for r in config['rooms']])}")
