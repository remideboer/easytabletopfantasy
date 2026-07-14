#!/usr/bin/env python3
"""Generate one class ability HTML page per class (with anchor sections)."""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from class_abilities_data import all_abilities, build_registry
from class_subclasses_data import all_subclass_features, get_subclasses_by_class

ROOT = SCRIPT_DIR.parent
OUT_DIR = ROOT / "rules" / "class-abilities"

CLASS_ORDER = [
    "artificer", "barbarian", "bard", "cleric", "druid", "fighter",
    "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard",
]


def render_ability_card(ability: dict) -> str:
    meta_parts = []
    if ability.get("subclass_name"):
        meta_parts.append(f'<span><strong>Subclass:</strong> {ability["subclass_name"]}</span>')
    if ability.get("action"):
        meta_parts.append(f'<span><strong>Action:</strong> {ability["action"]}</span>')
    meta_html = ""
    if meta_parts:
        meta_html = f'<div class="spell-card-meta">{"".join(meta_parts)}</div>\n'

    return f"""<div class="spell-card ability-feature-card" id="{ability["anchor"]}">
  <div class="spell-card-header">
    <h4 class="spell-card-name">{ability["name"]}</h4>
    <span class="spell-card-level">{ability["level"]}</span>
  </div>
  {meta_html}  <div class="spell-card-description">
    <p><em>{ability["summary"]}</em></p>
    {ability["body"]}
  </div>
</div>
"""


def render_subclass_block(subclass: dict) -> str:
    cards = "".join(render_ability_card(feat) for feat in subclass["features"])

    source = ""
    if subclass.get("bfrd_url"):
        source = (
            f'<p class="source-note">Adapted from '
            f'<a href="{subclass["bfrd_url"]}" rel="noopener">BFRD {subclass["subclass_name"]}</a>.</p>'
        )

    return f"""<div class="subclass-group" id="{subclass["subclass_id"]}">
  <h3 class="subclass-name">{subclass["subclass_name"]}</h3>
  <p class="subclass-summary">{subclass["summary"]}</p>
  <div class="spells-container">
{cards}
  </div>
  {source}
</div>
"""


def render_class_page(class_id: str, class_name: str, abilities: list, subclasses: list) -> str:
    seen = set()
    sections = []
    toc = []

    for ability in abilities:
        if ability["anchor"] in seen:
            continue
        seen.add(ability["anchor"])
        sections.append(render_ability_card(ability))
        toc.append(
            f'<li><a href="#{ability["anchor"]}">{ability["name"]}</a> '
            f'<span class="text-muted">({ability["level"]})</span></li>'
        )

    subclass_blocks = []
    if subclasses:
        toc.append('<li><a href="#subclasses">Subclass Features</a></li>')
        for i, sub in enumerate(subclasses):
            toc.append(
                f'<li class="toc-sub"><a href="#{sub["subclass_id"]}">{sub["subclass_name"]}</a></li>'
            )
            for feat in sub["features"]:
                if feat["anchor"] not in seen:
                    seen.add(feat["anchor"])
                toc.append(
                    f'<li class="toc-sub toc-feature"><a href="#{feat["anchor"]}">{feat["name"]}</a> '
                    f'<span class="text-muted">({feat["level"]})</span></li>'
                )
            subclass_blocks.append(render_subclass_block(sub))
            if i < len(subclasses) - 1:
                subclass_blocks.append('<hr class="subclass-divider" />')

    toc_html = "\n".join(toc)
    class_features_html = ""
    if sections:
        class_features_html = f"""<section class="ability-features-section" id="class-features">
  <h2>Class Features</h2>
  <div class="spells-container">
{"".join(sections)}
  </div>
</section>
"""

    subclass_html = ""
    if subclass_blocks:
        subclass_html = (
            '<hr class="ability-section-divider" id="subclasses" />\n'
            '<section class="ability-features-section ability-features-subclasses">\n'
            '<h2>Subclass Features</h2>\n'
            '<p class="subclasses-intro">Choose your subclass at <strong>2nd level</strong>. '
            'Subclass features arrive at <strong>2nd, 4th, 6th, and 8th</strong> level.</p>\n'
            + "\n".join(subclass_blocks)
            + "\n</section>\n"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{class_name} Abilities | YMIAT</title>
<meta name="description" content="Full rules for every {class_name} class and subclass feature in You-Meet-In-A-Tavern (YMIAT)." />
<link rel="canonical" href="rules/class-abilities/{class_id}.html" />
<link rel="stylesheet" href="../../assets/styles.css" />
<script src="../../assets/includes.js"></script>
</head>
<body>
<header data-include="nav"></header>
<main>
  <h1>{class_name} Abilities</h1>
  <div class="content">
    <p class="lede">Full rules for every {class_name} feature and subclass, adapted from the <a href="https://bfrd.net/classes/" rel="noopener">Black Flag Reference Document</a> for YMIAT 10-level play.</p>
    <p><a href="../classes.html#{class_id}">← Back to {class_name}</a> · <a href="index.html#{class_id}">All classes</a></p>
    <nav class="ability-toc toc" aria-label="{class_name} abilities">
      <h2 id="contents">On this page</h2>
      <ul>
{toc_html}
      </ul>
    </nav>
{class_features_html}
{subclass_html}
    <p class="source-note"><a href="../classes.html#{class_id}">← Back to {class_name}</a></p>
  </div>
</main>
<footer class="legal" data-include="footer"></footer>
<script src="../../assets/site.js"></script>
</body>
</html>
"""


def render_index(by_class: dict, subclasses_by_class: dict) -> str:
    sections = []
    for class_id in CLASS_ORDER:
        abilities = by_class.get(class_id, [])
        subclasses = subclasses_by_class.get(class_id, [])
        if not abilities and not subclasses:
            continue
        class_name = (
            abilities[0]["class_name"]
            if abilities
            else subclasses[0]["class_name"]
        )
        sections.append(f'<h2 id="{class_id}"><a href="{class_id}.html">{class_name}</a></h2>')
        sections.append("<h3>Class Features</h3><ul>")
        seen = set()
        for ability in abilities:
            if ability["anchor"] in seen:
                continue
            seen.add(ability["anchor"])
            sections.append(
                f'<li><a href="{class_id}.html#{ability["anchor"]}">{ability["name"]}</a> '
                f'<span class="text-muted">({ability["level"]})</span></li>'
            )
        sections.append("</ul>")
        if subclasses:
            sections.append("<h3>Subclasses</h3><ul>")
            for sub in subclasses:
                sections.append(
                    f'<li><a href="{class_id}.html#{sub["subclass_id"]}">{sub["subclass_name"]}</a>'
                )
                sections.append("<ul>")
                for feat in sub["features"]:
                    sections.append(
                        f'<li><a href="{class_id}.html#{feat["anchor"]}">{feat["name"]}</a> '
                        f'<span class="text-muted">({feat["level"]})</span></li>'
                    )
                sections.append("</ul></li>")
            sections.append("</ul>")

    body = "\n".join(sections)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Class Abilities | YMIAT</title>
<meta name="description" content="All class and subclass feature abilities for You-Meet-In-A-Tavern (YMIAT)." />
<link rel="canonical" href="rules/class-abilities/index.html" />
<link rel="stylesheet" href="../../assets/styles.css" />
<script src="../../assets/includes.js"></script>
</head>
<body>
<header data-include="nav"></header>
<main>
  <h1>Class Abilities</h1>
  <div class="content">
    <p class="lede">Full rules for every class and subclass feature, adapted from the <a href="https://bfrd.net/classes/" rel="noopener">Black Flag Reference Document</a> for YMIAT 10-level play. One page per class.</p>
    <p><a href="../classes.html">← Back to Classes</a></p>
    {body}
  </div>
</main>
<footer class="legal" data-include="footer"></footer>
<script src="../../assets/site.js"></script>
</body>
</html>
"""


def cleanup_stale_files(keep_names: set) -> int:
    removed = 0
    for path in OUT_DIR.glob("*.html"):
        if path.name not in keep_names:
            path.unlink()
            removed += 1
    return removed


def main():
    abilities = all_abilities()
    subclass_features = all_subclass_features()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    by_class = {}
    for ability in abilities:
        by_class.setdefault(ability["class_id"], []).append(ability)

    subclasses_by_class = get_subclasses_by_class()

    keep_names = {"index.html"}
    for class_id in CLASS_ORDER:
        class_abilities = by_class.get(class_id, [])
        class_subclasses = subclasses_by_class.get(class_id, [])
        if not class_abilities and not class_subclasses:
            continue
        class_name = (
            class_abilities[0]["class_name"]
            if class_abilities
            else class_subclasses[0]["class_name"]
        )
        filename = f"{class_id}.html"
        keep_names.add(filename)
        path = OUT_DIR / filename
        path.write_text(
            render_class_page(class_id, class_name, class_abilities, class_subclasses),
            encoding="utf-8",
        )

    index_path = OUT_DIR / "index.html"
    index_path.write_text(render_index(by_class, subclasses_by_class), encoding="utf-8")

    removed = cleanup_stale_files(keep_names)
    registry = build_registry(abilities + subclass_features)
    print(f"Wrote {len(keep_names) - 1} class ability pages to {OUT_DIR}")
    print(f"Subclass features: {len(subclass_features)}")
    print(f"Removed {removed} stale pages")
    print(f"Registry entries: {len(registry)}")


if __name__ == "__main__":
    main()
