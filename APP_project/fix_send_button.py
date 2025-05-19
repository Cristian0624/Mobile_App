#!/usr/bin/env python3
import re
import os
import shutil

def fix_send_button():
    """
    Fix the send button in the VoiceScreen to use a proper icon image instead of a drawn triangle.
    - Check if send.png exists in the icons directory
    - Replace the triangle drawing code with proper image icon
    - Ensure consistent styling across themes
    """
    if not os.path.exists('home.py'):
        print("Error: home.py not found")
        return
    
    # Make a backup of the original file
    backup_file = 'home.py.send_button_backup'
    if not os.path.exists(backup_file):
        shutil.copy('home.py', backup_file)
        print(f"Created backup at {backup_file}")
    
    # Check if send.png exists
    send_icon_exists = os.path.exists(os.path.join('icons', 'send.png'))
    print(f"Send icon exists: {send_icon_exists}")
    
    # Read the home.py file
    with open('home.py', 'r') as file:
        content = file.read()
    
    # Find the send button creation code in VoiceScreen
    send_button_pattern = r'# Send button with new design using our custom BorderedButton.*?self\.send_btn\.bind\(on_release=self\.send_text_message\)'
    
    # Create improved send button code using the icon
    if send_icon_exists:
        # Use the existing send.png icon
        improved_send_button = '''# Send button with new design using a proper icon
        self.send_btn = Button(
            size_hint=(0.2, None),
            height=dp(50),
            background_normal='',
            background_color=(1, 1, 1, 1) if not self.theme_manager.is_dark_mode else (0.2, 0.2, 0.22, 1)
        )
        
        # Add send icon as an image
        send_icon_layout = RelativeLayout(size_hint=(1, 1))
        self.send_icon = Image(
            source='icons/send.png',
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        send_icon_layout.add_widget(self.send_icon)
        self.send_btn.add_widget(send_icon_layout)
        
        # Bind to send message
        self.send_btn.bind(on_release=self.send_text_message)'''
    else:
        # Create a better triangle icon with border
        improved_send_button = '''# Send button with new design using our custom BorderedButton
        self.send_btn = BorderedButton(
            size_hint=(0.2, None),
            height=dp(50),
            background_normal='',
            background_color=(1, 1, 1, 1),  # White background
            border_color=(0.2, 0.6, 0.9, 1)  # Light blue border
        )
        
        # Add send icon directly drawn instead of using an image
        with self.send_btn.canvas.after:
            # Draw a paper airplane icon - filled triangle
            self.send_icon_color = Color(0.2, 0.6, 0.9, 1)  # Light blue
            
            # Calculate center position and size
            icon_size = dp(30)  # Increased size for better visibility
            center_x = 0
            center_y = 0
            
            # Create a filled triangle pointing right
            self.send_icon_shape = Triangle(
                points=[
                    center_x - icon_size/2, center_y + icon_size/2,  # Top left
                    center_x - icon_size/2, center_y - icon_size/2,  # Bottom left
                    center_x + icon_size/2, center_y                 # Right point
                ]
            )
        
        # Update the send icon position when button size/position changes
        self.send_btn.bind(pos=self._update_send_icon, size=self._update_send_icon)
        self.send_btn.bind(on_release=self.send_text_message)'''
    
    # Replace the send button code
    content = re.sub(send_button_pattern, improved_send_button, content, flags=re.DOTALL)
    
    # If using image icon, we need to update the update_theme method as well
    if send_icon_exists:
        # Find the update_theme method in VoiceScreen
        update_theme_pattern = r'def update_theme\(self, \*args\):.*?# Update send button colors.*?self\.send_btn\._update_canvas\(\)  # Force update.*?if hasattr\(self, \'send_icon_color\'\):.*?self\.send_icon_color\.rgba = \(0\.2, 0\.6, 0\.9, 1\)  # Always light blue'
        
        # Create improved update_theme code
        improved_update_theme = '''def update_theme(self, *args):
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

        # Update send button colors - white in light mode, dark in dark mode
        if hasattr(self, 'send_btn'):
            if is_dark:
                self.send_btn.background_color = (0.2, 0.2, 0.22, 1)  # Dark background in dark mode
            else:
                self.send_btn.background_color = (1, 1, 1, 1)  # White background in light mode'''
        
        # Replace the update_theme method
        content = re.sub(update_theme_pattern, improved_update_theme, content, flags=re.DOTALL)
        
        # Also need to remove the _update_send_icon method since we're not using it anymore
        update_send_icon_pattern = r'def _update_send_icon\(self, instance, value\):.*?"""Update the send icon position based on the button size/position""".*?if hasattr\(self, \'send_icon_shape\'\):.*?self\.send_icon_shape\.points = \[.*?\]'
        
        # Replace with empty string to remove the method
        content = re.sub(update_send_icon_pattern, '', content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open('home.py', 'w') as file:
        file.write(content)
    
    print("Successfully updated send button to use a proper icon")

if __name__ == "__main__":
    fix_send_button() 