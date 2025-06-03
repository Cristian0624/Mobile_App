import json
import os

class UserDatabase:
    def __init__(self):
        self.users_file = 'users.json'
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def add_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = password
        self.save_users()
        return True, "User registered successfully"

    def verify_user(self, username, password):
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username] != password:
            return False, "Incorrect password"
        
        return True, "Login successful" 