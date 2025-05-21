#!/usr/bin/env python3

# This script extracts the CameraScreen and VoiceScreen classes from home.py.bak and adds them back to home.py

# Read backup file
with open('home.py.bak', 'r') as file:
    backup_lines = file.readlines()

# Find classes in the backup
camera_screen_start = None
camera_screen_end = None
voice_screen_start = None
voice_screen_end = None

# Find CameraScreen class
for i, line in enumerate(backup_lines):
    if line.strip() == 'class CameraScreen(BaseScreen):':
        camera_screen_start = i
        break

if camera_screen_start is None:
    print("Could not find CameraScreen class in backup file")
    exit(1)

# Find VoiceScreen class
for i, line in enumerate(backup_lines):
    if line.strip() == 'class VoiceScreen(BaseScreen):':
        voice_screen_start = i
        break

if voice_screen_start is None:
    print("Could not find VoiceScreen class in backup file")
    exit(1)

# Find the end of CameraScreen (start of VoiceScreen class)
camera_screen_end = voice_screen_start

# Find the end of VoiceScreen (next class definition)
for i in range(voice_screen_start + 1, len(backup_lines)):
    if backup_lines[i].startswith('class ') and 'VoiceScreen' not in backup_lines[i]:
        voice_screen_end = i
        break

# If we couldn't find the end, use the end of file
if voice_screen_end is None:
    voice_screen_end = len(backup_lines)

# Extract the classes
camera_screen_code = backup_lines[camera_screen_start:camera_screen_end]
voice_screen_code = backup_lines[voice_screen_start:voice_screen_end]

print(f"Extracted CameraScreen class: {len(camera_screen_code)} lines")
print(f"Extracted VoiceScreen class: {len(voice_screen_code)} lines")

# Read current home.py
with open('home.py', 'r') as file:
    current_lines = file.readlines()

# Find where to insert the classes
# We'll look for HomeScreen which should come after both classes
insert_position = None
for i, line in enumerate(current_lines):
    if 'class HomeScreen(Screen):' in line:
        insert_position = i
        break

if insert_position is None:
    print("Could not find appropriate insertion point for classes")
    exit(1)

print(f"Found insertion point at line {insert_position+1}")

# Add a blank line before the classes
current_lines.insert(insert_position, '\n')
insert_position += 1

# Insert the CameraScreen class
for line in camera_screen_code:
    current_lines.insert(insert_position, line)
    insert_position += 1

# Add a blank line between classes
current_lines.insert(insert_position, '\n')
insert_position += 1

# Insert the VoiceScreen class
for line in voice_screen_code:
    current_lines.insert(insert_position, line)
    insert_position += 1

# Write the updated file
with open('home.py', 'w') as file:
    file.writelines(current_lines)

print("Successfully restored CameraScreen and VoiceScreen classes to home.py") 