#!/usr/bin/env python3

def fix_settings_screen():
    """Fix the SettingsScreen class in home.py to properly handle theme_manager.bind"""
    
    try:
        with open('home.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the SettingsScreen class
        settings_start = content.find('class SettingsScreen(BaseScreen):')
        if settings_start == -1:
            print("SettingsScreen class not found in home.py")
            return False
        
        # Extract the SettingsScreen class
        next_class = content.find('class ', settings_start + 10)
        if next_class == -1:
            # If there's no class after SettingsScreen, take the rest of the file
            settings_content = content[settings_start:]
        else:
            settings_content = content[settings_start:next_class]
        
        # Fix the __init__ method to properly initialize and use ThemeManager
        if '__init__' in settings_content:
            # Replace the init method with a corrected version
            old_init_start = settings_content.find('    def __init__')
            old_init_end = settings_content.find('    def', old_init_start + 10)
            old_init = settings_content[old_init_start:old_init_end]
            
            # Create a new init method with proper theme_manager handling
            new_init = """    def __init__(self, **kwargs):
        # Initialize the base screen first
        super(SettingsScreen, self).__init__(auto_update_theme=False, **kwargs)

        # Make sure we have a theme manager
        from theme_manager import ThemeManager
        if not hasattr(self, 'theme_manager') or not self.theme_manager:
            self.theme_manager = ThemeManager()
        
        # Set up layout
        self.orientation = 'vertical'
        self.spacing = dp(20)
        self.padding = dp(20)
        
        # Add settings specific UI components here
        
        # Now bind to theme changes after everything is set up
        # This will connect our update_theme method to theme changes
        try:
            self.theme_manager.bind(is_dark_mode=self.update_theme)
        except Exception as e:
            print(f"Error binding theme_manager: {e}")
        
        # Update theme for initial rendering
        self.update_theme()
"""
            
            # Replace the old init with the new one
            settings_content = settings_content.replace(old_init, new_init)
        
        # Fix the update_theme method to handle errors gracefully
        if 'def update_theme' in settings_content:
            old_update_start = settings_content.find('    def update_theme')
            old_update_end = settings_content.find('    def', old_update_start + 10)
            if old_update_end == -1:
                old_update_end = len(settings_content)
            old_update = settings_content[old_update_start:old_update_end]
            
            # Create a new update_theme method with proper error handling
            new_update = """    def update_theme(self, *args):
        # Update theme colors for all widgets in this screen
        try:
            # Make sure we have a theme manager
            if not hasattr(self, 'theme_manager') or not self.theme_manager:
                from theme_manager import ThemeManager
                self.theme_manager = ThemeManager()

            # Get colors from theme
            colors = self.theme_manager.get_colors()
            is_dark = self.theme_manager.is_dark_mode
            
            # Set background color
            self.canvas.before.clear()
            with self.canvas.before:
                Color(*colors['background'])
                Rectangle(pos=self.pos, size=self.size)
            
            # Update setting labels if they exist
            if hasattr(self, 'setting_labels'):
                for label in self.setting_labels:
                    label.color = colors['text']
            
            # Update other widgets as needed
        except Exception as e:
            print(f"Error updating theme: {e}")
"""
            
            # Replace the old update_theme with the new one
            settings_content = settings_content.replace(old_update, new_update)
        
        # Replace the SettingsScreen class in the original content
        if next_class == -1:
            new_content = content[:settings_start] + settings_content
        else:
            new_content = content[:settings_start] + settings_content + content[next_class:]
        
        with open('home.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Fixed SettingsScreen class in home.py")
        return True
    
    except Exception as e:
        print(f"Error fixing SettingsScreen: {e}")
        return False

if __name__ == "__main__":
    fix_settings_screen() 