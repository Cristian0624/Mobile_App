import re

def fix_screen_update_methods(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all screen classes
    screen_classes = [
        'BaseScreen', 'ReminderScreen', 'CameraScreen', 'VoiceScreen', 
        'HomeScreen', 'SettingsScreen'
    ]
    
    for screen_class in screen_classes:
        # Find the class definition
        class_match = re.search(r'class\s+' + screen_class + r'\(', content)
        if not class_match:
            print(f"{screen_class} class not found")
            continue
        
        class_start = class_match.start()
        
        # Find the next class to determine where this class ends
        next_class_match = re.search(r'class\s+', content[class_start + 10:])
        if next_class_match:
            class_end = class_start + 10 + next_class_match.start()
        else:
            class_end = len(content)
        
        class_content = content[class_start:class_end]
        
        # Find all update_theme methods in this class
        update_theme_matches = list(re.finditer(r'(?:^|\n)\s*def\s+update_theme\s*\(\s*self\s*,\s*\*args\s*\)\s*:', class_content))
        
        if len(update_theme_matches) == 0:
            print(f"No update_theme method found in {screen_class}")
            continue
        
        if len(update_theme_matches) > 1:
            print(f"Found {len(update_theme_matches)} update_theme methods in {screen_class}, fixing...")
            
            # Keep only the first update_theme method
            first_match = update_theme_matches[0]
            first_match_start = class_start + first_match.start()
            
            # Find the end of the first method (start of next method)
            next_method_match = re.search(r'(?:\n\s*def|\n\s*class)', class_content[first_match.end():update_theme_matches[1].start()])
            if next_method_match:
                first_match_end = class_start + first_match.end() + next_method_match.start()
            else:
                first_match_end = class_start + update_theme_matches[1].start()
            
            # Create a fixed class content without duplicate methods
            new_class_content = class_content[:first_match.end()]
            
            # Extract properly indented method body from the first method
            method_body = content[first_match_start:first_match_end]
            
            # Check if the method is properly indented, if not fix it
            if not re.match(r'^\s{4}def', method_body):
                # Fix indentation by ensuring 4 spaces before 'def'
                method_body = re.sub(r'^(\s*)def', r'    def', method_body)
                
                # Also fix the docstring and method body indentation if needed
                method_body = re.sub(r'\n(\s*)"""', r'\n        """', method_body)
                method_body = re.sub(r'\n(\s*)(?!def|class|\s*def|\s*class)', r'\n        ', method_body)
            
            # Make sure the super call uses the correct class name
            method_body = method_body.replace(f'super({screen_class}, self)', f'super({screen_class}, self)')
            
            # Add the fixed method body
            new_class_content += method_body
            
            # Add everything after the last update_theme method
            last_match = update_theme_matches[-1]
            last_match_end = last_match.end()
            
            # Find the end of the last method (start of next method)
            next_method_match = re.search(r'(?:\n\s*def|\n\s*class)', class_content[last_match_end:])
            if next_method_match:
                last_method_end = last_match_end + next_method_match.start()
            else:
                last_method_end = len(class_content)
            
            new_class_content += class_content[last_method_end:]
            
            # Replace the old class content with the new one
            content = content[:class_start] + new_class_content + content[class_end:]
        
        # Check indentation for the remaining method
        else:
            match = update_theme_matches[0]
            method_start = class_start + match.start()
            
            # Find where the method ends
            next_method_match = re.search(r'(?:\n\s*def|\n\s*class)', class_content[match.end():])
            if next_method_match:
                method_end = class_start + match.end() + next_method_match.start()
            else:
                method_end = class_end
            
            method_body = content[method_start:method_end]
            
            # Check if the method is properly indented
            if not re.match(r'^\s{4}def', method_body):
                # Fix indentation
                fixed_method = re.sub(r'^(\s*)def', r'    def', method_body)
                fixed_method = re.sub(r'\n(\s*)"""', r'\n        """', fixed_method)
                fixed_method = re.sub(r'\n(\s*)(?!def|class|\s*def|\s*class)', r'\n        ', fixed_method)
                
                # Make sure super call uses correct class name
                fixed_method = fixed_method.replace(f'super(', f'super({screen_class}, self)')
                
                # Replace the method in the content
                content = content[:method_start] + fixed_method + content[method_end:]
    
    # Write fixed content back to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed update_theme methods in {filename}")

if __name__ == "__main__":
    fix_screen_update_methods() 