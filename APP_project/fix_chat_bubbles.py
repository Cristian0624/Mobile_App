#!/usr/bin/env python3
import re
import os
import shutil

def fix_chat_bubbles():
    """
    Improve the ChatBubble class to ensure consistent styling:
    1. Add proper theme handling
    2. Ensure consistent corner radius
    3. Fix color transitions between themes
    """
    if not os.path.exists('home.py'):
        print("Error: home.py not found")
        return
    
    # Make a backup of the original file
    backup_file = 'home.py.chat_backup'
    if not os.path.exists(backup_file):
        shutil.copy('home.py', backup_file)
        print(f"Created backup at {backup_file}")
    
    # Read the home.py file
    with open('home.py', 'r') as file:
        content = file.read()
    
    # Find the ChatBubble class
    chat_bubble_pattern = r'class ChatBubble\(BoxLayout\):.*?def __init__\(self, message, is_user=False, \*\*kwargs\):.*?def _update_rect\(self, instance, value\):.*?(?=\n\n)'
    
    # Create an improved ChatBubble class with better theme handling
    improved_chat_bubble = '''class ChatBubble(BoxLayout):
    def __init__(self, message, is_user=False, **kwargs):
        super(ChatBubble, self).__init__(orientation='vertical', **kwargs)
        
        self.is_user = is_user
        self.message = message
        self.size_hint_y = None
        self.height = dp(50)  # Initial height, will be updated based on text content
        
        # Get app theme manager if available
        app = App.get_running_app()
        self.theme_manager = getattr(app, 'theme_manager', None)
        is_dark = self.theme_manager.is_dark_mode if self.theme_manager else False
        
        # Set up colors based on theme and sender
        if is_user:
            if is_dark:
                bg_color = (0.2, 0.4, 0.7, 1)  # Dark blue for user in dark mode
                text_color = (1, 1, 1, 1)  # White text in dark mode
            else:
                bg_color = (0.2, 0.6, 0.9, 1)  # Blue for user in light mode
                text_color = (1, 1, 1, 1)  # White text in light mode
        else:
            if is_dark:
                bg_color = (0.25, 0.25, 0.3, 1)  # Dark gray for AI in dark mode
                text_color = (0.9, 0.9, 0.9, 1)  # Light gray text in dark mode
            else:
                bg_color = (0.9, 0.9, 0.9, 1)  # Light gray for AI in light mode
                text_color = (0.1, 0.1, 0.1, 1)  # Dark text in light mode
        
        # Create a container with proper alignment
        container = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, None),
            height=dp(50)  # Initial height, will be updated
        )
        
        # Position the bubble on the left or right based on sender
        if is_user:
            container.padding = [dp(50), dp(5), dp(10), dp(5)]  # More padding on the left
        else:
            container.padding = [dp(10), dp(5), dp(50), dp(5)]  # More padding on the right
        
        # Create the bubble with rounded corners
        self.bubble = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            padding=[dp(10), dp(8)]
        )
        
        # Add background with rounded corners
        with self.bubble.canvas.before:
            self.bg_color = Color(*bg_color)
            self.bg_rect = RoundedRectangle(
                pos=self.bubble.pos, 
                size=self.bubble.size,
                radius=[dp(12)]
            )
            self.bubble.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add message text
        self.message_label = Label(
            text=message,
            color=text_color,
            size_hint=(1, 1),
            halign='left',
            valign='middle',
            text_size=(None, None),  # Will be updated
            shorten=False,
            markup=True,
            font_size=dp(16)
        )
        
        # Add widgets to layout
        self.bubble.add_widget(self.message_label)
        container.add_widget(self.bubble)
        self.add_widget(container)
        
        # Update size after a short delay to allow text to render
        Clock.schedule_once(self._update_size, 0.1)
    
    def _update_size(self, instance, value=None):
        """Update height based on text content"""
        # Calculate text size and adjust bubble height
        self.message_label.text_size = (self.width - dp(120), None)
        self.message_label.texture_update()
        
        if self.message_label.texture_size[1] > 0:
            new_height = self.message_label.texture_size[1] + dp(20)  # Add padding
            self.bubble.height = new_height
            self.height = new_height + dp(10)
    
    def _update_rect(self, instance, value):
        """Update the background rectangle"""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size
            
    def update_theme(self, is_dark=None):
        """Update colors based on theme"""
        if is_dark is None and hasattr(self, 'theme_manager'):
            is_dark = self.theme_manager.is_dark_mode
        
        # Set up colors based on theme and sender
        if self.is_user:
            if is_dark:
                bg_color = (0.2, 0.4, 0.7, 1)  # Dark blue for user in dark mode
                text_color = (1, 1, 1, 1)  # White text in dark mode
            else:
                bg_color = (0.2, 0.6, 0.9, 1)  # Blue for user in light mode
                text_color = (1, 1, 1, 1)  # White text in light mode
        else:
            if is_dark:
                bg_color = (0.25, 0.25, 0.3, 1)  # Dark gray for AI in dark mode
                text_color = (0.9, 0.9, 0.9, 1)  # Light gray text in dark mode
            else:
                bg_color = (0.9, 0.9, 0.9, 1)  # Light gray for AI in light mode
                text_color = (0.1, 0.1, 0.1, 1)  # Dark text in light mode
                
        # Update colors
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = bg_color
            
        if hasattr(self, 'message_label'):
            self.message_label.color = text_color'''
    
    # Replace the ChatBubble class
    content = re.sub(chat_bubble_pattern, improved_chat_bubble, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open('home.py', 'w') as file:
        file.write(content)
    
    print("Successfully updated ChatBubble class with improved styling")

if __name__ == "__main__":
    fix_chat_bubbles() 