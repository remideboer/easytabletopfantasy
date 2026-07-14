#!/usr/bin/env python3
"""Use singular Wound when the amount is exactly 1."""

import re
from pathlib import Path

ROOT = Path(__file__).parent

# <strong>1</strong> [optional <strong>Type</strong>...] <strong>Wounds</strong>
STRONG_ONE_WOUNDS = re.compile(
    r'(<strong>1</strong>(?:\s*\+\s*<strong>1</strong>)?(?:\s*<strong>[A-Za-z]+</strong>)*\s*)<strong>Wounds</strong>'
)

REPLACEMENTS = [
    (r'\bheals 1 Wounds\b', 'heals 1 Wound'),
    (r'\bheal 1 Wounds\b', 'heal 1 Wound'),
    (r'\btakes 1 Wounds\b', 'takes 1 Wound'),
    (r'\btake 1 Wounds\b', 'take 1 Wound'),
    (r'\bdeals 1 Wounds\b', 'deals 1 Wound'),
    (r'\bdeal 1 Wounds\b', 'deal 1 Wound'),
    (r'\binflicts 1 Wounds\b', 'inflicts 1 Wound'),
    (r'\binflict 1 Wounds\b', 'inflict 1 Wound'),
    (r'\bgains 1 Wounds\b', 'gains 1 Wound'),
    (r'\b1 Wounds of a type\b', '1 Wound of a type'),
    (r'\b1 Wounds\b', '1 Wound'),
    # Typed wounds only — never touch "Max Wounds"
    (r'\b1 (?!Max\b)([A-Z][a-z]+) Wounds\b', r'1 \1 Wound'),
]


def fix_text(text: str) -> str:
    text = STRONG_ONE_WOUNDS.sub(r'\1<strong>Wound</strong>', text)
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    return text


def main():
    changed = 0
    for path in ROOT.rglob('*.html'):
        if 'fix-wound' in path.name or 'migrate-wounds' in path.name:
            continue
        original = path.read_text(encoding='utf-8')
        updated = fix_text(original)
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            changed += 1
    print(f'Updated {changed} files')


if __name__ == '__main__':
    main()
