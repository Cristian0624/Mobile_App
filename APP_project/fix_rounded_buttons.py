#!/usr/bin/env python3
import re
import os
import shutil

def fix_rounded_buttons():
    """
    Improve the RoundedButton class to ensure consistent styling:
    1. Add proper theme handling
    2. Ensure consistent corner radius
    3. Fix color transitions when pressed
    """
    if not os.path.exists('home.py'):
        print("Error: home.py not found")
        return
    
    # Make a backup of the original file
    backup_file = 'home.py.buttons_backup'
    if not os.path.exists(backup_file):
        shutil.copy('home.py', backup_file)
        print(f"Created backup at {backup_file}")
    
    # Read the home.py file
    with open('home.py', 'r') as file:
        content = file.read()
    
    # Find the RoundedButton class
    rounded_button_pattern = r'class RoundedButton\(Button\):.*?def __init__\(self, \*\*kwargs\):.*?def on_release\(self\):.*?(?=\n\n)'
    
    # Create an improved RoundedButton class with better theme handling
    improved_rounded_button = '''class RoundedButton(Button):
    def __init__(self, **kwargs):
        # Extract our custom properties before passing to the parent class
        self.corner_radius = kwargs.pop('corner_radius', dp(10))
        self.bg_color = kwargs.pop('bg_color', (0.2, 0.6, 0.9, 1))  # Default blue
        self.pressed_bg_color = kwargs.pop('pressed_bg_color', None)  # Will be calculated if None
        
        # Set up default button properties
        kwargs['background_normal'] = ''
        kwargs['background_color'] = (0, 0, 0, 0)  # Transparent
        kwargs['background_down'] = ''
        kwargs['border'] = (0, 0, 0, 0)
        
        super(RoundedButton, self).__init__(**kwargs)
        
        # Calculate pressed color if not provided (30% darker)
        if self.pressed_bg_color is None:
            self.pressed_bg_color = [max(0, c * 0.7) for c in self.bg_color[:3]] + [self.bg_color[3]]
        
        # Set up the canvas
        with self.canvas.before:
            self.bg_color_obj = Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=[self.corner_radius]
            )
        
        # Bind to size and pos changes
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        
    def _update_canvas(self, *args):
        """Update the button's canvas"""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
    
    def on_press(self):
        """Change background color when pressed"""
        if hasattr(self, 'bg_color_obj'):
            self.bg_color_obj.rgba = self.pressed_bg_color
    
    def on_release(self):
        """Restore original background color"""
        if hasattr(self, 'bg_color_obj'):
            self.bg_color_obj.rgba = self.bg_color
            
    def update_theme(self, *args):
        """Update button colors based on theme"""
        app = App.get_running_app()
        if not hasattr(app, 'theme_manager'):
            return
            
        # Get theme colors
        colors = app.theme_manager.get_colors()
        is_dark = app.theme_manager.is_dark_mode
        
        # Only update colors if they're not custom (check if they match theme colors)
        if self.bg_color == (0.2, 0.6, 0.9, 1):  # Default blue
            self.bg_color = colors['primary']
            self.pressed_bg_color = [max(0, c * 0.7) for c in self.bg_color[:3]] + [self.bg_color[3]]
            
            if hasattr(self, 'bg_color_obj'):
                self.bg_color_obj.rgba = self.bg_color'''
    
    # Replace the RoundedButton class
    content = re.sub(rounded_button_pattern, improved_rounded_button, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open('home.py', 'w') as file:
        file.write(content)
    
    print("Successfully updated RoundedButton class with improved styling")

if __name__ == "__main__":
    fix_rounded_buttons() 