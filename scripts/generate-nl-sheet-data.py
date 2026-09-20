#!/usr/bin/env python3
"""Generate assets/nl/*-data.json from nl/rules HTML over EN JSON skeletons.

NL character sheet loads these packs so UI + PDF export use Dutch descriptions.
Mechanical ids/classes/caps stay aligned with EN so stored characters keep working.
"""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
NL_RULES = ROOT / "nl" / "rules"
OUT_DIR = ASSETS / "nl"

NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def slugify(name: str) -> str:
    text = (name or "").lower().strip()
    text = NON_ALNUM_RE.sub("-", text)
    return text.strip("-") or "item"


def strip_html(html: str) -> str:
    text = TAG_RE.sub(" ", html or "")
    text = WS_RE.sub(" ", text)
    return text.strip()


def teaser(html: str, max_len: int = 220) -> str:
    plain = strip_html(html)
    if len(plain) <= max_len:
        return plain
    cut = plain[: max_len - 1].rsplit(" ", 1)[0]
    return cut + "…"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def extract_divs_by_class(html: str, class_token: str) -> list[tuple[int, int, str]]:
    """Return (start, end, html) for each div whose class attribute contains class_token."""
    results: list[tuple[int, int, str]] = []
    needle = 'class="'
    idx = 0
    while True:
        start = html.find("<div", idx)
        if start < 0:
            break
        gt = html.find(">", start)
        if gt < 0:
            break
        open_tag = html[start : gt + 1]
        if needle not in open_tag or class_token not in open_tag:
            idx = gt + 1
            continue
        i = start
        depth = 0
        end = None
        while i < len(html):
            if html.startswith("<div", i):
                depth += 1
                i = html.find(">", i) + 1
                continue
            if html.startswith("</div>", i):
                depth -= 1
                i += 6
                if depth == 0:
                    end = i
                    break
                continue
            i += 1
        if end is None:
            break
        results.append((start, end, html[start:end]))
        idx = end
    return results


def first_attr(html: str, attr: str) -> str | None:
    m = re.search(rf'\b{attr}="([^"]+)"', html)
    return m.group(1) if m else None


def inner_by_class(card: str, class_name: str) -> str:
    m = re.search(
        rf'<div[^>]*class="[^"]*{re.escape(class_name)}[^"]*"[^>]*>([\s\S]*?)</div>',
        card,
        re.I,
    )
    return m.group(1) if m else ""


def text_by_class(card: str, class_name: str, tag: str = "h4") -> str:
    m = re.search(
        rf'<{tag}[^>]*class="[^"]*{re.escape(class_name)}[^"]*"[^>]*>([\s\S]*?)</{tag}>',
        card,
        re.I,
    )
    return strip_html(m.group(1)) if m else ""


def paragraphs_to_text(html: str) -> str:
    parts = []
    for m in re.finditer(r"<p[^>]*>([\s\S]*?)</p>", html or "", re.I):
        t = strip_html(m.group(1))
        if t:
            parts.append(t)
    if parts:
        return "\n\n".join(parts)
    return strip_html(html)


def list_items_to_bullets(html: str) -> str:
    items = [strip_html(m.group(1)) for m in re.finditer(r"<li[^>]*>([\s\S]*?)</li>", html or "", re.I)]
    items = [i for i in items if i]
    if not items:
        return ""
    return "\n".join(f"• {i}" for i in items)


def meta_map(card: str) -> dict[str, str]:
    """Parse .spell-card-meta spans into label -> value (lowercase label keys)."""
    meta_html = inner_by_class(card, "spell-card-meta")
    out: dict[str, str] = {}
    for m in re.finditer(
        r"<span[^>]*>\s*<strong>([^<:]+):</strong>\s*([\s\S]*?)</span>",
        meta_html or "",
        re.I,
    ):
        label = strip_html(m.group(1)).lower()
        value = strip_html(m.group(2))
        if label and value:
            out[label] = value
    return out


def first_em_summary(desc_html: str) -> str:
    m = re.search(r"<em>([\s\S]*?)</em>", desc_html or "", re.I)
    if m:
        return strip_html(m.group(1))
    # fallback: first paragraph
    m2 = re.search(r"<p[^>]*>([\s\S]*?)</p>", desc_html or "", re.I)
    return teaser(m2.group(1), 160) if m2 else teaser(desc_html, 160)


# ---------------------------------------------------------------------------
# Spells
# ---------------------------------------------------------------------------

META_FIELD_ALIASES = {
    "castingTime": ("casttijd", "casting time", "castingtime"),
    "range": ("bereik", "range"),
    "duration": ("duur", "duration"),
    "components": ("componenten", "components"),
    "school": ("school",),
}


def build_nl_spells(en_spells: list[dict], magic_html: str) -> tuple[list[dict], list[str]]:
    cards = extract_divs_by_class(magic_html, "spell-card")
    by_slug: dict[str, str] = {}
    for _, _, card in cards:
        # Skip ability feature cards if any leaked in
        if "ability-feature-card" in card[:120]:
            continue
        name = text_by_class(card, "spell-card-name")
        if not name:
            continue
        by_slug[slugify(name)] = card

    unmatched: list[str] = []
    out: list[dict] = []
    for spell in en_spells:
        row = deepcopy(spell)
        card = by_slug.get(spell["id"]) or by_slug.get(slugify(spell.get("name", "")))
        if not card:
            unmatched.append(spell["id"])
            out.append(row)
            continue
        nl_name = text_by_class(card, "spell-card-name")
        if nl_name:
            row["name"] = nl_name
        desc_html = inner_by_class(card, "spell-card-description")
        desc = paragraphs_to_text(desc_html)
        if desc:
            row["description"] = desc
        meta = meta_map(card)
        for field, aliases in META_FIELD_ALIASES.items():
            for alias in aliases:
                if alias in meta and meta[alias]:
                    row[field] = meta[alias]
                    break
        out.append(row)
    return out, unmatched


# ---------------------------------------------------------------------------
# Talents / lineages / heritages / backgrounds (lineage-item pattern)
# ---------------------------------------------------------------------------

def parse_lineage_items(html: str) -> dict[str, dict]:
    """Map id -> {name, content_html, prerequisite, description}."""
    items: dict[str, dict] = {}
    for _, _, block in extract_divs_by_class(html, "lineage-item"):
        item_id = first_attr(block, "id")
        if not item_id:
            continue
        name = ""
        m_title = re.search(
            r'class="lineage-title"[^>]*>([\s\S]*?)</span>', block, re.I
        )
        if m_title:
            name = strip_html(m_title.group(1))
        content_m = re.search(
            r'<div[^>]*class="[^"]*lineage-content[^"]*"[^>]*>([\s\S]*)</div>\s*$',
            block,
            re.I,
        )
        # lineage-content is not always at end; use simpler search
        content_m = re.search(
            r'<div[^>]*class="[^"]*lineage-content[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>\s*$',
            block,
            re.I,
        )
        if not content_m:
            content_m = re.search(
                r'<div[^>]*class="[^"]*lineage-content[^"]*"[^>]*>([\s\S]*)</div>',
                block,
                re.I,
            )
        content = content_m.group(1) if content_m else ""
        prereq = ""
        m_pr = re.search(
            r"<p>\s*<strong>(?:Voorwaarde|Prerequisite):</strong>\s*([\s\S]*?)</p>",
            content,
            re.I,
        )
        if m_pr:
            prereq = strip_html(m_pr.group(1))
        bullets = list_items_to_bullets(content)
        if not bullets:
            # strip prerequisite paragraph then use remaining text
            cleaned = re.sub(
                r"<p>\s*<strong>(?:Voorwaarde|Prerequisite):</strong>[\s\S]*?</p>",
                "",
                content,
                flags=re.I,
            )
            bullets = paragraphs_to_text(cleaned) or strip_html(cleaned)
        items[item_id] = {
            "id": item_id,
            "name": name,
            "content_html": content,
            "prerequisite": prereq,
            "description": bullets,
            "body": content.strip(),
            "teaser": teaser(content),
        }
    return items


def build_nl_talents(en_talents: list[dict], talents_html: str) -> tuple[list[dict], list[str]]:
    items = parse_lineage_items(talents_html)
    unmatched: list[str] = []
    out: list[dict] = []
    for talent in en_talents:
        row = deepcopy(talent)
        hit = items.get(talent.get("id") or "") or items.get(slugify(talent.get("name", "")))
        if not hit:
            unmatched.append(talent.get("id") or talent.get("name") or "?")
            out.append(row)
            continue
        if hit["name"]:
            row["name"] = hit["name"]
        if hit["prerequisite"] or talent.get("prerequisite"):
            # prefer NL prerequisite when present
            if hit["prerequisite"]:
                row["prerequisite"] = hit["prerequisite"]
        if hit["description"]:
            row["description"] = hit["description"]
        out.append(row)
    return out, unmatched


def overlay_catalog_entries(en_list: list[dict], nl_items: dict[str, dict]) -> tuple[list[dict], list[str]]:
    unmatched: list[str] = []
    out: list[dict] = []
    for entry in en_list:
        row = deepcopy(entry)
        hit = nl_items.get(entry["id"])
        if not hit:
            unmatched.append(entry["id"])
            out.append(row)
            continue
        if hit["name"]:
            row["name"] = hit["name"]
        if hit["body"]:
            row["body"] = hit["body"]
            row["teaser"] = hit["teaser"] or teaser(hit["body"])
            # rebuild trait features from NL body when possible
            features = []
            for match in re.finditer(
                r"<p>\s*<strong>([^<]+?)(?:\.)?</strong>\s*([\s\S]*?)</p>",
                hit["body"],
                re.I,
            ):
                fname = match.group(1).strip().rstrip(".")
                if fname.lower() in {"age", "size", "speed", "languages", "leeftijd", "grootte", "snelheid", "talen"}:
                    continue
                features.append(
                    {
                        "name": fname,
                        "summary": teaser(match.group(2), 160),
                    }
                )
            if features:
                row["features"] = features
        out.append(row)
    return out, unmatched


# ---------------------------------------------------------------------------
# Class abilities from nl/rules/class-abilities/*.html
# ---------------------------------------------------------------------------

def parse_ability_cards(html: str) -> dict[str, dict]:
    """Map card id / slug(name) -> {name, summary, description}."""
    cards: dict[str, dict] = {}
    for _, _, card in extract_divs_by_class(html, "ability-feature-card"):
        card_id = first_attr(card, "id") or ""
        name = text_by_class(card, "spell-card-name")
        desc_html = inner_by_class(card, "spell-card-description")
        summary = first_em_summary(desc_html)
        description = paragraphs_to_text(desc_html)
        entry = {
            "id": card_id,
            "name": name,
            "summary": summary,
            "description": description,
        }
        if card_id:
            cards[card_id] = entry
        if name:
            cards[slugify(name)] = entry
            # also bare name key for exact match
            cards[name.lower()] = entry
    return cards


def match_ability(cards: dict[str, dict], name: str) -> dict | None:
    if not name:
        return None
    key = slugify(name)
    if key in cards:
        return cards[key]
    # strip common prefixes like "Bardic Performance: "
    if ":" in name:
        tail = name.split(":", 1)[1].strip()
        hit = cards.get(slugify(tail)) or cards.get(tail.lower())
        if hit:
            return hit
    return cards.get(name.lower())


def overlay_class_abilities(creator: dict) -> list[str]:
    unmatched: list[str] = []
    for cls in creator.get("classes") or []:
        cid = cls.get("id")
        path = NL_RULES / "class-abilities" / f"{cid}.html"
        if not path.exists():
            unmatched.append(f"class-file:{cid}")
            continue
        cards = parse_ability_cards(path.read_text(encoding="utf-8"))
        for ab in cls.get("abilities") or []:
            hit = match_ability(cards, ab.get("name", ""))
            if not hit:
                unmatched.append(f"{cid}/{ab.get('name')}")
                continue
            if hit["name"]:
                ab["name"] = hit["name"]
            if hit["summary"]:
                ab["summary"] = hit["summary"]
        for sub in cls.get("subclasses") or []:
            for feat in sub.get("features") or []:
                hit = match_ability(cards, feat.get("name", ""))
                if not hit:
                    unmatched.append(f"{cid}/{sub.get('id')}/{feat.get('name')}")
                    continue
                if hit["name"]:
                    feat["name"] = hit["name"]
                if hit["summary"]:
                    feat["summary"] = hit["summary"]
    return unmatched


def main() -> int:
    en_spells = load_json(ASSETS / "spells-data.json")
    en_talents = load_json(ASSETS / "talents-data.json")
    en_creator = load_json(ASSETS / "character-creator-data.json")

    magic_html = (NL_RULES / "magic.html").read_text(encoding="utf-8")
    talents_html = (NL_RULES / "talents.html").read_text(encoding="utf-8")
    lineages_html = (NL_RULES / "lineages.html").read_text(encoding="utf-8")
    heritages_html = (NL_RULES / "heritages.html").read_text(encoding="utf-8")
    backgrounds_html = (NL_RULES / "backgrounds.html").read_text(encoding="utf-8")

    nl_spells, miss_spells = build_nl_spells(en_spells, magic_html)
    nl_talents, miss_talents = build_nl_talents(en_talents, talents_html)

    creator = deepcopy(en_creator)
    creator["locale"] = "nl"
    creator["generatedFrom"] = list(creator.get("generatedFrom") or []) + [
        "scripts/generate-nl-sheet-data.py",
        "nl/rules/*.html",
    ]

    nl_lineages, miss_lin = overlay_catalog_entries(
        creator.get("lineages") or [], parse_lineage_items(lineages_html)
    )
    nl_heritages, miss_her = overlay_catalog_entries(
        creator.get("heritages") or [], parse_lineage_items(heritages_html)
    )
    nl_backgrounds, miss_bg = overlay_catalog_entries(
        creator.get("backgrounds") or [], parse_lineage_items(backgrounds_html)
    )
    creator["lineages"] = nl_lineages
    creator["heritages"] = nl_heritages
    creator["backgrounds"] = nl_backgrounds

    miss_abil = overlay_class_abilities(creator)

    write_json(OUT_DIR / "spells-data.json", nl_spells)
    write_json(OUT_DIR / "talents-data.json", nl_talents)
    write_json(OUT_DIR / "character-creator-data.json", creator)

    def report(label: str, missing: list[str]) -> None:
        print(f"{label}: {len(missing)} unmatched")
        for item in missing[:12]:
            print(f"  - {item}")
        if len(missing) > 12:
            print(f"  … +{len(missing) - 12} more")

    print(f"Wrote {OUT_DIR / 'spells-data.json'} ({len(nl_spells)} spells)")
    print(f"Wrote {OUT_DIR / 'talents-data.json'} ({len(nl_talents)} talents)")
    print(f"Wrote {OUT_DIR / 'character-creator-data.json'}")
    report("spells", miss_spells)
    report("talents", miss_talents)
    report("lineages", miss_lin)
    report("heritages", miss_her)
    report("backgrounds", miss_bg)
    report("abilities", miss_abil)
    return 0


if __name__ == "__main__":
    sys.exit(main())
