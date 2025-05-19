with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the show_add_reminder method
show_add_index = None
for i, line in enumerate(lines):
    if "def show_add_reminder(self, instance):" in line:
        show_add_index = i
        break

if show_add_index:
    # Add a check to recreate the frequency button if it's missing
    for j in range(show_add_index, show_add_index + 50):
        if j < len(lines) and "self.frequency_button.disabled = False" in lines[j]:
            # Add logic to re-create the frequency button if it was removed
            new_content = [
                "        # Re-add the frequency button if it was removed\n",
                "        if hasattr(self, 'frequency_button_parent') and not hasattr(self.frequency_button, 'parent'):\n",
                "            print(\"Re-adding frequency button to parent\")\n",
                "            frequency_layout = None\n",
                "            for child in self.form_container.children:\n",
                "                if hasattr(child, 'children'):\n",
                "                    for grid_child in child.children:\n",
                "                        if hasattr(grid_child, 'children') and len(grid_child.children) > 0:\n",
                "                            for potential_freq in grid_child.children:\n",
                "                                if hasattr(potential_freq, 'children') and len(potential_freq.children) > 0:\n",
                "                                    if any('frequency' in str(c) for c in potential_freq.children):\n",
                "                                        frequency_layout = potential_freq\n",
                "                                        break\n",
                "            if frequency_layout:\n",
                "                # Add button back to layout\n",
                "                if self.frequency_button not in frequency_layout.children:\n",
                "                    frequency_layout.add_widget(self.frequency_button, 1)  # Insert at position 1 (between label and spinner)\n",
                "                    # Rebind button\n",
                "                    self.frequency_button.bind(on_release=self.toggle_spinner)\n",
                "        \n"
            ]
            for line in reversed(new_content):
                lines.insert(j+1, line)
            break

# Fix the hide_form method to not completely remove the button
hide_form_index = None
for i, line in enumerate(lines):
    if "def hide_form(self, instance=None):" in line:
        hide_form_index = i
        break

if hide_form_index:
    # Find the part where it's removing the frequency button
    for j in range(hide_form_index, hide_form_index + 50):
        if j < len(lines) and "self.frequency_button.parent.remove_widget(self.frequency_button)" in lines[j]:
            # Comment out the removal line to prevent the button from being removed
            lines[j] = "            # Don't remove the button completely - self.frequency_button.parent.remove_widget(self.frequency_button)\n"
            break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed frequency button reappearance issue") 