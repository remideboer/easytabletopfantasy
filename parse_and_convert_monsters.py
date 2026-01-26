#!/usr/bin/env python3
"""
Parse monster HTML files and convert them to ETF format.
Extracts stat blocks and converts them to JSON for use in monsters.html
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

MONSTERS_DIR = Path('foundation/monsters-bfrd')
OUTPUT_FILE = Path('foundation/monsters_data.json')

def parse_cr_value(cr_text: str) -> float:
    """Parse CR value from text like 'CR 0', 'CR 1/8', 'CR 1/4', 'CR 1/2', 'CR 5'"""
    if not cr_text:
        return 0.0
    
    # Remove 'CR' prefix
    cr_text = re.sub(r'^CR\s*', '', cr_text.strip(), flags=re.IGNORECASE)
    
    # Handle fractions
    if '/' in cr_text:
        parts = cr_text.split('/')
        if len(parts) == 2:
            try:
                num = float(parts[0].strip())
                den = float(parts[1].strip())
                return num / den
            except:
                return 0.0
    
    # Handle decimal or integer
    try:
        return float(cr_text.strip())
    except:
        return 0.0

def convert_to_hit_to_defense_save_dc(text: str) -> str:
    """Convert attack rolls to Defense Save DC: +X to hit -> Defense Save DC (11+X)"""
    def replace_attack(match):
        to_hit_str = match.group(1)
        try:
            to_hit = int(to_hit_str)
            dc = 11 + to_hit
            return f"Defense Save DC {dc}"
        except:
            return match.group(0)
    
    # Pattern: "Melee Weapon Attack: +X to hit" or "+X to hit"
    text = re.sub(r'Melee Weapon Attack:\s*\+(\d+)\s+to hit', replace_attack, text)
    text = re.sub(r'Ranged Weapon Attack:\s*\+(\d+)\s+to hit', replace_attack, text)
    text = re.sub(r'\+(\d+)\s+to hit', replace_attack, text)
    
    return text

def convert_hp(hp_text: str) -> int:
    """Convert HP: HP/10, round up (e.g., 85 -> 9, 9 -> 1)"""
    # Extract number from text like "Hit Points 85" or "85"
    match = re.search(r'(\d+)', hp_text)
    if match:
        hp = int(match.group(1))
        # Round up: divide by 10, round up
        converted = (hp + 9) // 10  # This rounds up
        return max(1, converted)  # Minimum 1
    return 1

def modifier_to_score(modifier: int) -> int:
    """Convert modifier to ability score: score = modifier * 2 + 10"""
    return modifier * 2 + 10

def score_to_modifier(score: int) -> int:
    """Convert ability score to modifier: modifier = floor((score - 10) / 2)"""
    return (score - 10) // 2

def convert_ability_scores_table(html: str) -> str:
    """Convert D&D ability scores table to ETF 3-column table"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all ability score tables
    tables = soup.find_all('figure', class_='monster-ability-scores')
    
    for table_figure in tables:
        table = table_figure.find('table')
        if not table:
            continue
        
        thead = table.find('thead')
        tbody = table.find('tbody')
        
        if not thead or not tbody:
            continue
        
        # Get header row
        header_row = thead.find('tr')
        if not header_row:
            continue
        
        # Get data row
        data_row = tbody.find('tr')
        if not data_row:
            continue
        
        # Extract modifiers from original table
        headers = [th.get_text().strip() for th in header_row.find_all('th')]
        cells = [td.get_text().strip() for td in data_row.find_all('td')]
        
        # Find indices for each ability
        str_idx = next((i for i, h in enumerate(headers) if h.upper() == 'STR'), None)
        dex_idx = next((i for i, h in enumerate(headers) if h.upper() == 'DEX'), None)
        con_idx = next((i for i, h in enumerate(headers) if h.upper() == 'CON'), None)
        int_idx = next((i for i, h in enumerate(headers) if h.upper() == 'INT'), None)
        wis_idx = next((i for i, h in enumerate(headers) if h.upper() == 'WIS'), None)
        cha_idx = next((i for i, h in enumerate(headers) if h.upper() == 'CHA'), None)
        
        if None in [str_idx, dex_idx, con_idx, int_idx, wis_idx, cha_idx]:
            continue
        
        # Parse modifiers (handle +0, -4, etc.)
        def parse_modifier(text: str) -> int:
            text = text.strip()
            if not text:
                return 0
            if text.startswith('+'):
                return int(text[1:]) if text[1:] else 0
            elif text.startswith('-'):
                return int(text) if text != '-' else 0
            else:
                return int(text) if text else 0
        
        str_mod = parse_modifier(cells[str_idx])
        dex_mod = parse_modifier(cells[dex_idx])
        con_mod = parse_modifier(cells[con_idx])
        int_mod = parse_modifier(cells[int_idx])
        wis_mod = parse_modifier(cells[wis_idx])
        cha_mod = parse_modifier(cells[cha_idx])
        
        # Convert modifiers to scores
        str_score = modifier_to_score(str_mod)
        dex_score = modifier_to_score(dex_mod)
        con_score = modifier_to_score(con_mod)
        int_score = modifier_to_score(int_mod)
        wis_score = modifier_to_score(wis_mod)
        cha_score = modifier_to_score(cha_mod)
        
        # Calculate ETF composite scores (round down)
        fitness_score = (str_score + dex_score + con_score) // 3
        insight_score = (int_score + wis_score) // 2
        willpower_score = (wis_score + cha_score) // 2
        
        # Calculate ETF modifiers
        fitness_mod = score_to_modifier(fitness_score)
        insight_mod = score_to_modifier(insight_score)
        willpower_mod = score_to_modifier(willpower_score)
        
        # Format modifiers
        def format_modifier(mod: int) -> str:
            if mod >= 0:
                return f'+{mod}'
            return str(mod)
        
        # Clear and rebuild header row
        header_row.clear()
        for ability in ['FIT', 'INS', 'WIL']:
            th = soup.new_tag('th')
            th['class'] = 'has-text-align-center'
            th['data-align'] = 'center'
            th.string = ability
            header_row.append(th)
        
        # Clear and rebuild data row
        data_row.clear()
        for mod in [fitness_mod, insight_mod, willpower_mod]:
            td = soup.new_tag('td')
            td['class'] = 'has-text-align-center'
            td['data-align'] = 'center'
            td.string = f'\n          {format_modifier(mod)}\n        '
            data_row.append(td)
    
    return str(soup)

def convert_ability_scores(text: str) -> str:
    """Convert D&D ability scores references in text to ETF"""
    # First convert the table
    text = convert_ability_scores_table(text)
    
    # Then convert text references
    replacements = {
        r'\bSTR\b': 'FIT',
        r'\bDEX\b': 'FIT',
        r'\bCON\b': 'FIT',
        r'\bINT\b': 'INS',
        r'\bWIS\b': 'INS',
        r'\bCHA\b': 'WIL',
        r'\bStrength\b': 'Fitness',
        r'\bDexterity\b': 'Fitness',
        r'\bConstitution\b': 'Fitness',
        r'\bIntelligence\b': 'Insight',
        r'\bWisdom\b': 'Insight',
        r'\bCharisma\b': 'Willpower',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def convert_terminology(text: str) -> str:
    """Convert D&D terminology to ETF"""
    replacements = {
        r'\bActions\b': 'Moments',
        r'\bopportunity attacks\b': 'reactions',
        r'\bhalf the damage\b': 'half as much damage',
        r'\bDC\s+(\d+)\s+CHA\s+save\b': r'DC \1 WIL save',
        r'\bDC\s+(\d+)\s+CON\s+save\b': r'DC \1 FIT save',
        r'\bDC\s+(\d+)\s+DEX\s+save\b': r'DC \1 FIT save',
        r'\bDC\s+(\d+)\s+STR\s+save\b': r'DC \1 FIT save',
        r'\bDC\s+(\d+)\s+INT\s+save\b': r'DC \1 INS save',
        r'\bDC\s+(\d+)\s+WIS\s+save\b': r'DC \1 INS save',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def extract_monster_stat_block(article_html: str) -> Optional[Dict]:
    """Extract monster data from an article HTML block"""
    soup = BeautifulSoup(article_html, 'html.parser')
    
    # Find monster name
    name_elem = soup.find('h1', class_='title')
    if not name_elem:
        return None
    
    monster_name = name_elem.get_text().strip()
    
    # Find CR
    cr = 0.0
    cr_elem = soup.find(string=re.compile(r'CR\s+[\d/]+', re.IGNORECASE))
    if cr_elem:
        cr_text = cr_elem.strip()
        cr = parse_cr_value(cr_text)
    
    # Find HP
    hp = 1
    hp_elem = soup.find(string=re.compile(r'Hit Points\s+\d+', re.IGNORECASE))
    if hp_elem:
        hp_text = hp_elem.strip()
        hp = convert_hp(hp_text)
    
    # Find AC
    ac = 10
    ac_elem = soup.find(string=re.compile(r'Armor Class\s+\d+', re.IGNORECASE))
    if ac_elem:
        ac_text = ac_elem.strip()
        ac_match = re.search(r'(\d+)', ac_text)
        if ac_match:
            ac = int(ac_match.group(1))
    
    # Get full stat block HTML (original)
    stat_block_html = str(soup.find('div', class_='post-single-content'))
    
    # Convert to ETF
    etf_stat_block = stat_block_html
    
    # Convert to hit to Defense Save DC
    etf_stat_block = convert_to_hit_to_defense_save_dc(etf_stat_block)
    
    # Convert ability scores
    etf_stat_block = convert_ability_scores(etf_stat_block)
    
    # Convert terminology
    etf_stat_block = convert_terminology(etf_stat_block)
    
    # Replace HP in ETF version
    etf_stat_block = re.sub(
        r'<strong>Hit Points</strong>\s*(\d+)',
        lambda m: f'<strong>Hit Points</strong> {convert_hp(m.group(1))}',
        etf_stat_block,
        flags=re.IGNORECASE
    )
    
    return {
        'name': monster_name,
        'cr': cr,
        'hp': hp,
        'ac': ac,
        'original_html': stat_block_html,
        'etf_html': etf_stat_block
    }

def parse_monster_file(filepath: Path) -> List[Dict]:
    """Parse all monsters from a single HTML file"""
    monsters = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all monster stat blocks
    stat_blocks = soup.find_all('div', class_='monster-stat-block')
    
    for stat_block in stat_blocks:
        article = stat_block.find('article')
        if article:
            monster_data = extract_monster_stat_block(str(article))
            if monster_data:
                monsters.append(monster_data)
    
    return monsters

def main():
    """Parse all monster HTML files and create JSON data"""
    if not MONSTERS_DIR.exists():
        print(f"Directory {MONSTERS_DIR} does not exist!")
        return
    
    all_monsters = []
    
    # Get all monster HTML files
    html_files = sorted(MONSTERS_DIR.glob('monster-cr-*.html'))
    
    print(f"Found {len(html_files)} monster HTML files")
    print("=" * 60)
    
    for html_file in html_files:
        print(f"Parsing {html_file.name}...")
        monsters = parse_monster_file(html_file)
        print(f"  Found {len(monsters)} monsters")
        all_monsters.extend(monsters)
    
    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_monsters, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"Total monsters parsed: {len(all_monsters)}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
