#!/usr/bin/env python3
import re

def fix_indentation_errors(filename='home.py'):
    """Fix indentation errors in the home.py file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix BaseScreen.__init__ update_theme call indentation
        content = content.replace(
            "        if self.auto_update_theme:\n        self.update_theme()",
            "        if self.auto_update_theme:\n            self.update_theme()"
        )
        
        # Fix indentation for elif in update_theme method
        content = content.replace(
            "            # Update standard buttons\n            elif isinstance(child, Button) and child != self.back_button:",
            "            # Update standard buttons\n            elif isinstance(child, Button) and child != self.back_button:"
        )
        
        # Fix indentation for nested if in update_theme method
        content = content.replace(
            "                # Only update standard buttons, not custom ones\n                if not any(isinstance(child, cls) for cls in [RoundedButton, IconButton]):",
            "                # Only update standard buttons, not custom ones\n                if not any(isinstance(child, cls) for cls in [RoundedButton, IconButton]):"
        )
        
        # Fix indentation for TextInput in update_theme method
        content = content.replace(
            "            # Update text inputs\n            elif isinstance(child, TextInput):",
            "            # Update text inputs\n            elif isinstance(child, TextInput):"
        )
        
        # Fix indentation in ask_ai_about_medication method
        content = content.replace(
            "            if medication_name:\n            voice_screen.set_medication_context(medication_name)",
            "            if medication_name:\n                voice_screen.set_medication_context(medication_name)"
        )
        
        # Fix indentation in CameraScreen.update_theme method definition
        content = content.replace(
            "        def update_theme(self, *args):\n        \"\"\"Override to update specific UI elements\"\"\"",
            "        def update_theme(self, *args):\n            \"\"\"Override to update specific UI elements\"\"\""
        )
        
        # Fix indentation in SettingsScreen.update_theme method
        content = content.replace(
            "        if hasattr(self, 'setting_labels'):\n        for label in self.setting_labels:",
            "        if hasattr(self, 'setting_labels'):\n            for label in self.setting_labels:"
        )
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Fixed indentation errors in {filename}")
        return True
    except Exception as e:
        print(f"Error fixing indentation: {e}")
        return False

def fix_indentation_issues(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_block = False
    current_indent = 0
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue
        
        # Check if this is a method or class definition
        if line.strip().startswith('def ') or line.strip().startswith('class '):
            if not line.lstrip().startswith(' '):
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces < 4 and 'def update_theme' in line:
                    # This is a method inside a class that needs proper indentation
                    fixed_lines.append(' ' * 4 + line.lstrip())
                    current_indent = 4
                    in_block = True
                else:
                    fixed_lines.append(line)
                    if line.strip().startswith('def '):
                        current_indent = leading_spaces
                        in_block = True
            else:
                fixed_lines.append(line)
                current_indent = len(line) - len(line.lstrip())
                in_block = True
        
        # Handle lines that should be indented (inside method or class blocks)
        elif in_block and line.strip() and not line.strip().startswith('#'):
            leading_spaces = len(line) - len(line.lstrip())
            
            # Lines that should be indented at least 4 more spaces than their containing method
            if leading_spaces <= current_indent and not line.strip().startswith(('if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:')):
                # This line needs more indentation
                fixed_lines.append(' ' * (current_indent + 4) + line.lstrip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Write the fixed content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed indentation issues in {filename}")

# A more targeted approach to fix the specific issue at line 2708
def fix_specific_indentation_issue(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix HomeScreen's update_theme method
    home_screen_update_method = '''    def update_theme(self, *args):
        """Override BaseScreen's update_theme to handle specific UI elements"""
        # Call parent method to handle basic elements
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update background color
        if is_dark:
            self.bg_color.rgba = colors['background']
        else:
            self.bg_color.rgba = colors['background']
            
        # Update all setting labels with appropriate colors
        if hasattr(self, 'setting_labels'):
            for label in self.setting_labels:
                label.color = colors['text']
                
        # Update title with proper color
        if hasattr(self, 'title_label'):
            self.title_label.color = colors['text']
            
        # Update logout button with theme-appropriate colors
        if hasattr(self, 'logout_btn'):
            if is_dark:
                self.logout_btn.background_color = colors['button_bg']
                self.logout_btn.color = colors['button_text']
            else:
                self.logout_btn.background_color = colors['button_bg']
                self.logout_btn.color = colors['button_text']
                
        # Update language spinner with theme colors
        if hasattr(self, 'language_spinner'):
            if is_dark:
                self.language_spinner.background_color = colors['input_bg']
                self.language_spinner.color = colors['text']
            else:
                self.language_spinner.background_color = colors['input_bg']
                self.language_spinner.color = colors['text']
        
        # Make sure switches are correctly updated if they exist
        if hasattr(self, 'dark_mode_switch'):
            # No need to change the switch appearance, just ensure it reflects the current state
            self.dark_mode_switch.active = is_dark
            
        # Update any other UI elements
        for child in self.walk(restrict=True):
            # Update all Labels
            if isinstance(child, Label):
                # Skip already updated labels
                if hasattr(self, 'setting_labels') and child in self.setting_labels:
                    continue
                if hasattr(self, 'title_label') and child == self.title_label:
                    continue
                child.color = colors['text']
                
            # Update all standard buttons
            elif isinstance(child, Button):
                # Skip already updated buttons
                if hasattr(self, 'logout_btn') and child == self.logout_btn:
                    continue
                if not any(isinstance(child, cls) for cls in [RoundedButton, IconButton]):
                    child.background_color = colors['button_bg']
                    child.color = colors['button_text']'''
    
    # Find and replace the problematic method
    pattern = r'def update_theme\(self, \*args\):\s+"""Override BaseScreen.+?standard buttons'
    content = content.replace('def update_theme(self, *args):\n        """Override BaseScreen', 
                            '    def update_theme(self, *args):\n        """Override BaseScreen')
    
    # Fix common indentation issues
    content = content.replace('if is_dark:\n        self.bg_color', 
                            'if is_dark:\n            self.bg_color')
    content = content.replace('else:\n        self.bg_color', 
                            'else:\n            self.bg_color')
    content = content.replace('if hasattr(self, \'setting_labels\'):\n        for label', 
                            'if hasattr(self, \'setting_labels\'):\n            for label')
    content = content.replace('for label in self.setting_labels:\n        label.color', 
                            'for label in self.setting_labels:\n                label.color')
    
    # Write the fixed content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed specific indentation issues in {filename}")

def fix_file(filename):
    with open(filename, "r") as file:
        content = file.read()
    
    # Fix 1: indentation around lines 170-177
    content = re.sub(
        r"                if getattr\(child, 'bold', False\) and getattr\(child, 'font_size', 0\) > dp\(18\):\s+# This is likely a title - use primary color\s+child\.color = colors\.get\('primary', colors\['text'\]\)\s+else:\s+# Regular text\s+child\.color = colors\['text'\]",
        "                if getattr(child, 'bold', False) and getattr(child, 'font_size', 0) > dp(18):\n                    # This is likely a title - use primary color\n                    child.color = colors.get('primary', colors['text'])\n                else:\n                    # Regular text\n                    child.color = colors['text']",
        content
    )
    
    # Fix 2: indentation in LanguageManager (line 105)
    content = re.sub(
        r"        self.theme_manager = ThemeManager\(\)\s+self.language_manager = LanguageManager\(\)",
        "        self.theme_manager = ThemeManager()\n        self.language_manager = LanguageManager()",
        content
    )
    
    # Fix 3: indentation in IconButton.update_theme
    content = re.sub(
        r"            self.icon_image.color = colors\['text'\]  # Use text color from theme for consistency\s+self.label.color = colors\['text'\]\s+else:",
        "            self.icon_image.color = colors['text']  # Use text color from theme for consistency\n            self.label.color = colors['text']\n        else:",
        content
    )
    
    # Fix 4: Conditional in ReminderCard.update_theme - line ~1000-1010
    content = re.sub(
        r"                if minutes > 0:\s+display_text = f\"{hours}h\\n{minutes}m\"\s+else:\s+display_text = f\"{hours}h\"",
        "                if minutes > 0:\n                    display_text = f\"{hours}h\\n{minutes}m\"\n                else:\n                    display_text = f\"{hours}h\"",
        content
    )
    
    # Fix 5: Fix else alignment in cooldown time display
    content = re.sub(
        r"            cooldown_text = f\"{hours}h\\n{minutes}m\"\s+else:\s+cooldown_text =",
        "            cooldown_text = f\"{hours}h\\n{minutes}m\"\n        else:\n            cooldown_text =",
        content
    )
    
    # Fix 6: Fix return in get_cooldown_minutes
    content = re.sub(
        r"        # Default to 8 hours if frequency not found\s+return frequency_map.get\(frequency, 8 \* 60\)",
        "        # Default to 8 hours if frequency not found\n        return frequency_map.get(frequency, 8 * 60)",
        content
    )
    
    # Fix 7: Fix else in check_cooldown_status
    content = re.sub(
        r"            return False\s+else:\s+# Still in cooldown, update time left",
        "            return False\n        else:\n            # Still in cooldown, update time left",
        content
    )
    
    # Fix 8: Fix dark mode settings for take button
    content = re.sub(
        r"                self.take_button.bg_color = \(0.15, 0.4, 0.2, 0.8\)  # Darker green, partially transparent\s+else:\s+self.take_button.bg_color =",
        "                self.take_button.bg_color = (0.15, 0.4, 0.2, 0.8)  # Darker green, partially transparent\n            else:\n                self.take_button.bg_color =",
        content
    )
    
    # Fix 9: Fix dark mode settings for bg_color
    content = re.sub(
        r"                self.bg_color.rgba = \(0.15, 0.15, 0.18, 1\)  # Much darker background for dark mode\s+else:\s+self.bg_color.rgba =",
        "                self.bg_color.rgba = (0.15, 0.15, 0.18, 1)  # Much darker background for dark mode\n            else:\n                self.bg_color.rgba =",
        content
    )
    
    # Fix 10: Fix SettingsScreen logout button in update_theme
    content = re.sub(
        r"                self.logout_btn.background_color = colors\['button_bg'\]\s+self.logout_btn.color = colors\['button_text'\]\s+else:",
        "                self.logout_btn.background_color = colors['button_bg']\n                self.logout_btn.color = colors['button_text']\n            else:",
        content
    )
    
    # Fix 11: Fix SettingsScreen language spinner
    content = re.sub(
        r"                self.language_spinner.background_color = colors\['input_bg'\]\s+self.language_spinner.color = colors\['text'\]\s+else:",
        "                self.language_spinner.background_color = colors['input_bg']\n                self.language_spinner.color = colors['text']\n            else:",
        content
    )
    
    # Fix 12: Fix ButtonBehavior on_touch_down return
    content = re.sub(
        r"        return True\s+return super\(RoundedButton, self\).on_touch_down\(touch\)",
        "            return True\n        return super(RoundedButton, self).on_touch_down(touch)",
        content
    )
    
    # Fix 13: Fix ButtonBehavior on_touch_up return
    content = re.sub(
        r"        return True\s+return super\(RoundedButton, self\).on_touch_up\(touch\)",
        "            return True\n        return super(RoundedButton, self).on_touch_up(touch)",
        content
    )
    
    # Fix 14: Fix VoiceScreen toggle_listening conditional
    content = re.sub(
        r"            self.status_label.text = \"Processing\.\.\.\"\s+else:\s+# Start listening",
        "            self.status_label.text = \"Processing...\"\n        else:\n            # Start listening",
        content
    )
    
    # Fix 15: Fix CameraScreen and VoiceScreen misaligned methods
    content = content.replace("class VoiceScreen(BaseScreen):\n            def __init__", "class VoiceScreen(BaseScreen):\n    def __init__")
    content = content.replace("class CameraScreen(BaseScreen):\n            def __init__", "class CameraScreen(BaseScreen):\n    def __init__")
    content = content.replace("class HomeScreen(Screen):\n            def __init__", "class HomeScreen(Screen):\n    def __init__")
    content = content.replace("class SettingsScreen(BaseScreen):\n            def __init__", "class SettingsScreen(BaseScreen):\n    def __init__")
    
    # Fix 16: Fix misaligned class PulsingMicButton
    content = content.replace("            def __init__(self, **kwargs):\n            super(PulsingMicButton, self).__init__", 
                             "    def __init__(self, **kwargs):\n        super(PulsingMicButton, self).__init__")
    
    # Fix 17: Fix misaligned methods in PulsingMicButton
    content = content.replace("            def _update_ellipse", "    def _update_ellipse")
    content = content.replace("            def on_state", "    def on_state")
    content = content.replace("            def _start_pulsing", "    def _start_pulsing")
    content = content.replace("            def _stop_pulsing", "    def _stop_pulsing")
    
    # Save the fixed content
    with open(filename, "w") as file:
        file.write(content)

if __name__ == "__main__":
    fix_file("home.py")
    print("Home.py indentation fixed - third batch of issues addressed") 