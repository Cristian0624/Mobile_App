import re

with open('home.py', 'r') as file:
    content = file.read()

# Fix 1: save_reminder method around line 716
content = re.sub(r'success = False\n\s+if self\.editing_id:', 'success = False\n        if self.editing_id:', content)
content = re.sub(r'if success:\n\s+self\.show_message\(message\)\n\s+self\.hide_dialog\(\)\n\s+# Refresh the list\n\s+Clock\.schedule_once', 'if success:\n            self.show_message(message)\n            self.hide_dialog()\n            # Refresh the list\n            Clock.schedule_once', content)

# Fix 2: ReminderScreen __init__ around line 1011
content = re.sub(r'self\.language_manager = LanguageManager\(\)\n\s+self\.reminder_manager = MedicationReminder\(\)', 'self.language_manager = LanguageManager()\n        self.reminder_manager = MedicationReminder()', content)

# Fix 3: load_reminders method around line 1320
content = re.sub(r'else:\n\s+# Add each reminder to the layout\n\s+for reminder in reminders:', 'else:\n            # Add each reminder to the layout\n            for reminder in reminders:', content)

with open('home.py', 'w') as file:
    file.write(content)

print("Fixed indentation issues in home.py") 