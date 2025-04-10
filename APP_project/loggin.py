from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.utils import platform
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import json
import os

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
        
        # Use a colored rectangle to fill the entire background first
        with self.canvas.before:
            Color(0.99, 0.99, 0.99, 1)  # Light cream background to match home screen
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add a container for login elements with semi-transparent background
        # Make sure it's centered
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
        # Ensure text color has good contrast
        if 'color' not in kwargs:
            self.color = (0, 0, 0, 1)  # Black text by default
        self.bind(size=self._update_text_size)
        
    def _update_text_size(self, instance, value):
        self.text_size = self.size
        
class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super(StyledTextInput, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.9)
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0.1, 0.5, 0.9, 1)
        self.font_size = dp(18)
        self.padding = [15, 15]
        self.multiline = False
        self.halign = 'center'
        
class StyledButton(Button):
    def __init__(self, **kwargs):
        super(StyledButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = kwargs.get('background_color', (0.1, 0.5, 0.9, 1))
        self.color = (1, 1, 1, 1)
        self.font_size = dp(18)
        self.bold = True
        self.halign = 'center'
        
class StyledCheckBox(CheckBox):
    def __init__(self, **kwargs):
        # Remove active_color if it's in kwargs
        if 'active_color' in kwargs:
            del kwargs['active_color']
            
        super(StyledCheckBox, self).__init__(**kwargs)
        # Use cream background when unchecked
        self.background_checkbox_normal = ''
        self.background_checkbox_down = ''
        # Green checkmark when checked
        self.color = (0.2, 0.7, 0.2, 1)  # Green color for visibility

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        # Use full screen background
        main_layout = FullScreenBackground()
        
        # Content box - center in the screen
        content = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(10),
            size_hint=(None, None),
            width=dp(300),
            height=dp(450),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Add a semi-transparent background to the content box
        with content.canvas.before:
            Color(0.95, 0.95, 0.95, 0.9)  # Light background for content
            self.content_bg = Rectangle(pos=content.pos, size=content.size)
            content.bind(pos=self._update_content_bg, size=self._update_content_bg)
                          
        # Add title
        title = CenteredLabel(
            text='LOG IN', 
            font_size=dp(32), 
            size_hint_y=None, 
            height=dp(60), 
            bold=True, 
            color=(0.1, 0.1, 0.1, 1)
        )
        content.add_widget(title)
        
        # Status message (for errors/feedback)
        self.status_label = CenteredLabel(
            text='', 
            font_size=dp(14), 
            size_hint_y=None, 
            height=dp(25), 
            color=(0.8, 0.2, 0.2, 1)
        )
        content.add_widget(self.status_label)
        
        # Username input
        username_label = CenteredLabel(
            text='Username', 
            size_hint_y=None, 
            height=dp(25),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(18)
        )
        content.add_widget(username_label)
        
        self.username = StyledTextInput(size_hint_y=None, height=dp(45))
        content.add_widget(self.username)
        
        # Password input - reduced spacing
        password_label = CenteredLabel(
            text='Password', 
            size_hint_y=None, 
            height=dp(25),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(18)
        )
        content.add_widget(password_label)
        
        self.password = StyledTextInput(password=True, size_hint_y=None, height=dp(45))
        content.add_widget(self.password)
        
        # Show password checkbox - with cream background
        show_password_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(40),
            orientation='horizontal',
            padding=[dp(20), 0]
        )
        
        # Custom checkbox with cream background
        self.show_password_checkbox = StyledCheckBox(
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        # Add a cream background for the checkbox
        with self.show_password_checkbox.canvas.before:
            Color(0.85, 0.82, 0.78, 1)  # Cream color
            self.check_bg = Rectangle(
                pos=self.show_password_checkbox.pos, 
                size=self.show_password_checkbox.size
            )
            self.show_password_checkbox.bind(pos=self._update_check_bg, size=self._update_check_bg)
            
        self.show_password_checkbox.bind(active=self.show_password)
        show_password_layout.add_widget(self.show_password_checkbox)
        
        # Add clear label for the checkbox
        show_password_text = Label(
            text='Show Password',
            color=(0.1, 0.1, 0.1, 1),
            font_size=dp(16),
            bold=True,
            halign='left'
        )
        show_password_layout.add_widget(show_password_text)
        
        content.add_widget(show_password_layout)
        
        # Login button
        login_btn = StyledButton(
            text='Login', 
            size_hint_y=None, 
            height=dp(50),
            background_color=(0.85, 0.82, 0.78, 1)  # Cream color
        )
        login_btn.bind(on_press=self.login)
        content.add_widget(login_btn)
        
        # Register button - closer to login
        register_btn = StyledButton(
            text='Sign Up', 
            background_color=(0.75, 0.72, 0.68, 1),  # Slightly darker cream
            size_hint_y=None, 
            height=dp(50)
        )
        register_btn.bind(on_press=self.register)
        content.add_widget(register_btn)
        
        main_layout.login_container.add_widget(content)
        self.add_widget(main_layout)
    
    def _update_content_bg(self, instance, value):
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size
    
    def _update_check_bg(self, instance, value):
        self.check_bg.pos = instance.pos
        self.check_bg.size = instance.size
    
    def show_password(self, checkbox, value):
        self.password.password = not value
    
    def login(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.status_label.text = "Please enter both username and password"
            self.status_label.color = (1, 0.5, 0.5, 1)  # Light red
            return
        
        app = App.get_running_app()
        success, message = app.user_db.verify_user(username, password)
        
        if success:
            self.status_label.text = ""
            app.on_login_success(username)
        else:
            self.status_label.text = message
            self.status_label.color = (1, 0.5, 0.5, 1)  # Light red
    
    def register(self, instance):
        # Switch to register screen with animation
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'register'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        
        # Use full screen background
        main_layout = FullScreenBackground()
        
        # Content box - more compact and centered
        content = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(10),
            size_hint=(None, None),
            width=dp(300),
            height=dp(500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Add a semi-transparent background to the content box
        with content.canvas.before:
            Color(0.95, 0.95, 0.95, 0.9)  # Light background for content
            self.content_bg = Rectangle(pos=content.pos, size=content.size)
            content.bind(pos=self._update_content_bg, size=self._update_content_bg)
        
        # Add title
        title = CenteredLabel(
            text='SIGN UP', 
            font_size=dp(32), 
            size_hint_y=None, 
            height=dp(60), 
            bold=True, 
            color=(0.1, 0.1, 0.1, 1)
        )
        content.add_widget(title)
        
        # Status message (for errors/feedback)
        self.status_label = CenteredLabel(
            text='', 
            font_size=dp(14), 
            size_hint_y=None, 
            height=dp(25), 
            color=(0.8, 0.2, 0.2, 1)
        )
        content.add_widget(self.status_label)
        
        # Username input
        username_label = CenteredLabel(
            text='Username', 
            size_hint_y=None, 
            height=dp(25),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(18)
        )
        content.add_widget(username_label)
        
        self.username = StyledTextInput(size_hint_y=None, height=dp(45))
        content.add_widget(self.username)
        
        # Email input - reduced spacing
        email_label = CenteredLabel(
            text='Email', 
            size_hint_y=None, 
            height=dp(25),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(18)
        )
        content.add_widget(email_label)
        
        self.email = StyledTextInput(size_hint_y=None, height=dp(45))
        content.add_widget(self.email)
        
        # Password input - reduced spacing
        password_label = CenteredLabel(
            text='Password', 
            size_hint_y=None, 
            height=dp(25),
            color=(0.1, 0.1, 0.1, 1), 
            font_size=dp(18)
        )
        content.add_widget(password_label)
        
        self.password = StyledTextInput(password=True, size_hint_y=None, height=dp(45))
        content.add_widget(self.password)
        
        # Show password checkbox - with cream background
        show_password_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(40),
            orientation='horizontal',
            padding=[dp(20), 0]
        )
        
        # Custom checkbox with cream background
        self.show_password_checkbox = StyledCheckBox(
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        # Add a cream background for the checkbox
        with self.show_password_checkbox.canvas.before:
            Color(0.85, 0.82, 0.78, 1)  # Cream color
            self.check_bg = Rectangle(
                pos=self.show_password_checkbox.pos, 
                size=self.show_password_checkbox.size
            )
            self.show_password_checkbox.bind(pos=self._update_check_bg, size=self._update_check_bg)
            
        self.show_password_checkbox.bind(active=self.show_password)
        show_password_layout.add_widget(self.show_password_checkbox)
        
        # Add clear label for the checkbox
        show_password_text = Label(
            text='Show Password',
            color=(0.1, 0.1, 0.1, 1),
            font_size=dp(16),
            bold=True,
            halign='left'
        )
        show_password_layout.add_widget(show_password_text)
        
        content.add_widget(show_password_layout)
        
        # Sign Up button - closer spacing
        signup_btn = StyledButton(
            text='Sign Up', 
            size_hint_y=None, 
            height=dp(50),
            background_color=(0.85, 0.82, 0.78, 1)  # Cream color
        )
        signup_btn.bind(on_press=self.signup)
        content.add_widget(signup_btn)
        
        # Back button
        back_btn = StyledButton(
            text='Back to Login', 
            background_color=(0.75, 0.72, 0.68, 1),  # Slightly darker cream
            size_hint_y=None, 
            height=dp(50)
        )
        back_btn.bind(on_press=self.back_to_login)
        content.add_widget(back_btn)
        
        main_layout.login_container.add_widget(content)
        self.add_widget(main_layout)
    
    def _update_content_bg(self, instance, value):
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size
    
    def _update_check_bg(self, instance, value):
        self.check_bg.pos = instance.pos
        self.check_bg.size = instance.size
    
    def show_password(self, checkbox, value):
        self.password.password = not value
    
    def signup(self, instance):
        username = self.username.text.strip()
        email = self.email.text.strip()
        password = self.password.text.strip()
        
        # Validate inputs
        if not username or not password:
            self.status_label.text = "Username and password are required"
            self.status_label.color = (1, 0.5, 0.5, 1)  # Light red
            return
        
        # Add user to database
        app = App.get_running_app()
        success, message = app.user_db.add_user(username, password, email)
        
        if success:
            self.status_label.text = "Registration successful!"
            self.status_label.color = (0.5, 1, 0.5, 1)  # Light green
            
            # Clear fields
            self.username.text = ""
            self.email.text = ""
            self.password.text = ""
            
            # Navigate to login after a delay
            Clock.schedule_once(lambda dt: self.back_to_login(None), 1.5)
        else:
            self.status_label.text = message
            self.status_label.color = (1, 0.5, 0.5, 1)  # Light red
    
    def back_to_login(self, instance):
        # Switch to login screen with animation
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'

# Hello World screen that appears after login
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        # Create layout for Hello World page
        main_layout = FullScreenBackground()
        
        content_layout = BoxLayout(orientation='vertical', 
                                padding=dp(20), 
                                spacing=dp(20))
        
        # Welcome message
        self.welcome_label = CenteredLabel(
            text="Hello, World!",
            font_size=dp(32),
            bold=True,
            color=(1, 1, 1, 1)
        )
        content_layout.add_widget(self.welcome_label)
        
        # User name display
        self.user_label = CenteredLabel(
            text="Welcome, User!",
            font_size=dp(24),
            color=(1, 1, 1, 1)
        )
        content_layout.add_widget(self.user_label)
        
        # Add a nice message
        message_label = CenteredLabel(
            text="You have successfully logged in to your account.",
            font_size=dp(18),
            color=(1, 1, 1, 0.9)
        )
        content_layout.add_widget(message_label)
        
        # Add some space
        content_layout.add_widget(BoxLayout(size_hint_y=None, height=dp(30)))
        
        # Logout button
        logout_btn = StyledButton(
            text='Logout',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5}
        )
        logout_btn.bind(on_press=self.logout)
        content_layout.add_widget(logout_btn)
        
        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)
    
    def on_pre_enter(self):
        # Update welcome message with current user's name when entering screen
        app = App.get_running_app()
        if app and hasattr(app, 'current_user'):
            self.user_label.text = f"Welcome, {app.current_user}!"
    
    def logout(self, instance):
        # Clear current user and go back to login
        app = App.get_running_app()
        if app:
            app.current_user = None
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.user_db = UserDatabase()
        self.current_user = None
        
    def build(self):
        # Set window size based on platform
        if platform == 'android':
            # For Android, we'll let the system determine the window size
            pass
        else:
            # For desktop testing, use a mobile-like aspect ratio (taller than wider)
            Window.size = (400, 700)
        
        # Create and return screen manager
        sm = ScreenManager(transition=SlideTransition())
        
        # Add login screen
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)
        
        # Add register screen
        register_screen = RegisterScreen(name='register')
        sm.add_widget(register_screen)
        
        # Add home screen (Hello World)
        home_screen = HomeScreen(name='home')
        sm.add_widget(home_screen)
        
        return sm

if __name__ == '__main__':
    MyApp().run()