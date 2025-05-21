with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. First fix the toggle_spinner method - make it more robust
toggle_spinner_index = None
for i, line in enumerate(lines):
    if "def toggle_spinner(self, instance):" in line:
        toggle_spinner_index = i
        break

if toggle_spinner_index:
    # Replace the entire toggle_spinner method with a more robust version
    new_toggle_method = [
        "    def toggle_spinner(self, instance):\n",
        "        \"\"\"Toggle the visibility of the frequency spinner dropdown\"\"\"\n",
        "        print(\"Toggle spinner called\")\n",
        "        # Only proceed if we have the required widgets\n",
        "        if not hasattr(self, 'spinner_container') or not self.spinner_container:\n",
        "            print(\"No spinner container\")\n",
        "            return False\n",
        "            \n",
        "        # Check form visibility in a simpler way\n",
        "        if not self.form_visible:\n",
        "            print(\"Form not visible\")\n",
        "            return False\n",
        "            \n",
        "        # If button is disabled, don't toggle\n",
        "        if hasattr(self, 'frequency_button') and self.frequency_button.disabled:\n",
        "            print(\"Button disabled\")\n",
        "            return False\n",
        "            \n",
        "        # Toggle the spinner visibility\n",
        "        if self.spinner_container.height == dp(0):\n",
        "            print(\"Opening spinner dropdown\")\n",
        "            self.spinner_container.height = dp(120)  # Increased height for better visibility\n",
        "            self.spinner_container.opacity = 1\n",
        "        else:\n",
        "            print(\"Closing spinner dropdown\")\n",
        "            self.spinner_container.height = dp(0)\n",
        "            self.spinner_container.opacity = 0\n",
        "        return True\n"
    ]
    
    # Find the end of the method
    end_toggle_index = toggle_spinner_index
    while end_toggle_index < len(lines) and not lines[end_toggle_index].strip() == "":
        end_toggle_index += 1
    
    # Replace the method
    lines[toggle_spinner_index:end_toggle_index] = new_toggle_method

# 2. Fix the spinner_container setup in __init__ method to ensure it's properly configured
frequency_spinner_index = None
for i, line in enumerate(lines):
    if "self.frequency_spinner = Spinner(" in line:
        frequency_spinner_index = i
        break

if frequency_spinner_index:
    # Look for where we set up the spinner container
    for i in range(frequency_spinner_index-20, frequency_spinner_index+20):
        if i < len(lines) and "self.spinner_container = BoxLayout(" in lines[i]:
            # Make sure the spinner container has a proper size and is visible by default
            container_start = i
            for j in range(i, i+10):
                if j < len(lines) and "height=dp(0)" in lines[j]:
                    lines[j] = lines[j].replace("height=dp(0)", "height=dp(120)")
                if j < len(lines) and "opacity=0" in lines[j]:
                    lines[j] = lines[j].replace("opacity=0", "opacity=1")

with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed frequency button toggle functionality") 