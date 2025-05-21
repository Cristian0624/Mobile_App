import re

def fix_camera_screen_indentation():
    with open('home.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the CameraScreen class
    camera_match = re.search(r'class\s+CameraScreen\(BaseScreen\):', content)
    if not camera_match:
        print("CameraScreen class not found")
        return
    
    # Get the content after CameraScreen
    camera_class_start = camera_match.start()
    class_content = content[camera_class_start:]
    
    # Find all update_theme methods in the class
    update_theme_matches = list(re.finditer(r'(?:def|    def)\s+update_theme\s*\(\s*self\s*,\s*\*args\s*\)\s*:', class_content))
    
    if len(update_theme_matches) < 2:
        print(f"Found only {len(update_theme_matches)} update_theme methods in CameraScreen class, expected at least 2")
        return
    
    # Keep only the first update_theme method and remove the second one
    first_method_start = camera_class_start + update_theme_matches[0].start()
    second_method_start = camera_class_start + update_theme_matches[1].start()
    
    # Find where the first method ends (start of the next method or class)
    first_method_end_match = re.search(r'\n    def\s+', class_content[update_theme_matches[0].end():update_theme_matches[1].start()])
    if first_method_end_match:
        first_method_end = camera_class_start + update_theme_matches[0].end() + first_method_end_match.start()
    else:
        # If no method found, use the start of the second update_theme
        first_method_end = second_method_start
    
    # Find where the second method ends
    if len(update_theme_matches) > 2:
        second_method_end = camera_class_start + update_theme_matches[2].start()
    else:
        # Check for the next method after the second update_theme
        next_method_match = re.search(r'\n    def\s+', class_content[update_theme_matches[1].end():])
        if next_method_match:
            second_method_end = camera_class_start + update_theme_matches[1].end() + next_method_match.start()
        else:
            # If no next method found, search for the next class
            next_class_match = re.search(r'\nclass\s+', class_content[update_theme_matches[1].end():])
            if next_class_match:
                second_method_end = camera_class_start + update_theme_matches[1].end() + next_class_match.start()
            else:
                second_method_end = len(content)
    
    # Create a new content without the second update_theme method
    new_content = content[:second_method_start] + content[second_method_end:]
    
    # Ensure the remaining update_theme method is properly indented
    # Extract the method content
    method_content = new_content[first_method_start:first_method_end]
    
    # Check if the method declaration is properly indented
    if not method_content.startswith('    def'):
        method_content = method_content.replace('def', '    def', 1)
        new_content = new_content[:first_method_start] + method_content + new_content[first_method_end:]
    
    # Write the fixed content back to the file
    with open('home.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed CameraScreen update_theme methods")

if __name__ == "__main__":
    fix_camera_screen_indentation() 