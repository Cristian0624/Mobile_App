def fix_base_screen_update_theme(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the BaseScreen.update_theme method
    base_screen_update_theme_start = None
    base_screen_update_theme_end = None
    
    for i, line in enumerate(lines):
        if "def update_theme(self, *args):" in line and i > 70 and i < 90:
            base_screen_update_theme_start = i
            break
    
    if base_screen_update_theme_start is not None:
        # Now find the end of the method
        for i in range(base_screen_update_theme_start + 1, len(lines)):
            if line.strip() and line.startswith('    def '):
                base_screen_update_theme_end = i
                break
        
        if base_screen_update_theme_end is None:
            # If we couldn't find the end, set it to a reasonable default
            base_screen_update_theme_end = base_screen_update_theme_start + 50
        
        # Now fix the indentation of all lines in this method
        for i in range(base_screen_update_theme_start + 1, base_screen_update_theme_end):
            line = lines[i]
            if line.strip() and not line.startswith('        '):
                # This line needs to be indented
                lines[i] = '        ' + line.lstrip()
                print(f"Fixed indentation of line {i+1}: {line.strip()}")
    
    # Write the fixed content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Fixed BaseScreen.update_theme method indentation in {filename}")

if __name__ == "__main__":
    fix_base_screen_update_theme() 