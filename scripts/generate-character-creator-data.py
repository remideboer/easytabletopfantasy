#!/usr/bin/env python3
"""Generate assets/character-creator-data.json from YMIAT Python data sources."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from character_options_data import (  # noqa: E402
    BACKGROUNDS,
    HERITAGES,
    LINEAGE_HERITAGE_RECOMMENDATIONS,
    LINEAGES,
)
from class_subclasses_data import get_subclasses_by_class  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "generate_classes_html", SCRIPT_DIR / "generate-classes-html.py"
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
CLASSES = _mod.CLASSES

ROOT = SCRIPT_DIR.parent
OUT = ROOT / "assets" / "character-creator-data.json"


def slugify(name: str) -> str:
    text = name.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "item"


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def teaser(html: str, max_len: int = 220) -> str:
    plain = strip_html(html)
    if len(plain) <= max_len:
        return plain
    return plain[: max_len - 1].rsplit(" ", 1)[0] + "…"


def key_ability_code(key_ability: str) -> str:
    upper = key_ability.upper()
    if "FIT" in upper:
        return "fit"
    if "INS" in upper:
        return "ins"
    if "WIL" in upper:
        return "wil"
    return "fit"


def build_heritage_recommendations() -> dict[str, list[str]]:
    """Map lineage name -> list of recommended heritage names."""
    by_lineage: dict[str, list[str]] = {}
    for lineage_label, heritage_list in LINEAGE_HERITAGE_RECOMMENDATIONS:
        names = [h.strip() for h in heritage_list.split(",")]
        # Normalize keys: use base lineage name before parenthetical
        base = re.sub(r"\s*\(.*\)", "", lineage_label).strip()
        by_lineage.setdefault(lineage_label, []).extend(names)
        by_lineage.setdefault(base, []).extend(names)
    for key in list(by_lineage):
        by_lineage[key] = sorted(set(by_lineage[key]))
    return by_lineage


def export_classes() -> list[dict]:
    subs_by_class = get_subclasses_by_class()
    result = []
    for cls in CLASSES:
        cid = cls["id"]
        subclasses = subs_by_class.get(cid, [])
        result.append(
            {
                "id": cid,
                "name": cls["name"],
                "summary": cls.get("summary", ""),
                "maxWd": cls.get("max_wd"),
                "keyAbility": key_ability_code(cls.get("key_ability", "")),
                "keyAbilityLabel": cls.get("key_ability", ""),
                "saves": cls.get("saves", ""),
                "proficiencies": cls.get("proficiencies", ""),
                "spellcasting": cls.get("spellcasting"),
                "rulesUrl": f"rules/classes.html#{cid}",
                "abilitiesUrl": f"rules/class-abilities/{cid}.html",
                "subclasses": [
                    {
                        "id": sub["subclass_id"],
                        "name": sub["subclass_name"],
                        "summary": sub.get("summary", ""),
                        "rulesUrl": f"rules/class-abilities/{cid}.html#{sub['subclass_id']}",
                    }
                    for sub in subclasses
                ],
            }
        )
    return result


def export_named_options(items: list[dict], *, rules_page: str) -> list[dict]:
    exported = []
    for item in items:
        name = item["name"]
        sid = slugify(name)
        exported.append(
            {
                "id": sid,
                "name": name,
                "teaser": teaser(item.get("body", "")),
                "body": item.get("body", ""),
                "tag": item.get("tag"),
                "recommendedFor": item.get("recommended"),
                "rulesUrl": f"rules/{rules_page}.html#{sid}",
            }
        )
    return exported


STEPS = [
    {
        "id": "concept",
        "title": "Character Concept",
        "shortTitle": "Concept",
        "overviewAnchor": "character-concept",
        "description": "What kind of hero do you want to play? Pick an archetype and jot a few notes—mechanical choices come next.",
        "type": "concept",
    },
    {
        "id": "class",
        "title": "Choose a Class",
        "shortTitle": "Class",
        "overviewAnchor": "choose-a-class",
        "description": "Your class defines combat role, Max Wounds, and core features.",
        "type": "class",
    },
    {
        "id": "subclass",
        "title": "Choose a Subclass",
        "shortTitle": "Subclass",
        "overviewAnchor": "choose-a-class",
        "description": "At 2nd level in YMIAT you take a subclass—choose yours now so your build stays cohesive.",
        "type": "subclass",
        "requires": ["class"],
    },
    {
        "id": "abilities",
        "title": "Determine Ability Scores",
        "shortTitle": "Abilities",
        "overviewAnchor": "determine-ability-scores",
        "description": "Assign Fitness, Insight, and Willpower modifiers using your group's preferred method.",
        "type": "abilities",
    },
    {
        "id": "lineage",
        "title": "Choose a Lineage",
        "shortTitle": "Lineage",
        "overviewAnchor": "choose-a-lineage",
        "description": "Lineage traits shape ancestry and fundamental abilities.",
        "type": "lineage",
    },
    {
        "id": "heritage",
        "title": "Choose a Heritage",
        "shortTitle": "Heritage",
        "overviewAnchor": "choose-a-heritage",
        "description": "Heritage adds cultural flavor and extra traits. Any heritage works with any lineage—recommendations highlight common pairings.",
        "type": "heritage",
        "requires": ["lineage"],
    },
    {
        "id": "background",
        "title": "Choose a Background",
        "shortTitle": "Background",
        "overviewAnchor": "choose-a-background",
        "description": "Background reflects life before adventuring—skills, gear, and a defining talent.",
        "type": "background",
    },
    {
        "id": "equipment",
        "title": "Starting Equipment",
        "shortTitle": "Equipment",
        "overviewAnchor": "starting-equipment",
        "description": "Take standard packages or roll starting wealth—confirm with your GM.",
        "type": "equipment",
        "requires": ["class", "background"],
    },
    {
        "id": "review",
        "title": "Review Character",
        "shortTitle": "Review",
        "overviewAnchor": "character-creation-overview",
        "description": "Check your choices, copy a summary, or start over.",
        "type": "review",
    },
]

CONCEPT_ARCHETYPES = [
    {
        "id": "melee",
        "label": "Melee Combatant",
        "hint": "Front-line fighter with sword, axe, or fist.",
        "suggestedKeyAbility": "fit",
        "suggestedClasses": ["barbarian", "fighter", "paladin", "monk"],
    },
    {
        "id": "magic",
        "label": "Magic User",
        "hint": "Spells to harm, heal, or control the field.",
        "suggestedKeyAbility": "ins",
        "suggestedClasses": ["wizard", "cleric", "druid", "sorcerer", "warlock", "bard", "theurge", "witch"],
    },
    {
        "id": "ranged",
        "label": "Ranged Fighter",
        "hint": "Bow, crossbow, or thrown weapons at distance.",
        "suggestedKeyAbility": "fit",
        "suggestedClasses": ["ranger", "fighter", "rogue"],
    },
    {
        "id": "sneaky",
        "label": "Sneaky Character",
        "hint": "Stealth, cunning, and precision.",
        "suggestedKeyAbility": "fit",
        "suggestedClasses": ["rogue", "ranger", "monk"],
    },
    {
        "id": "support",
        "label": "Support Character",
        "hint": "Buff allies, heal, and control enemies.",
        "suggestedKeyAbility": "wil",
        "suggestedClasses": ["cleric", "bard", "druid", "vanguard", "witch"],
    },
    {
        "id": "hybrid",
        "label": "Hybrid Character",
        "hint": "Blend martial prowess with magic or tactics.",
        "suggestedKeyAbility": "fit",
        "suggestedClasses": ["paladin", "ranger", "artificer", "theurge", "vanguard"],
    },
]

ABILITY_METHODS = [
    {
        "id": "standard-array",
        "label": "Standard Array",
        "description": "Assign +2, +1, and +0 to Fitness, Insight, and Willpower in any order.",
    },
    {
        "id": "point-buy",
        "label": "Point-Buy",
        "description": "Start at 0 with 3 points. Each ability may be −1 to +2; lowering one below 0 frees a point.",
    },
    {
        "id": "gm-roll",
        "label": "Rolling (GM)",
        "description": "Rolling is still being adapted for YMIAT—use another method or agree on rolls with your GM.",
        "disabled": True,
    },
]

EQUIPMENT_METHODS = [
    {
        "id": "packages",
        "label": "Class & background equipment",
        "description": "Take the gear listed for your class and background—fastest option at the table.",
    },
    {
        "id": "wealth",
        "label": "Starting wealth",
        "description": "Receive starting gold from your class and buy gear from the equipment lists.",
    },
]


def main() -> None:
    payload = {
        "version": 1,
        "generatedFrom": [
            "scripts/character_options_data.py",
            "scripts/generate-classes-html.py",
            "scripts/class_subclasses_data.py",
        ],
        "rulesOverviewUrl": "rules/characters.html#character-creation-overview",
        "steps": STEPS,
        "conceptArchetypes": CONCEPT_ARCHETYPES,
        "abilityMethods": ABILITY_METHODS,
        "equipmentMethods": EQUIPMENT_METHODS,
        "classes": export_classes(),
        "lineages": export_named_options(LINEAGES, rules_page="lineages"),
        "heritages": export_named_options(HERITAGES, rules_page="heritages"),
        "backgrounds": export_named_options(BACKGROUNDS, rules_page="backgrounds"),
        "heritageRecommendations": build_heritage_recommendations(),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUT} "
        f"({len(payload['classes'])} classes, "
        f"{len(payload['lineages'])} lineages, "
        f"{len(payload['heritages'])} heritages, "
        f"{len(payload['backgrounds'])} backgrounds)"
    )


if __name__ == "__main__":
    main()
