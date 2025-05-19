#!/usr/bin/env python3

# This script fixes both VoiceScreen, CameraScreen, and ReminderScreen update_theme methods by adding
# proper super() calls to make the dark theme apply consistently across all screens

import re

with open('home.py', 'r') as file:
    content = file.read()

# Fixed update_theme methods for each screen

# ReminderScreen update_theme with super() call added
reminder_update = '''    def update_theme(self, *args):
        """Override to update specific UI elements"""
        # First call parent's update_theme to handle basic elements
        super(ReminderScreen, self).update_theme(*args)
        
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update form background color based on theme
        if self.theme_manager.is_dark_mode:
            self.form_bg_color.rgba = (0.15, 0.15, 0.15, 1)  # Darker background for dark mode
        else:
            self.form_bg_color.rgba = (0.97, 0.97, 0.97, 1)  # Light background for light mode
        
        # Update text colors
        self.title_label.color = colors['text']
        self.form_title.color = colors.get('primary', (0.2, 0.4, 0.8, 1))
        
        # Update form labels
        if hasattr(self, 'name_label'):
            self.name_label.color = colors['text']
        if hasattr(self, 'dosage_label'):
            self.dosage_label.color = colors['text']
        if hasattr(self, 'frequency_label'):
            self.frequency_label.color = colors['text']
        if hasattr(self, 'duration_label'):
            self.duration_label.color = colors['text']
        if hasattr(self, 'notes_label'):
            self.notes_label.color = colors['text']
        
        # Circle plus button should remain green regardless of theme
        # But text below should respect theme for visibility
        if hasattr(self, 'add_text'):
            self.add_text.color = (0.2, 0.7, 0.3, 1)  # Keep green but adjust brightness for dark mode
            
        # Update all reminder cards
        if hasattr(self, 'reminders_layout'):
            for child in self.reminders_layout.children:
                if isinstance(child, ReminderCard):
                    child.update_theme()
                    
        # Update the "no reminders" label
        if hasattr(self, 'no_reminders_label'):
            self.no_reminders_label.color = colors['text']
            
        # Update form inputs
        if hasattr(self, 'name_input'):
            self.name_input.background_color = colors['input_bg']
            self.name_input.foreground_color = colors['text']
            
        if hasattr(self, 'dosage_input'):
            self.dosage_input.background_color = colors['input_bg']
            self.dosage_input.foreground_color = colors['text']
            
        if hasattr(self, 'duration_input'):
            self.duration_input.background_color = colors['input_bg']
            self.duration_input.foreground_color = colors['text']
            
        if hasattr(self, 'notes_input'):
            self.notes_input.background_color = colors['input_bg']
            self.notes_input.foreground_color = colors['text']
            
        # Frequency button theme
        if hasattr(self, 'frequency_button'):
            # Keep frequency button yellow but adjust darkness
            if is_dark:
                self.frequency_button.color = (0.1, 0.1, 0.1, 1)  # Dark text
            else:
                self.frequency_button.color = (0.1, 0.1, 0.1, 1)  # Dark text'''

# CameraScreen update_theme with super() call added
camera_update = '''    def update_theme(self, *args):
        """Override to update specific UI elements"""
        # First call parent's update_theme to handle basic elements
        super(CameraScreen, self).update_theme(*args)
        
        # Update text colors based on theme
        colors = self.theme_manager.get_colors()
        
        if hasattr(self, 'title_label'):
            self.title_label.color = colors.get('primary', (0.2, 0.4, 0.8, 1))
            
        if hasattr(self, 'content_label'):
            self.content_label.color = colors['text']
            
        if hasattr(self, 'coming_soon_btn'):
            self.coming_soon_btn.background_color = self.theme_manager.get_button_color()
            self.coming_soon_btn.color = self.theme_manager.get_button_text_color()'''

# VoiceScreen update_theme with super() call added
voice_update = '''    def update_theme(self, *args):
        """Override to update specific UI elements for this screen"""
        # First call parent's update_theme to handle basic elements
        super(VoiceScreen, self).update_theme(*args)
        
        # Update colors based on theme
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update title and subtitle colors
        self.title_label.color = colors.get('primary', (0.2, 0.4, 0.8, 1))
        self.subtitle_label.color = colors['text_secondary'] if 'text_secondary' in colors else (0.5, 0.5, 0.5, 1)
        
        # Update status label
        self.status_label.color = colors['text_secondary'] if 'text_secondary' in colors else (0.5, 0.5, 0.5, 1)
        
        # Update send button colors
        self.send_btn.bg_color = self.theme_manager.get_accent_color()
        self.send_btn.color = (1, 1, 1, 1)  # Keep text white for contrast
        
        # Update text input colors for dark/light theme
        self.text_input.background_color = colors['input_bg']
        self.text_input.foreground_color = colors['text']
        self.text_input.cursor_color = colors['primary']
        
        # Update chat bubbles if any exist
        for child in self.chat_layout.children:
            if isinstance(child, ChatBubble) and hasattr(child, 'update_theme'):
                child.update_theme(is_dark)
            elif isinstance(child, BoxLayout):
                # This may be a message container
                for message_part in child.children:
                    if isinstance(message_part, Label):
                        message_part.color = colors['text']'''

# Regex patterns to find and replace each method
reminder_pattern = r'def update_theme\(self, \*args\):\s+"""Override to update specific UI elements""".*?def '
voice_pattern = r'def update_theme\(self, \*args\):\s+"""Override to update specific UI elements for this screen""".*?def '
camera_pattern = r'def update_theme\(self, \*args\):\s+"""Override to update specific UI elements""".*?def '

# Find reminder screen update_theme method and replace it
content_updated = re.sub(
    reminder_pattern,
    lambda match: reminder_update + '\n\n    def ',
    content,
    flags=re.DOTALL
)

# Find camera screen update_theme method and replace it - focusing on the first instance
content_updated = re.sub(
    camera_pattern,
    lambda match: camera_update + '\n\n    def ',
    content_updated,
    flags=re.DOTALL,
    count=1  # Replace only the first occurrence
)

# Find voice screen update_theme method and replace it
content_updated = re.sub(
    voice_pattern,
    lambda match: voice_update + '\n\n    def ',
    content_updated,
    flags=re.DOTALL
)

# Write the updated content back to the file
with open('home.py', 'w') as file:
    file.write(content_updated)

print("Fixed update_theme methods in ReminderScreen, CameraScreen, and VoiceScreen") 