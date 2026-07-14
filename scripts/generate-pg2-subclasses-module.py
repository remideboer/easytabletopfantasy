#!/usr/bin/env python3
"""Generate pg2_subclasses_data.py from ToV PG2 PDF + progression metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "foundation" / "ToV+Players+Guide+2_Final_PDF_2026.pdf"
OUT = Path(__file__).resolve().parent / "pg2_subclasses_data.py"

# Already implemented in class_subclasses_data.py (BFRD + full PG2)
EXISTING: dict[str, set[str]] = {
    "barbarian": {"berserker", "wild-fury", "chaos", "four-winds", "kraken"},
    "bard": {"lore", "victory"},
    "cleric": {"life", "light", "war"},
    "druid": {"leaf", "shifter", "elementalist", "fey", "stoneheart"},
    "fighter": {"spell-blade", "weapon-master"},
    "artificer": {"alchemist", "armorer", "artillerist", "battle-smith"},
    "monk": {"flickering-dark", "open-hand"},
    "paladin": {"devotion", "justice"},
    "ranger": {"hunter", "pack-master"},
    "rogue": {"enforcer", "thief"},
    "sorcerer": {"chaos", "draconic"},
    "warlock": {"archfey", "fiend", "great-old-one"},
    "wizard": {"battle-mage", "cantrip-adept"},
    "theurge": {"conduit", "illuminary", "source-spinner"},
    "vanguard": {"bulwark", "herald", "marshal"},
    "witch": {"crimson-cord", "night-song", "twilight-soul"},
}

TOV_URL = "https://www.talesofthevaliant.com/"


def adapt_tov(text: str) -> str:
    pairs = [
        (r"\bSTR\b", "FIT"),
        (r"\bDEX\b", "FIT"),
        (r"\bCON\b", "FIT"),
        (r"\bINT\b", "INS"),
        (r"\bWIS\b", "WIL"),
        (r"\bCHA\b", "WIL"),
        ("hit point maximum", "Max Wounds"),
        ("Hit point maximum", "Max Wounds"),
        ("hit points", "Wounds"),
        ("Hit points", "Wounds"),
        ("hit point", "Wound"),
        ("Hit point", "Wound"),
        ("Hit dice", "Recovery Points"),
        ("hit dice", "Recovery Points"),
        ("bonus action", "free action"),
        ("Bonus action", "Free action"),
        ("spell slots", "spell circles"),
        ("Spell slots", "Spell circles"),
        ("spell slot", "spell circle"),
        ("Spell slot", "Spell circle"),
    ]
    out = text
    for old, new in pairs:
        out = out.replace(old, new)
    return out


def html_para(text: str) -> str:
    text = adapt_tov(text.strip())
    text = re.sub(r"\s+", " ", text)
    return f"<p>{text}</p>"


def extract_subclass_meta(text: str) -> list[dict]:
    class_map = {"Mechanist": "artificer"}

    def slug(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

    subs: list[dict] = []
    pattern = (
        r"(Barbarian|Bard|Cleric|Druid|Fighter|Mechanist|Monk|Paladin|Ranger|Rogue|"
        r"Sorcerer|Warlock|Wizard|Theurge|Vanguard|Witch)\s+Subclass:\s*([^\n]+)\n"
    )
    for m in re.finditer(pattern, text):
        cls, name = m.group(1), m.group(2).strip()
        if "Domain" in name:
            name = name.replace(" Domain", "")
        cid = class_map.get(cls, cls.lower())
        start = m.end()
        block = text[start : start + 4000]
        summary_lines = []
        for line in block.split("\n")[:12]:
            stripped = line.strip()
            if not stripped or "Progression" in stripped:
                continue
            if stripped.endswith("Progression") or stripped in ("Features", "Monk Level", "Paladin Level"):
                break
            if re.match(r"^\d+$", stripped):
                continue
            if re.match(r"^\d+(?:st|nd|rd|th)$", stripped):
                continue
            summary_lines.append(stripped)
            if len(summary_lines) >= 3:
                break
        summary = " ".join(summary_lines)[:220]
        prog_m = re.search(
            rf"{re.escape(name)}\s+Progression\n\w+ Level\nFeatures\n"
            r"((?:3rd\n.+?\n)+(?:7th\n.+?\n)?(?:11th\n.+?\n)?(?:15th\n.+?\n)?)",
            block,
        )
        if not prog_m:
            prog_m = re.search(
                r"Progression\n\w+ Level\nFeatures\n"
                r"((?:3rd\n.+?\n)+(?:7th\n.+?\n)?(?:11th\n.+?\n)?(?:15th\n.+?\n)?)",
                block,
            )
        feats: dict[str, str] = {}
        if prog_m:
            prog = prog_m.group(prog_m.lastindex or 1)
            for lvl in ("3rd", "7th", "11th", "15th"):
                fm = re.search(lvl + r"\n(.+?)(?=\n(?:7th|11th|15th|\Z))", prog, re.S)
                if fm:
                    feats[lvl] = re.sub(r"\s+", " ", fm.group(1).strip())
        subs.append(
            {
                "class": cid,
                "class_name": "Artificer" if cls == "Mechanist" else cls,
                "name": name,
                "id": slug(name),
                "summary": summary,
                "features": feats,
            }
        )
    return subs


def split_feature_names(raw: str) -> list[str]:
    if not raw:
        return []
    names: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in raw:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch == "," and depth == 0:
            name = "".join(current).strip()
            if name and not name.endswith(":") and not name.endswith(" Wild"):
                names.append(name)
            current = []
        else:
            current.append(ch)
    name = "".join(current).strip()
    if name and not name.endswith(":") and not name.endswith(" Wild"):
        names.append(name)
    return names


def extract_feature_bodies(text: str) -> dict[str, str]:
    """Map feature title -> body text from class options section."""
    bodies: dict[str, str] = {}
    # Feature blocks: Title\nNd-Level ... Feature\nBody until next Title or Progression
    pattern = re.compile(
        r"^([A-Z][^\n]{2,80})\n"
        r"(?:\d+(?:st|nd|rd|th)-Level[^\n]+\n)?"
        r"((?:(?!^[A-Z][^\n]{2,80}\n(?:\d+(?:st|nd|rd|th)-Level|\w+ Progression))[\s\S])+?)"
        r"(?=^[A-Z][^\n]{2,80}\n|\Z)",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        title = m.group(1).strip()
        body = m.group(2).strip()
        if len(body) < 40 or "Progression" in title:
            continue
        if title in ("Heroic Boons", "Epic Boons", "PLAYER'S GUIDE 2", "CLASS OPTIONS"):
            continue
        bodies[title] = body
    return bodies


def py_str(s: str) -> str:
    return json.dumps(s)


def main() -> None:
    doc = fitz.open(PDF)
    full_text = ""
    for i in range(10, 103):
        full_text += doc[i].get_text() + "\n"
    bodies = extract_feature_bodies(full_text)
    meta = extract_subclass_meta(full_text)

    lines = [
        '#!/usr/bin/env python3',
        '"""ToV Player\'s Guide 2 subclasses not yet inlined in class_subclasses_data.py."""',
        '',
        'from class_subclasses_data import _sf, _sub, _ymiat_level_label',
        '',
        f'TOV_PG2 = {py_str(TOV_URL)}',
        '',
    ]

    fn_blocks: list[str] = []
    by_class: dict[str, list] = {}
    for entry in meta:
        cid = entry["class"]
        sid = entry["id"]
        if sid in EXISTING.get(cid, set()):
            continue
        by_class.setdefault(cid, []).append(entry)

    for cid in sorted(by_class.keys()):
        cname = by_class[cid][0]["class_name"]
        fn_name = f"{cid}_pg2_subclasses"
        fn_lines = [f"def {fn_name}():", f'    cid, cname = {py_str(cid)}, {py_str(cname)}', "    return ["]
        for entry in by_class[cid]:
            sid = entry["id"]
            sname = entry["name"]
            summary = adapt_tov(entry.get("summary") or f"{sname} subclass from ToV Player's Guide 2.")
            fn_lines.append(f"        _sub(")
            fn_lines.append(f"            cid, cname, {py_str(sid)}, {py_str(sname)},")
            fn_lines.append(f"            {py_str(summary)},")
            fn_lines.append("            [")
            feature_lines: list[str] = []
            for lvl in ("3rd", "7th", "11th", "15th"):
                raw = entry.get("features", {}).get(lvl, "")
                for fname in split_feature_names(raw):
                    body_text = bodies.get(fname.split("(")[0].strip(), "")
                    if not body_text:
                        for k, v in bodies.items():
                            if fname.lower().startswith(k.lower()[:12]) or k.lower().startswith(fname.lower()[:12]):
                                body_text = v
                                break
                    if body_text:
                        summary_line = body_text.split("\n")[0][:120]
                        body_html = html_para(body_text[:1200])
                    else:
                        summary_line = f"{fname} — {sname} subclass feature."
                        body_html = html_para(
                            f"{fname}: see Tales of the Valiant Player's Guide 2 ({sname} subclass)."
                        )
                    feature_lines.append(
                        f"                _sf(cid, cname, {py_str(sid)}, {py_str(sname)}, "
                        f"[{py_str(fname)}], _ymiat_level_label({py_str(lvl)}),"
                    )
                    feature_lines.append(f"                    {py_str(summary_line)},")
                    feature_lines.append(f"                    {py_str(body_html)}),")
            if not feature_lines:
                stub_summary = f"{sname} subclass feature from ToV Player's Guide 2."
                stub_body = (
                    f"<p>{sname} subclass features from Tales of the Valiant Player's Guide 2. "
                    "Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell circles).</p>"
                )
                for lvl in ("3rd", "7th", "11th", "15th"):
                    feature_lines.append(
                        f"                _sf(cid, cname, {py_str(sid)}, {py_str(sname)}, "
                        f"[{py_str(sname + ' Feature')}], _ymiat_level_label({py_str(lvl)}),"
                    )
                    feature_lines.append(f"                    {py_str(stub_summary)},")
                    feature_lines.append(f"                    {py_str(stub_body)}),")
            fn_lines.extend(feature_lines)
            fn_lines.append("            ],")
            fn_lines.append("            TOV_PG2,")
            fn_lines.append("        ),")
        fn_lines.append("    ]")
        fn_blocks.append("\n".join(fn_lines))

    lines.extend(fn_blocks)
    lines.extend([
        "",
        "def pg2_only_subclasses():",
        "    groups = [",
    ])
    for cid in sorted(by_class.keys()):
        lines.append(f"        {cid}_pg2_subclasses,")
    lines.extend([
        "    ]",
        "    result = []",
        "    for fn in groups:",
        "        result.extend(fn())",
        "    return result",
        "",
    ])

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(by_class)} classes, {sum(len(v) for v in by_class.values())} subclasses)")


if __name__ == "__main__":
    main()
