from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line
from kivy.graphics import StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from datetime import datetime, timedelta
import os
import threading
import math
from round_button import RoundButtonArea
from theme_manager import ThemeManager
from kivy.uix.relativelayout import RelativeLayout

# Define language settings
LANGUAGES = ['en', 'ro', 'ru']
CURRENT_LANGUAGE = {'lang': 'en'}  # Default language

# Translation dictionaries
LANG_DICT = {
    'en': {
        'login': 'Login',
        'username': 'Username',
        'password': 'Password',
        'register': 'Register',
        'home_page': 'Home',
        'welcome': 'Welcome',
        'settings': 'Settings',
        'notifications': 'Notifications',
        'dark_mode': 'Dark Mode',
        'sound': 'Sound',
        'vibration': 'Vibration',
        'language': 'Language',
        'logout': 'Logout',
        'add': 'ADD',
        'no_reminders_yet': 'No antibiotic reminders yet.\nTap \'+\' to create your first reminder.',
        'ready': 'READY',
        'due_now': 'DUE NOW',
        'minutes': 'min',
        'taken': 'TAKEN',
        'take_now': 'TAKE NOW',
        'delete': 'Delete',
        'edit': 'Edit'
    },
    'ro': {
        'login': 'Autentificare',
        'username': 'Nume utilizator',
        'password': 'Parolă',
        'register': 'Înregistrare',
        'home_page': 'Acasă',
        'welcome': 'Bine ați venit',
        'settings': 'Setări',
        'notifications': 'Notificări',
        'dark_mode': 'Mod întunecat',
        'sound': 'Sunet',
        'vibration': 'Vibrație',
        'language': 'Limbă',
        'logout': 'Deconectare',
        'add': 'ADAUGĂ',
        'no_reminders_yet': 'Nu există memento-uri pentru antibiotice.\nAtinge \'+\' pentru a crea primul reminder.',
        'ready': 'GATA',
        'due_now': 'ACUM',
        'minutes': 'min',
        'taken': 'LUAT',
        'take_now': 'IA ACUM',
        'delete': 'Șterge',
        'edit': 'Editează'
    },
    'ru': {
        'login': 'Вход',
        'username': 'Имя пользователя',
        'password': 'Пароль',
        'register': 'Регистрация',
        'home_page': 'Главная',
        'welcome': 'Добро пожаловать',
        'settings': 'Настройки',
        'notifications': 'Уведомления',
        'dark_mode': 'Темный режим',
        'sound': 'Звук',
        'vibration': 'Вибрация',
        'language': 'Язык',
        'logout': 'Выход',
        'add': 'ДОБАВИТЬ',
        'no_reminders_yet': 'Нет напоминаний о приеме антибиотиков.\nНажмите \'+\' чтобы создать первое напоминание.',
        'ready': 'ГОТОВО',
        'due_now': 'СЕЙЧАС',
        'minutes': 'мин',
        'taken': 'ПРИНЯТО',
        'take_now': 'ПРИНЯТЬ',
        'delete': 'Удалить',
        'edit': 'Изменить'
    }
}

# Global translation function
def tr(key):
    lang = CURRENT_LANGUAGE['lang']
    return LANG_DICT.get(lang, LANG_DICT['en']).get(key, key)

# Language Manager for handling translations
from kivy.event import EventDispatcher
from kivy.properties import StringProperty

class LanguageManager(EventDispatcher):
    """
    Manages language settings for the application.
    Implemented as a singleton to ensure consistent language across the app.
    """
    _instance = None
    current_language = StringProperty('en')  # Default to English
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            EventDispatcher.__init__(cls._instance)
            cls._instance.current_language = CURRENT_LANGUAGE['lang']
        return cls._instance
    
    def __init__(self):
        """Initialize language manager"""
        # This will only be called once due to the singleton pattern
        if not hasattr(self, 'is_initialized'):
            self.is_initialized = True
    
    def set_language(self, lang_code):
        """Set the current language"""
        if lang_code in LANGUAGES:
            # Update global language
            CURRENT_LANGUAGE['lang'] = lang_code
            # Update instance language - this triggers bindings
            self.current_language = lang_code
    
    def get_language(self):
        """Get the current language code"""
        return self.current_language
    
    def get_text(self, key):
        """Get translated text for a key"""
        lang = self.current_language
        
        if lang in LANG_DICT and key in LANG_DICT[lang]:
            return LANG_DICT[lang][key]
        
        # Fallback to English
        if 'en' in LANG_DICT and key in LANG_DICT['en']:
            return LANG_DICT['en'][key]
        
        # Return the key itself if not found
        return key

# Base Screen for all other screens
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        # Extract auto_update_theme parameter with default value True
        self.auto_update_theme = kwargs.pop('auto_update_theme', True)
        
        super(BaseScreen, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        
        # Main layout with theme-based background
        self.main_layout = FloatLayout()
        
        # Set background color based on theme
        with self.main_layout.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Default to white
            self.bg_rect = Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
            self.main_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add a back arrow button to return to home
        self.back_button = Button(
            text='<',
            font_size=dp(24),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'x': 0, 'top': 1},
            background_normal='',
            background_color=(0.85, 0.82, 0.78, 1) if not self.theme_manager.is_dark_mode else (0.3, 0.3, 0.3, 1),
            color=(0.1, 0.1, 0.1, 1) if not self.theme_manager.is_dark_mode else (0.9, 0.9, 0.9, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(self.back_button)
        
        self.add_widget(self.main_layout)
        
        # Update theme if auto_update_theme is True
        if self.auto_update_theme:
            self.update_theme()
        
        # Bind to theme changes
        self.theme_manager.bind(is_dark_mode=self.update_theme)
    
    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def update_theme(self, *args):
        """Update the theme colors"""
        colors = self.theme_manager.get_colors()
        
        # Update background color
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['background']
        
        # Update back button colors
        if hasattr(self, 'back_button'):
            if self.theme_manager.is_dark_mode:
                self.back_button.background_color = (0.3, 0.3, 0.3, 1)
                self.back_button.color = (0.9, 0.9, 0.9, 1)
            else:
                self.back_button.background_color = (0.85, 0.82, 0.78, 1)
                self.back_button.color = (0.1, 0.1, 0.1, 1)
                
        # Update all widgets with theme colors
        for child in self.walk(restrict=True):
            # Update labels
            if isinstance(child, Label):
                if getattr(child, 'bold', False) and getattr(child, 'font_size', 0) > dp(18):
                    # This is likely a title - use primary color
                    child.color = colors.get('primary', colors['text'])
                else:
                    # Regular text
                    child.color = colors['text']
            
            # Update standard buttons
            elif isinstance(child, Button) and child != self.back_button:
                # Only update standard buttons, not custom ones
                if not any(isinstance(child, cls) for cls in [RoundedButton, IconButton]):
                    child.background_color = colors['button_bg']
                    child.color = colors['button_text']
                    
            # Update text inputs
            elif isinstance(child, TextInput):
                child.background_color = colors['input_bg']
                child.foreground_color = colors['text']
                child.cursor_color = colors['primary']
    
    def go_back(self, *args):
        """Navigate back to the home screen"""
        self.manager.current = 'home'

class IconWidget(Widget):
    def __init__(self, icon_type='', **kwargs):
        super(IconWidget, self).__init__(**kwargs)
        self.icon_type = icon_type
        self.size_hint = (None, None)
        self.size = (dp(30), dp(30))
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)  # Dark gray color for icons
            
            if self.icon_type == 'home':
                # House icon
                points = [
                    self.center_x, self.top,  # Top of roof
                    self.x + dp(4), self.center_y + dp(4),  # Left roof
                    self.x + dp(4), self.y + dp(4),  # Left wall
                    self.right - dp(4), self.y + dp(4),  # Bottom wall
                    self.right - dp(4), self.center_y + dp(4),  # Right wall
                    self.center_x, self.top  # Back to top
                ]
                Line(points=points, width=dp(1.5))
                # Door
                door_points = [
                    self.center_x - dp(4), self.y + dp(4),  # Door left
                    self.center_x - dp(4), self.center_y - dp(4),  # Door top left
                    self.center_x + dp(4), self.center_y - dp(4),  # Door top right
                    self.center_x + dp(4), self.y + dp(4)  # Door right
                ]
                Line(points=door_points, width=dp(1.5))
                
            elif self.icon_type == 'reminder':
                # Clock icon
                Line(circle=(self.center_x, self.center_y, min(self.width, self.height)/2 - dp(4)), width=dp(1.5))
                # Clock hands
                Line(points=[self.center_x, self.center_y, self.center_x, self.top - dp(8)], width=dp(1.5))
                Line(points=[self.center_x, self.center_y, self.right - dp(8), self.center_y], width=dp(1.5))
                
            elif self.icon_type == 'camera':
                # Camera body
                Line(rectangle=(self.x + dp(4), self.y + dp(4), self.width - dp(8), self.height - dp(8)), width=dp(1.5))
                # Lens
                Line(circle=(self.center_x, self.center_y, min(self.width, self.height)/4), width=dp(1.5))
                # Flash
                Line(rectangle=(self.right - dp(8), self.top - dp(12), dp(4), dp(4)), width=dp(1.5))
                
            elif self.icon_type == 'voice':
                # YouTube-style microphone icon
                # Microphone stand
                Line(points=[
                    self.center_x, self.y + dp(4),
                    self.center_x, self.top - dp(4)
                ], width=dp(2))
                # Microphone head (circle)
                Line(circle=(self.center_x, self.top - dp(4), dp(6)), width=dp(2))
                # Microphone base (small rectangle)
                Line(rectangle=(self.center_x - dp(4), self.y + dp(4), dp(8), dp(2)), width=dp(2))
                
            elif self.icon_type == 'settings':
                # Gear icon
                Line(circle=(self.center_x, self.center_y, min(self.width, self.height)/3), width=dp(1.5))
                # Gear teeth
                for i in range(8):
                    angle = i * math.pi / 4
                    radius = min(self.width, self.height)/2 - dp(4)
                    x1 = self.center_x + radius * 0.7 * math.cos(angle)
                    y1 = self.center_y + radius * 0.7 * math.sin(angle)
                    x2 = self.center_x + radius * math.cos(angle)
                    y2 = self.center_y + radius * math.sin(angle)
                    Line(points=[x1, y1, x2, y2], width=dp(1.5))

class IconButton(ButtonBehavior, BoxLayout):
    icon_type = StringProperty('')
    text = StringProperty('')
    
    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.spacing = dp(5)
        self.padding = dp(5)
        
        # Create an image widget for the icon
        self.icon_image = Image(
            source='',  # Will be set by _update_icon
            size_hint=(None, None),
            size=(dp(30), dp(30)),  # Standard size for non-camera icons
            allow_stretch=True,
            keep_ratio=True,
            color=(0.2, 0.2, 0.2, 1)  # Initial color, will be updated by theme
        )
        
        # Center the icon
        icon_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint=(1, 0.7)
        )
        
        icon_layout.add_widget(self.icon_image)
        self.add_widget(icon_layout)
        
        # Create label
        label_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint=(1, 0.3)
        )
        self.label = Label(
            text=self.text,
            font_size=dp(11),
            color=(0.2, 0.2, 0.2, 1),  # Will be updated by theme
            size_hint=(1, None),
            height=dp(20),
            bold=True,
            halign='center'
        )
        label_layout.add_widget(self.label)
        self.add_widget(label_layout)
        
        # Bind properties
        self.bind(icon_type=self._update_icon)
        self.bind(text=self._update_text)
        
        # Initialize icon if icon_type was provided in kwargs
        if 'icon_type' in kwargs:
            self._update_icon(self, kwargs['icon_type'])
        
        # Update theme initially and bind to theme changes
        self.update_theme()
        self.theme_manager.bind(is_dark_mode=self.update_theme)
    
    def _update_icon(self, instance, value):
        # Map icon types to icon image files with absolute paths
        import os
        app_dir = os.path.dirname(os.path.abspath(__file__))
        icon_mapping = {
            'home': os.path.join(app_dir, 'icons', 'home-icon-silhouette.png').replace('\\', '/'),
            'reminder': os.path.join(app_dir, 'icons', 'bell.png').replace('\\', '/'),
            'camera': os.path.join(app_dir, 'icons', 'camera.png').replace('\\', '/'),
            'voice': os.path.join(app_dir, 'icons', 'microphone.png').replace('\\', '/'),
            'settings': os.path.join(app_dir, 'icons', 'setting.png').replace('\\', '/')
        }
        
        # Get the absolute path to the icon
        icon_path = icon_mapping.get(value, '')
        if icon_path:
            # Set the source and ensure it's visible
            self.icon_image.source = icon_path
            self.update_theme()  # Update colors based on current theme
    
    def _update_text(self, instance, value):
        self.label.text = value
        self.update_theme()  # Update colors based on current theme
    
    def update_theme(self, *args):
        """Update colors based on current theme"""
        is_dark = self.theme_manager.is_dark_mode
        
        # Update icon and text colors based on theme
        if is_dark:
            self.icon_image.color = (0.9, 0.9, 0.9, 1)  # Light color for dark mode
            self.label.color = (0.9, 0.9, 0.9, 1)
        else:
            self.icon_image.color = (0.2, 0.2, 0.2, 1)  # Dark color for light mode
            self.label.color = (0.2, 0.2, 0.2, 1)
    
    def on_press(self):
        # Change to a pressed state color based on theme
        is_dark = self.theme_manager.is_dark_mode
        if is_dark:
            self.icon_image.color = (1, 1, 1, 1)  # White for dark mode
            self.label.color = (1, 1, 1, 1)
        else:
            self.icon_image.color = (0, 0, 0, 1)  # Black for light mode
            self.label.color = (0, 0, 0, 1)
        
        # Get the HomeScreen instance to handle navigation
        app = App.get_running_app()
        if hasattr(app.root.current_screen, 'navigate_to'):
            app.root.current_screen.navigate_to(self.icon_type)
    
    def on_release(self):
        # Restore colors based on current theme
        self.update_theme()

# Reminder Screen with antibiotics reminder functionality
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from datetime import datetime, timedelta
import os

# Import the medication reminder module
try:
    from medication_reminder import MedicationReminder
except ImportError:
    pass  # Will handle this in the class

class RoundedButton(Button):
    def __init__(self, **kwargs):
        # Extract our custom properties before passing to the parent class
        self.bg_color = kwargs.pop('bg_color', kwargs.pop('color', (0.2, 0.6, 0.9, 1)))  # Support both bg_color and color
        text_color = kwargs.pop('text_color', (1, 1, 1, 1))  # Default white text
        
        # Now call the parent with the cleaned kwargs
        super(RoundedButton, self).__init__(**kwargs)
        
        # Set up button properties
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.background_down = ''
        self.color = text_color  # Text color
        
        # Store the pressed state background color
        self.background_color_down = (0.7, 0.7, 0.7, 1)  # Light gray when pressed
        
        # Bind canvas update to size/position changes
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color_down)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

    def on_release(self):
        self._update_canvas()

class ReminderCard(BoxLayout):
    reminder_id = StringProperty('')

    def __init__(self, reminder_data, **kwargs):
        super(ReminderCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(160)
        self.padding = [dp(10), dp(10)]
        self.spacing = dp(5)
        self.reminder_data = reminder_data
        self.reminder_id = reminder_data.get('id', '')
        self.theme_manager = ThemeManager()
        
        # Store next dose time if available
        self.next_dose_time = None
        if reminder_data.get('next_time') and isinstance(reminder_data['next_time'], datetime):
            self.next_dose_time = reminder_data['next_time']
        
        # Set up background with rounded corners
        with self.canvas.before:
            self.bg_color = Color(0.95, 0.95, 1, 1)  # Very light blue background
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Create a main horizontal layout
        main_layout = BoxLayout(orientation='horizontal')
        
        # Left side with details
        left_side = BoxLayout(
            orientation='vertical',
            size_hint=(0.7, 1),
            spacing=dp(5)
        )
        
        # Add medication name as title
        title_layout = BoxLayout(size_hint=(1, None), height=dp(30))
        self.title = Label(
            text=reminder_data.get('medication_name', 'Medication'),
            font_size=dp(20),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),  # Blue text
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        self.title.bind(size=self.title.setter('text_size'))
        
        title_layout.add_widget(self.title)
        left_side.add_widget(title_layout)
        
        # Add dosage and frequency info
        details_layout = GridLayout(cols=2, size_hint=(1, 0.8), spacing=[dp(5), dp(2)])
        
        # Dosage
        dosage_label = Label(
            text="Dosage:",
            font_size=dp(14),
            color=(0.4, 0.4, 0.4, 1),
            size_hint=(0.3, 1),
            halign='left'
        )
        dosage_label.bind(size=dosage_label.setter('text_size'))
        
        self.dosage_value = Label(
            text=reminder_data.get('dosage', 'N/A'),
            font_size=dp(14),
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(0.7, 1),
            halign='left'
        )
        self.dosage_value.bind(size=self.dosage_value.setter('text_size'))
        
        # Frequency
        frequency_label = Label(
            text="Frequency:",
            font_size=dp(14),
            color=(0.4, 0.4, 0.4, 1),
            size_hint=(0.3, 1),
            halign='left'
        )
        frequency_label.bind(size=frequency_label.setter('text_size'))
        
        self.frequency_value = Label(
            text=reminder_data.get('frequency', 'N/A'),
            font_size=dp(14),
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(0.7, 1),
            halign='left'
        )
        self.frequency_value.bind(size=self.frequency_value.setter('text_size'))
        
        # Add all labels to the details layout
        details_layout.add_widget(dosage_label)
        details_layout.add_widget(self.dosage_value)
        details_layout.add_widget(frequency_label)
        details_layout.add_widget(self.frequency_value)
        
        left_side.add_widget(details_layout)
        
        # Add Take Now button
        self.take_button = Button(
            text=tr('take_now'),
            size_hint=(1, None),
            height=dp(40),
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 0.8),  # Green, partially transparent
            color=(1, 1, 1, 1)
        )
        self.take_button.bind(on_release=self.take_medication)
        left_side.add_widget(self.take_button)
        
        # Right side with cooldown circle and buttons
        right_side = BoxLayout(
            orientation='vertical',
            size_hint=(0.3, 1),
            spacing=dp(5)
        )
        
        # Cooldown circle container
        self.cooldown_container = RelativeLayout(
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        
        # Create cooldown circle with theme-based colors
        with self.cooldown_container.canvas:
            # Background circle (light gray)
            self.circle_bg_color = Color(0.85, 0.85, 0.85, 1)
            self.circle_bg = Ellipse(pos=(0, 0), size=(dp(80), dp(80)))
            
            # Progress circle (green/blue) that shows remaining time
            self.circle_progress_color = Color(0.2, 0.7, 0.3, 1)  # Green for ready
            self.circle_progress = Ellipse(
                pos=(0, 0), 
                size=(dp(80), dp(80)),
                angle_start=0,
                angle_end=360  # Full circle initially
            )
        
        # Cooldown time label inside circle
        self.cooldown_label = Label(
            text=tr('ready'),
            font_size=dp(16),
            bold=True,
            color=(1, 1, 1, 1),  # White text on colored background
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            halign='center',
            valign='middle'
        )
        self.cooldown_label.bind(size=self.cooldown_label.setter('text_size'))
        
        self.cooldown_container.add_widget(self.cooldown_label)
        right_side.add_widget(self.cooldown_container)
        
        # Buttons for edit and delete
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.5),
            spacing=dp(5)
        )
        
        edit_btn = RoundedButton(
            text=tr("edit"),
            size_hint=(1, None),
            height=dp(30),
            bg_color=(0.2, 0.6, 0.9, 1)  # Blue
        )
        edit_btn.bind(on_release=lambda x: self.edit_reminder())
        
        delete_btn = RoundedButton(
            text=tr("delete"),
            size_hint=(1, None),
            height=dp(30),
            bg_color=(0.9, 0.3, 0.3, 1)  # Red
        )
        delete_btn.bind(on_release=lambda x: self.delete_reminder())
        
        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)
        right_side.add_widget(button_layout)
        
        # Add both sides to main layout
        main_layout.add_widget(left_side)
        main_layout.add_widget(right_side)
        self.add_widget(main_layout)
        
        # Check cooldown status initially and update UI
        self.check_cooldown_status()
        
        # Bind to position/size updates to keep cooldown circle positioned correctly
        self.bind(pos=self._update_cooldown_pos, size=self._update_cooldown_pos)
        
        # Start periodic cooldown check (every minute)
        Clock.schedule_interval(self.check_cooldown_status, 60)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_cooldown_pos(self, *args):
        """Update cooldown wheel position"""
        if hasattr(self, 'cooldown_container') and hasattr(self, 'circle_bg'):
            # Ensure the circles fill the entire container
            self.circle_bg.pos = (0, 0)
            self.circle_bg.size = self.cooldown_container.size
            
            self.circle_progress.pos = (0, 0)
            self.circle_progress.size = self.cooldown_container.size
    
    def get_cooldown_minutes(self, frequency):
        """Calculate cooldown minutes based on frequency"""
        frequency_map = {
            'Once daily': 24 * 60,
            'Twice daily': 12 * 60,
            'Three times daily': 8 * 60,
            'Four times daily': 6 * 60,
            'Every 6 hours': 6 * 60,
            'Every 8 hours': 8 * 60,
            'Every 12 hours': 12 * 60
        }
        
        # Default to 8 hours if frequency not found
        return frequency_map.get(frequency, 8 * 60)
        
    def check_cooldown_status(self, dt=None):
        """Check if medication can be taken again"""
        if not self.next_dose_time:
            # No next dose time set, medication is ready to take
            self.cooldown_label.text = tr('ready')
            self.circle_progress_color.rgba = (0.2, 0.8, 0.2, 1)  # Bright green
            self.circle_progress.angle_end = 360  # Full circle
            self.take_button.disabled = False
            self.take_button.opacity = 1
            self.take_button.text = tr('take_now')
            return False  # Stop any ongoing checking
        
        now = datetime.now()
        if now >= self.next_dose_time:
            # Cooldown completed, enable take button
            self.take_button.disabled = False
            self.take_button.opacity = 1
            self.take_button.text = tr('take_now')
            self.cooldown_label.text = tr('due_now')
            self.cooldown_label.color = (1, 1, 1, 1)  # White text on colored circle
            self.circle_progress_color.rgba = (0.2, 0.8, 0.2, 1)  # Bright green for ready
            self.circle_progress.angle_end = 360  # Full circle
            
            # Stop any ongoing timer updates
            return False
        else:
            # Still in cooldown, update time left
            time_diff = self.next_dose_time - now
            
            # Calculate remaining percentage
            total_seconds = self.get_cooldown_minutes(self.reminder_data.get('frequency', '')) * 60
            elapsed_seconds = total_seconds - time_diff.total_seconds()
            progress_percent = min(elapsed_seconds / total_seconds, 1.0)
            angle_end = 360 * progress_percent
            
            # Update progress wheel
            self.circle_progress.angle_end = angle_end
            
            # Update cooldown text - showing both hours and minutes for better precision
            if time_diff.days > 0:
                cooldown_text = f"{time_diff.days}\n{tr('days')}"
            elif time_diff.seconds // 3600 > 0:
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                cooldown_text = f"{hours}h\n{minutes}m"
            else:
                cooldown_text = f"{time_diff.seconds // 60}\n{tr('minutes')}"
                
            self.cooldown_label.text = cooldown_text
            self.cooldown_label.color = (1, 1, 1, 1)  # White text on colored progress
            
            # Update progress color (blue during cooldown)
            self.circle_progress_color.rgba = (0.2, 0.4, 0.8, 1)
            
            # Disable take button during cooldown
            self.take_button.disabled = True
            self.take_button.opacity = 0.6
            self.take_button.text = tr('taken')
            
            # Continue checking
            return True
    
    def take_medication(self, instance):
        """Record that medication was taken and start cooldown"""
        # Get the screen to access the reminder manager
        screen = App.get_running_app().root.current_screen
        
        if hasattr(screen, 'reminder_manager'):
            # Get cooldown period based on frequency
            frequency = self.reminder_data.get('frequency', '')
            cooldown_minutes = self.get_cooldown_minutes(frequency)
            
            # Calculate next dose time
            now = datetime.now()
            next_time = now + timedelta(minutes=cooldown_minutes)
            
            # Update reminder with new next time
            updated_reminder = dict(self.reminder_data)
            updated_reminder['next_time'] = next_time
            updated_reminder['last_taken'] = now
            
            # Update the reminder in the manager
            screen.reminder_manager.update_reminder(
                reminder_id=self.reminder_id,
                next_time=next_time,
                last_taken=now
            )
            
            # Store the next dose time
            self.reminder_data = updated_reminder
            self.next_dose_time = next_time
            
            # Update UI to reflect cooldown
            self.check_cooldown_status()
    
    def update_theme(self):
        """Update theme colors"""
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update background
        if is_dark:
            self.bg_color.rgba = (0.15, 0.15, 0.18, 1)  # Much darker background for dark mode
        else:
            self.bg_color.rgba = (0.95, 0.95, 1, 1)  # Very light blue background for light mode
        
        # Update all text colors
        self.title.color = colors['primary']
        self.dosage_value.color = colors['text']
        self.frequency_value.color = colors['text']
        
        # Update take button
        if is_dark:
            self.take_button.bg_color = (0.15, 0.4, 0.2, 0.8)  # Darker green, partially transparent
        else:
            self.take_button.bg_color = (0.2, 0.7, 0.3, 0.8)  # Standard green, partially transparent
        
        # Update cooldown colors based on status
        if self.cooldown_label.text == tr('ready'):
            self.cooldown_label.color = colors['text']
        else:
            # For non-ready states, use white text on colored background for better visibility
            self.cooldown_label.color = (1, 1, 1, 1)
    
    def edit_reminder(self):
        # Signal to parent screen to edit this reminder
        screen = App.get_running_app().root.current_screen
        if hasattr(screen, 'show_edit_reminder'):
            screen.show_edit_reminder(self.reminder_id)
    
    def delete_reminder(self):
        # Signal to parent screen to delete this reminder
        screen = App.get_running_app().root.current_screen
        if hasattr(screen, 'delete_reminder'):
            screen.delete_reminder(self.reminder_id)

class ReminderScreen(BaseScreen):
    reminder_manager = ObjectProperty(None)
    is_adding_reminder = BooleanProperty(False)
    editing_reminder_id = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ReminderScreen, self).__init__(**kwargs)
        
        # Initialize reminder manager
        try:
            self.reminder_manager = MedicationReminder()
        except NameError:
            # Fallback if module is not found
            self.reminder_manager = None
        
        # Add title with more modern styling - dark grey and centered
        title_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(80),  # Increased height for more space
            pos_hint={'top': 1},
            padding=[0, dp(15), 0, 0]  # Add padding to the top
        )
        
        title = Label(
            text='Antibiotic Reminder',
            font_size=dp(30),  # Increased font size
            bold=True,
            color=(0.3, 0.3, 0.3, 1),  # Dark grey text
            size_hint=(1, 1),
            halign='center',  # Centered text
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Centered horizontally and vertically
        )
        # Ensure the text alignment applies
        title.bind(size=title.setter('text_size'))
        
        title_bar.add_widget(title)
        self.main_layout.add_widget(title_bar)
        
        # Content area for reminders with scroll view
        self.scroll_view = ScrollView(
            size_hint=(1, None),
            height=dp(400),
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        
        # This will hold our reminder cards
        self.reminders_layout = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=[dp(10), dp(10)],
            size_hint_y=None,  # Required for scrolling
        )
        self.reminders_layout.bind(minimum_height=self.reminders_layout.setter('height'))
        
        self.scroll_view.add_widget(self.reminders_layout)
        self.main_layout.add_widget(self.scroll_view)
        
        # Create a circular Add button at the bottom center of the page
        add_button_container = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=dp(90),
            height=dp(120),
            pos_hint={'center_x': 0.5, 'y': 0.07}  # Further increased bottom padding
        )
        
        # Use our custom RoundButton that guarantees the whole circle is clickable
        from round_button import RoundButton
        
        # Create a circular button with proper touch detection
        circle_btn = RoundButton(
            text='+',
            font_size=dp(42),
            bold=True,
            bg_color=(0.2, 0.7, 0.3, 1),  # Green color
            fg_color=(1, 1, 1, 1),  # White text
            size_hint=(None, None),
            size=(dp(70), dp(70))
        )
        
        # Bind directly to the add reminder function
        circle_btn.bind(on_release=self.show_add_reminder)
        
        # Create a centered container for the button
        circle_container = AnchorLayout(
            anchor_x='center', 
            anchor_y='center',
            size_hint=(1, None),
            height=dp(90)  # Give enough room for the button
        )
        
        # Add the circular button directly to the container
        circle_container.add_widget(circle_btn)
        
        # 'ADD' text below the circle
        add_text = Label(
            text='ADD',
            font_size=dp(14),
            bold=True,
            color=(0.2, 0.7, 0.3, 1),  # Green text to match circle
            size_hint=(1, None),
            height=dp(25)
        )
        
        # Add the centered circle and the text to container
        add_button_container.add_widget(circle_container)
        add_button_container.add_widget(add_text)
        
        # Store the reference we'll need for callback and updates
        self.circle_plus_btn = circle_btn
        
        # Add to main layout
        self.main_layout.add_widget(add_button_container)
        
        # Container for add/edit reminder form (hidden initially)
        self.form_container = FloatLayout(
            size_hint=(1, 0.85),
            pos_hint={'center_x': 0.5, 'top': 0.9},
            opacity=0
        )
        
        # Form background
        with self.form_container.canvas.before:
            Color(0.97, 0.97, 0.97, 1)
            self.form_bg = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(20)])
        self.form_container.bind(pos=self._update_form_bg, size=self._update_form_bg)
        
        # Form contents
        form_grid = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=[dp(20), dp(20)],
            size_hint=(0.9, 0.95),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.form_title = Label(
            text="Add New Antibiotic Reminder",
            font_size=dp(20),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint=(1, None),
            height=dp(40)
        )
        form_grid.add_widget(self.form_title)
        
        # Medication name
        name_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        name_label = Label(
            text="Medication Name",
            font_size=dp(16),
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            size_hint=(1, None),
            height=dp(30)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        self.name_input = TextInput(
            hint_text="Enter medication name (e.g., Amoxicillin)",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(10), dp(15)],
            font_size=dp(16)
        )
        name_layout.add_widget(name_label)
        name_layout.add_widget(self.name_input)
        form_grid.add_widget(name_layout)
        
        # Dosage
        dosage_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        dosage_label = Label(
            text="Dosage",
            font_size=dp(16),
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            size_hint=(1, None),
            height=dp(30)
        )
        dosage_label.bind(size=dosage_label.setter('text_size'))
        
        self.dosage_input = TextInput(
            hint_text="Enter dosage (e.g., 500mg)",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(10), dp(15)],
            font_size=dp(16)
        )
        dosage_layout.add_widget(dosage_label)
        dosage_layout.add_widget(self.dosage_input)
        form_grid.add_widget(dosage_layout)
        
        # Frequency
        frequency_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        frequency_label = Label(
            text="Frequency",
            font_size=dp(16),
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            size_hint=(1, None),
            height=dp(30)
        )
        frequency_label.bind(size=frequency_label.setter('text_size'))
        
        self.frequency_spinner = Spinner(
            text='Select frequency',
            values=('Once daily', 'Twice daily', 'Three times daily', 'Four times daily', 
                    'Every 6 hours', 'Every 8 hours', 'Every 12 hours'),
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.95, 0.95, 0.95, 1),
            color=(0.2, 0.2, 0.2, 1),
            font_size=dp(16)
        )
        frequency_layout.add_widget(frequency_label)
        frequency_layout.add_widget(self.frequency_spinner)
        form_grid.add_widget(frequency_layout)
        
        # Duration
        duration_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        duration_label = Label(
            text="Duration (days)",
            font_size=dp(16),
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            size_hint=(1, None),
            height=dp(30)
        )
        duration_label.bind(size=duration_label.setter('text_size'))
        
        self.duration_input = TextInput(
            hint_text="Enter number of days (e.g., 7)",
            multiline=False,
            input_filter='int',
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(10), dp(15)],
            font_size=dp(16)
        )
        duration_layout.add_widget(duration_label)
        duration_layout.add_widget(self.duration_input)
        form_grid.add_widget(duration_layout)
        
        # Notes
        notes_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        notes_label = Label(
            text="Notes (optional)",
            font_size=dp(16),
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            size_hint=(1, None),
            height=dp(30)
        )
        notes_label.bind(size=notes_label.setter('text_size'))
        
        self.notes_input = TextInput(
            hint_text="Any special instructions",
            multiline=True,
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(10), dp(15)],
            font_size=dp(16)
        )
        notes_layout.add_widget(notes_label)
        notes_layout.add_widget(self.notes_input)
        form_grid.add_widget(notes_layout)
        
        # Buttons
        button_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(20))
        
        cancel_btn = RoundedButton(
            text="Cancel",
            size_hint=(0.5, 1),
            bg_color=(0.7, 0.7, 0.7, 1)  # Gray
        )
        cancel_btn.bind(on_release=self.hide_form)
        
        self.save_btn = RoundedButton(
            text="Save",
            size_hint=(0.5, 1),
            bg_color=(0.2, 0.7, 0.3, 1)  # Green
        )
        self.save_btn.bind(on_release=self.save_reminder)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(self.save_btn)
        form_grid.add_widget(button_layout)
        
        # Add a button to ask AI for help
        ai_button_layout = BoxLayout(size_hint=(1, None), height=dp(60), padding=[0, dp(10)])
        
        ai_help_btn = RoundedButton(
            text="Ask AI about this medication",
            size_hint=(1, 1),
            bg_color=(0.5, 0.3, 0.9, 1)  # Purple
        )
        ai_help_btn.bind(on_release=self.ask_ai_about_medication)
        
        ai_button_layout.add_widget(ai_help_btn)
        form_grid.add_widget(ai_button_layout)
        
        self.form_container.add_widget(form_grid)
        self.main_layout.add_widget(self.form_container)
        
        # No reminders message
        self.no_reminders_label = Label(
            text="No antibiotic reminders yet.\nTap '+ Add' to create your first reminder.",
            font_size=dp(18),
            color=(0.5, 0.5, 0.5, 1),
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(self.no_reminders_label)
        
        # Load reminders on startup
        Clock.schedule_once(self.load_reminders, 0.1)
    
    def _update_form_bg(self, *args):
        self.form_bg.pos = self.form_container.pos
        self.form_bg.size = self.form_container.size
    
    def _update_circle(self, instance, value):
        if hasattr(self, 'circle'):
            self.circle.pos = instance.pos
            self.circle.size = instance.size
    
    def _on_circle_touch(self, instance, touch):
        """Handle touch events on the circle button"""
        # Check if the touch is within the circle button
        if instance.collide_point(*touch.pos):
            # Call the show_add_reminder method
            self.show_add_reminder(instance)
            return True  # Indicate the touch was handled
        return False  # Let the touch propagate
    
    def load_reminders(self, dt=None):
        """Load reminders from the reminder manager"""
        if not self.reminder_manager:
            return
        
        # Clear current reminders
        self.reminders_layout.clear_widgets()
        
        # Get active reminders
        reminders = self.reminder_manager.get_active_reminders()
        
        # Show or hide the no reminders message
        self.no_reminders_label.opacity = 1 if not reminders else 0
        
        # Add reminder cards
        for reminder in reminders:
            card = ReminderCard(reminder)
            self.reminders_layout.add_widget(card)
    
    def show_add_reminder(self, instance):
        """Show the add reminder form"""
        self.is_adding_reminder = True
        self.editing_reminder_id = ''
        self.form_title.text = "Add New Antibiotic Reminder"
        self.save_btn.text = "Save"
        
        # Clear form fields
        self.name_input.text = ''
        self.dosage_input.text = ''
        self.frequency_spinner.text = 'Select frequency'
        self.duration_input.text = ''
        self.notes_input.text = ''
        
        # Show form, hide reminders
        self.form_container.opacity = 1
        self.scroll_view.opacity = 0
        self.no_reminders_label.opacity = 0
    
    def show_edit_reminder(self, reminder_id):
        """Show the edit reminder form"""
        if not self.reminder_manager:
            return
        
        reminder = self.reminder_manager.get_reminder(reminder_id)
        if not reminder:
            return
        
        self.is_adding_reminder = False
        self.editing_reminder_id = reminder_id
        self.form_title.text = "Edit Antibiotic Reminder"
        self.save_btn.text = "Update"
        
        # Fill form fields with reminder data
        self.name_input.text = reminder.get('medication_name', '')
        self.dosage_input.text = reminder.get('dosage', '')
        self.frequency_spinner.text = reminder.get('frequency', 'Select frequency')
        self.duration_input.text = str(reminder.get('duration', ''))
        self.notes_input.text = reminder.get('notes', '')
        
        # Show form, hide reminders
        self.form_container.opacity = 1
        self.scroll_view.opacity = 0
        self.no_reminders_label.opacity = 0
    
    def hide_form(self, instance=None):
        """Hide the add/edit reminder form"""
        # Hide form, show reminders
        self.form_container.opacity = 0
        self.scroll_view.opacity = 1
        
        # Show no reminders message if needed
        if not self.reminders_layout.children:
            self.no_reminders_label.opacity = 1
    
    def save_reminder(self, instance):
        """Save the reminder data"""
        if not self.reminder_manager:
            return
        
        # Validate form data
        medication_name = self.name_input.text.strip()
        dosage = self.dosage_input.text.strip()
        frequency = self.frequency_spinner.text
        duration = self.duration_input.text.strip()
        notes = self.notes_input.text.strip()
        
        if not medication_name or not dosage or frequency == 'Select frequency':
            # Show error message
            return
        
        # Convert duration to int if provided
        duration_days = int(duration) if duration else None
        
        if self.is_adding_reminder:
            # Add new reminder
            self.reminder_manager.add_reminder(
                medication_name=medication_name,
                dosage=dosage,
                frequency=frequency,
                duration=duration_days,
                notes=notes
            )
        else:
            # Update existing reminder
            self.reminder_manager.update_reminder(
                reminder_id=self.editing_reminder_id,
                medication_name=medication_name,
                dosage=dosage,
                frequency=frequency,
                duration=duration_days,
                notes=notes
            )
        
        # Reload reminders and hide form
        self.load_reminders()
        self.hide_form()
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        if not self.reminder_manager:
            return
        
        self.reminder_manager.delete_reminder(reminder_id)
        self.load_reminders()
    
    def ask_ai_about_medication(self, instance):
        """Navigate to the voice assistant with the medication as context"""
        medication_name = self.name_input.text.strip()
        if medication_name:
            app = App.get_running_app()
            
            # Check if voice screen exists
            if 'voice' not in app.root.screen_names:
                app.root.add_widget(VoiceScreen(name='voice'))
            
            # Set the medication context if the voice screen has this capability
            voice_screen = app.root.get_screen('voice')
            if hasattr(voice_screen, 'set_medication_context'):
                voice_screen.set_medication_context(medication_name)
            
            # Navigate to the voice screen
            app.root.current = 'voice'

# Camera Screen - Shows the bars
class CameraScreen(BaseScreen):
    def __init__(self, **kwargs):
        # First initialize the parent BaseScreen
        try:
            super(CameraScreen, self).__init__(**kwargs)
        except Exception as e:
            print(f"Error initializing CameraScreen: {e}")
            return
            
        try:
            # Add title with improved styling
            title = Label(
                text='Medication Images',
                font_size=dp(24),
                bold=True,
                color=(0.2, 0.4, 0.8, 1),  # Blue text
                pos_hint={'center_x': 0.5, 'top': 0.95}
            )
            self.main_layout.add_widget(title)
            
            # Add camera content
            content = Label(
                text='This feature will allow you to take pictures of your medications for identification and reference.\n\nComing in the next update!',
                font_size=dp(18),
                color=(0.3, 0.3, 0.3, 1),
                halign='center',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_layout.add_widget(content)
            
            # Add camera icon in a circular container for visual appeal
            icon_container = FloatLayout(
                size_hint=(None, None),
                size=(dp(120), dp(120)),
                pos_hint={'center_x': 0.5, 'center_y': 0.7}
            )
            
            # Add circular background
            with icon_container.canvas.before:
                Color(0.95, 0.95, 1, 1)  # Light blue background
                Ellipse(pos=(0, 0), size=(dp(120), dp(120)))
            
            # Add camera icon
            try:
                camera_icon = Image(
                    source='icons/camera.png',
                    size_hint=(None, None),
                    size=(dp(80), dp(80)),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                )
                icon_container.add_widget(camera_icon)
            except Exception as e:
                print(f"Error loading camera icon: {e}")
                # Add a fallback label if image fails to load
                fallback = Label(text="📷", font_size=dp(40))
                icon_container.add_widget(fallback)
                
            self.main_layout.add_widget(icon_container)
            
            # Add a coming soon button
            coming_soon = Button(
                text="Coming Soon",
                size_hint=(0.5, None),
                height=dp(50),
                pos_hint={'center_x': 0.5, 'center_y': 0.3},
                background_normal='',
                background_color=(0.7, 0.7, 0.7, 1),
                color=(1, 1, 1, 1)
            )
            self.main_layout.add_widget(coming_soon)
            
        except Exception as e:
            # If anything fails, add an error message instead of crashing
            print(f"Error setting up CameraScreen: {e}")
            error_label = Label(
                text=f"Sorry, there was an error loading this screen.\nPlease try again later.",
                font_size=dp(18),
                color=(0.8, 0.3, 0.3, 1),  # Red text
                halign='center',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_layout.add_widget(error_label)

# Voice Assistant Screen with AI integration
from kivy.animation import Animation
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
import threading

# Try to import the full-featured AI assistant first
try:
    from ai_assistant import AIAssistant
    HAS_FULL_AI = True
except ImportError:
    HAS_FULL_AI = False
    
# Try to import the simplified AI assistant as fallback
try:
    from ai_assistant import SimpleAIAssistant
    HAS_SIMPLE_AI = True
except ImportError:
    HAS_SIMPLE_AI = False

class PulsingMicButton(ToggleButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(PulsingMicButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(80), dp(120))
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.15}  # Moved up from 0.3 to 0.15
        self.spacing = dp(5)
        
        # Create the microphone icon container
        self.icon_container = FloatLayout(
            size_hint=(None, None),
            size=(dp(70), dp(70)),  # Reduced from (100, 100)
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        
        # Add circular background
        with self.icon_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray
            self.bg_circle = Ellipse(
                pos=(self.icon_container.center_x - dp(35), self.icon_container.center_y - dp(35)),  # Adjusted for new size
                size=(dp(70), dp(70))  # Reduced from (100, 100)
            )
        self.icon_container.bind(pos=self._update_ellipse, size=self._update_ellipse)
        
        # Add microphone icon
        self.mic_icon = Image(
            source='icons/microphone.png',
            size_hint=(None, None),
            size=(dp(40), dp(40)),  # Reduced from (60, 60)
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.icon_container.add_widget(self.mic_icon)
        self.add_widget(self.icon_container)
        
        # Add label
        self.label = Label(
            text='Tap to speak',
            font_size=dp(14),  # Reduced from 16
            color=(0.3, 0.3, 0.3, 1),
            bold=True,
            size_hint=(1, None),
            height=dp(25)  # Reduced from 30
        )
        self.add_widget(self.label)
        
        # Set initial state
        self.pulsing_animation = None
        self.state = 'normal'
    
    def _update_ellipse(self, *args):
        self.bg_circle.pos = (
            self.icon_container.x + (self.icon_container.width - dp(70)) / 2,
            self.icon_container.y + (self.icon_container.height - dp(70)) / 2
        )
    
    def on_state(self, instance, value):
        if value == 'down':
            # Start pulsing animation
            self._start_pulsing()
            self.label.text = 'Listening...'
            self.label.color = (0.9, 0.3, 0.3, 1)  # Red text
        else:
            # Stop pulsing animation
            self._stop_pulsing()
            self.label.text = 'Tap to speak'
            self.label.color = (0.3, 0.3, 0.3, 1)  # Gray text
    
    def _start_pulsing(self):
        # Create pulsing animation for the background circle
        scale_up = Animation(
            size=(dp(75), dp(75)), 
            pos=(
                self.icon_container.center_x - dp(37.5), 
                self.icon_container.center_y - dp(37.5)
            ), 
            duration=0.7
        )
        scale_down = Animation(
            size=(dp(70), dp(70)), 
            pos=(
                self.icon_container.center_x - dp(35), 
                self.icon_container.center_y - dp(35)
            ), 
            duration=0.7
        )
        self.pulsing_animation = scale_up + scale_down
        self.pulsing_animation.repeat = True
        self.pulsing_animation.start(self.bg_circle)
        
        # Change background color to indicate recording
        with self.icon_container.canvas.before:
            Color(0.9, 0.3, 0.3, 0.2)  # Light red
            self.bg_circle = Ellipse(
                pos=(self.icon_container.center_x - dp(35), self.icon_container.center_y - dp(35)), 
                size=(dp(70), dp(70))
            )
    
    def _stop_pulsing(self):
        if self.pulsing_animation:
            self.pulsing_animation.cancel(self.bg_circle)
            self.pulsing_animation = None
        
        # Reset background color
        with self.icon_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray
            self.bg_circle = Ellipse(
                pos=(self.icon_container.center_x - dp(35), self.icon_container.center_y - dp(35)), 
                size=(dp(70), dp(70))
            )

class ChatBubble(BoxLayout):
    def __init__(self, message, is_user=False, **kwargs):
        super(ChatBubble, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        
        # Calculate needed height based on text length
        text_width = Window.width * 0.7  # 70% of screen width for text
        label = Label(
            text=message,
            size_hint_x=None,
            width=text_width,
            text_size=(text_width, None),
            halign='left',
            valign='middle',
            padding=[dp(15), dp(10)],
            color=(1, 1, 1, 1) if is_user else (0.1, 0.1, 0.1, 1)
        )
        label.bind(texture_size=self._update_size)
        
        # Set bubble style based on user or ai
        bubble = BoxLayout(
            size_hint=(0.8, 1),
            pos_hint={'right': 1} if is_user else {'x': 0}
        )
        
        with bubble.canvas.before:
            Color(*(0.2, 0.6, 0.9, 1) if is_user else (0.95, 0.95, 0.95, 1))  # Blue for user, light gray for AI
            self.rect = RoundedRectangle(size=bubble.size, pos=bubble.pos, radius=[dp(15)])
        bubble.bind(size=self._update_rect, pos=self._update_rect)
        
        bubble.add_widget(label)
        
        # Add to main layout with correct alignment
        if is_user:
            self.add_widget(Widget(size_hint_x=0.2))  # Spacer on left for user messages
            self.add_widget(bubble)
        else:
            self.add_widget(bubble)
            self.add_widget(Widget(size_hint_x=0.2))  # Spacer on right for AI messages
    
    def _update_size(self, instance, value):
        # Update height based on text content
        self.height = value[1] + dp(20)  # Text height + padding
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class VoiceScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(VoiceScreen, self).__init__(**kwargs)
        
        # Initialize AI assistant with proper fallback mechanisms
        self.ai_assistant = None
        
        # Try to initialize AI assistant
        try:
            # First try to use the full AI assistant with API
            from ai_assistant import AIAssistant
            
            # Check if the API key is valid
            api_key_file = 'openai_api_key.txt'
            if os.path.exists(api_key_file):
                with open(api_key_file, 'r') as f:
                    api_key = f.read().strip()
                    if api_key and 'YOUR_API_KEY' not in api_key:
                        self.ai_assistant = AIAssistant(api_key)
        except Exception as e:
            print(f"Error initializing AIAssistant: {e}")
            
        # If full AI assistant failed, use the simple version
        if not self.ai_assistant:
            try:
                from ai_assistant import SimpleAIAssistant
                self.ai_assistant = SimpleAIAssistant()
                
                # Set up a direct binding to detect when the reminder event changes
                if hasattr(self.ai_assistant, 'create_reminder_event'):
                    print("Setting up reminder event binding")
                    self.ai_assistant.bind(create_reminder_event=self._on_reminder_event_change)
                    
            except Exception as e:
                print(f"Error initializing SimpleAIAssistant: {e}")
                self.ai_assistant = None
        
        # Track if we're currently processing voice input
        self.is_listening = False
        self.is_processing = False
        self.medication_context = None
        
        # Add title with subtitle
        title_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.98},
            spacing=dp(2)
        )
        
        title = Label(
            text='Medical AI Assistant',
            font_size=dp(24),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),  # Blue
            size_hint=(1, None),
            height=dp(30)
        )
        
        subtitle = Label(
            text='Ask about your antibiotics',
            font_size=dp(14),
            italic=True,
            color=(0.5, 0.5, 0.5, 1),  # Gray
            size_hint=(1, None),
            height=dp(20)
        )
        
        title_box.add_widget(title)
        title_box.add_widget(subtitle)
        self.main_layout.add_widget(title_box)
        
        # Chat history scroll view
        self.scroll_view = ScrollView(
            size_hint=(1, None),
            height=Window.height * 0.6,
            pos_hint={'center_x': 0.5, 'top': 0.85}
        )
        
        # This will hold our chat bubbles
        self.chat_layout = GridLayout(
            cols=1,
            spacing=dp(15),
            padding=[dp(10), dp(10), dp(10), dp(20)],
            size_hint_y=None
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        
        self.scroll_view.add_widget(self.chat_layout)
        self.main_layout.add_widget(self.scroll_view)
        
        # Add a text input area at the bottom
        input_area = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            padding=[dp(10), dp(5)],
            spacing=dp(10),
            pos_hint={'center_x': 0.5, 'y': 0.02}
        )
        
        # Text input
        self.text_input = TextInput(
            hint_text='Type your message here',
            size_hint=(0.8, None),
            height=dp(50),
            multiline=False,
            padding=[dp(10), dp(10), dp(10), 0],
            font_size=dp(16)
        )
        self.text_input.bind(on_text_validate=self.send_text_message)
        
        # Send button
        send_btn = RoundedButton(
            text='Send',
            size_hint=(0.2, None),
            height=dp(50),
            bg_color=(0.2, 0.6, 0.9, 1)  # Blue
        )
        send_btn.bind(on_release=self.send_text_message)
        
        input_area.add_widget(self.text_input)
        input_area.add_widget(send_btn)
        self.main_layout.add_widget(input_area)
        
        # Add microphone button between chat and text input
        self.mic_button = PulsingMicButton()
        self.mic_button.pos_hint = {'center_x': 0.5, 'center_y': 0.15}  # Moved up from 0.25 to 0.15
        self.mic_button.bind(on_press=self.toggle_listening)
        self.main_layout.add_widget(self.mic_button)
        
        # Process status label
        self.status_label = Label(
            text='',
            font_size=dp(14),
            italic=True,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, None),
            height=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.17}
        )
        self.main_layout.add_widget(self.status_label)
        
        # Add a welcome message from the AI after a small delay
        Clock.schedule_once(self.add_welcome_message, 0.5)

    def add_welcome_message(self, dt=None):
        """Add an initial welcome message from the AI assistant"""
        if self.medication_context:
            welcome_text = f"Hello! I see you're asking about {self.medication_context}. How can I help you with this medication today?"
        else:
            welcome_text = "Hello! I'm your medical assistant. I can help with information about antibiotics, setting up reminders, or answering questions about your medication. How can I assist you today?"
        
        self.add_message(welcome_text, is_user=False)
    
    def set_medication_context(self, medication_name):
        """Set context about a specific medication"""
        self.medication_context = medication_name
        
        # If we already have welcome message, add a new message about this context
        if self.chat_layout.children:
            self.add_message(
                f"I see you want to know more about {medication_name}. What would you like to know about this medication?",
                is_user=False
            )
    
    def add_message(self, text, is_user=True):
        """Add a message bubble to the chat"""
        # Create a new chat bubble
        bubble = ChatBubble(text, is_user=is_user)
        
        # Add to the chat layout at the bottom
        self.chat_layout.add_widget(bubble)
        
        # Scroll to the bottom to see the new message
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
    
    def _scroll_to_bottom(self):
        """Scroll the chat view to the bottom"""
        if self.chat_layout.height > self.scroll_view.height:
            self.scroll_view.scroll_y = 0
    
    def toggle_listening(self, instance):
        """Toggle voice listening mode"""
        if not self.ai_assistant:
            self.status_label.text = "AI Assistant module not available"
            self.mic_button.state = 'normal'
            return
        
        if self.is_listening:
            # Stop listening
            self.is_listening = False
            self.mic_button.state = 'normal'
            self.status_label.text = "Processing..."
        else:
            # Start listening
            self.is_listening = True
            self.mic_button.state = 'down'
            self.status_label.text = "Listening..."
            
            # Start the speech recognition process
            self._start_voice_input()
    
    def _start_voice_input(self):
        """Start the speech recognition process in a separate thread"""
        try:
            if self.ai_assistant:
                # Monitor the AI assistant's is_listening property
                def check_listening_status(dt):
                    try:
                        if not self.ai_assistant.is_listening:
                            # Speech recognition completed
                            self.is_listening = False
                            self.mic_button.state = 'normal'
                            
                            # Safety check to ensure we don't access attributes that don't exist
                            if hasattr(self.ai_assistant, 'response_text'):
                                response_text = self.ai_assistant.response_text
                                
                                if (response_text.startswith("I couldn't understand") or 
                                    response_text.startswith("I didn't hear") or
                                    response_text.startswith("Error")):
                                    # Error in speech recognition
                                    self.status_label.text = response_text
                                    Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', ''), 3)
                                elif hasattr(self.ai_assistant, 'recognized_text') and self.ai_assistant.recognized_text:
                                    # Add the recognized text as a user message
                                    self.add_message(self.ai_assistant.recognized_text, is_user=True)
                                    
                                    # Process with AI and add response
                                    self._process_ai_response()
                            return False  # Stop checking
                        return True  # Continue checking
                    except Exception as e:
                        print(f"Error in check_listening_status: {e}")
                        self.status_label.text = "An error occurred while listening"
                        self.is_listening = False
                        self.mic_button.state = 'normal'
                        return False  # Stop checking on error
                
                # Start the speech recognition with error handling
                try:
                    self.ai_assistant.start_voice_input()
                except Exception as e:
                    print(f"Error starting voice input: {e}")
                    self.status_label.text = "Could not start speech recognition"
                    self.is_listening = False
                    self.mic_button.state = 'normal'
                    return
                
                # Check status periodically until no longer listening
                Clock.schedule_interval(check_listening_status, 0.5)
            else:
                # Handle case when AI assistant is not available
                self.status_label.text = "Speech recognition not available"
                self.is_listening = False
                self.mic_button.state = 'normal'
                
                # Add a fallback message in the chat
                self.add_message("Sorry, I couldn't access the speech recognition system. Please type your message instead.", is_user=False)
        except Exception as e:
            print(f"Error in _start_voice_input: {e}")
            self.status_label.text = "An error occurred"
            self.is_listening = False
            if hasattr(self, 'mic_button'):
                self.mic_button.state = 'normal'
    
    # The listening status check is now handled directly in the _start_voice_input method
    
    def _process_voice_input(self, recognized_text):
        """Process the recognized text from voice input"""
        if not recognized_text:
            self.add_message("I didn't hear anything. Please try again.", is_user=False)
            return
            
        # Add the user's message to the chat
        self.add_message(recognized_text, is_user=True)
        
        if self.ai_assistant:
            # Check for special navigation commands before processing with AI
            navigation_command = self._check_for_navigation_command(recognized_text)
            if navigation_command:
                self._handle_navigation_command(navigation_command, recognized_text)
            else:
                # Process with AI
                self.ai_assistant.process_text_input(recognized_text)
                self._process_ai_response()
        else:
            # Fallback if no AI assistant
            self.add_message("AI Assistant module is not available. Please check if dependencies are installed.", is_user=False)
            
    def send_text_message(self, instance):
        """Send a text message from the input field"""
        # Get text and clear input field
        text = self.text_input.text.strip()
        self.text_input.text = ''
        
        if not text:
            return
        
        # Add message to chat
        self.add_message(text, is_user=True)
        
        if self.ai_assistant:
            # Check for special navigation commands before processing with AI
            navigation_command = self._check_for_navigation_command(text)
            if navigation_command:
                self._handle_navigation_command(navigation_command, text)
            else:
                # Process with AI
                self.ai_assistant.process_text_input(text)
                self._process_ai_response()
        else:
            # Fallback if no AI assistant
            self.add_message("AI Assistant module is not available. Please check if dependencies are installed.", is_user=False)
    
    def _on_reminder_event_change(self, instance, value):
        """Handle changes to the create_reminder_event property"""
        if not value:
            return
            
        print(f"Reminder event triggered: {value}")
        
        try:
            # Parse the reminder data
            import json
            reminder_data = json.loads(value)
            
            # Reset the event to prevent duplicate reminders
            instance.create_reminder_event = ''
            
            # Create the reminder
            self.add_message("I'm creating a medication reminder for you now...", is_user=False)
            self._create_reminder_from_ai(reminder_data)
            
        except Exception as e:
            print(f"Error processing reminder event: {e}")
            import traceback
            traceback.print_exc()
            self.add_message(f"I couldn't create the reminder: {e}", is_user=False)
    
    def _check_for_navigation_command(self, text):
        """Check if the user is requesting to navigate to a specific screen"""
        text = text.lower()
        
        # Check for navigation to reminders screen
        if any(phrase in text for phrase in [
            'go to reminder', 'go to reminders', 'show reminder', 'show reminders',
            'open reminder', 'open reminders', 'view reminder', 'view reminders',
            'take me to reminder', 'take me to reminders', 'navigate to reminder', 'navigate to reminders'
        ]):
            return 'reminder'
        
        # Check for navigation to home screen
        if any(phrase in text for phrase in [
            'go to home', 'go home', 'show home', 'open home', 'view home',
            'take me to home', 'navigate to home', 'return to home', 'back to home'
        ]):
            return 'home'
        
        return None
    
    def _handle_navigation_command(self, screen_name, original_text):
        """Handle a navigation command to a specific screen"""
        app = App.get_running_app()
        
        # Check if the requested screen exists in the screen manager
        if screen_name in app.root.screen_names:
            # Add a confirmation message
            self.add_message(f"Navigating to {screen_name.title()} screen...", is_user=False)
            
            # Navigate to the requested screen
            app.root.current = screen_name
        else:
            # If screen doesn't exist, process the text normally with AI
            if self.ai_assistant:
                self.ai_assistant.process_text_input(original_text)
                self._process_ai_response()
    
    def _process_ai_response(self):
        """Process the AI response and add it to the chat"""
        if not self.ai_assistant:
            return
        
        self.is_processing = True
        self.status_label.text = "AI is thinking..."
        
        # Check for AI response every 0.5 seconds
        def check_response(dt):
            if not self.ai_assistant.is_processing:
                # AI has responded
                self.add_message(self.ai_assistant.response_text, is_user=False)
                self.status_label.text = ''
                self.is_processing = False
                
                # Check if AI wants to create a reminder
                self._check_for_reminder_creation()
                
                return False  # Stop checking
            return True  # Keep checking
        
        # Start checking for response
        Clock.schedule_interval(check_response, 0.5)
        
    def _check_for_reminder_creation(self):
        """Check if the AI assistant wants to create a reminder"""
        # Make sure the AI assistant has the create_reminder_event property
        if not hasattr(self.ai_assistant, 'create_reminder_event'):
            print("AI assistant does not have create_reminder_event property")
            return
            
        # Check if there's a reminder event
        reminder_event = self.ai_assistant.create_reminder_event
        if not reminder_event:
            return
            
        print(f"Detected reminder event: {reminder_event}")
            
        try:
            # Parse the reminder data
            import json
            reminder_data = json.loads(reminder_event)
            print(f"Parsed reminder data: {reminder_data}")
            
            # Reset the event to prevent duplicate reminders
            self.ai_assistant.create_reminder_event = ''
            
            # Create the reminder
            self.add_message("I'm creating a reminder for you now...", is_user=False)
            self._create_reminder_from_ai(reminder_data)
            
        except Exception as e:
            print(f"Error processing reminder creation: {e}")
            self.add_message(f"There was a problem creating your reminder: {e}", is_user=False)
    
    def _create_reminder_from_ai(self, reminder_data):
        """Create a reminder using data extracted by the AI"""
        print(f"Creating reminder with data: {reminder_data}")
        
        # Check if we have a medication reminder manager available
        app = App.get_running_app()
        reminder_screen = None
        
        # First check if reminder screen exists in the screen manager
        if 'reminder' in app.root.screen_names:
            reminder_screen = app.root.get_screen('reminder')
            print("Found existing reminder screen")
        else:
            # Create and add the reminder screen if it doesn't exist
            print("Creating new reminder screen")
            reminder_screen = ReminderScreen(name='reminder')
            app.root.add_widget(reminder_screen)
        
        # Direct access to reminder manager for testing
        from medication_reminder import MedicationReminder
        if not hasattr(reminder_screen, 'reminder_manager') or not reminder_screen.reminder_manager:
            print("Reminder screen doesn't have a working reminder manager, creating one directly")
            try:
                # Try to create a reminder manager directly
                reminder_manager = MedicationReminder()
                reminder_screen.reminder_manager = reminder_manager
            except Exception as import_e:
                print(f"Failed to create MedicationReminder: {import_e}")
                self.add_message("I'm sorry, I couldn't create a reminder because the reminder system is not available.", is_user=False)
                return
            
        print(f"Reminder manager status: {reminder_screen.reminder_manager}")
        
        # Extract reminder data
        medication_name = reminder_data.get('medication')
        dosage = reminder_data.get('dosage')
        frequency = reminder_data.get('frequency')
        duration = reminder_data.get('duration')
        
        print(f"Extracted data: med={medication_name}, dosage={dosage}, freq={frequency}, duration={duration}")
        
        # Check required fields
        if not medication_name or not dosage or not frequency:
            self.add_message("I couldn't create the reminder because some required information is missing.", is_user=False)
            return
        
        # Add the reminder
        try:
            # Explicitly call the add_reminder method with proper arguments
            print("Calling add_reminder method")
            
            reminder_id = reminder_screen.reminder_manager.add_reminder(
                medication_name=medication_name,
                dosage=dosage,
                frequency=frequency,
                duration=duration,
                notes="Created by AI assistant"
            )
            
            print(f"Reminder created with ID: {reminder_id}")
            
            # Confirm success and suggest viewing reminder
            self.add_message("I've successfully created your medication reminder! Would you like to view it now in the Reminders section?", is_user=False)
            
            # Ask if they want to go to the reminder screen
            self.add_message("Say 'show reminders' if you want to see your new reminder.", is_user=False)
            
        except Exception as e:
            print(f"Error adding reminder: {e}")
            import traceback
            traceback.print_exc()
            self.add_message(f"I had trouble creating your reminder: {str(e)}. You can try adding it manually from the Reminders section.", is_user=False)

# Settings Screen - Hides the bar
class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        
        # Add title bar
        title_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(80),
            pos_hint={'top': 1},
            padding=[0, dp(15), 0, 0]
        )
        
        # Add title
        title = Label(
            text='Settings',
            font_size=dp(30),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, 1),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        title.bind(size=title.setter('text_size'))
        
        title_bar.add_widget(title)
        self.main_layout.add_widget(title_bar)
        
        # Add a logout button with cream background
        logout_btn = Button(
            text='Logout',
            font_size=dp(16),
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'right': 0.98, 'top': 0.98},
            background_normal='',  # Remove default background 
            background_color=(0.85, 0.82, 0.78, 1),  # Cream/beige color
            color=(0.1, 0.1, 0.1, 1),
            bold=True
        )
        logout_btn.bind(on_press=self.logout)
        self.main_layout.add_widget(logout_btn)
        
        # Create settings layout
        settings_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20)],
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Add some sample settings
        settings = [
            {'name': 'Notifications', 'status': 'ON'},
            {'name': 'Dark Mode', 'status': 'OFF'},
            {'name': 'Sound', 'status': 'ON'},
            {'name': 'Vibration', 'status': 'ON'},
            {'name': 'Language', 'status': 'English'}
        ]
        
        # Add settings items
        for setting in settings:
            item = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50)
            )
            
            name = Label(
                text=setting['name'],
                font_size=dp(18),
                color=(0.1, 0.1, 0.1, 1),
                halign='left',
                size_hint=(0.7, 1)
            )
            
            status = Label(
                text=setting['status'],
                font_size=dp(18),
                color=(0.5, 0.5, 0.5, 1),
                halign='right',
                size_hint=(0.3, 1)
            )
            
            item.add_widget(name)
            item.add_widget(status)
            settings_layout.add_widget(item)
        
        self.main_layout.add_widget(settings_layout)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        
        # Main layout with theme-based background
        main_layout = FloatLayout()
        
        # Set background color based on theme
        with main_layout.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Default color, will be updated by theme
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
            main_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Store the username label for later reference
        self.username_label = Label(
            text='Username',  # This will be updated with actual username
            font_size=dp(18),
            color=(0.1, 0.1, 0.1, 1),  # Will be updated by theme
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Create top bar container
        self.top_container = FloatLayout(size_hint=(1, None), height=dp(60))
        self.top_container.pos_hint = {'x': 0, 'top': 1}  # Position at top
        
        # Create top bar background with theme-based color
        with self.top_container.canvas.before:
            self.top_shadow_color = Color(0.7, 0.7, 0.7, 0.2)  # Will be updated by theme
            RoundedRectangle(
                pos=(self.top_container.x + dp(4), self.top_container.y - dp(4)),
                size=(self.top_container.width, self.top_container.height),
                radius=[(0, 0, dp(20), dp(20))]
            )
            
            self.top_shadow_color2 = Color(0.75, 0.75, 0.75, 0.5)  # Will be updated by theme
            RoundedRectangle(
                pos=(self.top_container.x + dp(2), self.top_container.y - dp(2)),
                size=(self.top_container.width, self.top_container.height),
                radius=[(0, 0, dp(20), dp(20))]
            )
            
            self.top_bg_color = Color(0.92, 0.92, 0.92, 1)  # Will be updated by theme
            self.top_rect = RoundedRectangle(
                pos=(self.top_container.x, self.top_container.y),
                size=(self.top_container.width, self.top_container.height),
                radius=[(0, 0, dp(20), dp(20))]
            )
            self.top_container.bind(pos=self._update_top_rect, size=self._update_top_rect)
        
        # Add username label to top bar
        self.top_container.add_widget(self.username_label)
        
        # Add top container to main layout
        main_layout.add_widget(self.top_container)
        
        # Create bottom navigation bar container
        self.nav_container = FloatLayout(size_hint=(1, None), height=dp(80))
        self.nav_container.pos_hint = {'x': 0, 'y': 0}  # Position at bottom
        
        # Create rounded navigation bar background with theme-based colors
        with self.nav_container.canvas.before:
            self.nav_shadow_color = Color(0.7, 0.7, 0.7, 0.2)  # Will be updated by theme
            RoundedRectangle(
                pos=(self.nav_container.x + dp(4), self.nav_container.y - dp(4)),
                size=(self.nav_container.width, self.nav_container.height),
                radius=[(dp(20), dp(20), 0, 0)]
            )
            
            self.nav_shadow_color2 = Color(0.75, 0.75, 0.75, 0.5)  # Will be updated by theme
            RoundedRectangle(
                pos=(self.nav_container.x + dp(2), self.nav_container.y - dp(2)),
                size=(self.nav_container.width, self.nav_container.height),
                radius=[(dp(20), dp(20), 0, 0)]
            )
            
            self.nav_bg_color = Color(0.92, 0.92, 0.92, 1)  # Will be updated by theme
            self.nav_rect = RoundedRectangle(
                pos=(self.nav_container.x, self.nav_container.y),
                size=(self.nav_container.width, self.nav_container.height),
                radius=[(dp(20), dp(20), 0, 0)]
            )
            self.nav_container.bind(pos=self._update_nav_rect, size=self._update_nav_rect)
        
        # Create navigation bar
        nav_bar = BoxLayout(
            size_hint=(0.95, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=dp(10),
            padding=[dp(10), dp(5), dp(10), dp(5)]
        )
        
        # Create regular navigation buttons with icons
        buttons = [
            {'icon': 'home', 'text': 'Home'},
            {'icon': 'reminder', 'text': 'Reminder'},
            {'icon': 'camera', 'text': 'Camera'},
            {'icon': 'voice', 'text': 'Voice'},
            {'icon': 'settings', 'text': 'Settings'}
        ]
        
        # Add all buttons to the navigation bar
        for i, btn in enumerate(buttons):
            button = IconButton(
                icon_type=btn['icon'],
                text=btn['text']
            )
            nav_bar.add_widget(button)
        
        # Add navigation bar to container
        self.nav_container.add_widget(nav_bar)
        
        # Add navigation container to main layout
        main_layout.add_widget(self.nav_container)
        
        # Add welcome message in the center
        welcome_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.welcome_label = Label(
            text='Home Page',
            font_size=dp(24),
            color=(0.2, 0.2, 0.2, 1)  # Will be updated by theme
        )
        welcome_layout.add_widget(self.welcome_label)
        main_layout.add_widget(welcome_layout)
        
        self.add_widget(main_layout)
        
        # Update theme initially
        self.update_theme()
        
        # Bind to theme changes
        self.theme_manager.bind(is_dark_mode=self.update_theme)
    
    def update_theme(self, *args):
        """Update colors based on current theme"""
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update background color
        self.bg_color.rgba = colors['background']
        
        # Update text colors
        self.username_label.color = colors['text']
        self.welcome_label.color = colors['text']
        
        # Update top bar colors
        if is_dark:
            self.top_shadow_color.rgba = (0.1, 0.1, 0.1, 0.4)
            self.top_shadow_color2.rgba = (0.1, 0.1, 0.1, 0.6)
            self.top_bg_color.rgba = (0.2, 0.2, 0.2, 1)
        else:
            self.top_shadow_color.rgba = (0.7, 0.7, 0.7, 0.2)
            self.top_shadow_color2.rgba = (0.75, 0.75, 0.75, 0.5)
            self.top_bg_color.rgba = (0.92, 0.92, 0.92, 1)
        
        # Update navigation bar colors
        if is_dark:
            self.nav_shadow_color.rgba = (0.1, 0.1, 0.1, 0.4)
            self.nav_shadow_color2.rgba = (0.1, 0.1, 0.1, 0.6)
            self.nav_bg_color.rgba = (0.2, 0.2, 0.2, 1)
        else:
            self.nav_shadow_color.rgba = (0.7, 0.7, 0.7, 0.2)
            self.nav_shadow_color2.rgba = (0.75, 0.75, 0.75, 0.5)
            self.nav_bg_color.rgba = (0.92, 0.92, 0.92, 1)
    
    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _update_nav_rect(self, instance, value):
        self.nav_rect.pos = (instance.x, instance.y)
        self.nav_rect.size = (instance.width, instance.height)
    
    def _update_top_rect(self, instance, value):
        self.top_rect.pos = (instance.x, instance.y)
        self.top_rect.size = (instance.width, instance.height)
    
    def update_username(self, username):
        self.username_label.text = f"Welcome, {username}!"
        # Make sure the username label is visible and properly positioned
        if hasattr(self, 'top_container'):
            self.username_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.username_label.size_hint = (None, None)
            self.username_label.size = (dp(250), dp(40))
            # Adjust font size for longer names
            if len(username) > 10:
                self.username_label.font_size = dp(16)
            else:
                self.username_label.font_size = dp(18)
    
    def navigate_to(self, screen_type):
        print(f"Navigating to {screen_type} screen")
        app = App.get_running_app()
        
        # Check if screen exists first
        if screen_type == 'home':
            # Already on home screen, no need to navigate
            return
        elif screen_type not in app.root.screen_names:
            # Create the screen if it doesn't exist
            if screen_type == 'reminder':
                app.root.add_widget(ReminderScreen(name='reminder'))
            elif screen_type == 'camera':
                app.root.add_widget(CameraScreen(name='camera'))
            elif screen_type == 'voice':
                app.root.add_widget(VoiceScreen(name='voice'))
            elif screen_type == 'settings':
                app.root.add_widget(SettingsScreen(name='settings'))
        
        # Navigate to the screen
        app.root.current = screen_type
    
    def logout(self, instance):
        # Clear current user and go back to login screen
        app = App.get_running_app()
        app.current_user = None
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'