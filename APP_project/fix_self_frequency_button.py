with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix the attribute error by checking if parent exists
lines[1553] = '        # Make sure spinner is added back and hidden\n'
lines[1554] = '        if hasattr(self, "frequency_button") and self.frequency_button and self.frequency_button.parent and self.spinner_container not in self.frequency_button.parent.children:\n'

# Fix the same issue in the show_edit_reminder method
for i in range(1580, 1600):
    if "if self.spinner_container not in self.frequency_button.parent.children:" in lines[i]:
        lines[i] = '        if hasattr(self, "frequency_button") and self.frequency_button and self.frequency_button.parent and self.spinner_container not in self.frequency_button.parent.children:\n'
        break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed NoneType attribute error in home.py") 