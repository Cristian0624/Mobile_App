import re

def fix_camera_screen():
    with open('home.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find CameraScreen class
    camera_match = re.search(r'class\s+CameraScreen\(BaseScreen\):', content)
    if not camera_match:
        print("CameraScreen class not found")
        return
    
    # Find its update_theme method
    camera_start = camera_match.start()
    update_theme_match = re.search(r'def\s+update_theme\s*\(\s*self\s*,\s*\*args\s*\)\s*:', content[camera_start:])
    if not update_theme_match:
        print("update_theme method not found in CameraScreen")
        return
    
    # Get the method content
    method_start = camera_start + update_theme_match.start()
    next_def_match = re.search(r'def\s+', content[method_start + 10:])
    if next_def_match:
        method_end = method_start + 10 + next_def_match.start()
    else:
        method_end = len(content)
    
    # Create a new update_theme method without the form_bg_color reference
    new_method = """    def update_theme(self, *args):
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
"""
    
    # Replace the method in the content
    new_content = content[:method_start] + new_method + content[method_end:]
    
    # Save the fixed content
    with open('home.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed CameraScreen.update_theme method")

if __name__ == "__main__":
    fix_camera_screen() 