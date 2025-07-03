#!/usr/bin/env python3
"""
Script to fix Path() to str(Path()) conversions in example files
"""

import os
import re
from pathlib import Path

def fix_file(file_path):
    """Fix Path() to str(Path()) in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match mjcf_path=Path() followed by .joinpath() calls
    pattern = r'(mjcf_path=Path\(\)\s*\.joinpath\([^)]+\)(?:\s*\.joinpath\([^)]+\))*)'
    
    def replace_match(match):
        path_expr = match.group(1)
        # Add str() wrapper
        return f"mjcf_path=str({path_expr})"
    
    new_content = re.sub(pattern, replace_match, content, flags=re.MULTILINE | re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {file_path}")
        return True
    return False

def main():
    """Fix all example files"""
    examples_dir = Path(".")
    
    # Files to fix based on the grep search results
    files_to_fix = [
        "galbot_interface_examples/sensors/right_wrist_camera.py",
        "galbot_interface_examples/sensors/left_wrist_camera.py", 
        "galbot_interface_examples/sensors/front_head_camera.py",
        "galbot_interface_examples/basic/right_gripper.py",
        "galbot_interface_examples/basic/right_arm.py",
        "galbot_interface_examples/basic/leg.py",
        "galbot_interface_examples/basic/left_gripper.py",
        "galbot_interface_examples/basic/left_arm.py",
        "galbot_interface_examples/basic/head.py",
    ]
    
    fixed_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_file(file_path):
                fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main() 