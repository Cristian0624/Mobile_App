with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Restore the form visibility in show_add_reminder method
# Look for where we set spinner_container opacity after safety checks
for i in range(1559, 1565):
    if "self.spinner_container.opacity = 0" in lines[i]:
        # Add the missing line after spinner settings
        lines.insert(i+1, '        # Show form, hide reminders\n')
        lines.insert(i+2, '        self.form_container.opacity = 1\n')
        break

# Ensure the same in show_edit_reminder method
for i in range(1585, 1595):
    if "self.spinner_container.opacity = 0" in lines[i]:
        # Check if the next line has form_container.opacity
        if "self.form_container.opacity = 1" not in lines[i+1]:
            lines.insert(i+1, '        # Show form, hide reminders\n')
            lines.insert(i+2, '        self.form_container.opacity = 1\n')
        break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Restored form visibility in home.py") 