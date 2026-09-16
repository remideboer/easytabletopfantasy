#!/usr/bin/env python3
"""Copy live English HTML into nl/ with path and lang fixes.

Usage (from repo root):
  python i18n/adapters/static-mirror/mirror_paths.py
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
NL = ROOT / "nl"

# Live site HTML only (skip foundation, includes fragments, scripts, nl itself)
SKIP_DIR_NAMES = {
    "foundation",
    "nl",
    "i18n",
    "scripts",
    "node_modules",
    ".git",
    "includes",
    "data",
    "assets",
}


def en_depth(rel: Path) -> int:
    """Directory depth of an English page relative to site root."""
    return len(rel.parts) - 1


def rewrite_html(html: str, depth: int) -> str:
    """Add one ../ for asset/includes paths; set lang=nl; tweak inLanguage."""
    # lang
    html = re.sub(r'(<html\b[^>]*\blang=")en(")', r'\1nl\2', html, count=1, flags=re.I)
    if re.search(r"<html\b", html, re.I) and not re.search(r'<html\b[^>]*\blang=', html, re.I):
        html = re.sub(r"<html\b", '<html lang="nl"', html, count=1, flags=re.I)

    html = html.replace('"inLanguage": "en"', '"inLanguage": "nl"')
    html = html.replace('"inLanguage":"en"', '"inLanguage":"nl"')

    # Asset / script path prefixes used on EN pages:
    # depth 0: assets/... or href="assets/
    # depth 1: ../assets/
    # depth 2: ../../assets/
    en_prefix = "../" * depth
    nl_prefix = "../" * (depth + 1)

    def bump(match: re.Match) -> str:
        quote = match.group(1)
        path = match.group(2)
        # Already has enough ../ for nl? Detect absolute-ish
        if path.startswith("/") or path.startswith("http"):
            return match.group(0)
        # Only rewrite paths that point at shared assets or root tools
        if not (
            path.startswith(en_prefix + "assets/")
            or path == en_prefix + "assets/includes.js"
            or path.startswith(en_prefix + "assets/")
            or (depth == 0 and path.startswith("assets/"))
        ):
            # Also catch site.js etc under assets
            return match.group(0)
        # Replace leading en_prefix with nl_prefix
        if depth == 0 and path.startswith("assets/"):
            return f"{quote}{nl_prefix}{path}{quote}"
        if path.startswith(en_prefix):
            return f"{quote}{nl_prefix}{path[len(en_prefix):]}{quote}"
        return match.group(0)

    # href/src with relative assets
    pattern = re.compile(
        r"""(?P<attr>\b(?:href|src)=)(?P<q>["'])(?P<path>(?:\.\./)*assets/[^"']+)(?P=q)"""
    )

    def bump_assets(m: re.Match) -> str:
        path = m.group("path")
        q = m.group("q")
        attr = m.group("attr")
        # count existing ../
        ups = 0
        rest = path
        while rest.startswith("../"):
            ups += 1
            rest = rest[3:]
        if not rest.startswith("assets/"):
            return m.group(0)
        # EN depth ups should equal depth; NL needs depth+1
        new_ups = depth + 1
        return f"{attr}{q}{'../' * new_ups}{rest}{q}"

    html = pattern.sub(bump_assets, html)

    # Shared data/ at site root (e.g. monsters_data.json)
    def bump_data(m: re.Match) -> str:
        path = m.group("path")
        q = m.group("q")
        attr = m.group("attr")
        ups = 0
        rest = path
        while rest.startswith("../"):
            ups += 1
            rest = rest[3:]
        if not rest.startswith("data/"):
            return m.group(0)
        new_ups = depth + 1
        return f"{attr}{q}{'../' * new_ups}{rest}{q}"

    data_pattern = re.compile(
        r"""(?P<attr>\b(?:href|src)=)(?P<q>["'])(?P<path>(?:\.\./)*data/[^"']+)(?P=q)"""
    )
    html = data_pattern.sub(bump_data, html)
    # Also inline fetch('../data/...') in scripts
    html = re.sub(
        rf"fetch\((['\"])((?:\.\./){{{depth}})data/)",
        lambda m: f"fetch({m.group(1)}{'../' * (depth + 1)}data/",
        html,
    )

    # hreflang pair (insert after charset/viewport if missing)
    if 'hreflang="nl"' not in html and 'hreflang="en"' not in html:
        # sibling link placeholder — concrete href filled per file below
        pass

    return html


def add_hreflang(html: str, en_href: str, nl_href: str) -> str:
    links = (
        f'<link rel="alternate" hreflang="en" href="{en_href}" />\n'
        f'<link rel="alternate" hreflang="nl" href="{nl_href}" />\n'
        f'<link rel="alternate" hreflang="x-default" href="{en_href}" />\n'
    )
    if "hreflang=" in html:
        return html
    return re.sub(r"(<head[^>]*>)", r"\1\n" + links, html, count=1, flags=re.I)


def iter_en_html() -> list[Path]:
    files = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIR_NAMES for part in rel.parts):
            continue
        files.append(p)
    return sorted(files)


def main() -> None:
    if NL.exists():
        shutil.rmtree(NL)
    NL.mkdir(parents=True)

    count = 0
    for src in iter_en_html():
        rel = src.relative_to(ROOT)
        dest = NL / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        depth = en_depth(rel)
        html = src.read_text(encoding="utf-8")
        html = rewrite_html(html, depth)

        # hreflang: relative from nl page to en twin and self
        ups = "../" * (depth + 1)
        en_href = ups + rel.as_posix()
        nl_href = rel.name if depth == 0 else rel.as_posix()  # same-folder relative messy
        # From nl/rel, self is fine as filename or relative path within nl
        # Use root-absolute-ish relative from this file:
        self_rel = rel.as_posix()
        # From dest file, link to EN: go up depth+1 then into rel
        en_from_nl = "../" * (depth + 1) + self_rel
        # EN alternate from NL page
        # NL alternate can be the current path relative — use ./file for same dir
        nl_self = dest.name
        html = add_hreflang(html, en_from_nl, nl_self)

        dest.write_text(html, encoding="utf-8")
        count += 1

    print(f"Mirrored {count} HTML files into {NL}")


if __name__ == "__main__":
    main()
