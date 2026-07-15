"""
Build assets/spells-data.json by scraping the spell cards already published on
rules/magic.html - the site's authoritative, YMIAT-adapted spell text (Wound-
based damage wording, "Moment" casting times, etc.), rather than the raw SRD
drafts in foundation/. magic.html tags spells by 5e class name; YMIAT classes
are mapped onto those tags. Theurge and Witch have no 5e equivalent, so
they're approximated as the union of their closest thematic lists (Theurge:
Wizard+Cleric for Arcane+Divine; Witch: Warlock+Druid for Wyrd magic) since no
explicit spell-list crosswalk exists in the rules text.

Re-run this whenever rules/magic.html's spell cards change.
"""
import json
import re
from bs4 import BeautifulSoup

ROOT = r"d:\projecten\dndlite"
SOURCE = f"{ROOT}\\rules\\magic.html"
DEST = f"{ROOT}\\assets\\spells-data.json"

# YMIAT class id -> 5e class tags (as used in magic.html's "Classes:" line) that count as eligible.
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

LEVEL_WORD_TO_CIRCLE = {"cantrip": 0}


def slugify(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def clean_text(text):
    # get_text(" ", ...) inserts a space at every tag boundary, including
    # right before punctuation that followed a <strong> run (e.g. "Wound .").
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def parse_circle(level_text):
    level_text = level_text.strip().lower()
    if level_text in LEVEL_WORD_TO_CIRCLE:
        return LEVEL_WORD_TO_CIRCLE[level_text]
    m = re.match(r"(\d+)", level_text)
    if not m:
        raise ValueError(f"Could not parse spell level: {level_text!r}")
    return int(m.group(1))


def meta_field(meta_div, label):
    for span in meta_div.select("span"):
        strong = span.find("strong")
        if strong and strong.get_text(strip=True).rstrip(":") == label:
            text = span.get_text(" ", strip=True)
            return clean_text(text[len(strong.get_text(strip=True)):])
    return ""


def main():
    with open(SOURCE, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    out = []
    seen_ids = set()
    for card in soup.select(".spell-card"):
        name = card.select_one(".spell-card-name").get_text(strip=True)
        circle = parse_circle(card.select_one(".spell-card-level").get_text())
        meta = card.select_one(".spell-card-meta")
        classes_text = meta_field(meta, "Classes")
        card_classes = [c.strip() for c in classes_text.split(",") if c.strip()]

        eligible = [cid for cid, tags in CLASS_MAP.items() if any(t in card_classes for t in tags)]
        if not eligible:
            continue

        desc_div = card.select_one(".spell-card-description")
        paragraphs = [clean_text(p.get_text(" ")) for p in desc_div.select("p")] if desc_div else []
        description = "\n\n".join(p for p in paragraphs if p)

        base_id = slugify(name)
        spell_id = base_id
        n = 2
        while spell_id in seen_ids:
            spell_id = f"{base_id}-{n}"
            n += 1
        seen_ids.add(spell_id)

        out.append({
            "id": spell_id,
            "name": name,
            "circle": circle,
            "school": meta_field(meta, "School"),
            "classes": eligible,
            "castingTime": meta_field(meta, "Casting Time"),
            "range": meta_field(meta, "Range"),
            "duration": meta_field(meta, "Duration"),
            "components": meta_field(meta, "Components"),
            "description": description,
        })

    out.sort(key=lambda s: (s["circle"], s["name"]))

    with open(DEST, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(out)} spells to {DEST}")


if __name__ == "__main__":
    main()
