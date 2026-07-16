#!/usr/bin/env python3
"""ToV-sourced character options for YMIAT (backgrounds, talents, lineages)."""

from __future__ import annotations

import re


def adapt_tov(text: str) -> str:
    """Map ToV terminology to YMIAT where straightforward."""
    if not text:
        return text
    out = text
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
        ("1 Luck", "1 Resolve"),
        ("2 Luck", "2 Resolve"),
        ("Luck total", "Resolve total"),
        (" Luck", " Resolve"),
        ("technical talents", "utility talents"),
        ("Technical talents", "Utility talents"),
        ("spell slots", "spell levels"),
        ("Spell slots", "Spell levels"),
        ("spell slot", "spell level"),
        ("Spell slot", "Spell level"),
    ]
    for old, new in pairs:
        out = out.replace(old, new)
    return out


def _bg(name: str, body: str) -> dict:
    return {"name": name, "body": adapt_tov(body)}


BACKGROUNDS = [
    _bg(
        "Adherent",
        """<p>Before you began adventuring, you committed yourself to a faith, belief, or cause. Skill, equipment, and devotion from that life still shape you.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from History, Investigation, Religion, or Persuasion.</p>
<p><strong>Additional Proficiencies:</strong> Artist's tools and one additional tool of your choice.</p>
<p><strong>Equipment:</strong> A prayer book or ceremonial dagger, a holy symbol, fragrant incense, vestments, common clothes, and a pouch containing 10 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Field Medic</em>, <em>Mental Fortitude</em>, or <em>Ritualist</em>.</p>""",
    ),
    _bg(
        "Alchemist",
        """<p>You combine natural and alchemical components to create wonders—potions, poisons, and transformative substances.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Arcana, Investigation, Nature, or Perception.</p>
<p><strong>Additional Proficiencies:</strong> Alchemist's tools and one of charlatan's tools, herbalism tools, or provisioner's tools.</p>
<p><strong>Equipment:</strong> Common clothes, alchemist's tools, stained gloves, a flask of alchemist's fire, glass vials, and a coin purse with 5 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Alchemy Adept</em>, <em>Elemental Savant</em>, or <em>Learned Researcher</em>.</p>""",
    ),
    _bg(
        "Artist",
        """<p>You doggedly practiced an artistic pursuit before adventuring—acrobat, puppeteer, thespian, singer, or similar.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Acrobatics, Insight, Performance, or Persuasion.</p>
<p><strong>Additional Proficiencies:</strong> One additional language and one tool representing your art.</p>
<p><strong>Equipment:</strong> A musical instrument or artisan tool, steel mirror, fine clothes, ink and quill, and 4 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Quick</em>, <em>Scrutinous</em>, or <em>Trade Skills</em>.</p>""",
    ),
    _bg(
        "Chronicler",
        """<p>You documented the world—records, investigations, or daily life preserved for posterity.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from History, Investigation, Perception, or Persuasion.</p>
<p><strong>Additional Proficiencies:</strong> One additional language and artist's, navigator's, or provisioner's tools.</p>
<p><strong>Equipment:</strong> Proficient tools from above, ink and 25 sheets of paper, bedroll, common clothes, and 3 gp in small coin.</p>
<p><strong>Talent:</strong> Choose one: <em>Learned Researcher</em>, <em>Polyglot</em>, or <em>Spell Recall</em>.</p>""",
    ),
    _bg(
        "Courtier",
        """<p>You spent years in royal or noble courts, learning decorum, duty, and the station of others.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from History, Religion, Insight, or Deception.</p>
<p><strong>Additional Proficiencies:</strong> One additional language, artist's or navigator's tools, and a musical instrument.</p>
<p><strong>Equipment:</strong> A writ of nobility or patronage, signet ring, fine clothes, and 12 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Combat Conditioning</em>, <em>Mental Fortitude</em>, or <em>Polyglot</em>.</p>""",
    ),
    _bg(
        "Criminal",
        """<p>You survived the criminal underworld as cutpurse, grifter, thief, or assassin.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Stealth, Investigation, Insight, or Deception.</p>
<p><strong>Additional Proficiencies:</strong> Thieves' Cant (or another language if you already know it), plus one tool and one vehicle.</p>
<p><strong>Equipment:</strong> Five pieces of chalk, grappling hook, dark traveler's clothes or costume, and 10 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Covert</em>, <em>Scrutinous</em>, or <em>Touch of Luck</em>.</p>""",
    ),
    _bg(
        "Gravedigger",
        """<p>You put the dead to rest—city graveyards, crypts, or lonely burial grounds.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Athletics, Insight, Nature, or Religion.</p>
<p><strong>Additional Proficiencies:</strong> Construction tools and either scythes or thieves' tools.</p>
<p><strong>Equipment:</strong> Common clothes, construction tools, holy water, small shovel, a burial keepsake, and 2 gp in copper and silver.</p>
<p><strong>Talent:</strong> Choose one: <em>Empathetic</em>, <em>Hardy</em>, or <em>Mental Fortitude</em>.</p>""",
    ),
    _bg(
        "Healer",
        """<p>You cared for your community with herbal remedies, charms, and practical lore.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Arcana, Insight, Medicine, or Survival.</p>
<p><strong>Additional Proficiencies:</strong> Herbalism tools and one additional tool.</p>
<p><strong>Equipment:</strong> Herbalism tools, healer's kit, candle, potion bottles, common clothes, and 5 days of rations.</p>
<p><strong>Talent:</strong> Choose one: <em>Empathetic</em>, <em>Field Medic</em>, or <em>Ritualist</em>.</p>""",
    ),
    _bg(
        "Homesteader",
        """<p>You forged a livelihood between civilization and the wild hinterlands.</p>
<p><strong>Skill Proficiencies:</strong> Survival and one of Athletics, Animal Handling, or Intimidation.</p>
<p><strong>Additional Proficiencies:</strong> Herbalism or navigator's tools.</p>
<p><strong>Equipment:</strong> Hunting trap, fishing tackle, skinning knife, canvas hammock, heavy traveler's clothes, and 8 gp of gold-crusted quartz.</p>
<p><strong>Talent:</strong> Choose one: <em>Aware</em>, <em>Dungeoneer</em>, or <em>Far Traveler</em>.</p>""",
    ),
    _bg(
        "Investigator",
        """<p>You solved problems for pay—authority, clients, or yourself.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Deception, Insight, Investigation, or Perception.</p>
<p><strong>Additional Proficiencies:</strong> Charlatan's and thieves' tools.</p>
<p><strong>Equipment:</strong> Common and fine clothes, charlatan's or thieves' tools, letter of reference, magnifying glass, notebook, case memento, and two purses of 5 gp each.</p>
<p><strong>Talent:</strong> Choose one: <em>Scrutinous</em>, <em>Situational Awareness</em>, or <em>Sleuth</em>.</p>""",
    ),
    _bg(
        "Maker",
        """<p>You pursued a craft until expert quality defined your reputation.</p>
<p><strong>Skill Proficiencies:</strong> Investigation and one of History, Performance, or Sleight of Hand.</p>
<p><strong>Additional Proficiencies:</strong> One tool; double proficiency bonus on checks with that tool.</p>
<p><strong>Equipment:</strong> That tool, personal emblem stamp or chisel, traveler's clothes, and 10 gp in shavings or dust.</p>
<p><strong>Talent:</strong> Choose one: <em>Artillerist</em>, <em>School Specialization</em>, or <em>Trade Skills</em>.</p>""",
    ),
    _bg(
        "Outcast",
        """<p>You survived on scraps and street skills, sometimes on the wrong side of the law.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Deception, Insight, Sleight of Hand, or Stealth.</p>
<p><strong>Additional Proficiencies:</strong> One gaming set and charlatan's, herbalism, or thieves' tools.</p>
<p><strong>Equipment:</strong> Dark cloak and clothes, a silver coin from a stranger, and 10 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Aware</em>, <em>Opportunist</em>, or <em>Quick</em>.</p>""",
    ),
    _bg(
        "Rebel",
        """<p>You fought for your beliefs against the status quo—openly or from the shadows.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from History, Insight, Performance, or Persuasion.</p>
<p><strong>Additional Proficiencies:</strong> Artist's or alchemist's tools and provisioner's tools, a musical instrument, or Thieves' Cant.</p>
<p><strong>Equipment:</strong> Common clothes, artist's or alchemist's tools, flag or banner, pamphlets, alchemist's fire, and 3 gp in small coin.</p>
<p><strong>Talent:</strong> Choose one: <em>Brave</em>, <em>Comrade</em>, or <em>Hard to Kill</em>.</p>""",
    ),
    _bg(
        "Rustic",
        """<p>Years of hard work gave you unshakeable resolve, but no grand mysteries in your past.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Athletics, Acrobatics, Investigation, or Medicine.</p>
<p><strong>Additional Proficiencies:</strong> Land vehicles and one martial weapon, instrument, tool, or armor type.</p>
<p><strong>Equipment:</strong> Backpack, bedroll, woven blanket, three candles, traveler's clothes, and 20 sp.</p>
<p><strong>Talent:</strong> Choose one: <em>Comrade</em>, <em>Hand to Hand</em>, or <em>Physical Fortitude</em>.</p>""",
    ),
    _bg(
        "Scholar",
        """<p>Years in academic pursuits honed your mind and intellectual lens on the world.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Arcana, History, Nature, or Religion.</p>
<p><strong>Additional Proficiencies:</strong> Two languages or one tool or vehicle relevant to your field.</p>
<p><strong>Equipment:</strong> Ink, quill, knife, reference book, common clothes, and 10 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Polyglot</em>, <em>Ritualist</em>, or <em>School Specialization</em>.</p>""",
    ),
    _bg(
        "Servant",
        """<p>You anticipated others' needs while working behind the scenes for employers.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Insight, Perception, Sleight of Hand, or Stealth.</p>
<p><strong>Additional Proficiencies:</strong> Two of clothier's, provisioner's, thieves', tinkerer's tools, or a musical instrument.</p>
<p><strong>Equipment:</strong> Common clothes, sturdy shoes, proficient tools, notebook, employer's essential item, and 3 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Hardy</em>, <em>Quick</em>, or <em>Tag Team</em>.</p>""",
    ),
    _bg(
        "Smuggler",
        """<p>You moved contraband where it was forbidden, by wit and careful planning.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Deception, Persuasion, Sleight of Hand, or Stealth.</p>
<p><strong>Additional Proficiencies:</strong> Thieves' Cant (or another language), navigator's tools, and one vehicle.</p>
<p><strong>Equipment:</strong> Navigator's tools, magnifying glass, merchant's scale, common and fine clothes, hooded cloak, lantern, empty pouches, and 10 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Covert</em>, <em>Escamotage</em>, or <em>Slippery</em>.</p>""",
    ),
    _bg(
        "Soldier",
        """<p>Rigorous training and discipline defined your time in military service.</p>
<p><strong>Skill Proficiencies:</strong> Choose two from Animal Handling, Athletics, Medicine, or Survival.</p>
<p><strong>Additional Proficiencies:</strong> One tool and one vehicle.</p>
<p><strong>Equipment:</strong> Symbol of rank, mess kit, playing cards or dice, common clothes, and 10 gp.</p>
<p><strong>Talent:</strong> Choose one: <em>Combat Casting</em>, <em>Combat Conditioning</em>, or <em>Field Medic</em>.</p>""",
    ),
]


def _talent(category: str, name: str, body: str, prereq: str | None = None) -> dict:
    entry = {"category": category, "name": name, "body": adapt_tov(body)}
    if prereq:
        entry["prereq"] = adapt_tov(prereq)
    return entry


TALENTS = [
    # --- Magic (existing + ToV) ---
    _talent("magic", "Arcanist", """<ul>
<li>Double proficiency bonus on Arcana checks.</li>
<li>Once per rest, replace one known cantrip or spell (not from a spellbook) with another of the same level from your source list.</li>
<li>Learn one additional cantrip from your spellcasting source.</li></ul>""", "Spellcasting class feature"),
    _talent("magic", "Combat Casting", """<ul>
<li>On Fitness saves to maintain concentration, treat d20 rolls of 7 or less as 8.</li>
<li>When a creature provokes an opportunity attack, cast a cantrip with your reaction instead of a melee attack.</li>
<li>Use a shield or weapon as a spellcasting focus.</li></ul>"""),
    _talent("magic", "Elemental Savant", """<p>Choose acid, cold, fire, lightning, or thunder. When you cast a spell that deals damage, you may convert its damage type to your chosen type. When rolling damage for spells that naturally use that type, reroll 1s on damage dice. Selectable multiple times for different types.</p>""", "Ability to cast at least one damaging spell"),
    _talent("magic", "Mental Fortitude", """<ul>
<li>Once per short rest, reroll a failed Insight or Willpower save.</li>
<li>When you start your turn charmed, frightened, paralyzed, or stunned, gain 1 Resolve.</li></ul>"""),
    _talent("magic", "Ritualist", """<p>Gain a ritual book. Choose Arcane, Divine, Primordial, or Wyrd as your ritual source. Add one ritual per spell level you have unlocked; add another when you gain access to a new level.</p>""", "Spellcasting class feature"),
    _talent("magic", "School Specialization", """<ul>
<li>+1 to spell attack and save DC for your chosen school.</li>
<li>Halve gold and time to copy spells of that school into a spellbook.</li>
<li>When spending 2+ sorcery points on a spell of that school, regain 1 sorcery point at end of turn.</li></ul>
<p>Selectable multiple times for different schools.</p>"""),
    _talent("magic", "Spell Duelist", """<ul>
<li>When damaged by a spell, react to cast a cantrip at the attacker.</li>
<li>Spell attacks ignore half/three-quarters cover; touch range becomes 15 feet; double spell range otherwise.</li></ul>""", "Ability to cast one or more cantrips"),
    _talent("magic", "Chaos Caster", """<p>When casting with Spell Power, attempt to cast as one level higher (ability check vs DC 11 + base level). On success, roll on the Volatile Spell Effect table. Uses per long rest equal to proficiency bonus.</p>""", "Spellcasting class feature"),
    _talent("magic", "Spell Recall", """<ul>
<li>Prepare additional spells equal to half proficiency bonus (rounded down).</li>
<li>As a bonus action, swap one prepared spell for another (ability check DC 10 + level or lose the attempt).</li></ul>""", "Prepared spellcaster (Cleric, Druid, Theurge, or Wizard)"),
    _talent("magic", "Magical Trickster", """<ul>
<li>Learn <em>minor illusion</em> and <em>prestidigitation</em> or <em>thaumaturgy</em> (no components; double range).</li>
<li>As a bonus action, impose disadvantage on one creature's next attack (Willpower save); uses per day equal to proficiency bonus.</li></ul>"""),
    # --- Martial ---
    _talent("martial", "Armor Expert", """<ul>
<li>While wearing medium or heavy armor you're proficient with: +1 Defense, advantage on Fitness saves vs. pull/shove/prone.</li></ul>""", "Fitness +1 or higher"),
    _talent("martial", "Armor Training", """<ul>
<li>Gain next armor proficiency step (light→medium→heavy and shields).</li>
<li>No disadvantage on Stealth in medium armor; add up to +3 Fitness to Defense in medium armor.</li></ul>""", "Proficiency with light or medium armor"),
    _talent("martial", "Athletic", """<ul>
<li>Double proficiency on Athletics checks.</li>
<li>Increased carry/push/lift capacity; stand from prone for 5 ft movement; +10 ft running long jump, +3 ft high jump.</li></ul>"""),
    _talent("martial", "Artillerist", """<ul>
<li>Ignore Loading on proficient ranged weapons.</li>
<li>Advantage on siege weapon attacks.</li>
<li>With advantage on a ranged attack, reroll one d20.</li></ul>""", "Fitness +1 or higher"),
    _talent("martial", "Brave", """<ul>
<li>Advantage on saves vs. fear; inspire ally within 5× proficiency bonus feet with advantage on one fear save.</li>
<li>Once per long rest, end frightened on yourself or an ally within 5 feet as a bonus action.</li></ul>"""),
    _talent("martial", "Combat Conditioning", """<ul>
<li>Max Wounds +2 per character level (retroactive and on future levels).</li>
<li>+1 maximum Recovery Point; regain all Recovery Points on a long rest.</li></ul>"""),
    _talent("martial", "Critical Training", """<ul>
<li>Critical hit on 19–20 with weapons.</li>
<li>On weapon crits, add the attack ability modifier to damage an extra time.</li></ul>"""),
    _talent("martial", "Hand to Hand", """<ul>
<li>Unarmed strikes deal 1d6 + Fitness modifier.</li>
<li>Proficiency with improvised weapons (1d8 one-hand, 1d10 two-hand minimum).</li>
<li>Advantage on grapple checks; grappled foes take Fitness modifier bludgeoning at start of your turn.</li></ul>"""),
    _talent("martial", "Opportunist", """<ul>
<li>Advantage on opportunity attacks.</li>
<li>Opportunity attacks when foes stand from prone or Use an Object.</li></ul>"""),
    _talent("martial", "Physical Fortitude", """<ul>
<li>Once per turn, reroll a failed Fitness save by spending a Recovery Point.</li>
<li>Gain 1 Resolve when you start blinded, deafened, restrained, or poisoned.</li>
<li>Advantage vs. prone, pull, or push.</li></ul>"""),
    _talent("martial", "Return Fire", """<p>When a visible attacker hits or misses you with a ranged attack, react with a ranged or thrown weapon attack if in range.</p>"""),
    _talent("martial", "Spell Hunter", """<ul>
<li>React with melee attack when a reachable foe casts; extra damage equal to spell level (crit interrupts spell).</li>
<li>Advantage on saves vs. their spells within 5 feet; they have disadvantage on concentration.</li>
<li>Grappled creatures can't cast spells requiring somatic components.</li></ul>"""),
    _talent("martial", "Vanguard", """<ul>
<li>React with melee attack when a foe in reach attacks someone else.</li>
<li>Opportunity attacks when creatures leave reach even without provoking.</li>
<li>Readied melee attacks gain +proficiency bonus; on hit, target's speed becomes 0 until end of its next turn.</li></ul>"""),
    _talent("martial", "Weapon Discipline", """<p>Choose one proficient simple or martial weapon: +1 attack and damage; extra weapon die on crit; temp Wounds equal to proficiency bonus when you drop a foe with that weapon.</p>""", "Proficiency with at least one martial weapon"),
    # --- Utility ---
    _talent("utility", "Alchemy Adept", """<ul>
<li>Double proficiency on alchemist's tool checks.</li>
<li>Craft alchemical items faster during downtime; proficient with alchemical ranged attacks using Fitness or Insight.</li>
<li>+proficiency bonus to concoction save DC; range 30/60 ft.</li></ul>""", "Proficiency with alchemist's tools"),
    _talent("utility", "Aware", """<ul>
<li>On initiative, treat d20 rolls of 9 or less as 10.</li>
<li>Can't be surprised while conscious.</li>
<li>Hidden attackers don't gain advantage against you.</li></ul>"""),
    _talent("utility", "Bottomless Luck", """<ul>
<li>When you roll 20 on a d20, one ally who can see or hear you gains 1 Resolve.</li>
<li>When resetting Resolve, roll d20 in four bands (see core rules) and keep the better of two rolls if you roll twice.</li>
<li>When spending Resolve to reroll, roll twice and keep the better result.</li></ul>"""),
    _talent("utility", "Comrade", """<ul>
<li>Help as a bonus action.</li>
<li>Spend Resolve to boost an ally's roll within 30 feet.</li>
<li>When an ally within 30 feet fails a death save or reaches Max Wounds, gain 2 Resolve.</li></ul>"""),
    _talent("utility", "Covert", """<ul>
<li>Hide in three-quarters cover or while lightly obscured.</li>
<li>Darkvision users can't see you while motionless in dim light or darkness.</li>
<li>No disadvantage attacking or perceiving in dim light.</li>
<li>Reaction Stealth vs. Perception to stay hidden after being spotted (once per creature per 24 hours).</li></ul>""", "Stealth proficiency, Fitness +1"),
    _talent("utility", "Dungeoneer", """<ul>
<li>Add proficiency bonus to disarm traps/open doors even without tools; first failure on traps doesn't trigger them.</li>
<li>Advantage finding secrets, traps, and illusions; advantage vs. traps and hazards; resistance to trap/hazard damage.</li>
<li>At combat start, you and allies within 5 feet may roll Stealth for surprise.</li></ul>"""),
    _talent("utility", "Empathetic", """<ul>
<li>Discern simple intent from body language in unknown languages.</li>
<li>+5 passive Insight; proficiency in Persuasion (or double proficiency).</li>
<li>After 10 minutes of friendly conversation, advantage on Willpower (Persuasion) checks.</li></ul>"""),
    _talent("utility", "Escamotage", """<ul>
<li>Proficiency in Sleight of Hand (or double proficiency).</li>
<li>Spend 2 Resolve to reroll Sleight of Hand checks.</li>
<li>Action to pick a visible worn nonmagical item (DC 10 + target's Fitness bonus + CR).</li></ul>"""),
    _talent("utility", "Far Traveler", """<ul>
<li>Travel 10 hours/day before forced march saves; fast pace doesn't reduce passive Perception.</li>
<li>Advantage on Survival checks to avoid getting lost.</li>
<li>Ignore one level of exhaustion.</li></ul>"""),
    _talent("utility", "Field Medic", """<ul>
<li>On Medicine checks, treat d20 rolls of 9 or less as 10.</li>
<li>Action: heal Wounds equal to proficiency bonus + Fitness modifier (once per target per rest).</li>
<li>When spending Recovery Points on a short rest, reroll up to proficiency bonus dice.</li></ul>"""),
    _talent("utility", "Hardy", """<ul>
<li>Once per long rest, drop to 1 Wound instead of 0 when reduced to 0 Wounds.</li>
<li>Advantage on checks to avoid or reduce exhaustion; once per long rest ignore gaining a level of exhaustion.</li></ul>""", "Fitness +1 or higher"),
    _talent("utility", "Learned Researcher", """<p>Choose two of Arcana, History, Nature, or Religion: treat d20 rolls of 9 or less as 10 (uses per day = proficiency bonus). Downtime research costs and time divided by proficiency bonus; advantage on research resolution rolls.</p>"""),
    _talent("utility", "Polyglot", """<ul>
<li>Learn three languages.</li>
<li>Once per long rest, advantage on one Willpower check to influence a creature you share a non-Common language with.</li>
<li>Add proficiency bonus when deciphering unknown languages (double if also proficient in relevant skill/tool).</li></ul>"""),
    _talent("utility", "Quick", """<ul>
<li>+10 ft speed without medium/heavy armor.</li>
<li>Dash along vertical surfaces; reduce fall distance by 5× proficiency bonus as a reaction.</li>
<li>Bonus action: move 5 feet without provoking opportunity attacks.</li></ul>"""),
    _talent("utility", "Scrutinous", """<ul>
<li>Read lips in languages you know.</li>
<li>+5 passive Perception and Investigation.</li>
<li>After 1 minute examining an object, ask the GM one truthful question about it.</li>
<li>Mimic voices after hearing speech for 1 minute.</li></ul>"""),
    _talent("utility", "Situational Awareness", """<ul>
<li>Advantage on checks to avoid surprise.</li>
<li>After melee damage, react to move 10 feet without provoking opportunity attacks.</li></ul>"""),
    _talent("utility", "Sleuth", """<p>Choose two of Insight, Investigation, Perception, or Survival: treat 9 or less as 10. After 1 minute talking with a creature, produce a <em>zone of truth</em> effect (uses per day = proficiency bonus).</p>""", "Insight +1 or Willpower +1"),
    _talent("utility", "Slippery", """<ul>
<li>First 5× proficiency bonus feet of difficult terrain each move costs normal movement.</li>
<li>Advantage to avoid and end grappled.</li></ul>"""),
    _talent("utility", "Tag Team", """<p>Mark an enemy within 30 feet for 1 minute. If you miss a melee attack against the mark without disadvantage, the next ally to attack it has advantage. Once per short or long rest.</p>"""),
    _talent("utility", "Touch of Luck", """<ul>
<li>When you would gain 1 Resolve from a failed save or attack, gain 2 instead.</li>
<li>At 4 Resolve, when you would gain more, reset Resolve using the d20 band table in core rules.</li></ul>"""),
    _talent("utility", "Trade Skills", """<ul>
<li>Gain proficiency in one skill and related tool/vehicle (or two tools/vehicles).</li>
<li>Double proficiency on one chosen skill.</li>
<li>Advantage when both a proficient tool and skill apply.</li></ul>"""),
    _talent("utility", "Trailblazer", """<ul>
<li>Climb and swim speeds equal to walking speed.</li>
<li>Advantage on exhaustion checks while climbing or swimming.</li>
<li>Hold breath for 1 + twice Fitness modifier minutes.</li></ul>"""),
]


def _lineage(name: str, body: str, *, tov: bool = True, tag: str | None = None) -> dict:
    entry = {"name": name, "body": adapt_tov(body), "tov": tov}
    if tag:
        entry["tag"] = tag
    return entry


LINEAGES = [
    _lineage("Beastkin", """<p><strong>Age.</strong> Adulthood within 5 years; lifespan up to a century (some only 20–30 years).</p>
<p><strong>Size.</strong> Medium or Small (under 4 feet tall → Small).</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Animal Instinct.</strong> Proficiency in Perception or Survival.</p>
<p><strong>Natural Weapons.</strong> Unarmed strikes deal 1 Wound + Fitness modifier (work with your GM on damage type).</p>
<p><strong>Natural Adaptation.</strong> Choose one: Avian (fly speed = walk), Agile (climb speed = walk; advantage vs. prone), Aquatic (swim speed = walk; hold breath 20 min), or Sturdy (AC 13 + Fitness without armor; count as one size larger for carry capacity).</p>
<p><em>PG2 expansion:</em> Fossorial (burrow 20 ft through soft earth) or Quillback (reaction quill strike when hit in melee).</p>"""),
    _lineage("Dhampir", """<p>Children of vampires and mortals—compelling or repulsive to those they meet.</p>
<p><strong>Age.</strong> Mature in late teens; can live up to 750 years.</p>
<p><strong>Size.</strong> Medium or Small.</p>
<p><strong>Speed.</strong> 30 feet walk, 30 feet climb (hands free).</p>
<p><strong>Dark Thirst.</strong> Bite: 1 Wound piercing; optional feed for +1 Wound necrotic, temp Wounds, and advantage on your next attack.</p>
<p><strong>Darkvision.</strong> 60 feet; disadvantage on Insight (Perception) by sight in sunlight.</p>
<p><strong>Hybrid Humanoid.</strong> Advantage vs. poisoned and exhaustion checks.</p>""", tag="PG2"),
    _lineage("Dragonborn", """<p>Draconic humanoids with breath weapons and scaled hides.</p>
<p><strong>Age.</strong> Adult by 15; ~80 years.</p>
<p><strong>Size.</strong> Medium (~6–7 ft, ~300 lb).</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Breath Weapon.</strong> Bonus action: 30×5 ft line or 15-ft cone (Fitness save); 1 Wound on fail, none on success; damage type by ancestry; scales at higher levels. Uses = proficiency bonus per long rest.</p>
<p><strong>Draconic Ancestry.</strong> Black/Copper acid, Blue/Bronze lightning, Brass/Gold/Red fire, Green poison, Silver/White cold, Void necrotic, Yellow radiant.</p>
<p><strong>Dragon Hide.</strong> Resistance to your ancestry damage type.</p>
<p><strong>Dragon Sight.</strong> Darkvision 60 ft and keensense 10 ft.</p>""", tag="PG2"),
    _lineage("Drow", """<p>Variant elf lineage adapted to the underworld.</p>
<p><strong>Age.</strong> Physical maturity ~20; full maturity ~100; lifespan to 750.</p>
<p><strong>Size.</strong> Medium.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Arachnid Kismet.</strong> Advantage interacting with spiders and scorpions; when a d20 result includes 8, gain 1 Resolve.</p>
<p><strong>Superior Darkvision.</strong> 120 feet; disadvantage on Perception by sight in sunlight.</p>
<p><strong>Trance.</strong> 4 hours of trance replaces sleep.</p>""", tag="PG2 variant"),
    _lineage("Duergar", """<p>Variant dwarf lineage from the deep underworld.</p>
<p><strong>Age.</strong> Mature by 20; ~350 years (often shorter in the depths).</p>
<p><strong>Size.</strong> Medium, 4–5 ft, dense build.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Duergar Resilience.</strong> Advantage vs. charmed or paralyzed; advantage vs. illusions.</p>
<p><strong>Enlarge.</strong> Bonus action: Large for 1 minute, double weapon damage dice, advantage on Fitness checks/saves (once per long rest).</p>
<p><strong>Superior Darkvision.</strong> 120 feet.</p>""", tag="PG2 variant"),
    _lineage("Dwarf", """<p><strong>Age.</strong> Mature ~20; young until 50; ~350 years.</p>
<p><strong>Size.</strong> Medium, 4–5 ft, broad frame.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Dwarven Resilience.</strong> Advantage vs. poisoned; resistance to poison Wounds.</p>
<p><strong>Dwarven Toughness.</strong> Max Wounds +1, and +1 Max Wounds each level.</p>"""),
    _lineage("Elemental Scion", """<p>Mortals infused with elemental power (sometimes called jinnborn).</p>
<p><strong>Age.</strong> Adult ~15; ~75 years (up to 150).</p>
<p><strong>Size.</strong> Medium, 5–7 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Hybrid Humanoid.</strong> Poison resistance; resistance by adaptation; advantage vs. paralyzed, petrified, poisoned.</p>
<p><strong>Natural Adaptation.</strong> Earthborn (tremorsense 10 ft, ignore difficult terrain), Fireborn (emit light; +proficiency fire on melee hit), Waterborn (swim speed, squeeze through 1-inch gaps), or Windborn (fly 10 ft hover; hold breath for proficiency bonus hours).</p>""", tag="PG2"),
    _lineage("Elf", """<p><strong>Age.</strong> Physical maturity ~20; emotional maturity ~100; up to 750 years.</p>
<p><strong>Size.</strong> Medium, slender builds.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Heightened Senses.</strong> Advantage on Perception (sight/hearing); see through light obscurement.</p>
<p><strong>Magic Ancestry.</strong> Advantage vs. charmed; magic can't put you to sleep.</p>
<p><strong>Trance.</strong> 4 hours of trance replaces sleep.</p>"""),
    _lineage("Gearforged", """<p>Living minds in mechanical bodies of metal and wood.</p>
<p><strong>Age.</strong> Soul age varies; body lasts indefinitely with maintenance.</p>
<p><strong>Size.</strong> Medium or Small (pick a chassis lineage such as human or kobold).</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Constructed Vitality.</strong> No eat/drink/breathe; 6-hour dormant rest.</p>
<p><strong>Hybrid Humanoid.</strong> Disease immune; poison resistance; advantage vs. paralyzed, petrified, poisoned.</p>
<p><strong>Machine Speech.</strong> Speak and understand Machine Speech.</p>
<p><strong>Upgrade.</strong> Always Armed (integrated weapons), Bulk Up (Large temporarily), or Quick Fix (temp Wounds when below half Max Wounds).</p>""", tag="PG2"),
    _lineage("Goblin", """<p>Adaptable humanoids found in vast numbers across harsh environments.</p>
<p><strong>Age.</strong> Adult 14–16; rarely past 100.</p>
<p><strong>Size.</strong> Small, 3–4 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Nimble Escape.</strong> Bonus action Disengage or Hide.</p>
<p><strong>Strength in Numbers.</strong> Extra damage equal to proficiency bonus when an ally is within 5 feet of your target.</p>""", tag="PG2"),
    _lineage("Gnoll", """<p>Hyena-like humanoids; often found in deserts and port cities.</p>
<p><strong>Age.</strong> Adult ~12; rarely past 70.</p>
<p><strong>Size.</strong> Medium, 7–8 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Scent Prey.</strong> Advantage on Survival checks relying on smell.</p>
<p><strong>Sprinter.</strong> When you Dash, move triple speed (uses per day = proficiency bonus).</p>""", tov=False),
    _lineage("Human", """<p><strong>Age.</strong> Adult late teens; rarely past 100.</p>
<p><strong>Size.</strong> Medium or Small.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Ambitious.</strong> One skill proficiency and one talent (any list, meeting prerequisites).</p>"""),
    _lineage("Kobold", """<p>Small draconic humanoids with mechanical aptitude.</p>
<p><strong>Age.</strong> Teen adulthood; elderly ~80; rarely 100.</p>
<p><strong>Size.</strong> Small, or Medium if truescale (~5 ft).</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Tinker's Fascination.</strong> Add 1d8 to tool ability checks.</p>
<p><strong>Natural Adaptation.</strong> Fierce (Small: react attack when Large+ hits you) or Truescale (Medium: AC 13 + Fitness; one elemental resistance).</p>"""),
    _lineage("Orc", """<p>Resilient explorers driven to travel and survive extremes.</p>
<p><strong>Age.</strong> Adult within two decades; seldom past 60.</p>
<p><strong>Size.</strong> Medium, 6–8 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Heightened Senses.</strong> As elf (sight/hearing).</p>
<p><strong>Orcish Perseverance.</strong> Instead of dying from suffocation or exhaustion levels, enter death-like stasis until healed or destroyed.</p>
<p><strong>Stalwart.</strong> Make end-of-turn saves at the start of your turn instead.</p>"""),
    _lineage("Rachisan", """<p>Plant-featured humanoids resembling ground-grown vegetables.</p>
<p><strong>Age.</strong> Adult ~5; typically ~50 (up to 100).</p>
<p><strong>Size.</strong> Small, 3–4 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Hybrid Humanoid.</strong> Advantage vs. paralyzed, petrified, and exhaustion effects.</p>
<p><strong>Green Thumb.</strong> +1d8 on plant-related checks; ignore difficult terrain from plant growth.</p>
<p><strong>Natural Adaptation.</strong> Alliumite (blinding spore reaction), Cruciferan (rest meal heals allies), or Tuberkith (immune blinded; hear while unconscious).</p>""", tag="PG2"),
    _lineage("Sapopova", """<p>Amphibious folk with frog or toad traits.</p>
<p><strong>Age.</strong> Mature ~8; rarely past 50.</p>
<p><strong>Size.</strong> Small, 2–4 ft.</p>
<p><strong>Speed.</strong> 30 feet walk, 30 feet swim.</p>
<p><strong>Amphibian.</strong> Breathe air and water.</p>
<p><strong>Superior Vision.</strong> Darkvision 60 ft; color in dim light/darkness; advantage locating moving targets.</p>
<p><strong>Natural Adaptation.</strong> Frogkin (Athletics proficiency; standing long/high jump) or Toadfolk (cheek storage; spit improvised ranged attacks 30 ft).</p>""", tag="PG2"),
    _lineage("Sea Elf", """<p>Variant elf lineage from undersea realms.</p>
<p><strong>Age.</strong> As elf.</p>
<p><strong>Size.</strong> Medium, sleek swimmer's build.</p>
<p><strong>Speed.</strong> 30 feet walk, swim speed equal to walk; Dash as bonus action while submerged.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Seaborn.</strong> Breathe air and water; comfortable to 0°F; ignore extreme cold hazard.</p>
<p><strong>Trance.</strong> 4 hours.</p>""", tag="PG2 variant"),
    _lineage("Shade", """<p>Beings caught between life and undeath, formed from memory.</p>
<p><strong>Age.</strong> Appear as at death; potentially centuries.</p>
<p><strong>Size.</strong> Medium or Small (living form lineage).</p>
<p><strong>Speed.</strong> As living form.</p>
<p><strong>Hybrid Humanoid.</strong> Poison resistance; advantage vs. poisoned and exhaustion.</p>
<p><strong>Phantasmal Form.</strong> Action: ghostly form 1 minute (resistance to nonmagical B/P/S, pass through creatures/objects, fly 30 ft hover) once per long rest.</p>
<p><strong>Spectral Sight.</strong> Darkvision 60 ft; see into Ethereal Plane 30 ft (uses = proficiency bonus per long rest).</p>""", tag="PG2"),
    _lineage("Smallfolk", """<p><strong>Age.</strong> Adult ~20; ~150 years (gnomes sometimes twice).</p>
<p><strong>Size.</strong> Small.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Grounded.</strong> Once per day reroll a failed save and gain 1 Resolve.</p>
<p><strong>Small Stature.</strong> Move through Medium+ spaces; hide behind Medium+ creatures.</p>
<p><strong>Natural Adaptation.</strong> Gnomish (darkvision 60 ft, <em>minor illusion</em>) or Halfling (advantage vs. charmed/frightened).</p>"""),
    _lineage("Syderean", """<p>Plane-touched mortals (starborn) tied to cosmic forces.</p>
<p><strong>Age.</strong> Adult ~20; ~150 years.</p>
<p><strong>Size.</strong> Medium, 5–7 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Far Sight.</strong> Darkvision 60 ft; see in magical darkness 30 ft.</p>
<p><strong>Otherworldly Form.</strong> Necrotic resistance; double time without air, food, water, or sleep.</p>
<p><strong>Natural Adaptation.</strong> Celestial (Blessed Guise), Fiendish (Dreadful Guise), Aberrant, or Spellborn (see PG2 expansion).</p>"""),
    _lineage("Tiefling", """<p>Offspring of humans and fiends with varied infernal traits.</p>
<p><strong>Age.</strong> As human, slightly longer.</p>
<p><strong>Size.</strong> Medium.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Darkvision.</strong> 60 feet.</p>
<p><strong>Fiendish Legacy.</strong> Abyssal, Chthonic, or Infernal: resistance, cantrip, and leveled spells at 3rd and 5th (Willpower as spellcasting ability).</p>"""),
    _lineage("Tosculi", """<p>Insectoid wasp-folk, often hive-born.</p>
<p><strong>Age.</strong> Mature ~13; rarely past 40.</p>
<p><strong>Size.</strong> Small, 3–4 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Glide.</strong> Reaction when falling 10+ ft: glide 30 ft horizontally.</p>
<p><strong>Hive Mind.</strong> Bonus action telepathic link 30 ft (uses = proficiency bonus).</p>
<p><strong>Hiveborn Duty.</strong> Detached Drone (Golden Song charm/deafen) or Roving Trooper (stinger unarmed + poison).</p>""", tag="PG2"),
    _lineage("Eonic Human", """<p>Displaced time travelers from a dying far-future civilization.</p>
<p><strong>Age.</strong> Effectively immortal from time dilation.</p>
<p><strong>Size.</strong> Medium, 5–6 ft.</p>
<p><strong>Speed.</strong> 30 feet.</p>
<p><strong>Jittery.</strong> Can't be surprised while conscious; unseen attackers don't gain advantage on your first combat turn.</p>
<p><strong>Practiced and Prepared.</strong> Once per rest, add 1d6 to an ability check when shaping recorded history.</p>
<p><strong>Wizened Flesh.</strong> Disadvantage on Willpower (Persuasion); +proficiency bonus to Defense; exhaustion from wearing armor (light 1, medium 2, heavy 3 levels, recovered when doffed).</p>""", tov=False),
]


def _heritage(name: str, body: str, *, recommended: str | None = None, tag: str | None = None, tov: bool = True) -> dict:
    entry = {"name": name, "body": adapt_tov(body), "tov": tov}
    if recommended:
        entry["recommended"] = recommended
    if tag:
        entry["tag"] = tag
    return entry


# Typical pairings from ToV; any heritage may be chosen with any lineage.
LINEAGE_HERITAGE_RECOMMENDATIONS = [
    ("Beastkin", "Slayer, Wildlands"),
    ("Dhampir", "Conflicted, Supplicant"),
    ("Dragonborn", "Coterminous, Slayer"),
    ("Drow (Elf variant)", "Conflicted, Covenant"),
    ("Duergar (Dwarf variant)", "Conflicted, Diaspora"),
    ("Dwarf", "Fireforge, Stone"),
    ("Elemental Scion", "Coterminous, Seafarer"),
    ("Elf", "Cloud, Grove"),
    ("Gearforged", "Cosmopolitan, Ironwrought"),
    ("Goblin", "Conflicted, Salvager"),
    ("Human", "Cosmopolitan, Nomadic"),
    ("Kobold", "Supplicant, Salvager"),
    ("Orc", "Diaspora, Slayer"),
    ("Rachisan", "Cottage, Feysworn"),
    ("Sapopova", "Islander, Waterside"),
    ("Sea Elf (Elf variant)", "Seafarer, Waterside"),
    ("Shade", "Diaspora, Vexed"),
    ("Smallfolk", "Cottage, Salvager"),
    ("Syderean", "Anointed, Vexed"),
    ("Tosculi", "Hivebound, Wildlands"),
]


HERITAGES = [
    _heritage(
        "Anointed",
        """<p>You have accepted a supernatural connection to extraplanar forces or cosmic purpose—marked by omens, rites, or ancestral burden.</p>
<p><strong>Favored Disciple.</strong> You know the <em>thaumaturgy</em> cantrip and have advantage on death saves.</p>
<p><strong>Occult Studies.</strong> Proficiency in History or Religion. Advantage on checks to recall information about Celestials, Fiends, or Outsiders.</p>
<p><strong>Languages.</strong> Common plus two additional (typical: Abyssal, Celestial, or Infernal).</p>""",
        recommended="Syderean",
    ),
    _heritage(
        "Cloud",
        """<p>You were raised among arcane towers and academies where magic is the center of civic life.</p>
<p><strong>Touch of Magic.</strong> Choose a school of magic; learn one cantrip from it. At 3rd character level, learn one 1st-level spell from that school—cast once per long rest without Spell Power. Spellcasting ability: Insight or Willpower (choose at creation).</p>
<p><strong>World of Wonders.</strong> Proficiency in Arcana.</p>
<p><strong>Languages.</strong> Common plus two additional (typical: Elvish and Draconic).</p>""",
        recommended="Elf",
    ),
    _heritage(
        "Cosmopolitan",
        """<p>Raised in a major city or nomadic between cultures—you are a citizen of the wider world.</p>
<p><strong>Street Smarts.</strong> In urban environments: advantage on checks to avoid getting lost or find public destinations; can't be surprised unless asleep or incapacitated.</p>
<p><strong>Worldly Wisdom.</strong> Proficiency in History. Add PB to checks about unfamiliar cultures' buildings, rites, or objects (double PB if proficient in a relevant skill or tool).</p>
<p><strong>Languages.</strong> Common plus three additional (typical: Dwarvish and Elvish).</p>""",
        recommended="Human, Gearforged",
    ),
    _heritage(
        "Cottage",
        """<p>You grew up in a tight agricultural community—hardworking, practical, and hearth-focused.</p>
<p><strong>Comforts of Home.</strong> During a long rest, cook or comfort up to PB allies (including you); each gains temp Wounds equal to twice PB until your next long rest.</p>
<p><strong>Homesteader.</strong> Proficiency in Animal Handling or Nature.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Halfling or Gnomish).</p>""",
        recommended="Smallfolk, Rachisan",
    ),
    _heritage(
        "Diaspora",
        """<p>Your displaced community preserves the legacy of a lost homeland through guilds, mercenary companies, or faith.</p>
<p><strong>Preserved Traditions.</strong> Proficiency in History and one martial weapon of your choice.</p>
<p><strong>Timeless Resolve.</strong> You and allies within 5 feet have advantage on saves vs. frightened.</p>
<p><strong>Languages.</strong> Common plus one additional (often Orcish or Dwarvish).</p>""",
        recommended="Orc, Duergar, Shade",
    ),
    _heritage(
        "Fireforge",
        """<p>Raised in volcanic forge-clans where dwarves craft amid magma and ally with elementals.</p>
<p><strong>Forgecraft.</strong> Smithing tools proficiency; double PB on checks with them. You know <em>mending</em>.</p>
<p><strong>Heat Resilience.</strong> Fire damage resistance.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Dwarvish).</p>""",
        recommended="Dwarf",
    ),
    _heritage(
        "Grove",
        """<p>Forest communities living in harmony with nature—sacred groves, canopy paths, and guardians of the wild.</p>
<p><strong>Canopy Walker.</strong> Climb speed equal to walking speed.</p>
<p><strong>Nature's Camouflage.</strong> Advantage on Stealth while lightly obscured by natural phenomena; you can Hide when lightly obscured by nature even if normally you couldn't.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Elvish).</p>""",
        recommended="Elf",
    ),
    _heritage(
        "Nomadic",
        """<p>Your people migrate with seasons, trade routes, or tradition—you know the rigors of the road.</p>
<p><strong>Resilient.</strong> Advantage vs. extreme weather effects. Once per long rest, reduce exhaustion by one when you finish a short rest.</p>
<p><strong>Traveler.</strong> Proficiency in Survival.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Dwarvish or Elvish).</p>""",
        recommended="Human",
    ),
    _heritage(
        "Salvager",
        """<p>Raised to build, repair, and survive with whatever materials are at hand—patient, resourceful, and inventive.</p>
<p><strong>Repurpose.</strong> In 1 minute, create a Tiny nonmagical item (≤25 gp adventuring gear) from surroundings; lasts one use then breaks.</p>
<p><strong>Tinkerer.</strong> Tinker's tools or other tool proficiency; double PB on checks to create, identify, or disarm objects/traps with relevant proficiency.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Draconic or Gnomish).</p>""",
        recommended="Kobold, Smallfolk, Goblin",
    ),
    _heritage(
        "Slayer",
        """<p>Monster-hunting packs trained from youth to track and kill dangerous predators.</p>
<p><strong>Natural Predator.</strong> Proficiency in Intimidation; advantage on Intimidation vs. Beasts and Animals.</p>
<p><strong>Tracker.</strong> Add PB to locate/spot/track checks (double PB if proficient in the skill or tool used).</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Primordial or Sylvan).</p>""",
        recommended="Beastkin, Orc, Dragonborn",
    ),
    _heritage(
        "Stone",
        """<p>Subterranean miners and masons who defend ancestral delves beneath the world.</p>
<p><strong>Ancestral Arts.</strong> Construction tools proficiency (double PB); proficiency with one martial weapon.</p>
<p><strong>Eye for Quality.</strong> Add PB to checks about metal/stone objects or structures (double PB if proficient in a relevant skill or tool).</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Dwarvish).</p>""",
        recommended="Dwarf",
    ),
    _heritage(
        "Supplicant",
        """<p>A community bound to serve a monstrous overlord—often dragons—building traps and hazards around their lair.</p>
<p><strong>Scurry.</strong> Bonus action: move 10 feet without opportunity attacks; doesn't trigger traps you know about.</p>
<p><strong>Supplicant.</strong> Proficiency in Insight or Persuasion. When a creature within 30 feet spends Resolve, you have advantage on checks and saves until your next turn.</p>
<p><strong>Languages.</strong> Common plus one additional (overlord's tongue: Draconic, Giant, or Undercommon).</p>""",
        recommended="Kobold, Dhampir",
    ),
    _heritage(
        "Vexed",
        """<p>Your life is defined by defying a supernatural bond—claimed at birth, haunted by dreams, or inheriting a blood debt.</p>
<p><strong>Prodigal Disciple.</strong> Treat d20 rolls of 9 or lower as 10 on saves vs. charmed or possessed.</p>
<p><strong>Quarry's Cunning.</strong> Proficiency in Deception or Insight.</p>
<p><strong>Languages.</strong> Common plus one additional (typical esoteric: Abyssal, Celestial, or Infernal).</p>""",
        recommended="Syderean, Shade",
    ),
    _heritage(
        "Wildlands",
        """<p>Primordial-magic communities where beasts and humanoids live as equals in unspoiled territory.</p>
<p><strong>Beast Affinity.</strong> Communicate simple ideas with Beasts/Animals; advantage interacting with them.</p>
<p><strong>Shepherd's Gift.</strong> Animal Handling proficiency. Beasts/Animals with CR ≤ PB must pass a Willpower (Animal Handling) contest to attack you or choose a new target.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Sylvan).</p>""",
        recommended="Beastkin, Tosculi",
    ),
    _heritage(
        "Conflicted",
        """<p>Raised in a society torn by factional violence, revolution, or rebellion—survival means reading danger early.</p>
<p><strong>Prepared for Trouble.</strong> Proficiency with improvised weapons. Disarm traps without thieves' tools.</p>
<p><strong>Talk Your Way Out.</strong> Proficiency in Deception or Persuasion.</p>
<p><strong>Languages.</strong> Common plus one additional (language of the conflict zone).</p>""",
        recommended="Dhampir, Drow, Duergar, Goblin, Gearforged, Shade",
        tag="PG2",
    ),
    _heritage(
        "Coterminous",
        """<p>From a border community where the Material Plane meets an Elemental Plane—trade hub, genie dominion, and elemental hazard.</p>
<p><strong>Elemental Community.</strong> Choose Air (lightning), Earth (acid), Fire (fire), or Water (cold).</p>
<p><strong>Ambient Absorption.</strong> When you take your element's damage type, roll d8s equal to half PB (min 1) and reduce damage by the total.</p>
<p><strong>Environmental Acclimatization.</strong> Proficiency on checks/saves vs. hazards of your element (double PB if already proficient).</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Primordial).</p>""",
        recommended="Dragonborn, Elemental Scion",
        tag="PG2",
    ),
    _heritage(
        "Covenant",
        """<p>A magic-obsessed community hoarding arcane power near raw magical nodes—spellcraft above all else.</p>
<p><strong>Expert Caster.</strong> Arcana proficiency; learn one cantrip from any source (Insight or Willpower as casting ability).</p>
<p><strong>Spell Inoculation.</strong> Advantage on saves vs. spells that target you specifically (not area effects).</p>
<p><strong>Languages.</strong> Common plus two additional (typical: Draconic, Infernal, or Sylvan).</p>""",
        recommended="Drow",
        tag="PG2",
    ),
    _heritage(
        "Feysworn",
        """<p>Raised under fey dominion, bound by oaths to archfey and their alien goals.</p>
<p><strong>Accustomed to Trickery.</strong> You know <em>prestidigitation</em> (Insight or Willpower). Advantage vs. charmed; on failed charm save, gain 2 Resolve instead of 1.</p>
<p><strong>Enchanting Call.</strong> Action: one creature makes Willpower save (DC 10 + PB) or is charmed until end of your next turn. Or spend 2 Resolve to attempt frighten (Resolve lost only if successful). Once per short or long rest.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Sylvan).</p>""",
        recommended="Rachisan",
        tag="PG2",
    ),
    _heritage(
        "Hivebound",
        """<p>A telepathically linked community functioning as a collective—unity over individuality.</p>
<p><strong>Open Mind.</strong> Insight proficiency. Bonus action: temporary telepathic link with one willing creature you touch until you stop touching or link someone else.</p>
<p><strong>Unity.</strong> When you Help on a check, target gains +PB; when helped, you gain +PB from the helper.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Primordial or Sylvan).</p>""",
        recommended="Tosculi",
        tag="PG2",
    ),
    _heritage(
        "Ironwrought",
        """<p>Raised among gearforged and artificers who treat born and made people as equals.</p>
<p><strong>Construct Affinity.</strong> Communicate simple ideas with Constructs; advantage interacting with them.</p>
<p><strong>Mechanic.</strong> Tinker's or smithing tools proficiency; double PB on checks to create, repair, or upgrade metal-bodied creatures with relevant proficiency.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Dwarvish or Draconic).</p>""",
        recommended="Gearforged",
        tag="PG2",
    ),
    _heritage(
        "Islander",
        """<p>From an archipelago chain trading specialty goods between islands—hardy, personable, and resilient.</p>
<p><strong>Like Water off Your Back.</strong> Advantage on saves vs. frightened.</p>
<p><strong>Tiderider.</strong> Vehicles (water) proficiency; swim speed equal to walking speed.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Halfling or Sylvan).</p>""",
        recommended="Sapopova",
        tag="PG2",
    ),
    _heritage(
        "Joymonger",
        """<p>Raised in a community that sells happiness—performers, artisans, and laborers keeping attractions running.</p>
<p><strong>Joyful Endurance.</strong> Advantage on Fitness checks for weariness/survival outside combat. Once per long rest, negate gaining an exhaustion level.</p>
<p><strong>Welcome to the Show.</strong> Proficiency in Persuasion or Performance.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Halfling or Gnomish).</p>""",
        tag="PG2",
    ),
    _heritage(
        "Kithren",
        """<p>Nomadic rebuilders who travel to devastated settlements and help survivors recover.</p>
<p><strong>Helping Hands.</strong> Medicine or Survival proficiency; proficiency with one melee weapon of your choice.</p>
<p><strong>Search and Rescue.</strong> Network of kithren contacts can point toward a Humanoid's last known location (GM discretion). Cast <em>mending</em> once per long rest even if not a spellcaster.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Goblin or Gnomish).</p>""",
        tag="PG2",
    ),
    _heritage(
        "Seafarer",
        """<p>Raised on a traveling flotilla—scout ships, farms, trawlers, and cruisers crossing open water together.</p>
<p><strong>Jack of all Trades.</strong> Once per long rest, add PB to a tool or ability check without proficiency.</p>
<p><strong>Sea Legs.</strong> Vehicles (water) proficiency; advantage on Fitness checks aboard floating vessels.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Dwarvish or Elvish).</p>""",
        recommended="Sea Elf, Elemental Scion",
        tag="PG2",
    ),
    _heritage(
        "Waterside",
        """<p>Edge-of-water communities splitting life between land and water—fishing, boating, and aquaculture.</p>
<p><strong>Knowledgeable.</strong> History or Nature proficiency; double PB on that skill for waterside areas.</p>
<p><strong>Water Legs.</strong> Vehicles (water) proficiency; advantage on Fitness (Athletics) and Fitness (Acrobatics) balance checks near water; water up to waist isn't difficult terrain.</p>
<p><strong>Languages.</strong> Common plus one additional (typical: Sylvan, Dwarvish, or Elvish).</p>""",
        recommended="Sapopova, Sea Elf",
        tag="PG2",
    ),
]
