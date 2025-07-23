#!/usr/bin/env python3
"""
Copy learning materials data to frontend for web access
"""

import json
import shutil
from pathlib import Path

def copy_learning_materials():
    """Copy JSON data to frontend data directory"""
    
    # Paths
    materials_dir = Path("../learning-materials")
    frontend_data_dir = Path("data")
    
    # Create frontend data directory
    frontend_data_dir.mkdir(exist_ok=True)
    
    # Copy all topic directories
    if materials_dir.exists():
        for topic_dir in materials_dir.iterdir():
            if topic_dir.is_dir():
                target_dir = frontend_data_dir / topic_dir.name
                target_dir.mkdir(exist_ok=True)
                
                # Copy JSON files
                for json_file in topic_dir.glob("*.json"):
                    shutil.copy2(json_file, target_dir / json_file.name)
                    print(f"Copied {json_file} -> {target_dir / json_file.name}")
        
        print(f"\n✓ Learning materials copied to {frontend_data_dir}")
        print("You can now run a local server to access the frontend")
        print("\nTo start a simple HTTP server:")
        print("python3 -m http.server 8000")
        print("Then open: http://localhost:8000")
    else:
        print("❌ Learning materials directory not found")
        print("Run the learning materials generation script first")

if __name__ == "__main__":
    copy_learning_materials()