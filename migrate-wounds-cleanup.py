#!/usr/bin/env python3
"""Second-pass cleanup for Wounds terminology."""

from pathlib import Path

ROOT = Path(__file__).parent

REPLACEMENTS = [
    ('half the damage', 'half as many Wounds (rounded down)'),
    ('Half the damage', 'Half as many Wounds (rounded down)'),
    ('only half damage', 'only half as many Wounds (rounded down)'),
    ('take only half damage', 'take only half as many Wounds (rounded down)'),
    ('takes only half damage', 'takes only half as many Wounds (rounded down)'),
    ('regaining all its HP', 'healing all its Wounds'),
    ('regains all its HP', 'heals all its Wounds'),
    ('regain all its HP', 'heal all its Wounds'),
    ('regains all their HP', 'heals all their Wounds'),
    ('regains 10 HP', 'heals 10 Wounds'),
    ('regains 14 (4d6) HP', 'heals 14 (4d6) Wounds'),
    ('regains 5 (2d4) HP', 'heals 5 (2d4) Wounds'),
    ('regain 10 (3d6) HP', 'heal 10 (3d6) Wounds'),
    ('regains 10 HP for each', 'heals 10 Wounds for each'),
    ('if it has at least 1 HP', 'if it has fewer than Max Wounds'),
    ('if it has at least 1 Max Wounds', 'if it has fewer than Max Wounds'),
    ('retains its HP,', 'retains its current Wounds and Max Wounds,'),
    ('retains its HP and', 'retains its current Wounds and Max Wounds and'),
    ('AC 20; 10 HP;', 'AC 20; 10 Max Wounds;'),
    ('; 10 HP;', '; 10 Max Wounds;'),
    ('25 or more damage', '25 or more Wounds'),
    ('or more damage in a single turn', 'or more Wounds in a single turn'),
    ('deals double damage to objects', 'inflicts double Wounds to objects'),
    ('weapon\'s normal damage', 'weapon\'s normal Wounds'),
    ('extra 3d8 damage of the type', 'extra 3d8 Wounds of the type'),
    ('3d8) damage of the type', '3d8) Wounds of the type'),
    ('slashing  damage', 'Slashing Wounds'),
    ('type of damage:', 'type of Wounds:'),
    ('one type of damage associated', 'one wound type associated'),
    ('resistant to one type of damage', 'resistant to one wound type'),
    ('any damage the wearer takes', 'any Wounds the wearer takes'),
    ('half of any damage the wearer takes', 'half of any Wounds the wearer takes'),
    ('reduction to the creature\'s HP maximum', 'reduction to the creature\'s Max Wounds'),
    ('Hit Points and Scale', 'Wounds and Scale'),
    ('regains the maximum number of Hit Points possible from any healing', 'heals the maximum number of Wounds possible from any healing'),
    ('regains Hit Points from a level', 'heals Wounds from a level'),
    ('the steed regains the same number of Hit Points', 'the steed heals the same number of Wounds'),
    ('HP 5 + 10 per spell level', 'Max Wounds 5 + 10 per spell level'),
    ('(the steed has a number of Hit Dice', '(the steed has a number of Hit Dice'),
    ('Necrotic (Fiend) damage', 'Necrotic (Fiend) Wounds'),
    ('Psychic (Fey), or Necrotic (Fiend) damage', 'Psychic (Fey), or Necrotic (Fiend) Wounds'),
    ('regains a number of Hit Points equal to', 'heals a number of Wounds equal to'),
    ('Regains a number of Hit Points equal to', 'Heals a number of Wounds equal to'),
    ('restore Hit Points', 'heal Wounds'),
    ('restores Hit Points', 'heals Wounds'),
    ('Hit Points equal to', 'Wounds equal to'),
    ('<div class="hp-name">Hit Points</div>', '<div class="hp-name">Wounds</div>'),
    ('Compressed hit points using hits and wounds', 'Compressed Wounds scale: harm adds Wounds from 0 up to Max Wounds'),
]

HP_REGEX = [
    (r'\bregains (\d+(?: \(\d+d\d+(?: \+ \d+)?\))?) HP\b', r'heals \1 Wounds'),
    (r'\bregain (\d+(?: \(\d+d\d+(?: \+ \d+)?\))?) HP\b', r'heal \1 Wounds'),
]

import re

def cleanup(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r'\bregains (\d+(?: \(\d+d\d+(?: \+ \d+)?\))?) HP\b', r'heals \1 Wounds', text)
    text = re.sub(r'\bregain (\d+(?: \(\d+d\d+(?: \+ \d+)?\))?) HP\b', r'heal \1 Wounds', text)
    text = re.sub(r'\bretains its HP\b', 'retains its current Wounds and Max Wounds', text)
    # Only replace remaining HP when not already part of Max Wounds
    text = re.sub(r'(?<!Max )\bHP\b', 'Max Wounds', text)
    # Fix over-replacements in magic steed block
    text = text.replace('regain Max Wounds from a level', 'heal Wounds from a level')
    text = text.replace('When you heal Wounds from a level', 'When you heal Wounds from a level')
    # Fix hit points in 5e description toggle areas - read sample
    text = text.replace('fifth edition Max Wounds', 'fifth edition hit points')
    return text


def main():
    count = 0
    for path in ROOT.rglob('*.html'):
        if 'migrate-wounds' in path.name:
            continue
        text = path.read_text(encoding='utf-8')
        new = cleanup(text)
        if new != text:
            path.write_text(new, encoding='utf-8')
            count += 1
    print(f'Cleanup updated {count} files')


if __name__ == '__main__':
    main()
