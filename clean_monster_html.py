#!/usr/bin/env python3
"""
Clean up monster HTML files by removing non-stat-block elements:
- <div class="bottomad left"> (advertisements)
- <div class="breadcrumb"> (breadcrumb navigation)
- <div class="source-url"> (source URL divs we added)
- <div class="tags"> (tag divs)
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

OUTPUT_DIR = Path('foundation/monsters-bfrd')

def clean_monster_html(filepath):
    """Clean a single monster HTML file"""
    print(f"Cleaning {filepath.name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove source-url divs
    source_urls = soup.find_all('div', class_='source-url')
    for div in source_urls:
        div.decompose()
    
    # Remove breadcrumb divs
    breadcrumbs = soup.find_all('div', class_='breadcrumb')
    for div in breadcrumbs:
        div.decompose()
    
    # Remove tags divs
    tags_divs = soup.find_all('div', class_='tags')
    for div in tags_divs:
        div.decompose()
    
    # Remove bottomad (advertisement) divs
    bottomads = soup.find_all('div', class_='bottomad')
    for div in bottomads:
        div.decompose()
    
    # Also remove any divs with "bottomad" in class
    bottomads_any = soup.find_all('div', class_=re.compile('bottomad', re.I))
    for div in bottomads_any:
        div.decompose()
    
    # Remove Ezoic ad placeholders
    ezoic_ads = soup.find_all('div', id=re.compile('ezoic', re.I))
    for div in ezoic_ads:
        div.decompose()
    
    # Remove adsbygoogle ins elements
    adsbygoogle = soup.find_all('ins', class_='adsbygoogle')
    for ins in adsbygoogle:
        ins.decompose()
    
    # Remove comment blocks that mention ads
    from bs4 import Comment
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'ad' in comment.lower() or 'ezoic' in comment.lower():
            comment.extract()
    
    # Clean up empty divs that might be left behind
    empty_divs = soup.find_all('div', class_='bottomad left')
    for div in empty_divs:
        div.decompose()
    
    # Remove CSS for source-url since we removed those elements
    style_tag = soup.find('style')
    if style_tag:
        # Remove source-url CSS rules
        style_content = style_tag.string
        if style_content:
            # Remove .source-url CSS block
            style_content = re.sub(r'\.source-url\s*\{[^}]*\}', '', style_content)
            style_content = re.sub(r'\.source-url\s+[^{]*\{[^}]*\}', '', style_content)
            style_tag.string = style_content
    
    # Write cleaned content back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  Cleaned {filepath.name}")

def main():
    """Clean all monster HTML files"""
    if not OUTPUT_DIR.exists():
        print(f"Directory {OUTPUT_DIR} does not exist!")
        return
    
    html_files = list(OUTPUT_DIR.glob('monster-cr-*.html'))
    
    if not html_files:
        print(f"No HTML files found in {OUTPUT_DIR}")
        return
    
    print(f"Found {len(html_files)} HTML files to clean")
    print("=" * 60)
    
    for html_file in sorted(html_files):
        try:
            clean_monster_html(html_file)
        except Exception as e:
            print(f"  Error cleaning {html_file.name}: {e}")
    
    print("=" * 60)
    print("Cleaning complete!")

if __name__ == '__main__':
    main()
