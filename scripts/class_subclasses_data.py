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
                    """<p>Choose a fourth animal focus. While raging, you have advantage on initiative and can move up to half your speed when you enter a rage.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "chaos", "Chaos",
            "Entropic fury warps the battlefield around your rage.",
            _stub_features(
                cid, cname, "chaos", "Chaos",
                "YMIAT Chaos barbarian features are being drafted. Ask your GM for the current playtest packet.",
            ),
        ),
        _sub(
            cid, cname, "four-winds", "Four Winds",
            "Elemental winds empower your movement and strikes.",
            _stub_features(
                cid, cname, "four-winds", "Four Winds",
                "YMIAT Four Winds barbarian features are being drafted. Ask your GM for the current playtest packet.",
            ),
        ),
        _sub(
            cid, cname, "kraken", "Kraken",
            "Crushing tentacle-like force and abyssal resilience.",
            _stub_features(
                cid, cname, "kraken", "Kraken",
                "YMIAT Kraken barbarian features are being drafted. Ask your GM for the current playtest packet.",
            ),
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
                    "Choose talents from magic or technical lists.",
                    """<p>When you gain a new talent from Improvement, you can select it from either the <a href="../talents.html">magic</a> or <a href="../talents.html">technical</a> talent lists.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Jack of All Trades"], _ymiat_level_label("3rd"),
                    "Half PB on ability checks that don't already include PB.",
                    """<p>Add half your PB (rounded down) to any ability check that doesn't already include your PB.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Swift Ritual"], _ymiat_level_label("7th"),
                    "Cast a known ritual as an action once per long rest.",
                    """<p>You can cast an Arcane ritual you know as an <strong>action</strong> instead of its listed casting time. You must still provide all other components. Once used, you can't use this again until you finish a long rest.</p>""",
                    action="action"),
                _sf(cid, cname, "lore", "Lore", ["Magical Rites"], _ymiat_level_label("11th"),
                    "Learn two extra ritual spells from any source.",
                    """<p>Learn two ritual spells of your choice from any source list. Each must be of a circle you can cast. They count as Arcane spells for you and don't count against rituals known from your class table.</p>"""),
                _sf(cid, cname, "lore", "Lore", ["Peerless Skill"], _ymiat_level_label("15th"),
                    "Spend Bardic Inspiration on ability checks; keep the die on success.",
                    """<p>When you make an ability check and have Bardic Inspiration available, you can roll a Bardic Inspiration die and add it to the check. If you succeed, you keep the die; if you fail, the die is expended.</p>"""),
            ],
            "https://bfrd.net/classes/bard/bard-subclasses/",
        ),
        _sub(
            cid, cname, "victory", "Victory",
            "Inspire allies to triumph through martial cadence.",
            _stub_features(
                cid, cname, "victory", "Victory",
                "YMIAT Victory bard features are being drafted. See the <a href=\"https://bfrd.net/classes/bard/\" rel=\"noopener\">BFRD Bard</a> for inspiration.",
            ),
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
                    """<p>When you cast a Divine spell of 1st circle or higher to restore Wounds, the target regains <strong>2 + the spell's circle</strong> additional Wounds.</p>"""),
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
                    """<p>When you cast a Divine spell of 1st circle or higher that restores Wounds to another creature, you regain <strong>2 + the spell's circle</strong> Wounds.</p>"""),
                _sf(cid, cname, "life", "Life", ["Greater Preservation"], _ymiat_level_label("11th"),
                    "Expanded Preserve Life with condition cleansing.",
                    """<p>Preserve Life affects creatures within <strong>60 feet</strong>. When you use it, one target can also: cure all diseases; end blinded, deafened, paralyzed, or poisoned; or neutralize all poisons.</p>"""),
                _sf(cid, cname, "life", "Life", ["Perfect Healing"], _ymiat_level_label("15th"),
                    "Healing spells restore maximum Wounds.",
                    """<p>When you cast a Divine spell of 1st circle or higher that restores Wounds, you automatically restore the maximum possible Wounds (no dice rolling).</p>"""),
            ],
        ),
        _sub(
            cid, cname, "light", "Light",
            "Wield radiant fire and searing truth against darkness.",
            _stub_features(
                cid, cname, "light", "Light",
                "Light domain rules are being adapted for YMIAT. See BFRD Light domain for reference.",
            ),
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
            _stub_features(
                cid, cname, "leaf", "Leaf",
                "YMIAT Leaf druid features are being drafted. See BFRD Leaf ring for reference.",
            ),
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
            _stub_features(
                cid, cname, "spell-blade", "Spell Blade",
                "Spell Blade grants partial spellcasting (see multiclass rules). Full YMIAT Spell Blade features are being drafted.",
            ),
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
                    "Regain stunt uses when initiative is rolled with none left.",
                    """<p>When you roll initiative with no Stunt uses remaining, regain <strong>3</strong> uses. Once per long rest.</p>"""),
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
    return [metallurgist] + [
        _sub(cid, cname, sid, sname, desc, _stub_features(cid, cname, sid, sname, f"YMIAT {sname} artificer features are being drafted."))
        for sid, sname, desc in stubs
    ]


# ── MONK ──────────────────────────────────────────────────────────────────────

def monk_subclasses():
    cid, cname = "monk", "Monk"
    return [
        _sub(
            cid, cname, "flickering-dark", "Flickering Dark",
            "Harness shadow energy between strikes.",
            _stub_features(
                cid, cname, "flickering-dark", "Flickering Dark",
                "YMIAT Flickering Dark monk features are being drafted.",
            ),
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
                    "Heal when rolling initiative.",
                    """<p>When you roll initiative with at least 1 Wound remaining, regain Wounds equal to <strong>Fitness modifier + monk level</strong>.</p>"""),
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
            _stub_features(
                cid, cname, "justice", "Justice",
                "YMIAT Justice paladin features are being drafted. See BFRD Justice oath for reference.",
            ),
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
            _stub_features(
                cid, cname, "pack-master", "Pack Master",
                "YMIAT Pack Master ranger features are being drafted.",
            ),
        ),
    ]


# ── ROGUE ─────────────────────────────────────────────────────────────────────

def rogue_subclasses():
    cid, cname = "rogue", "Rogue"
    return [
        _sub(
            cid, cname, "enforcer", "Enforcer",
            "Intimidation, control, and ruthless precision.",
            _stub_features(
                cid, cname, "enforcer", "Enforcer",
                "YMIAT Enforcer rogue features are being drafted.",
            ),
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
                    """<p>Take two turns in round one: normal initiative and a second turn at initiative − 10. Can't use if surprised.</p>"""),
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
            _stub_features(
                cid, cname, "chaos", "Chaos",
                "YMIAT Chaos sorcerer features are being drafted.",
            ),
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
<p>You learn additional origin spells at 2nd, 5th, 7th, and 9th level per BFRD Draconic Origin table (adapted to YMIAT circles).</p>"""),
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
            _stub_features(
                cid, cname, "archfey", "Archfey",
                "YMIAT Archfey warlock features are being drafted. See BFRD Archfey patron for reference.",
            ),
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
            _stub_features(
                cid, cname, "great-old-one", "Great Old One",
                "YMIAT Great Old One warlock features are being drafted.",
            ),
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
                    """<p>When you cast an Arcane spell of 1st circle+, weave a ward for 1 minute: <strong>+PB AC</strong> and resistance to B/P/S (ends if unconscious or you end a turn without casting a leveled spell). PB uses per long rest.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Tactical Caster"], _ymiat_level_label("3rd"),
                    "Allies immune to your damaging spells.",
                    """<p>When you cast a damaging Arcane spell, choose yourself and allies you can see to be immune to that spell's damage. PB uses per long rest.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Contingency Plan"], _ymiat_level_label("7th"),
                    "Redirect missed spell attack to another target.",
                    """<p>When a spell attack misses, use your reaction to redirect it to a different target in range with a new attack roll.</p>""",
                    action="reaction"),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Blasting Power"], _ymiat_level_label("11th"),
                    "Empowered spell damage after successful saves.",
                    """<p>When a creature succeeds on a save against your Arcane spell but takes no damage, it takes force damage equal to <strong>spell circle d6 + Insight modifier</strong>.</p>"""),
                _sf(cid, cname, "battle-mage", "Battle Mage", ["Counterstrike"], _ymiat_level_label("15th"),
                    "Punish creatures that save against your spells.",
                    """<p>When a creature succeeds on a save against your Arcane spell and would suffer no effect, it takes force damage per Blasting Power. Once per turn.</p>"""),
            ],
        ),
        _sub(
            cid, cname, "cantrip-adept", "Cantrip Adept",
            "Cantrip mastery and ritual ingenuity.",
            _stub_features(
                cid, cname, "cantrip-adept", "Cantrip Adept",
                "YMIAT Cantrip Adept wizard features are being drafted.",
            ),
        ),
    ]


def all_subclasses():
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
    ]
    result = []
    for fn in groups:
        result.extend(fn())
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
