#!/usr/bin/env python3
"""Third-pass: remaining damage/HP phrasing."""

from pathlib import Path
import re

ROOT = Path(__file__).parent

REPLACEMENTS = [
    ('take the same damage', 'take the same Wounds'),
    ("weapon's normal damage", "weapon's normal Wounds"),
    ('deals one extra die of its damage', 'deals one extra die of Wounds'),
    ('deals triple damage to objects', 'inflicts triple Wounds to objects'),
    ('deals double damage to objects', 'inflicts double Wounds to objects'),
    ('deals double damage  to objects', 'inflicts double Wounds to objects'),
    ('takes 60 damage or more', 'takes 60 Wounds or more'),
    ('takes 50 damage or more', 'takes 50 Wounds or more'),
    ('takes 30 damage or more', 'takes 30 Wounds or more'),
    ('taking 60 damage or more', 'taking 60 Wounds or more'),
    ('reducing the damage by', 'reducing the Wounds by'),
    ('halves the damage from', 'halves the Wounds from'),
    ('damage taken', 'Wounds taken'),
    ('because of taking damage', 'because of taking Wounds'),
    ('loses concentration because of taking damage', 'loses concentration because of taking Wounds'),
    ('missing any of its Hit Points', 'has any Wounds'),
    ('Temporary Hit Points', 'temporary Max Wounds'),
    ('temporary Hit Points', 'temporary Max Wounds'),
    ('Hit Point Dice', 'Hit Dice'),
    ('Hit Point maximum', 'Max Wounds'),
    ('Hit Points, and', 'current Wounds and Max Wounds, and'),
    ('its Hit Points', 'its current Wounds'),
    ('all its Hit Points', 'all its Wounds (reset to 0)'),
    ('returns to life with all its Wounds (reset to 0)', 'returns to life with 0 Wounds'),
    ('Hit Points equal to your Hit Point maximum', 'Max Wounds equal to your Max Wounds'),
    ('Hit Points equal to your Max Wounds maximum', 'Max Wounds equal to your Max Wounds'),
    ('drops to <strong>0</strong> Points', 'reaches Max Wounds'),
    ('If it drops to', 'If it reaches'),
    ('damage from holy water', 'Wounds from holy water'),
    ('or damage from holy water', 'or Wounds from holy water'),
    ('including any damage that reduces', 'including any Wounds that bring'),
    ('takes 14 damage or less', 'takes 14 Wounds or less'),
    ('takes 10 damage or less', 'takes 10 Wounds or less'),
    ('If damage reduces the zombie to Max Wounds', 'If Wounds bring the zombie to Max Wounds'),
    ('drops to 1 Max Wounds instead', 'is left at Max Wounds minus 1 instead'),
    ('without taking damage from them', 'without taking Wounds from them'),
    ('taking no falling damage', 'taking no falling Wounds'),
    ('an extra 1d6 damage of the weapon\'s type', 'an extra 1d6 Wounds of the weapon\'s type'),
    ('an extra 3 (1d6) damage of the weapon\'s type', 'an extra 3 (1d6) Wounds of the weapon\'s type'),
    ('an extra 7 (2d6) damage of the weapon\'s type', 'an extra 7 (2d6) Wounds of the weapon\'s type'),
    ('the damage dealt by the wound', 'the Wounds dealt by the wound'),
    ('immunity to one type of damage', 'immunity to one wound type'),
    ('immunity to all nonmagical damage', 'immunity to all nonmagical Wounds'),
    ('except the damage it takes from sunlight', 'except the Wounds it takes from sunlight'),
    ('resistance against this damage', 'resistance against these Wounds'),
    ('rolls damage dice three times', 'rolls Wound dice three times'),
    ('taking 21 (6d6) damage on a failed save', 'taking 21 (6d6) Wounds on a failed save'),
    ('force the grappled creature to take the damage instead', 'force the grappled creature to take the Wounds instead'),
    ('If the target would take enough damage to reduce it to Max Wounds', 'If the target would take enough Wounds to reach Max Wounds'),
    ('regains Hit Points equal to', 'heals Wounds equal to'),
    ('regain Hit Points equal to', 'heal Wounds equal to'),
    ('regains a number of Hit Points equal to', 'heals a number of Wounds equal to'),
    ('regains Hit Points equal to <strong>', 'heals Wounds equal to <strong>'),
    ('regain Hit Points equal to <strong>', 'heal Wounds equal to <strong>'),
    ('also regain <strong>', 'also heal <strong>'),
    ('gains the same number of Hit Points', 'heals the same number of Wounds'),
    ('Hit Point maximum also increases', 'Max Wounds also increases'),
    ('half the amount of <strong>Necrotic</strong> dealt', 'half the <strong>Necrotic</strong> Wounds dealt (rounded down)'),
    ('Regardless of its Hit Points', 'Regardless of its Wounds'),
    ('Hit Points Effect', 'Wounds Effect'),
]

# Divine Word table uses HP thresholds - in wound system high wounds = bad
# 0-20 HP effect "dies" -> at Max Wounds
# Need special handling - skip for now or convert table

def cleanup(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r'\b(\d+) damage or less\b', r'\1 Wounds or less', text)
    text = re.sub(r'\b(\d+) damage or more\b', r'\1 Wounds or more', text)
    text = re.sub(r'\b(\d+) damage on a failed save\b', r'\1 Wounds on a failed save', text)
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
    print(f'Third pass updated {count} files')


if __name__ == '__main__':
    main()
