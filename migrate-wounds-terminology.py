#!/usr/bin/env python3
"""Migrate HP/damage/hits terminology to Wounds/Max Wounds across HTML files."""

import re
from pathlib import Path

ROOT = Path(__file__).parent

SKIP_DIRS = {'.git', 'node_modules', '.cursor', 'foundation'}

# Ordered replacements: longer/more specific phrases first
REPLACEMENTS = [
    # Anchors and headings
    ('id="converting-hit-points"', 'id="converting-max-wounds"'),
    ('#converting-hit-points', '#converting-max-wounds'),
    ('Converting Hit Points', 'Converting Max Wounds'),
    ('#hit-points-and-scale', '#wounds-and-scale'),
    ('#damage-and-healing', '#wounds-and-healing'),

    # Class / formula phrases
    ('class start Hit Points', 'class start Max Wounds'),
    ('class hit die maximum', 'class Max Wounds base'),
    ('class hit points', 'class Max Wounds'),
    ('compressed hit point scale', 'compressed Wounds scale'),
    ('fifth edition hit points', 'fifth edition hit points'),  # keep for conversion context
    ('one-tenth of their fifth edition hit points', 'one-tenth of their fifth edition hit points'),

    # Stat block header
    ('<strong>Hit Points</strong>', '<strong>Max Wounds</strong>'),

    # HP phrases (longest first)
    ("can't regain Hit Points", "can't heal Wounds"),
    ("can't regain HP", "can't heal Wounds"),
    ('regain Hit Points until', 'heal Wounds until'),
    ('regain HP until', 'heal Wounds until'),
    ('hit point maximum increases', 'Max Wounds increases'),
    ('hit point maximum is reduced', 'Max Wounds is reduced'),
    ('hit point maximum to 0', 'Max Wounds to 0'),
    ('HP maximum is reduced', 'Max Wounds is reduced'),
    ('HP maximum to 0', 'Max Wounds to 0'),
    ('reduces its HP maximum', 'reduces its Max Wounds'),
    ('reduces the target\'s HP maximum', 'reduces the target\'s Max Wounds'),
    ('its HP maximum', 'its Max Wounds'),
    ('their HP maximum', 'their Max Wounds'),
    ('hit point maximum', 'Max Wounds'),
    ('current hit points', 'current Wounds'),
    ('current Hit Points', 'current Wounds'),
    ('hit points regained', 'Wounds healed'),
    ('hit points of healing', 'Wounds of healing'),
    ('regain hit points', 'heal Wounds'),
    ('regains hit points', 'heals Wounds'),
    ('regained hit points', 'healed Wounds'),
    ('restore hit points', 'heal Wounds'),
    ('restores hit points', 'heals Wounds'),
    ('restored hit points', 'healed Wounds'),
    ('regain HP', 'heal Wounds'),
    ('regains HP', 'heals Wounds'),
    ('regaining HP', 'healing Wounds'),
    ('regained HP', 'healed Wounds'),
    ('magically regains', 'magically heals'),
    ('regains all its HP', 'heals all its Wounds'),
    ('regains all its Hit Points', 'heals all its Wounds'),
    ('regain all their HP', 'heal all their Wounds'),
    ('no HP is restored', 'no Wounds are healed'),
    ('restore HP again', 'heal Wounds again'),
    ('regain HP equal to', 'heal Wounds equal to'),
    ('regains HP equal to', 'heals Wounds equal to'),
    ('gains temporary HP equal to', 'gains temporary Max Wounds equal to'),
    ('gain temporary HP', 'gain temporary Max Wounds'),
    ('gains temporary HP', 'gains temporary Max Wounds'),
    ('temporary HP', 'temporary Max Wounds'),
    ('Requires Temporary HP', 'Requires Temporary Max Wounds'),
    ('has 1 or more temporary Max Wounds', 'has temporary Max Wounds remaining'),
    ("can't regain Max Wounds or gain temporary Max Wounds", "can't heal Wounds or gain temporary Max Wounds"),
    ('reduced to 0 HP', 'reaches Max Wounds'),
    ('reduces the target to 0 HP', "fills the target's Wounds to Max Wounds"),
    ('reduce a creature to 0 HP', "fill a creature's Wounds to Max Wounds"),
    ('reduces a creature to 0 HP', "fills a creature's Wounds to Max Wounds"),
    ('at 0 HP', 'at Max Wounds'),
    ('to 0 HP', 'to Max Wounds'),
    ('reaches 0 HP', 'reaches Max Wounds'),
    ('all of their HP', '0 Wounds'),
    ('all of its HP', '0 Wounds'),
    ("doesn't have all of their HP", 'has taken Wounds'),
    ("doesn't have all of its HP", 'has taken Wounds'),
    ("doesn't have all its HP", 'has taken Wounds'),
    ('any creature that doesn\'t have all its HP', 'any creature that has taken Wounds'),
    ('any creature that doesn\'t have all of their HP', 'any creature that has taken Wounds'),
    ('half of its HP or fewer', 'Wounds at or above half its Max Wounds'),
    ('after regaining HP', 'after healing Wounds'),
    ('even after regaining HP', 'even after healing Wounds'),
    ('then hearts, then HP', 'then hearts, then Wounds'),
    ('then HP', 'then Wounds'),
    ('retains its Celestial Resilience and Inscrutable traits and its HP, HD', 'retains its Celestial Resilience and Inscrutable traits and its Max Wounds, HD'),
    ('is stable but poisoned for 1 hour, even after healing Wounds, and', 'is stable but poisoned for 1 hour, even after healing Wounds, and'),
    ('reduced to 1 HP instead', 'left with Max Wounds minus 1 instead'),
    ('that would reduce it to 0 HP', 'that would bring it to Max Wounds'),
    ('loses 2 (1d4) HP at the start', 'gains 2 (1d4) Wounds at the start'),
    ('lose 7 (2d6) HP at the start', 'gain 7 (2d6) Wounds at the start'),
    ('loses most of its memories', 'loses most of its memories'),  # no change

    # YMIAT hit-as-damage unit
    ('1 hit of damage', '1 Wound'),
    ('2 hits of damage', '2 Wounds'),
    ('deals 1 hit of damage', 'inflicts 1 Wound'),
    ('deal 1 hit of damage', 'inflict 1 Wound'),
    ('deals <strong>1 hit</strong> of damage', 'inflicts <strong>1 Wound</strong>'),
    ('deals <strong>2 hits</strong>', 'inflicts <strong>2 Wounds</strong>'),
    ('Each missile deals 1 hit', 'Each missile inflicts 1 Wound'),
    ('number of hits dealt', 'number of Wounds inflicted'),
    ('number of hits', 'number of Wounds'),
    ('normal hits (e.g. 1 hit, or 2 on a critical)', 'normal Wounds (e.g. 1 Wound, or 2 on a critical)'),
    ('in <strong>hits</strong>', 'in <strong>Wounds</strong>'),
    ('expressed in <strong>hits</strong>', 'expressed in <strong>Wounds</strong>'),
    ('expressed in hits', 'expressed in Wounds'),
    ('converted into hits', 'converted into Wounds'),
    ('convert dice-based values from fifth edition:', 'convert dice-based values from fifth edition:'),
    ('→ 2 hits', '→ 2 Wounds'),
    ('→ 1 hit', '→ 1 Wound'),
    ('→ 3 hits', '→ 3 Wounds'),
    ('→ 4 hits', '→ 4 Wounds'),
    ('Total: 2 hits.', 'Total: 2 Wounds.'),
    ('1 Hit +', '1 Wound +'),
    ('1 Hit damage', '1 Wound'),
    ('takes 1 hit on a failed save', 'takes 1 Wound on a failed save'),
    ('no damage on a successful one', 'no Wounds on a successful one'),
    ('no damage on a successful save', 'no Wounds on a successful save'),
    ('half as much damage on a successful', 'half as many Wounds (rounded down) on a successful'),
    ('half as much damage on a failed', 'half as many Wounds (rounded down) on a failed'),
    ('half as much damage', 'half as many Wounds (rounded down)'),
    ('half the necrotic damage dealt', 'half the necrotic Wounds dealt'),
    ('equal to the necrotic damage taken', 'equal to the necrotic Wounds taken'),
    ('equal to the damage taken', 'equal to the Wounds taken'),

    # Spell damage tags
    ('<strong>damage</strong>', '<strong>Wounds</strong>'),
    ('The damage increases', 'The Wounds increase'),
    ('spell\'s damage', 'spell\'s Wounds'),
    ('to the damage', 'to the Wounds'),
    ('add it to the damage', 'add it to the Wounds'),
    ('maximum number of these d20s you can add to the spell\'s Wounds', 'maximum number of these d20s you can add to the spell\'s Wounds'),

    # Damage types in prose (lowercase type + damage)
    ('acid damage', 'Acid Wounds'),
    ('bludgeoning damage', 'Bludgeoning Wounds'),
    ('cold damage', 'Cold Wounds'),
    ('fire damage', 'fire Wounds'),
    ('force damage', 'Force Wounds'),
    ('lightning damage', 'Lightning Wounds'),
    ('necrotic damage', 'necrotic Wounds'),
    ('piercing damage', 'Piercing Wounds'),
    ('poison damage', 'Poison Wounds'),
    ('psychic damage', 'Psychic Wounds'),
    ('radiant damage', 'Radiant Wounds'),
    ('slashing damage', 'Slashing Wounds'),
    ('thunder damage', 'Thunder Wounds'),
    ('poison Wounds', 'Poison Wounds'),  # fix double
    ('Fire Wounds', 'Fire Wounds'),
    ('deal fire Wounds', 'inflict Fire Wounds'),
    ('deal damage', 'inflict Wounds'),
    ('deals damage', 'inflicts Wounds'),
    ('take damage', 'take Wounds'),
    ('takes damage', 'takes Wounds'),
    ('no damage', 'no Wounds'),
    ('deal a small amount of damage', 'inflict a small number of Wounds'),
    ('dealing damage', 'inflicting Wounds'),
    ('dealing consistent damage', 'inflicting consistent Wounds'),
    ('deal damage in melee', 'inflict Wounds in melee'),
    ('damage resistance', 'resistance'),
    ('damage type', 'wound type'),
    ('damage types', 'wound types'),
    ('Damage type', 'Wound type'),
    ('Damage types', 'Wound types'),
    ('Damage Resistance', 'Resistance'),
    ('damage rolls', 'attack rolls'),
    ('attack and attack rolls', 'attack rolls'),

    # Healing spells
    ('heals a number of Hit Points equal to', 'heals a number of Wounds equal to'),
    ('heals a number of hit points equal to', 'heals a number of Wounds equal to'),
    ('regains a number of hit points equal to', 'heals a number of Wounds equal to'),
    ('regains hit points equal to', 'heals Wounds equal to'),
    ('regain hit points equal to', 'heal Wounds equal to'),

    # Table headers
    ('<th>HP</th>', '<th>Max WD</th>'),

    # Formula boxes
    ('<span class="variable">HP</span>', '<span class="variable">Max Wounds</span>'),

    # Misc
    ('calculate modifiers and hit points', 'calculate modifiers and Max Wounds'),
    ('determines your hit points', 'determines your Max Wounds'),
    ('your hit point maximum increases', 'your Max Wounds increases'),
    ('your hit point maximum', 'your Max Wounds'),
    ('spend hit dice to regain hit points', 'spend Recovery Points to heal Wounds'),
    ('${baseDamage} hits', '${baseDamage} Wounds'),
    ('data-base-damage', 'data-base-wounds'),
    ('base-damage', 'base-wounds'),
    ('Filter by damage type:', 'Filter by wound type:'),
    ('slashing or lightning damage', 'slashing or Lightning Wounds'),
    ('lightning or slashing damage', 'Lightning or slashing Wounds'),
]

# Regex replacements (applied after string replacements)
REGEX_REPLACEMENTS = [
    # Attack line: "Hit: X (YdZ) type damage" -> "Hit: X (YdZ) type Wounds"
    (re.compile(r'\b(\w+) damage\b', re.IGNORECASE), lambda m: f"{m.group(1).capitalize() if m.group(1).lower() in ('acid','cold','fire','force','lightning','necrotic','piercing','poison','psychic','radiant','slashing','thunder','bludgeoning') else m.group(1)} Wounds" if m.group(1).lower() not in ('maximum', 'type', 'types', 'resistance', 'roll', 'rolls') else m.group(0)),
    # Remaining standalone HP in monster text - careful
    (re.compile(r'\b(\d+) HP\b'), r'\1 Max Wounds'),
    (re.compile(r'\bHP\b'), 'Max Wounds'),
    # Hit dice in talents - keep as Recovery Points context
]

# Files to process
def should_process(path: Path) -> bool:
    if path.suffix != '.html':
        return False
    parts = path.parts
    if any(p in SKIP_DIRS for p in parts):
        return False
    return True


def migrate_text(text: str, path: Path) -> str:
    original = text
    for old, new in REPLACEMENTS:
        if old == new:
            continue
        text = text.replace(old, new)

    # Fix over-replacements
    text = text.replace('Poison Wounds', 'Poison Wounds')
    text = text.replace('poison Wounds', 'Poison Wounds')
    text = text.replace('necrotic Wounds', 'Necrotic Wounds')
    text = text.replace('fire Wounds', 'Fire Wounds')
    text = text.replace('resistance to poison Wounds', 'resistance to Poison Wounds')
    text = text.replace('resistance to fire Wounds', 'resistance to Fire Wounds')
    text = text.replace('wound type associated with your fiendish legacy', 'wound type associated with your fiendish legacy')
    text = text.replace('inflict fire Wounds', 'inflict Fire Wounds')
    text = text.replace('Wound types have no rules', 'Wound types have no rules')
    text = text.replace('Filter by wound type:', 'Filter by wound type:')
    text = text.replace('data-filter-type="damage"', 'data-filter-type="damage"')  # keep filter attrs
    text = text.replace('data-damage=', 'data-damage=')
    text = text.replace('data-spell-types="damage"', 'data-spell-types="damage"')
    text = text.replace('toggleDamageFilter', 'toggleDamageFilter')
    text = text.replace('getAttribute(\'data-base-wounds\')', "getAttribute('data-base-wounds')")
    # Fix "Hit:" attack lines - restore if broken
    text = re.sub(r'\bWounds:\s', 'Hit: ', text)  # shouldn't happen
  # Don't run broad HP regex on conversion.html fifth edition references
    if 'conversion.html' in str(path):
        text = text.replace('one-tenth of their fifth edition Max Wounds', 'one-tenth of their fifth edition hit points')
        text = text.replace('fifth edition Max Wounds', 'fifth edition hit points')

    # Remaining hit counts in breath weapon etc.
    text = re.sub(r'\b(\d+) hits when you reach', r'\1 Wounds when you reach', text)
    text = re.sub(r'\(2 hits\)', '(2 Wounds)', text)
    text = re.sub(r'\(3 hits\)', '(3 Wounds)', text)
    text = re.sub(r'\(4 hits\)', '(4 Wounds)', text)
    text = re.sub(r'damage increases by (\d+) when you reach levels', r'Wounds increase by \1 when you reach levels', text)
    text = re.sub(r'takes (\d+) damage of a type', r'takes \1 Wounds of a type', text)
    text = re.sub(r'If the attack inflicts Wounds, it can be', 'If the attack inflicts Wounds, it can be', text)
    text = re.sub(r'whether it does bludgeoning, piercing, or slashing Wounds', 'whether it inflicts Bludgeoning, Piercing, or Slashing Wounds', text)

    return text


def main():
    changed_files = []
    for path in ROOT.rglob('*.html'):
        if not should_process(path):
            continue
        if 'migrate-wounds' in path.name:
            continue
        text = path.read_text(encoding='utf-8')
        new_text = migrate_text(text, path)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            changed_files.append(path.relative_to(ROOT))
    print(f'Updated {len(changed_files)} files:')
    for f in sorted(changed_files)[:50]:
        print(f'  {f}')
    if len(changed_files) > 50:
        print(f'  ... and {len(changed_files) - 50} more')


if __name__ == '__main__':
    main()
