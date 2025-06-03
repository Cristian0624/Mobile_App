from kivy.event import EventDispatcher
from kivy.properties import StringProperty

# Dictionary of supported languages
SUPPORTED_LANGUAGES = ['en', 'ro', 'ru']

# Global current language
CURRENT_LANGUAGE = {'lang': 'en'}

class LanguageManager(EventDispatcher):
    """
    Manages language settings for the application.
    Implemented as a singleton to ensure consistent language across the app.
    """
    _instance = None
    current_language = StringProperty('en')  # Default to English
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            EventDispatcher.__init__(cls._instance)
            cls._instance.current_language = CURRENT_LANGUAGE['lang']
        return cls._instance
    
    def __init__(self):
        """Initialize language manager"""
        # This will only be called once due to the singleton pattern
        if not hasattr(self, 'is_initialized'):
            self.is_initialized = True
    
    def set_language(self, lang_code):
        """Set the current language"""
        if lang_code in SUPPORTED_LANGUAGES:
            # Update global language
            CURRENT_LANGUAGE['lang'] = lang_code
            # Update instance language - this triggers bindings
            self.current_language = lang_code
    
    def get_language(self):
        """Get the current language code"""
        return self.current_language
    
    def get_text(self, key):
        """Get translated text for a key"""
        from home import LANG_DICT
        lang = self.current_language
        
        if lang in LANG_DICT and key in LANG_DICT[lang]:
            return LANG_DICT[lang][key]
        
        # Fallback to English
        if 'en' in LANG_DICT and key in LANG_DICT['en']:
            return LANG_DICT['en'][key]
        
        # Return the key itself if not found
        return key
        
    def register_event_type(self, event_type):
        """Register an event type"""
        EventDispatcher.register_event_type(self, event_type)
    
    def bind(self, **kwargs):
        """Bind callbacks to events"""
        EventDispatcher.bind(self, **kwargs)
        
    def dispatch(self, event_type, *args):
        """Dispatch an event"""
        EventDispatcher.dispatch(self, event_type, *args) 