#!/usr/bin/env python3
import re
import os

def fix_home_screen_ui():
    """
    Improve the HomeScreen UI elements:
    1. Ensure consistent button styling across themes
    2. Fix theme change listeners
    3. Improve visual consistency
    """
    if not os.path.exists('home.py'):
        print("Error: home.py not found")
        return
    
    # Read the home.py file
    with open('home.py', 'r') as file:
        content = file.read()
    
    # Fix HomeScreen's update_theme method to properly handle theme changes
    home_update_theme_pattern = r'def update_theme\(self, \*args\):\s+"""Update colors based on current theme"""\s+# Call parent\'s update_theme.+?(?=def)'
    
    improved_update_theme = '''def update_theme(self, *args):
        """Update colors based on current theme"""
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update background colors
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['background']
        
        if hasattr(self, 'nav_bg_color'):
            self.nav_bg_color.rgba = colors['nav_bg']
            
        if hasattr(self, 'top_bg_color'):
            self.top_bg_color.rgba = colors['background']
        
        # Update welcome label
        if hasattr(self, 'welcome_label'):
            self.welcome_label.color = colors['text']
            
        if hasattr(self, 'username_label'):
            self.username_label.color = colors['primary']
            
        # Update navigation buttons
        for btn_name in ['home_btn', 'reminder_btn', 'camera_btn', 'voice_btn', 'settings_btn']:
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                if hasattr(btn, 'update_theme'):
                    btn.update_theme()
        
        # Ensure consistent button colors
        for child in self.main_layout.children:
            if hasattr(child, 'update_theme'):
                child.update_theme()
    
    def _update_rect(self, instance, value):
        """Update the background rectangle"""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
    
    def _update_nav_rect(self, instance, value):
        """Update the navigation bar rectangle"""
        if hasattr(self, 'nav_rect'):
            self.nav_rect.pos = instance.pos
            self.nav_rect.size = instance.size
    
    def _update_top_rect(self, instance, value):
        """Update the top bar rectangle"""
        if hasattr(self, 'top_rect'):
            self.top_rect.pos = instance.pos
            self.top_rect.size = instance.size
    '''
    
    # Replace the update_theme method in HomeScreen
    content = re.sub(home_update_theme_pattern, improved_update_theme, content, flags=re.DOTALL)
    
    # Fix IconButton update_theme method to ensure consistent colors
    icon_button_update_theme_pattern = r'def update_theme\(self, \*args\):\s+"""Update colors based on current theme""".+?(?=def on_press)'
    
    improved_icon_button_update_theme = '''def update_theme(self, *args):
        """Update colors based on current theme"""
        app = App.get_running_app()
        if not hasattr(app, 'theme_manager'):
            return
            
        colors = app.theme_manager.get_colors()
        is_dark = app.theme_manager.is_dark_mode
        
        # Update background color based on theme
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['button_bg']
            
        # Update text color based on theme
        if hasattr(self, 'label') and hasattr(self.label, 'color'):
            self.label.color = colors['button_text']
            
        # Update icon color based on theme
        if hasattr(self, 'icon_widget') and hasattr(self.icon_widget, 'update_canvas'):
            self.icon_widget.update_canvas()
    '''
    
    # Replace the IconButton update_theme method
    content = re.sub(icon_button_update_theme_pattern, improved_icon_button_update_theme, content, flags=re.DOTALL)
    
    # Write the updated content back to a new file
    with open('fix_home_ui.py.tmp', 'w') as file:
        file.write(content)
    
    print("Successfully created temporary file with HomeScreen UI improvements")
    
    # Now create a function to apply these changes
    with open('fix_home_ui.py.tmp', 'r') as file:
        tmp_content = file.read()
    
    # Replace the temporary file with a proper script
    with open('fix_home_ui.py', 'w') as file:
        file.write('''#!/usr/bin/env python3
import re
import os
import shutil

def fix_home_screen_ui():
    """
    Improve the HomeScreen UI elements:
    1. Ensure consistent button styling across themes
    2. Fix theme change listeners
    3. Improve visual consistency
    """
    if not os.path.exists('home.py'):
        print("Error: home.py not found")
        return
    
    # Make a backup of the original file
    backup_file = 'home.py.ui_backup'
    if not os.path.exists(backup_file):
        shutil.copy('home.py', backup_file)
        print(f"Created backup at {backup_file}")
    
    # Read the home.py file
    with open('home.py', 'r') as file:
        content = file.read()
    
    # Fix HomeScreen's update_theme method to properly handle theme changes
    home_update_theme_pattern = r'def update_theme\\(self, \\*args\\):\\s+"""Update colors based on current theme"""\\s+# Call parent\'s update_theme.+?(?=def)'
    
    improved_update_theme = """def update_theme(self, *args):
        \\"\\"\\"Update colors based on current theme\\"\\"\\"
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update background colors
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['background']
        
        if hasattr(self, 'nav_bg_color'):
            self.nav_bg_color.rgba = colors['nav_bg']
            
        if hasattr(self, 'top_bg_color'):
            self.top_bg_color.rgba = colors['background']
        
        # Update welcome label
        if hasattr(self, 'welcome_label'):
            self.welcome_label.color = colors['text']
            
        if hasattr(self, 'username_label'):
            self.username_label.color = colors['primary']
            
        # Update navigation buttons
        for btn_name in ['home_btn', 'reminder_btn', 'camera_btn', 'voice_btn', 'settings_btn']:
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                if hasattr(btn, 'update_theme'):
                    btn.update_theme()
        
        # Ensure consistent button colors
        for child in self.main_layout.children:
            if hasattr(child, 'update_theme'):
                child.update_theme()
    
    def _update_rect(self, instance, value):
        \\"\\"\\"Update the background rectangle\\"\\"\\"
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
    
    def _update_nav_rect(self, instance, value):
        \\"\\"\\"Update the navigation bar rectangle\\"\\"\\"
        if hasattr(self, 'nav_rect'):
            self.nav_rect.pos = instance.pos
            self.nav_rect.size = instance.size
    
    def _update_top_rect(self, instance, value):
        \\"\\"\\"Update the top bar rectangle\\"\\"\\"
        if hasattr(self, 'top_rect'):
            self.top_rect.pos = instance.pos
            self.top_rect.size = instance.size
    """
    
    # Replace the update_theme method in HomeScreen
    content = re.sub(home_update_theme_pattern, improved_update_theme, content, flags=re.DOTALL)
    
    # Fix IconButton update_theme method to ensure consistent colors
    icon_button_update_theme_pattern = r'def update_theme\\(self, \\*args\\):\\s+"""Update colors based on current theme""".+?(?=def on_press)'
    
    improved_icon_button_update_theme = """def update_theme(self, *args):
        \\"\\"\\"Update colors based on current theme\\"\\"\\"
        app = App.get_running_app()
        if not hasattr(app, 'theme_manager'):
            return
            
        colors = app.theme_manager.get_colors()
        is_dark = app.theme_manager.is_dark_mode
        
        # Update background color based on theme
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['button_bg']
            
        # Update text color based on theme
        if hasattr(self, 'label') and hasattr(self.label, 'color'):
            self.label.color = colors['button_text']
            
        # Update icon color based on theme
        if hasattr(self, 'icon_widget') and hasattr(self.icon_widget, 'update_canvas'):
            self.icon_widget.update_canvas()
    """
    
    # Replace the IconButton update_theme method
    content = re.sub(icon_button_update_theme_pattern, improved_icon_button_update_theme, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open('home.py', 'w') as file:
        file.write(content)
    
    print("Successfully updated home.py with UI improvements")

if __name__ == "__main__":
    fix_home_screen_ui()
''')
    
    # Clean up temporary file
    if os.path.exists('fix_home_ui.py.tmp'):
        os.remove('fix_home_ui.py.tmp')

if __name__ == "__main__":
    fix_home_screen_ui() 