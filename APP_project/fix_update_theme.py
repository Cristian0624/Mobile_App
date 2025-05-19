#!/usr/bin/env python3

# This script fixes all update_theme methods that call super() incorrectly

with open('home.py', 'r') as file:
    lines = file.readlines()

# Line numbers to check
line_numbers = {
    'VoiceScreen': 1958,  # The super() call in VoiceScreen.update_theme
}

# Fix VoiceScreen
if "super(BaseScreen, self).update_theme" in lines[line_numbers['VoiceScreen']-1]:
    # Remove the entire line with the super() call
    lines.pop(line_numbers['VoiceScreen']-1)
    print(f"Removed super() call in VoiceScreen.update_theme")

# Check for any other super() calls in update_theme methods
fixed_count = 0
i = 0
while i < len(lines):
    # Look for "def update_theme" followed by super
    if i+1 < len(lines) and "def update_theme" in lines[i] and "super(" in lines[i+1]:
        # Make sure it's not the BaseScreen itself
        if "super(BaseScreen, self)" in lines[i+1] or "super(VoiceScreen, self)" in lines[i+1] or "super(CameraScreen, self)" in lines[i+1]:
            # Remove the super line
            print(f"Found and removing problematic super() call at line {i+2}")
            lines.pop(i+1)
            fixed_count += 1
            # Don't increment i since we removed a line
            continue
    i += 1

# Write the fixed file
with open('home.py', 'w') as file:
    file.writelines(lines)
print(f"Fixed {fixed_count+1} super() calls in update_theme methods")

def fix_base_screen_update_theme():
    """Fix the indentation issues in BaseScreen.update_theme method"""
    
    try:
        # Read the entire file
        with open('home.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for BaseScreen class
        base_screen_start = content.find('class BaseScreen(Screen):')
        if base_screen_start == -1:
            print("BaseScreen class not found")
            return False
        
        # Find the update_theme method within BaseScreen
        update_theme_start = content.find('def update_theme(self, *args):', base_screen_start)
        if update_theme_start == -1:
            print("update_theme method not found in BaseScreen")
            return False
        
        # Find the next method to determine the end of update_theme
        next_method = content.find('def ', update_theme_start + 10)
        if next_method == -1:
            print("Could not find end of update_theme method")
            return False
        
        # Extract the update_theme method
        original_method = content[update_theme_start:next_method]
        
        # Create a fixed version with proper indentation
        fixed_method = """    def update_theme(self, *args):
        \"\"\"Update UI elements based on current theme\"\"\"
        # Make sure we have a theme manager
        if not hasattr(self, 'theme_manager') or not self.theme_manager:
            self.theme_manager = ThemeManager()
            
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update background color
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['background']
        
        # Update back button colors based on theme
        if hasattr(self, 'back_button'):
            # Back button should match theme
            self.back_button.background_color = colors['button_bg']
            self.back_button.color = colors['button_text']
        
        # Recursively update all widgets with appropriate colors
        for child in self.walk(restrict=True):
            # Skip widgets that will be handled by more specific update methods
            if isinstance(child, (RoundedButton, IconButton)):
                continue
                
            # Update standard labels
            if isinstance(child, Label):
                # Different treatment for titles vs regular text
                if getattr(child, 'bold', False) and getattr(child, 'font_size', 0) > dp(18):
                    # This is likely a title - use primary color
                    child.color = colors.get('primary', colors['text'])
                else:
                    # Regular text
                    child.color = colors['text']
            
            # Update standard buttons
            elif isinstance(child, Button) and child != self.back_button:
                # Only update standard buttons, not custom ones
                if not any(isinstance(child, cls) for cls in [RoundedButton, IconButton]):
                    child.background_color = colors['button_bg']
                    child.color = colors['button_text']
            
            # Update text inputs
            elif isinstance(child, TextInput):
                child.background_color = colors['input_bg']
                child.foreground_color = colors['text']
                # Cursor should be visible on the background
                child.cursor_color = colors['primary']
        
        # Force canvas to redraw - helps with some widgets
        self.canvas.ask_update()
            
        # Schedule another update after a short delay to ensure everything updates
        # This helps catch elements that might be added dynamically
        Clock.schedule_once(lambda dt: self.canvas.ask_update(), 0.1)"""
        
        # Replace the original method with the fixed version
        new_content = content[:update_theme_start] + fixed_method + content[next_method:]
        
        # Write the fixed content back to the file
        with open('home.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Fixed BaseScreen.update_theme method")
        return True
        
    except Exception as e:
        print(f"Error fixing BaseScreen.update_theme: {e}")
        return False

if __name__ == "__main__":
    fix_base_screen_update_theme() 