#!/usr/bin/env python3

import re

# Read file content
with open('home.py', 'r') as file:
    content = file.read()

# Fix 1: save_reminder method indentation
content = re.sub(r'success = False\n\s+if self\.editing_id:', 
                'success = False\n        if self.editing_id:', 
                content)

content = re.sub(r'if success:\n\s+self\.show_message\(message\)\n\s+self\.hide_dialog\(\)\n\s+# Refresh the list\n\s+Clock\.schedule_once', 
                'if success:\n            self.show_message(message)\n            self.hide_dialog()\n            # Refresh the list\n            Clock.schedule_once', 
                content)

# Fix 2: ReminderScreen.__init__ indentation
content = re.sub(r'self\.language_manager = LanguageManager\(\)\n\s+self\.reminder_manager = MedicationReminder\(\)', 
                'self.language_manager = LanguageManager()\n        self.reminder_manager = MedicationReminder()', 
                content)

# Fix 3: load_reminders method indentation
content = re.sub(r'else:\n\s+# Add each reminder to the layout\n\s+for reminder in reminders:', 
                'else:\n            # Add each reminder to the layout\n            for reminder in reminders:', 
                content)

# Fix 4: Update switch_view method to handle 'timers' instead of 'timer'
content = re.sub(r'self\.timers_btn\.bind\(on_release=lambda x: self\.switch_view\(\'timer\'\)\)', 
                'self.timers_btn.bind(on_release=lambda x: self.switch_view(\'timers\'))', 
                content)

# Write changes back to file
with open('home.py', 'w') as file:
    file.write(content)

print("Fixed indentation issues in home.py") 