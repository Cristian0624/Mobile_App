with open('home.py', 'r') as f:
    content = f.read()

# Define the setup_dialog method
setup_dialog_method = """    def setup_dialog(self):
        \"\"\"Set up the dialog for adding/editing reminders\"\"\"
        self.dialog_bg = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0  # Hidden initially
        )
        
        # Semi-transparent background
        with self.dialog_bg.canvas.before:
            Color(0, 0, 0, 0.8)  # Even darker background for better contrast
            self.bg_rect = Rectangle(pos=self.dialog_bg.pos, size=self.dialog_bg.size)
        self.dialog_bg.bind(pos=self._update_bg_rect, size=self._update_bg_rect)
        
        # Create dialog content
        self.dialog = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, None),
            height=dp(500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=[dp(15), dp(15), dp(15), dp(30)],
            spacing=dp(8)
        )
        
        # Set colors based on theme
        is_dark = self.theme_manager.is_dark_mode
        bg_color = (0.2, 0.2, 0.2, 1) if is_dark else (0.95, 0.95, 0.95, 1)
        text_color = (0.9, 0.9, 0.9, 1) if is_dark else (0.2, 0.2, 0.2, 1)
        
        with self.dialog.canvas.before:
            Color(*bg_color)
            self.dialog_rect = RoundedRectangle(pos=self.dialog.pos, size=self.dialog.size, radius=[dp(10)])
        self.dialog.bind(pos=self._update_dialog_rect, size=self._update_dialog_rect)
        
        # Dialog title - make it much more visible with a background
        title_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(50),
            padding=[0, dp(5), 0, dp(10)]
        )
        
        with title_container.canvas.before:
            Color(0.2, 0.6, 0.9, 1) if not is_dark else Color(0.3, 0.3, 0.5, 1)  # Blue background
            self.title_bg = RoundedRectangle(pos=title_container.pos, size=title_container.size, radius=[dp(5)])
            title_container.bind(pos=self._update_title_bg, size=self._update_title_bg)
        
        self.dialog_title = Label(
            text="Add Reminder",  # Hardcoded for visibility, will be updated by language manager
            font_size=dp(22),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)  # White text for better contrast
        )
        title_container.add_widget(self.dialog_title)
        self.dialog.add_widget(title_container)
        
        # Medication name field with required indicator
        name_label = Label(
            text=self.language_manager.get_text('medication_name') + " *",  # Add asterisk to indicate required field
            size_hint_y=None,
            height=dp(25),  # Smaller height
            halign='left',
            font_size=dp(16),
            color=text_color
        )
        name_label.bind(size=lambda *x: setattr(name_label, 'text_size', name_label.size))
        self.dialog.add_widget(name_label)
        
        self.name_input = TextInput(
            hint_text=self.language_manager.get_text('enter_medication_name'),
            multiline=False,
            size_hint_y=None,
            height=dp(40),  # Smaller height
            font_size=dp(16),
            foreground_color=text_color,
            background_color=(1, 1, 1, 0.8) if not is_dark else (0.15, 0.15, 0.15, 1)
        )
        self.dialog.add_widget(self.name_input)
        
        # Dosage field
        dosage_label = Label(
            text=self.language_manager.get_text('dosage') + " *",
            size_hint_y=None,
            height=dp(25),  # Smaller height
            halign='left',
            font_size=dp(16),
            color=text_color
        )
        dosage_label.bind(size=lambda *x: setattr(dosage_label, 'text_size', dosage_label.size))
        self.dialog.add_widget(dosage_label)
        
        self.dosage_input = TextInput(
            hint_text=self.language_manager.get_text('enter_dosage'),
            multiline=False,
            size_hint_y=None,
            height=dp(40),  # Smaller height
            font_size=dp(16),
            foreground_color=text_color,
            background_color=(1, 1, 1, 0.8) if not is_dark else (0.15, 0.15, 0.15, 1)
        )
        self.dialog.add_widget(self.dosage_input)
        
        # Frequency field
        frequency_label = Label(
            text=self.language_manager.get_text('frequency') + " *",
            size_hint_y=None,
            height=dp(25),  # Smaller height
            halign='left',
            font_size=dp(16),
            color=text_color
        )
        frequency_label.bind(size=lambda *x: setattr(frequency_label, 'text_size', frequency_label.size))
        self.dialog.add_widget(frequency_label)
        
        self.frequency_input = TextInput(
            hint_text=self.language_manager.get_text('enter_frequency'),
            multiline=False,
            size_hint_y=None,
            height=dp(40),  # Smaller height
            font_size=dp(16),
            foreground_color=text_color,
            background_color=(1, 1, 1, 0.8) if not is_dark else (0.15, 0.15, 0.15, 1)
        )
        self.dialog.add_widget(self.frequency_input)
        
        # Duration field
        duration_label = Label(
            text=self.language_manager.get_text('duration_days'),
            size_hint_y=None,
            height=dp(25),  # Smaller height
            halign='left',
            font_size=dp(16),
            color=text_color
        )
        duration_label.bind(size=lambda *x: setattr(duration_label, 'text_size', duration_label.size))
        self.dialog.add_widget(duration_label)
        
        self.duration_input = TextInput(
            hint_text=self.language_manager.get_text('enter_duration'),
            multiline=False,
            size_hint_y=None,
            height=dp(40),  # Smaller height
            font_size=dp(16),
            input_filter='int',
            text='',
            foreground_color=text_color,
            background_color=(1, 1, 1, 0.8) if not is_dark else (0.15, 0.15, 0.15, 1)
        )
        self.dialog.add_widget(self.duration_input)
        
        # Notes field
        notes_label = Label(
            text=self.language_manager.get_text('notes'),
            size_hint_y=None,
            height=dp(25),  # Smaller height
            halign='left',
            font_size=dp(16),
            color=text_color
        )
        notes_label.bind(size=lambda *x: setattr(notes_label, 'text_size', notes_label.size))
        self.dialog.add_widget(notes_label)
        
        self.notes_input = TextInput(
            hint_text=self.language_manager.get_text('enter_notes'),
            multiline=True,
            size_hint_y=None,
            height=dp(60),  # Smaller height
            font_size=dp(16),
            foreground_color=text_color,
            background_color=(1, 1, 1, 0.8) if not is_dark else (0.15, 0.15, 0.15, 1)
        )
        self.dialog.add_widget(self.notes_input)
        
        # Button row
        buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        self.cancel_button = Button(
            text=self.language_manager.get_text('cancel'),
            size_hint_x=0.5,
            background_color=(0.9, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.cancel_button.bind(on_press=self.hide_dialog)
        buttons.add_widget(self.cancel_button)
        
        self.save_button = Button(
            text=self.language_manager.get_text('save'),
            size_hint_x=0.5,
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.save_button.bind(on_press=self.save_reminder)
        buttons.add_widget(self.save_button)
        
        self.dialog.add_widget(buttons)
        
        # Add to main layout but keep hidden
        self.dialog_bg.add_widget(self.dialog)
        self.main_layout.add_widget(self.dialog_bg)
        
        # Set up for editing mode
        self.editing_id = None"""

# Insert the new method before _update_top_rect
marker = "    def _update_top_rect(self, instance, value):"
updated_content = content.replace(marker, setup_dialog_method + "\n\n" + marker)

# Also add methods for handling the dialog
additional_methods = """
    def show_add_dialog(self, instance):
        \"\"\"Show dialog to add a new reminder\"\"\"
        print("Showing add dialog")
        
        # Make sure we're not already in the process of showing the dialog
        if self.dialog_bg.opacity == 1:
            return
            
        # Clear form
        self.name_input.text = ""
        self.dosage_input.text = ""
        self.frequency_input.text = ""
        self.duration_input.text = ""
        self.notes_input.text = ""
        
        # Set title and edit mode
        self.dialog_title.text = "Add Reminder"
        self.editing_id = None
        
        # Show dialog
        self.dialog_bg.opacity = 1
        
        # Focus on the name input
        Clock.schedule_once(lambda dt: setattr(self.name_input, 'focus', True), 0.1)
    
    def hide_dialog(self, instance=None):
        \"\"\"Hide the dialog for adding/editing reminders\"\"\"
        print("Hiding dialog")
        
        # Hide dialog
        self.dialog_bg.opacity = 0
    
    def edit_reminder(self, reminder_id):
        \"\"\"Show dialog to edit an existing reminder\"\"\"
        print(f"Editing reminder: {reminder_id}")
        if not self.reminder_manager:
            return
        
        # Get the reminder data
        reminder = self.reminder_manager.get_reminder(reminder_id)
        if not reminder:
            print("Reminder not found!")
            return
        
        # Set dialog to edit mode
        self.editing_id = reminder_id
        self.dialog_title.text = self.language_manager.get_text('edit_reminder')
        
        # Fill form with reminder data
        self.name_input.text = reminder.get('medication_name', '')
        self.dosage_input.text = reminder.get('dosage', '')
        self.frequency_input.text = reminder.get('frequency', '')
        self.duration_input.text = str(reminder.get('duration', '30'))
        self.notes_input.text = reminder.get('notes', '')
        
        # Show dialog
        self.dialog_bg.opacity = 1
    
    def save_reminder(self, instance):
        \"\"\"Save the current reminder (add or edit)\"\"\"
        print("Saving reminder")
        if not self.reminder_manager:
            self.hide_dialog()
            return
        
        # Get form data
        name = self.name_input.text.strip()
        dosage = self.dosage_input.text.strip()
        frequency = self.frequency_input.text.strip()
        duration = self.duration_input.text.strip()
        notes = self.notes_input.text.strip()
        
        # Validate required fields
        if not name:
            self.show_error_message("Medication name is required")
            self.name_input.focus = True
            return
            
        if not dosage:
            self.show_error_message("Dosage is required")
            self.dosage_input.focus = True
            return
            
        if not frequency:
            self.show_error_message("Frequency is required")
            self.frequency_input.focus = True
            return
        
        # Convert duration to integer if present
        duration_days = 30  # default
        if duration:
            try:
                duration_days = int(duration)
            except ValueError:
                self.show_error_message("Duration must be a number")
                self.duration_input.focus = True
                return
        
        # Create reminder data
        reminder_data = {
            'medication_name': name,
            'dosage': dosage,
            'frequency': frequency,
            'duration': duration_days,
            'notes': notes
        }
        
        # Save the reminder
        success = False
        if self.editing_id:
            # Update existing reminder
            success = self.reminder_manager.update_reminder(self.editing_id, reminder_data)
            message = "Reminder updated successfully"
        else:
            # Add new reminder
            success = self.reminder_manager.add_reminder(reminder_data)
            message = "Reminder added successfully"
        
        # Check result
        if success:
            self.show_message(message)
            self.hide_dialog()
            # Refresh the list
            Clock.schedule_once(lambda dt: self.refresh(), 0.5)
        else:
            self.show_error_message("Failed to save reminder")
    
    def show_error_message(self, message):
        \"\"\"Show an error message to the user\"\"\"
        popup = Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
        
    def show_message(self, message):
        \"\"\"Show a message to the user\"\"\"
        popup = Popup(
            title="Success",
            content=Label(text=message),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
        # Auto dismiss after 2 seconds
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def create_reminder_card(self, reminder_data):
        \"\"\"Create a card to display a reminder\"\"\"
        # Container for the whole card - make it centered
        card = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(200),
            padding=dp(10),
            spacing=dp(5)
        )
        
        # Set card background
        with card.canvas.before:
            Color(0.9, 0.9, 1, 1) if not self.theme_manager.is_dark_mode else Color(0.2, 0.2, 0.3, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
        card.bind(pos=lambda instance, value: self._update_card_bg(instance, card),
                  size=lambda instance, value: self._update_card_bg(instance, card))
        
        # Header with medication name
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40)
        )
        
        title = Label(
            text=reminder_data.get('medication_name', 'Medication'),
            font_size=dp(18),
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint_x=0.7,
            halign='left'
        )
        title.bind(size=lambda *x: setattr(title, 'text_size', title.size))
        header.add_widget(title)
        
        card.add_widget(header)
        
        # Content area with details
        content = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(100),
            spacing=[dp(10), dp(5)]
        )
        
        # Dosage
        dosage_label = Label(
            text=self.language_manager.get_text('dosage') + ":",
            font_size=dp(14),
            halign='left',
            size_hint_x=0.4
        )
        dosage_label.bind(size=lambda *x: setattr(dosage_label, 'text_size', dosage_label.size))
        content.add_widget(dosage_label)
        
        dosage_value = Label(
            text=reminder_data.get('dosage', ''),
            font_size=dp(14),
            halign='left',
            size_hint_x=0.6
        )
        dosage_value.bind(size=lambda *x: setattr(dosage_value, 'text_size', dosage_value.size))
        content.add_widget(dosage_value)
        
        card.add_widget(content)
        
        # Buttons for edit and delete
        buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        edit_btn = Button(
            text="Edit",
            size_hint_x=0.5,
            background_color=(0.3, 0.5, 0.9, 1)
        )
        edit_btn.bind(on_press=lambda x: self.edit_reminder(reminder_data.get('id', '')))
        buttons.add_widget(edit_btn)
        
        delete_btn = Button(
            text="Delete",
            size_hint_x=0.5,
            background_color=(0.9, 0.3, 0.3, 1)
        )
        delete_btn.bind(on_press=lambda x: self.delete_reminder(reminder_data.get('id', '')))
        buttons.add_widget(delete_btn)
        
        card.add_widget(buttons)
        
        return card
    
    def _update_card_bg(self, instance, card):
        \"\"\"Update card background\"\"\"
        with card.canvas.before:
            card.canvas.before.clear()
            Color(0.9, 0.9, 1, 1) if not self.theme_manager.is_dark_mode else Color(0.2, 0.2, 0.3, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
    
    def delete_reminder(self, reminder_id):
        \"\"\"Delete a reminder after confirmation\"\"\"
        print(f"Deleting reminder: {reminder_id}")
        if not self.reminder_manager:
            return
        
        # Create popup for confirmation
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        msg = Label(
            text=self.language_manager.get_text('delete_reminder_confirm'),
            size_hint_y=None,
            height=dp(50)
        )
        content.add_widget(msg)
        
        buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        no_btn = Button(
            text=self.language_manager.get_text('no'),
            size_hint_x=0.5
        )
        buttons.add_widget(no_btn)
        
        yes_btn = Button(
            text=self.language_manager.get_text('yes'),
            size_hint_x=0.5,
            background_color=(0.9, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        buttons.add_widget(yes_btn)
        
        content.add_widget(buttons)
        
        popup = Popup(
            title=self.language_manager.get_text('delete_reminder'),
            content=content,
            size_hint=(0.8, None),
            height=dp(200),
            auto_dismiss=True
        )
        
        # Bind buttons
        no_btn.bind(on_press=popup.dismiss)
        yes_btn.bind(on_press=lambda x: self.confirm_delete(reminder_id, popup))
        
        # Show popup
        popup.open()
    
    def confirm_delete(self, reminder_id, popup):
        \"\"\"Actually delete the reminder after confirmation\"\"\"
        print(f"Confirming delete for {reminder_id}")
        if not self.reminder_manager:
            popup.dismiss()
            return
        
        # Delete the reminder
        success = self.reminder_manager.delete_reminder(reminder_id)
        print(f"Delete result: {success}")
        
        # Close popup
        popup.dismiss()
        
        # Refresh the list
        if success:
            self.show_message("Reminder deleted successfully")
            Clock.schedule_once(lambda dt: self.refresh(), 0.5)
    
    def on_timer_action(self, reminder_id, action):
        \"\"\"Handle timer action (taken or skipped)\"\"\"
        print(f"Timer action: {action} for reminder {reminder_id}")
        if not self.reminder_manager:
            return
        
        try:
            if action == 'taken':
                self.reminder_manager.mark_dose_taken(reminder_id)
            elif action == 'skipped':
                self.reminder_manager.skip_dose(reminder_id)
            
            # Refresh the display after action
            Clock.schedule_once(lambda dt: self.refresh(), 0.5)
        except Exception as e:
            print(f"Error handling timer action: {e}")"""

# Insert additional methods before the next class
marker = "\n\n# Any other classes after this point"
if marker in updated_content:
    updated_content = updated_content.replace(marker, additional_methods + marker)
else:
    # Just append to the end
    updated_content += additional_methods

# Write back to the file
with open('home.py', 'w') as f:
    f.write(updated_content)

print("Added setup_dialog method and related methods to HomeScreen class") 