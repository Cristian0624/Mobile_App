def fix_home_indentation(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check line 82 and fix its indentation
    if len(lines) >= 82:
        # Ensure line 82 has proper indentation
        line_82 = lines[81]  # 0-based index
        if not line_82.startswith('        '):
            # This line is part of a method body, so it should have 8 spaces of indentation
            lines[81] = '        ' + line_82.lstrip()
            print(f"Fixed indentation of line 82: {line_82.strip()}")
    
    # Fix indentation of other problematic lines
    for i in range(len(lines)):
        line = lines[i]
        if "def update_theme(self, *args):" in line and not line.startswith('    '):
            # Fix method definition indentation
            lines[i] = '    ' + line.lstrip()
            print(f"Fixed method definition at line {i+1}: {line.strip()}")
        
        if '"""""' in line:
            # Fix incorrectly formatted docstrings
            lines[i] = line.replace('""""', '"""')
            print(f"Fixed docstring at line {i+1}")
        
        if 'super(' in line and '.update_theme(' in line:
            # Ensure super calls have proper indentation
            if not line.startswith('        '):
                lines[i] = '        ' + line.lstrip()
                print(f"Fixed super call at line {i+1}: {line.strip()}")
    
    # Write the fixed content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Completed indentation fixes in {filename}")

if __name__ == "__main__":
    fix_home_indentation() 