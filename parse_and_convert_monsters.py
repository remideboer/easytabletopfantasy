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

MONSTERS_DIR = Path('rules/monsters-bfrd')
OUTPUT_FILE = Path('data/monsters_data.js')

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

def cr_to_level(cr: float) -> int:
    """Convert CR to ETF level (same as JavaScript function)"""
    if cr <= 0:
        return 1
    if cr <= 1:
        return 1
    if cr <= 3:
        return 2
    if cr <= 5:
        return 3
    if cr <= 7:
        return 4
    if cr <= 9:
        return 5
    if cr <= 11:
        return 6
    if cr <= 13:
        return 7
    if cr <= 15:
        return 8
    if cr <= 17:
        return 9
    return 10

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

def convert_weapon_damage(text: str) -> str:
    """
    Convert weapon attack damage to ETF format.
    Weapons always deal 1 hit (2 hits on critical hit).
    According to rules/conversion.html#converting-weapons:
    - Weapon damage dice convert to attack bonuses, NOT to hits
    - All weapon attacks deal 1 hit on a successful hit
    
    This function identifies weapon attacks by looking for "Melee Weapon Attack" 
    or "Ranged Weapon Attack" patterns and converts their damage to "1 hit".
    """
    def replace_weapon_hit_single(match):
        """Replace single weapon damage"""
        damage_type = match.group(1).strip() if match.lastindex >= 1 and match.group(1) else ''
        if damage_type:
            return f"Hit: 1 hit of {damage_type} damage"
        return "Hit: 1 hit of damage"
    
    def replace_weapon_hit_plus(match):
        """Replace weapon damage with plus"""
        first_type = match.group(1).strip() if match.lastindex >= 1 and match.group(1) else ''
        second_type = match.group(2).strip() if match.lastindex >= 2 and match.group(2) else ''
        if first_type and second_type:
            return f"Hit: 1 hit of {first_type} damage plus 1 hit of {second_type} damage"
        elif first_type:
            return f"Hit: 1 hit of {first_type} damage plus 1 hit of damage"
        elif second_type:
            return f"Hit: 1 hit of damage plus 1 hit of {second_type} damage"
        return "Hit: 1 hit of damage plus 1 hit of damage"
    
    # Strategy: Find all "Hit:" patterns that appear after a weapon attack
    # We'll process the text by finding weapon attack sections and converting their damage
    
    # Split text into chunks around weapon attacks
    # Find all positions where weapon attacks occur
    weapon_positions = []
    for match in re.finditer(r'(Melee|Ranged)\s+Weapon\s+Attack', text, re.IGNORECASE):
        weapon_positions.append(match.start())
    
    if not weapon_positions:
        # No weapon attacks found, return as-is
        return text
    
    # Process each weapon attack section
    result_parts = []
    last_pos = 0
    
    for weapon_pos in weapon_positions:
        # Add text before this weapon attack
        result_parts.append(text[last_pos:weapon_pos])
        
        # Find the "Hit:" pattern after this weapon attack (within 500 chars)
        section_end = min(weapon_pos + 500, len(text))
        section = text[weapon_pos:section_end]
        
        # Find "Hit:" damage in this section
        hit_match = re.search(
            r'Hit:\s*\d+\s*\(\d+d\d+(?:\s*[+\-]\s*\d+)?\)\s*([^.]+?)?\s*damage(?:\s+plus\s+\d+\s*\(\d+d\d+(?:\s*[+\-]\s*\d+)?\)\s*([^.]+?)?\s*damage)?',
            section,
            re.IGNORECASE
        )
        
        if hit_match:
            # Replace the damage part
            hit_start = weapon_pos + hit_match.start()
            hit_end = weapon_pos + hit_match.end()
            
            # Get the damage replacement
            if 'plus' in hit_match.group(0).lower():
                replacement = replace_weapon_hit_plus(hit_match)
            else:
                replacement = replace_weapon_hit_single(hit_match)
            
            # Add text up to the hit, then replacement, then continue
            result_parts.append(text[weapon_pos:hit_start])
            result_parts.append(replacement)
            last_pos = hit_end
        else:
            # No hit found in this section, just add the section
            result_parts.append(section)
            last_pos = section_end
    
    # Add remaining text
    result_parts.append(text[last_pos:])
    
    return ''.join(result_parts)

def convert_damage_to_hits(text: str) -> str:
    """
    Convert D&D damage expressions to ETF hits format.
    Rules from conversion.html:
    - For WEAPONS: Always 1 hit (handled by convert_weapon_damage)
    - For SPELLS/EFFECTS: 
      1. Take maximum total of dice expression
      2. Divide by 6
      3. Round to nearest whole number
    For mixed: convert dice and bonus separately, then add.
    
    Examples (spells/effects):
    - "Hit: 16 (2d10 + 5) piercing damage" -> "Hit: 4 hits of piercing damage"
      (2d10 max=20, 20/6=3.33->3 hits; +5, 5/6=0.83->1 hit; total=4 hits)
    - "Hit: 2 (1d4) piercing damage" -> "Hit: 1 hit of piercing damage"
      (1d4 max=4, 4/6=0.67->1 hit)
    - "Hit: 6 (1d6 + 3) bludgeoning damage plus 9 (2d8) piercing damage" 
      -> "Hit: 2 hits of bludgeoning damage plus 3 hits of piercing damage"
    """
    # First, convert weapon damage (weapons always deal 1 hit)
    text = convert_weapon_damage(text)
    
    def calculate_hits(dice_expr: str, bonus: int = 0) -> int:
        """Calculate hits from dice expression and optional bonus"""
        # Parse dice (e.g., "2d10", "3d4", "1d8")
        dice_match = re.match(r'(\d+)d(\d+)', dice_expr.strip())
        if not dice_match:
            return 1
        
        num_dice = int(dice_match.group(1))
        die_size = int(dice_match.group(2))
        max_dice = num_dice * die_size
        
        # Divide by 6, round to nearest
        dice_hits = round(max_dice / 6)
        dice_hits = max(1, dice_hits)  # Minimum 1 hit from dice
        
        # Add bonus hits if any
        if bonus > 0:
            bonus_hits = round(bonus / 6)
            dice_hits += bonus_hits
        
        return max(1, dice_hits)  # Ensure minimum 1 hit total
    
    def convert_single_damage_expr(dice_expr: str, damage_type: str = '') -> str:
        """Convert a single damage expression to hits format"""
        bonus_match = re.search(r'([+\-])\s*(\d+)', dice_expr)
        bonus = 0
        if bonus_match:
            sign = bonus_match.group(1)
            bonus_val = int(bonus_match.group(2))
            dice_expr = re.sub(r'\s*[+\-]\s*\d+', '', dice_expr)
            if sign == '+':
                bonus = bonus_val
        
        hits = calculate_hits(dice_expr, bonus if bonus > 0 else 0)
        hit_text = f"{hits} hit{'s' if hits != 1 else ''}"
        
        if damage_type:
            return f"{hit_text} of {damage_type} damage"
        else:
            return hit_text
    
    # Pattern 1: "Hit: X (YdZ + B) damage_type damage plus A (BdC) other_type damage"
    # Handle "plus" patterns first (most complex)
    def replace_hit_with_plus(match):
        # Extract both damage parts
        first_dice = match.group(1)
        first_type = match.group(2).strip() if match.lastindex >= 2 and match.group(2) else ''
        second_dice = match.group(3)
        second_type = match.group(4).strip() if match.lastindex >= 4 and match.group(4) else ''
        
        first_converted = convert_single_damage_expr(first_dice, first_type)
        second_converted = convert_single_damage_expr(second_dice, second_type)
        
        return f"Hit: {first_converted} plus {second_converted}"
    
    # Match "Hit: X (YdZ) type damage plus A (BdC) other_type damage"
    text = re.sub(
        r'Hit:\s*\d+\s*\((\d+d\d+(?:\s*[+\-]\s*\d+)?)\)\s*([^.]+?)?\s*damage\s+plus\s+\d+\s*\((\d+d\d+(?:\s*[+\-]\s*\d+)?)\)\s*([^.]+?)?\s*damage',
        replace_hit_with_plus,
        text,
        flags=re.IGNORECASE
    )
    
    # Pattern 2: "Hit: X (YdZ + B) damage_type damage" (single damage)
    def replace_hit_damage(match):
        dice_expr = match.group(1)
        damage_type = match.group(2).strip() if match.lastindex >= 2 and match.group(2) else ''
        converted = convert_single_damage_expr(dice_expr, damage_type)
        return f"Hit: {converted}"
    
    text = re.sub(
        r'Hit:\s*\d+\s*\((\d+d\d+(?:\s*[+\-]\s*\d+)?)\)\s*([^.]+?)?\s*damage',
        replace_hit_damage,
        text,
        flags=re.IGNORECASE
    )
    
    # Pattern 3: Just dice in parentheses, like "2 (1d4) damage" (without "Hit:")
    def replace_damage_in_parens(match):
        dice_expr = match.group(1)
        damage_type = match.group(2).strip() if match.lastindex >= 2 and match.group(2) else ''
        converted = convert_single_damage_expr(dice_expr, damage_type)
        return f"({converted})"
    
    text = re.sub(
        r'\(\s*(\d+d\d+(?:\s*[+\-]\s*\d+)?)\s*\)\s*([^.]+?)?\s*damage',
        replace_damage_in_parens,
        text,
        flags=re.IGNORECASE
    )
    
    return text

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
        r'\bCR\s+': 'Level ',
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
    
    # Convert damage to hits
    etf_stat_block = convert_damage_to_hits(etf_stat_block)
    
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
    
    # Calculate default ETF level from CR
    level = cr_to_level(cr)
    
    return {
        'name': monster_name,
        'cr': cr,
        'level': level,
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
    
    # Save to JavaScript file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('const monstersDataEmbedded = ')
        json.dump(all_monsters, f, indent=2, ensure_ascii=False)
        f.write(';\n')

    print("=" * 60)
    print(f"Total monsters parsed: {len(all_monsters)}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
