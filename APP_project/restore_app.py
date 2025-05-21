#!/usr/bin/env python3
import os
import shutil

def restore_app():
    """Restore app functionality by copying home_fixed.py to home.py"""
    try:
        # Check if home_fixed.py exists
        if not os.path.exists('home_fixed.py'):
            print("Error: home_fixed.py not found")
            return False
        
        # Create a backup of current home.py if it exists
        if os.path.exists('home.py'):
            backup_name = 'home.py.bak'
            count = 1
            while os.path.exists(backup_name):
                backup_name = f'home.py.bak{count}'
                count += 1
            
            shutil.copy2('home.py', backup_name)
            print(f"Created backup of current home.py as {backup_name}")
        
        # Copy home_fixed.py to home.py
        shutil.copy2('home_fixed.py', 'home.py')
        print("Successfully restored app functionality by copying home_fixed.py to home.py")
        
        # Add theme_manager.py if it doesn't exist
        if not os.path.exists('theme_manager.py'):
            create_theme_manager()
            print("Created theme_manager.py")
        
        # Add language_manager.py if it doesn't exist
        if not os.path.exists('language_manager.py'):
            create_language_manager()
            print("Created language_manager.py")
        
        return True
    except Exception as e:
        print(f"Error restoring app: {e}")
        return False

def create_theme_manager():
    """Create theme_manager.py file with necessary code"""
    content = """from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.event import EventDispatcher
from kivy.app import App

class ThemeManager(EventDispatcher):
    \"\"\"
    Manages theme settings for the application including dark/light mode and colors.
    Implemented as a singleton to ensure consistent theming across the app.
    \"\"\"
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
                'background': (1, 1, 1, 1),
                'text': (0.2, 0.2, 0.2, 1),
                'text_secondary': (0.5, 0.5, 0.5, 1),
                'primary': (0.2, 0.4, 0.8, 1),
                'secondary': (0.1, 0.7, 0.3, 1),
                'button_bg': (0.95, 0.95, 0.95, 1),
                'button_text': (0.2, 0.2, 0.2, 1),
                'nav_bg': (0.98, 0.98, 0.98, 1),
                'input_bg': (0.95, 0.95, 0.95, 1),
                'error': (0.8, 0.2, 0.2, 1)
            }
            
            cls._instance.dark_colors = {
                'background': (0.12, 0.12, 0.14, 1),
                'text': (0.9, 0.9, 0.9, 1),
                'text_secondary': (0.7, 0.7, 0.7, 1),
                'primary': (0.3, 0.5, 0.9, 1),
                'secondary': (0.2, 0.8, 0.4, 1),
                'button_bg': (0.2, 0.2, 0.22, 1),
                'button_text': (0.9, 0.9, 0.9, 1),
                'nav_bg': (0.15, 0.15, 0.17, 1),
                'input_bg': (0.2, 0.2, 0.22, 1),
                'error': (0.9, 0.3, 0.3, 1)
            }
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            # Initialize EventDispatcher explicitly
            EventDispatcher.__init__(self)
            self.initialized = True
            self._setup_colors()
    
    def bind(self, **kwargs):
        \"\"\"Bind callbacks to events\"\"\"
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
        \"\"\"Get the current theme colors based on mode\"\"\"
        return self.dark_colors if self.is_dark_mode else self.light_colors
    
    def set_dark_mode(self, is_dark):
        \"\"\"Set the theme to dark or light mode\"\"\"
        self.is_dark_mode = is_dark
    
    def get_button_color(self):
        \"\"\"Get the button background color for current theme\"\"\"
        return self.dark_colors['button_bg'] if self.is_dark_mode else self.light_colors['button_bg']
    
    def get_button_text_color(self):
        \"\"\"Get the button text color for current theme\"\"\"
        return self.dark_colors['button_text'] if self.is_dark_mode else self.light_colors['button_text']
    
    def get_accent_color(self):
        \"\"\"Get an accent color for highlight elements\"\"\"
        return (0.4, 0.6, 0.9, 1) if self.is_dark_mode else (0.2, 0.4, 0.8, 1)
"""
    with open('theme_manager.py', 'w') as f:
        f.write(content)

def create_language_manager():
    """Create language_manager.py file with necessary code"""
    content = """from kivy.event import EventDispatcher
from kivy.properties import StringProperty

# Dictionary of supported languages
SUPPORTED_LANGUAGES = ['en', 'ro', 'ru']

# Global current language
CURRENT_LANGUAGE = {'lang': 'en'}

class LanguageManager(EventDispatcher):
    \"\"\"
    Manages language settings for the application.
    Implemented as a singleton to ensure consistent language across the app.
    \"\"\"
    _instance = None
    current_language = StringProperty('en')  # Default to English
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            EventDispatcher.__init__(cls._instance)
            cls._instance.current_language = CURRENT_LANGUAGE['lang']
        return cls._instance
    
    def __init__(self):
        \"\"\"Initialize language manager\"\"\"
        # This will only be called once due to the singleton pattern
        if not hasattr(self, 'is_initialized'):
            self.is_initialized = True
    
    def set_language(self, lang_code):
        \"\"\"Set the current language\"\"\"
        if lang_code in SUPPORTED_LANGUAGES:
            # Update global language
            CURRENT_LANGUAGE['lang'] = lang_code
            # Update instance language - this triggers bindings
            self.current_language = lang_code
    
    def get_language(self):
        \"\"\"Get the current language code\"\"\"
        return self.current_language
    
    def get_text(self, key):
        \"\"\"Get translated text for a key\"\"\"
        from home import LANG_DICT
        lang = self.current_language
        
        if lang in LANG_DICT and key in LANG_DICT[lang]:
            return LANG_DICT[lang][key]
        
        # Fallback to English
        if 'en' in LANG_DICT and key in LANG_DICT['en']:
            return LANG_DICT['en'][key]
        
        # Return the key itself if not found
        return key
"""
    with open('language_manager.py', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    restore_app()
    print("App restoration complete. You can now run your app.") 