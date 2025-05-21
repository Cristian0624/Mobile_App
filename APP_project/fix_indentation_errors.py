#!/usr/bin/env python3

def fix_indentation_errors():
    """Fix all identified indentation errors in home.py"""
    
    try:
        with open('home.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix BaseScreen.__init__ update_theme() indentation
        content = content.replace(
            "        if self.auto_update_theme:\n        self.update_theme()",
            "        if self.auto_update_theme:\n            self.update_theme()"
        )
        
        # Fix indentation for elif statements in BaseScreen.update_theme
        content = content.replace(
            "            # Update standard buttons\n            elif isinstance(child, Button) and child != self.back_button:",
            "            # Update standard buttons\n                elif isinstance(child, Button) and child != self.back_button:"
        )
        
        content = content.replace(
            "            # Update text inputs\n            elif isinstance(child, TextInput):",
            "            # Update text inputs\n                elif isinstance(child, TextInput):"
        )
        
        # Fix SettingsScreen.update_theme indentation
        content = content.replace(
            "        if hasattr(self, 'setting_labels'):\n        for label in self.setting_labels:",
            "        if hasattr(self, 'setting_labels'):\n            for label in self.setting_labels:"
        )
        
        # Fix ReminderScreen.update_theme indentation
        content = content.replace(
            "        def update_theme(self, *args):\n        \"\"\"Override to update specific UI elements\"\"\"",
            "        def update_theme(self, *args):\n            \"\"\"Override to update specific UI elements\"\"\""
        )
        
        # Fix ask_ai_about_medication indentation
        content = content.replace(
            "            if medication_name:\n            voice_screen.set_medication_context(medication_name)",
            "            if medication_name:\n                voice_screen.set_medication_context(medication_name)"
        )
        
        # Write the fixed content back to the file
        with open('home.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Fixed indentation errors in home.py")
        return True
        
    except Exception as e:
        print(f"Error fixing indentation errors: {e}")
        return False

if __name__ == "__main__":
    fix_indentation_errors() 