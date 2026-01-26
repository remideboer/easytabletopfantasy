#!/usr/bin/env python3
"""Quick test to verify pagination works"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BFRD_BASE_URL = 'https://bfrd.net'
cr_tag = 'cr-0'

def get_monster_count_from_page(url):
    """Count monsters on a page"""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.status_code == 404:
            return 0, False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        monster_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/monsters/' in href and href != '/monsters/':
                full_url = urljoin(BFRD_BASE_URL, href)
                if full_url not in monster_links:
                    monster_links.append(full_url)
        
        return len(monster_links), True
    except Exception as e:
        print(f"Error: {e}")
        return 0, False

base_url = f"{BFRD_BASE_URL}/tag/{cr_tag}/"
page_num = 1
total = 0

print(f"Testing pagination for {cr_tag}...")
print()

while page_num <= 5:  # Test first 5 pages
    if page_num == 1:
        url = base_url
    else:
        url = f"{base_url}page/{page_num}/"
    
    count, exists = get_monster_count_from_page(url)
    
    if not exists:
        print(f"Page {page_num}: 404 (does not exist)")
        break
    
    total += count
    print(f"Page {page_num}: {count} monsters (total so far: {total})")
    
    if count == 0:
        print(f"  No monsters found - checking if next page exists...")
        next_url = f"{base_url}page/{page_num + 1}/"
        next_response = requests.head(next_url, timeout=10, allow_redirects=True)
        if next_response.status_code == 404:
            print(f"  Next page is 404 - done")
            break
    
    page_num += 1

print()
print(f"Total monsters found across {page_num - 1} pages: {total}")
