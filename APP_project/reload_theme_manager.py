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
        '__pycache__',
        'theme_manager/__pycache__' if os.path.isdir('theme_manager') else None
    ]
    
    for pycache in pycache_dirs:
        if pycache and os.path.isdir(pycache):
            print(f"Removing {pycache} directory")
            shutil.rmtree(pycache)
    
    pyc_files = [
        'theme_manager.pyc',
        os.path.join('__pycache__', 'theme_manager.cpython-*.pyc')
    ]
    
    for pattern in pyc_files:
        import glob
        for file in glob.glob(pattern):
            print(f"Removing {file}")
            os.remove(file)
    
    # Force Python to reload the module if already imported
    if 'theme_manager' in sys.modules:
        print("ThemeManager already imported, reloading...")
        try:
            # Force reload the module
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
            theme_manager.ThemeManager.__bases__ = (EventDispatcher,)
            print("Fixed ThemeManager inheritance. EventDispatcher is now in the bases.")
            
            # Verify fix
            tm = theme_manager.ThemeManager()
            print(f"Fixed ThemeManager has bind method: {hasattr(tm, 'bind')}")
        
        print("ThemeManager verification complete.")
        
    except Exception as e:
        print(f"Error verifying ThemeManager: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reload_theme_manager() 