#!/usr/bin/env python3
import sys
import inspect
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

print("Sys path:", sys.path)
print("\nEventDispatcher exists in kivy.event:", EventDispatcher is not None)
print("BooleanProperty exists in kivy.properties:", BooleanProperty is not None)

# Check EventDispatcher methods
event_dispatcher = EventDispatcher()
print("\nEventDispatcher methods:")
for name, method in inspect.getmembers(event_dispatcher, inspect.ismethod):
    if name not in ['__init__']:
        print(f"- {name}")

# Try importing ThemeManager and check methods
print("\n--- Importing ThemeManager ---")
try:
    from theme_manager import ThemeManager
    tm = ThemeManager()
    print("ThemeManager successfully imported and instantiated")
    
    # Check ThemeManager methods
    print("\nThemeManager methods:")
    for name, method in inspect.getmembers(tm, inspect.ismethod):
        print(f"- {name}")
    
    # Check class hierarchy
    print("\nClass hierarchy:")
    for cls in ThemeManager.__mro__:
        print(f"- {cls.__name__}")
    
    # Check for bind method specifically
    has_bind = hasattr(tm, 'bind')
    print(f"\nThemeManager has bind method: {has_bind}")
    
    if has_bind:
        bind_method = getattr(tm, 'bind')
        print(f"Bind method: {bind_method}")
        
        # Try binding to a property
        def on_dark_mode_change(instance, value):
            print(f"Dark mode changed to: {value}")
        
        print("\nTrying to bind to is_dark_mode...")
        tm.bind(is_dark_mode=on_dark_mode_change)
        print("Binding successful")
        
        print("Changing is_dark_mode to True...")
        tm.is_dark_mode = True
    
except Exception as e:
    print(f"Error with ThemeManager: {e}")
    import traceback
    traceback.print_exc() 