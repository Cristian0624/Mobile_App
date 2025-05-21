#!/usr/bin/env python3

# This script performs a targeted fix to remove the problematic line

with open('home.py', 'r') as file:
    content = file.read()

# Replace the problematic super() line, being very precise with the pattern
fixed_content = content.replace('        super(BaseScreen, self).update_theme(*args)\n', '')

# Write the fixed file
with open('home.py', 'w') as file:
    file.write(fixed_content)

print("Fixed problematic super() calls") 