from kivy.uix.button import Button
from kivy.metrics import dp

class CreamButton(Button):
    def __init__(self, **kwargs):
        super(CreamButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.85, 0.82, 0.78, 1)
        self.color = (0.1, 0.1, 0.1, 1)
        self.font_size = dp(16)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50) 