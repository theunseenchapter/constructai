#!/usr/bin/env python3
"""
Quick fix for the BOQ renderer - remove duplicate layout code
"""

import re

# Read the current file
with open('boq_renderer.py', 'r') as f:
    content = f.read()

# Find and remove the duplicate layout code section
# The duplicate starts after "# Room creation starts here" and before "for i, room in enumerate(rooms):"
pattern = r'(# Room creation starts here.*?current_y = wall_thickness\ninternal_wall_thickness = 0\.2\n)(.*?)(for i, room in enumerate\(rooms\):)'
replacement = r'\1\3'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('boq_renderer.py', 'w') as f:
    f.write(new_content)

print("Fixed BOQ renderer by removing duplicate layout code")
