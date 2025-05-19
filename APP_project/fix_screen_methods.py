import re

def find_class_definition(content, class_name):
    """Find the start and end positions of a class definition in the content"""
    pattern = r'class\s+' + class_name + r'\('
    match = re.search(pattern, content)
    if not match:
        return None, None
    
    start_pos = match.start()
    
    # Find the next class definition to get the end
    next_class_match = re.search(r'class\s+', content[start_pos + 10:])
    if next_class_match:
        end_pos = start_pos + 10 + next_class_match.start()
    else:
        end_pos = len(content)
    
    return start_pos, end_pos

def find_method_in_class(content, class_start_pos, class_end_pos, method_name):
    """Find a method definition within a class"""
    class_content = content[class_start_pos:class_end_pos]
    method_pattern = r'def\s+' + method_name + r'\s*\('
    match = re.search(method_pattern, class_content)
    if not match:
        return None, None
    
    # Calculate absolute positions
    method_start = class_start_pos + match.start()
    
    # Find the next method definition to get the end
    next_method_match = re.search(r'def\s+', class_content[match.end():])
    if next_method_match:
        method_end = class_start_pos + match.end() + next_method_match.start()
    else:
        method_end = class_end_pos
    
    return method_start, method_end

def fix_screen_methods(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix PulsingMicButton's super() call
    content = content.replace(
        'super(PulsingMicButton, self).__init__(**kwargs)', 
        'super().__init__(**kwargs)'
    )
    
    # Fix ReminderScreen's update_theme method
    reminder_start, reminder_end = find_class_definition(content, 'ReminderScreen')
    if reminder_start is not None and reminder_end is not None:
        method_start, method_end = find_method_in_class(
            content, reminder_start, reminder_end, 'update_theme'
        )
        if method_start is not None and method_end is not None:
            method_content = content[method_start:method_end]
            
            # Replace the super call or add it if missing
            if 'super(' in method_content:
                method_content = re.sub(
                    r'super\([^)]+\)\.update_theme\(\*args\)',
                    'super(ReminderScreen, self).update_theme(*args)',
                    method_content
                )
            else:
                method_content = method_content.replace(
                    '# First call parent\'s update_theme to handle basic elements\n',
                    '# First call parent\'s update_theme to handle basic elements\n        super(ReminderScreen, self).update_theme(*args)\n'
                )
            
            # Update the content
            content = content[:method_start] + method_content + content[method_end:]
    
    # Fix CameraScreen's update_theme method
    camera_start, camera_end = find_class_definition(content, 'CameraScreen')
    if camera_start is not None and camera_end is not None:
        method_start, method_end = find_method_in_class(
            content, camera_start, camera_end, 'update_theme'
        )
        if method_start is not None and method_end is not None:
            method_content = content[method_start:method_end]
            
            # Replace the super call
            method_content = re.sub(
                r'super\([^)]+\)\.update_theme\(\*args\)',
                'super(CameraScreen, self).update_theme(*args)',
                method_content
            )
            
            # Update the content
            content = content[:method_start] + method_content + content[method_end:]
    
    # Fix VoiceScreen's update_theme method
    voice_start, voice_end = find_class_definition(content, 'VoiceScreen')
    if voice_start is not None and voice_end is not None:
        method_start, method_end = find_method_in_class(
            content, voice_start, voice_end, 'update_theme'
        )
        if method_start is not None and method_end is not None:
            method_content = content[method_start:method_end]
            
            # Replace the super call
            method_content = re.sub(
                r'super\([^)]+\)\.update_theme\(\*args\)',
                'super(VoiceScreen, self).update_theme(*args)',
                method_content
            )
            
            # Update the content
            content = content[:method_start] + method_content + content[method_end:]
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed screen methods in {file_path}")

if __name__ == "__main__":
    fix_screen_methods("home.py") 