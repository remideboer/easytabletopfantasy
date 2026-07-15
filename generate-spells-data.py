"""
Build assets/spells-data.json from the foundation SRD-derived spell packs.

Source files (foundation/, gitignored drafts) are keyed by 5e class names.
YMIAT classes are mapped onto those tags; Theurge and Witch have no 5e
equivalent, so they're approximated as the union of their closest thematic
lists (Theurge: Wizard+Cleric for Arcane+Divine; Witch: Warlock+Druid for
Wyrd magic) since no explicit spell-list crosswalk exists in the rules text.

Re-run this whenever the foundation spell packs change.
"""
import json
import re

ROOT = r"d:\projecten\dndlite"

SOURCES = [
    f"{ROOT}\\foundation\\easy_tabletop_fantasy_spells_cantrip_and_level1.json",
    f"{ROOT}\\foundation\\easy_tabletop_fantasy_spells_level2_to_9.json",
]

# YMIAT class id -> foundation "classes" tags that count as eligible.
CLASS_MAP = {
    "bard": ["Bard"],
    "cleric": ["Cleric"],
    "druid": ["Druid"],
    "paladin": ["Paladin"],
    "ranger": ["Ranger"],
    "sorcerer": ["Sorcerer"],
    "warlock": ["Warlock"],
    "wizard": ["Wizard"],
    "theurge": ["Wizard", "Cleric"],
    "witch": ["Warlock", "Druid"],
}


def slugify(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def main():
    all_spells = []
    for path in SOURCES:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        for _, entries in doc["spells"].items():
            all_spells.extend(entries)

    out = []
    seen_ids = set()
    for s in all_spells:
        eligible = [cid for cid, tags in CLASS_MAP.items() if any(t in s["classes"] for t in tags)]
        if not eligible:
            continue
        base_id = slugify(s["name"])
        spell_id = base_id
        n = 2
        while spell_id in seen_ids:
            spell_id = f"{base_id}-{n}"
            n += 1
        seen_ids.add(spell_id)
        out.append({
            "id": spell_id,
            "name": s["name"],
            "circle": s["level"],
            "school": s.get("school", ""),
            "classes": eligible,
            "castingTime": s.get("casting_time_easy", ""),
            "range": s.get("range", ""),
            "duration": s.get("duration", ""),
            "components": s.get("components", ""),
            "description": s.get("description_easy", ""),
        })

    out.sort(key=lambda s: (s["circle"], s["name"]))

    dest = f"{ROOT}\\assets\\spells-data.json"
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(out)} spells to {dest}")


if __name__ == "__main__":
    main()
