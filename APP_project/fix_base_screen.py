#!/usr/bin/env python3

def fix_base_screen():
    """Fix the BaseScreen class in home.py to properly handle theme_manager.bind"""
    
    try:
        with open('home.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get the position of BaseScreen class
        base_screen_start = content.find('class BaseScreen(Screen):')
        if base_screen_start == -1:
            print("BaseScreen class not found in home.py")
            return False
        
        # Extract the BaseScreen class
        next_class = content.find('class ', base_screen_start + 10)
        base_screen_content = content[base_screen_start:next_class]
        
        # Fix the __init__ method
        fixed_content = base_screen_content.replace(
            "    def __init__(self, auto_update_theme=True, **kwargs):",
            """    def __init__(self, auto_update_theme=True, **kwargs):
        # Initialize Screen first
        super(BaseScreen, self).__init__(**kwargs)
        
        # Initialize theme manager
        from theme_manager import ThemeManager
        self.theme_manager = ThemeManager()"""
        )
        
        # Replace the old content with the fixed content
        new_content = content[:base_screen_start] + fixed_content + content[next_class:]
        
        # Also ensure ThemeManager is imported at the top
        if "from theme_manager import ThemeManager" not in content[:base_screen_start]:
            import_line = "from theme_manager import ThemeManager\n"
            # Find a good place to add the import (after other imports)
            last_import = content[:base_screen_start].rfind("import ")
            last_import_end = content[:base_screen_start].find("\n", last_import)
            new_content = content[:last_import_end+1] + import_line + content[last_import_end+1:]
        
        with open('home.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Fixed BaseScreen class in home.py")
        return True
    
    except Exception as e:
        print(f"Error fixing BaseScreen: {e}")
        return False

if __name__ == "__main__":
    fix_base_screen() 