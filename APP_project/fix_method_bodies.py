def fix_method_bodies(filename='home.py'):
    """Fix indentation in all method bodies in the file"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_method = False
    method_indent = 0
    class_indent = 0
    
    for i in range(len(lines)):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
        
        # Detect class definitions
        if stripped.startswith('class '):
            in_method = False
            class_indent = len(line) - len(line.lstrip())
            continue
        
        # Detect method definitions with parameters
        if 'def ' in stripped and '(' in stripped and ')' in stripped and ':' in stripped:
            leading_spaces = len(line) - len(line.lstrip())
            # Check if this is a method in a class
            if leading_spaces > class_indent:
                in_method = True
                method_indent = leading_spaces
                # Ensure method has proper indentation (usually 4 spaces in a class)
                if method_indent != class_indent + 4:
                    lines[i] = ' ' * (class_indent + 4) + line.lstrip()
                    print(f"Fixed method definition at line {i+1}: {stripped}")
            else:
                in_method = False
            continue
        
        # Fix indentation within method bodies
        if in_method:
            leading_spaces = len(line) - len(line.lstrip())
            # Method body should be indented more than the method def
            if stripped and leading_spaces <= method_indent:
                # Add proper indentation
                lines[i] = ' ' * (method_indent + 4) + line.lstrip()
                print(f"Fixed method body line {i+1}: {stripped}")
    
    # Write the fixed lines back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Fixed method body indentation in {filename}")

if __name__ == "__main__":
    fix_method_bodies() 