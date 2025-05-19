with open('home.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the problematic line
for i, line in enumerate(lines):
    if '"""Update UI elements based on current theme"""' in line and i > 2440 and i < 2460:
        # Fix the indentation
        if not line.startswith('        '):
            print(f"Fixing line {i+1}: {line.strip()}")
            lines[i] = '        """Update UI elements based on current theme"""\n'

# Write back to the file
with open('home.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed indentation issue in home.py") 