from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Translate, Rotate, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
import math
from kivy.metrics import dp

class RoundButton(ButtonBehavior, Widget):
    """A specialized button that reliably detects touches within a circular area"""
    
    def __init__(self, **kwargs):
        # Get background color for the circle
        self.bg_color = kwargs.pop('bg_color', kwargs.pop('color', (1, 1, 1, 1)))  # Default white
        self.fg_color = kwargs.pop('fg_color', (0, 0, 0, 1))  # Default black
        self.text = kwargs.pop('text', '+')
        self.font_size = kwargs.pop('font_size', 24)
        self.bold = kwargs.pop('bold', False)
        
        # Initialize as widget first
        super(RoundButton, self).__init__(**kwargs)
        
        # Draw the circle in the canvas
        with self.canvas:
            # Background circle
            Color(*self.bg_color)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            
            # Create a label for the text
            self.label = CoreLabel(text=self.text, font_size=self.font_size, bold=self.bold)
            self.label.refresh()
            
            # Text in the center
            Color(*self.fg_color)
            
            # Calculate text position - center perfectly
            text_width, text_height = self.label.texture.size
            text_x = self.center_x - text_width / 2
            text_y = self.center_y - text_height / 2
            
            # Draw the text
            self.text_rect = Rectangle(
                pos=(text_x, text_y),
                size=self.label.texture.size,
                texture=self.label.texture
            )
        
        # Bind to size and position changes
        self.bind(size=self._update_graphics, pos=self._update_graphics)
    
    def set_colors(self, bg_color=(1, 1, 1, 1), fg_color=(0, 0, 0, 1)):
        """Explicitly set the background and foreground colors"""
        self.bg_color = bg_color
        self.fg_color = fg_color
        self._update_graphics()
        
    def _update_graphics(self, *args):
        """Update all graphical elements when position or size changes"""
        # Update circle
        self.circle.pos = self.pos
        self.circle.size = self.size
        
        # Update text - ensure it's always centered
        self.label = CoreLabel(text=self.text, font_size=self.font_size, bold=self.bold)
        self.label.refresh()
        
        text_width, text_height = self.label.texture.size
        text_x = self.center_x - text_width / 2
        text_y = self.center_y - text_height / 2
        
        self.text_rect.texture = self.label.texture
        self.text_rect.size = self.label.texture.size
        self.text_rect.pos = (text_x, text_y)
    
    def collide_point(self, x, y):
        """Check if a point is within the circular area"""
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) / 2
        return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) <= radius
