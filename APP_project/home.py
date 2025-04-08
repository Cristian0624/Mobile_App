from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.image import Image
import math

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
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.spacing = dp(5)
        self.padding = dp(5)
        
        # Map icon types to icon image files
        icon_mapping = {
            'home': 'icons/home-icon-silhouette.png',
            'reminder': 'icons/alarm.png',
            'camera': 'icons/camera.png',
            'voice': 'icons/microphone.png',
            'settings': 'icons/gear.png'
        }
        
        # Create an image widget for the icon
        self.icon_image = Image(
            source=icon_mapping.get(self.icon_type, ''),
            size_hint=(None, None),
            size=(dp(30), dp(30)),  # Standard size for non-camera icons
            allow_stretch=True,
            keep_ratio=True
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
            font_size=dp(11),  # Standard size for all buttons
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, None),
            height=dp(20),
            bold=True,
            halign='center'  # Center text horizontally
        )
        label_layout.add_widget(self.label)
        self.add_widget(label_layout)
        
        # Bind properties
        self.bind(icon_type=self._update_icon)
        self.bind(text=self._update_text)
    
    def _update_icon(self, instance, value):
        # Map icon types to icon image files
        icon_mapping = {
            'home': 'icons/home-icon-silhouette.png',
            'reminder': 'icons/alarm.png',
            'camera': 'icons/camera.png',
            'voice': 'icons/microphone.png',
            'settings': 'icons/gear.png'
        }
        self.icon_image.source = icon_mapping.get(value, '')
    
    def _update_text(self, instance, value):
        self.label.text = value
    
    def on_press(self):
        # Change icon and text to black when pressed
        self.icon_image.color = (0, 0, 0, 1)
        self.label.color = (0, 0, 0, 1)
        
        # Get the HomeScreen instance to handle navigation
        app = App.get_running_app()
        if hasattr(app.root.current_screen, 'navigate_to'):
            app.root.current_screen.navigate_to(self.icon_type)
    
    def on_release(self):
        # Restore original colors
        self.icon_image.color = (1, 1, 1, 1)
        self.label.color = (0.1, 0.1, 0.1, 1)

# Base Screen for all other screens
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        
        # Main layout with cream background
        self.main_layout = FloatLayout()
        
        # Set cream background color
        with self.main_layout.canvas.before:
            Color(0.99, 0.99, 0.99, 1)  # Very light, almost white
            self.bg_rect = Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
            self.main_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add a back arrow button to return to home with darker cream background
        self.back_arrow = Button(
            text='<',
            font_size=dp(30),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'x': 0.02, 'top': 0.98},
            background_color=(0.85, 0.82, 0.78, 1),  # Darker cream/beige color
            color=(0.1, 0.1, 0.1, 1),
            bold=True
        )
        self.back_arrow.bind(on_press=self.go_back_home)
        self.main_layout.add_widget(self.back_arrow)
        
        self.add_widget(self.main_layout)
    
    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def go_back_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'
    
    def logout(self, instance):
        # Clear current user and go back to login screen
        app = App.get_running_app()
        app.current_user = None
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'

# Reminder Screen - Hides the bar
class ReminderScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(ReminderScreen, self).__init__(**kwargs)
        
        # Add title
        title = Label(
            text='Reminders',
            font_size=dp(30),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.main_layout.add_widget(title)
        
        # Add reminder content
        content = Label(
            text='This is where your reminders would appear.\nThe navigation bar is hidden on this screen.',
            font_size=dp(18),
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(content)

# Camera Screen - Shows the bars
class CameraScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        
        # Add title
        title = Label(
            text='Camera',
            font_size=dp(30),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.main_layout.add_widget(title)
        
        # Add camera content
        content = Label(
            text='This is the camera screen.\nYou would see a camera feed here.',
            font_size=dp(18),
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(content)
        
        # Add camera icon for visual indication
        camera_icon = Image(
            source='icons/camera.png',
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.main_layout.add_widget(camera_icon)

# Voice Assistant Screen - Hides the bar
class VoiceScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(VoiceScreen, self).__init__(**kwargs)
        
        # Add title
        title = Label(
            text='Voice Assistant',
            font_size=dp(30),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.main_layout.add_widget(title)
        
        # Add voice content
        content = Label(
            text='This is the voice assistant screen.\nSpeak a command to interact.',
            font_size=dp(18),
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(content)
        
        # Add microphone icon for visual indication
        mic_icon = Image(
            source='icons/microphone.png',
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.main_layout.add_widget(mic_icon)

# Settings Screen - Hides the bar
class SettingsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        
        # Add title
        title = Label(
            text='Settings',
            font_size=dp(30),
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.main_layout.add_widget(title)
        
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
        
        # Main layout with cream background
        main_layout = FloatLayout()
        
        # Set cream background color
        with main_layout.canvas.before:
            Color(0.99, 0.99, 0.99, 1)  # Very light, almost white
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
            main_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Store the username label for later reference
        self.username_label = Label(
            text='Username',  # This will be updated with actual username
            font_size=dp(18),
            color=(0.1, 0.1, 0.1, 1),
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Create top bar container
        self.top_container = FloatLayout(size_hint=(1, None), height=dp(60))
        self.top_container.pos_hint = {'x': 0, 'top': 1}  # Position at top
        
        # Create top bar background with same color as nav bar
        with self.top_container.canvas.before:
            # Multiple shadow layers for depth
            # First shadow layer (farthest)
            Color(0.7, 0.7, 0.7, 0.2)  # Light gray shadow
            RoundedRectangle(
                pos=(self.top_container.x + dp(4), self.top_container.y - dp(4)),
                size=(self.top_container.width, self.top_container.height),
                radius=[(0, 0, dp(20), dp(20))]  # Rounded corners at bottom
            )
            
            # Second shadow layer (closer)
            Color(0.75, 0.75, 0.75, 0.5)  # Medium gray shadow
            RoundedRectangle(
                pos=(self.top_container.x + dp(2), self.top_container.y - dp(2)),
                size=(self.top_container.width, self.top_container.height),
                radius=[(0, 0, dp(20), dp(20))]
            )
            
            # Main top bar
            Color(0.92, 0.92, 0.92, 1)  # Same color as nav bar
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
        
        # Create rounded navigation bar background with enhanced shadow
        with self.nav_container.canvas.before:
            # Multiple shadow layers for depth
            # First shadow layer (farthest)
            Color(0.7, 0.7, 0.7, 0.2)  # Light gray shadow
            RoundedRectangle(
                pos=(self.nav_container.x + dp(4), self.nav_container.y - dp(4)),  # Larger offset
                size=(self.nav_container.width, self.nav_container.height),
                radius=[(dp(20), dp(20), 0, 0)]
            )
            
            # Second shadow layer (closer)
            Color(0.75, 0.75, 0.75, 0.5)  # Medium gray shadow
            RoundedRectangle(
                pos=(self.nav_container.x + dp(2), self.nav_container.y - dp(2)),  # Medium offset
                size=(self.nav_container.width, self.nav_container.height),
                radius=[(dp(20), dp(20), 0, 0)]
            )
            
            # Main navigation bar
            Color(0.92, 0.92, 0.92, 1)  # Darker than before
            self.nav_rect = RoundedRectangle(
                pos=(self.nav_container.x, self.nav_container.y),
                size=(self.nav_container.width, self.nav_container.height),
                radius=[(dp(20), dp(20), 0, 0)]  # Rounded corners only at top
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
        welcome_label = Label(
            text='Home Page',
            font_size=dp(24),
            color=(0.2, 0.2, 0.2, 1)
        )
        welcome_layout.add_widget(welcome_label)
        main_layout.add_widget(welcome_layout)
        
        self.add_widget(main_layout)
    
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
