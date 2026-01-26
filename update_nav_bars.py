#!/usr/bin/env python3
"""
Update navigation bars in all HTML files to include monsters.html link
"""

import re
from pathlib import Path

# Files to update (excluding monsters.html itself)
HTML_FILES = [
    'rules/index.html',
    'rules/core.html',
    'rules/characters.html',
    'rules/lineages.html',
    'rules/backgrounds.html',
    'rules/talents.html',
    'rules/conversion.html',
    'rules/combat.html',
    'rules/magic.html',
    'rules/gear.html',
    'rules/monster-abilities.html',
    'convert.html',
    'faq.html',
    'legal.html'
]

def update_nav_bar(filepath):
    """Update nav bar to include monsters.html link"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find the nav bar section with gear.html
    # We want to add monsters.html after gear.html
    pattern = r'(<a href="[^"]*gear\.html"[^>]*>Gear</a>)(\s*<a href="[^"]*faq\.html")'
    
    # Check if monsters link already exists
    if 'monsters.html' in content and 'Monsters</a>' in content:
        print(f"  {filepath.name}: Already has monsters link")
        return False
    
    # Try to add after gear.html
    replacement = r'\1<a href="monsters.html">Monsters</a>\2'
    new_content = re.sub(pattern, replacement, content)
    
    # If pattern didn't match, try alternative pattern (for files in different directories)
    if new_content == content:
        # Try with ../ prefix for root level files
        pattern2 = r'(<a href="[^"]*gear\.html"[^>]*>Gear</a>)(\s*<a href="[^"]*faq\.html")'
        replacement2 = r'\1<a href="rules/monsters.html">Monsters</a>\2'
        new_content = re.sub(pattern2, replacement2, content)
    
    # If still no match, try to find gear.html and add after it
    if new_content == content:
        # More flexible pattern
        pattern3 = r'(<a href="[^"]*gear\.html"[^>]*>Gear</a>)'
        replacement3 = r'\1<a href="monsters.html">Monsters</a>'
        new_content = re.sub(pattern3, replacement3, content)
        
        # Try with rules/ prefix
        if new_content == content:
            pattern4 = r'(<a href="[^"]*gear\.html"[^>]*>Gear</a>)'
            replacement4 = r'\1<a href="rules/monsters.html">Monsters</a>'
            new_content = re.sub(pattern4, replacement4, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  {filepath.name}: Updated")
        return True
    else:
        print(f"  {filepath.name}: Could not find insertion point")
        return False

def main():
    """Update all HTML files"""
    print("Updating navigation bars...")
    print("=" * 60)
    
    updated_count = 0
    
    for html_file in HTML_FILES:
        filepath = Path(html_file)
        if filepath.exists():
            if update_nav_bar(filepath):
                updated_count += 1
        else:
            print(f"  {html_file}: File not found")
    
    print("=" * 60)
    print(f"Updated {updated_count} files")

if __name__ == '__main__':
    main()
