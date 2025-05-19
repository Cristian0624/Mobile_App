import json
import os
import uuid
from datetime import datetime, timedelta

class MedicationReminder:
    """Class to manage medication reminders"""
    
    def __init__(self):
        self.reminders_file = "medication_reminders.json"
        self.reminders = self.load_reminders()
    
    def load_reminders(self):
        """Load reminders from file or return empty dict if file doesn't exist"""
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, 'r') as f:
                    reminders = json.load(f)
                    
                    # Convert string ISO dates back to datetime objects
                    for reminder_id, reminder in reminders.items():
                        # Convert next_time
                        if reminder.get('next_time'):
                            try:
                                reminder['next_time'] = datetime.fromisoformat(reminder['next_time'])
                            except (ValueError, TypeError):
                                reminder['next_time'] = None
                        
                        # Convert last_taken
                        if reminder.get('last_taken'):
                            try:
                                reminder['last_taken'] = datetime.fromisoformat(reminder['last_taken'])
                            except (ValueError, TypeError):
                                reminder['last_taken'] = None
                    
                    return reminders
            except Exception as e:
                print(f"Error loading reminders: {e}")
                return {}
        return {}
    
    def save_reminders(self):
        """Save reminders to file"""
        try:
            # Create a copy of reminders for serialization
            reminders_copy = {}
            
            for reminder_id, reminder in self.reminders.items():
                reminder_copy = dict(reminder)
                
                # Convert datetime objects to ISO format strings for JSON serialization
                if isinstance(reminder_copy.get('next_time'), datetime):
                    reminder_copy['next_time'] = reminder_copy['next_time'].isoformat()
                
                if isinstance(reminder_copy.get('last_taken'), datetime):
                    reminder_copy['last_taken'] = reminder_copy['last_taken'].isoformat()
                
                reminders_copy[reminder_id] = reminder_copy
            
            with open(self.reminders_file, 'w') as f:
                json.dump(reminders_copy, f)
            return True
        except Exception as e:
            print(f"Error saving reminders: {e}")
            return False
    
    def add_reminder(self, medication_name, dosage, frequency, duration=0, notes="", doses_taken=0):
        """Add a new medication reminder"""
        reminder_id = str(uuid.uuid4())
        now = datetime.now()
        
        self.reminders[reminder_id] = {
            "id": reminder_id,
            "medication_name": medication_name,
            "dosage": dosage,
            "frequency": frequency,
            "duration": duration,
            "notes": notes,
            "created_at": now.isoformat(),
            "last_taken": None,
            "next_time": None,
            "is_active": True,
            "doses_taken": doses_taken
        }
        
        self.save_reminders()
        return reminder_id
    
    def update_reminder(self, reminder_id, **kwargs):
        """Update an existing reminder with any provided fields"""
        if reminder_id not in self.reminders:
            return False
        
        # Update only the fields that are provided
        for key, value in kwargs.items():
            if key in self.reminders[reminder_id]:
                self.reminders[reminder_id][key] = value
        
        self.save_reminders()
        return True
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder by ID"""
        if reminder_id in self.reminders:
            del self.reminders[reminder_id]
            self.save_reminders()
            return True
        return False
    
    def get_reminder(self, reminder_id):
        """Get a single reminder by ID"""
        return self.reminders.get(reminder_id)
    
    def get_active_reminders(self):
        """Get all active reminders"""
        # Convert to list and sort by most recently created first
        active_reminders = [r for r in self.reminders.values() if r.get('is_active', True)]
        active_reminders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return active_reminders