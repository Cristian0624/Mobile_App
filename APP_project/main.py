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
from home import HomeScreen, ReminderScreen, BaseScreen, VoiceScreen
from home import IconButton, tr
from theme_manager import ThemeManager
# Import our new SettingsScreen
from settings_screen import SettingsScreen
# Keep these imports from their respective files
from login import LoginScreen
from register import RegisterScreen

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
    
    def add_user(self, username, password, email=""):
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = {
            "password": password,
            "email": email
        }
        self.save_users()
        return True, "User registered successfully"
    
    def verify_user(self, username, password):
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username]["password"] != password:
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

class CreamCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(CreamCheckBox, self).__init__(**kwargs)
        self.background_checkbox_normal = ''
        self.background_checkbox_down = ''
        self.color = (0.2, 0.2, 0.2, 1)
        self.active = False

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        main_layout = FullScreenBackground()
        
        content = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(10),
            size_hint=(None, None),
            width=dp(300),
            height=dp(450),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        with content.canvas.before:
            Color(0.95, 0.95, 0.95, 0.9)
            self.content_bg = Rectangle(pos=content.pos, size=content.size)
            content.bind(pos=self._update_content_bg, size=self._update_content_bg)
        
        title = CenteredLabel(
            text=tr('login').upper(), 
            font_size=dp(32), 
            size_hint_y=None, 
            height=dp(60), 
            bold=True, 
            color=(0.1, 0.1, 0.1, 1)
        )
        content.add_widget(title)
        
        self.status_label = CenteredLabel(
            text='', 
            font_size=dp(14), 
            size_hint_y=None, 
            height=dp(25), 
            color=(0.8, 0.2, 0.2, 1)
        )
        content.add_widget(self.status_label)
        
        username_label = Label(
            text=tr('username'), 
            size_hint_y=None, 
            height=dp(30),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(16),
            halign='left',
            valign='bottom'
        )
        username_label.bind(size=lambda *x: setattr(username_label, 'text_size', username_label.size))
        content.add_widget(username_label)
        
        self.username = StyledTextInput()
        content.add_widget(self.username)
        
        password_label = Label(
            text=tr('password'), 
            size_hint_y=None, 
            height=dp(30),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(16),
            halign='left',
            valign='bottom'
        )
        password_label.bind(size=lambda *x: setattr(password_label, 'text_size', password_label.size))
        content.add_widget(password_label)
        
        self.password = StyledTextInput(password=True)
        content.add_widget(self.password)
        
        show_password_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(40),
            orientation='horizontal',
            spacing=dp(10)
        )
        
        checkbox_container = BoxLayout(
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        
        with checkbox_container.canvas.before:
            Color(0.85, 0.82, 0.78, 1)
            Rectangle(pos=checkbox_container.pos, size=checkbox_container.size)
            checkbox_container.bind(pos=lambda *x: self._update_checkbox_bg(checkbox_container), 
                                  size=lambda *x: self._update_checkbox_bg(checkbox_container))
        
        self.show_password_checkbox = CheckBox(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            color=(0.2, 0.2, 0.2, 1),
            active=False
        )
        self.show_password_checkbox.bind(active=self.toggle_password_visibility)
        checkbox_container.add_widget(self.show_password_checkbox)
        
        show_password_layout.add_widget(checkbox_container)
        
        show_password_label = Label(
            text=tr('show_password'),
            font_size=dp(16),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            valign='middle'
        )
        show_password_label.bind(size=lambda *x: setattr(show_password_label, 'text_size', show_password_label.size))
        show_password_layout.add_widget(show_password_label)
        
        content.add_widget(show_password_layout)
        
        login_btn = CreamButton(text=tr('login'))
        login_btn.bind(on_press=self.login)
        content.add_widget(login_btn)
        
        register_btn = CreamButton(
            text=tr('sign_up'),
            background_color=(0.75, 0.72, 0.68, 1)
        )
        register_btn.bind(on_press=self.register)
        content.add_widget(register_btn)
        
        main_layout.login_container.add_widget(content)
        self.add_widget(main_layout)
    
    def _update_content_bg(self, instance, value):
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size
    
    def _update_checkbox_bg(self, checkbox_container):
        checkbox_container.canvas.before.clear()
        with checkbox_container.canvas.before:
            Color(0.85, 0.82, 0.78, 1)
            Rectangle(pos=checkbox_container.pos, size=checkbox_container.size)
    
    def toggle_password_visibility(self, checkbox, value):
        self.password.password = not value
    
    def login(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.status_label.text = "Please enter both username and password"
            self.status_label.color = (1, 0.5, 0.5, 1)
            return
        
        app = App.get_running_app()
        success, message = app.user_db.verify_user(username, password)
        
        if success:
            self.status_label.text = ""
            app.on_login_success(username)
        else:
            self.status_label.text = message
            self.status_label.color = (1, 0.5, 0.5, 1)
    
    def register(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        
        main_layout = FullScreenBackground()
        
        content = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(10),
            size_hint=(None, None),
            width=dp(300),
            height=dp(500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        with content.canvas.before:
            Color(0.95, 0.95, 0.95, 0.9)
            self.content_bg = Rectangle(pos=content.pos, size=content.size)
            content.bind(pos=self._update_content_bg, size=self._update_content_bg)
        
        title = CenteredLabel(
            text=tr('sign_up').upper(), 
            font_size=dp(32), 
            size_hint_y=None, 
            height=dp(60), 
            bold=True, 
            color=(0.1, 0.1, 0.1, 1)
        )
        content.add_widget(title)
        
        self.status_label = CenteredLabel(
            text='', 
            font_size=dp(14), 
            size_hint_y=None, 
            height=dp(25), 
            color=(0.8, 0.2, 0.2, 1)
        )
        content.add_widget(self.status_label)
        
        username_label = Label(
            text=tr('username'),
            font_size=dp(16),
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='bottom'
        )
        username_label.bind(size=lambda *x: setattr(username_label, 'text_size', username_label.size))
        content.add_widget(username_label)
        
        self.username = StyledTextInput()
        content.add_widget(self.username)
        
        email_label = Label(
            text=tr('email'),
            font_size=dp(16),
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='bottom'
        )
        email_label.bind(size=lambda *x: setattr(email_label, 'text_size', email_label.size))
        content.add_widget(email_label)
        
        self.email = StyledTextInput()
        content.add_widget(self.email)
        
        password_label = Label(
            text=tr('password'),
            font_size=dp(16),
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='bottom'
        )
        password_label.bind(size=lambda *x: setattr(password_label, 'text_size', password_label.size))
        content.add_widget(password_label)
        
        self.password = StyledTextInput(password=True)
        content.add_widget(self.password)
        
        checkbox_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None, 
            height=dp(40),
            spacing=dp(10)
        )
        
        checkbox_container = BoxLayout(
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        
        with checkbox_container.canvas.before:
            Color(0.85, 0.82, 0.78, 1)
            Rectangle(pos=checkbox_container.pos, size=checkbox_container.size)
            checkbox_container.bind(pos=lambda *x: self._update_checkbox_bg(checkbox_container), 
                                  size=lambda *x: self._update_checkbox_bg(checkbox_container))
        
        self.show_password_checkbox = CheckBox(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            color=(0.2, 0.2, 0.2, 1),
            active=False
        )
        self.show_password_checkbox.bind(active=self.toggle_password_visibility)
        checkbox_container.add_widget(self.show_password_checkbox)
        
        checkbox_row.add_widget(checkbox_container)
        
        show_password_label = Label(
            text=tr('show_password'),
            font_size=dp(16),
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            valign='middle'
        )
        show_password_label.bind(size=lambda *x: setattr(show_password_label, 'text_size', show_password_label.size))
        checkbox_row.add_widget(show_password_label)
        
        content.add_widget(checkbox_row)
        
        register_btn = CreamButton(text=tr('sign_up'))
        register_btn.bind(on_press=self.signup)
        content.add_widget(register_btn)
        
        back_btn = CreamButton(
            text=tr('back_to_login'),
            background_color=(0.75, 0.72, 0.68, 1)
        )
        back_btn.bind(on_press=self.back_to_login)
        content.add_widget(back_btn)
        
        main_layout.login_container.add_widget(content)
        self.add_widget(main_layout)
    
    def _update_content_bg(self, instance, value):
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size
    
    def _update_checkbox_bg(self, checkbox_container):
        checkbox_container.canvas.before.clear()
        with checkbox_container.canvas.before:
            Color(0.85, 0.82, 0.78, 1)
            Rectangle(pos=checkbox_container.pos, size=checkbox_container.size)
    
    def toggle_password_visibility(self, checkbox, value):
        self.password.password = not value
    
    def signup(self, instance):
        username = self.username.text.strip()
        email = self.email.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.status_label.text = "Username and password are required"
            self.status_label.color = (1, 0.5, 0.5, 1)
            return
        
        app = App.get_running_app()
        success, message = app.user_db.add_user(username, password, email)
        
        if success:
            self.status_label.text = "Registration successful!"
            self.status_label.color = (0.5, 1, 0.5, 1)
            
            self.username.text = ""
            self.email.text = ""
            self.password.text = ""
            
            Clock.schedule_once(lambda dt: self.back_to_login(None), 1.5)
        else:
            self.status_label.text = message
            self.status_label.color = (1, 0.5, 0.5, 1)
    
    def back_to_login(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.screen_manager = None
        self.user_db = UserDatabase()
        self.current_user = None
        
        # Create a theme manager that will be shared by all screens
        self.theme_manager = ThemeManager()
    
    def build(self):
        # Create the screen manager
        self.screen_manager = ScreenManager(transition=SlideTransition())
        
        # Set window size
        Window.size = (400, 700)
        
        # Create simplified screens for testing
        class DummyScreen(Screen):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                layout = BoxLayout(orientation='vertical')
                title = Label(
                    text=f"This is the {kwargs.get('name', 'unknown')} screen",
                    font_size=24
                )
                back_btn = Button(
                    text="Back to Home",
                    size_hint=(1, 0.1)
                )
                back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
                layout.add_widget(title)
                layout.add_widget(back_btn)
                self.add_widget(layout)

            def update_theme(self, *args):
                # Dummy method to prevent errors
                pass
                
            def update_username(self, username):
                # Dummy method to prevent errors
                pass
        
        # Import the real screens from home.py
        from home import HomeScreen, ReminderScreen, VoiceScreen
        
        # Add login and register screens
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(RegisterScreen(name='register'))
        
        # Use real screens where available
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.add_widget(ReminderScreen(name='reminder'))
        self.screen_manager.add_widget(VoiceScreen(name='voice'))
        
        # Create a dummy camera screen for MediScan
        self.screen_manager.add_widget(DummyScreen(name='mediscan'))
        
        # Set the login screen as the first screen
        self.screen_manager.current = 'login'
        
        # Set window background color
        self.update_theme()
        
        return self.screen_manager
    
    def on_start(self):
        """Called when the application starts"""
        # Apply the theme to all screens
        self.update_theme()
        
        # Bind to screen changes to ensure proper theme application
        self.screen_manager.bind(current=self.on_screen_change)
    
    def on_screen_change(self, instance, value):
        """Called when screen changes, ensures theme is applied to the new screen"""
        # Make sure theme is applied to the current screen
        if self.theme_manager.is_dark_mode:
            screen = self.screen_manager.current_screen
            if hasattr(screen, 'update_theme'):
                screen.update_theme()
    
    def on_login_success(self, username):
        # Set the current user
        self.current_user = username
        
        # Navigate to the home screen
        self.screen_manager.current = 'home'
        
        # Update the username display on the home screen
        home_screen = self.screen_manager.get_screen('home')
        home_screen.update_username(username)
    
    def update_theme(self, *args):
        # Update window background color based on current theme
        from kivy.core.window import Window
        if hasattr(self, 'theme_manager'):
            colors = self.theme_manager.get_colors()
            Window.clearcolor = colors['background']
            
            # Force update all screens
            if hasattr(self, 'screen_manager'):
                for screen_name in self.screen_manager.screen_names:
                    screen = self.screen_manager.get_screen(screen_name)
                    if hasattr(screen, 'update_theme'):
                        # Pass the theme manager to each screen's update_theme
                        screen.update_theme()

if __name__ == '__main__':
    MainApp().run() 