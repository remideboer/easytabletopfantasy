#!/usr/bin/env python3
"""
Convert monsters_data.json to a JavaScript file that can be embedded
"""

import json
from pathlib import Path

JSON_FILE = Path('data/monsters_data.json')
JS_FILE = Path('data/monsters_data.js')

def main():
    print(f"Reading {JSON_FILE}...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Converting to JavaScript...")
    # Convert to JavaScript variable
    js_content = 'const monstersDataEmbedded = ' + json.dumps(data, indent=2, ensure_ascii=False) + ';'
    
    print(f"Writing to {JS_FILE}...")
    with open(JS_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Done! Created {JS_FILE}")
    print(f"File size: {JS_FILE.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    main()
