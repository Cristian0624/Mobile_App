with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix the indentation issue
lines[1553] = '        # Make sure spinner is added back and hidden\n'
lines[1554] = '        if hasattr(self, "frequency_button") and self.frequency_button and self.frequency_button.parent and self.spinner_container not in self.frequency_button.parent.children:\n'
lines[1555] = '            self.frequency_button.parent.add_widget(self.spinner_container)\n'
lines[1556] = '        self.spinner_container.height = dp(0)\n'
lines[1557] = '        self.spinner_container.opacity = 0\n'

# Apply the same fix to the show_edit_reminder method
for i in range(1580, 1600):
    if "if self.spinner_container not in self.frequency_button.parent.children:" in lines[i]:
        lines[i] = '        if hasattr(self, "frequency_button") and self.frequency_button and self.frequency_button.parent and self.spinner_container not in self.frequency_button.parent.children:\n'
        lines[i+1] = '            self.frequency_button.parent.add_widget(self.spinner_container)\n'
        break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed indentation after if statement in home.py") 