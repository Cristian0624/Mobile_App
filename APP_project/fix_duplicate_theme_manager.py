#!/usr/bin/env python3

def remove_duplicate_theme_manager():
    """Remove the duplicate ThemeManager class from home.py"""
    
    try:
        with open('home.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the start and end of the duplicate ThemeManager class
        class_start = content.find("class ThemeManager:")
        
        # Make sure we found it
        if class_start == -1:
            print("No duplicate ThemeManager class found in home.py")
            return False
        
        # Find the next class definition to mark the end of the ThemeManager class
        next_class = content.find("class ", class_start + 10)
        
        # Extract the duplicate ThemeManager class
        duplicate_class = content[class_start:next_class].strip()
        
        # Remove the duplicate class
        new_content = content.replace(duplicate_class, "")
        
        # Write the updated content back to the file
        with open('home.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Removed duplicate ThemeManager class from home.py")
        return True
        
    except Exception as e:
        print(f"Error removing duplicate ThemeManager: {e}")
        return False

if __name__ == "__main__":
    remove_duplicate_theme_manager() 