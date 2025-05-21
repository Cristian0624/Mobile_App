with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the RoundedButton class definition
rounded_button_index = None
for i, line in enumerate(lines):
    if "class RoundedButton(Button):" in line:
        rounded_button_index = i
        break

if rounded_button_index:
    # Find the on_touch_down method
    on_touch_down_index = None
    for i in range(rounded_button_index, rounded_button_index + 50):
        if i < len(lines) and "def on_touch_down(self, touch):" in lines[i]:
            on_touch_down_index = i
            break
    
    if on_touch_down_index:
        # Replace the on_touch_down method with an improved version
        improved_touch_method = [
            "    def on_touch_down(self, touch):\n",
            "        # Improved touch handling to make the entire button area clickable\n",
            "        if self.disabled:\n",
            "            return False\n",
            "        if self.collide_point(*touch.pos):\n",
            "            touch.grab(self)\n",
            "            self.dispatch('on_press')\n",
            "            return True\n",
            "        return False\n",
            "\n",
            "    def on_touch_up(self, touch):\n",
            "        # Handle touch release\n",
            "        if touch.grab_current is self:\n",
            "            touch.ungrab(self)\n",
            "            self.dispatch('on_release')\n",
            "            return True\n",
            "        return False\n"
        ]
        
        # Find the end of the on_touch_down method
        end_touch_index = on_touch_down_index
        while end_touch_index < len(lines) and "def " not in lines[end_touch_index + 1]:
            end_touch_index += 1
        
        # Replace the old method with the improved one
        lines[on_touch_down_index:end_touch_index + 1] = improved_touch_method

# Also improve the binding of the edit and delete buttons in ReminderCard
for i, line in enumerate(lines):
    if "self.edit_btn.bind(on_press=self._on_edit_press)" in line:
        # Change it to on_release for better user experience
        lines[i] = "        self.edit_btn.bind(on_release=self._on_edit_press)\n"
    
    if "self.delete_btn.bind(on_press=self._on_delete_press)" in line:
        # Change it to on_release for better user experience
        lines[i] = "        self.delete_btn.bind(on_release=self._on_delete_press)\n"

# Add extra padding to buttons for a larger touchable area
for i, line in enumerate(lines):
    if "self.edit_btn = RoundedButton(" in line:
        for j in range(i, i+10):
            if "height=dp(" in lines[j]:
                # Increase button height
                current_height = int(lines[j].split("height=dp(")[1].split(")")[0])
                new_height = max(current_height, 50)  # Minimum height of 50dp
                lines[j] = lines[j].replace(f"height=dp({current_height})", f"height=dp({new_height})")
    
    if "self.delete_btn = RoundedButton(" in line:
        for j in range(i, i+10):
            if "height=dp(" in lines[j]:
                # Increase button height
                current_height = int(lines[j].split("height=dp(")[1].split(")")[0])
                new_height = max(current_height, 50)  # Minimum height of 50dp
                lines[j] = lines[j].replace(f"height=dp({current_height})", f"height=dp({new_height})")

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Improved button touchability throughout the app") 