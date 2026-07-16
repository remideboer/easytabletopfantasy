#!/usr/bin/env python3
"""YMIAT subclass ability definitions. Source: BFRD + foundation drafts, 10-level play."""

from ability_utils import make_anchor


def _sf(class_id, class_name, subclass_id, subclass_name, names, level, summary, body, action=None):
    primary = names[0]
    entry = {
        "anchor": f"{subclass_id}-{make_anchor(primary)}",
        "class_id": class_id,
        "class_name": class_name,
        "subclass_id": subclass_id,
        "subclass_name": subclass_name,
        "name": primary,
        "names": names,
        "level": level,
        "summary": summary,
        "body": body,
        "is_subclass": True,
    }
    if action:
        entry["action"] = action
    return entry


def _sub(class_id, class_name, subclass_id, subclass_name, summary, features, bfrd_url=None):
    return {
        "class_id": class_id,
        "class_name": class_name,
        "subclass_id": subclass_id,
        "subclass_name": subclass_name,
        "summary": summary,
        "bfrd_url": bfrd_url,
        "features": features,
    }


def _stub_features(class_id, class_name, subclass_id, subclass_name, note):
    return [
        _sf(
            class_id, class_name, subclass_id, subclass_name,
            [f"{subclass_name} Subclass"],
            "2nd, 4th, 6th, and 8th level",
            f"{subclass_name} subclass features.",
            f"<p>{note}</p>",
        ),
    ]


def _ymiat_level_label(bfrd_levels: str) -> str:
    """Map BFRD 3/7/11/15 progression labels to YMIAT 2/4/6/8."""
    mapping = {
        "3rd": "2nd-level subclass feature",
        "7th": "4th-level subclass feature",
        "11th": "6th-level subclass feature",
        "15th": "8th-level subclass feature",
    }
    if bfrd_levels in mapping:
        return mapping[bfrd_levels]
    return bfrd_levels


# ── BARBARIAN ───────────────────────────────────────────────────────────────

def barbarian_subclasses():
    cid, cname = "barbarian", "Barbarian"
    return [
        _sub(
            cid, cname, "berserker", "Berserker",
            "Primal bloodlust pushes your rage into a devastating frenzy.",
            [
                _sf(cid, cname, "berserker", "Berserker", ["Frenzy"], _ymiat_level_label("3rd"),
                    "Optional frenzy with rage; extra melee attack while frenzied.",
                    """<p>When you rage, you can choose to enter a <strong>frenzy</strong> as part of the same free action.</p>
<p>While frenzied, once per turn you can make <strong>one extra melee weapon attack as your second action</strong> (you must not have moved this turn, per YMIAT second-action rules).</p>""",
                    action="free action (with Rage)"),
                _sf(cid, cname, "berserker", "Berserker", ["Ruthless Bearing"], _ymiat_level_label("3rd"),
                    "Intimidation proficiency; double advantage if already proficient.",
                    """<p>You gain proficiency in the <strong>Intimidation</strong> skill. If you are already proficient, you have <strong>double advantage</strong> on Intimidation checks.</p>"""),
                _sf(cid, cname, "berserker", "Berserker", ["Mindless Rage"], _ymiat_level_label("7th"),
                    "Ignore exhaustion while raging; immune to charm and frighten; temp HP on crit or kill during frenzy.",
                    """<p>While raging, you gain the following benefits:</p>
<ul>
<li>You ignore any levels of exhaustion for the duration of your rage.</li>
<li>You can't be charmed or frightened while raging. If you are already charmed or frightened when you enter a rage, the effect is suspended for the duration.</li>
<li>During a frenzy, if you score a critical hit or reduce a creature to 0 Wounds, you gain temporary Wounds equal to your <strong>PB + your Fitness modifier</strong>. These last until expended or until you finish a short or long rest.</li>
</ul>"""),
                _sf(cid, cname, "berserker", "Berserker", ["Intimidating Presence"], _ymiat_level_label("11th"),
                    "Bonus damage vs. frightened foes; free action to frighten nearby creatures.",
                    """<p>Your weapon attacks deal extra damage equal to your <strong>PB</strong> (same damage type as the weapon) to frightened creatures.</p>
<p>As a <strong>free action</strong>, you can attempt to frighten up to <strong>PB</strong> creatures within 30 feet that can see or hear you. Each target makes an <strong>Insight save</strong> (DC 8 + PB + Willpower modifier + temporary Wounds from Mindless Rage). On a failure, a creature is frightened of you until the end of your next turn.</p>
<p>On subsequent turns, you can use a free action to extend the effect on each frightened creature until the end of your next turn. The effect ends if the creature ends its turn more than 60 feet away or can no longer see or hear you. On a successful save, you can't use this feature on that creature again for 24 hours.</p>""",
                    action="free action"),
                _sf(cid, cname, "berserker", "Berserker", ["Retaliation"], _ymiat_level_label("15th"),
                    "Reaction: close on attacker and strike back.",
                    """<p>When a creature hits or misses you with an attack, you can use your <strong>reaction</strong> to move up to half your speed toward that creature and make a single melee attack against it. If the creature is Large or larger, you have advantage on the attack roll.</p>""",
                    action="reaction"),
            ],
            "https://bfrd.net/classes/barbarian/barbarian-subclasses/",
        ),
        _sub(
            cid, cname, "wild-fury", "Wild Fury",
            "Animal spirits guide your rage—choose a beast focus at each subclass level.",
            [
                _sf(cid, cname, "wild-fury", "Wild Fury", ["Animal Focus"], _ymiat_level_label("3rd"),
                    "Choose your first animal focus (2nd level in YMIAT).",
                    """<p>At <strong>2nd level</strong>, choose an <strong>animal focus</strong> that shapes how your rage manifests. You choose another focus at 4th, 6th, and 8th level.</p>
<p>Options include: Alligator, Bear, Tiger, Toad, Hawk, Lizard, Turtle, Wolf, Crane, Ram, Shark, and Snake. Each focus grants a thematic benefit while you rage (movement, senses, damage type, or defense). Work with your GM to apply the BFRD Wild Fury focus rules adapted to YMIAT.</p>"""),
                _sf(cid, cname, "wild-fury", "Wild Fury", ["Deepening Focus"], _ymiat_level_label("7th"),
                    "Second animal focus (4th level in YMIAT).",
                    """<p>Choose a second animal focus. Its benefits stack with your first while you rage.</p>"""),
                _sf(cid, cname, "wild-fury", "Wild Fury", ["Primal Synthesis"], _ymiat_level_label("11th"),
                    "Third animal focus (6th level in YMIAT).",
                    """<p>Choose a third animal focus. When you rage, you can blend two active focuses for one enhanced effect once per rage.</p>"""),
                _sf(cid, cname, "wild-fury", "Wild Fury", ["Apex Predator"], _ymiat_level_label("15th"),
                    "Fourth animal focus (8th level in YMIAT).",
                    """<p>Choose a fourth animal focus. While raging, you can move up to half your speed when you enter a rage. Once per combat, if you enter a rage on your first turn, the first successful melee attack you make that turn deals <strong>2 Wounds</strong> instead of 1 (unless it is already a critical hit).</p>"""),
            ],
        ),
        _sub(
            cid, cname, "chaos", "Chaos",
            "Entropic fury warps the battlefield around your rage.",
            [
                _sf(cid, cname, "chaos", "Chaos", ["Chaos Conduit"], _ymiat_level_label("3rd"),
                    "Chaos Dice empower melee hits with random banes while raging.",
                    """<p>While raging, when you hit with a melee attack you can expend one <strong>Chaos Die</strong> (d10). You have Chaos Dice equal to <strong>PB + 1</strong> (minimum 3), regained on a short or long rest.</p>
<p>Roll the die: the target takes extra force damage equal to the result and suffers a <strong>Chaos Bane</strong> of your choice:</p>
<ul>
<li><strong>Enervate:</strong> Insight save or disadvantage on its next attack before end of its next turn.</li>
<li><strong>Impede:</strong> Insight save or it can't take reactions until start of its next turn.</li>
<li><strong>Martyr:</strong> Roll the die again; target and you each take force damage equal to that roll (can't be reduced by your resistances).</li>
<li><strong>Shunt:</strong> Fitness save or teleport up to 30 feet to an unoccupied space you can see.</li>
</ul>
<p>Bane save DC = 8 + PB + Fitness modifier (your choice of Fitness for the modifier).</p>"""),
                _sf(cid, cname, "chaos", "Chaos", ["Random Polymath"], _ymiat_level_label("3rd"),
                    "Random skill proficiency (or double PB) after each long rest.",
                    """<p>When you finish a long rest, roll d20 on the Random Skill table. You gain proficiency in that skill until your next long rest. If you already have proficiency, add double your PB to checks with that skill instead.</p>"""),
                _sf(cid, cname, "chaos", "Chaos", ["Invoke Entropy"], _ymiat_level_label("7th"),
                    "Reaction: force a nearby creature to reroll a check.",
                    """<p>As a <strong>reaction</strong> when you or a creature you can see within 30 feet succeeds or fails an ability check, force that creature to reroll and use the new result. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "chaos", "Chaos", ["Mayhem Shield"], _ymiat_level_label("11th"),
                    "Spend Chaos Dice to reduce incoming damage; 1s and 10s trigger extra effects.",
                    """<p>When a creature hits you with an attack, expend one or more Chaos Dice and reduce the damage by the total rolled. For each <strong>1</strong> rolled, regain expended Chaos Dice up to your maximum. For each <strong>10</strong> rolled, the attacker takes force damage equal to the total of your expended dice.</p>"""),
                _sf(cid, cname, "chaos", "Chaos", ["Cry Havoc"], _ymiat_level_label("15th"),
                    "Regain a Chaos Die and gain advantage on your first attack when empty.",
                    """<p>If you start your turn with no Chaos Dice remaining, you automatically regain one die and have advantage on the first attack roll you make before the end of your turn.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "four-winds", "Four Winds",
            "Elemental winds empower your movement and strikes.",
            [
                _sf(cid, cname, "four-winds", "Four Winds", ["Implacable Presence"], _ymiat_level_label("3rd"),
                    "Acrobatics proficiency or double PB on Acrobatics checks.",
                    """<p>You gain proficiency in <strong>Acrobatics</strong>. If you are already proficient, add double your PB to Acrobatics checks instead.</p>"""),
                _sf(cid, cname, "four-winds", "Four Winds", ["Winds of Wrath"], _ymiat_level_label("3rd"),
                    "Rage grants wind protection, thunder leaps, or thrown-weapon recklessness.",
                    """<p>When you enter a rage, swirling winds surround you. While raging and conscious, you can't be knocked prone and always land on your feet after falling.</p>
<p>When you first enter a rage, choose one benefit for its duration:</p>
<ul>
<li><strong>Buffeting winds:</strong> lightly obscured; ranged attacks against you at disadvantage; resistance to lightning and thunder.</li>
<li><strong>Thunder leap:</strong> if you leap 10+ feet toward a foe and hit with melee on the same turn, add 1d6 thunder per 10 feet traveled (max 10d6). On any thunder damage, Fitness save (DC = damage dealt) or prone.</li>
<li><strong>Thrown wrath:</strong> Reckless Attack with thrown weapons using Fitness; thrown range doubled; double rage damage bonus on the throw.</li>
</ul>
<p>When you enter a rage, you can expend an additional Rage use to take a second option.</p>"""),
                _sf(cid, cname, "four-winds", "Four Winds", ["Cyclonic Ward"], _ymiat_level_label("7th"),
                    "Reduce falling damage; reaction to shield allies and reposition them.",
                    """<p>Reduce falling damage by twice your barbarian level (after rage halving while raging).</p>
<p>While raging, as a <strong>reaction</strong> when you or an ally within 30 feet takes damage, reduce that damage by your barbarian level and move the ally up to 10 feet (if willing).</p>""",
                    action="reaction"),
                _sf(cid, cname, "four-winds", "Four Winds", ["Howling Charge"], _ymiat_level_label("11th"),
                    "Free action Dash; ignore difficult terrain and paralysis/restraint until next turn.",
                    """<p>As a <strong>free action</strong>, take the Dash action. Until the start of your next turn, ignore difficult terrain and you can't be paralyzed or restrained.</p>""",
                    action="free action"),
                _sf(cid, cname, "four-winds", "Four Winds", ["Raging Storm"], _ymiat_level_label("15th"),
                    "Thunder aura on hits; cyclonic retaliation and lightning throws.",
                    """<p>While raging:</p>
<ul>
<li>Each melee or unarmed hit deals 1d6 thunder to the target and each hostile creature within 10 feet.</li>
<li>When you use Cyclonic Ward against a melee attack, the attacker makes a Fitness save (DC 8 + PB + Fitness) or takes 4d6 thunder (half on success). Fail by 5+ = deafened 1 minute.</li>
<li>First thrown weapon hit (Fitness) each turn: target and creatures within 10 feet take 3d6 lightning.</li>
</ul>
<p>Thunder from Raging Storm is audible out to 300 feet.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "kraken", "Kraken",
            "Crushing tentacle-like force and abyssal resilience.",
            [
                _sf(cid, cname, "kraken", "Kraken", ["Deep Vision"], _ymiat_level_label("3rd"),
                    "Swim speed, water breathing, enhanced darkvision underwater.",
                    """<p>You gain a swimming speed equal to your walking speed and can breathe water. While submerged, you gain darkvision 60 feet (or +30 feet if you already have darkvision).</p>"""),
                _sf(cid, cname, "kraken", "Kraken", ["Kraken's Grasp"], _ymiat_level_label("3rd"),
                    "Spectral tentacles while raging: grapple, damage scaling d4→d10.",
                    """<p>When you rage, two spectral tentacles sprout (reach 10 ft., proficient melee weapons). As a <strong>free action</strong> when you rage (or later on your turn), make up to two tentacle attacks (one per tentacle). On hit: force damage = tentacle die + Fitness modifier; Large or smaller targets are grappled (escape DC 8 + PB + Fitness). A grappling tentacle can attack only its grappled target.</p>
<p>Tentacle damage die scales: <strong>d4</strong> (2nd), <strong>d6</strong> (4th), <strong>d8</strong> (6th), <strong>d10</strong> (8th). Tentacles can lift objects up to Fitness × PB pounds and perform simple tasks (not wield weapons or use tools).</p>""",
                    action="free action"),
                _sf(cid, cname, "kraken", "Kraken", ["Ink Cloud"], _ymiat_level_label("7th"),
                    "Free action inky obscurement you can see through.",
                    """<p>As a <strong>free action</strong>, create a stationary 20-foot-radius heavily obscured sphere centered on you. You see normally inside it. Lasts 1 minute or until dismissed. PB uses per long rest.</p>""",
                    action="free action"),
                _sf(cid, cname, "kraken", "Kraken", ["Titan Grip"], _ymiat_level_label("7th"),
                    "Grappled foes restrained; tentacles can replace Attack action attacks.",
                    """<p>Creatures grappled by your tentacles are <strong>restrained</strong> until the grapple ends. When you take the Attack action, you can use tentacles for any number of your attacks.</p>"""),
                _sf(cid, cname, "kraken", "Kraken", ["Tentacle Fling"], _ymiat_level_label("11th"),
                    "Hurl grappled foes up to 30 feet for falling damage.",
                    """<p>When you take the Attack action, you can use one or more attacks to throw a tentacle-grappled creature up to 30 feet. It lands prone; bludgeoning damage 1d6 per 10 feet thrown (also to a struck creature on failed Fitness save, DC 8 + PB + Fitness).</p>"""),
                _sf(cid, cname, "kraken", "Kraken", ["Leviathan Wakes"], _ymiat_level_label("15th"),
                    "+10 ft tentacle reach; one extra tentacle attack per free action.",
                    """<p>Tentacle reach increases by 10 feet. Each time you use a free action for tentacle attacks, you can make <strong>one additional</strong> tentacle attack as part of that same free action.</p>"""),
            ],
        ),
    ]


# ── BARD ──────────────────────────────────────────────────────────────────────

def bard_subclasses():
    cid, cname = "bard", "Bard"
    return [
        _sub(
            cid, cname, "lore", "Lore",
            "A collector of knowledge who weaves magic and talents from every tradition.",
            [
                _sf(cid, cname, "lore", "Lore",
                    ["Bardic Performance: Ode to Heroes", "Ode to Heroes"],
                    _ymiat_level_label("3rd"),
                    "Performance that helps allies and hinders foes on ability checks.",
                    """<p>You gain the <strong>Ode to Heroes</strong> Bardic Performance option. When you perform, choose <strong>Fitness, Insight, or Willpower</strong>. While your performance lasts, allies in range have advantage on ability checks using that ability and enemies have disadvantage.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Expanded Talent List"], _ymiat_level_label("3rd"),
                    "Choose talents from magic or utility lists.",
                    """<p>When you gain a new talent from Improvement, you can select it from either the <a href="../talents.html">magic</a> or <a href="../talents.html">utility</a> talent lists.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Jack of All Trades"], _ymiat_level_label("3rd"),
                    "Half PB on ability checks that don't already include PB.",
                    """<p>Add half your PB (rounded down) to any ability check that doesn't already include your PB.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Swift Ritual"], _ymiat_level_label("7th"),
                    "Cast a known ritual as an action once per long rest.",
                    """<p>You can cast an Arcane ritual you know as an <strong>action</strong> instead of its listed casting time. You must still provide all other components. Once used, you can't use this again until you finish a long rest.</p>""",
                    action="action"),
                _sf(cid, cname, "lore", "Lore", ["Magical Rites"], _ymiat_level_label("11th"),
                    "Learn two extra ritual spells from any source.",
                    """<p>Learn two ritual spells of your choice from any source list. Each must be of a level you can cast. They count as Arcane spells for you and don't count against rituals known from your class table.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Peerless Skill"], _ymiat_level_label("15th"),
                    "Spend Bardic Inspiration on ability checks; keep the die on success.",
                    """<p>When you make an ability check and have Bardic Inspiration available, you can roll a Bardic Inspiration die and add it to the check. If you succeed, you keep the die; if you fail, the die is expended.</p>"""),
            ],
            "https://bfrd.net/classes/bard/bard-subclasses/",
        ),
        _sub(
            cid, cname, "victory", "Victory",
            "Inspire allies to triumph through martial cadence.",
            [
                _sf(cid, cname, "victory", "Victory",
                    ["Bardic Performance: Battle March", "Battle March"],
                    _ymiat_level_label("3rd"),
                    "Performance lets allies react-move; medium armor and martial weapon.",
                    """<p>You gain <strong>Battle March</strong> as a Bardic Performance option. When you perform—and as part of each free action spent maintaining it—you can command up to three willing allies who can see or hear you to use their <strong>reaction</strong> to move up to half their speed without opportunity attacks.</p>
<p>You also gain proficiency with medium armor, shields, and one martial weapon of your choice.</p>
<p>When Improvement grants a new talent, you can choose from the martial or utility talent lists.</p>"""),
                _sf(cid, cname, "victory", "Victory", ["Multiattack"], _ymiat_level_label("7th"),
                    "Two attacks when you take the Attack action.",
                    """<p>When you take the Attack action on your turn, you can make <strong>two attacks</strong> instead of one.</p>"""),
                _sf(cid, cname, "victory", "Victory", ["Unified Front"], _ymiat_level_label("11th"),
                    "Reaction: boost your save and allies auto-succeed on area effects.",
                    """<p>When you are targeted by an area effect that requires a save, use your <strong>reaction</strong> to expend a Bardic Inspiration die and add it to your save. On a success, every friendly creature in the area automatically succeeds on their saves as well.</p>""",
                    action="reaction"),
                _sf(cid, cname, "victory", "Victory", ["Inspired Strike"], _ymiat_level_label("15th"),
                    "Spend Bardic Inspiration on attacks; keep the die on a hit.",
                    """<p>Once per turn when you make a weapon or spell attack and have Bardic Inspiration available, roll a Bardic Inspiration die and add it to the attack roll. If you hit, you keep the die; if you miss, the die is expended.</p>"""),
            ],
        ),
    ]


# ── CLERIC ────────────────────────────────────────────────────────────────────

def _domain_spells_body(spells_by_level):
    rows = "".join(
        f"<li><strong>Level {lvl}:</strong> {', '.join(spells)}</li>"
        for lvl, spells in spells_by_level.items()
    )
    return f"<p>These domain spells are always prepared:</p><ul>{rows}</ul>"


def cleric_subclasses():
    cid, cname = "cleric", "Cleric"
    return [
        _sub(
            cid, cname, "life", "Life",
            "Celebrate vitality and oppose the perversion of undeath.",
            [
                _sf(cid, cname, "life", "Life",
                    ["Channel Divinity: Preserve Life", "Preserve Life"],
                    _ymiat_level_label("3rd"),
                    "Channel divinity to distribute healing among nearby allies.",
                    """<p>As an <strong>action</strong>, present your holy symbol and restore Wounds equal to <strong>5 × your cleric level</strong>, divided among creatures within 30 feet. No creature can be restored above half its Max Wounds. No effect on Constructs or Undead.</p>""",
                    action="action"),
                _sf(cid, cname, "life", "Life", ["Disciple of Life"], _ymiat_level_label("3rd"),
                    "Healing spells restore extra Wounds.",
                    """<p>When you cast a Divine spell of 1st level or higher to restore Wounds, the target regains <strong>2 + the spell's level</strong> additional Wounds.</p>"""),
                _sf(cid, cname, "life", "Life", ["Life Domain Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared life domain spells.",
                    _domain_spells_body({
                        2: ["bless", "cure wounds", "gentle repose", "restoration"],
                        5: ["mass healing word", "revivify"],
                        7: ["death ward", "guardian of faith"],
                        9: ["greater restoration", "mass cure wounds"],
                    })),
                _sf(cid, cname, "life", "Life", ["Blessed Healer"], _ymiat_level_label("7th"),
                    "Healing others heals you.",
                    """<p>When you cast a Divine spell of 1st level or higher that restores Wounds to another creature, you regain <strong>2 + the spell's level</strong> Wounds.</p>"""),
                _sf(cid, cname, "life", "Life", ["Greater Preservation"], _ymiat_level_label("11th"),
                    "Expanded Preserve Life with condition cleansing.",
                    """<p>Preserve Life affects creatures within <strong>60 feet</strong>. When you use it, one target can also: cure all diseases; end blinded, deafened, paralyzed, or poisoned; or neutralize all poisons.</p>"""),
                _sf(cid, cname, "life", "Life", ["Perfect Healing"], _ymiat_level_label("15th"),
                    "Healing spells restore maximum Wounds.",
                    """<p>When you cast a Divine spell of 1st level or higher that restores Wounds, you automatically restore the maximum possible Wounds (no dice rolling).</p>"""),
            ],
        ),
        _sub(
            cid, cname, "light", "Light",
            "Wield radiant fire and searing truth against darkness.",
            [
                _sf(cid, cname, "light", "Light",
                    ["Channel Divinity: Searing Radiance", "Searing Radiance"],
                    _ymiat_level_label("3rd"),
                    "Channel radiance through your magical lights.",
                    """<p>As an <strong>action</strong>, present your holy symbol and channel radiance through every magical light source you created on the same plane. Each hostile creature in their bright light makes a <strong>Fitness save</strong>. Roll 2 × PB d8s; failed save = full radiant damage, success = half. Aberrations and Undead have disadvantage.</p>""",
                    action="action"),
                _sf(cid, cname, "light", "Light", ["Imbue Light"], _ymiat_level_label("3rd"),
                    "Learn light and dancing lights; dancing lights needs no concentration.",
                    """<p>You learn <em>light</em> and <em>dancing lights</em> if you don't know them. <em>Dancing lights</em> requires no concentration and lasts for the duration or until you cast it again. Both count as Divine cantrips and don't count against cantrips known.</p>"""),
                _sf(cid, cname, "light", "Light", ["Light Domain Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared light domain spells.",
                    _domain_spells_body({
                        2: ["burning hands", "guiding bolt", "moonbeam", "scorching ray"],
                        5: ["daylight", "fireball"],
                        7: ["elemental shield", "wall of fire"],
                        9: ["dispel evil and good", "flame strike"],
                    })),
                _sf(cid, cname, "light", "Light", ["Overwhelming Flash"], _ymiat_level_label("3rd"),
                    "Reaction penalizes nearby attack rolls with blinding light.",
                    """<p>When a creature within 10 feet makes an attack roll, use your <strong>reaction</strong> to release divine light. The attacker takes a penalty equal to your <strong>Insight modifier</strong> on the roll. If the attack still hits, the attacker is blinded until end of its turn. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "light", "Light", ["Radiant Spellcasting"], _ymiat_level_label("7th"),
                    "Cantrips and lit weapons deal extra radiant damage.",
                    """<p>Your Divine damaging cantrips deal an extra <strong>1d8 radiant</strong> damage. While holding a weapon under <em>light</em> or <em>continual flame</em>, the first time it deals damage each turn, add radiant damage equal to your Insight modifier.</p>"""),
                _sf(cid, cname, "light", "Light", ["Lux Malediction"], _ymiat_level_label("11th"),
                    "Searing Radiance becomes sunlight; Overwhelming Flash curses foes.",
                    """<p>Searing Radiance makes your lights magical sunlight for 1 minute. When you use Overwhelming Flash, curse the target (one at a time): can't regain Wounds until end of next turn; radiant damage = cleric level; −10 Insight (Perception) for 10 minutes; or can't benefit from invisibility for 1 minute. <em>Remove curse</em> ends it; magical darkness on both turns ends it.</p>"""),
                _sf(cid, cname, "light", "Light", ["Luminous Shroud"], _ymiat_level_label("15th"),
                    "Advantage on saves in bright light; charm/frighten immunity; damage choice.",
                    """<p>While in bright light, you have advantage on saves, can't be charmed or frightened, and gain immunity to radiant damage <strong>or</strong> resistance to necrotic damage (your choice).</p>"""),
            ],
        ),
        _sub(
            cid, cname, "war", "War",
            "Champion courage and decisive victory in battle.",
            [
                _sf(cid, cname, "war", "War",
                    ["Channel Divinity: Mark of Triumph", "Mark of Triumph"],
                    _ymiat_level_label("3rd"),
                    "Mark a foe so allies gain advantage on the first attack against it.",
                    """<p>As a <strong>free action</strong>, present your holy symbol and mark one creature within 60 feet you can see. Until the start of your next turn, the first attack roll each ally makes against the marked creature has advantage.</p>""",
                    action="free action"),
                _sf(cid, cname, "war", "War", ["Disciple of War"], _ymiat_level_label("3rd"),
                    "Extra weapon attack when you hit with the Attack action.",
                    """<p>Once per turn when you hit with a weapon attack during the Attack action, you can make one additional weapon attack as part of that same action. Uses per short or long rest equal to your PB.</p>"""),
                _sf(cid, cname, "war", "War", ["Expanded Talent List"], _ymiat_level_label("3rd"),
                    "Martial or magic talents on Improvement.",
                    """<p>When you gain a talent from Improvement, you can choose from the magic or martial talent lists.</p>"""),
                _sf(cid, cname, "war", "War", ["War Domain Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared war domain spells.",
                    _domain_spells_body({
                        2: ["command", "magic weapon", "shield of faith", "warding bond"],
                        5: ["fear", "spirit guardians"],
                        7: ["death ward", "guardian of faith"],
                        9: ["antilife shell", "flame strike"],
                    })),
                _sf(cid, cname, "war", "War", ["Blessed Warrior"], _ymiat_level_label("7th"),
                    "Martial weapon proficiency and Fitness-based attacks.",
                    """<p>You gain proficiency with martial weapons. You can use Fitness for attack and damage rolls with martial weapons.</p>"""),
                _sf(cid, cname, "war", "War", ["Greater Triumph"], _ymiat_level_label("11th"),
                    "Marked creatures have disadvantage on saves against your spells.",
                    """<p>Creatures marked by Mark of Triumph have disadvantage on saves against your Divine spells until the mark ends.</p>"""),
                _sf(cid, cname, "war", "War", ["Holy Strike"], _ymiat_level_label("15th"),
                    "Weapon attacks deal extra radiant damage once per turn.",
                    """<p>Once per turn when you hit with a weapon attack, the attack deals <strong>1d8 radiant damage</strong> in addition to the weapon's damage.</p>"""),
            ],
        ),
    ]


# ── DRUID ─────────────────────────────────────────────────────────────────────

def druid_subclasses():
    cid, cname = "druid", "Druid"
    return [
        _sub(
            cid, cname, "leaf", "Leaf",
            "Guardian of growing things and peaceful wild places.",
            [
                _sf(cid, cname, "leaf", "Leaf", ["Leaf Ring Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared leaf ring spells.",
                    _domain_spells_body({
                        2: ["barkskin", "entangle", "goodberry", "spike growth"],
                        5: ["plant growth", "speak with plants"],
                        7: ["blight", "freedom of movement"],
                        9: ["greater hold", "tree stride"],
                    })),
                _sf(cid, cname, "leaf", "Leaf", ["Green Song"], _ymiat_level_label("3rd"),
                    "Speak with plants; inspect flora with an action.",
                    """<p>As an <strong>action</strong>, focus on a nonmagical plant within 30 feet to learn if it is edible, poisonous, its typical environment, and its condition. Plant creatures understand your speech and you understand theirs.</p>""",
                    action="action"),
                _sf(cid, cname, "leaf", "Leaf", ["Wild Shape: Sacred Grove"], _ymiat_level_label("3rd"),
                    "Wild Shape creates a magical pocket grove.",
                    """<p>Expend Wild Shape as an <strong>action</strong> to create a 10-foot-radius sacred grove for 1 minute (one at a time). Choose one property:</p>
<ul>
<li><strong>Tangle Weed:</strong> difficult terrain; reaction to restrain movers (Fitness save vs spell DC).</li>
<li><strong>Tree Line:</strong> disadvantage on attacks against creatures in the grove; reaction to intercept one attack against you on solid ground (grove destroyed).</li>
<li><strong>Wildflowers:</strong> advantage vs charmed/frightened; bonus action to destroy grove and end one creature's conditions—allies on solid ground gain temp Wounds = PB.</li>
</ul>""",
                    action="action"),
                _sf(cid, cname, "leaf", "Leaf", ["Take Root"], _ymiat_level_label("7th"),
                    "Bonus action root yourself; spend hit dice for healing while rooted.",
                    """<p>As a <strong>free action</strong> on solid ground, root in place (speed 0, can't be moved or knocked prone) until you end it. If rooted when your turn begins, spend one hit die to regain Wounds = roll + Fitness modifier.</p>""",
                    action="free action"),
                _sf(cid, cname, "leaf", "Leaf", ["Grove Warden"], _ymiat_level_label("11th"),
                    "Sacred grove expands to 30 feet; choose who is immune to its effects.",
                    """<p>Sacred Grove radius becomes <strong>30 feet</strong>. You decide whether each ally (including yourself) is immune to any effects the grove imposes.</p>"""),
                _sf(cid, cname, "leaf", "Leaf", ["Heart of the Forest"], _ymiat_level_label("15th"),
                    "Grove saves you at 0 Wounds; acorn resurrection if destroyed.",
                    """<p>At 0 Wounds inside your sacred grove, the grove withers and you regain Wounds equal to your druid level (once per long rest). If your body is destroyed, an acorn remains; if undisturbed or planted, you gain a new body in 1d10 days with full Wounds.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "shifter", "Shifter",
            "Master of beast forms and primal transformation.",
            [
                _sf(cid, cname, "shifter", "Shifter", ["Potent Forms"], _ymiat_level_label("3rd"),
                    "Higher-CR beast forms; speak while transformed.",
                    """<p>Choose beast forms with CR up to 1 (scaling with level per Improved Beast Form). You use the creature's Max Wounds when you transform. You can speak languages you know in beast form but still can't cast spells.</p>"""),
                _sf(cid, cname, "shifter", "Shifter", ["Quick Shift"], _ymiat_level_label("3rd"),
                    "Beast Form as a free action.",
                    """<p>When you use Beast Form, you can transform as a <strong>free action</strong> instead of an action.</p>""",
                    action="free action"),
                _sf(cid, cname, "shifter", "Shifter", ["Shifter Ring Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared shifter ring spells.",
                    _domain_spells_body({
                        2: ["alter self", "animal friendship", "speak with animals"],
                        5: ["conjure animals", "water breathing"],
                        7: ["giant insect", "polymorph"],
                        9: ["dominate", "insect plague"],
                    })),
                _sf(cid, cname, "shifter", "Shifter", ["Beast's Fury"], _ymiat_level_label("7th"),
                    "Bonus natural attack after Attack action in beast form.",
                    """<p>After you take the Attack action in beast form, you can use your <strong>second action</strong> (if you haven't moved) to make one natural weapon attack for <strong>1d6 + PB</strong> damage. Melee damage in beast form counts as magical.</p>"""),
                _sf(cid, cname, "shifter", "Shifter", ["Elemental Infusion"], _ymiat_level_label("11th"),
                    "Infuse beast form with air, earth, fire, or water power.",
                    """<p>Expend two Wild Shape uses to infuse your beast form with an elemental power (Air, Earth, Fire, or Water), gaining movement, resistance, and a rechargeable action per BFRD Shifter. Alternatively, spend one use as a reaction to switch infusion while transformed.</p>"""),
                _sf(cid, cname, "shifter", "Shifter", ["Manifold Mind"], _ymiat_level_label("15th"),
                    "Cast spells in beast form.",
                    """<p>You can cast Primordial spells while in beast form, performing verbal and somatic components normally. Material components still apply.</p>"""),
            ],
            "https://bfrd.net/classes/druid/druid-subclasses/shifter",
        ),
        _sub(
            cid, cname, "elementalist", "Elementalist",
            "Command acid, cold, fire, lightning, and thunder to protect nature.",
            [
                _sf(cid, cname, "elementalist", "Elementalist", ["Elemental Convergence"], _ymiat_level_label("3rd"),
                    "Bonus elemental cantrip; convert damage dice between elemental types.",
                    """<p>Learn one cantrip from: <em>acid splash</em>, <em>electric jolt</em>, <em>firebolt</em>, <em>hoarfrost</em>, <em>ray of frost</em>, or <em>shocking grasp</em>. It counts as Primordial and doesn't count against cantrips known. Switch it when you finish a long rest. When you deal damage with one of these cantrips, add extra damage of its type equal to your <strong>PB</strong>.</p>
<p>When you deal acid, cold, fire, lightning, or thunder damage, you can change any number of damage dice to one of the other listed types.</p>"""),
                _sf(cid, cname, "elementalist", "Elementalist", ["Elementalist Ring Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared elementalist ring spells.",
                    _domain_spells_body({
                        2: ["acid arrow", "burning hands", "shatter", "thunderwave"],
                        5: ["call lightning", "fireball"],
                        7: ["conjure minor elementals", "elemental shield"],
                        9: ["cone of cold", "conjure elemental"],
                    })),
                _sf(cid, cname, "elementalist", "Elementalist", ["Wild Shape: Elemental Conduit"], _ymiat_level_label("3rd"),
                    "Wild Shape becomes an elemental conduit with reactive powers.",
                    """<p>As a <strong>free action</strong>, expend Wild Shape to become a living elemental conduit for 10 minutes (or until dismissed, incapacitated, or dead).</p>
<p>As a <strong>reaction</strong> while active, choose one:</p>
<ul>
<li><strong>Elemental Absorption:</strong> When you take acid, cold, fire, lightning, or thunder damage, become resistant to that type until your next turn (immune if already resistant).</li>
<li><strong>Elemental Empowerment:</strong> When you deal elemental damage, reroll damage dice up to your <strong>Willpower modifier</strong> (minimum 1).</li>
<li><strong>Elemental Enervation:</strong> When a creature within 30 feet succeeds on a save vs. elemental damage, force it to reroll.</li>
</ul>""",
                    action="free action / reaction"),
                _sf(cid, cname, "elementalist", "Elementalist", ["Elemental Deflection"], _ymiat_level_label("7th"),
                    "Reaction: grant an ally resistance to incoming elemental damage.",
                    """<p>As a <strong>reaction</strong> when a friendly creature within 30 feet takes acid, cold, fire, lightning, or thunder damage, that creature becomes resistant to that type (including the triggering effect) until the start of its next turn. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "elementalist", "Elementalist", ["Elemental Bulwark"], _ymiat_level_label("11th"),
                    "Elemental conduit grants broad resistances and condition immunity.",
                    """<p>While using Elemental Conduit, you are resistant to acid, cold, fire, lightning, and thunder damage and immune to paralyzed, petrified, poisoned, and unconscious.</p>"""),
                _sf(cid, cname, "elementalist", "Elementalist", ["Elemental Flare"], _ymiat_level_label("15th"),
                    "Retaliate with elemental damage; extended conduit with movement modes.",
                    """<p>As a <strong>reaction</strong> when a creature within 5 feet hits you, it takes acid, cold, fire, lightning, or thunder damage (your choice) equal to half your druid level (rounded down).</p>
<p>Elemental Conduit now lasts 1 hour. While active, you gain burrowing, flying (hover), and swimming speeds equal to your walking speed.</p>""",
                    action="reaction"),
            ],
            "https://www.talesofthevaliant.com/",
        ),
        _sub(
            cid, cname, "fey", "Fey",
            "Summon seelie spirits and wield mercurial fey magic.",
            [
                _sf(cid, cname, "fey", "Fey", ["Enchanting Presence"], _ymiat_level_label("3rd"),
                    "Speak Sylvan; use Willpower for social checks vs. fey.",
                    """<p>You know Sylvan. Use your <strong>Willpower modifier</strong> instead of another ability on Willpower checks, and have advantage on Willpower checks when interacting with Fey.</p>"""),
                _sf(cid, cname, "fey", "Fey", ["Fey Ring Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared fey ring spells.",
                    _domain_spells_body({
                        2: ["charm", "disguise self", "misty step", "suggestion"],
                        5: ["conjure animals", "major image"],
                        7: ["conjure woodland beings", "dimension door"],
                        9: ["seeming", "tree stride"],
                    })),
                _sf(cid, cname, "fey", "Fey", ["Wild Shape: Seelie Spirit"], _ymiat_level_label("3rd"),
                    "Wild Shape summons a seasonal fey spirit with spectral effects.",
                    """<p>As a <strong>free action</strong>, expend Wild Shape to summon a spectral fey spirit within 60 feet (not a creature; doesn't occupy space). Choose a season (spring, summer, autumn, winter) per the Seelie Seasons table. Move it up to 30 feet and trigger its effect as a free action on your turn. Lasts 1 minute or until dismissed, incapacitated, or you end your turn more than 120 feet away.</p>
<ul>
<li><strong>Spring — Euphoric Perfume:</strong> One ally within 5 feet has advantage on its next save before your next turn.</li>
<li><strong>Summer — Fey Ferocity:</strong> One ally within 5 feet has advantage on its next attack before your next turn.</li>
<li><strong>Autumn — Enchanting Distraction:</strong> One hostile within 5 feet has disadvantage on its next attack before your next turn.</li>
<li><strong>Winter — Sorrowful Rebuke:</strong> When a chosen ally within 5 feet takes damage from a creature within 10 feet, that attacker makes a Fitness save vs. your spell DC or takes cold damage equal to your PB.</li>
</ul>""",
                    action="free action"),
                _sf(cid, cname, "fey", "Fey", ["Mercurial Magic"], _ymiat_level_label("7th"),
                    "Resist charm/unconscious; reaction to aid allies' saves vs. fey effects.",
                    """<p>You are resistant to charmed and unconscious. As a <strong>reaction</strong> when a friendly creature within 60 feet (including you) makes a save vs. charmed, frightened, poisoned, unconscious, or a Fey effect, grant advantage on that save. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "fey", "Fey", ["Superior Seelie"], _ymiat_level_label("11th"),
                    "Season spirits gain stronger seasonal effects and longer duration.",
                    """<p>Seelie Spirit effects range increases to 15 feet (20 for Sorrowful Rebuke). Spirit lasts up to 10 minutes. Each season gains a second effect:</p>
<ul>
<li><strong>Spring's Vigor:</strong> Next hit by target grants temp Wounds = PB.</li>
<li><strong>Summer's Exuberance:</strong> +10 ft speed until your next turn.</li>
<li><strong>Autumn's Charm:</strong> Hostile creature makes WIL save or is charmed until your next turn.</li>
<li><strong>Winter's Grasp:</strong> Hostile creature makes FIT save or is restrained until your next turn.</li>
</ul>"""),
                _sf(cid, cname, "fey", "Fey", ["Archfey's Blessing"], _ymiat_level_label("15th"),
                    "Ageless fey resilience; twin spirits with extended range.",
                    """<p>You can't die of old age. Immune to charmed and unconscious; resistant to frightened and poisoned.</p>
<p>Seelie Spirit range becomes 30 feet (40 for Sorrowful Rebuke), move 60 feet, and you can summon <strong>two spirits</strong> of different seasons per use, controlling both with one free action.</p>"""),
            ],
            "https://www.talesofthevaliant.com/",
        ),
        _sub(
            cid, cname, "stoneheart", "Stoneheart",
            "Wrap yourself in earthen armor and stand as nature's sentinel.",
            [
                _sf(cid, cname, "stoneheart", "Stoneheart", ["Stone Intuition"], _ymiat_level_label("3rd"),
                    "Enhanced shillelagh; advantage identifying stone and metal work.",
                    """<p>Learn <em>shillelagh</em> if you don't know it. Your <em>shillelagh</em> club or quarterstaff becomes stone (non-flammable, light as wood). You can shape a 1-foot cube of stone or earth into a club or quarterstaff.</p>
<p>Advantage on checks to determine the origin or purpose of metal or stone objects and structures.</p>"""),
                _sf(cid, cname, "stoneheart", "Stoneheart", ["Stoneheart Ring Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared stoneheart ring spells.",
                    _domain_spells_body({
                        2: ["boulder toss", "circle of stones", "entangle", "shield of faith"],
                        5: ["elemental fusion (earth only)", "meld into stone"],
                        7: ["stone shape", "stoneskin"],
                        9: ["conjure elemental (earth only)", "wall of stone"],
                    })),
                _sf(cid, cname, "stoneheart", "Stoneheart", ["Wild Shape: Earthen Armor"], _ymiat_level_label("3rd"),
                    "Wild Shape wraps you in protective earth armor.",
                    """<p>As a <strong>free action</strong> while not wearing armor, expend Wild Shape to don earthen armor for hours equal to your PB (or until you expend another use).</p>
<ul>
<li><em>Shillelagh</em> damage die becomes <strong>d10</strong>.</li>
<li>Burrowing speed equal to walking speed.</li>
<li>Tremorsense 10 feet.</li>
<li>AC = 13 + Willpower modifier.</li>
</ul>""",
                    action="free action"),
                _sf(cid, cname, "stoneheart", "Stoneheart", ["Stone's Vengeance"], _ymiat_level_label("7th"),
                    "Two attacks; earth pillars impose disadvantage on ally attacks.",
                    """<p>When you take the Attack action, make <strong>two attacks</strong>.</p>
<p>When a friendly creature within 30 feet on the ground is attacked, summon a pillar to impose disadvantage on the attack. If it still hits, the attacker takes bludgeoning damage equal to your druid level. PB uses per long rest.</p>"""),
                _sf(cid, cname, "stoneheart", "Stoneheart", ["Stone Sentinel"], _ymiat_level_label("11th"),
                    "Improved earthen armor: d12 shillelagh, AC 15 + WIL, silent burrowing.",
                    """<p>While Earthen Armor is active:</p>
<ul>
<li><em>Shillelagh</em> damage die becomes <strong>d12</strong>.</li>
<li>Double damage to objects/structures with metal or stone weapons.</li>
<li>Burrowing doesn't disturb material.</li>
<li>AC = 15 + Willpower modifier.</li>
<li>Tremorsense 20 feet.</li>
</ul>"""),
                _sf(cid, cname, "stoneheart", "Stoneheart", ["Stone Heart"], _ymiat_level_label("15th"),
                    "Resist acid and bludgeoning; immune while armored with temp Wounds each turn.",
                    """<p>Resistant to acid and bludgeoning. While Earthen Armor is active, immune to those types instead and gain temp Wounds equal to your PB at the start of each of your turns.</p>"""),
            ],
            "https://www.talesofthevaliant.com/",
        ),
    ]


# ── FIGHTER ─────────────────────────────────────────────────────────────────

def fighter_subclasses():
    cid, cname = "fighter", "Fighter"
    stunt_list = """<p>Stunt save DC = 8 + PB + Fitness modifier. Uses per short or long rest = PB + 1. One stunt per turn.</p>
<ul>
<li><strong>Arcing Strike</strong> (heavy melee): splash half damage to a second target in reach.</li>
<li><strong>Cheap Shot</strong> (melee): extra unarmed strike on hit during Attack action.</li>
<li><strong>Make It Count</strong>: single attack at +10; extra damage equal to fighter level.</li>
<li><strong>Parry</strong> (melee, reaction): reduce damage by 1d10 + PB.</li>
<li><strong>Redirect</strong> (reaction): reroll missed attack against adjacent target.</li>
<li><strong>Riposte</strong> (melee, reaction): attack when enemy misses you.</li>
<li><strong>Straight Through</strong> (ranged): splash half damage to adjacent target.</li>
<li><strong>Tactical Retreat</strong> (melee): move half speed after hit without opportunity attacks.</li>
</ul>"""
    advanced_stunts = """<ul>
<li><strong>Assassin's Ambush</strong>: double damage dice from hidden.</li>
<li><strong>Bulwark</strong> (shield, reaction): reduce spell damage by AC.</li>
<li><strong>Felling Sweep</strong> (heavy melee, action): one attack roll vs. all in reach.</li>
<li><strong>Preemptive Strike</strong> (melee, reaction): attack when foe enters reach.</li>
<li><strong>Rapid Release</strong> (ranged/thrown): bonus attack after Attack action.</li>
<li><strong>Wrestler's Clutch</strong> (melee): grapple on hit; stunts vs. grappled foe don't cost uses.</li>
</ul>"""
    return [
        _sub(
            cid, cname, "spell-blade", "Spell Blade",
            "Blend arcane magic with weapon mastery.",
            [
                _sf(cid, cname, "spell-blade", "Spell Blade", ["Arcane Spellcasting"], _ymiat_level_label("3rd"),
                    "Partial Arcane spellcasting (abjuration/evocation focus).",
                    """<p>You cast Arcane spells using <strong>Insight</strong> as your spellcasting ability (save DC 8 + PB + Insight; attack + PB + Insight).</p>
<p>At 2nd level: learn <strong>2 cantrips</strong> and <strong>3 1st-level</strong> abjuration or evocation spells (one may be from any school). You have <strong>2 1st-level slots</strong>, regained on a long rest. Learn additional cantrips and spells at 4th, 6th, and 8th level per the Spell Blade table in the Player's Guide (adapted to YMIAT spell levels).</p>
<p>When Improvement grants a talent, choose from magic or martial lists.</p>"""),
                _sf(cid, cname, "spell-blade", "Spell Blade", ["Enchant Weapon"], _ymiat_level_label("3rd"),
                    "Imbue a weapon (+1, scaling to +3); bonus action summon.",
                    """<p>After 1 hour of focus on a weapon (during a rest), imbue it as a magic weapon: <strong>bonus action</strong> to summon to your hand if on the same plane; <strong>+1</strong> to attack and damage (stacks with existing magic bonuses). Bonus becomes <strong>+2</strong> at 6th level and <strong>+3</strong> at 8th. Only one enchanted weapon at a time.</p>""",
                    action="bonus action"),
                _sf(cid, cname, "spell-blade", "Spell Blade", ["Spell Multiattack"], _ymiat_level_label("7th"),
                    "Replace one Multiattack swing with a cantrip.",
                    """<p>When you use Multiattack, you can replace one attack with casting a cantrip you know (casting time 1 action). Only one cantrip per Attack action.</p>"""),
                _sf(cid, cname, "spell-blade", "Spell Blade", ["Follow Through"], _ymiat_level_label("11th"),
                    "Weapon attack after casting a spell.",
                    """<p>When you take the Cast a Spell action, you can make one weapon attack as part of that same action if a target is in range.</p>"""),
                _sf(cid, cname, "spell-blade", "Spell Blade", ["Charged Strike"], _ymiat_level_label("15th"),
                    "Add Insight to melee damage; weapon damage counts as magical.",
                    """<p>Add your <strong>Insight modifier</strong> (minimum +1) to melee weapon damage in addition to Fitness or Dexterity. All weapon damage you deal is magical.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "weapon-master", "Weapon Master",
            "Mastery of chosen weapons and tactical stunts.",
            [
                _sf(cid, cname, "weapon-master", "Weapon Master", ["Mastery"], _ymiat_level_label("3rd"),
                    "Master three weapon types; reroll damage or weapon-option damage.",
                    """<p>Choose three simple or martial weapon types you have proficiency with. Once per turn when you roll damage with a mastered weapon, reroll the weapon damage dice and use either result. Once per turn with a mastered weapon option, you can roll damage even if the option normally wouldn't.</p>"""),
                _sf(cid, cname, "weapon-master", "Weapon Master", ["Stunts"], _ymiat_level_label("3rd"),
                    "Tactical maneuvers with weapon-specific requirements.",
                    stunt_list),
                _sf(cid, cname, "weapon-master", "Weapon Master", ["Deadly Flourish"], _ymiat_level_label("7th"),
                    "19–20 crits with mastered weapons; reaction attacks on crit.",
                    """<p>Attacks with mastered weapons crit on <strong>19–20</strong>. On a crit, use your reaction to either: make a ranged attack against up to PB creatures within 15 feet of the target, or make a separate melee attack against each creature within 5 feet of you.</p>"""),
                _sf(cid, cname, "weapon-master", "Weapon Master", ["Advanced Stunts"], _ymiat_level_label("11th"),
                    "Powerful stunts available whenever you could use a stunt.",
                    advanced_stunts),
                _sf(cid, cname, "weapon-master", "Weapon Master", ["Grand Finale"], _ymiat_level_label("15th"),
                    "Regain stunt uses when combat begins with none left.",
                    """<p>When combat begins with no Stunt uses remaining, regain <strong>3</strong> uses. Once per long rest.</p>"""),
            ],
            "https://bfrd.net/classes/fighter/fighter-subclasses/",
        ),
    ]


# ── ARTIFICER (Mechanist) ───────────────────────────────────────────────────

def artificer_subclasses():
    cid, cname = "artificer", "Artificer"
    metallurgist = _sub(
        cid, cname, "armorer", "Armorer",
        "Mystic metal armor and absorbing augments (BFRD Metallurgist).",
        [
            _sf(cid, cname, "armorer", "Armorer", ["Augment: Absorbing"], _ymiat_level_label("3rd"),
                "Armor/shield absorbs elemental damage and grants resistance.",
                """<p>Unique augment (doesn't count against known augments): when you take acid, cold, fire, force, lightning, poison, or thunder damage while wearing/wielding the item, use your reaction to reduce damage by <strong>2 × Insight modifier</strong> and gain resistance to that type for 1 minute. PB uses per long rest.</p>"""),
            _sf(cid, cname, "armorer", "Armorer", ["Mystic Metal"], _ymiat_level_label("3rd"),
                "Transmute armor into wearable mystic metal suit.",
                """<p>After 1 hour of focus, transmute a nonmagical suit of armor into <strong>mystic metal</strong> (AC 13 + Insight modifier; gauntlets 1d6 + FIT or INS; summon as free action within 5 feet). Reverts if another creature dons it.</p>"""),
            _sf(cid, cname, "armorer", "Armorer", ["Heavy Hitter"], _ymiat_level_label("7th"),
                "Extra force damage and improved crit range in mystic metal.",
                """<p>While wearing mystic metal: weapon attacks deal <strong>1d6 force</strong> (1d8 at 5th artificer level, 1d10 at 10th); crit on 19–20.</p>"""),
            _sf(cid, cname, "armorer", "Armorer", ["Juggernaut"], _ymiat_level_label("11th"),
                "Athletics advantage; charge grants attack advantage.",
                """<p>While in mystic metal: Athletics proficiency (or advantage if proficient); advantage on grapple/shove checks; if you move 15+ feet before a melee attack, advantage on that attack.</p>"""),
            _sf(cid, cname, "armorer", "Armorer", ["Full Metal"], _ymiat_level_label("15th"),
                "Brief immunity to physical damage.",
                """<p>As a free action, enter Full Metal for 1 minute: immune to B/P/S; resistance to all other damage. Auto-activates at 0 Wounds once per long rest.</p>""",
                action="free action"),
        ],
        "https://bfrd.net/classes/mechanist/",
    )
    stubs = [
        ("alchemist", "Alchemist", "Brew volatile concoctions and supportive elixirs."),
        ("artillerist", "Artillerist", "Deploy ranged magical ordnance."),
        ("battle-smith", "Battle Smith", "Field a steel defender companion."),
    ]
    alchemist = _sub(
        cid, cname, "alchemist", "Alchemist",
        "Brew volatile concoctions and supportive elixirs.",
        [
            _sf(cid, cname, "alchemist", "Alchemist", ["Experimental Elixir"], _ymiat_level_label("3rd"),
                "Long-rest elixir for yourself or an ally.",
                """<p>When you finish a long rest, create one experimental elixir in a vial. As a <strong>bonus action</strong>, a creature can drink it (or you can throw it 20 feet; shatter on impact). Roll d6 for the effect:</p>
<ul>
<li><strong>1–2 Healing:</strong> regain 2d4 + Insight Wounds.</li>
<li><strong>3 Swiftness:</strong> +10 ft speed for 1 hour.</li>
<li><strong>4 Resilience:</strong> +1 AC for 10 minutes.</li>
<li><strong>5 Flight:</strong> fly speed 10 ft for 10 minutes.</li>
<li><strong>6 Transformation:</strong> <em>alter self</em> for 10 minutes (Insight as spellcasting ability).</li>
</ul>
<p>Unexpended elixirs lose potency after 24 hours. PB elixirs per long rest at 8th level.</p>"""),
            _sf(cid, cname, "alchemist", "Alchemist", ["Alchemical Savant"], _ymiat_level_label("3rd"),
                "Add Insight to alchemist-spell damage and healing.",
                """<p>When you cast an artificer spell that restores Wounds or deals acid, fire, necrotic, or poison damage, add your <strong>Insight modifier</strong> to one Wound restoration or damage roll.</p>"""),
            _sf(cid, cname, "alchemist", "Alchemist", ["Restorative Reagents"], _ymiat_level_label("7th"),
                "Free healing when casting certain spells.",
                """<p>When you cast an artificer spell of 1st level or higher using a slot, the target (or you if self-targeted) regains Wounds equal to <strong>2d6 + Insight modifier</strong>.</p>"""),
            _sf(cid, cname, "alchemist", "Alchemist", ["Chemical Mastery"], _ymiat_level_label("11th"),
                "Resistance to acid/poison; greater restoration on demand.",
                """<p>You have resistance to acid and poison damage and are immune to the poisoned condition. As an action, touch a creature and end one of: poisoned, paralyzed, or petrified (once per long rest).</p>""",
                action="action"),
        ],
    )
    artillerist = _sub(
        cid, cname, "artillerist", "Artillerist",
        "Deploy ranged magical ordnance.",
        [
            _sf(cid, cname, "artillerist", "Artillerist", ["Arcane Grenades"], _ymiat_level_label("3rd"),
                "Throw force grenades; damage scales 1d8→4d8.",
                """<p>As an action (Use an Object) or by replacing one Attack action attack, throw an arcane grenade (range 20/60, proficient). Use Dexterity or Insight for attack; hit = force damage d8 + Insight (2d8 at 4th, 3d8 at 6th, 4d8 at 8th). One grenade per turn. PB modified grenades per short or long rest (dispersal, flash, kinetic, smoke—see Grenadier rules).</p>"""),
            _sf(cid, cname, "artillerist", "Artillerist", ["Augment: Explosive"], _ymiat_level_label("3rd"),
                "Unique augment: trap objects with force bursts.",
                """<p>Unique augment (doesn't count against known augments): imbue a Medium or smaller stationary item to explode on your trigger (10-ft sphere, DEX save vs augment DC, (PB+1)d6 force minimum 3d6). PB triggers per long rest.</p>"""),
            _sf(cid, cname, "artillerist", "Artillerist", ["Controlled Blasts"], _ymiat_level_label("7th"),
                "No close-range disadvantage; protect allies from your ordnance.",
                """<p>No disadvantage on ranged attacks (including grenades) from enemies within 5 feet. When your items or grenades deal damage or impose conditions, choose up to PB allies to be immune. You are immune to your own grenades and augment explosions. Two grenades per turn.</p>"""),
            _sf(cid, cname, "artillerist", "Artillerist", ["Superior Firepower"], _ymiat_level_label("15th"),
                "Turn misses into hits; extended range; disintegrating crits.",
                """<p>Once per turn when a grenade attack misses, turn it into a hit (Insight modifier uses per long rest). Grenade range 40/80. Crit that drops a foe to 0 Wounds disintegrates it (no magic items). Three grenades per turn.</p>"""),
        ],
    )
    battle_smith = _sub(
        cid, cname, "battle-smith", "Battle Smith",
        "Field a steel defender companion.",
        [
            _sf(cid, cname, "battle-smith", "Battle Smith", ["Battle Ready"], _ymiat_level_label("3rd"),
                "Insight for magic weapons; steel defender companion.",
                """<p>You can use <strong>Insight</strong> for attack and damage with magic weapons. You gain a <strong>steel defender</strong> (Medium Construct, PB + Insight AC, Wounds = 5 + five × artificer level). It acts after your turn, obeys commands, and makes force attacks (+ PB to hit, 1d8 + PB force). If reduced to 0 Wounds, revive after a long rest or 1-hour ritual.</p>"""),
            _sf(cid, cname, "battle-smith", "Battle Smith", ["Augment: Messenger"], _ymiat_level_label("3rd"),
                "Augment items with disruptive noise or remote voice.",
                """<p>Unique augment: imbue a held/worn item with disruptive noise (WIS save or deafened 1 round; break concentration) or Master's Voice (speak/hear through item 1 minute). PB activations per long rest.</p>"""),
            _sf(cid, cname, "battle-smith", "Battle Smith", ["Arcane Jolt"], _ymiat_level_label("7th"),
                "Defender or you jolt a hit for extra force and advantage.",
                """<p>When you or your defender hits with a magic weapon, add <strong>2d6 force</strong> damage. Once per turn when you cast an artificer spell, the next defender attack before your next turn has advantage.</p>"""),
            _sf(cid, cname, "battle-smith", "Battle Smith", ["Improved Defender"], _ymiat_level_label("15th"),
                "Defender gains Multiattack; jolt heals you.",
                """<p>Your steel defender makes <strong>two attacks</strong> when commanded to Attack. When you use Arcane Jolt, you or the defender regains Wounds equal to half the force damage dealt.</p>"""),
        ],
    )
    return [metallurgist, alchemist, artillerist, battle_smith]


# ── MONK ──────────────────────────────────────────────────────────────────────

def monk_subclasses():
    cid, cname = "monk", "Monk"
    return [
        _sub(
            cid, cname, "flickering-dark", "Flickering Dark",
            "Harness shadow energy between strikes.",
            [
                _sf(cid, cname, "flickering-dark", "Flickering Dark", ["Dark Flame"], _ymiat_level_label("3rd"),
                    "Bonus action shadow aura: clawing, grasp, or spreading darkness.",
                    """<p>As a <strong>free action</strong>, spend <strong>2 technique points</strong> for a 10-foot-radius magical darkness (moves with you, 1 minute, not dispelled by spells of 5th level or lower). Choose one property:</p>
<ul>
<li><strong>Clawing Shadows:</strong> creatures entering or starting turn inside take necrotic = martial arts die; you regain Wounds equal to necrotic dealt (Constructs/Undead unaffected).</li>
<li><strong>Grasp of Nothingness:</strong> unarmed strikes deal extra necrotic = PB.</li>
<li><strong>Spreading Darkness:</strong> action + 1 technique point to cast <em>darkness</em> without a slot.</li>
</ul>
<p>At 6th level, choose two properties instead of one.</p>""",
                    action="free action"),
                _sf(cid, cname, "flickering-dark", "Flickering Dark", ["Obsidian Eyes"], _ymiat_level_label("3rd"),
                    "Grant darkvision through magical darkness; upgrades at 4th/6th.",
                    """<p>After 1 minute of meditation (during a rest), grant a willing creature obsidian eyes until their next long rest: see in dim light, darkness, and magical darkness as bright light (60 ft). At 4th monk level they see invisible creatures; at 6th they can't be blinded.</p>"""),
                _sf(cid, cname, "flickering-dark", "Flickering Dark", ["Grace of Umbra"], _ymiat_level_label("7th"),
                    "Step of the Wind grants intangibility and shadow teleport.",
                    """<p>When you use Step of the Wind, you become insubstantial until end of next turn—outside sunlight you and your gear can move through narrow openings. Spend +1 technique point to teleport up to your speed to dim light, darkness, or magical darkness you can see. At 8th level, resistance to all damage except radiant while active.</p>"""),
                _sf(cid, cname, "flickering-dark", "Flickering Dark", ["Feeding Dark"], _ymiat_level_label("11th"),
                    "Weaken attackers in your magical darkness; long-range shadow step.",
                    """<p>Creatures starting turn in your magical darkness make a Fitness save or deal half damage with Fitness/Dexterity weapon attacks until end of turn. When a creature saves or fails, use a <strong>reaction</strong> to teleport up to 1 mile adjacent to it (once per long rest, or 3 technique points).</p>""",
                    action="reaction"),
                _sf(cid, cname, "flickering-dark", "Flickering Dark", ["Strike of Searing Shadow"], _ymiat_level_label("15th"),
                    "Reaction finisher that pulls foes toward a dying enemy.",
                    """<p>When you hit with a melee attack, use a <strong>reaction</strong> and spend <strong>5 technique points</strong>. Target makes Fitness save: 3d10 fire + 3d10 necrotic (half on success). Creatures you choose within 30 feet make Fitness save vs technique DC or take 2d10 force and are pulled 20 feet toward the target. Reducing a creature to 0 Wounds with this leaves its shadow permanently on the surface; you gain temp Wounds = half its Max Wounds.</p>""",
                    action="reaction"),
            ],
        ),
        _sub(
            cid, cname, "open-hand", "Open Hand",
            "Push, trip, and shatter foes with perfected technique.",
            [
                _sf(cid, cname, "open-hand", "Open Hand", ["Focus Intent"], _ymiat_level_label("3rd"),
                    "Reaction: add martial arts die to ally or enemy roll.",
                    """<p>When you or a creature within 5 feet makes an ability check or attack roll, use your <strong>reaction</strong> to roll your martial arts die and add or subtract it from the roll. Uses = Insight modifier per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "open-hand", "Open Hand", ["Open Hand Technique"], _ymiat_level_label("3rd"),
                    "Flurry of Blows imposes knockdown, push, or no reactions.",
                    """<p>When you hit with a Flurry of Blows attack, impose one effect: target can't take reactions until your next turn; Insight save or knocked prone; Fitness save or pushed 15 feet.</p>"""),
                _sf(cid, cname, "open-hand", "Open Hand", ["Wholeness of Body"], _ymiat_level_label("7th"),
                    "Heal when combat begins.",
                    """<p>When combat begins with at least 1 Wound remaining, regain Wounds equal to <strong>Fitness modifier + monk level</strong>.</p>"""),
                _sf(cid, cname, "open-hand", "Open Hand", ["Tranquil Soul"], _ymiat_level_label("11th"),
                    "Long-duration sanctuary via technique points.",
                    """<p>As an action, spend <strong>3 technique points</strong> to cast <em>sanctuary</em> on yourself until your next short or long rest (or until it ends normally).</p>""",
                    action="action"),
                _sf(cid, cname, "open-hand", "Open Hand", ["Quivering Palm"], _ymiat_level_label("15th"),
                    "Store lethal vibrations in a struck foe.",
                    """<p>As an action, make one unarmed strike. On a hit, spend <strong>4 technique points</strong> to store vibrations for days equal to monk level. Later, use an action to end them: target makes Fitness save or takes force damage equal to <strong>5 × monk level</strong> and is paralyzed; failure by 5+ is instant death. Cost increases by 2 per additional use until long rest.</p>""",
                    action="action"),
            ],
        ),
    ]


# ── PALADIN ───────────────────────────────────────────────────────────────────

def paladin_subclasses():
    cid, cname = "paladin", "Paladin"
    oath_spells = _domain_spells_body({
        2: ["sanctuary"],
        5: ["warding bond"],
        7: ["protection from energy"],
        9: ["stoneskin"],
        10: ["mass cure wounds"],
    })
    return [
        _sub(
            cid, cname, "devotion", "Devotion",
            "Oath-bound knight of duty, honor, and righteous order.",
            [
                _sf(cid, cname, "devotion", "Devotion",
                    ["Channel Divinity: Sacred Weapon", "Sacred Weapon"],
                    _ymiat_level_label("3rd"),
                    "Empower a held weapon with radiant light.",
                    """<p>As an action, imbue a held weapon for 1 minute: add Willpower modifier to attack rolls (min +1); bright light 20 ft. Weapon becomes magical for the duration.</p>""",
                    action="action"),
                _sf(cid, cname, "devotion", "Devotion",
                    ["Channel Divinity: Sanctifying Light", "Sanctifying Light"],
                    _ymiat_level_label("3rd"),
                    "Blind aberrations, fey, fiends, and undead.",
                    """<p>As an action, each Aberration, Fey, Fiend, or Undead within 30 feet that can see you makes a Willpower save or is blinded for 1 minute (Fitness save ends on self each turn).</p>""",
                    action="action"),
                _sf(cid, cname, "devotion", "Devotion", ["Devotion Oath Spells"], _ymiat_level_label("3rd"),
                    "Always-known oath spells.",
                    oath_spells),
                _sf(cid, cname, "devotion", "Devotion", ["Aura of Devotion"], _ymiat_level_label("7th"),
                    "Allies near you can't be charmed.",
                    """<p>You and friendly creatures within 10 feet can't be charmed while you are conscious (30 feet at 8th paladin level via Aura Improvements).</p>"""),
                _sf(cid, cname, "devotion", "Devotion", ["Purity of Spirit"], _ymiat_level_label("11th"),
                    "Protection from supernatural creatures.",
                    """<p>Against Aberrations, Celestials, Elementals, Fey, Fiends, Undead, and Outsiders: they have disadvantage attacking you; you can't be charmed, frightened, or possessed; Divine Sense detects all listed types.</p>"""),
                _sf(cid, cname, "devotion", "Devotion", ["Holy Nimbus"], _ymiat_level_label("15th"),
                    "Radiant sunlight aura damages enemies.",
                    """<p>As an action, emit sunlight (30 ft bright / 30 ft dim) for 1 minute. Enemies starting turn in bright light take radiant damage equal to paladin level. You have advantage on saves. Once per long rest.</p>""",
                    action="action"),
            ],
        ),
        _sub(
            cid, cname, "justice", "Justice",
            "Paladin of law who punishes the guilty without mercy.",
            [
                _sf(cid, cname, "justice", "Justice",
                    ["Channel Divinity: Burden of Guilt", "Burden of Guilt"],
                    _ymiat_level_label("3rd"),
                    "Curse a foe with halved speed and grounded flight.",
                    """<p>As a <strong>free action</strong>, curse one foe you can see within 30 feet for 1 minute: speed halved; if flying at end of turn, Willpower save or fall. Ends if you fall unconscious.</p>""",
                    action="free action"),
                _sf(cid, cname, "justice", "Justice",
                    ["Channel Divinity: Judgement", "Judgement"],
                    _ymiat_level_label("3rd"),
                    "Mark a quarry for advantage and radiant damage.",
                    """<p>As a <strong>free action</strong>, mark one target within 10 feet for 1 minute: advantage on attacks against it; weapon hits deal extra radiant = Willpower modifier. Ends if you damage another creature.</p>""",
                    action="free action"),
                _sf(cid, cname, "justice", "Justice", ["Justice Oath Spells"], _ymiat_level_label("3rd"),
                    "Always-known justice oath spells.",
                    _domain_spells_body({
                        2: ["pendulum"],
                        5: ["misty step"],
                        9: ["haste"],
                        10: ["greater invisibility"],
                    })),
                _sf(cid, cname, "justice", "Justice", ["Aura of Vigilance"], _ymiat_level_label("7th"),
                    "Allies near you reposition when combat begins.",
                    """<p>When combat begins, you and friendly creatures within 10 feet (30 feet at 8th paladin level) can each move up to <strong>10 feet</strong> without provoking opportunity attacks before the first turn. You must not be incapacitated.</p>"""),
                _sf(cid, cname, "justice", "Justice", ["Unworthy Adversary"], _ymiat_level_label("11th"),
                    "Reaction intercept: move toward attacker and strike judged quarry.",
                    """<p>When a creature within 30 feet attacks an ally, use your <strong>reaction</strong> to move up to half your speed toward the attacker. If the attacker is your Judgement target, make a weapon attack as part of the same reaction.</p>""",
                    action="reaction"),
                _sf(cid, cname, "justice", "Justice", ["Divine Executioner"], _ymiat_level_label("15th"),
                    "Hour-long avatar of decisive justice.",
                    """<p>As an <strong>action</strong>, channel order for 1 hour (once per long rest): reroll any damage you deal (must use new result); one extra attack when you take the Attack action; reaction when an enemy within 10 feet damages you or an ally forces that enemy to take half the damage dealt (same type).</p>""",
                    action="action"),
            ],
        ),
    ]


# ── RANGER ────────────────────────────────────────────────────────────────────

def ranger_subclasses():
    cid, cname = "ranger", "Ranger"
    return [
        _sub(
            cid, cname, "hunter", "Hunter",
            "Slayer of supernatural predators threatening the wilds.",
            [
                _sf(cid, cname, "hunter", "Hunter", ["Hunter Calling Spells"], _ymiat_level_label("3rd"),
                    "Always-known hunter spells.",
                    _domain_spells_body({
                        2: ["protection from evil and good"],
                        5: ["misty step"],
                        9: ["nondetection"],
                        10: ["banishment"],
                    })),
                _sf(cid, cname, "hunter", "Hunter", ["Killer Instinct"], _ymiat_level_label("3rd"),
                    "Learn target resistances and vulnerabilities.",
                    """<p>As a free action, learn a creature's immunities, resistances, and vulnerabilities within 60 feet (blocked by anti-divination). PB uses per long rest.</p>""",
                    action="free action"),
                _sf(cid, cname, "hunter", "Hunter", ["Relentless Pursuit"], _ymiat_level_label("3rd"),
                    "Extra damage vs. wounded quarry.",
                    """<p>Once per turn when you hit a creature below Max Wounds, deal extra damage equal to your Mystic Mark die (same damage type).</p>"""),
                _sf(cid, cname, "hunter", "Hunter", ["Favored Foe"], _ymiat_level_label("7th"),
                    "Prepare against a creature type after research.",
                    """<p>During a long rest, choose a creature type (Aberration, Beast, Celestial, etc.). For 24 hours, that type has disadvantage attacking you and you have advantage on saves vs. their charm, frighten, or possession.</p>"""),
                _sf(cid, cname, "hunter", "Hunter", ["No Escape"], _ymiat_level_label("11th"),
                    "Teleport to marked prey that tries to flee.",
                    """<p>When a creature marked by Mystic Mark moves, use your reaction to teleport up to 30 feet. If you end within reach, make an opportunity attack as part of the same reaction.</p>"""),
                _sf(cid, cname, "hunter", "Hunter", ["Predator's Shield"], _ymiat_level_label("15th"),
                    "Resistance to damage from a seen attacker.",
                    """<p>When you take damage from a creature you can see, use your reaction to gain resistance to all damage from that creature for 1 minute (including the triggering hit). Once per long rest.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "pack-master", "Pack Master",
            "Lead beast companions and coordinated pack tactics.",
            [
                _sf(cid, cname, "pack-master", "Pack Master", ["Beast Spirit"], _ymiat_level_label("3rd"),
                    "Ritual-bound beast spirit companion (avian, agile, aquatic, or sturdy).",
                    """<p>After a 1-hour ritual (during a rest), bind a beast spirit in a Medium animal form (avian/agile/aquatic/sturdy). It is friendly, shares your initiative (acts after you), and uses your PB in its statistics. Natural weapon: +4 + PB to hit, 1d8 + 4 + PB damage (B/P/S your choice). Multiattack count = half PB (rounded down). At 0 Wounds the body is destroyed; repeat ritual to recreate. See Pack Master stat block in Player's Guide.</p>"""),
                _sf(cid, cname, "pack-master", "Pack Master", ["Life Link"], _ymiat_level_label("3rd"),
                    "Reaction: take your companion's damage.",
                    """<p>When your beast spirit takes damage within 30 feet, use your <strong>reaction</strong> to take any amount of that damage instead (not reduced by your resistances). PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "pack-master", "Pack Master", ["Pack Master Calling Spells"], _ymiat_level_label("3rd"),
                    "Always-known pack master calling spells.",
                    _domain_spells_body({
                        2: ["animal friendship"],
                        5: ["wildsense"],
                        9: ["spirit guardians"],
                        10: ["polymorph"],
                    })),
                _sf(cid, cname, "pack-master", "Pack Master", ["Shared Mark"], _ymiat_level_label("7th"),
                    "Companion attacks are magical; extra damage vs Mystic Mark.",
                    """<p>Your beast spirit's attacks count as magical. While a creature bears your Mystic Mark, the spirit's hits deal extra damage equal to your Mystic Mark die (scales with ranger level).</p>"""),
                _sf(cid, cname, "pack-master", "Pack Master", ["Soul Bond"], _ymiat_level_label("11th"),
                    "Share spell targeting and delivery with your spirit.",
                    """<p>When you are targeted by a spell, your spirit within 30 feet can be targeted too and receives the same benefits. When you cast a non-self spell, your spirit within 100 feet can use its reaction to deliver it using your spellcasting modifier and DC.</p>""",
                    action="reaction"),
                _sf(cid, cname, "pack-master", "Pack Master", ["Undying Friendship"], _ymiat_level_label("15th"),
                    "Spirit sacrifice restores you at 0 Wounds.",
                    """<p>At 0 Wounds or instant death while your spirit is active, it can sacrifice itself: its body is destroyed and you return with Wounds equal to those it had. Requires a long rest before you can perform the binding ritual again.</p>"""),
            ],
        ),
    ]


# ── ROGUE ─────────────────────────────────────────────────────────────────────

def rogue_subclasses():
    cid, cname = "rogue", "Rogue"
    return [
        _sub(
            cid, cname, "enforcer", "Enforcer",
            "Intimidation, control, and ruthless precision.",
            [
                _sf(cid, cname, "enforcer", "Enforcer", ["Ambush"], _ymiat_level_label("3rd"),
                    "First-round advantage; auto-crit vs surprised foes.",
                    """<p>During the first round of combat, you have advantage on the first attack roll you make against each creature in the combat. Attacks against surprised creatures are automatic critical hits.</p>"""),
                _sf(cid, cname, "enforcer", "Enforcer", ["Cold-Blooded"], _ymiat_level_label("3rd"),
                    "Bonus attack when you drop a foe.",
                    """<p>Once per turn when you reduce a creature to 0 Wounds with a weapon attack, immediately make one additional weapon attack against a different creature within range (no Sneak Attack on this bonus attack).</p>"""),
                _sf(cid, cname, "enforcer", "Enforcer", ["Expanded Talent List"], _ymiat_level_label("3rd"),
                    "Martial or utility talents on Improvement.",
                    """<p>When you gain a talent from Improvement, choose from the martial or utility talent lists.</p>"""),
                _sf(cid, cname, "enforcer", "Enforcer", ["Brawler"], _ymiat_level_label("7th"),
                    "Sneak Attack in melee without ally adjacency; unarmed eligible.",
                    """<p>Sneak Attack works against a target within 5 feet even if no other creatures are adjacent—you don't need advantage but can't have disadvantage. Sneak Attack applies to unarmed strikes.</p>"""),
                _sf(cid, cname, "enforcer", "Enforcer", ["Ready to Rumble"], _ymiat_level_label("11th"),
                    "Can't be surprised; first-turn edge when combat begins.",
                    """<p>While not incapacitated, you can't be surprised. When combat begins and you aren't surprised, you have advantage on the first attack roll you make on your first turn.</p>"""),
                _sf(cid, cname, "enforcer", "Enforcer", ["Kill Shot"], _ymiat_level_label("15th"),
                    "Reroll Sneak Attack dice; Sneak Attack on opportunity attacks.",
                    """<p>When you roll Sneak Attack damage, reroll any dice (must use new results). You can apply Sneak Attack to an eligible opportunity attack if you haven't used Sneak Attack this round.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "thief", "Thief",
            "Climb, appraise, and strike before foes react.",
            [
                _sf(cid, cname, "thief", "Thief", ["Fast Hands"], _ymiat_level_label("3rd"),
                    "Cunning Action can sleight of hand, use object, or pick locks.",
                    """<p>Your Cunning Action free action can also: Sleight of Hand; Use an Object; or use thieves' tools to disarm a trap or open a lock.</p>"""),
                _sf(cid, cname, "thief", "Thief", ["Second-Story Work"], _ymiat_level_label("3rd"),
                    "Climbing speed and improved jumps.",
                    """<p>Climbing speed equals walking speed (+10 ft if you already had climbing speed). Long jump uses walking speed with 10 ft run-up; standing long jump half speed. May use Acrobatics instead of Athletics for jump checks.</p>"""),
                _sf(cid, cname, "thief", "Thief", ["Appraising Eye"], _ymiat_level_label("7th"),
                    "Identify value and magic of objects.",
                    """<p>Action to inspect an object within 10 feet: learn if nonmagical (and value) or magical (1 minute study reveals type, rarity, curse, attunement; can ignore class requirements after study).</p>""",
                    action="action"),
                _sf(cid, cname, "thief", "Thief", ["Trap Specialist"], _ymiat_level_label("11th"),
                    "Reaction disarm traps including magical ones.",
                    """<p>When you or an ally within 5 feet triggers a trap, reaction to disarm it. Magical traps: ability check using Fitness modifier vs. trap DC.</p>"""),
                _sf(cid, cname, "thief", "Thief", ["Thief's Reflexes"], _ymiat_level_label("15th"),
                    "Two turns in the first round of combat.",
                    """<p>When combat begins and you are not surprised, on your first turn you may take a <strong>second action</strong> as if you had moved 0 feet, <strong>without</strong> the usual penalties for a second action. You can't use this feature if you are surprised.</p>"""),
            ],
        ),
    ]


# ── SORCERER ────────────────────────────────────────────────────────────────

def sorcerer_subclasses():
    cid, cname = "sorcerer", "Sorcerer"
    return [
        _sub(
            cid, cname, "chaos", "Chaos",
            "Wild surges of uncontrolled arcane power.",
            [
                _sf(cid, cname, "chaos", "Chaos", ["Chaos Manifestation"], _ymiat_level_label("3rd"),
                    "Random surge on crit or dropping foes with spell attacks.",
                    """<p>When you reduce creatures to 0 Wounds or score a critical hit with a spell attack, roll d6 on the Chaos Manifestation table (invisibility, force burst, AC bonus, phasing, magical darkness, or teleport-with-risk). Once per turn.</p>"""),
                _sf(cid, cname, "chaos", "Chaos", ["Chaos Origin Spells"], _ymiat_level_label("3rd"),
                    "Always-known chaos origin spells.",
                    _domain_spells_body({
                        2: ["misty step", "shatter"],
                        5: ["blink", "hypnotic pattern"],
                        7: ["compulsion", "polymorph"],
                        9: ["seeming", "telekinesis"],
                        10: ["eyebite", "irresistible dance"],
                    })),
                _sf(cid, cname, "chaos", "Chaos", ["Volatile Magic"], _ymiat_level_label("3rd"),
                    "Leveled spells may trigger extra volatile effects.",
                    """<p>When you cast a spell of 1st level or higher, roll d20 vs volatile DC (<strong>20 − sorcerer level + spell level</strong>). On a failure the spell still resolves but you also roll on the Volatile Spell Effect table (see Player's Guide). At 0 Luck, roll twice and take the higher result.</p>"""),
                _sf(cid, cname, "chaos", "Chaos", ["Embrace Chaos"], _ymiat_level_label("7th"),
                    "Bonus action: suffer a volatile effect for sorcery points or temp Wounds.",
                    """<p>As a <strong>free action</strong>, roll on the Volatile Spell Effect table and suffer it as if targeted. Even result = gain PB sorcery points; odd result = gain temp Wounds = Fitness score for 1 hour. Once per short or long rest.</p>""",
                    action="free action"),
                _sf(cid, cname, "chaos", "Chaos", ["Inflict Disorder"], _ymiat_level_label("11th"),
                    "Redirect volatile effects onto attackers.",
                    """<p>When targeted by a spell or attack, use your <strong>reaction</strong> to roll on the Volatile Spell Effect table; spend 1 sorcery point to force the attacker to suffer the effect instead. Once per long rest, or spend 2 sorcery points to reuse.</p>""",
                    action="reaction"),
                _sf(cid, cname, "chaos", "Chaos", ["Apotheosis of Discord"], _ymiat_level_label("15th"),
                    "6th-level+ spells trigger a minute of chaotic mastery.",
                    """<p>When you cast a spell of 6th level or higher, become a conduit for 1 minute (until unconscious): metamagic costs −1 (min 0); resistance to all damage until end of next turn after casting a leveled spell; cast any known Arcane or origin spell (≤1 minute casting, spell level ≤ half PB) without slots or components. Once per long rest, or spend 15 sorcery points.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "draconic", "Draconic",
            "Innate power from draconic ancestry.",
            [
                _sf(cid, cname, "draconic", "Draconic", ["Draconic Resilience"], _ymiat_level_label("3rd"),
                    "Natural AC and extra Max Wounds.",
                    """<p>While not wearing armor: AC = 10 + Fitness modifier + Willpower modifier. Max Wounds increase by 1 per sorcerer level.</p>"""),
                _sf(cid, cname, "draconic", "Draconic", ["Dragon Ancestor"], _ymiat_level_label("3rd"),
                    "Draconic language and affinity; origin spells by dragon type.",
                    """<p>Choose a dragon type (sets damage type for later features). Speak, read, and write Draconic. On dragon-related ability checks, treat d20 rolls below your sorcerer level as equal to your sorcerer level.</p>
<p>You learn additional origin spells at 2nd, 5th, 7th, and 9th level per BFRD Draconic Origin table (adapted to YMIAT spell levels).</p>"""),
                _sf(cid, cname, "draconic", "Draconic", ["Elemental Affinity"], _ymiat_level_label("7th"),
                    "Add Willpower modifier to one damage roll of your ancestry type per cast.",
                    """<p>When you cast a spell that deals damage of your ancestry type, add your <strong>Willpower modifier</strong> to one damage roll of that spell.</p>"""),
                _sf(cid, cname, "draconic", "Draconic", ["Imperious Wings"], _ymiat_level_label("11th"),
                    "Sprout wings for fly speed.",
                    """<p>As a free action, sprout wings for fly speed equal to walking speed until dismissed. Creatures that see you have disadvantage avoiding frighten/intimidate. Can't use while wearing armor.</p>""",
                    action="free action"),
                _sf(cid, cname, "draconic", "Draconic", ["Draconic Vengeance"], _ymiat_level_label("15th"),
                    "Brand a foe vulnerable to your element.",
                    """<p>Action: target within 60 feet makes Willpower save or becomes vulnerable to your ancestry damage type until end of your next turn (immunity unchanged). Once per long rest, or spend 4 sorcery points to reuse.</p>""",
                    action="action"),
            ],
        ),
    ]


# ── WARLOCK ───────────────────────────────────────────────────────────────────

def warlock_subclasses():
    cid, cname = "warlock", "Warlock"
    pact_spells = _domain_spells_body({
        2: ["burning hands", "command"],
        5: ["scorching ray", "suggestion"],
        9: ["fireball", "stinking cloud"],
        10: ["blight", "wall of fire"],
    })
    return [
        _sub(
            cid, cname, "archfey", "Archfey",
            "Bargains with capricious fey lords.",
            [
                _sf(cid, cname, "archfey", "Archfey", ["Archfey Pact Spells"], _ymiat_level_label("3rd"),
                    "Always-known archfey pact spells.",
                    _domain_spells_body({
                        2: ["faerie fire", "sleep"],
                        5: ["calm emotions", "phantasmal force"],
                        9: ["blink", "plant growth"],
                        10: ["dominate beast", "greater invisibility"],
                    })),
                _sf(cid, cname, "archfey", "Archfey", ["Fey Presence"], _ymiat_level_label("3rd"),
                    "Action: charm or frighten creatures near you.",
                    """<p>As an <strong>action</strong>, each creature in a 10-foot cube originating from you makes a <strong>Willpower save</strong> or is charmed or frightened (your choice) until end of your next turn. Once per short or long rest.</p>""",
                    action="action"),
                _sf(cid, cname, "archfey", "Archfey", ["Misty Escape"], _ymiat_level_label("7th"),
                    "Turn invisible and teleport when hit.",
                    """<p>When you take damage, use your <strong>reaction</strong> to become invisible and teleport up to 60 feet to an unoccupied space you can see. Invisibility lasts until start of your next turn or until you attack or cast a spell. Once per short or long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "archfey", "Archfey", ["Beguiling Defenses"], _ymiat_level_label("11th"),
                    "Immune to charm; charmer must save or be charmed by you.",
                    """<p>You can't be charmed. When a creature tries to charm you, it makes a Willpower save; on a failure it is charmed by you for 1 minute or until it takes damage.</p>"""),
                _sf(cid, cname, "archfey", "Archfey", ["Dark Delirium"], _ymiat_level_label("15th"),
                    "Trap a foe in a fey illusion.",
                    """<p>As an <strong>action</strong>, one creature within 60 feet makes a Willpower save or is charmed and incapacitated, perceiving itself in an idyllic fey realm. The effect ends after 1 minute, if you dismiss it (no action), if the target takes damage, or if someone uses an action to shake the target awake. Once per long rest.</p>""",
                    action="action"),
            ],
        ),
        _sub(
            cid, cname, "fiend", "Fiend",
            "Power from a greater fiend patron.",
            [
                _sf(cid, cname, "fiend", "Fiend", ["Dark One's Blessing"], _ymiat_level_label("3rd"),
                    "Temp HP when foes fall nearby.",
                    """<p>When you reduce a hostile creature to 0 Wounds, or one within 30 feet does, gain temporary Wounds equal to <strong>PB + warlock level</strong> until expended or long rest.</p>"""),
                _sf(cid, cname, "fiend", "Fiend", ["Fiend Pact Spells"], _ymiat_level_label("3rd"),
                    "Always-known fiend pact spells.",
                    pact_spells),
                _sf(cid, cname, "fiend", "Fiend", ["Dark One's Own Luck"], _ymiat_level_label("7th"),
                    "Add 1d10 to a failed check or save.",
                    """<p>When you make an ability check or save, add <strong>1d10</strong>. Once per short or long rest.</p>"""),
                _sf(cid, cname, "fiend", "Fiend", ["Fiendish Resilience"], _ymiat_level_label("11th"),
                    "Resistance to a chosen damage type.",
                    """<p>After a short or long rest, choose a damage type. You have resistance until you choose again.</p>"""),
                _sf(cid, cname, "fiend", "Fiend", ["Hurl Through Hell"], _ymiat_level_label("15th"),
                    "Banish attacker through a nightmare.",
                    """<p>When you hit with an attack, the target disappears until end of your next turn, then returns (or nearest space). Non-fiends take <strong>10d10 psychic</strong> damage. Once per long rest.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "great-old-one", "Great Old One",
            "Whispers from beyond the stars.",
            [
                _sf(cid, cname, "great-old-one", "Great Old One", ["Great Old One Pact Spells"], _ymiat_level_label("3rd"),
                    "Always-known GOO pact spells.",
                    _domain_spells_body({
                        2: ["dissonant whispers", "hideous laughter"],
                        5: ["detect thoughts", "phantasmal force"],
                        9: ["clairvoyance", "sending"],
                        10: ["dominate beast", "evard's black tentacles"],
                    })),
                _sf(cid, cname, "great-old-one", "Great Old One", ["Awakened Mind"], _ymiat_level_label("3rd"),
                    "Telepathy with creatures you can see.",
                    """<p>You can communicate telepathically with any creature you can see within 30 feet. You don't need to share a language, but the target must understand at least one language.</p>"""),
                _sf(cid, cname, "great-old-one", "Great Old One", ["Entropic Ward"], _ymiat_level_label("7th"),
                    "Impose disadvantage on an attack against you.",
                    """<p>When a creature makes an attack roll against you, use your <strong>reaction</strong> to impose disadvantage. If the attack misses, you have advantage on the next attack roll you make against that creature before end of your next turn. Once per short or long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "great-old-one", "Great Old One", ["Thought Shield"], _ymiat_level_label("11th"),
                    "Psychic resistance; reflect psychic damage to attackers.",
                    """<p>You have resistance to psychic damage. When a creature deals psychic damage to you, that creature takes the same amount of psychic damage.</p>"""),
                _sf(cid, cname, "great-old-one", "Great Old One", ["Create Thrall"], _ymiat_level_label("15th"),
                    "Permanently charm a humanoid (until broken).",
                    """<p>As an <strong>action</strong>, one humanoid within 30 feet makes a Willpower save or is charmed by you until you use this feature again or until you die. The thrall obeys telepathic commands if you are on the same plane. The target repeats the save every time it takes damage, ending the effect on a success. Once per long rest.</p>""",
                    action="action"),
            ],
        ),
    ]


# ── WIZARD ────────────────────────────────────────────────────────────────────

def wizard_subclasses():
    cid, cname = "wizard", "Wizard"
    return [
        _sub(
            cid, cname, "battle-mage", "Battle Mage",
            "Arcane offense with martial discipline.",
            [
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Expanded Talent List"], _ymiat_level_label("3rd"),
                    "Magic or martial talents on Improvement.",
                    """<p>When you gain a talent from Improvement, choose from magic or martial talent lists.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Spell Ward"], _ymiat_level_label("3rd"),
                    "AC and physical resistance after casting.",
                    """<p>When you cast an Arcane spell of 1st level+, weave a ward for 1 minute: <strong>+PB AC</strong> and resistance to B/P/S (ends if unconscious or you end a turn without casting a leveled spell). PB uses per long rest.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Tactical Caster"], _ymiat_level_label("3rd"),
                    "Allies immune to your damaging spells.",
                    """<p>When you cast a damaging Arcane spell, choose yourself and allies you can see to be immune to that spell's damage. PB uses per long rest.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Contingency Plan"], _ymiat_level_label("7th"),
                    "Redirect missed spell attack to another target.",
                    """<p>When a spell attack misses, use your reaction to redirect it to a different target in range with a new attack roll.</p>""",
                    action="reaction"),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Blasting Power"], _ymiat_level_label("11th"),
                    "Empowered spell damage after successful saves.",
                    """<p>When a creature succeeds on a save against your Arcane spell but takes no damage, it takes force damage equal to <strong>spell level d6 + Insight modifier</strong>.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Counterstrike"], _ymiat_level_label("15th"),
                    "Punish creatures that save against your spells.",
                    """<p>When a creature succeeds on a save against your Arcane spell and would suffer no effect, it takes force damage per Blasting Power. Once per turn.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "cantrip-adept", "Cantrip Adept",
            "Cantrip mastery and ritual ingenuity.",
            [
                _sf(cid, cname, "cantrip-adept", "Cantrip Adept", ["Arcane Alacrity"], _ymiat_level_label("3rd"),
                    "Cast action cantrips as bonus actions.",
                    """<p>When you cast an Arcane cantrip with casting time 1 action, you can cast it as a <strong>bonus action</strong> for that casting. PB uses per long rest.</p>""",
                    action="bonus action"),
                _sf(cid, cname, "cantrip-adept", "Cantrip Adept", ["Cantrip Polymath"], _ymiat_level_label("3rd"),
                    "Learn cantrips from any magic source.",
                    """<p>Learn <strong>two cantrips</strong> from any spell list; they count as Arcane cantrips and don't count against cantrips known. Any cantrip from lineage or talents also counts as Arcane for you.</p>"""),
                _sf(cid, cname, "cantrip-adept", "Cantrip Adept", ["Versatile Cantrips"], _ymiat_level_label("7th"),
                    "Swap one cantrip after each rest.",
                    """<p>When you finish a short or long rest, replace one Arcane cantrip you know with another from your available lists (including Polymath picks).</p>"""),
                _sf(cid, cname, "cantrip-adept", "Cantrip Adept", ["Potent Cantrip"], _ymiat_level_label("11th"),
                    "Add Insight to one cantrip damage roll.",
                    """<p>Add your <strong>Insight modifier</strong> to one damage roll of any Arcane cantrip you cast.</p>"""),
                _sf(cid, cname, "cantrip-adept", "Cantrip Adept", ["Empowered Cantrips"], _ymiat_level_label("15th"),
                    "Maximum damage on cantrips.",
                    """<p>Once per turn when you cast a damaging Arcane cantrip, deal maximum damage. PB uses per long rest.</p>"""),
            ],
        ),
    ]


# ── THEURGE (ToV PG2) ───────────────────────────────────────────────────────

def theurge_subclasses():
    cid, cname = "theurge", "Theurge"
    tov = "https://www.talesofthevaliant.com/"
    return [
        _sub(
            cid, cname, "conduit", "Conduit",
            "Exchange vitality for spell power and disrupt enemy magic.",
            [
                _sf(cid, cname, "conduit", "Conduit", ["Energy Exchange"], _ymiat_level_label("3rd"),
                    "Trade Recovery Points or spell levels for spell recovery or item charges.",
                    """<p><strong>Exchange Life:</strong> Bonus action: expend Recovery Points equal to a spell level to recover that level (lose Wounds equal to rolls + Fitness modifier; reduce Max Wounds until long rest).</p>
<p><strong>Exchange Power:</strong> Action: expend a spell level to restore charges to a touched magic item.</p>""",
                    action="bonus action / action"),
                _sf(cid, cname, "conduit", "Conduit", ["Mystic Vitality"], _ymiat_level_label("3rd"),
                    "Unspent spell levels become Recovery Points on rest.",
                    """<p>After a long rest, regain extra Recovery Points equal to half your unspent spell levels (rounded down), up to your maximum.</p>"""),
                _sf(cid, cname, "conduit", "Conduit", ["Metabolize"], _ymiat_level_label("7th"),
                    "Store incoming energy to upcast a spell.",
                    """<p>Reaction when you take non-B/P/S damage: Fitness save (DC 10 or half damage). On success, store energy up to 1 minute; expend it to cast a spell one level higher. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "conduit", "Conduit", ["Spell Surge"], _ymiat_level_label("11th"),
                    "Expend Recovery Points to add spell damage.",
                    """<p>When your Arcane or Divine spell damages a creature, expend Recovery Points and add Fitness modifier; one target takes extra damage of the spell's type.</p>"""),
                _sf(cid, cname, "conduit", "Conduit", ["Nullify"], _ymiat_level_label("15th"),
                    "Suppress a creature's or item's magic.",
                    """<p>Action: suppress magic on one creature or item within 120 feet for 1 minute. Creatures must pass Fitness saves to cast or attack with magic. Items function as nonmagical. Once per long rest.</p>""",
                    action="action"),
            ],
            tov,
        ),
        _sub(
            cid, cname, "illuminary", "Illuminary",
            "Inscribe sacred signs and sigils to extend your magic.",
            [
                _sf(cid, cname, "illuminary", "Illuminary", ["Mystic Scribe"], _ymiat_level_label("3rd"),
                    "Learn languages and artist tools mastery.",
                    """<p>Gain artist's tools proficiency (double PB if proficient). Over 10 minutes, temporarily learn a language until you use this again.</p>"""),
                _sf(cid, cname, "illuminary", "Illuminary", ["Sacred Sign"], _ymiat_level_label("3rd"),
                    "Mark allies to cast touch spells at range.",
                    """<p>Bonus action: inscribe your symbol on a willing creature for 10 minutes. While active, cast touch spells on them within 120 feet; action to see through their senses.</p>
<p>Active symbols: 1 at 2nd level, 2 at 4th, 3 at 6th, 4 at 8th.</p>""",
                    action="bonus action"),
                _sf(cid, cname, "illuminary", "Illuminary", ["Spell Sigil"], _ymiat_level_label("7th"),
                    "Store spells in inscribed items.",
                    """<p>Action: inscribe a spell into a worn/wielded item for 24 hours. You or a designated ally activates it with an action. Half PB sigils active at once.</p>""",
                    action="action"),
                _sf(cid, cname, "illuminary", "Illuminary", ["Guarding Glyph"], _ymiat_level_label("11th"),
                    "Marked allies share defensive bonuses.",
                    """<p>When you mark a creature with Sacred Sign, you gain a reciprocal mark. You and marked allies within 30 feet gain +1 AC and saves per marked ally nearby.</p>"""),
                _sf(cid, cname, "illuminary", "Illuminary", ["Potent Symbol"], _ymiat_level_label("15th"),
                    "Cast symbol without cost.",
                    """<p>Action: cast <em>symbol</em> without Spell Power or components. Once per long rest.</p>""",
                    action="action"),
            ],
            tov,
        ),
        _sub(
            cid, cname, "source-spinner", "Source Spinner",
            "Unravel and realign the weave of magic.",
            [
                _sf(cid, cname, "source-spinner", "Source Spinner", ["Magic Theory"], _ymiat_level_label("3rd"),
                    "Bonus Spellcraft on magic knowledge; extra prepared spells.",
                    """<p>Add a Spellcraft die to magic knowledge checks without expending it. Gain additional always-prepared spells (<em>detect magic</em>, <em>perceive vulnerability</em>, and higher-level spells as you level).</p>"""),
                _sf(cid, cname, "source-spinner", "Source Spinner", ["Overwrite"], _ymiat_level_label("3rd"),
                    "End a spell when you cast on the same target.",
                    """<p>When you cast a spell on a creature, attempt to end one ongoing spell on it (auto if equal/lower spell level; otherwise Insight check vs. 10 + spell level).</p>"""),
                _sf(cid, cname, "source-spinner", "Source Spinner", ["Mystic Realignment"], _ymiat_level_label("7th"),
                    "Trade spell levels for recovered levels.",
                    """<p>Bonus action: exchange spell levels for recovered levels of equal or lesser total value (see ToV Source Spinner rules).</p>""",
                    action="bonus action"),
                _sf(cid, cname, "source-spinner", "Source Spinner", ["Unravel"], _ymiat_level_label("11th"),
                    "Turn failed saves into successes.",
                    """<p>Reaction: when you or an ally within 30 feet fails a save vs. magic, cause success instead; source takes force damage equal to your theurge level. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "source-spinner", "Source Spinner", ["Spell Loom"], _ymiat_level_label("15th"),
                    "Manipulate magic in a small area.",
                    """<p>Action: for 1 minute, heal when casting spells, redirect single-target spells that miss or you save against, and gain temp Wounds. Once per short or long rest.</p>""",
                    action="action"),
            ],
            tov,
        ),
    ]


# ── VANGUARD (ToV PG2) ──────────────────────────────────────────────────────

def vanguard_subclasses():
    cid, cname = "vanguard", "Vanguard"
    tov = "https://www.talesofthevaliant.com/"
    return [
        _sub(
            cid, cname, "bulwark", "Bulwark",
            "Battlefield healer and protector with the Surgeon's Standard banner.",
            [
                _sf(cid, cname, "bulwark", "Bulwark", ["Battlefield Healer"], _ymiat_level_label("3rd"),
                    "Fast stabilization and Medicine mastery.",
                    """<p>Medicine proficiency (double PB if proficient). Stabilize dying creatures as a bonus action; they regain Wounds equal to vanguard level + Willpower modifier.</p>""",
                    action="bonus action"),
                _sf(cid, cname, "bulwark", "Bulwark", ["War Banner: Surgeon's Standard"], _ymiat_level_label("3rd"),
                    "Healing war banner.",
                    """<p>War banner option: at start of your turns, heal PB allies within range for 1d4 + Willpower (scales to 4d4 at 8th level).</p>"""),
                _sf(cid, cname, "bulwark", "Bulwark", ["Safeguard"], _ymiat_level_label("7th"),
                    "Protect nearby allies.",
                    """<p>Bonus action: +2 AC for you and allies within 5 feet until next turn; reaction to redirect single-target attacks/spells to you. PB uses per rest.</p>"""),
                _sf(cid, cname, "bulwark", "Bulwark", ["Turn the Tide"], _ymiat_level_label("11th"),
                    "Mass healing rally.",
                    """<p>Action: expend vanguard Recovery Points; you and allies within 30 feet regain Wounds equal to total + Willpower modifier.</p>""",
                    action="action"),
                _sf(cid, cname, "bulwark", "Bulwark", ["Bastion of Defense"], _ymiat_level_label("15th"),
                    "Enhanced safeguard stance.",
                    """<p>While Safeguard is active: temp Wounds when activating; advantage and resistance vs. area damage for nearby allies.</p>"""),
            ],
            tov,
        ),
        _sub(
            cid, cname, "herald", "Herald",
            "Living standard-bearer who teleports allies through battle.",
            [
                _sf(cid, cname, "herald", "Herald", ["Color Guard"], _ymiat_level_label("3rd"),
                    "Move banners and extend stratagem range.",
                    """<p>Start of turn: move an active banner up to 30 feet. Allies need not see the banner; stratagems need not be seen or heard.</p>"""),
                _sf(cid, cname, "herald", "Herald", ["War Banner: Stirring Sign"], _ymiat_level_label("3rd"),
                    "Speed and extra attack banner.",
                    """<p>Allies starting turn in banner range double speed, gain advantage on Fitness saves, and can make one extra weapon attack when they Attack.</p>"""),
                _sf(cid, cname, "herald", "Herald", ["Regroup"], _ymiat_level_label("7th"),
                    "Teleport allies within banner range.",
                    """<p>Bonus action: teleport yourself or a willing ally within banner radius. Reaction: teleport a damaged ally into the radius.</p>"""),
                _sf(cid, cname, "herald", "Herald", ["Double Standard"], _ymiat_level_label("11th"),
                    "Two banner effects at once.",
                    """<p>When you plant a war banner, choose two active effects instead of one.</p>"""),
                _sf(cid, cname, "herald", "Herald", ["Flag Bearer"], _ymiat_level_label("15th"),
                    "Unlimited banners and emergency recovery.",
                    """<p>War Banner unlimited uses; banners persist if you are incapacitated. End a banner to regain Wounds (level × Willpower) when below half Max Wounds. Once per long rest.</p>"""),
            ],
            tov,
        ),
        _sub(
            cid, cname, "marshal", "Marshal",
            "Inspiring commander who coordinates allied strikes.",
            [
                _sf(cid, cname, "marshal", "Marshal", ["Inspiring Leadership"], _ymiat_level_label("3rd"),
                    "Grant advantage via stratagems.",
                    """<p>When you use Stratagems, grant advantage on the next attack to 1 ally (2 at 4th, 3 at 6th, 4 at 8th) who can see and hear you.</p>"""),
                _sf(cid, cname, "marshal", "Marshal", ["War Banner: Banner of Coordination"], _ymiat_level_label("3rd"),
                    "Coordinated attack banner.",
                    """<p>Allies in banner range gain +1 attack per other ally in range (max PB) until start of next turn.</p>"""),
                _sf(cid, cname, "marshal", "Marshal", ["General's Gambit"], _ymiat_level_label("7th"),
                    "Spend Recovery Points to fix failed rolls.",
                    """<p>When you or an ally within 30 feet fails a check or save, expend a Recovery Point and add the roll to the result.</p>"""),
                _sf(cid, cname, "marshal", "Marshal", ["Comrade in Arms"], _ymiat_level_label("11th"),
                    "Share advantage and bonus damage.",
                    """<p>When Inspiring Leadership grants advantage, you also gain advantage on your next attack. Hits with that advantage deal extra damage equal to PB + Willpower.</p>"""),
                _sf(cid, cname, "marshal", "Marshal", ["Battlefield Vigor"], _ymiat_level_label("15th"),
                    "Regain Wounds when bloodied.",
                    """<p>Start of turn below half Max Wounds (but above 0): regain Wounds equal to PB + Fitness modifier.</p>"""),
            ],
            tov,
        ),
    ]


# ── WITCH (ToV PG2) ─────────────────────────────────────────────────────────

def witch_subclasses():
    cid, cname = "witch", "Witch"
    tov = "https://www.talesofthevaliant.com/"
    return [
        _sub(
            cid, cname, "crimson-cord", "Crimson Cord",
            "Vitality witch who heals allies and wastes foes with blood magic.",
            [
                _sf(cid, cname, "crimson-cord", "Crimson Cord", ["Crimson Cord Coven Spells"], _ymiat_level_label("3rd"),
                    "Always-prepared coven spells.",
                    """<p>Gain coven spells at 2nd, 4th, 6th, and 8th level: <em>cure wounds</em>, <em>inflict wounds</em>, <em>restoration</em>, and higher-level healing and necrotic spells per ToV Crimson Cord table.</p>"""),
                _sf(cid, cname, "crimson-cord", "Crimson Cord", ["Life Transfer"], _ymiat_level_label("3rd"),
                    "Sacrifice Wounds to heal or harm.",
                    """<p>Action: sacrifice up to 4 × witch level Wounds to heal one creature within 30 feet or force a Fitness save for necrotic damage. PB uses per short or long rest.</p>""",
                    action="action"),
                _sf(cid, cname, "crimson-cord", "Crimson Cord", ["Wasting Hex"], _ymiat_level_label("3rd"),
                    "Hexes sap vitality.",
                    """<p>When you Hex a creature, it may take 2 × PB Wounds at turn start (Fitness save for half) and can't regain Wounds until next turn.</p>"""),
                _sf(cid, cname, "crimson-cord", "Crimson Cord", ["Sanguine Link"], _ymiat_level_label("7th"),
                    "Mystical blood bond.",
                    """<p>Action: link with a willing creature (reduce Max Wounds by 10). Linked targets can receive Life Transfer and <em>cure wounds</em> at range. Half PB links active.</p>""",
                    action="action"),
                _sf(cid, cname, "crimson-cord", "Crimson Cord", ["Scarlet Web"], _ymiat_level_label("15th"),
                    "Area life-drain and healing aura.",
                    """<p>Action: for 1 minute, hostiles in 30 feet take Wounds on entry/start of turn; allies ending turn nearby heal. Advantage on Fitness saves; resistance to nonmagical B/P/S. Once per long rest.</p>""",
                    action="action"),
            ],
            tov,
        ),
        _sub(
            cid, cname, "night-song", "Night Song",
            "Predator witch empowered by darkness and night blessings.",
            [
                _sf(cid, cname, "night-song", "Night Song", ["Night Blessing"], _ymiat_level_label("3rd"),
                    "Darkvision and nightly predator gifts.",
                    """<p>Advantage on Stealth in dim light/darkness; darkvision 60 feet (+30 if you already have it). After each long rest, choose Night Children, Night Crawler, or Night Creature blessing.</p>"""),
                _sf(cid, cname, "night-song", "Night Song", ["Rending Hex"], _ymiat_level_label("3rd"),
                    "Hexed prey takes extra weapon damage.",
                    """<p>When a hexed creature takes weapon damage, add Hex die + Willpower to damage without expending the die. Below half Wounds, Fitness save or allies gain advantage vs. target.</p>"""),
                _sf(cid, cname, "night-song", "Night Song", ["Draining Curse"], _ymiat_level_label("7th"),
                    "Curse prey and drain their life.",
                    """<p>Action or with Hex: sacrifice a Recovery Point to curse a creature for 1 hour; damage to cursed targets heals you up to witch level. PB uses per long rest.</p>"""),
                _sf(cid, cname, "night-song", "Night Song", ["Enhanced Blessing"], _ymiat_level_label("11th"),
                    "Switch blessings on rest; stronger gifts.",
                    """<p>Change Night Blessing on short or long rest. Each blessing gains an additional benefit (charm beasts, B/P/S resistance, or fly speed).</p>"""),
                _sf(cid, cname, "night-song", "Night Song", ["Apex Predator"], _ymiat_level_label("15th"),
                    "Full night transformation.",
                    """<p>Action: for 1 minute, gain two blessings, advantage vs. cursed targets, and regain 20 Wounds each turn outside sunlight. Once per long rest.</p>""",
                    action="action"),
            ],
            tov,
        ),
        _sub(
            cid, cname, "twilight-soul", "Twilight Soul",
            "Spirit diplomat with a sentinel companion.",
            [
                _sf(cid, cname, "twilight-soul", "Twilight Soul", ["Obscuring Hex"], _ymiat_level_label("3rd"),
                    "Invisible to hexed targets.",
                    """<p>When you Hex a creature, you are invisible to it for up to 1 minute until you attack, damage, or target it with a spell.</p>"""),
                _sf(cid, cname, "twilight-soul", "Twilight Soul", ["Spirit Sentinel"], _ymiat_level_label("3rd"),
                    "Tiny spirit scout and spell origin.",
                    """<p>10-minute ritual summons a Tiny spirit (bat, raven, cat, etc.). Cast spells from its space; telepathic senses; command Move, Hinder, or Invisible tasks.</p>"""),
                _sf(cid, cname, "twilight-soul", "Twilight Soul", ["Ephemeral Shroud"], _ymiat_level_label("7th"),
                    "Teleport away from attacks.",
                    """<p>Reaction when hit by a single-target attack: teleport up to 60 feet; attack misses. PB uses per long rest.</p>""",
                    action="reaction"),
                _sf(cid, cname, "twilight-soul", "Twilight Soul", ["Welcomed Spirits"], _ymiat_level_label("11th"),
                    "Ritual communion with spirits.",
                    """<p>10-minute ceremony: expend Recovery Points to cast <em>augury</em>, <em>speak with dead</em>, or <em>commune with nature</em> without Spell Power.</p>"""),
                _sf(cid, cname, "twilight-soul", "Twilight Soul", ["Soul Sanctum"], _ymiat_level_label("15th"),
                    "Spirits shield you and punish foes.",
                    """<p>Action: for 1 minute, hostiles near you or your sentinel take force damage at turn start; attackers have disadvantage vs. you; hostiles have disadvantage on saves vs. your spells. Once per long rest.</p>""",
                    action="action"),
            ],
            tov,
        ),
    ]


def all_subclasses():
    from pg2_subclasses_data import pg2_only_subclasses

    groups = [
        barbarian_subclasses,
        bard_subclasses,
        cleric_subclasses,
        druid_subclasses,
        fighter_subclasses,
        artificer_subclasses,
        monk_subclasses,
        paladin_subclasses,
        ranger_subclasses,
        rogue_subclasses,
        sorcerer_subclasses,
        warlock_subclasses,
        wizard_subclasses,
        theurge_subclasses,
        vanguard_subclasses,
        witch_subclasses,
    ]
    result = []
    for fn in groups:
        result.extend(fn())
    result.extend(pg2_only_subclasses())
    return result


def all_subclass_features():
    features = []
    for sub in all_subclasses():
        features.extend(sub["features"])
    return features


def get_subclasses_by_class():
    by_class = {}
    for sub in all_subclasses():
        by_class.setdefault(sub["class_id"], []).append(sub)
    return by_class


def build_subclass_registry(features=None):
    from ability_utils import normalize_feature_name as norm
    registry = {}
    features = features or all_subclass_features()
    for feat in features:
        for name in feat["names"]:
            registry[(feat["class_id"], norm(name))] = feat["anchor"]
            registry[(feat["class_id"], name.lower())] = feat["anchor"]
    return registry
