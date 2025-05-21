from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.theme_manager = None
        self.language_manager = None
        
        # Main layout
        self.main_layout = FloatLayout()
        
        # Set background color based on theme
        with self.main_layout.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Default to white
            self.bg_rect = Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
            self.main_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        self.add_widget(self.main_layout)
    
    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def update_theme(self, *args):
        """Update the theme colors"""
        if hasattr(self, 'theme_manager') and self.theme_manager:
            colors = self.theme_manager.get_colors()
            if hasattr(self, 'bg_color'):
                self.bg_color.rgba = colors['background'] 