#!/usr/bin/env python3
"""
Scrape Black Flag Reference Document (BFRD) monster stat blocks.
Visits each CR tag page, handles pagination, and saves complete stat blocks to HTML files.
"""

import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re

# Configuration
BFRD_BASE_URL = 'https://bfrd.net'
OUTPUT_DIR = Path('foundation/monsters-bfrd')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CR tags to process (0, 1/8, 1/4, 1/2, 1-30)
CR_TAGS = [
    'cr-0',
    'cr-1-8',
    'cr-1-4',
    'cr-1-2',
    'cr-1', 'cr-2', 'cr-3', 'cr-4', 'cr-5', 'cr-6', 'cr-7', 'cr-8', 'cr-9', 'cr-10',
    'cr-11', 'cr-12', 'cr-13', 'cr-14', 'cr-15', 'cr-16', 'cr-17', 'cr-18', 'cr-19', 'cr-20',
    'cr-21', 'cr-22', 'cr-23', 'cr-24', 'cr-25', 'cr-26', 'cr-27', 'cr-28', 'cr-29', 'cr-30'
]

def get_monster_links_from_page(url):
    """Get all monster page links from a CR tag page"""
    monster_links = []
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.status_code == 404:
            # Page doesn't exist, return empty list
            return monster_links
        if response.status_code not in [200, 301, 302]:
            print(f"  Warning: HTTP {response.status_code} for {url}")
            # Continue anyway, might still have content
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links to monster pages
        # Monster links typically have '/monsters/' in the path
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/monsters/' in href and href != '/monsters/':
                full_url = urljoin(BFRD_BASE_URL, href)
                if full_url not in monster_links:
                    monster_links.append(full_url)
        
        time.sleep(0.5)  # Be polite to the server
        
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
    
    return monster_links

def get_all_monster_links_for_cr(cr_tag):
    """Get all monster links for a CR tag, handling pagination"""
    print(f"  Fetching monster links for {cr_tag}...")
    
    all_monster_links = []
    base_url = f"{BFRD_BASE_URL}/tag/{cr_tag}/"
    page_num = 1
    
    while True:
        # Construct URL: base for page 1, /page/N for subsequent pages
        if page_num == 1:
            current_url = base_url
        else:
            current_url = f"{base_url}page/{page_num}/"
        
        print(f"    Page {page_num}: {current_url}")
        
        # Check if page exists first (faster than fetching full content)
        try:
            test_response = requests.head(current_url, timeout=10, allow_redirects=True)
            if test_response.status_code == 404:
                print(f"    Page {page_num} not found (404) - done with {cr_tag}")
                break
        except Exception as e:
            print(f"    Error checking page: {e}")
            # Continue to try fetching anyway
        
        # Get monster links from this page
        monster_links = get_monster_links_from_page(current_url)
        
        # Add new links (avoid duplicates)
        for link in monster_links:
            if link not in all_monster_links:
                all_monster_links.append(link)
        
        print(f"    Found {len(monster_links)} monsters on this page (total: {len(all_monster_links)})")
        
        # Move to next page
        page_num += 1
        
        # Safety limit to prevent infinite loops
        if page_num > 100:
            print(f"    Reached safety limit of 100 pages - stopping")
            break
    
    return all_monster_links

def extract_monster_stat_block(url):
    """Extract the complete monster stat block from a monster page"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"      Error: HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content area - typically in <article> or <main> or specific content div
        stat_block = None
        
        # Try different selectors
        article = soup.find('article')
        if article:
            stat_block = article
        else:
            main = soup.find('main')
            if main:
                stat_block = main
            else:
                # Look for content div
                content_div = soup.find('div', class_=re.compile('content|post|entry', re.I))
                if content_div:
                    stat_block = content_div
        
        if not stat_block:
            # Fallback: get body content
            stat_block = soup.find('body')
        
        if stat_block:
            # Return the HTML of the stat block
            return str(stat_block)
        
        return None
        
    except Exception as e:
        print(f"      Error fetching {url}: {e}")
        return None

def create_html_file(cr_tag, monster_stat_blocks):
    """Create an HTML file with all monster stat blocks for a CR level"""
    filename = f"monster-{cr_tag}.html"
    filepath = OUTPUT_DIR / filename
    
    # Create HTML structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BFRD Monsters - {cr_tag.upper()}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .monster-stat-block {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .monster-stat-block h1 {{
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 10px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 15px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 8px;
            text-align: center;
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        .source-url {{
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }}
        .source-url a {{
            color: #4a90e2;
            text-decoration: none;
        }}
        .source-url a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Black Flag Reference Document - Monsters ({cr_tag.upper()})</h1>
    <p>This file contains all monster stat blocks scraped from BFRD for Challenge Rating {cr_tag.replace('cr-', '').replace('-', '/')}.</p>
    <p>Total monsters: {len(monster_stat_blocks)}</p>
    <hr>
"""
    
    # Add each monster stat block
    for i, (url, stat_block_html) in enumerate(monster_stat_blocks, 1):
        html_content += f"""
    <div class="monster-stat-block">
        <div class="source-url">Monster {i} - Source: <a href="{url}" target="_blank">{url}</a></div>
        {stat_block_html}
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  Saved {len(monster_stat_blocks)} monsters to {filepath}")

def process_cr_tag(cr_tag):
    """Process a single CR tag: get all monsters and save to HTML"""
    print(f"\n{'='*60}")
    print(f"Processing {cr_tag.upper()}")
    print(f"{'='*60}")
    
    # Get all monster links for this CR
    monster_links = get_all_monster_links_for_cr(cr_tag)
    
    if not monster_links:
        print(f"  No monsters found for {cr_tag}")
        return
    
    print(f"  Found {len(monster_links)} total monster pages")
    
    # Extract stat blocks
    monster_stat_blocks = []
    for i, monster_url in enumerate(monster_links, 1):
        print(f"  [{i}/{len(monster_links)}] Extracting {monster_url}...")
        stat_block = extract_monster_stat_block(monster_url)
        if stat_block:
            monster_stat_blocks.append((monster_url, stat_block))
        time.sleep(0.3)  # Be polite
    
    # Save to HTML file
    if monster_stat_blocks:
        create_html_file(cr_tag, monster_stat_blocks)
    else:
        print(f"  No stat blocks extracted for {cr_tag}")

def main():
    """Main function"""
    import sys
    
    # Check for command line argument to start from a specific CR
    start_from = None
    if len(sys.argv) > 1:
        start_from = sys.argv[1]
        print(f"Starting from CR tag: {start_from}")
    
    print("BFRD Monster Scraper")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    print(f"CR tags to process: {len(CR_TAGS)}")
    print()
    
    # Skip CR tags before start_from if specified
    start_processing = False
    if start_from:
        start_processing = False
    
    for cr_tag in CR_TAGS:
        # Skip until we reach the start_from tag
        if start_from and not start_processing:
            if cr_tag == start_from:
                start_processing = True
            else:
                print(f"Skipping {cr_tag}...")
                continue
        try:
            process_cr_tag(cr_tag)
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\nError processing {cr_tag}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("Scraping complete!")
    print(f"Files saved to: {OUTPUT_DIR.absolute()}")

if __name__ == '__main__':
    main()
