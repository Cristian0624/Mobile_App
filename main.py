from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
import json
import os
# Import only what's available in home.py
from home import HomeScreen, ReminderScreen, BaseScreen, VoiceScreen, InitialScreen, SignupScreen, MediScanScreen
from home import IconButton, tr, RoundedButton
from theme_manager import ThemeManager
# Import our new SettingsScreen
from settings_screen import SettingsScreen
# Keep these imports from their respective files
from login import LoginScreen
from register import RegisterScreen
from cream_button import CreamButton
from kivy.uix.image import Image
from language_manager import LanguageManager
from database import UserDatabase

# User database management
class UserDatabase:
    def __init__(self):
        self.db_file = "users.json"
        self.users = self.load_users()
        
    def load_users(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f)
    
    def add_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = password
        self.save_users()
        return True, "User registered successfully"
    
    def verify_user(self, username, password):
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username] != password:
            return False, "Incorrect password"
            
        return True, "Login successful"

# Create a full-screen background 
class FullScreenBackground(FloatLayout):
    def __init__(self, **kwargs):
        super(FullScreenBackground, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.99, 0.99, 0.99, 1)  # Light cream background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.login_container = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint=(1, 1)
        )
        self.add_widget(self.login_container)
    
    def _update_rect(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class CenteredLabel(Label):
    def __init__(self, **kwargs):
        super(CenteredLabel, self).__init__(**kwargs)
        self.halign = 'center'
        self.valign = 'middle'
        self.text_size = self.size
        if 'color' not in kwargs:
            self.color = (0, 0, 0, 1)
        self.bind(size=self._update_text_size)
        
    def _update_text_size(self, instance, value):
        self.text_size = self.size

class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super(StyledTextInput, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = (0.1, 0.1, 0.1, 1)
        self.cursor_color = (0.1, 0.5, 0.9, 1)
        self.font_size = dp(18)
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        self.multiline = False
        self.halign = 'left'
        self.size_hint_y = None
        self.height = dp(45)

class CreamCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(CreamCheckBox, self).__init__(**kwargs)
        self.background_checkbox_normal = ''
        self.background_checkbox_down = ''
        self.color = (0.2, 0.2, 0.2, 1)
        self.active = False

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        self.user_db = UserDatabase()  # Initialize the database
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
            size_hint=(0.6, None),
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
            background_color=(1, 1, 1, 0.8)  # Transparent white background
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
            background_color=(1, 1, 1, 0.8)  # Transparent white background
        )
        self.main_layout.add_widget(self.password)

        # Confirm password input
        self.confirm_password = TextInput(
            hint_text="Confirm Password",
            password=True,
            multiline=False,
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            padding=[dp(10), dp(10)],
            font_size=dp(16),
            background_color=(1, 1, 1, 0.8)  # Transparent white background
        )
        self.main_layout.add_widget(self.confirm_password)
        
        # Container for Show password checkbox and label, centered
        show_password_container = BoxLayout(
            orientation='horizontal',
            size_hint=(0.6, None),
            height=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.38},
            spacing=dp(5)
        )

        # Register button
        register_btn = RoundedButton(
            text=self.language_manager.get_text('sign_up').upper(),
            font_size=dp(16),
            bold=True,
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.35},  # Adjusted to match login page
            bg_color=(0x44/255, 0x61/255, 0xcc/255, 1),  # Blue background (#4461cc)
            text_color=(1, 1, 1, 1)  # White text
        )
        register_btn.bind(on_release=self.register)
        self.main_layout.add_widget(register_btn)

        # Back to login button
        back_btn = RoundedButton(
            text=self.language_manager.get_text('back_to_login').upper(),
            font_size=dp(16),
            bold=True,
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},  # Adjusted to match login page
            bg_color=(0xf4/255, 0xf6/255, 0xff/255, 1),  # White background (#f4f6ff)
            text_color=(0x44/255, 0x61/255, 0xcc/255, 1)  # Blue text (#4461cc)
        )
        back_btn.bind(on_release=self.back_to_login)
        self.main_layout.add_widget(back_btn)

        self.add_widget(self.main_layout)
        self.main_layout.bind(size=self._update_bg_image, pos=self._update_bg_image)

    def _update_bg_image(self, *args):
        self.bg_image.size = self.main_layout.size
        self.bg_image.pos = self.main_layout.pos

    def update_theme(self):
        pass

    def register(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()
        
        if not username or not password or not confirm_password:
            self.error_label.text = self.language_manager.get_text('please_fill_all_fields')
            Clock.schedule_once(lambda dt: setattr(self.error_label, 'text', ''), 5)
            return
            
        if password != confirm_password:
            self.error_label.text = self.language_manager.get_text('passwords_dont_match')
            Clock.schedule_once(lambda dt: setattr(self.error_label, 'text', ''), 5)
            return
            
        if self.user_db.add_user(username, password):
            self.manager.current = 'login'
            self.error_label.text = ''
            self.username.text = ''
            self.password.text = ''
            self.confirm_password.text = ''
        else:
            self.error_label.text = self.language_manager.get_text('username_exists')
            Clock.schedule_once(lambda dt: setattr(self.error_label, 'text', ''), 5)

    def back_to_login(self, instance):
        self.manager.current = 'login'
        self.error_label.text = ''

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.current_user = None
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        
        # Set window size to match Android phone screen
        Window.size = (400, 680)  # Common Android phone screen size
        Window.minimum_width = 400
        Window.minimum_height = 680
        Window.maximum_width = 400
        Window.maximum_height = 680
        Window.clearcolor = (0.98, 0.98, 0.98, 1)  # Light background color
        
        # Ensure window size restrictions are applied
        Window.borderless = False
        Window.resizable = False

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(InitialScreen(name='initial'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ReminderScreen(name='reminder'))
        sm.add_widget(MediScanScreen(name='mediscan'))
        sm.add_widget(VoiceScreen(name='voice'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'initial'
        return sm
    
    def update_theme(self, *args):
        # Update window background color based on current theme
        colors = self.theme_manager.get_colors()
        Window.clearcolor = colors['background']

    def on_login_success(self, username):
        self.current_user = username
        # Update username in all screens that need it
        for screen in self.root.screens:
            if hasattr(screen, 'update_username'):
                screen.update_username(username)
        self.root.current = 'home'

if __name__ == '__main__':
    MainApp().run() 