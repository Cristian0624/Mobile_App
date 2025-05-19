from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from datetime import datetime, timedelta
import time
from plyer import notification

class TimerWidget(BoxLayout):
    """Widget that displays a countdown timer for medication reminders"""
    
    time_remaining = NumericProperty(0)  # In seconds
    medication_name = StringProperty('')
    dosage = StringProperty('')
    is_running = BooleanProperty(False)
    max_time = NumericProperty(0)  # Total duration in seconds
    on_complete = ObjectProperty(None)
    reminder_id = StringProperty('')
    
    def __init__(self, reminder_data, **kwargs):
        super(TimerWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(180)
        self.padding = [dp(15), dp(15)]
        self.spacing = dp(10)
        
        # Set data from reminder
        self.reminder_id = reminder_data.get('id', '')
        self.medication_name = reminder_data.get('medication_name', 'Medication')
        self.dosage = reminder_data.get('dosage', '')
        
        # Calculate time until next dose
        next_time = reminder_data.get('next_time')
        if next_time and isinstance(next_time, datetime):
            now = datetime.now()
            if next_time > now:
                time_diff = next_time - now
                self.time_remaining = time_diff.total_seconds()
                self.max_time = self.time_remaining
            else:
                self.time_remaining = 0
                self.max_time = 0
        
        # Set up background with rounded corners
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Add medication name and dosage
        title_layout = BoxLayout(size_hint=(1, None), height=dp(30))
        title = Label(
            text=f"{self.medication_name} - {self.dosage}",
            font_size=dp(18),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )
        title.bind(size=title.setter('text_size'))
        title_layout.add_widget(title)
        self.add_widget(title_layout)
        
        # Add time remaining label
        self.time_label = Label(
            text=self._format_time(self.time_remaining),
            font_size=dp(24),
            bold=True,
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(1, None),
            height=dp(40),
            halign='center'
        )
        self.add_widget(self.time_label)
        
        # Add progress bar
        self.progress = ProgressBar(
            max=self.max_time,
            value=self.time_remaining,
            size_hint=(1, None),
            height=dp(20)
        )
        self.add_widget(self.progress)
        
        # Add buttons
        button_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        self.take_now_btn = Button(
            text="Take Now",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 1),  # Green
            color=(1, 1, 1, 1)
        )
        self.take_now_btn.bind(on_release=self.take_medication_now)
        
        self.skip_btn = Button(
            text="Skip",
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.7, 0.7, 0.7, 1),  # Grey
            color=(1, 1, 1, 1)
        )
        self.skip_btn.bind(on_release=self.skip_dose)
        
        button_layout.add_widget(self.take_now_btn)
        button_layout.add_widget(self.skip_btn)
        self.add_widget(button_layout)
        
        # Start the timer if time remaining is greater than 0
        if self.time_remaining > 0:
            self.start_timer()
    
    def _update_rect(self, instance, value):
        """Update the background rectangle when size/position changes"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def _format_time(self, seconds):
        """Format seconds into a readable time string"""
        if seconds <= 0:
            return "Due Now!"
            
        total_seconds = int(seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def start_timer(self):
        """Start the countdown timer"""
        self.is_running = True
        Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        """Update the timer each second"""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.progress.value = self.time_remaining
            self.time_label.text = self._format_time(self.time_remaining)
            
            # Update colors based on time remaining
            if self.time_remaining < 60:  # Less than a minute
                self.time_label.color = (0.9, 0.3, 0.3, 1)  # Red
            elif self.time_remaining < 300:  # Less than 5 minutes
                self.time_label.color = (0.9, 0.6, 0.1, 1)  # Orange
            
            return True
        else:
            self.is_running = False
            self.time_label.text = "Due Now!"
            self.time_label.color = (0.9, 0.3, 0.3, 1)  # Red
            self.show_notification()
            return False
    
    def take_medication_now(self, instance):
        """Handle when user takes medication now"""
        # Stop the timer
        if self.is_running:
            self.is_running = False
            Clock.unschedule(self.update_timer)
        
        # Show a confirmation popup
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        msg_label = Label(
            text=f"Did you take your {self.medication_name} ({self.dosage})?",
            size_hint=(1, None),
            height=dp(40)
        )
        
        buttons = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))
        
        def confirm_taken(btn):
            popup.dismiss()
            self.record_taken()
            
        def cancel(btn):
            popup.dismiss()
        
        yes_btn = Button(text="Yes", size_hint=(0.5, 1), background_color=(0.2, 0.7, 0.3, 1), color=(1, 1, 1, 1))
        yes_btn.bind(on_release=confirm_taken)
        
        no_btn = Button(text="No", size_hint=(0.5, 1), background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        no_btn.bind(on_release=cancel)
        
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        
        content.add_widget(msg_label)
        content.add_widget(buttons)
        
        popup = Popup(
            title="Confirm Medication",
            content=content,
            size_hint=(0.8, None),
            height=dp(150),
            auto_dismiss=True
        )
        popup.open()
    
    def record_taken(self):
        """Record that medication was taken and update next dose time"""
        if self.on_complete:
            self.on_complete(self.reminder_id, 'taken')
    
    def skip_dose(self, instance):
        """Handle when user skips a dose"""
        # Show a confirmation popup
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        msg_label = Label(
            text=f"Are you sure you want to skip this dose of {self.medication_name}?",
            size_hint=(1, None),
            height=dp(40)
        )
        
        buttons = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))
        
        def confirm_skip(btn):
            popup.dismiss()
            if self.is_running:
                self.is_running = False
                Clock.unschedule(self.update_timer)
            if self.on_complete:
                self.on_complete(self.reminder_id, 'skipped')
            
        def cancel(btn):
            popup.dismiss()
        
        yes_btn = Button(text="Yes, Skip", size_hint=(0.5, 1), background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        yes_btn.bind(on_release=confirm_skip)
        
        no_btn = Button(text="No", size_hint=(0.5, 1), background_color=(0.2, 0.7, 0.3, 1), color=(1, 1, 1, 1))
        no_btn.bind(on_release=cancel)
        
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        
        content.add_widget(msg_label)
        content.add_widget(buttons)
        
        popup = Popup(
            title="Skip Dose",
            content=content,
            size_hint=(0.8, None),
            height=dp(150),
            auto_dismiss=True
        )
        popup.open()
    
    def show_notification(self):
        """Show a notification that it's time to take medication"""
        try:
            notification.notify(
                title=f"Time to take {self.medication_name}",
                message=f"It's time to take your {self.dosage} of {self.medication_name}",
                app_name="Medicine Assistant",
                timeout=10
            )
        except Exception as e:
            print(f"Failed to show notification: {e}") 