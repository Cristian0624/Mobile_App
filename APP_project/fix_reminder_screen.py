import re

def fix_reminder_screen():
    with open('home.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find ReminderScreen class
    reminder_match = re.search(r'class\s+ReminderScreen\(BaseScreen\):', content)
    if not reminder_match:
        print("ReminderScreen class not found")
        return
    
    # Find its update_theme method
    reminder_start = reminder_match.start()
    update_theme_match = re.search(r'def\s+update_theme\s*\(\s*self\s*,\s*\*args\s*\)\s*:', content[reminder_start:])
    if not update_theme_match:
        print("update_theme method not found in ReminderScreen")
        return
    
    # Get the method content
    method_start = reminder_start + update_theme_match.start()
    next_def_match = re.search(r'def\s+', content[method_start + 10:])
    if next_def_match:
        method_end = method_start + 10 + next_def_match.start()
    else:
        method_end = len(content)
    
    method_text = content[method_start:method_end]
    
    # Fix the super call
    fixed_method = method_text.replace(
        'super(CameraScreen, self)',
        'super(ReminderScreen, self)'
    )
    
    # Replace the method in the content
    new_content = content[:method_start] + fixed_method + content[method_end:]
    
    # Save the fixed content
    with open('home.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed ReminderScreen.update_theme method")

if __name__ == "__main__":
    fix_reminder_screen() 