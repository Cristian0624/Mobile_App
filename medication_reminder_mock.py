#!/usr/bin/env python3
import json
import os
import uuid
from datetime import datetime, timedelta

class MockMedicationReminder:
    """
    Mock implementation of the MedicationReminder class for testing purposes.
    """
    def __init__(self):
        self.reminders = {}
        self.reminders_file = "reminders_mock.json"
        self.load_reminders()
    
    def load_reminders(self):
        """Load reminders from file"""
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, 'r') as f:
                    self.reminders = json.load(f)
            except:
                self.reminders = {}
        else:
            self.reminders = {}
    
    def save_reminders(self):
        """Save reminders to file"""
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f)
    
    def add_reminder(self, medication_name, dosage, frequency, duration, notes=""):
        """Add a new reminder"""
        reminder_id = str(uuid.uuid4())
        start_date = datetime.now().strftime("%Y-%m-%d")
        
        self.reminders[reminder_id] = {
            "id": reminder_id,
            "medication_name": medication_name,
            "dosage": dosage,
            "frequency": frequency,
            "duration": duration,
            "notes": notes,
            "start_date": start_date,
            "last_taken": None,
            "next_time": None,
            "is_active": True,
            "created_at": datetime.now().isoformat()
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
        """Delete a reminder"""
        if reminder_id in self.reminders:
            del self.reminders[reminder_id]
            self.save_reminders()
            return True
        
        return False
    
    def get_reminder(self, reminder_id):
        """Get a specific reminder"""
        return self.reminders.get(reminder_id)
    
    def get_all_reminders(self):
        """Get all reminders"""
        return self.reminders
    
    def get_active_reminders(self):
        """Get all active reminders"""
        # Convert to list and sort by most recently created first
        active_reminders = [r for r in self.reminders.values() if r.get('is_active', True)]
        active_reminders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return active_reminders
    
    def mark_taken(self, reminder_id):
        """Mark a medication as taken"""
        if reminder_id in self.reminders:
            now = datetime.now()
            self.reminders[reminder_id]["last_taken"] = now.isoformat()
            
            # Calculate next dose time based on frequency
            frequency = self.reminders[reminder_id]["frequency"]
            hours_to_add = 8  # default to 8 hours
            
            if "daily" in frequency.lower():
                if "once" in frequency.lower():
                    hours_to_add = 24
                elif "twice" in frequency.lower():
                    hours_to_add = 12
                elif "three" in frequency.lower():
                    hours_to_add = 8
                elif "four" in frequency.lower():
                    hours_to_add = 6
            elif "every" in frequency.lower():
                # Parse hours from strings like "Every 6 hours"
                parts = frequency.lower().split()
                for i, part in enumerate(parts):
                    if part.isdigit() and i+1 < len(parts) and "hour" in parts[i+1]:
                        hours_to_add = int(part)
                        break
            
            next_time = now + timedelta(hours=hours_to_add)
            self.reminders[reminder_id]["next_time"] = next_time.isoformat()
            
            self.save_reminders()
            return True
        
        return False 