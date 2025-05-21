#!/usr/bin/env python3

# This script fixes the frequency spinner code in home.py by removing problematic bindings

with open('home.py', 'r') as file:
    lines = file.readlines()

# Find and remove all instances of the problematic code
i = 0
lines_removed = 0
while i < len(lines):
    if "def update_spinner_text(*args):" in lines[i]:
        print(f"Found update_spinner_text function at line {i+1}")
        # Remove 3 lines: function definition, body, and binding
        del lines[i:i+3]
        lines_removed += 3
        # Don't increment i since we deleted lines
    else:
        i += 1

if lines_removed > 0:
    # Write fixed file
    with open('home.py', 'w') as file:
        file.writelines(lines)
    print(f"Fixed home.py file written, removed {lines_removed} lines")
else:
    print("Could not find any update_spinner_text functions") 