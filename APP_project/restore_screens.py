def create_voice_screen():
    """Create a file with the VoiceScreen class implementation"""
    voice_screen_code = '''
class VoiceScreen(BaseScreen):
    def __init__(self, **kwargs):
        # First initialize the parent BaseScreen with auto_update_theme=False
        super().__init__(auto_update_theme=False, **kwargs)
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        
        # Create a medication context for AI assistant
        self.medication_context = ""
        
        # Create layout for messages
        self.messages_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=[dp(10), dp(0)])
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        
        # Create scroll view for messages
        self.scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={'top': 0.9})
        self.scroll_view.add_widget(self.messages_layout)
        self.main_layout.add_widget(self.scroll_view)
        
        # Add title with improved styling
        self.title_label = Label(
            text=tr('ai_assistant'),
            font_size=dp(24),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),  # Blue text
            size_hint=(1, 0.1),
            pos_hint={'top': 1}
        )
        self.main_layout.add_widget(self.title_label)
        
        # Add text input field at the bottom
        self.input_layout = BoxLayout(size_hint=(1, 0.1), pos_hint={'y': 0}, spacing=dp(5), padding=[dp(5), dp(5)])
        
        self.text_input = TextInput(
            hint_text=tr('ask_something'),
            multiline=False,
            font_size=dp(16),
            size_hint=(0.8, 1),
            background_normal='',
            background_active='',
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        self.text_input.bind(on_text_validate=self.send_text_message)
        
        self.send_button = Button(
            text=tr('send'),
            size_hint=(0.2, 1),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.send_button.bind(on_press=self.send_text_message)
        
        self.input_layout.add_widget(self.text_input)
        self.input_layout.add_widget(self.send_button)
        self.main_layout.add_widget(self.input_layout)
        
        # Add a pulsing mic button for voice input
        self.mic_button = PulsingMicButton()
        self.mic_button.bind(on_press=self.toggle_listening)
        self.main_layout.add_widget(self.mic_button)
        
        # Add a listening status label
        self.status_label = Label(
            text="",
            font_size=dp(14),
            size_hint=(1, 0.05),
            pos_hint={'y': 0.1},
            color=(0.5, 0.5, 0.5, 1)
        )
        self.main_layout.add_widget(self.status_label)
        
        # Flag to track if we're currently listening
        self.is_listening = False
        
        # Add a welcome message with a slight delay
        Clock.schedule_once(self.add_welcome_message, 0.5)
        
        # Bind to language changes
        self.language_manager.bind(current_language=self._update_language)
        
        # Get a medication reminder manager
        try:
            from medication_reminder import MedicationReminder
            self.reminder_manager = MedicationReminder()
        except ImportError:
            try:
                from medication_reminder_mock import MockMedicationReminder
                self.reminder_manager = MockMedicationReminder()
                print("MedicationReminder class not found, using a mock implementation")
            except ImportError:
                self.reminder_manager = None
                print("Could not load any medication reminder implementation")
        
        # Now that all UI elements are created, we can call update_theme
        self.update_theme()
    
    def _update_language(self, *args):
        """Update all text elements with the current language"""
        try:
            if hasattr(self, 'title_label'):
                self.title_label.text = tr('ai_assistant')
            if hasattr(self, 'text_input'):
                self.text_input.hint_text = tr('ask_something')
            if hasattr(self, 'send_button'):
                self.send_button.text = tr('send')
        except Exception as e:
            print(f"Error updating language in VoiceScreen: {e}")
    
    def update_theme(self, *args):
        """Override BaseScreen's update_theme to handle specific UI elements"""
        # First call parent's update_theme to handle basic elements
        super(VoiceScreen, self).update_theme(*args)
        
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update title with proper color
        if hasattr(self, 'title_label'):
            self.title_label.color = colors['text']
        
        # Update text input with theme colors
        if hasattr(self, 'text_input'):
            self.text_input.background_color = colors['input_bg']
            self.text_input.foreground_color = colors['text']
            
        # Update send button with theme colors
        if hasattr(self, 'send_button'):
            self.send_button.background_color = colors['button_bg']
            self.send_button.color = colors['button_text']
            
        # Update status label
        if hasattr(self, 'status_label'):
            self.status_label.color = colors['text']
            
        # Update all chat bubbles
        for child in self.messages_layout.children:
            if isinstance(child, ChatBubble) and hasattr(child, 'update_theme'):
                child.update_theme(is_dark)
                
        # Update background color
        with self.canvas.before:
            self.bg_color.rgba = colors['background']
'''

    camera_screen_code = '''
class CameraScreen(BaseScreen):
    def __init__(self, **kwargs):
        # First initialize the parent BaseScreen with auto_update_theme=False
        try:
            super().__init__(auto_update_theme=False, **kwargs)
            self.language_manager = LanguageManager()
        except Exception as e:
            print(f"Error initializing CameraScreen: {e}")
            return
            
        try:
            # Add title with improved styling
            self.title_label = Label(
                text=tr('medication_images'),
                font_size=dp(24),
                bold=True,
                color=(0.2, 0.4, 0.8, 1),  # Blue text
                pos_hint={'center_x': 0.5, 'top': 0.95}
            )
            self.main_layout.add_widget(self.title_label)
            
            # Add camera content
            self.content_label = Label(
                text=tr('camera_feature_description'),
                font_size=dp(18),
                color=(0.3, 0.3, 0.3, 1),
                halign='center',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_layout.add_widget(self.content_label)
            
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
            self.coming_soon_btn = Button(
                text=tr("coming_soon"),
                size_hint=(0.5, None),
                height=dp(50),
                pos_hint={'center_x': 0.5, 'center_y': 0.3},
                background_normal='',
                background_color=self.theme_manager.get_button_color(),
                color=self.theme_manager.get_button_text_color()
            )
            self.main_layout.add_widget(self.coming_soon_btn)
            
            # Bind to language changes to update text
            self.language_manager.bind(current_language=self._update_language)
            
            # Now that all UI elements are created, we can call update_theme
            self.update_theme()
            
        except Exception as e:
            # If anything fails, add an error message instead of crashing
            print(f"Error setting up CameraScreen: {e}")
            self.error_label = Label(
                text=tr('error_loading_screen'),
                font_size=dp(18),
                color=(0.8, 0.3, 0.3, 1),  # Red text
                halign='center',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_layout.add_widget(self.error_label)
    
    def _update_language(self, *args):
        """Update all text elements with the current language"""
        try:
            if hasattr(self, 'title_label'):
                self.title_label.text = tr('medication_images')
            if hasattr(self, 'content_label'):
                self.content_label.text = tr('camera_feature_description')
            if hasattr(self, 'coming_soon_btn'):
                self.coming_soon_btn.text = tr('coming_soon')
            if hasattr(self, 'error_label'):
                self.error_label.text = tr('error_loading_screen')
        except Exception as e:
            print(f"Error updating language in CameraScreen: {e}")
    
    def update_theme(self, *args):
        """Update UI elements based on current theme"""
        # Call parent's update_theme to handle basic elements
        super(CameraScreen, self).update_theme(*args)
        
        # Get theme colors
        colors = self.theme_manager.get_colors()
        is_dark = self.theme_manager.is_dark_mode
        
        # Update specific elements for this screen
        if hasattr(self, 'title_label'):
            self.title_label.color = colors['text']
        
        # Update all labels
        for child in self.walk(restrict=True):
            if isinstance(child, Label):
                child.color = colors['text']
            elif isinstance(child, Button) and not isinstance(child, RoundedButton):
                if hasattr(self, 'back_button') and child != self.back_button:
                    child.background_color = colors['button_bg']
                    child.color = colors['button_text']
        
        # Update background color
        with self.canvas.before:
            self.bg_color.rgba = colors['background']
'''

    # Read the home.py file
    with open('home.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where the VoiceScreen and CameraScreen classes should be
    voice_screen_pos = content.find("class VoiceScreen(BaseScreen):")
    camera_screen_pos = content.find("class CameraScreen(BaseScreen):")
    
    if voice_screen_pos == -1:
        # Find where to insert the VoiceScreen class
        voice_screen_insertion_point = content.find("class HomeScreen(Screen):")
        if voice_screen_insertion_point != -1:
            # Insert before HomeScreen
            content = content[:voice_screen_insertion_point] + voice_screen_code + content[voice_screen_insertion_point:]
            print("Added VoiceScreen class")
    
    if camera_screen_pos != -1:
        # Find the next class after CameraScreen
        next_class_pos = content.find("class", camera_screen_pos + 10)
        if next_class_pos != -1:
            # Replace the CameraScreen class
            content = content[:camera_screen_pos] + camera_screen_code + content[next_class_pos:]
            print("Replaced CameraScreen class")
    
    # Write the updated content back to the file
    with open('home.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Restored VoiceScreen and fixed CameraScreen")

if __name__ == "__main__":
    create_voice_screen() 