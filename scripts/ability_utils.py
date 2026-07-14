"""Shared helpers for class ability pages and linking."""
import re


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"['']", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def normalize_feature_name(name: str) -> str:
    """Strip level notes and parentheticals for matching."""
    name = re.sub(r"\s*\([^)]*\)", "", name)
    name = re.sub(r"^epic boon:\s*", "", name, flags=re.I)
    name = re.sub(r"^channel divinity:\s*", "", name, flags=re.I)
    name = re.sub(r"^bardic performance:\s*", "", name, flags=re.I)
    return name.strip().lower()


def make_anchor(name: str) -> str:
    return slugify(normalize_feature_name(name))


def ability_href(class_id: str, anchor: str) -> str:
    return f"class-abilities/{class_id}.html#{anchor}"


def linkify_feature_text(class_id: str, text: str, registry: dict) -> str:
    """Turn feature names in progression cells into links."""
    if not text or text == "—":
        return text
    if text == "Subclass Feature" or text.endswith(" Subclass"):
        return f'<a href="class-abilities/{class_id}.html#subclasses">{text}</a>'

    parts = re.split(r"(\s*;\s*|\s*,\s*)", text)
    out = []
    for part in parts:
        if part.strip() in (";", ",") or re.match(r"^\s*[;,]\s*$", part):
            out.append(part)
            continue
        key = normalize_feature_name(part)
        anchor = registry.get((class_id, key))
        stripped = part.strip()
        if stripped == "Subclass Feature" or stripped.endswith(" Subclass"):
            out.append(f'<a href="{ability_href(class_id, "subclasses")}">{stripped}</a>')
        elif anchor:
            display = stripped
            out.append(f'<a href="{ability_href(class_id, anchor)}">{display}</a>')
        else:
            out.append(part)
    return "".join(out)
