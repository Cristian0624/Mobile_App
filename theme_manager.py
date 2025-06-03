from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.event import EventDispatcher
from kivy.app import App

class ThemeManager(EventDispatcher):
    """
    Manages theme settings for the application including dark/light mode and colors.
    Implemented as a singleton to ensure consistent theming across the app.
    """
    # Define the property at class level
    is_dark_mode = BooleanProperty(False)
    
    _instance = None
    _updating = False
    
    def __new__(cls):
        if cls._instance is None:
            # Create the instance
            cls._instance = super(ThemeManager, cls).__new__(cls)
            
            # Initialize EventDispatcher explicitly
            EventDispatcher.__init__(cls._instance)
            
            # Define color palettes for light and dark modes
            cls._instance.light_colors = {
                'background': (0.98, 0.98, 0.98, 1),  # Light gray background
                'text': (0.2, 0.2, 0.2, 1),  # Dark text
                'text_secondary': (0.5, 0.5, 0.5, 1),  # Secondary text
                'primary': (0.2, 0.4, 0.8, 1),  # Primary blue
                'secondary': (0.1, 0.7, 0.3, 1),  # Secondary green
                'button_bg': (0.95, 0.95, 0.95, 1),  # Light button background
                'button_text': (0.2, 0.2, 0.2, 1),  # Dark button text
                'nav_bg': (0.98, 0.98, 0.98, 1),  # Light navigation background
                'input_bg': (0.95, 0.95, 0.95, 1),  # Light input background
                'error': (0.8, 0.2, 0.2, 1)  # Error red
            }
            
            cls._instance.dark_colors = {
                'background': (0.12, 0.12, 0.14, 1),  # Dark background
                'text': (0.9, 0.9, 0.9, 1),  # Light text
                'text_secondary': (0.7, 0.7, 0.7, 1),  # Secondary text
                'primary': (0.3, 0.5, 0.9, 1),  # Primary blue
                'secondary': (0.2, 0.8, 0.4, 1),  # Secondary green
                'button_bg': (0.2, 0.2, 0.22, 1),  # Dark button background
                'button_text': (0.9, 0.9, 0.9, 1),  # Light button text
                'nav_bg': (0.15, 0.15, 0.17, 1),  # Dark navigation background
                'input_bg': (0.2, 0.2, 0.22, 1),  # Dark input background
                'error': (0.9, 0.3, 0.3, 1)  # Error red
            }
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            # Initialize EventDispatcher explicitly
            EventDispatcher.__init__(self)
            self.initialized = True
            self._setup_colors()
    
    # Make sure bind method is defined
    def bind(self, **kwargs):
        """Bind callbacks to events"""
        for event_name, callback in kwargs.items():
            super(ThemeManager, self).bind(**{event_name: callback})
    
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
            'card_bg': [0.95, 0.95, 1, 1],  # Very light blue for cards
            'error': [0.8, 0.2, 0.2, 1]  # Red for error messages
        }
        
        # Dark theme colors - much darker to create contrast
        self.dark_colors = {
            'background': [0.12, 0.12, 0.14, 1],
            'text': [0.9, 0.9, 0.9, 1],
            'text_secondary': [0.7, 0.7, 0.7, 1],
            'primary': [0.3, 0.5, 0.9, 1],
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
            'card_bg': [0.15, 0.15, 0.2, 1],  # Dark blue-gray for cards
            'error': [0.9, 0.3, 0.3, 1]  # Red for error messages
        }
    
    def get_colors(self):
        """Return the current theme colors"""
        return self.dark_colors if self.is_dark_mode else self.light_colors
    
    def set_dark_mode(self, value):
        """Set dark mode and trigger theme updates"""
        if self._updating:
            return
            
        if self.is_dark_mode != value:
            self._updating = True
            try:
                self.is_dark_mode = value
                app = App.get_running_app()
                if app and hasattr(app, 'screen_manager'):
                    for screen_name in app.screen_manager.screen_names:
                        screen = app.screen_manager.get_screen(screen_name)
                        if hasattr(screen, 'update_theme'):
                            screen.update_theme()
                    if hasattr(app, 'update_theme'):
                        app.update_theme()
            finally:
                self._updating = False
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.set_dark_mode(not self.is_dark_mode)
        return self.is_dark_mode
    
    def get_accent_color(self):
        """Get accent color based on current theme"""
        return self.get_colors()['accent']
    
    def get_primary_color(self):
        """Get primary color based on current theme"""
        return self.get_colors()['primary']
