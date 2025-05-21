def fix_missing_line_breaks(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix line 76: missing line break between _update_rect and update_theme
    content = content.replace('self.bg_rect.size = instance.size    def update_theme', 
                              'self.bg_rect.size = instance.size\n\n    def update_theme')
    
    # Fix line 2698: missing line break between update_theme() and def update_theme
    content = content.replace('self.update_theme()    def update_theme', 
                              'self.update_theme()\n\n    def update_theme')
    
    # Write the fixed content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed missing line breaks in {filename}")

if __name__ == "__main__":
    fix_missing_line_breaks() 