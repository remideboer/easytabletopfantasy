#!/usr/bin/env python3
"""
Generate rules/classes.html from YMIAT class data.
Source: Black Flag Reference Document (BFRD) compressed to 10 levels.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from class_abilities_data import all_abilities, build_registry
from class_subclasses_data import all_subclass_features, build_subclass_registry, get_subclasses_by_class
from ability_utils import (
    TOV_URL,
    build_tooltip_registry,
    linkify_feature_text,
    render_tip_link,
    render_title_with_tov,
)

ROOT = SCRIPT_DIR.parent
OUT = ROOT / "rules" / "classes.html"

ABILITIES = all_abilities()
SUBCLASS_FEATURES = all_subclass_features()
ABILITY_REGISTRY = {**build_registry(ABILITIES), **build_subclass_registry(SUBCLASS_FEATURES)}
ABILITY_TOOLTIPS = build_tooltip_registry(ABILITIES + SUBCLASS_FEATURES)
SUBCLASSES_BY_CLASS = get_subclasses_by_class()

# Max spell circle by YMIAT level
MAX_LEVEL = 10
MAX_SPELL_CIRCLE = 9


def full_caster_circles(max_level=MAX_LEVEL, max_circle=MAX_SPELL_CIRCLE):
    """Full casters: +1 max circle per class level, capped at 9 (level 9–10 → circle 9)."""
    return {lvl: min(lvl, max_circle) for lvl in range(1, max_level + 1)}


def half_caster_circles(spell_start=2, max_level=MAX_LEVEL):
    """Half casters: max circle increases every 2 class levels from spellcasting start."""
    circles = {}
    for lvl in range(1, max_level + 1):
        if lvl < spell_start:
            circles[lvl] = None  # no spellcasting yet
        else:
            circles[lvl] = (lvl - spell_start) // 2 + 1
    return circles


def pact_caster_circles(max_level=MAX_LEVEL):
    """Warlock pact magic: +1 max circle every 2 levels from 1st (caps at 5 on level 9–10)."""
    return half_caster_circles(spell_start=1, max_level=max_level)


FULL_CASTER_CIRCLE = full_caster_circles()
HALF_CASTER_CIRCLE = half_caster_circles(spell_start=2)
PACT_CASTER_CIRCLE = pact_caster_circles()


def spell_circle_rows(circles, start=1):
    rows = []
    for lvl in range(1, 11):
        if lvl < start:
            rows.append(f"<tr><td>{lvl}</td><td>—</td></tr>")
        else:
            val = circles.get(lvl)
            rows.append(f"<tr><td>{lvl}</td><td>{val if val is not None else '—'}</td></tr>")
    return "\n".join(rows)


def render_progression(headers, rows, class_id):
    th = "".join(f"<th>{h}</th>" for h in headers)
    feat_idx = next((i for i, h in enumerate(headers) if h.lower() == "features"), None)
    body = ""
    for row in rows:
        cells = []
        for i, c in enumerate(row):
            text = str(c)
            if i == feat_idx:
                text = linkify_feature_text(class_id, text, ABILITY_REGISTRY, ABILITY_TOOLTIPS)
            cells.append(text)
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>\n"
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>\n{body}</tbody></table></div>'


def render_class(cls):
    pid = cls["id"]
    blocks = []
    blocks.append(f'<div class="lineage-item" id="{pid}">')
    blocks.append(
        f'<button class="lineage-header" onclick="toggleClass(this)">'
        f'{render_title_with_tov(cls["name"])}'
        f'<span class="lineage-toggle-icon">▼</span></button>'
    )
    blocks.append('<div class="lineage-content">')
    blocks.append(f'<p class="class-summary">{cls["summary"]}</p>')
    blocks.append(
        f"<p><strong>Max Wounds (start):</strong> {cls['max_wd']} + Fitness modifier. "
        f"<strong>Key ability:</strong> {cls['key_ability']}. "
        f"<strong>Saves:</strong> {cls['saves']}.</p>"
    )
    blocks.append(f"<p><strong>Proficiencies:</strong> {cls['proficiencies']}</p>")
    if cls.get("spellcasting"):
        blocks.append(f"<p><strong>Spellcasting:</strong> {cls['spellcasting']}</p>")
        if cls.get("spell_circles"):
            blocks.append("<p><strong>Max spell circle by level:</strong></p>")
            blocks.append(
                '<div class="table-wrap"><table><thead><tr><th>Level</th><th>Max Circle</th></tr></thead><tbody>'
                + spell_circle_rows(cls["spell_circles"], cls.get("spell_start", 1))
                + "</tbody></table></div>"
            )
        blocks.append(
            '<p>Casters use <a href="core.html#magic-and-spell-resources">Spell Power (SP)</a> '
            "instead of spell slots. Spell cost equals spell circle.</p>"
        )
    blocks.append(f'<h3 id="{pid}-progression">Progression</h3>')
    blocks.append(render_progression(cls["table_headers"], cls["table_rows"], pid))
    blocks.append(f'<h3 id="{pid}-features">Class Features</h3>')
    blocks.append(
        f'<p>Full rules: <a href="class-abilities/{pid}.html">All {cls["name"]} abilities →</a> '
        f'(<a href="class-abilities/index.html#{pid}">index</a>) · '
        f'<a href="class-abilities/{pid}.html#subclasses">subclasses</a></p>'
    )
    if cls.get("subclasses"):
        blocks.append(f'<h3 id="{pid}-subclasses">Subclasses</h3>')
        blocks.append("<p>Choose at 2nd level; features at 2nd, 4th, 6th, and 8th.</p>")
        blocks.append("<ul>")
        for sub_name in cls["subclasses"]:
            sub_entry = next(
                (s for s in SUBCLASSES_BY_CLASS.get(pid, []) if s["subclass_name"] == sub_name),
                None,
            )
            if sub_entry:
                sub_href = f"class-abilities/{pid}.html#{sub_entry['subclass_id']}"
                blocks.append(
                    f"<li><strong>{render_tip_link(sub_href, sub_name, sub_entry['summary'])}</strong></li>"
                )
            else:
                blocks.append(f"<li><strong>{sub_name}</strong></li>")
        blocks.append("</ul>")
    blocks.append(
        f'<p class="source-note">Adapted from '
        f'<a href="{TOV_URL}" rel="noopener">Tales of the Valiant</a> '
        f'(<a href="{cls["bfrd_url"]}" rel="noopener">BFRD {cls["name"]}</a>) '
        f"for YMIAT 10-level play.</p>"
    )
    blocks.append("</div></div>")
    return "\n".join(blocks)


CLASSES = [
    {
        "id": "barbarian",
        "name": "Barbarian",
        "summary": "A primal warrior who channels fury in battle. High Max Wounds, melee dominance, and resistance while raging.",
        "max_wd": 12,
        "key_ability": "Fitness (FIT)",
        "saves": "FIT (advantage on save)",
        "proficiencies": "Light and medium armor, shields, simple and martial weapons, herbalism tools. Skills: choose two from Animal Handling, Athletics, Intimidation, Nature, Perception, Survival.",
        "bfrd_url": "https://bfrd.net/classes/barbarian/",
        "table_headers": ["Level", "Rages", "Rage +", "Features"],
        "table_rows": [
            [1, 2, "+2", "Rage, Unarmored Defense, Danger Sense, Reckless Attack"],
            [2, 2, "+2", "Barbarian Subclass"],
            [3, 3, "+2", "Improvement; Fast Movement, Multiattack, Feral Instinct"],
            [4, 3, "+2", "Subclass Feature; Improvement"],
            [5, 4, "+3", "Brutal Critical (1 die); Heroic Boon"],
            [6, 4, "+3", "Subclass Feature"],
            [7, 5, "+3", "Brutal Critical (2 dice); Relentless Rage; Improvement"],
            [8, 5, "+3", "Subclass Feature"],
            [9, 6, "+4", "Brutal Critical (3 dice); Unyielding Might; Improvement"],
            [10, "Unlimited", "+5", "Epic Boon; Improvement"],
        ],
        "features": [
            {
                "name": "Unarmored Defense",
                "level": "1st-level feature",
                "text": "While you aren't wearing armor, your base AC equals 10 + 2× your Fitness modifier. You can use a shield and still gain this benefit.",
            },
            {
                "name": "Rage",
                "level": "1st-level feature (free action)",
                "text": "On your turn, you can rage as a free action. While raging (and not wearing heavy armor): advantage on FIT checks and saves; bonus melee damage per Rage + column; resistance to bludgeoning, piercing, and slashing (attackers have disadvantage). You can't cast or concentrate on spells while raging. Rage lasts 1 minute or ends early as in BFRD. Uses per long rest per progression table.",
            },
            {
                "name": "Danger Sense",
                "level": "1st-level feature",
                "text": "You have advantage on Fitness saving throws unless you have the Incapacitated condition.",
            },
            {
                "name": "Reckless Attack",
                "level": "1st-level feature",
                "text": "When you attack on your turn, you can attack recklessly: advantage on melee FIT attacks this turn, but disadvantage on your Defense roll until the start of your next turn.",
            },
            {
                "name": "Improvement",
                "level": "3rd, 5th, 7th, 9th, and 10th level",
                "text": "Increase one ability by 2, two abilities by 1 each, or one ability by 1 and choose a martial talent.",
            },
            {
                "name": "Heroic Boon",
                "level": "5th-level feature",
                "text": "Choose one: <strong>Instant Rage</strong> (rage without a free action when combat begins and you use Fast Movement's opening move); <strong>Stubborn Rage</strong> (rage ends only when duration expires, you fall unconscious, or you choose to end it); <strong>Bloody Rage</strong> (while raging, slashing damage you deal with weapon attacks ignores resistance); <strong>Vengeful Rage</strong> (when damaged while raging, stacking advantage on your first attack against that creature next turn).",
            },
            {
                "name": "Relentless Rage",
                "level": "7th-level feature",
                "text": "While raging, if reduced to Max Wounds, make a DC 10 FIT save to avoid falling unconscious until rage ends. DC increases by 5 each use; resets on rest.",
            },
            {
                "name": "Epic Boon: Primal Champion",
                "level": "10th-level feature",
                "text": "Your Fitness modifier increases by 2 (maximum modifier now +7).",
            },
        ],
        "subclasses": ["Berserker", "Wild Fury", "Chaos", "Four Winds", "Kraken"],
    },
    {
        "id": "bard",
        "name": "Bard",
        "summary": "A versatile performer whose magic and inspiration support allies and confound foes.",
        "max_wd": 8,
        "key_ability": "Willpower (WIL)",
        "saves": "WIL (advantage on save)",
        "proficiencies": "Light armor; simple weapons and martial finesse weapons; three musical instruments or tools; any three skills.",
        "spellcasting": "Arcane spells. Spells known (no preparation). Rituals known per level.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": "https://bfrd.net/classes/bard/",
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Bardic Inspiration (d6), Spellcasting, Expertise (2)"],
            [2, "Bard Subclass; Bardic Performance (Celebrate Life, Cutting Words)"],
            [3, "Improvement; Font of Inspiration"],
            [4, "Subclass Feature; Improvement; Bardic Inspiration (d8)"],
            [5, "Bardic Performance: Clarity of Thought; Expertise (4); Heroic Boon"],
            [6, "Subclass Feature; Magical Secrets"],
            [7, "Improvement; Bardic Inspiration (d10)"],
            [8, "Subclass Feature; Grand Performance"],
            [9, "Improvement; Magical Secrets"],
            [10, "Epic Boon: Curtain Call; Improvement"],
        ],
        "features": [
            {
                "name": "Bardic Inspiration",
                "level": "1st-level feature (action)",
                "text": "Grant a d6 inspiration die to a creature within 60 feet (not yourself). Uses equal to WIL modifier per long rest. Die becomes d8 at 4th, d10 at 7th. Font of Inspiration (3rd): regain uses on short or long rest; reaction to add die to failed roll.",
            },
            {
                "name": "Bardic Performance",
                "level": "2nd-level feature",
                "text": "Performance effects as action; maintain with action each turn. Uses per PB per long rest. Celebrate Life heals allies; Cutting Words subtracts inspiration die from enemy rolls; Clarity of Thought (5th) grants charm/frighten protection.",
            },
        ],
        "subclasses": ["Lore", "Victory", "Allure", "Mockery", "Sound"],
    },
    {
        "id": "cleric",
        "name": "Cleric",
        "summary": "A divine champion who channels deity power through spells and channel divinity.",
        "max_wd": 8,
        "key_ability": "Insight (INS)",
        "saves": "INS (advantage on save)",
        "proficiencies": "Light and medium armor, shields, simple weapons. Skills: History, Insight, Medicine, Persuasion, Religion (choose two).",
        "spellcasting": "Divine spells (prepared). Domain spells always prepared.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": "https://bfrd.net/classes/cleric/",
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Manifestation of Faith, Spellcasting"],
            [2, "Cleric Subclass; Channel Divinity: Turn the Profane"],
            [3, "Improvement"],
            [4, "Subclass Feature; Improvement; Destroy the Profane (CR ½)"],
            [5, "Channel Divinity (2/rest); Heroic Boon"],
            [6, "Subclass Feature; Destroy the Profane (CR 1)"],
            [7, "Improvement; Divine Intervention"],
            [8, "Subclass Feature; Destroy the Profane (CR 2)"],
            [9, "Improvement; Channel Divinity (3/rest)"],
            [10, "Epic Boon: Divine Herald; Destroy the Profane (CR 4)"],
        ],
        "features": [
            {
                "name": "Channel Divinity",
                "level": "2nd-level feature (free action)",
                "text": "Turn the Profane: Fiends and Undead within 30 feet make INS save or are turned. Uses increase at 5th and 9th. Destroy the Profane destroys turned creatures at or below listed CR.",
            },
            {
                "name": "Manifestation of Faith",
                "level": "1st-level feature",
                "text": "Manifest Might (heavy armor, martial weapon, +PB radiant/necrotic once per turn) or Manifest Miracles (extra cantrip, +PB to cantrip damage).",
            },
        ],
        "subclasses": ["Life", "Light", "War", "Death", "Nature", "Tempest"],
    },
    {
        "id": "druid",
        "name": "Druid",
        "summary": "A guardian of nature wielding primordial magic and wild shape.",
        "max_wd": 8,
        "key_ability": "Insight (INS)",
        "saves": "INS (advantage on save)",
        "proficiencies": "Light and medium armor, shields, simple weapons, herbalist tools.",
        "spellcasting": "Primordial spells (prepared). Ring spells always prepared.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": "https://bfrd.net/classes/druid/",
        "table_headers": ["Level", "Wild Shape", "Features"],
        "table_rows": [
            [1, "—", "Druidic, Nature's Gift, Spellcasting"],
            [2, "1/rest", "Druid Subclass; Wild Shape (Beast Form, Draw Power)"],
            [3, "1/rest", "Improvement; Improved Beast Form (CR ¼)"],
            [4, "2/rest", "Subclass Feature; Improvement"],
            [5, "2/rest", "Improved Beast Form (CR ½); Heroic Boon"],
            [6, "2/rest", "Subclass Feature"],
            [7, "3/rest", "Improved Beast Form (CR 1); Improvement"],
            [8, "3/rest", "Subclass Feature; Nature's Grace"],
            [9, "4/rest", "Improved Beast Form (CR 2); Improvement"],
            [10, "4/rest", "Epic Boon: Archdruid"],
        ],
        "features": [
            {
                "name": "Wild Shape",
                "level": "2nd-level feature (free action for Beast Form)",
                "text": "Beast Form: assume a known beast form. Draw Power: recover an expended spell circle ≤ PB. Uses per rest per table.",
            },
            {
                "name": "Nature's Gift",
                "level": "1st-level feature (action)",
                "text": "Heal a creature within 5 feet for PB d4s (minimum 2d4). Uses per PB per long rest. No effect on Constructs or Undead.",
            },
        ],
        "subclasses": ["Leaf", "Shifter", "Elementalist", "Fey", "Stoneheart"],
    },
    {
        "id": "fighter",
        "name": "Fighter",
        "summary": "A master of weapons and battlefield tactics with action surge and martial actions.",
        "max_wd": 10,
        "key_ability": "Fitness (FIT)",
        "saves": "FIT (advantage on save)",
        "proficiencies": "All armor and shields; simple and martial weapons.",
        "bfrd_url": "https://bfrd.net/classes/fighter/",
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Last Stand, Martial Action"],
            [2, "Fighter Subclass; Action Surge"],
            [3, "Improvement; Multiattack (2)"],
            [4, "Subclass Feature; Improvement"],
            [5, "Heroic Boon"],
            [6, "Subclass Feature; Multiattack (3)"],
            [7, "Improvement; Action Surge (2/rest)"],
            [8, "Subclass Feature"],
            [9, "Improvement; Multiattack (4)"],
            [10, "Epic Boon: Turn the Tide; Action Surge (3/rest)"],
        ],
        "features": [
            {
                "name": "Martial Action",
                "level": "1st-level feature (second action if no movement used)",
                "text": "Choose Aim, Guard, Quick Strike, or Wind Up. In YMIAT, use as your second action when you have not moved this turn (attacks at disadvantage if second action is an attack).",
            },
            {
                "name": "Action Surge",
                "level": "2nd-level feature",
                "text": "Gain another action on your turn once per short rest (twice at 7th, thrice at 10th; once per turn max).",
            },
            {
                "name": "Last Stand",
                "level": "1st-level feature (reaction)",
                "text": "When damage would bring you below half Max Wounds, spend hit dice (up to PB) to heal.",
            },
        ],
        "subclasses": ["Spell Blade", "Weapon Master", "Scrapper", "Stunt Archer", "Twinblade"],
    },
    {
        "id": "artificer",
        "name": "Artificer",
        "summary": "An inventor who augments gear and crafts magical items. (BFRD Mechanist.)",
        "max_wd": 8,
        "key_ability": "Insight (INS)",
        "saves": "INS (advantage on save)",
        "proficiencies": "Light and medium armor, shields, all weapons, tinker tools + two tools.",
        "bfrd_url": "https://bfrd.net/classes/mechanist/",
        "table_headers": ["Level", "Augments", "Items", "Features"],
        "table_rows": [
            [1, "—", "—", "Eyes of the Maker, Shard of Creation"],
            [2, 2, 3, "Artificer Subclass; Augment, Efficient Action"],
            [3, 3, 3, "Improvement; Multiattack (2)"],
            [4, 4, 4, "Subclass Feature; Improvement; Rapid Augment"],
            [5, 5, 4, "Greater Creation; Heroic Boon"],
            [6, 6, 5, "Subclass Feature; Engineer's Insight"],
            [7, 7, 5, "Improvement; Ranged Augment"],
            [8, 8, 6, "Subclass Feature; Always Prepared"],
            [9, 8, 7, "Improvement; Perfect Creation"],
            [10, 9, 7, "Epic Boon"],
        ],
        "features": [
            {
                "name": "Augment",
                "level": "2nd-level feature",
                "text": "Apply augment effects to items you carry. Know augment effects and maintain augmented items per progression table.",
            },
            {
                "name": "Shard of Creation",
                "level": "1st-level feature",
                "text": "Tiny magical shard with charges equal to INS modifier (min 1), regained on long rest. Inspire, Mend, and other properties per BFRD.",
            },
        ],
        "subclasses": ["Alchemist", "Armorer", "Artillerist", "Battle Smith", "Cog Augur", "Grenadier", "Toymaker"],
    },
    {
        "id": "monk",
        "name": "Monk",
        "summary": "A martial artist channeling technique points for supernatural strikes and mobility.",
        "max_wd": 8,
        "key_ability": "Fitness (FIT)",
        "saves": "FIT (advantage on save)",
        "proficiencies": "Simple weapons, shortswords; no armor.",
        "bfrd_url": "https://bfrd.net/classes/monk/",
        "table_headers": ["Level", "Martial Arts", "Technique Pts", "Movement", "Features"],
        "table_rows": [
            [1, "1d4", "—", "—", "Martial Arts, Unarmored Defense"],
            [2, "1d4", 3, "+10 ft", "Monk Subclass; Techniques, Unarmored Movement"],
            [3, "1d6", 5, "+10 ft", "Improvement; Multiattack (2), Stunning Strike"],
            [4, "1d6", 7, "+15 ft", "Subclass Feature; Improvement; Empowered Strikes, Evasion"],
            [5, "1d6", 9, "+15 ft", "Perfect Motion; Heroic Boon"],
            [6, "1d8", 11, "+20 ft", "Subclass Feature"],
            [7, "1d8", 13, "+20 ft", "Improvement; Astral Teachings, Diamond Soul"],
            [8, "1d8", 15, "+25 ft", "Subclass Feature; Timeless Self"],
            [9, "1d10", 17, "+25 ft", "Improvement; Empty Body"],
            [10, "1d10", 20, "+30 ft", "Epic Boon: Boundless Technique"],
        ],
        "features": [
            {
                "name": "Techniques",
                "level": "2nd-level feature",
                "text": "Spend technique points on Flurry of Blows, Patient Defense, Step of the Wind, and more. Regain points on short or long rest (30 min meditation).",
            },
            {
                "name": "Unarmored Defense",
                "level": "1st-level feature",
                "text": "AC = 10 + Fitness modifier + INS modifier while unarmored and without shield.",
            },
        ],
        "subclasses": ["Flickering Dark", "Open Hand", "Affliction Eater", "Elemental Voice", "Seal Guardian"],
    },
    {
        "id": "paladin",
        "name": "Paladin",
        "summary": "A holy warrior combining martial prowess with divine spells and smites.",
        "max_wd": 10,
        "key_ability": "Fitness (FIT)",
        "saves": "INS (advantage on save)",
        "proficiencies": "All armor, shields, simple and martial weapons.",
        "spellcasting": "Divine spells known (half caster). Oath spells always known.",
        "spell_circles": HALF_CASTER_CIRCLE,
        "spell_start": 2,
        "bfrd_url": "https://bfrd.net/classes/paladin/",
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Divine Sense, Lay on Hands"],
            [2, "Paladin Subclass; Divine Smite, Martial Action, Spellcasting"],
            [3, "Improvement; Multiattack (2)"],
            [4, "Subclass Feature; Improvement; Aura of Protection"],
            [5, "Heroic Boon; Aura of Courage"],
            [6, "Subclass Feature; Channel Divinity (2/rest)"],
            [7, "Improvement; Cleansing Touch"],
            [8, "Subclass Feature; Aura Improvements (30 ft)"],
            [9, "Improvement; Channel Divinity (3/rest)"],
            [10, "Epic Boon: Aura of Salvation"],
        ],
        "features": [
            {
                "name": "Lay on Hands",
                "level": "1st-level feature (action)",
                "text": "Pool of healing equal to 5 × paladin level, restored on long rest. Restore Wounds to a willing creature you touch.",
            },
            {
                "name": "Divine Smite",
                "level": "2nd-level feature",
                "text": "Once per turn on hit, spend Spell Power to deal extra radiant damage (2d8 + 1d8 per circle above 1st, max 5d8; +1d8 vs Fiend/Undead).",
            },
        ],
        "subclasses": ["Devotion", "Justice", "Anathema", "Safekeeping", "Unbound"],
    },
    {
        "id": "ranger",
        "name": "Ranger",
        "summary": "A wilderness hunter marked by mystic quarry and primordial magic.",
        "max_wd": 10,
        "key_ability": "Fitness (FIT)",
        "saves": "FIT (advantage on save)",
        "proficiencies": "Light and medium armor, shields, all weapons; herbalist, navigator, or trapper tools.",
        "spellcasting": "Primordial spells known (half caster).",
        "spell_circles": HALF_CASTER_CIRCLE,
        "spell_start": 2,
        "bfrd_url": "https://bfrd.net/classes/ranger/",
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Explorer, Mystic Mark"],
            [2, "Ranger Subclass; Martial Action, Spellcasting"],
            [3, "Improvement; Multiattack (2); Mystic Mark (d6)"],
            [4, "Subclass Feature; Improvement; Empowered Mark"],
            [5, "Stalker's Step; Heroic Boon"],
            [6, "Subclass Feature; Mystic Mark (d8)"],
            [7, "Improvement; Keensense"],
            [8, "Subclass Feature; Strider"],
            [9, "Improvement; Mystic Mark (d10)"],
            [10, "Epic Boon: Foe Slayer"],
        ],
        "features": [
            {
                "name": "Mystic Mark",
                "level": "1st-level feature",
                "text": "Mark quarry on hit for extra damage (d4→d6→d8→d10). Uses per PB per long rest.",
            },
            {
                "name": "Explorer",
                "level": "1st-level feature",
                "text": "Climbing or swimming speed; advantage tracking; ignore difficult terrain movement penalty.",
            },
        ],
        "subclasses": ["Hunter", "Pack Master", "Arrow Binder", "Shadow", "Trailblazer"],
    },
    {
        "id": "rogue",
        "name": "Rogue",
        "summary": "A skilled infiltrator delivering precision Sneak Attack damage.",
        "max_wd": 8,
        "key_ability": "Fitness (FIT)",
        "saves": "FIT (advantage on save)",
        "proficiencies": "Light armor; simple and martial finesse weapons; thieves' tools; four skills.",
        "bfrd_url": "https://bfrd.net/classes/rogue/",
        "table_headers": ["Level", "Sneak Attack", "Features"],
        "table_rows": [
            [1, "1d6", "Expertise (2), Sneak Attack, Thieves' Cant"],
            [2, "1d6", "Rogue Subclass; Cunning Action (free action)"],
            [3, "2d6", "Improvement; Uncanny Dodge"],
            [4, "3d6", "Subclass Feature; Improvement; Evasion, Expertise (4)"],
            [5, "4d6", "Reliable Talent; Heroic Boon"],
            [6, "5d6", "Subclass Feature; Precise Critical (1 die)"],
            [7, "6d6", "Improvement; Keensense"],
            [8, "7d6", "Subclass Feature; Precise Critical (2 dice)"],
            [9, "8d6", "Improvement; Elusive"],
            [10, "10d6", "Epic Boon: Stroke of Luck"],
        ],
        "features": [
            {
                "name": "Sneak Attack",
                "level": "1st-level feature",
                "text": "Once per turn, extra damage when you have advantage or an ally is within 5 feet of target. Finesse or ranged weapons only.",
            },
            {
                "name": "Cunning Action",
                "level": "2nd-level feature (free action)",
                "text": "Dash, Disengage, or Hide as a free action on your turn.",
            },
        ],
        "subclasses": ["Enforcer", "Thief", "Con Arcanist", "Nightblade", "Trapsmith"],
    },
    {
        "id": "sorcerer",
        "name": "Sorcerer",
        "summary": "An innate spellcaster shaping arcane magic with metamagic and sorcery points.",
        "max_wd": 6,
        "key_ability": "Willpower (WIL)",
        "saves": "WIL (advantage on save)",
        "proficiencies": "Simple weapons.",
        "spellcasting": "Arcane spells known. Sorcery points for metamagic and flexible casting.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": "https://bfrd.net/classes/sorcerer/",
        "table_headers": ["Level", "Sorcery Pts", "Features"],
        "table_rows": [
            [1, 2, "Font of Magic, Spellcasting"],
            [2, 3, "Sorcerer Subclass; Metamagic (2)"],
            [3, 5, "Improvement; Sorcerous Renewal"],
            [4, 7, "Subclass Feature; Improvement; Metamagic (3)"],
            [5, 9, "Heroic Boon"],
            [6, 11, "Subclass Feature; Sorcerous Renewal (2 dice)"],
            [7, 13, "Improvement; Devour Spell"],
            [8, 15, "Subclass Feature; Metamagic (4)"],
            [9, 17, "Improvement; Sorcerous Renewal (3 dice)"],
            [10, 21, "Epic Boon: Arcane Conjunction; Metamagic (5)"],
        ],
        "features": [
            {
                "name": "Metamagic",
                "level": "2nd-level feature",
                "text": "Twist spells with sorcery points. Options include Careful, Quickened, Twinned, Heightened, and more per BFRD.",
            },
            {
                "name": "Font of Magic",
                "level": "1st-level feature",
                "text": "Sorcery points per table; convert points and spell circles per BFRD flexible casting.",
            },
        ],
        "subclasses": ["Chaos", "Draconic", "Abominable", "Cyclonic", "Sacred"],
    },
    {
        "id": "warlock",
        "name": "Warlock",
        "summary": "A pact-bound spellcaster with eldritch invocations and short-rest recovery.",
        "max_wd": 8,
        "key_ability": "Willpower (WIL)",
        "saves": "WIL (advantage on save)",
        "proficiencies": "Light and medium armor, shields, simple weapons.",
        "spellcasting": "Arcane spells (pact magic). Few slots, short-rest recovery. Invocations at 2nd level.",
        "spell_circles": PACT_CASTER_CIRCLE,
        "bfrd_url": "https://bfrd.net/classes/warlock/",
        "table_headers": ["Level", "Slots", "Slot Level", "Features"],
        "table_rows": [
            [1, 1, "1st", "Pact Magic, Eldritch Invocations (2)"],
            [2, 2, "1st", "Warlock Subclass"],
            [3, 2, "2nd", "Improvement; Eldritch Invocations (3)"],
            [4, 2, "2nd", "Subclass Feature; Improvement"],
            [5, 2, "3rd", "Heroic Boon; Eldritch Invocations (4)"],
            [6, 2, "3rd", "Subclass Feature"],
            [7, 2, "4th", "Improvement; Eldritch Invocations (5)"],
            [8, 2, "4th", "Subclass Feature"],
            [9, 2, "5th", "Improvement; Eldritch Invocations (6)"],
            [10, 2, "5th", "Epic Boon"],
        ],
        "features": [
            {
                "name": "Pact Magic",
                "level": "1st-level feature",
                "text": "Few spell slots of your slot level, all slots recovered on short rest. Spells known per BFRD. Also use Spell Power for additional casting per YMIAT magic rules.",
            },
            {
                "name": "Eldritch Invocations",
                "level": "1st-level feature",
                "text": "Choose invocations to customize your pact. Gain more at listed levels.",
            },
        ],
        "subclasses": ["Archfey", "Fiend", "Great Old One", "Archon", "Elemental Regent", "Fey Noble"],
    },
    {
        "id": "wizard",
        "name": "Wizard",
        "summary": "A scholarly arcane caster with a spellbook and ritual mastery.",
        "max_wd": 6,
        "key_ability": "Insight (INS)",
        "saves": "INS (advantage on save)",
        "proficiencies": "Simple weapons.",
        "spellcasting": "Arcane spells (prepared from spellbook). Rituals and rote spells.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": "https://bfrd.net/classes/wizard/",
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Arcane Recovery, Spellcasting"],
            [2, "Wizard Subclass; Magic Sense"],
            [3, "Improvement; Rote Spell (1st)"],
            [4, "Subclass Feature; Improvement; Superior Recovery"],
            [5, "Rote Spell (2nd); Heroic Boon"],
            [6, "Subclass Feature"],
            [7, "Improvement; Rote Spell (3rd); Spellguard"],
            [8, "Subclass Feature"],
            [9, "Improvement; Rote Spell (4th); Spell Mastery"],
            [10, "Epic Boon: Archmage"],
        ],
        "features": [
            {
                "name": "Spellbook",
                "level": "1st-level feature",
                "text": "Prepare INS modifier + wizard level spells from spellbook. Add two spells per level. Arcane Recovery on short rest once per day.",
            },
            {
                "name": "Rote Spell",
                "level": "3rd-level feature",
                "text": "Always-prepared spells at 1st (3rd), 2nd (5th), 3rd (7th), and 4th (9th) circle.",
            },
        ],
        "subclasses": ["Battle Mage", "Cantrip Adept", "Arcanist", "Necromancer", "Summoner"],
    },
    {
        "id": "theurge",
        "name": "Theurge",
        "summary": "A dual-source caster who prepares Arcane and Divine spells from a mystic libram and manipulates magic with Spellcraft.",
        "max_wd": 6,
        "key_ability": "Insight (INS)",
        "saves": "INS (advantage on save)",
        "proficiencies": "Simple weapons. Skills: choose two from Arcana, History, Insight, Investigation, Medicine, and Religion.",
        "spellcasting": "Arcane and Divine spells (prepared from libram). Rituals known per level. Must include spells from both lists when learning.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": TOV_URL,
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Spell Nexus, Spellcasting (Libram)"],
            [2, "Theurge Subclass; Spellcraft, Summon Libram"],
            [3, "Improvement"],
            [4, "Subclass Feature; Improvement"],
            [5, "Spell Synthesis; Heroic Boon"],
            [6, "Subclass Feature; Superior Focus"],
            [7, "Improvement"],
            [8, "Subclass Feature"],
            [9, "Improvement; Spellcraft (d8)"],
            [10, "Epic Boon; Improvement"],
        ],
        "features": [
            {
                "name": "Spell Nexus",
                "level": "1st-level feature",
                "text": "Bonus action while your libram is within 100 feet: swap one prepared spell for another of the same circle and source in your libram. PB uses per long rest.",
            },
            {
                "name": "Libram",
                "level": "1st-level feature (Spellcasting)",
                "text": "Your libram holds Arcane and Divine spells (at least two of each at 1st level). Prepare INS modifier + theurge level spells. Add two spells per level (one Arcane, one Divine). Cantrips from both lists.",
            },
            {
                "name": "Spellcraft",
                "level": "2nd-level feature",
                "text": "Spellcraft dice (d6, d8 at 9th) equal to INS modifier. Spend to boost spell damage/healing, concentration saves, or Arcana checks. Short or long rest recovery.",
            },
            {
                "name": "Spell Synthesis",
                "level": "5th-level feature",
                "text": "Once per rest, cast one Arcane and one Divine prepared spell on the same turn (action + bonus action, or two action spells together). Can't take reactions until your next turn.",
            },
            {
                "name": "Superior Focus",
                "level": "6th-level feature",
                "text": "Maintain concentration on one Arcane and one Divine spell simultaneously. CON save each turn to hold both (disadvantage when damaged).",
            },
            {
                "name": "Improvement",
                "level": "3rd, 5th, 7th, 9th, and 10th level",
                "text": "Increase one ability by 2, two abilities by 1 each, or one ability by 1 and choose a magic talent.",
            },
        ],
        "subclasses": ["Conduit", "Illuminary", "Source Spinner"],
    },
    {
        "id": "vanguard",
        "name": "Vanguard",
        "summary": "A battlefield commander who plants war banners, issues stratagems, and shields allies through tactical leadership.",
        "max_wd": 12,
        "key_ability": "Willpower (WIL)",
        "saves": "WIL (advantage on save)",
        "proficiencies": "All armor, shields, simple and martial weapons. Skills: choose two from Animal Handling, Athletics, History, Insight, Intimidation, Medicine, and Persuasion.",
        "bfrd_url": TOV_URL,
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Born Leader, War Banner"],
            [2, "Vanguard Subclass; Stratagems, Support Action"],
            [3, "Improvement; Multiattack (2)"],
            [4, "Subclass Feature; Improvement"],
            [5, "Superior Stratagems; Heroic Boon"],
            [6, "Subclass Feature; War Banner: Lucky Colors"],
            [7, "Improvement; Manifold Tactic"],
            [8, "Subclass Feature"],
            [9, "Improvement; Valiant Commander, Battlefield Resolve"],
            [10, "Epic Boon; Improvement"],
        ],
        "features": [
            {
                "name": "Born Leader",
                "level": "1st-level feature",
                "text": "Choose Authority (allies within 5 feet add PB damage on weapon hits) or Community (allies within 5 feet gain PB on first save each turn). Gain Intimidation or Persuasion proficiency (double PB if already proficient).",
            },
            {
                "name": "War Banner",
                "level": "1st-level feature (action, in combat)",
                "text": "Plant a mystical banner within 5 feet during encounter play. Choose Banner of Mercy (absorb ally damage) or Black Flag (hinder foes). PB uses per long rest; 15-foot range. Subclasses add banner options.",
            },
            {
                "name": "Stratagems",
                "level": "2nd-level feature",
                "text": "Tactical commands that reposition allies, grant advantage, or disrupt enemies. Known stratagems increase with level; Superior Stratagems (5th) unlocks advanced options.",
            },
            {
                "name": "Support Action",
                "level": "2nd-level feature",
                "text": "Use your Support Action to stabilize dying allies, grant temporary Wounds, or rally companions (see class ability page).",
            },
            {
                "name": "Improvement",
                "level": "3rd, 5th, 7th, 9th, and 10th level",
                "text": "Increase one ability by 2, two abilities by 1 each, or one ability by 1 and choose a martial talent.",
            },
        ],
        "subclasses": ["Bulwark", "Herald", "Marshal"],
    },
    {
        "id": "witch",
        "name": "Witch",
        "summary": "A Wyrd caster who hexes foes, binds spirits, and draws power from otherworldly covens.",
        "max_wd": 8,
        "key_ability": "Willpower (WIL)",
        "saves": "WIL (advantage on save)",
        "proficiencies": "Light armor, simple weapons. Skills: choose two from Arcana, Animal Handling, Insight, Intimidation, Nature, and Religion.",
        "spellcasting": "Wyrd spells (known, not prepared). Rituals known per level. Coven spells from subclass.",
        "spell_circles": FULL_CASTER_CIRCLE,
        "bfrd_url": TOV_URL,
        "table_headers": ["Level", "Features"],
        "table_rows": [
            [1, "Hex (d6), Spellcasting"],
            [2, "Witch Subclass; Shadow Craft, Spirit Binding"],
            [3, "Improvement"],
            [4, "Subclass Feature; Improvement"],
            [5, "Greater Hex; Heroic Boon"],
            [6, "Subclass Feature"],
            [7, "Improvement"],
            [8, "Subclass Feature"],
            [9, "Improvement; Otherworldly Form"],
            [10, "Epic Boon; Improvement"],
        ],
        "features": [
            {
                "name": "Hex",
                "level": "1st-level feature",
                "text": "Bonus action: mark a creature with a Hex die (d6, d8 at 5th, d10 at 9th). Spend the die to reduce attack rolls, ability checks, or saves. WIL modifier uses per long rest.",
            },
            {
                "name": "Spellcasting",
                "level": "1st-level feature",
                "text": "Wyrd spells known (no preparation). Willpower is your spellcasting ability. Cantrips and rituals per progression table.",
            },
            {
                "name": "Shadow Craft",
                "level": "2nd-level feature",
                "text": "Weave minor illusions and obscuring magic tied to your coven. Options expand at 6th and 9th level.",
            },
            {
                "name": "Spirit Binding",
                "level": "2nd-level feature",
                "text": "Bind helpful spirits for scouting, spell delivery, and coven rites. Number of bound spirits increases at 6th and 13th (9th in YMIAT).",
            },
            {
                "name": "Greater Hex",
                "level": "5th-level feature",
                "text": "When you give a creature a Hex die, it also has disadvantage on the first attack roll against you before the die is spent.",
            },
            {
                "name": "Improvement",
                "level": "3rd, 5th, 7th, 9th, and 10th level",
                "text": "Increase one ability by 2, two abilities by 1 each, or one ability by 1 and choose a magic talent.",
            },
        ],
        "subclasses": ["Crimson Cord", "Night Song", "Twilight Soul"],
    },
]

GLANCE_ROWS = [
    ["Barbarian", "12", "FIT", "FIT (advantage)", "Martial"],
    ["Bard", "8", "WIL", "WIL (advantage)", "Arcane"],
    ["Cleric", "8", "INS", "INS (advantage)", "Divine"],
    ["Druid", "8", "INS", "INS (advantage)", "Primordial"],
    ["Fighter", "10", "FIT", "FIT (advantage)", "Martial"],
    ["Artificer", "8", "INS", "INS (advantage)", "Martial/Utility"],
    ["Monk", "8", "FIT", "FIT (advantage)", "Martial"],
    ["Paladin", "10", "FIT", "INS (advantage)", "Divine/Martial"],
    ["Ranger", "10", "FIT", "FIT (advantage)", "Primordial/Martial"],
    ["Rogue", "8", "FIT", "FIT (advantage)", "Martial"],
    ["Sorcerer", "6", "WIL", "WIL (advantage)", "Arcane"],
    ["Warlock", "8", "WIL", "WIL (advantage)", "Arcane"],
    ["Theurge", "6", "INS", "INS (advantage)", "Arcane/Divine"],
    ["Vanguard", "12", "WIL", "WIL (advantage)", "Martial"],
    ["Witch", "8", "WIL", "WIL (advantage)", "Wyrd"],
    ["Wizard", "6", "INS", "INS (advantage)", "Arcane"],
]

HTML_HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Classes | You-Meet-In-A-Tavern (YMIAT)</title>
<meta name="description" content="Character classes for You-Meet-In-A-Tavern (YMIAT), adapted from Black Flag for 10-level play." />
<link rel="canonical" href="rules/classes.html" />
<link rel="stylesheet" href="../assets/styles.css" />
<script src="../assets/includes.js"></script>
<meta property="og:title" content="Classes | You-Meet-In-A-Tavern (YMIAT)" />
<meta property="og:description" content="Character classes for You-Meet-In-A-Tavern (YMIAT)." />
<meta property="og:type" content="website" />
<meta property="og:url" content="rules/classes.html" />
</head>
<body>
<header data-include="nav"></header>
<main>
  <h1>Character Classes</h1>
  <div class="content">
    <p class="lede">Every adventurer has a class that defines their heroic capabilities. <strong>You-Meet-In-A-Tavern</strong> (YMIAT) adapts classes from <a href="{TOV_URL}" rel="noopener">Tales of the Valiant</a> and the <a href="https://bfrd.net/classes/" rel="noopener">Black Flag Reference Document</a>, compressing 20-level progression into <strong>10 meaningful levels</strong>, using Fitness, Insight, and Willpower instead of traditional six abilities.</p>
    <p>Subclass features arrive at <strong>2nd, 4th, 6th, and 8th</strong> level. Improvement (talents or ability increases) arrives at <strong>3rd, 5th, 7th, 9th, and 10th</strong> level. Casters use <a href="core.html#magic-and-spell-resources">Spell Power</a> and max spell circles per level instead of daily spell slots. Each class lists <strong>one</strong> save with advantage—the class's primary saving throw. Progression features link to the <a href="class-abilities/index.html">class ability pages</a> (one page per class).</p>

    <h2 id="classes-at-a-glance">Classes at a Glance</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Class</th><th>Max WD</th><th>Key Ability</th><th>Saves</th><th>Spell Source</th></tr></thead>
      <tbody>
"""

HTML_MID = """      </tbody>
    </table></div>

    <div class="lineages-controls">
      <button id="expand-all-classes" class="lineage-control-btn" onclick="expandAllClasses()">Expand All</button>
      <button id="collapse-all-classes" class="lineage-control-btn" onclick="collapseAllClasses()">Collapse All</button>
    </div>

    <div class="lineages-container">
"""

HTML_FOOT = """    </div>
  </div>
</main>
<footer class="legal" data-include="footer"></footer>
<script>
function classItems(){
  return document.querySelectorAll('.lineages-container > .lineage-item');
}
function setClassExpanded(item, expanded){
  const content = item.querySelector('.lineage-content');
  const btn = item.querySelector('.lineage-header');
  if(!content || !btn) return;
  const icon = btn.querySelector('.lineage-toggle-icon');
  content.classList.toggle('expanded', expanded);
  content.style.removeProperty('display');
  icon.textContent = expanded ? '▲' : '▼';
  btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
}
function collapseAllClasses(){
  classItems().forEach(function(item){ setClassExpanded(item, false); });
}
function expandClassFromHash(){
  const raw = window.location.hash;
  if(!raw || raw.length < 2) return;
  const target = document.getElementById(decodeURIComponent(raw.slice(1)));
  if(!target || !target.classList.contains('lineage-item') || !target.closest('.lineages-container')) return;
  collapseAllClasses();
  setClassExpanded(target, true);
  requestAnimationFrame(function(){
    target.scrollIntoView({behavior:'smooth', block:'start'});
  });
}
function toggleClass(button){
  const item = button.closest('.lineage-item');
  if(!item) return;
  const content = item.querySelector('.lineage-content');
  setClassExpanded(item, !content.classList.contains('expanded'));
}
function expandAllClasses(){
  classItems().forEach(function(item){ setClassExpanded(item, true); });
}
document.addEventListener('DOMContentLoaded', function(){
  collapseAllClasses();
  expandClassFromHash();
  window.addEventListener('hashchange', expandClassFromHash);
  const glance = document.getElementById('classes-at-a-glance');
  if(glance){
    glance.addEventListener('click', function(event){
      const link = event.target.closest('a[href^="#"]');
      if(!link) return;
      window.setTimeout(expandClassFromHash, 0);
    });
  }
  initAbilityTooltips();
});
function initAbilityTooltips(){
  let tipEl = document.getElementById('ability-hover-tip');
  if(!tipEl){
    tipEl = document.createElement('div');
    tipEl.id = 'ability-hover-tip';
    tipEl.setAttribute('role', 'tooltip');
    tipEl.hidden = true;
    document.body.appendChild(tipEl);
  }
  let active = null;
  function position(link){
    const rect = link.getBoundingClientRect();
    const margin = 8;
    let left = rect.left;
    let top = rect.bottom + margin;
    tipEl.style.left = left + 'px';
    tipEl.style.top = top + 'px';
    const box = tipEl.getBoundingClientRect();
    if(box.right > window.innerWidth - margin){
      left -= box.right - window.innerWidth + margin;
      tipEl.style.left = Math.max(margin, left) + 'px';
    }
    if(box.bottom > window.innerHeight - margin){
      tipEl.style.top = Math.max(margin, rect.top - box.height - margin) + 'px';
    }
  }
  function show(link){
    const text = link.getAttribute('data-tip');
    if(!text) return;
    active = link;
    tipEl.textContent = text;
    tipEl.hidden = false;
    position(link);
  }
  function hide(){
    active = null;
    tipEl.hidden = true;
  }
  document.querySelectorAll('.ability-tip[data-tip]').forEach(function(link){
    link.removeAttribute('title');
    link.addEventListener('mouseenter', function(){ show(link); });
    link.addEventListener('focus', function(){ show(link); });
    link.addEventListener('mouseleave', hide);
    link.addEventListener('blur', hide);
    link.addEventListener('mousemove', function(){ if(active === link) position(link); });
  });
}
</script>
<script src="../assets/site.js"></script>
</body>
</html>
"""


def main():
    parts = [HTML_HEAD]
    for row in GLANCE_ROWS:
        name, wd, key, saves, spell = row
        link = name.lower().replace("artificer", "artificer")
        cid = "artificer" if name == "Artificer" else name.lower()
        parts.append(
            f'        <tr><td><a href="#{cid}">{name}</a></td><td>{wd}</td><td>{key}</td><td>{saves}</td><td>{spell}</td></tr>\n'
        )
    parts.append(HTML_MID)
    for cls in CLASSES:
        parts.append(render_class(cls))
        parts.append("\n")
    parts.append(HTML_FOOT)
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({len(CLASSES)} classes)")


if __name__ == "__main__":
    main()
