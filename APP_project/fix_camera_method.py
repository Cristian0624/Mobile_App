import re

def fix_camera_method():
    # Create the replacement method text
    replacement = '''    def update_theme(self, *args):
        """Update UI elements based on current theme"""
        # Call parent's update_theme to handle basic elements
        super(CameraScreen, self).update_theme(*args)
        
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update specific elements for this screen
        if hasattr(self, 'title_label'):
            self.title_label.color = colors['text']
        
        # Update all labels
        for child in self.walk(restrict=True):
            if isinstance(child, Label):
                child.color = colors['text']
            elif isinstance(child, Button) and not isinstance(child, RoundedButton):
                if child != self.back_button:
                    child.background_color = colors['button_bg']
                    child.color = colors['button_text']
        
        # Update background color
        with self.canvas.before:
            self.bg_color.rgba = colors['background']
'''
    
    # Read the file content
    with open('home.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the camera screen class
    camera_class_match = re.search(r'class\s+CameraScreen\(BaseScreen\):', content)
    if not camera_class_match:
        print("CameraScreen class not found")
        return
    
    camera_class_start = camera_class_match.start()
    
    # Find the update_theme method in the camera screen class
    method_match = re.search(r'def\s+update_theme\s*\(\s*self\s*,\s*\*args\s*\)\s*:', content[camera_class_start:])
    if not method_match:
        print("update_theme method not found in CameraScreen")
        return
    
    method_start = camera_class_start + method_match.start()
    
    # Find the end of the method (next method or class)
    method_end_match = re.search(r'(?:\n\s*def|\n\s*class)', content[method_start + 10:])
    if method_end_match:
        method_end = method_start + 10 + method_end_match.start()
    else:
        method_end = len(content)
    
    # Replace the method
    new_content = content[:method_start] + replacement + content[method_end:]
    
    # Write back to the file
    with open('home.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed CameraScreen.update_theme method")

if __name__ == "__main__":
    fix_camera_method() 