import os
import json
from datetime import datetime

# List all ultra_varied files and sort by modification time
renders_dir = r'd:\constructai\public\renders'
ultra_files = []

for file in os.listdir(renders_dir):
    if file.startswith('ultra_varied_') and file.endswith('.obj'):
        filepath = os.path.join(renders_dir, file)
        mtime = os.path.getmtime(filepath)
        size = os.path.getsize(filepath)
        ultra_files.append({
            'file': file,
            'path': filepath,
            'mtime': mtime,
            'size': size,
            'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        })

# Sort by modification time (newest first)
ultra_files.sort(key=lambda x: x['mtime'], reverse=True)

print('Latest ultra-varied OBJ files:')
for i, f in enumerate(ultra_files[:5]):
    filename = f['file']
    modified = f['modified']
    size = f['size']
    print(f'{i+1}. {filename}')
    print(f'   Modified: {modified}')
    print(f'   Size: {size:,} bytes')
    print()

if ultra_files:
    latest = ultra_files[0]
    latest_file = latest['file']
    print(f'LATEST FILE: {latest_file}')
    print(f'WEB PATH: /renders/{latest_file}')
