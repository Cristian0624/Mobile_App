#!/usr/bin/env python3

# This script removes problematic super() calls in the update_theme methods

with open('home.py', 'r') as file:
    lines = file.readlines()

# Fix VoiceScreen
voice_line = 2966  # Line with the VoiceScreen super() call
if "super(BaseScreen, self).update_theme" in lines[voice_line-1]:
    # Remove the line completely
    lines.pop(voice_line-1)
    print(f"Removed VoiceScreen super() call on line {voice_line}")
else:
    print(f"Line {voice_line} does not contain the expected super() call")

# Fix CameraScreen
camera_lines = [2452, 2596]  # Lines with the CameraScreen super() calls
for line_number in camera_lines:
    if line_number < len(lines) and "super(CameraScreen, self).update_theme" in lines[line_number-1]:
        # Replace problematic super() call
        lines[line_number-1] = lines[line_number-1].replace("super(CameraScreen, self).update_theme", "# super() call removed")
        print(f"Fixed CameraScreen super() call on line {line_number}")
    else:
        print(f"Line {line_number} does not contain the expected super() call")

# Write fixed file
with open('home.py', 'w') as file:
    file.writelines(lines)
print("Fixed home.py file written") 