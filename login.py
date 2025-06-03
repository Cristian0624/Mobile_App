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
from kivy.app import App
from kivy.uix.widget import Widget
from home import RoundedButton
from database import UserDatabase
from kivy.clock import Clock

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        self.user_db = UserDatabase()  # Initialize the database
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
        
        # Add a semi-transparent dark overlay to darken the background image
        with self.main_layout.canvas.before:
            Color(0, 0, 0, 0.6) # Dark color with 60% opacity
            self.overlay_rect = Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
        self.main_layout.bind(pos=self._update_overlay, size=self._update_overlay)
        
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
        
        # Error label
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),
            size_hint=(0.6, None),
            height=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.72},
            font_size=dp(14)
        )
        self.main_layout.add_widget(self.error_label)
        
        # Username input
        self.username = TextInput(
            hint_text=self.language_manager.get_text('username'),
            multiline=False,
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
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
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)
        )
        self.main_layout.add_widget(self.password)
        
        # Container for Show password checkbox and label, centered
        show_password_container = BoxLayout(
            orientation='horizontal',
            size_hint=(0.6, None),
            height=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            spacing=dp(5)
        )

        # Show password checkbox
        self.show_password_checkbox = CheckBox(
            size_hint=(None, None),
            size=(dp(25), dp(25)),
            color=(0.2, 0.2, 0.2, 1),
            active=False
        )
        self.show_password_checkbox.bind(active=self.toggle_password_visibility)

        self.show_password_label = Label(
            text=self.language_manager.get_text('show_password'),
            font_size=dp(15),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(120), dp(30)),
            halign='left',
            valign='middle'
        )
        self.show_password_label.bind(size=self.show_password_label.setter('text_size'))

        show_password_container.add_widget(Widget(size_hint_x=None, width=dp(10)))
        show_password_container.add_widget(self.show_password_checkbox)
        show_password_container.add_widget(self.show_password_label)
        show_password_container.add_widget(Widget())

        self.main_layout.add_widget(show_password_container)
        
        # Login button
        login_btn = RoundedButton(
            text=self.language_manager.get_text('login').upper(),
            font_size=dp(16),
            bold=True,
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            bg_color=(0x44/255, 0x61/255, 0xcc/255, 1),  # Blue background (#4461cc)
            text_color=(1, 1, 1, 1)  # White text
        )
        login_btn.bind(on_release=self.login)
        self.main_layout.add_widget(login_btn)
        
        # Sign On button
        signon_btn = RoundedButton(
            text="REGISTER",
            font_size=dp(16),
            bold=True,
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            bg_color=(0xf4/255, 0xf6/255, 0xff/255, 1),  # White background (#f4f6ff)
            text_color=(0x44/255, 0x61/255, 0xcc/255, 1)  # Blue text (#4461cc)
        )
        signon_btn.bind(on_release=self.go_to_register)
        self.main_layout.add_widget(signon_btn)
        
        self.add_widget(self.main_layout)
        
        # Bind background image size to layout size
        self.main_layout.bind(size=self._update_bg_image, pos=self._update_bg_image)
    
    def _update_bg_image(self, *args):
        self.bg_image.size = self.main_layout.size
        self.bg_image.pos = self.main_layout.pos
    
    def _update_overlay(self, instance, value):
        # Update the position and size of the overlay rectangle
        self.overlay_rect.pos = instance.pos
        self.overlay_rect.size = instance.size
    
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
                elif child.text == "REGISTER":
                    child.text = "REGISTER"
    
    def toggle_password_visibility(self, checkbox, value):
        self.password.password = not value
    
    def login(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.error_label.text = self.language_manager.get_text('please_fill_all_fields')
            Clock.schedule_once(lambda dt: setattr(self.error_label, 'text', ''), 5)
            return
            
        success, message = self.user_db.verify_user(username, password)
        
        if not success:
            self.error_label.text = message
            Clock.schedule_once(lambda dt: setattr(self.error_label, 'text', ''), 5)
            return
            
        # Only proceed if authentication was successful
        app = App.get_running_app()
        app.on_login_success(username)
        self.manager.current = 'home'
        self.error_label.text = ''
        # Clear the input fields
        self.username.text = ''
        self.password.text = ''
    
    def go_to_register(self, instance):
        self.manager.current = 'register'
        self.error_label.text = '' 