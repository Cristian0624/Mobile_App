from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from theme_manager import ThemeManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.metrics import dp
import os # Import os for file path
from kivy.uix.widget import Widget # Import Widget for spacing if needed

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout using FloatLayout for absolute positioning, like LoginScreen
        self.main_layout = FloatLayout()

        # Get absolute path to the image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, 'icons', 'Screenshot 2025-05-21 at 17.58.57.png')

        # Set screenshot as background image
        self.bg_image = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.main_layout.add_widget(self.bg_image)

        # Add a semi-transparent dark overlay to darken the background image
        with self.main_layout.canvas.before:
            Color(0, 0, 0, 0.6) # Dark color with 60% opacity
            self.overlay_rect = Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
        self.main_layout.bind(pos=self._update_overlay, size=self._update_overlay)

        # Title - Set text directly as requested
        self.title_label = Label(
            text='Register', # Keeping the title as 'Register' based on your last change
            font_size=dp(32),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(0.8, None), # Keep consistent with login
            height=dp(60),
            pos_hint={'center_x': 0.5, 'center_y': 0.85} # Keep title position
        )
        self.main_layout.add_widget(self.title_label)

        # Username input
        self.username = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint=(0.6, None),  # Already at 0.6
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.username)

        # Email input
        self.email = TextInput(
            hint_text='Email',
            multiline=False,
            size_hint=(0.6, None),  # Already at 0.6
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.62},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.email)

        # Password input
        self.password = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint=(0.6, None),  # Already at 0.6
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.54},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.password)

        # Confirm Password input
        self.confirm_password = TextInput(
            hint_text='Confirm Password',
            password=True,
            multiline=False,
            size_hint=(0.6, None),  # Already at 0.6
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.46},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.confirm_password)

        # Register button (main button)
        register_btn = Button(
            text='REGISTER',
            font_size=dp(16),
            bold=True,
            size_hint=(0.6, None),  # Already at 0.6
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.38},
            background_color=(0x44/255, 0x61/255, 0xcc/255, 1)
        )
        register_btn.bind(on_press=self.register)
        self.main_layout.add_widget(register_btn)

        # Login link (secondary button)
        login_btn = Button(
            text='Already have an account? LOG IN',
            font_size=dp(14),
            bold=True,
            size_hint=(0.6, None),  # Already at 0.6
            height=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=(0.9, 0.9, 0.9, 1)
        )
        login_btn.bind(on_press=self.go_to_login)
        self.main_layout.add_widget(login_btn)

        self.add_widget(self.main_layout)
        self.main_layout.bind(size=self._update_bg_image, pos=self._update_bg_image)
    
    def _update_bg_image(self, *args):
        self.bg_image.size = self.main_layout.size
        self.bg_image.pos = self.main_layout.pos

    def _update_overlay(self, instance, value):
        # Update the position and size of the overlay rectangle
        self.overlay_rect.pos = instance.pos
        self.overlay_rect.size = instance.size

    def update_theme(self):
        # Theme update logic for elements that respond to theme changes
        colors = self.theme_manager.get_colors()
        # For this screen with a background image, only update text input and button colors if needed by theme
        # Assuming the screenshot background image doesn't change with theme.
        # If text/button colors need to adapt, add logic here.
        pass # No theme updates needed for this specific screen's current design
    
    def register(self, instance):
        # TODO: Implement registration logic
        if self.password.text != self.confirm_password.text:
            # TODO: Show error message
            pass # Need to implement visual feedback
        else:
             # Assuming successful registration for now, navigate to login or home
            self.manager.current = 'login' # Navigate to login after registration
    
    def go_to_login(self, instance):
        self.manager.current = 'login' 