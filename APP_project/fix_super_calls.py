import re

def fix_super_calls(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the PulsingMicButton super call
    pattern = r'super\(PulsingMicButton, self\).__init__\(\*\*kwargs\)'
    replacement = 'super().__init__(**kwargs)'
    content = re.sub(pattern, replacement, content)
    
    # Fix the ReminderScreen update_theme method's missing super call
    pattern = r'def update_theme\(self, \*args\):\s+"""Override to update specific UI elements"""\s+# First call parent\'s update_theme to handle basic elements\s+\n\s+# Get theme colors'
    replacement = 'def update_theme(self, *args):\n        """Override to update specific UI elements"""\n        # First call parent\'s update_theme to handle basic elements\n        super(ReminderScreen, self).update_theme(*args)\n        \n        # Get theme colors'
    content = re.sub(pattern, replacement, content)
    
    # Fix CameraScreen update_theme method
    pattern = r'super\(ReminderScreen, self\)\.update_theme\(\*args\)'
    replacement = 'super(CameraScreen, self).update_theme(*args)'
    content = re.sub(pattern, replacement, content)
    
    # Fix VoiceScreen update_theme method
    pattern = r'super\(ReminderScreen, self\)\.update_theme\(\*args\)'
    replacement = 'super(VoiceScreen, self).update_theme(*args)'
    content = re.sub(pattern, replacement, content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed super() calls in {file_path}")

if __name__ == "__main__":
    fix_super_calls("home.py") 