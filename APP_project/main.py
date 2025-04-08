from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from home import HomeScreen, ReminderScreen, CameraScreen, VoiceScreen, SettingsScreen
from home import IconButton
from loggin import LoginScreen, RegisterScreen, UserDatabase

# Custom Button class with cream background
class CreamButton(Button):
    def __init__(self, **kwargs):
        super(CreamButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.85, 0.82, 0.78, 1)  # Darker cream/beige color
        self.color = (0.1, 0.1, 0.1, 1)  # Dark text
        self.bold = True

# Override the IconButton methods for press and release
original_on_press = IconButton.on_press
original_on_release = IconButton.on_release

def new_on_press(self):
    # Turn icon and text black
    self.icon_image.color = (0, 0, 0, 1)
    self.label.color = (0, 0, 0, 1)
    
    # Call the original method for navigation
    if hasattr(App.get_running_app().root.current_screen, 'navigate_to'):
        App.get_running_app().root.current_screen.navigate_to(self.icon_type)

def new_on_release(self):
    # Restore original colors
    self.icon_image.color = (1, 1, 1, 1)
    self.label.color = (0.1, 0.1, 0.1, 1)

# Override the methods
IconButton.on_press = new_on_press
IconButton.on_release = new_on_release

# Override the Button class in the home module
from home import BaseScreen
original_init = BaseScreen.__init__

def new_init(self, **kwargs):
    # Call the original init method
    original_init(self, **kwargs)
    
    # Replace the back arrow button with our custom cream button
    if hasattr(self, 'main_layout'):
        # Find and remove the original button
        for child in list(self.main_layout.children):
            if isinstance(child, Button) and child.text == '<':
                self.main_layout.remove_widget(child)
        
        # Add our custom cream button
        back_arrow = CreamButton(
            text='<',
            font_size=30,
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'x': 0.02, 'top': 0.98}
        )
        back_arrow.bind(on_press=self.go_back_home)
        self.main_layout.add_widget(back_arrow)

# Replace the __init__ method
BaseScreen.__init__ = new_init

# Original settings screen init
original_settings_init = SettingsScreen.__init__

# New settings screen init to ensure logout button has cream color
def new_settings_init(self, **kwargs):
    # Call original init
    original_settings_init(self, **kwargs)
    
    # Find and remove the original logout button
    for child in list(self.main_layout.children):
        if isinstance(child, Button) and child.text == 'Logout':
            self.main_layout.remove_widget(child)
    
    # Add our custom cream logout button
    logout_btn = CreamButton(
        text='Logout',
        font_size=16,
        size_hint=(None, None),
        size=(80, 40),
        pos_hint={'right': 0.98, 'top': 0.98}
    )
    logout_btn.bind(on_press=self.logout)
    self.main_layout.add_widget(logout_btn)

# Replace the SettingsScreen.__init__ method
SettingsScreen.__init__ = new_settings_init

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.user_db = UserDatabase()
        self.current_user = None
    
    def build(self):
        # Set window size for desktop testing (mobile-like aspect ratio)
        Window.size = (400, 700)
        
        # Create screen manager with transition
        sm = ScreenManager(transition=SlideTransition())
        
        # Add login screen
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)
        
        # Add register screen
        register_screen = RegisterScreen(name='register')
        sm.add_widget(register_screen)
        
        # Add home screen
        home_screen = HomeScreen(name='home')
        sm.add_widget(home_screen)
        
        # Start with login screen
        sm.current = 'login'
        
        return sm
    
    def on_login_success(self, username):
        """Called when login is successful"""
        self.current_user = username
        
        # Update username on home screen
        home_screen = self.root.get_screen('home')
        home_screen.update_username(username)
        
        # Navigate to home screen
        self.root.transition = SlideTransition(direction='left')
        self.root.current = 'home'

if __name__ == '__main__':
    MainApp().run() 