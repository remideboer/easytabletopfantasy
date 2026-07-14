#!/usr/bin/env python3
"""Generate nested Characters dropdown for assets/includes.js."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from ability_utils import slugify
from character_options_data import BACKGROUNDS, HERITAGES, LINEAGES, TALENTS
from class_subclasses_data import get_subclasses_by_class


def _load_classes_module():
    path = SCRIPT_DIR / "generate-classes-html.py"
    spec = importlib.util.spec_from_file_location("generate_classes_html", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_gch = _load_classes_module()
CLASSES = _gch.CLASSES
CLASS_ORDER = [
    "artificer", "barbarian", "bard", "cleric", "druid", "fighter",
    "monk", "paladin", "ranger", "rogue", "sorcerer", "theurge",
    "vanguard", "warlock", "witch", "wizard",
]

INCLUDES_PATH = ROOT / "assets" / "includes.js"
BEGIN_MARKER = "// BEGIN GENERATED CHARACTERS NAV"
END_MARKER = "// END GENERATED CHARACTERS NAV"

TALENT_CATEGORIES = [
    ("magic", "Magic"),
    ("martial", "Martial"),
    ("utility", "Utility"),
]


def root_href(path: str) -> str:
    return f"{{{{ROOT}}}}{path}"


def link(path: str, label: str) -> str:
    return f'<a href="{root_href(path)}">{label}</a>'


def flyout_panel(
    content_html: str,
    *,
    columns: bool = False,
    scroll: bool = False,
    branch_list: bool = False,
) -> str:
    inner_cls = "nav-submenu-panel-inner"
    if branch_list:
        inner_cls += " nav-submenu-panel-inner--branch-list"
    if columns:
        inner_cls += " nav-submenu-panel--columns"
    if scroll:
        inner_cls += " nav-submenu-panel-inner--scroll"
    return (
        f'<div class="nav-submenu-panel">'
        f'<div class="{inner_cls}">{content_html}</div>'
        f"</div>"
    )


def branch_link(path: str, label: str, panel_html: str) -> str:
    return (
        f'<div class="nav-submenu nav-submenu--branch">'
        f'<a href="{root_href(path)}" class="nav-submenu-link">{label}</a>'
        f"{panel_html}"
        f"</div>"
    )


def top_branch(label: str, panel_html: str) -> str:
    return (
        f'<div class="nav-submenu nav-submenu--branch">'
        f'<span class="nav-submenu-label">{label}</span>'
        f"{panel_html}"
        f"</div>"
    )


def branch_list_panel(overview_html: str, branches_html: str) -> str:
    """Overview links stay fixed; only branch rows scroll."""
    return (
        f'<div class="nav-submenu-panel">'
        f'<div class="nav-submenu-panel-inner nav-submenu-panel-inner--intro">'
        f"{overview_html}</div>"
        f'<div class="nav-submenu-panel-inner nav-submenu-panel-inner--branch-list">'
        f"{branches_html}</div>"
        f"</div>"
    )


def render_classes_submenu() -> str:
    by_id = {c["id"]: c for c in CLASSES}
    subclasses = get_subclasses_by_class()
    branches = []
    for class_id in CLASS_ORDER:
        cls = by_id.get(class_id)
        if not cls:
            continue
        subs = subclasses.get(class_id, [])
        sub_links = "".join(
            link(
                f"rules/class-abilities/{class_id}.html#{s['subclass_id']}",
                s["subclass_name"],
            )
            for s in subs
        )
        if not sub_links:
            sub_links = link(
                f"rules/class-abilities/{class_id}.html",
                "Class abilities",
            )
        panel = flyout_panel(sub_links)
        branches.append(
            branch_link(f"rules/classes.html#{class_id}", cls["name"], panel)
        )
    overview = (
        link("rules/classes.html", "All classes")
        + link("rules/class-abilities/index.html", "Class abilities index")
    )
    return top_branch(
        "Classes",
        branch_list_panel(overview, "".join(branches)),
    )


def render_named_list_submenu(label: str, page: str, items: list[dict]) -> str:
    links = link(f"rules/{page}", f"All {label.lower()}")
    links += "".join(
        link(f"rules/{page}#{slugify(item['name'])}", item["name"]) for item in items
    )
    use_columns = len(items) > 10
    return top_branch(label, flyout_panel(links, columns=use_columns, scroll=True))


def render_talents_submenu() -> str:
    branches = []
    for cat_id, cat_label in TALENT_CATEGORIES:
        group = [t for t in TALENTS if t["category"] == cat_id]
        if not group:
            continue
        talent_links = "".join(
            link(f"rules/talents.html#{slugify(t['name'])}", t["name"]) for t in group
        )
        panel = flyout_panel(talent_links, columns=len(group) > 8, scroll=True)
        branches.append(
            branch_link(f"rules/talents.html#{cat_id}-talents", cat_label, panel)
        )
    overview = link("rules/talents.html", "All talents")
    return top_branch("Talents", branch_list_panel(overview, "".join(branches)))


def build_characters_nav() -> str:
    parts = [
        '<div class="nav-dropdown">',
        link("rules/characters.html", "Characters"),
        '<div class="nav-dropdown-menu nav-dropdown-menu-nested">',
        link("rules/characters.html", "Character Creation"),
        render_classes_submenu(),
        render_named_list_submenu("Lineages", "lineages.html", LINEAGES),
        render_named_list_submenu("Heritages", "heritages.html", HERITAGES),
        render_named_list_submenu("Backgrounds", "backgrounds.html", BACKGROUNDS),
        render_talents_submenu(),
        "</div></div>",
    ]
    return "".join(parts)


def patch_includes(nav_html: str) -> None:
    text = INCLUDES_PATH.read_text(encoding="utf-8")
    block = (
        f"{BEGIN_MARKER}\n"
        f"const GENERATED_CHARACTERS_NAV = `{nav_html}`;\n"
        f"{END_MARKER}"
    )
    pattern = re.compile(
        re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit(
            f"Markers not found in {INCLUDES_PATH}. "
            "Add BEGIN/END GENERATED CHARACTERS NAV blocks first."
        )
    text = pattern.sub(block, text, count=1)
    INCLUDES_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    nav_html = build_characters_nav()
    patch_includes(nav_html)
    print(f"Updated Characters nav in {INCLUDES_PATH.name}")


if __name__ == "__main__":
    main()
