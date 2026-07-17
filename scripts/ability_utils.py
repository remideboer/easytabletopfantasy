"""Shared helpers for class ability pages and linking."""
import re

TOV_URL = "https://www.talesofthevaliant.com/"
SRD_51_URL = "https://www.dndbeyond.com/srd#PreviousSRDReleases"
SRD_521_URL = "https://www.dndbeyond.com/srd"


def render_tov_pill() -> str:
    """Small source tag linking to Tales of the Valiant."""
    return (
        f'<a href="{TOV_URL}" class="source-pill source-pill-tov" rel="noopener" '
        f'title="Tales of the Valiant Player\'s Guide" onclick="event.stopPropagation()">ToV</a>'
    )


def render_srd51_pill() -> str:
    """Small source tag for content genuinely from the 5.1 SRD (Creative Commons)."""
    return (
        f'<a href="{SRD_51_URL}" class="source-pill source-pill-srd51" rel="noopener" '
        f'title="D&amp;D 5.1 System Reference Document (Creative Commons license)" '
        f'onclick="event.stopPropagation()">SRD 5.1 CC</a>'
    )


def render_srd521_pill() -> str:
    """Small source tag for content from the 5.2.1 SRD (Wizards' newer game license, not CC)."""
    return (
        f'<a href="{SRD_521_URL}" class="source-pill source-pill-srd521" rel="noopener" '
        f'title="D&amp;D 5.2.1 System Reference Document (Wizards of the Coast Game License)" '
        f'onclick="event.stopPropagation()">SRD 5.2.1</a>'
    )


def render_title_with_tov(title: str) -> str:
    return (
        f'<span class="lineage-title-wrap">'
        f'<span class="lineage-title">{title}</span>'
        f"{render_tov_pill()}"
        f"</span>"
    )


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


def escape_html_attr(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def format_ability_tooltip(ability: dict) -> str:
    parts = [ability["summary"]]
    if ability.get("action"):
        parts.append(f"Action: {ability['action']}")
    parts.append(ability["level"])
    return " — ".join(parts)


def build_tooltip_registry(abilities) -> dict:
    registry = {}
    for ability in abilities:
        tip = format_ability_tooltip(ability)
        for name in ability["names"]:
            registry[(ability["class_id"], normalize_feature_name(name))] = tip
            registry[(ability["class_id"], name.lower())] = tip
    return registry


def render_tip_link(href: str, text: str, tip: str | None = None) -> str:
    if not tip:
        return f'<a href="{href}">{text}</a>'
    attr = escape_html_attr(tip)
    return f'<a href="{href}" class="ability-tip" data-tip="{attr}">{text}</a>'


SUBCLASS_CHOICE_TIP = (
    "Choose your subclass at 2nd level. Subclass features arrive at 2nd, 4th, 6th, and 8th."
)
SUBCLASS_FEATURE_TIP = "Subclass feature at this level. See subclass rules on the class ability page."


def linkify_feature_text(class_id: str, text: str, registry: dict, tooltips: dict | None = None) -> str:
    """Turn feature names in progression cells into links with hover tooltips."""
    tooltips = tooltips or {}
    if not text or text == "—":
        return text
    if text == "Subclass Feature":
        return render_tip_link(
            ability_href(class_id, "subclasses"), text, SUBCLASS_FEATURE_TIP
        )
    if text.endswith(" Subclass"):
        return render_tip_link(
            ability_href(class_id, "subclasses"), text, SUBCLASS_CHOICE_TIP
        )

    parts = re.split(r"(\s*;\s*|\s*,\s*)", text)
    out = []
    for part in parts:
        if part.strip() in (";", ",") or re.match(r"^\s*[;,]\s*$", part):
            out.append(part)
            continue
        key = normalize_feature_name(part)
        anchor = registry.get((class_id, key))
        stripped = part.strip()
        if stripped == "Subclass Feature":
            out.append(
                render_tip_link(
                    ability_href(class_id, "subclasses"), stripped, SUBCLASS_FEATURE_TIP
                )
            )
        elif stripped.endswith(" Subclass"):
            out.append(
                render_tip_link(
                    ability_href(class_id, "subclasses"), stripped, SUBCLASS_CHOICE_TIP
                )
            )
        elif anchor:
            tip = tooltips.get((class_id, key)) or tooltips.get((class_id, stripped.lower()))
            out.append(
                render_tip_link(ability_href(class_id, anchor), stripped, tip)
            )
        else:
            out.append(part)
    return "".join(out)
