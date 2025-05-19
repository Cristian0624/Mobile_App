#!/usr/bin/env python3

# This script finds and removes all problematic super() calls in update_theme methods

with open('home.py', 'r') as file:
    content = file.read()

# Find and replace all instances of super(BaseScreen, self).update_theme(*args)
fixed_content = content.replace('        super(BaseScreen, self).update_theme(*args)\n', '')

# Also fix other super calls in update_theme methods
fixed_content = fixed_content.replace('        super(ReminderScreen, self).update_theme(*args)\n', '')
fixed_content = fixed_content.replace('        super(CameraScreen, self).update_theme(*args)\n', '')
fixed_content = fixed_content.replace('        super(VoiceScreen, self).update_theme(*args)\n', '')
fixed_content = fixed_content.replace('        super(SettingsScreen, self).update_theme(*args)\n', '')

# Write the fixed file
with open('home.py', 'w') as file:
    file.write(fixed_content)

print("Fixed all problematic super() calls in update_theme methods") 