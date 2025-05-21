with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the safe_toggle_spinner definition and binding
safe_toggle_index = None
for i, line in enumerate(lines):
    if "def safe_toggle_spinner(instance):" in line:
        safe_toggle_index = i
        break

if safe_toggle_index:
    # Find where we bind to the frequency button
    for i in range(safe_toggle_index, safe_toggle_index + 15):
        if i < len(lines) and "self.frequency_button.bind(on_release=safe_toggle_spinner)" in lines[i]:
            # Change to direct binding to improve response
            lines[i] = "        self.frequency_button.bind(on_release=self.toggle_spinner)\n"
            break

# Also fix the show_add_reminder and show_edit_reminder methods to always ensure the spinner container is properly positioned
for i, line in enumerate(lines):
    if "def show_add_reminder(self, instance):" in line:
        show_add_index = i
        for j in range(show_add_index, show_add_index + 50):
            if "self.spinner_container.opacity = 0" in lines[j]:
                # Add a line to ensure the spinner is properly initialized and visible when needed
                lines.insert(j+1, "        # Ensure spinner container is properly configured for dropdown\n")
                lines.insert(j+2, "        self.spinner_container.size_hint = (1, None)\n")
                break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed frequency button binding for better responsiveness") 