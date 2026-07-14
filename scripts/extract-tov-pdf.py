#!/usr/bin/env python3
"""
Extract Tales of the Valiant Player's Guide PDFs to markdown.

Output: foundation/tov-extract/
  README.md
  tov-2026-options/     — Class Options supplement (TOC-split)
  tov-2024-update/      — Full 2024 update (chapter-split)
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
FOUNDATION = ROOT / "foundation"
OUT = FOUNDATION / "tov-extract"

PDF_2026 = FOUNDATION / "ToV+Players+Guide+2_Final_PDF_2026.pdf"
PDF_2024 = FOUNDATION / "ToV_Players_Guide_2024_Update.pdf"

CHAPTERS_2024 = [
    ("introduction", "Introduction", 1, 10),
    ("01-character-creation", "Character Creation & Leveling", 11, 20),
    ("02-classes", "Character Classes", 21, 104),
    ("03-lineages-heritages", "Lineages & Heritages", 105, 116),
    ("04-backgrounds-talents", "Backgrounds & Talents", 117, 132),
    ("05-equipment-magic-items", "Equipment & Magic Items", 133, 202),
    ("06-playing-the-game", "Playing the Game", 203, 238),
    ("07-spellcasting", "Spellcasting", 239, 384),
]

CLASS_PAGES_2024 = [
    ("Barbarian", 23),
    ("Bard", 28),
    ("Cleric", 33),
    ("Druid", 40),
    ("Fighter", 47),
    ("Mechanist", 53),
    ("Monk", 61),
    ("Paladin", 66),
    ("Ranger", 72),
    ("Rogue", 78),
    ("Sorcerer", 82),
    ("Warlock", 91),
    ("Wizard", 99),
]

SECTIONS_2026 = {
    "introduction": ("Introduction", 9, 10),
    "class-options": ("Class Options", 11, 103),
    "lineages-heritages": ("Lineages & Heritages", 104, 122),
    "backgrounds-talents": ("Backgrounds & Talents", 123, 136),
    "equipment-magic-items": ("Equipment & Magic Items", 137, 177),
    "spellcasting": ("Spellcasting", 178, 244),
    "expanded-rules": ("Expanded Rules", 245, 281),
    "appendix-tables": ("Appendix: Tables", 282, 291),
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-") or "section"


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def page_to_markdown(page: fitz.Page, page_num: int) -> str:
    """Convert one PDF page to markdown with basic heading detection."""
    blocks = page.get_text("dict").get("blocks", [])
    parts: list[str] = []

    for block in blocks:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(span.get("text", "") for span in spans)
            text = text.replace("\u0000", "").strip()
            if not text:
                continue
            if text in {"PLAYER'S GUIDE", "PLAYER'S GUIDE 2"}:
                continue
            if re.fullmatch(r"\d+", text):
                continue

            max_size = max(span.get("size", 0) for span in spans)
            bold = any("Bold" in span.get("font", "") for span in spans)

            if max_size >= 15:
                parts.append(f"## {text}")
            elif max_size >= 12 or (bold and max_size >= 10 and len(text) < 90):
                parts.append(f"### {text}")
            elif text.isupper() and 4 < len(text) < 80 and max_size >= 9:
                parts.append(f"#### {text}")
            else:
                parts.append(text)

    body = clean_text("\n\n".join(parts))
    if not body:
        return f"<!-- page {page_num}: no extractable text -->\n"
    return f"<!-- page {page_num} -->\n\n{body}"


def pages_range_to_markdown(doc: fitz.Document, start_page: int, end_page: int) -> str:
    """Extract inclusive 1-based page range to markdown."""
    chunks: list[str] = []
    start_idx = max(0, start_page - 1)
    end_idx = min(doc.page_count - 1, end_page - 1)
    for page_idx in range(start_idx, end_idx + 1):
        chunks.append(page_to_markdown(doc[page_idx], page_idx + 1))
    return clean_text("\n\n---\n\n".join(chunks))


def write_markdown(path: Path, title: str, source: str, body: str, meta: dict | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {title}",
        "",
        f"> **Source:** {source}",
    ]
    if meta:
        for key, value in meta.items():
            lines.append(f"> **{key}:** {value}")
    lines.extend(["", body, ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def toc_to_markdown(toc: list[list], title: str) -> str:
    lines = [f"# {title}", ""]
    for level, heading, page in toc:
        indent = "  " * (level - 1)
        lines.append(f"{indent}- [{heading}](#page-{page}) (p{page})")
    lines.append("")
    return "\n".join(lines)


def split_toc_level2(doc: fitz.Document, toc: list[list], parent: str) -> list[tuple[str, str, int, int]]:
    """Return (slug, title, start_page, end_page) for level-2 items under parent."""
    entries = [(lvl, title, page) for lvl, title, page in toc]
    parent_idx = next(i for i, (_, title, _) in enumerate(entries) if title == parent)
    parent_page = entries[parent_idx][2]

    siblings: list[tuple[str, int]] = []
    for lvl, title, page in entries[parent_idx + 1 :]:
        if lvl == 1:
            break
        if lvl == 2:
            siblings.append((title, page))

    sections: list[tuple[str, str, int, int]] = []
    for i, (title, start) in enumerate(siblings):
        end = siblings[i + 1][1] - 1 if i + 1 < len(siblings) else None
        if end is None:
            # Until next level-1 section
            for lvl, next_title, next_page in entries[parent_idx + 1 :]:
                if lvl == 1 and next_title != parent:
                    end = next_page - 1
                    break
            if end is None:
                end = doc.page_count
        sections.append((slugify(title), title, start, end))
    return sections


def trim_supplement_class(body: str, class_title: str) -> str:
    """Drop bleed-over from previous PDF spread (2026 options supplement only)."""
    markers = [
        f"## {class_title} Subclasses",
        f"### {class_title} Subclass:",
        f"## {class_title} Boons",
        f"### {class_title} Boon",
    ]
    for marker in markers:
        idx = body.find(marker)
        if idx != -1:
            return body[idx:].lstrip()
    return body


def detect_class_starts_2024(doc: fitz.Document) -> list[tuple[str, int]]:
    """Return (class name, start page) using the printed TOC page numbers."""
    return list(CLASS_PAGES_2024)


def extract_2026() -> dict:
    doc = fitz.open(PDF_2026)
    out_dir = OUT / "tov-2026-options"
    source = PDF_2026.name

    write_markdown(
        out_dir / "00-toc.md",
        "Table of Contents",
        source,
        toc_to_markdown(doc.get_toc(), "ToV Player's Guide 2 — Table of Contents"),
    )

    stats = {"files": 1, "pages": doc.page_count}

    for slug, (title, start, end) in SECTIONS_2026.items():
        body = pages_range_to_markdown(doc, start, end)
        write_markdown(
            out_dir / f"{slug}.md",
            title,
            source,
            body,
            {"pages": f"{start}–{end}"},
        )
        stats["files"] += 1

    class_dir = out_dir / "class-options"
    for class_slug, class_title, start, end in split_toc_level2(doc, doc.get_toc(), "Class Options"):
        body = trim_supplement_class(pages_range_to_markdown(doc, start, end), class_title)
        write_markdown(
            class_dir / f"{class_slug}.md",
            class_title,
            source,
            body,
            {"pages": f"{start}–{end}"},
        )
        stats["files"] += 1

    doc.close()
    return stats


def extract_2024() -> dict:
    doc = fitz.open(PDF_2024)
    out_dir = OUT / "tov-2024-update"
    source = PDF_2024.name
    stats = {"files": 0, "pages": doc.page_count}

    write_markdown(
        out_dir / "00-full-text.md",
        "Full Text (all pages)",
        source,
        pages_range_to_markdown(doc, 1, doc.page_count),
        {"pages": f"1–{doc.page_count}"},
    )
    stats["files"] += 1

    for slug, title, start, end in CHAPTERS_2024:
        body = pages_range_to_markdown(doc, start, end)
        write_markdown(
            out_dir / f"{slug}.md",
            title,
            source,
            body,
            {"pages": f"{start}–{end}"},
        )
        stats["files"] += 1

    class_dir = out_dir / "classes"
    class_starts = detect_class_starts_2024(doc)
    for i, (class_name, start) in enumerate(class_starts):
        end = class_starts[i + 1][1] - 1 if i + 1 < len(class_starts) else 104
        body = pages_range_to_markdown(doc, start, end)
        write_markdown(
            class_dir / f"{slugify(class_name)}.md",
            class_name,
            source,
            body,
            {"pages": f"{start}–{end}"},
        )
        stats["files"] += 1

    doc.close()
    return stats


def write_readme(stats_2026: dict, stats_2024: dict) -> None:
    readme = textwrap.dedent(
        f"""\
        # Tales of the Valiant — PDF Extract

        Machine-readable markdown extracted from the ToV Player's Guide PDFs for YMIAT
        class, subclass, background, and feature work.

        ## Sources

        | Folder | PDF | Pages | Files |
        |--------|-----|-------|-------|
        | `tov-2026-options/` | `{PDF_2026.name}` | {stats_2026['pages']} | {stats_2026['files']} |
        | `tov-2024-update/` | `{PDF_2024.name}` | {stats_2024['pages']} | {stats_2024['files']} |

        ## Layout

        ### `tov-2026-options/` (Player's Guide 2 — options supplement)

        Focus: **new subclasses, boons, lineages, backgrounds, talents, equipment, spells**.

        - `00-toc.md` — embedded PDF table of contents
        - `introduction.md`, `class-options.md`, `lineages-heritages.md`, … — major sections
        - `class-options/*.md` — one file per class (Barbarian, Bard, … Wizard; includes subclasses & boons)

        **Note:** Theurge, Vanguard, and Witch appear only in the 2026 supplement, not the 2024 core update.

        ### `tov-2024-update/` (2024 core update)

        Focus: **full class rules, progression tables, core backgrounds**.

        - `00-full-text.md` — complete extract (search / reference)
        - `01-character-creation.md` … `07-spellcasting.md` — chapter splits
        - `classes/*.md` — per-class extracts from Chapter 2

        ## Regenerate

        ```bash
        python scripts/extract-tov-pdf.py
        ```

        ## Notes

        - Extraction uses PyMuPDF text + font-size heuristics for headings (`##`, `###`, `####`).
        - Tables and multi-column layout may need manual cleanup.
        - Page markers (`<!-- page N -->`) help trace content back to the PDF.
        - This folder lives under `foundation/` (gitignored) — local reference only.
        """
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    if not PDF_2026.exists():
        raise SystemExit(f"Missing PDF: {PDF_2026}")
    if not PDF_2024.exists():
        raise SystemExit(f"Missing PDF: {PDF_2024}")

    print("Extracting ToV 2026 options PDF...")
    stats_2026 = extract_2026()
    print(f"  -> {stats_2026['files']} files")

    print("Extracting ToV 2024 update PDF...")
    stats_2024 = extract_2024()
    print(f"  -> {stats_2024['files']} files")

    write_readme(stats_2026, stats_2024)
    print(f"Done. Output: {OUT}")


if __name__ == "__main__":
    main()
