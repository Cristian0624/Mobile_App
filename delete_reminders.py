from medication_reminder import MedicationReminder

# Create a reminder manager instance
reminder_manager = MedicationReminder()

# Get all active reminders
reminders = reminder_manager.get_active_reminders()
print(f"Found {len(reminders)} reminders")

# Delete each reminder
for reminder in reminders:
    reminder_id = reminder.get('id', '')
    if reminder_id:
        print(f'Deleting reminder: {reminder.get("medication_name", "Unknown")}')
        reminder_manager.delete_reminder(reminder_id)

print('All reminders deleted successfully') 