#!/usr/bin/env python3
import re
import os

def fix_send_button():
    """
    Fix the send button in VoiceScreen to use the send.png icon.
    """
    if not os.path.exists('home.py'):
        print("Error: home.py not found")
        return
    
    # Check if send.png exists
    send_icon_exists = os.path.exists(os.path.join('icons', 'send.png'))
    if not send_icon_exists:
        print("Error: send.png not found in icons directory")
        return
    
    print(f"Found send.png icon in icons directory")
    
    # Read the home.py file
    with open('home.py', 'r') as file:
        content = file.read()
    
    # Find the VoiceScreen class
    voice_screen_match = re.search(r'class VoiceScreen\(BaseScreen\):.*?def __init__\(self, \*\*kwargs\):(.*?)def update_theme\(self, \*args\):', content, re.DOTALL)
    
    if not voice_screen_match:
        print("Error: Could not find VoiceScreen.__init__ method")
        return
    
    init_method = voice_screen_match.group(1)
    
    # Find the send button code
    send_button_match = re.search(r'# Send button.*?self\.send_btn\.bind\(on_release=self\.send_text_message\)', init_method, re.DOTALL)
    
    if not send_button_match:
        print("Error: Could not find send button code")
        return
    
    send_button_code = send_button_match.group(0)
    
    # Create new send button code with icon
    new_send_button_code = """# Send button with icon
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
        self.send_btn.bind(on_release=self.send_text_message)"""
    
    # Replace the send button code
    new_content = content.replace(send_button_code, new_send_button_code)
    
    # Write the updated content back to the file
    with open('home.py', 'w') as file:
        file.write(new_content)
    
    print("Successfully updated send button to use the send.png icon")

if __name__ == "__main__":
    fix_send_button() 