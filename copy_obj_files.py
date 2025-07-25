#!/usr/bin/env python3
"""
Utility script to copy existing OBJ files from backend/generated_models to public/renders
This fixes the download issue for previously generated models
"""

import os
import shutil
from pathlib import Path

def copy_obj_files():
    """Copy all OBJ files from backend to public directory"""
    
    # Define directories
    backend_dir = Path("backend/generated_models")
    public_dir = Path("public/renders")
    
    # Create public directory if it doesn't exist
    public_dir.mkdir(parents=True, exist_ok=True)
    
    if not backend_dir.exists():
        print(f"❌ Backend directory doesn't exist: {backend_dir}")
        return
    
    # Find all OBJ files in backend directory
    obj_files = list(backend_dir.glob("*.obj"))
    
    if not obj_files:
        print(f"📁 No OBJ files found in {backend_dir}")
        return
    
    print(f"🔍 Found {len(obj_files)} OBJ files in backend directory")
    
    copied_count = 0
    for obj_file in obj_files:
        try:
            # Copy to public directory
            dest_file = public_dir / obj_file.name
            shutil.copy2(obj_file, dest_file)
            print(f"✅ Copied: {obj_file.name}")
            copied_count += 1
            
            # Also copy associated MTL files if they exist
            mtl_file = obj_file.with_suffix('.mtl')
            if mtl_file.exists():
                dest_mtl = public_dir / mtl_file.name
                shutil.copy2(mtl_file, dest_mtl)
                print(f"✅ Copied: {mtl_file.name}")
                
        except Exception as e:
            print(f"❌ Failed to copy {obj_file.name}: {e}")
    
    print(f"🎉 Successfully copied {copied_count} OBJ files to public/renders")
    
    # List what's now available in public directory
    public_obj_files = list(public_dir.glob("*.obj"))
    print(f"📊 Public directory now has {len(public_obj_files)} OBJ files")

if __name__ == "__main__":
    print("🚀 ConstructAI OBJ File Copy Utility")
    print("=" * 50)
    copy_obj_files()
    print("=" * 50)
    print("✅ Copy operation complete!")
