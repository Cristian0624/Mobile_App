with open('home.py', 'r') as f:
    lines = f.readlines()

# Remove the incorrectly indented lines
if len(lines) >= 1418:
    # Find where the ai_help_btn.bind is followed by the broken enhance_ai_button_touch function
    for i in range(1410, 1420):
        if i < len(lines) and 'ai_button_layout.add_widget(self.ai_help_btn)' in lines[i]:
            # Replace the next few lines with the correctly indented function
            fixed_lines = [
                lines[i],  # Keep the add_widget line
                "\n",
                "        # Enhance AI button touchability\n",
                "        def enhance_ai_button_touch(instance, touch):\n",
                "            if instance.collide_point(*touch.pos):\n",
                "                return True\n",
                "            return False\n",
                "        self.ai_help_btn.bind(on_touch_down=enhance_ai_button_touch)\n"
            ]
            
            # Find where to continue after removing the broken lines
            continue_idx = i + 1
            while continue_idx < len(lines) and (
                'return False' in lines[continue_idx] or 
                'return True' in lines[continue_idx] or
                'enhance_ai_button_touch' in lines[continue_idx] or
                'instance.collide_point' in lines[continue_idx]
            ):
                continue_idx += 1
            
            # Combine the lines
            lines = lines[:i+1] + fixed_lines + lines[continue_idx:]
            break

with open('home.py', 'w') as f:
    f.writelines(lines)

print("Fixed indentation in ai_help_btn block") 