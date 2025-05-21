#!/usr/bin/env python3

"""
This script fixes the duplicate methods in home.py by removing the duplicate
_update_language and update_theme methods that were incorrectly placed in the 
ReminderScreen class.
"""

import os

def fix_home_py():
    # Define the file path
    file_path = 'home.py'
    
    # Make a backup
    backup_path = f"{file_path}.bak"
    os.system(f"cp {file_path} {backup_path}")
    print(f"Created backup at {backup_path}")
    
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.readlines()
    
    # Define the start and end lines of the duplicate methods to remove
    # These are the _update_language and update_theme methods that don't belong in ReminderScreen
    start_line = 1955  # Line number (0-based) where the duplicate _update_language starts
    end_line = 1996    # Line number (0-based) where the duplicate update_theme ends
    
    # Remove the duplicate methods
    new_content = content[:start_line] + content[end_line:]
    
    # Write the modified content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_content)
    
    print(f"Fixed {file_path}: Removed duplicate methods (lines {start_line+1}-{end_line+1})")

if __name__ == "__main__":
    fix_home_py() 