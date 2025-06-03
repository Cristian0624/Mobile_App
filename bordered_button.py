from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import ListProperty

class BorderedButton(Button):
    """Button with custom border color support and rounded corners"""
    border_color = ListProperty([0.2, 0.6, 0.9, 1])  # Default light blue
    
    def __init__(self, **kwargs):
        # Extract border color before passing to parent class
        if 'border_color' in kwargs:
            self.border_color = kwargs.pop('border_color')
        
        # Set up button properties
        kwargs['background_normal'] = ''
        kwargs['background_down'] = ''
        kwargs['background_color'] = [0, 0, 0, 0]  # Transparent background
        kwargs['color'] = [0, 0, 0, 0]  # Transparent text (we'll use an image instead)
            
        super(BorderedButton, self).__init__(**kwargs)
        
        # Bind to size and pos to update the border
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Initial canvas update
        self._update_rect()
    
    def _update_rect(self, *args):
        """Update the button's appearance"""
        self.canvas.before.clear()
        with self.canvas.before:
            # First draw blue border
            Color(*self.border_color)
            self.border_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8)]
            )
            
            # Then draw white background with smaller size (creating border effect)
            Color(1, 1, 1, 1)  # White
            border_width = dp(2)
            self.bg_rect = RoundedRectangle(
                pos=(self.x + border_width, self.y + border_width),
                size=(self.width - 2*border_width, self.height - 2*border_width),
                radius=[dp(6)]
            )
    
    def on_state(self, instance, value):
        """Handle button press state changes"""
        if value == 'down':
            # Pressed state - show gray background
            self.canvas.before.clear()
            with self.canvas.before:
                # Keep blue border
                Color(*self.border_color)
                self.border_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(8)]
                )
                
                # Light gray background for pressed state
                Color(0.9, 0.9, 0.9, 1)
                border_width = dp(2)
                self.bg_rect = RoundedRectangle(
                    pos=(self.x + border_width, self.y + border_width),
                    size=(self.width - 2*border_width, self.height - 2*border_width),
                    radius=[dp(6)]
                )
        else:
            # Normal state - white background
            self.canvas.before.clear()
            with self.canvas.before:
                # Blue border
                Color(*self.border_color)
                self.border_rect = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(8)]
                )
                
                # White background
                Color(1, 1, 1, 1)
                border_width = dp(2)
                self.bg_rect = RoundedRectangle(
                    pos=(self.x + border_width, self.y + border_width),
                    size=(self.width - 2*border_width, self.height - 2*border_width),
                    radius=[dp(6)]
                ) 