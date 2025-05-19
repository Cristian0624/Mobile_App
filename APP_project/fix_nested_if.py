with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix the nested if statements in show_add_reminder
lines[1554] = '        if hasattr(self, "frequency_button") and self.frequency_button and self.frequency_button.parent and hasattr(self, "spinner_container") and self.spinner_container and self.spinner_container not in self.frequency_button.parent.children:\n'
lines[1555] = '            self.frequency_button.parent.add_widget(self.spinner_container)\n'
lines[1556] = '        \n'
lines[1557] = '        if hasattr(self, "spinner_container") and self.spinner_container:\n'
lines[1558] = '            self.spinner_container.height = dp(0)\n'
lines[1559] = '            self.spinner_container.opacity = 0\n'

# Make similar changes in show_edit_reminder
for i in range(1580, 1600):
    if "if hasattr(self, \"frequency_button\")" in lines[i]:
        lines[i] = '        if hasattr(self, "frequency_button") and self.frequency_button and self.frequency_button.parent and hasattr(self, "spinner_container") and self.spinner_container and self.spinner_container not in self.frequency_button.parent.children:\n'
        lines[i+1] = '            self.frequency_button.parent.add_widget(self.spinner_container)\n'
        lines[i+2] = '        \n'
        lines[i+3] = '        if hasattr(self, "spinner_container") and self.spinner_container:\n'
        lines[i+4] = '            self.spinner_container.height = dp(0)\n'
        lines[i+5] = '            self.spinner_container.opacity = 0\n'
        break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed nested if statements in home.py") 