#!/usr/bin/env python3

def fix_theme_manager():
    """Fix ThemeManager class in theme_manager.py to properly inherit from EventDispatcher"""
    with open('theme_manager.py', 'w') as f:
        f.write("""from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.event import EventDispatcher
from kivy.app import App

class ThemeManager(EventDispatcher):
    # Define is_dark_mode BEFORE __new__ to ensure property registration
    is_dark_mode = BooleanProperty(False)
    _instance = None
    _updating = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            # It's critical to call EventDispatcher.__init__ explicitly
            EventDispatcher.__init__(self)
            self.initialized = True
            self._setup_colors()
    
    def _setup_colors(self):
        # Light theme colors - more saturated
        self.light_colors = {
            'background': [1, 1, 1, 1],  # White
            'text': [0.1, 0.1, 0.1, 1],  # Dark gray
            'text_secondary': [0.4, 0.4, 0.4, 1],  # Medium gray for secondary text
            'primary': [0.2, 0.6, 1, 1],  # Blue
            'secondary': [0.8, 0.8, 0.8, 1],  # Light Gray
            'input_bg': [0.95, 0.95, 0.95, 1],  # Very Light Gray
            'button_bg': [0.85, 0.85, 0.85, 1],  # Light grey for all buttons
            'button_text': [0.1, 0.1, 0.1, 1],  # Dark text for buttons
            'nav_bg': [0.95, 0.95, 0.95, 1],  # Light Gray for navigation
            'accent': [0.2, 0.7, 0.3, 1],  # Green accent
            'card_bg': [0.95, 0.95, 1, 1]  # Very light blue for cards
        }
        
        # Dark theme colors - much darker to create contrast
        self.dark_colors = {
            'background': [0.08, 0.08, 0.1, 1],  # Very Dark Gray/Black
            'text': [0.95, 0.95, 0.95, 1],  # Almost White
            'text_secondary': [0.7, 0.7, 0.7, 1],  # Light gray for secondary text
            'primary': [0.3, 0.7, 1, 1],  # Brighter Blue
            'secondary': [0.25, 0.25, 0.25, 1],  # Dark Gray
            'input_bg': [0.15, 0.15, 0.15, 1],  # Very Dark Gray
            'button_bg': [0.18, 0.18, 0.2, 1],  # Darker grey for all buttons
            'button_text': [0.95, 0.95, 0.95, 1],  # White text for buttons
            'nav_bg': [0.12, 0.12, 0.15, 1],  # Very Dark Gray for navigation
            'accent': [0.3, 0.8, 0.4, 1],  # Brighter Green accent
            'card_bg': [0.15, 0.15, 0.2, 1]  # Dark blue-gray for cards
        }
    
    def get_colors(self):
        return self.dark_colors if self.is_dark_mode else self.light_colors
    
    def set_dark_mode(self, value):
        # Prevent recursive updates
        if self._updating:
            return
        
        # Only update if the value is different
        if self.is_dark_mode != value:
            self._updating = True
            try:
                # Set the value - this will trigger property observers
                self.is_dark_mode = value
                
                # Manually update all screens
                app = App.get_running_app()
                if app and hasattr(app, 'screen_manager'):
                    # Force update all screens
                    for screen_name in app.screen_manager.screen_names:
                        screen = app.screen_manager.get_screen(screen_name)
                        if hasattr(screen, 'update_theme'):
                            screen.update_theme()
                    
                    # Update the window background
                    if hasattr(app, 'update_theme'):
                        app.update_theme()
            finally:
                self._updating = False
    
    def toggle_theme(self):
        self.set_dark_mode(not self.is_dark_mode)
        return self.is_dark_mode
    
    def get_button_color(self):
        return self.get_colors()['button_bg']
    
    def get_button_text_color(self):
        return self.get_colors()['button_text']
    
    def get_accent_color(self):
        return self.get_colors()['accent']
""")
    print("ThemeManager class has been completely replaced with a fixed version")

if __name__ == "__main__":
    fix_theme_manager() 