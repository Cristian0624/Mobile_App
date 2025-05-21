with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and improve the AI button touchability
ai_button_index = None
for i, line in enumerate(lines):
    if "self.ai_help_btn = Button(" in line:
        ai_button_index = i
        
        # Look up a bit to find the container height
        for j in range(i-10, i):
            if "height=dp(" in lines[j]:
                # Increase container height
                container_height = int(lines[j].split("height=dp(")[1].split(")")[0])
                new_container_height = max(container_height, 55)  # Increase to at least 55dp
                lines[j] = lines[j].replace(f"height=dp({container_height})", f"height=dp({new_container_height})")
                break
                
        # Add padding to the button
        for j in range(i, i+15):
            if j < len(lines) and "add_widget(self.ai_help_btn)" in lines[j]:
                # Add a custom on_touch_down method to the button after adding it
                new_content = [
                    "\n",
                    "        # Enhance AI button touchability\n",
                    "        def enhance_ai_button_touch(instance, touch):\n",
                    "            if instance.collide_point(*touch.pos):\n",
                    "                return True\n",
                    "            return False\n",
                    "        self.ai_help_btn.bind(on_touch_down=enhance_ai_button_touch)\n"
                ]
                
                for line in new_content:
                    lines.insert(j+1, line)
                break
        break

# Add debug logging to show touch events
screen_init_index = None
for i, line in enumerate(lines):
    if "class ReminderScreen(BaseScreen):" in line:
        screen_init_index = i
        break

if screen_init_index:
    # Find on_touch_down method in ReminderScreen
    for i in range(screen_init_index, screen_init_index + 100):
        if i < len(lines) and "def on_touch_down(self, touch):" in lines[i]:
            touch_method_index = i
            method_end = touch_method_index
            
            # Find end of method
            while method_end < len(lines) and not lines[method_end].strip() == "":
                method_end += 1
            
            # Replace with improved touch debugging method
            improved_method = [
                "    def on_touch_down(self, touch):\n",
                "        \"\"\"Intercept all touch events to prevent frequency button interaction when form is not visible\"\"\"\n",
                "        # Add debug for touch events\n",
                "        print(f\"Touch at {touch.pos}, form visible: {self.form_visible}\")\n",
                "        \n",
                "        # First check if we have a frequency button and need to block its interaction\n",
                "        if hasattr(self, 'frequency_button') and not self.form_visible:\n",
                "            # Check if touch is within the frequency button\n",
                "            if self.frequency_button.collide_point(*touch.pos):\n",
                "                print(\"Blocking touch on frequency button - form not visible\")\n",
                "                return True  # Block the touch event\n",
                "        \n",
                "        # Check all rounded buttons to ensure they receive touch events\n",
                "        if hasattr(self, 'form_container') and self.form_visible:\n",
                "            for child in self.form_container.walk(restrict=True):\n",
                "                if isinstance(child, Button) and child.collide_point(*touch.pos):\n",
                "                    print(f\"Touch detected on button: {child}\")\n",
                "                    child.dispatch('on_press')\n",
                "                    return True\n",
                "        \n",
                "        # Let the normal touch handling continue otherwise\n",
                "        return super(ReminderScreen, self).on_touch_down(touch)\n"
            ]
            
            lines[touch_method_index:method_end+1] = improved_method
            break

# Also find and improve save/cancel buttons if needed
for i, line in enumerate(lines):
    if "self.cancel_btn = Button(" in line or "self.save_btn = Button(" in line:
        # For standard buttons with RoundedRectangle in canvas, add increased padding
        for j in range(i, i+20):
            if j < len(lines) and "height=dp(" in lines[j]:
                current_height = int(lines[j].split("height=dp(")[1].split(")")[0])
                new_height = max(current_height, 50)  # Minimum height of 50dp
                lines[j] = lines[j].replace(f"height=dp({current_height})", f"height=dp({new_height})")
                break

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Improved standard button touchability") 