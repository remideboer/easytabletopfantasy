#!/usr/bin/env python3
"""Generate backgrounds, talents, and lineages HTML from ToV-sourced data."""

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from ability_utils import (
    TOV_URL,
    render_edition_pill,
    render_srd51_pill,
    render_srd521_pill,
    render_tag_pill,
    render_tov_pill,
    slugify,
)
from character_options_data import BACKGROUNDS, HERITAGES, LINEAGE_HERITAGE_RECOMMENDATIONS, LINEAGES, TALENTS

ROOT = SCRIPT_DIR.parent
RULES = ROOT / "rules"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} | You-Meet-In-A-Tavern (YMIAT)</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="rules/{filename}" />
<link rel="stylesheet" href="../assets/styles.css" />
<script src="../assets/includes.js"></script>
</head>
<body>
<header data-include="nav"></header>
<main>
  <h1>{heading}</h1>
  <div class="content">
{lede}
    <div class="lineages-controls">
      <button id="expand-all-{key}" class="lineage-control-btn" onclick="expandAll{js_key}()">Expand All</button>
      <button id="collapse-all-{key}" class="lineage-control-btn" onclick="collapseAll{js_key}()">Collapse All</button>
    </div>
    <div class="lineages-container">
{items}
    </div>
{extra}
  </div>
</main>
<footer class="legal" data-include="footer"></footer>
<script>
function toggle{js_key}(button){{
  const item = button.closest('.lineage-item');
  const content = item.querySelector('.lineage-content');
  const icon = button.querySelector('.lineage-toggle-icon');
  const isExpanded = content.style.display === 'block' || content.classList.contains('expanded');
  if(isExpanded){{
    content.style.display = 'none';
    content.classList.remove('expanded');
    icon.textContent = '▼';
    button.setAttribute('aria-expanded', 'false');
  }} else {{
    content.style.display = 'block';
    content.classList.add('expanded');
    icon.textContent = '▲';
    button.setAttribute('aria-expanded', 'true');
  }}
}}
function expandAll{js_key}(){{
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-content').forEach(content => {{
    content.style.display = 'block';
    content.classList.add('expanded');
  }});
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-toggle-icon').forEach(icon => {{
    icon.textContent = '▲';
  }});
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-header').forEach(button => {{
    button.setAttribute('aria-expanded', 'true');
  }});
}}
function collapseAll{js_key}(){{
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-content').forEach(content => {{
    content.style.display = 'none';
    content.classList.remove('expanded');
  }});
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-toggle-icon').forEach(icon => {{
    icon.textContent = '▼';
  }});
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-header').forEach(button => {{
    button.setAttribute('aria-expanded', 'false');
  }});
}}
function expand{js_key}FromHash(){{
  const raw = window.location.hash;
  if(!raw || raw.length < 2) return;
  const target = document.getElementById(decodeURIComponent(raw.slice(1)));
  if(!target || !target.classList.contains('lineage-item')) return;
  const content = target.querySelector('.lineage-content');
  const button = target.querySelector('.lineage-header');
  if(!content || !button) return;
  content.style.display = 'block';
  content.classList.add('expanded');
  const icon = button.querySelector('.lineage-toggle-icon');
  if(icon) icon.textContent = '▲';
  button.setAttribute('aria-expanded', 'true');
  requestAnimationFrame(function(){{
    target.scrollIntoView({{behavior:'smooth', block:'start'}});
  }});
}}
document.addEventListener('DOMContentLoaded', function(){{
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-content').forEach(content => {{
    content.style.display = 'none';
  }});
  document.querySelectorAll('.lineages-container > .lineage-item .lineage-header').forEach(button => {{
    button.setAttribute('aria-expanded', 'false');
  }});
  expand{js_key}FromHash();
}});
window.addEventListener('hashchange', expand{js_key}FromHash);
</script>
<script src="../assets/site.js"></script>
</body>
</html>
"""


def render_title(name: str, tov: bool = True, tag: str | None = None, edition: str | None = None) -> str:
    if edition and name.endswith(f" ({edition})"):
        name = name[: -len(f" ({edition})")]
    tag_pill = ""
    if tag == "SRD51":
        pill = render_srd51_pill()
    elif tag == "SRD52":
        pill = render_srd521_pill()
    elif tag:
        pill = render_tov_pill() if tov else ""
        tag_pill = render_tag_pill(tag)
    else:
        pill = render_tov_pill() if tov else ""
    if edition and edition != "5.5e":
        pill = f"{pill}{render_edition_pill(edition)}"
    pill = f"{pill}{tag_pill}"
    return f'<span class="lineage-title-wrap"><span class="lineage-title">{name}</span>{pill}</span>'


def js_toggle(js_key: str) -> str:
    """Keep onclick handlers aligned with HEAD script function names."""
    return f"toggle{js_key}"


def render_item(
    name: str, body: str, js_key: str, tov: bool = True, tag: str | None = None, edition: str | None = None
) -> str:
    toggle = js_toggle(js_key)
    item_id = slugify(name)
    return f"""      <div class="lineage-item" id="{item_id}">
        <button class="lineage-header" onclick="{toggle}(this)">
          {render_title(name, tov, tag, edition)}
          <span class="lineage-toggle-icon">▼</span>
        </button>
        <div class="lineage-content">
          {body}
        </div>
      </div>"""


def write_backgrounds():
    lede = f"""    <p class="lede">Background helps define your character's personal history before taking up the mantle of an adventurer.</p>
    <p>Backgrounds from the <a href="{TOV_URL}" rel="noopener">Tales of the Valiant</a> Player's Guide (2024 core and 2026 options). In YMIAT, only skills explicitly granted benefit from proficiency advantage.</p>"""
    items = "\n".join(
        render_item(
            b["name"], b["body"], "Backgrounds", tov=b.get("tov", True), tag=b.get("tag"), edition=b.get("edition")
        )
        for b in BACKGROUNDS
    )
    html = HEAD.format(
        title="Backgrounds",
        description="Character backgrounds for You-Meet-In-A-Tavern (YMIAT).",
        filename="backgrounds.html",
        heading="Backgrounds",
        lede=lede,
        key="backgrounds",
        js_key="Backgrounds",
        items=items,
        extra="",
    )
    (RULES / "backgrounds.html").write_text(html, encoding="utf-8")
    print(f"Wrote backgrounds.html ({len(BACKGROUNDS)} backgrounds)")


def write_talents():
    lede = f"""    <p class="lede">Talents from the <a href="{TOV_URL}" rel="noopener">Tales of the Valiant</a> Player's Guide, adapted for YMIAT (Resolve, Wounds, utility talents). Talents marked (SRD) are converted from the D&D 5e System Reference Document's feats.</p>
    <p>Talents are gained from backgrounds at 1st level and from class Improvement features.</p>"""
    sections = []
    for cat, heading in [("magic", "Magic Talents"), ("martial", "Martial Talents"), ("utility", "Utility Talents")]:
        group = [t for t in TALENTS if t["category"] == cat]
        if not group:
            continue
        if sections:
            sections.append("    <hr>")
        sections.append(f"    <h2 id=\"{cat}-talents\">{heading}</h2>")
        blocks = []
        for t in group:
            body = ""
            if t.get("prereq"):
                body += f'<p><strong>Prerequisite:</strong> {t["prereq"]}</p>'
            body += t["body"]
            blocks.append(
                render_item(
                    t["name"], body, "Talents", tov=t.get("tov", True), tag=t.get("tag"), edition=t.get("edition")
                )
            )
        sections.append('    <div class="lineages-container">')
        sections.extend(blocks)
        sections.append("    </div>")
    extra = f"""    <hr>
    <p><em>Additional talents appear in the ToV Player's Guide and Player's Guide 2. Only talents listed here are summarized for YMIAT play.</em></p>"""
    html = HEAD.format(
        title="Talents",
        description="Character talents for You-Meet-In-A-Tavern (YMIAT).",
        filename="talents.html",
        heading="Talents",
        lede=lede,
        key="talents",
        js_key="Talents",
        items="\n".join(sections[2:]) if len(sections) > 2 else "",
        extra=extra,
    )
    # Fix structure: lede + sections need custom assembly
    parts = [
        HEAD.split("{items}")[0].format(
            title="Talents",
            description="Character talents for You-Meet-In-A-Tavern (YMIAT).",
            filename="talents.html",
            heading="Talents",
            lede=lede,
            key="talents",
            js_key="Talents",
            items="",
            extra="",
        ).replace('<div class="lineages-container">\n\n    </div>', ""),
    ]
    # Rebuild talents page manually for multi-section layout
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Talents | You-Meet-In-A-Tavern (YMIAT)</title>
<link rel="stylesheet" href="../assets/styles.css" />
<script src="../assets/includes.js"></script>
</head>
<body>
<header data-include="nav"></header>
<main>
  <h1>Talents</h1>
  <div class="content">
{lede}
    <div class="lineages-controls">
      <button class="lineage-control-btn" onclick="expandAllTalents()">Expand All</button>
      <button class="lineage-control-btn" onclick="collapseAllTalents()">Collapse All</button>
    </div>
{chr(10).join(sections)}
{extra}
  </div>
</main>
<footer class="legal" data-include="footer"></footer>
<script>
function toggleTalents(button){{
  const item = button.closest('.lineage-item');
  const content = item.querySelector('.lineage-content');
  const icon = button.querySelector('.lineage-toggle-icon');
  const open = content.style.display === 'block' || content.classList.contains('expanded');
  content.style.display = open ? 'none' : 'block';
  content.classList.toggle('expanded', !open);
  icon.textContent = open ? '▼' : '▲';
  button.setAttribute('aria-expanded', open ? 'false' : 'true');
}}
function expandAllTalents(){{
  document.querySelectorAll('.lineage-item .lineage-content').forEach(c => {{ c.style.display='block'; c.classList.add('expanded'); }});
  document.querySelectorAll('.lineage-toggle-icon').forEach(i => i.textContent='▲');
  document.querySelectorAll('.lineage-header').forEach(b => b.setAttribute('aria-expanded','true'));
}}
function collapseAllTalents(){{
  document.querySelectorAll('.lineage-item .lineage-content').forEach(c => {{ c.style.display='none'; c.classList.remove('expanded'); }});
  document.querySelectorAll('.lineage-toggle-icon').forEach(i => i.textContent='▼');
  document.querySelectorAll('.lineage-header').forEach(b => b.setAttribute('aria-expanded','false'));
}}
function expandTalentsFromHash(){{
  const raw = window.location.hash;
  if(!raw || raw.length < 2) return;
  const target = document.getElementById(decodeURIComponent(raw.slice(1)));
  if(!target) return;
  if(target.classList.contains('lineage-item')){{
    const content = target.querySelector('.lineage-content');
    const button = target.querySelector('.lineage-header');
    if(content && button){{
      content.style.display = 'block';
      content.classList.add('expanded');
      const icon = button.querySelector('.lineage-toggle-icon');
      if(icon) icon.textContent = '▲';
      button.setAttribute('aria-expanded', 'true');
    }}
  }}
  requestAnimationFrame(function(){{
    target.scrollIntoView({{behavior:'smooth', block:'start'}});
  }});
}}
document.addEventListener('DOMContentLoaded', function(){{
  collapseAllTalents();
  expandTalentsFromHash();
}});
window.addEventListener('hashchange', expandTalentsFromHash);
</script>
<script src="../assets/site.js"></script>
</body>
</html>"""
    (RULES / "talents.html").write_text(html, encoding="utf-8")
    print(f"Wrote talents.html ({len(TALENTS)} talents)")


def write_lineages():
    lede = f"""    <p class="lede">Lineage represents blood ties and hereditary traits—YMIAT's replacement for traditional species/race.</p>
    <p>Lineages and variants from the <a href="{TOV_URL}" rel="noopener">Tales of the Valiant</a> Player's Guide (2024) and Player's Guide 2 (2026), adapted to Fitness, Insight, and Willpower. Pair with a cultural <a href="heritages.html">heritage</a> at character creation.</p>"""
    items = "\n".join(
        render_item(
            L["name"],
            L["body"],
            "Lineages",
            tov=L.get("tov", True),
            tag=L.get("tag"),
        )
        for L in LINEAGES
    )
    html = HEAD.format(
        title="Lineages",
        description="Character lineages for You-Meet-In-A-Tavern (YMIAT).",
        filename="lineages.html",
        heading="Lineages",
        lede=lede,
        key="lineages",
        js_key="Lineages",
        items=items,
        extra="",
    )
    (RULES / "lineages.html").write_text(html, encoding="utf-8")
    print(f"Wrote lineages.html ({len(LINEAGES)} lineages)")


def render_heritage_item(h: dict) -> str:
    body = h["body"]
    if h.get("recommended"):
        body = f'<p><strong>Common for lineages:</strong> {h["recommended"]}</p>\n' + body
    return render_item(h["name"], body, "Heritages", tov=h.get("tov", True), tag=h.get("tag"))


def write_heritages():
    lede = f"""    <p class="lede">Heritage represents upbringing and culture—what your community taught you, separate from bloodline <a href="lineages.html">lineage</a> traits.</p>
    <p>Heritage options from the <a href="{TOV_URL}" rel="noopener">Tales of the Valiant</a> Player's Guide (2024) and Player's Guide 2 (2026). You may choose <strong>any</strong> heritage with any lineage (e.g. human lineage with elven grove heritage).</p>"""
    rows = "\n".join(
        f"        <tr><td>{lineage}</td><td>{heritages}</td></tr>"
        for lineage, heritages in LINEAGE_HERITAGE_RECOMMENDATIONS
    )
    extra = f"""    <h2 id="heritages-by-lineage">Common Heritages by Lineage</h2>
    <p>Typical pairings for classic fantasy archetypes. These are suggestions, not requirements.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Lineage</th><th>Recommended Heritages</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table></div>"""
    items = "\n".join(render_heritage_item(h) for h in HERITAGES)
    html = HEAD.format(
        title="Heritages",
        description="Character heritages for You-Meet-In-A-Tavern (YMIAT).",
        filename="heritages.html",
        heading="Heritages",
        lede=lede,
        key="heritages",
        js_key="Heritages",
        items=items,
        extra=extra,
    )
    (RULES / "heritages.html").write_text(html, encoding="utf-8")
    print(f"Wrote heritages.html ({len(HERITAGES)} heritages)")


def main():
    write_backgrounds()
    write_talents()
    write_lineages()
    write_heritages()


if __name__ == "__main__":
    main()
