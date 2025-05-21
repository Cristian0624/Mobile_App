from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from theme_manager import ThemeManager
from language_manager import LanguageManager
from cream_button import CreamButton
import os

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        self.setup_ui()
        self.update_theme()
    
    def setup_ui(self):
        # Main layout using FloatLayout for absolute positioning
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
        
        # Title
        self.title_label = Label(
            text=self.language_manager.get_text('login').upper(),
            font_size=dp(32),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.main_layout.add_widget(self.title_label)
        
        # Username input
        self.username = TextInput(
            hint_text=self.language_manager.get_text('username'),
            multiline=False,
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.username)
        
        # Password input
        self.password = TextInput(
            hint_text=self.language_manager.get_text('password'),
            password=True,
            multiline=False,
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.password)
        
        # Show password checkbox
        self.show_password_checkbox = CheckBox(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={'center_x': 0.32, 'center_y': 0.53},
            color=(0.2, 0.2, 0.2, 1),
            active=False
        )
        self.show_password_checkbox.bind(active=self.toggle_password_visibility)
        self.main_layout.add_widget(self.show_password_checkbox)
        
        self.show_password_label = Label(
            text=self.language_manager.get_text('show_password'),
            font_size=dp(16),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(150), dp(30)),
            pos_hint={'center_x': 0.55, 'center_y': 0.53}
        )
        self.main_layout.add_widget(self.show_password_label)
        
        # Login button
        login_btn = Button(
            text=self.language_manager.get_text('login'),
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            background_color=(0.2, 0.6, 0.9, 0.9)
        )
        login_btn.bind(on_press=self.login)
        self.main_layout.add_widget(login_btn)
        
        # Sign On button
        signon_btn = CreamButton(
            text="Sign On",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.37}
        )
        signon_btn.bind(on_press=self.go_to_register)
        self.main_layout.add_widget(signon_btn)
        
        self.add_widget(self.main_layout)
        
        # Bind background image size to layout size
        self.main_layout.bind(size=self._update_bg_image, pos=self._update_bg_image)
    
    def _update_bg_image(self, *args):
        self.bg_image.size = self.main_layout.size
        self.bg_image.pos = self.main_layout.pos
    
    def update_theme(self):
        pass
    
    def update_language_text(self, *args):
        self.title_label.text = self.language_manager.get_text('login').upper()
        self.username.hint_text = self.language_manager.get_text('username')
        self.password.hint_text = self.language_manager.get_text('password')
        self.show_password_label.text = self.language_manager.get_text('show_password')
        for child in self.main_layout.children:
            if isinstance(child, Button):
                if 'login' in child.text.lower():
                    child.text = self.language_manager.get_text('login')
                elif child.text == "Sign On":
                    child.text = "Sign On"
    
    def toggle_password_visibility(self, checkbox, value):
        self.password.password = not value
    
    def login(self, instance):
        self.manager.current = 'home'
    
    def go_to_register(self, instance):
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        self.setup_ui()
        self.update_theme()
    
    def setup_ui(self):
        self.main_layout = FloatLayout()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, 'icons', 'Screenshot 2025-05-21 at 17.58.57.png')
        self.bg_image = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.main_layout.add_widget(self.bg_image)
        # Title
        self.title_label = Label(
            text=self.language_manager.get_text('sign_up').upper(),
            font_size=dp(32),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.main_layout.add_widget(self.title_label)
        # Username input
        self.username = TextInput(
            hint_text=self.language_manager.get_text('username'),
            multiline=False,
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.username)
        # Password input
        self.password = TextInput(
            hint_text=self.language_manager.get_text('password'),
            password=True,
            multiline=False,
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.password)
        # Confirm password input
        self.confirm_password = TextInput(
            hint_text=self.language_manager.get_text('confirm_password'),
            password=True,
            multiline=False,
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.52},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.confirm_password)
        # Register button
        register_btn = Button(
            text=self.language_manager.get_text('sign_up'),
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.42},
            background_color=(0.3, 0.8, 0.3, 0.9)
        )
        register_btn.bind(on_press=self.register)
        self.main_layout.add_widget(register_btn)
        # Back to login button
        back_btn = CreamButton(
            text=self.language_manager.get_text('back_to_login'),
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        back_btn.bind(on_press=self.back_to_login)
        self.main_layout.add_widget(back_btn)
        self.add_widget(self.main_layout)
        self.main_layout.bind(size=self._update_bg_image, pos=self._update_bg_image)
    def _update_bg_image(self, *args):
        self.bg_image.size = self.main_layout.size
        self.bg_image.pos = self.main_layout.pos
    def update_theme(self):
        pass
    def register(self, instance):
        self.manager.current = 'home'
    def back_to_login(self, instance):
        self.manager.current = 'login'