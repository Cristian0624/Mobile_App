#!/usr/bin/env python3
import os
import sys
import shutil

def main():
    """
    Apply all UI improvements to the Kivy mobile application
    """
    print("Starting UI improvement process...")
    
    # Make a complete backup of the home.py file
    if os.path.exists('home.py'):
        backup_file = 'home.py.complete_backup'
        if not os.path.exists(backup_file):
            shutil.copy('home.py', backup_file)
            print(f"Created complete backup at {backup_file}")
    else:
        print("Error: home.py not found")
        return
    
    # Import and run each improvement script
    try:
        # Fix HomeScreen UI
        print("\n1. Applying HomeScreen UI improvements...")
        from fix_home_ui import fix_home_screen_ui
        fix_home_screen_ui()
        
        # Fix RoundedButton styling
        print("\n2. Applying RoundedButton styling improvements...")
        from fix_rounded_buttons import fix_rounded_buttons
        fix_rounded_buttons()
        
        # Fix ChatBubble styling
        print("\n3. Applying ChatBubble styling improvements...")
        from fix_chat_bubbles import fix_chat_bubbles
        fix_chat_bubbles()
        
        print("\nAll UI improvements have been successfully applied!")
        print("The application now has:")
        print("- Consistent button styling across themes")
        print("- Improved chat bubble appearance")
        print("- Better theme change handling")
        print("- Consistent color scheme throughout the app")
        
    except Exception as e:
        print(f"\nError during UI improvement process: {e}")
        print("Restoring backup...")
        
        # Restore from backup if something went wrong
        if os.path.exists(backup_file):
            shutil.copy(backup_file, 'home.py')
            print("Backup restored successfully.")
        else:
            print("Could not restore backup: backup file not found.")

if __name__ == "__main__":
    main() 