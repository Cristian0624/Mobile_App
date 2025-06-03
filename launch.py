#!/usr/bin/env python3
import importlib
import sys
import os
import shutil

def reload_theme_manager():
    """Force reload of ThemeManager and clear any Python cache issues"""
    
    print("Reloading ThemeManager module...")
    
    # Clear __pycache__ directory and .pyc files for theme_manager
    pycache_dirs = [
        '__pycache__'
    ]
    
    for pycache in pycache_dirs:
        if os.path.isdir(pycache):
            print(f"Removing {pycache} directory")
            try:
                shutil.rmtree(pycache)
            except:
                print(f"Could not remove {pycache}")
    
    # Force Python to reload the module if already imported
    if 'theme_manager' in sys.modules:
        print("ThemeManager already imported, reloading...")
        try:
            importlib.reload(sys.modules['theme_manager'])
            print("ThemeManager module reloaded successfully")
        except Exception as e:
            print(f"Error reloading ThemeManager: {e}")
    
    # Verify the ThemeManager class
    try:
        # Import the module
        import theme_manager
        
        # Make sure we have the latest version of the class
        importlib.reload(theme_manager)
        
        # Create a ThemeManager instance
        tm = theme_manager.ThemeManager()
        
        # Check if bind method exists
        has_bind = hasattr(tm, 'bind')
        print(f"Reloaded ThemeManager has bind method: {has_bind}")
        
        if not has_bind:
            print("WARNING: ThemeManager still doesn't have 'bind' method!")
            
            # Fix the ThemeManager class directly
            from kivy.event import EventDispatcher
            from kivy.properties import BooleanProperty
            
            # Create a new ThemeManager class with proper inheritance
            class FixedThemeManager(EventDispatcher):
                # Define properties
                is_dark_mode = BooleanProperty(False)
                _instance = None
                _updating = False
                
                def __new__(cls):
                    if cls._instance is None:
                        cls._instance = super(FixedThemeManager, cls).__new__(cls)
                    return cls._instance
                
                def __init__(self):
                    if not hasattr(self, 'initialized'):
                        # Initialize EventDispatcher
                        EventDispatcher.__init__(self)
                        self.initialized = True
                        self._setup_colors()
                
                def _setup_colors(self):
                    # Copy from original ThemeManager
                    self.light_colors = tm.light_colors
                    self.dark_colors = tm.dark_colors
                
                def get_colors(self):
                    return self.dark_colors if self.is_dark_mode else self.light_colors
                
                def set_dark_mode(self, value):
                    # Copy functionality from original
                    if self._updating:
                        return
                    
                    if self.is_dark_mode != value:
                        self._updating = True
                        try:
                            self.is_dark_mode = value
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
            
            # Replace the original ThemeManager with our fixed version
            theme_manager.ThemeManager = FixedThemeManager
            print("Replaced ThemeManager with fixed version.")
            
            # Verify fix
            tm = theme_manager.ThemeManager()
            print(f"Fixed ThemeManager has bind method: {hasattr(tm, 'bind')}")
        
        # At this point we should have a working ThemeManager with bind method
        
        # Test binding to is_dark_mode property
        def on_theme_change(instance, value):
            print(f"Theme changed to dark mode: {value}")
        
        print("Testing binding to is_dark_mode...")
        tm.bind(is_dark_mode=on_theme_change)
        print("Binding successful!")
        
        # Apply a dummy change to verify binding works
        tm.is_dark_mode = not tm.is_dark_mode
        
    except Exception as e:
        print(f"Error verifying ThemeManager: {e}")
        import traceback
        traceback.print_exc()

print("Running launch.py - preparing environment before main.py")
reload_theme_manager()

print("\nStarting main.py...")
import main 