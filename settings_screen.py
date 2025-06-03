from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.popup import Popup
from theme_manager import ThemeManager
from language_manager import LanguageManager
from home import BaseScreen, tr, RoundedButton, IconButton

class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        # First call super without auto_update_theme to prevent premature theme update
        super(SettingsScreen, self).__init__(auto_update_theme=False, **kwargs)
        self.language_manager = LanguageManager()
        self.theme_manager = ThemeManager()
        
        # Settings title - moved to the top
        self.title_label = Label(
            text=tr('settings'),
            font_size=dp(24),
            bold=True,
            size_hint=(1, None),
            height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.main_layout.add_widget(self.title_label)
        
        # Main content area - adjusted padding from top
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(100), dp(20), dp(20)],  # Increased top padding to accommodate title
            size_hint=(1, 1)
        )
        
        # Create settings controls
        # 1. Dark Mode
        dark_mode_row = self._create_setting_row(tr('dark_mode'))
        self.dark_mode_switch = dark_mode_row.children[0]  # Get the switch widget
        self.dark_mode_switch.active = self.theme_manager.is_dark_mode
        self.dark_mode_switch.bind(active=self.toggle_dark_mode)
        content_layout.add_widget(dark_mode_row)
        
        # 2. Notifications
        notifications_row = self._create_setting_row(tr('notifications'))
        content_layout.add_widget(notifications_row)
        
        # 3. Sound
        sound_row = self._create_setting_row(tr('sound'))
        content_layout.add_widget(sound_row)
        
        # 4. Vibration
        vibration_row = self._create_setting_row(tr('vibration'))
        content_layout.add_widget(vibration_row)
        
        # 5. Language
        language_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50)
        )
        
        self.language_title = Label(
            text=tr('language'),
            font_size=dp(18),
            halign='left',
            valign='center',
            size_hint=(0.5, 1)
        )
        self.language_title.bind(size=self.language_title.setter('text_size'))
        
        # Map language codes to display names
        lang_names = {
            'en': 'English',
            'ro': 'Română',
            'ru': 'Русский'
        }
        
        # Create spinner for language selection with theme-based styling
        self.language_spinner = Spinner(
            text=lang_names.get(self.language_manager.current_language, 'English'),
            values=[lang_names[code] for code in ['en', 'ro', 'ru']],
            size_hint=(0.5, 0.8),
            pos_hint={'center_y': 0.5},
            font_size=dp(16),
            background_normal='',
            background_color=(0.85, 0.85, 0.85, 1) if not self.theme_manager.is_dark_mode else (0.3, 0.3, 0.3, 1)
        )
        self.language_spinner.bind(text=self.on_language_change)
        
        language_row.add_widget(self.language_title)
        language_row.add_widget(self.language_spinner)
        content_layout.add_widget(language_row)
        
        # Add some spacing
        content_layout.add_widget(Widget(size_hint_y=1))
        
        # Add logout button at the bottom
        self.logout_button = RoundedButton(
            text=tr('logout'),
            size_hint=(0.5, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            bg_color=(0.9, 0.3, 0.3, 1),  # Red color
            font_size=dp(18)
        )
        self.logout_button.bind(on_release=self.logout)
        content_layout.add_widget(self.logout_button)
        
        # Add content to main layout
        self.main_layout.add_widget(content_layout)
        
        # Now call update_theme manually since we disabled auto_update_theme
        self.update_theme()
        
        # Bind theme changes for future updates
        self.theme_manager.bind(is_dark_mode=self.update_theme)
    
    def _create_setting_row(self, label_text, default_active=True):
        """Helper method to create a setting row with a label and switch"""
        row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50)
        )
        
        label = Label(
            text=label_text,
            font_size=dp(18),
            halign='left',
            valign='center',
            size_hint=(0.7, 1)
        )
        label.bind(size=label.setter('text_size'))
        
        # Create a switch that works correctly
        switch = Switch(
            size_hint=(0.3, 1),
            pos_hint={'center_y': 0.5}
        )
        switch.active = default_active
        
        row.add_widget(label)
        row.add_widget(switch)
        return row
    
    def update_theme(self, *args):
        """Update UI based on theme"""
        super(SettingsScreen, self).update_theme(*args)
        
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update title color
        if hasattr(self, 'title_label'):
            self.title_label.color = colors['text']
            
        # Update language title if it exists
        if hasattr(self, 'language_title'):
            self.language_title.color = colors['text']

        # Update language spinner colors based on theme
        if hasattr(self, 'language_spinner'):
            self.language_spinner.background_color = (0.3, 0.3, 0.3, 1) if is_dark else (0.85, 0.85, 0.85, 1)
            self.language_spinner.color = (0.9, 0.9, 0.9, 1) if is_dark else (0.1, 0.1, 0.1, 1)
    
    def toggle_dark_mode(self, switch, value):
        """Toggle dark mode"""
        self.theme_manager.set_dark_mode(value)
    
    def on_language_change(self, spinner, text):
        """Handle language change"""
        # Map display names to language codes
        lang_map = {'English': 'en', 'Română': 'ro', 'Русский': 'ru'}
        lang_code = lang_map.get(text, 'en')
        
        # Update language
        self.language_manager.set_language(lang_code)
        
        # Show message about app restart
        toast = Popup(
            title='',
            content=Label(text=tr('restart_for_language')),
            size_hint=(None, None),
            size=(dp(300), dp(100)),
            auto_dismiss=True
        )
        toast.open()
        Clock.schedule_once(lambda dt: toast.dismiss(), 2)
    
    def logout(self, instance):
        """Log out and return to login screen"""
        app = App.get_running_app()
        app.current_user = None
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'