def fix_docstring_indentation(filename='home.py'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix docstring indentation
    # Pattern 1: docstring without indentation immediately after method definition
    content = content.replace(
        'def update_theme(self, *args):\n"""',
        'def update_theme(self, *args):\n        """'
    )
    
    # Pattern 2: docstring with improper indentation after method definition
    content = content.replace(
        'def update_theme(self, *args):\n    """',
        'def update_theme(self, *args):\n        """'
    )
    
    # Fix specific issue with docstrings in CameraScreen's update_theme
    content = content.replace(
        'def update_theme(self, *args):\n        """Update',
        'def update_theme(self, *args):\n        """Update'
    )
    
    # Fix specific issue with docstrings in VoiceScreen's update_theme
    content = content.replace(
        'def update_theme(self, *args):\n        """Override',
        'def update_theme(self, *args):\n        """Override'
    )
    
    # Fix missing line breaks
    content = content.replace(
        'def update_theme(self, *args):"""',
        'def update_theme(self, *args):\n        """'
    )
    
    # For any occurrences where a docstring is on the same line as the def statement
    import re
    content = re.sub(
        r'def update_theme\(self, \*args\):\s*"""(.+?)"""',
        r'def update_theme(self, *args):\n        """\1"""',
        content
    )
    
    # Write the fixed content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed docstring indentation in {filename}")

if __name__ == "__main__":
    fix_docstring_indentation() 