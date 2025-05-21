with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix access to spinner_container properties
lines[1556] = '        if hasattr(self, "spinner_container") and self.spinner_container:\n'
lines[1557] = '            self.spinner_container.height = dp(0)\n'
lines[1558] = '            self.spinner_container.opacity = 0\n'

# Apply the same fix to the show_edit_reminder method
for i in range(1585, 1600):
    if "self.spinner_container.height = dp(0)" in lines[i]:
        lines[i-1] = '        if hasattr(self, "spinner_container") and self.spinner_container:\n'
        lines[i] = '            self.spinner_container.height = dp(0)\n'
        lines[i+1] = '            self.spinner_container.opacity = 0\n'
        break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Added safety checks for spinner_container attribute access in home.py") 