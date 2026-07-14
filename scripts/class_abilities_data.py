#!/usr/bin/env python3
"""YMIAT class ability definitions. Source: BFRD, adapted for 10-level play."""

from ability_utils import make_anchor, ability_href


def _a(class_id, class_name, names, level, summary, body, action=None):
    primary = names[0]
    entry = {
        "anchor": make_anchor(primary),
        "class_id": class_id,
        "class_name": class_name,
        "name": primary,
        "names": names,
        "level": level,
        "summary": summary,
        "body": body,
    }
    if action:
        entry["action"] = action
    return entry


def improvement_body(talent_list: str) -> str:
    return f"""<p>At 3rd, 5th, 7th, 9th, and 10th level, choose one improvement (ability modifiers cannot exceed +7 with this feature):</p>
<ul>
<li>Increase a single ability modifier by 2.</li>
<li>Increase two different ability modifiers by 1 each.</li>
<li>Increase one ability modifier by 1 and select a talent from the <a href="../talents.html">{talent_list}</a> list.</li>
</ul>"""


def multiattack_body(max_attacks: str) -> str:
    return f"""<p>Your physical prowess has grown. On your turn, you can make up to <strong>{max_attacks}</strong> attacks when you take the Attack action.</p>
<p>In YMIAT, each successful weapon attack typically inflicts <strong>1 Wound</strong> (2 on a critical hit). Weapon bonuses apply to hit, not to the number of Wounds dealt.</p>"""


def spellcasting_body(class_name, source, prep: str, key_ability: str) -> str:
    prep_text = {
        "prepared": f"You prepare spells in advance. You can prepare a number of spells equal to your {key_ability} modifier + your {class_name.lower()} level (minimum one). Change your prepared list during a long rest.",
        "known": "You know a fixed list of spells and do not prepare them daily. Learn additional spells at the levels shown on your class progression table.",
        "spellbook": f"You keep a spellbook. Prepare spells from it equal to your {key_ability} modifier + your {class_name.lower()} level (minimum one). Add two spells to your spellbook each time you gain a level.",
    }[prep]
    return f"""<p>As a conduit for <strong>{source}</strong> magic, you cast spells using <a href="../core.html#magic-and-spell-resources">Spell Power (SP)</a>. Spell cost equals spell circle. Your max spell circle by level is shown on the <a href="../classes.html#{class_name.lower().replace(' ', '-')}">{class_name}</a> progression table.</p>
<p>{prep_text}</p>
<p><strong>Spellcasting ability:</strong> {key_ability}. Spell save DC and spell attack modifier use your proficiency bonus + {key_ability} modifier.</p>
<p><strong>Cantrips &amp; rituals:</strong> As shown on your progression table. Rituals do not cost Spell Power when cast using the ritual rules in <a href="../magic.html">Magic</a>.</p>
<p><strong>Second action casting:</strong> If you cast a spell as your second action (because you did not move this turn), spell attacks are at disadvantage and targets have advantage on saves against that spell.</p>"""


def all_abilities():
    abilities = []

    # ── BARBARIAN ──────────────────────────────────────────────────────────
    cid, cname = "barbarian", "Barbarian"
    abilities += [
        _a(cid, cname, ["Rage"], "1st-level feature",
           "Primal fury as a free action; bonus damage and physical resilience.",
           """<p>In battle, you fight with primal ferocity. On your turn, you can <strong>rage as a free action</strong>.</p>
<p>While raging (and not wearing heavy armor):</p>
<ul>
<li>You have advantage on <strong>Fitness</strong> ability checks and saves.</li>
<li>When you make a melee weapon attack using Fitness, you gain a bonus to damage per the <strong>Rage +</strong> column on your progression table.</li>
<li>You have resistance to bludgeoning, piercing, and slashing damage—attackers have <strong>disadvantage</strong> on those damage rolls against you.</li>
</ul>
<p>You cannot cast spells or concentrate on them while raging.</p>
<p>Your rage lasts 1 minute. It ends early if you are knocked unconscious, or if your turn ends and you have not attacked a hostile creature or taken damage from one since the start of your last turn. You can end rage early as a free action.</p>
<p>Uses per long rest: see the <strong>Rages</strong> column on your progression table.</p>""",
           action="free action"),
        _a(cid, cname, ["Unarmored Defense"], "1st-level feature",
           "High AC without armor when relying on raw toughness.",
           """<p>While you are not wearing armor, your base Armor Class equals <strong>10 + 2 × your Fitness modifier</strong>. You can use a shield and still gain this benefit.</p>"""),
        _a(cid, cname, ["Danger Sense"], "1st-level feature",
           "Advantage on Fitness saves against unseen peril.",
           """<p>You gain an uncanny sense of when things are not as they should be. You have <strong>advantage on Fitness saving throws</strong> unless you have the Incapacitated condition.</p>"""),
        _a(cid, cname, ["Reckless Attack"], "1st-level feature",
           "Trade defense for ferocious accuracy.",
           """<p>When you make an attack on your turn, you can attack <strong>recklessly</strong>. You have advantage on melee weapon attack rolls using Fitness during this turn, but you have <strong>disadvantage on your Defense roll</strong> until the start of your next turn.</p>"""),
        _a(cid, cname, ["Fast Movement"], "3rd-level feature",
           "Extra speed and opening repositioning.",
           """<p>Your speed increases by <strong>10 feet</strong> while you are not wearing heavy armor. When combat begins and you are not surprised, you can move up to half your speed before any turns are taken. This movement does not use your movement on your turn.</p>"""),
        _a(cid, cname, ["Multiattack"], "3rd-level feature",
           "Two attacks with the Attack action.",
           multiattack_body("two")),
        _a(cid, cname, ["Feral Instinct"], "3rd-level feature",
           "First-turn ferocity and surprise immunity when raging.",
           """<p>On the first turn of each combat, you have <strong>advantage on melee weapon attack rolls</strong> (this stacks with weapon proficiency as normal).</p>
<p>If you are surprised at the start of combat and are not incapacitated, you can act normally on your first turn if you enter a rage before doing anything else on that turn.</p>
<p>When using the <a href="../combat.html#combat-order">initiative variant</a>, you have advantage on initiative rolls.</p>"""),
        _a(cid, cname, ["Brutal Critical", "Brutal Critical (1 die)", "Brutal Critical (2 dice)", "Brutal Critical (3 dice)"],
           "5th, 7th, and 9th level",
           "Expanded critical range and extra critical damage dice.",
           """<p>You score a critical hit on a d20 roll of <strong>19 or 20</strong> with melee weapons and unarmed strikes.</p>
<p>You also roll additional weapon damage dice on melee critical hits:</p>
<ul>
<li><strong>5th level:</strong> 1 extra die</li>
<li><strong>7th level:</strong> 2 extra dice</li>
<li><strong>9th level:</strong> 3 extra dice</li>
</ul>
<p>On a critical hit in YMIAT, the attack inflicts <strong>2 Wounds</strong> before applying extra dice (exploding 20s still apply).</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Choose a powerful rage-enhancing boon.",
           """<p>Choose one heroic boon:</p>
<ul>
<li><strong>Instant Rage.</strong> When combat begins and you use Fast Movement's opening move, you can enter a rage without spending a free action if you have a use of Rage remaining.</li>
<li><strong>Stubborn Rage.</strong> Your rage ends only when its duration expires, you fall unconscious, or you choose to end it.</li>
<li><strong>Bloody Rage.</strong> While raging, slashing damage from your weapon attacks ignores resistance.</li>
<li><strong>Vengeful Rage.</strong> When a hostile creature damages you while you are raging, you have stacking advantage on the first attack you make against that creature on your next turn.</li>
</ul>"""),
        _a(cid, cname, ["Relentless Rage"], "7th-level feature",
           "Cling to consciousness while raging at Max Wounds.",
           """<p>While raging, if your Wounds reach your Max Wounds, you can make a <strong>DC 10 Fitness save</strong>. On a success, you do not fall unconscious until your rage ends. You still make <a href="../combat.html#life-and-death-saves">death saves</a> as normal.</p>
<p>Each time you use this feature after the first, the DC increases by 5. The DC resets when you finish a short or long rest.</p>"""),
        _a(cid, cname, ["Unyielding Might"], "9th-level feature",
           "Reliable Fitness and devastating blows against objects.",
           """<p>When you make an ability check or save using Fitness, treat any d20 roll of 9 or lower as a 10.</p>
<p>Your melee weapon attacks deal additional damage equal to your <strong>Fitness score</strong> (not modifier) against objects and structures.</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Primal Champion", "Primal Champion"], "10th-level feature",
           "Embody untamed power.",
           """<p><strong>Primal Champion.</strong> Your Fitness modifier increases by <strong>2</strong>. Your maximum Fitness modifier is now <strong>+7</strong>.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a martial talent.",
           improvement_body("martial talents")),
    ]

    # ── BARD ───────────────────────────────────────────────────────────────
    cid, cname = "bard", "Bard"
    abilities += [
        _a(cid, cname, ["Bardic Inspiration", "Bardic Inspiration (d6)", "Bardic Inspiration (d8)", "Bardic Inspiration (d10)"],
           "1st, 4th, and 7th level",
           "Grant an inspiration die to bolster an ally's roll.",
           """<p>As an <strong>action</strong>, choose one creature other than yourself within 60 feet that can hear or see you. That creature gains one Bardic Inspiration die (d6 at 1st level, d8 at 4th, d10 at 7th).</p>
<p>Within the next 10 minutes, the creature can roll the die and add the result to one ability check, attack roll, or save. The die is then lost.</p>
<p>Uses per long rest equal to your <strong>Willpower modifier</strong> (minimum 1). See <a href="bard.html#font-of-inspiration">Font of Inspiration</a> at 3rd level.</p>""",
           action="action"),
        _a(cid, cname, ["Spellcasting"], "1st-level feature",
           "Arcane spells known; uses Spell Power.",
           spellcasting_body("Bard", "Arcane", "known", "Willpower (WIL)")),
        _a(cid, cname, ["Expertise", "Expertise (2)", "Expertise (4)"], "1st and 5th level",
           "Double proficiency on chosen skills or tools.",
           """<p>Choose two skill or tool proficiencies (or one of each). You have <strong>advantage</strong> on ability checks that use either proficiency.</p>
<p>At 5th level, choose two more proficiencies to gain this benefit.</p>"""),
        _a(cid, cname, ["Bardic Performance", "Bardic Performance (Celebrate Life, Cutting Words)",
                        "Celebrate Life", "Cutting Words", "Clarity of Thought",
                        "Bardic Performance: Clarity of Thought"], "2nd and 5th level",
           "Weave magic into ongoing performances.",
           """<p>As an <strong>action</strong>, begin a performance (Celebrate Life, Cutting Words, or Clarity of Thought at 5th level). Maintain it by spending an <strong>action</strong> at the start of each of your turns, up to 1 minute.</p>
<ul>
<li><strong>Celebrate Life.</strong> Allies in range can expend a Recovery die at the start of their turn to heal; allies have advantage on death saves.</li>
<li><strong>Cutting Words.</strong> Reaction while performing: subtract an inspiration die from an enemy's check, attack, or damage roll.</li>
<li><strong>Clarity of Thought (5th).</strong> Allies in range cannot be charmed and have advantage on saves against fear.</li>
</ul>
<p>Uses per long rest equal to your proficiency bonus.</p>"""),
        _a(cid, cname, ["Font of Inspiration"], "3rd-level feature",
           "Regain inspiration on short rest; bolster failed rolls.",
           """<p>You regain all expended uses of Bardic Inspiration when you finish a <strong>short or long rest</strong>.</p>
<p>When a creature within 60 feet fails a check, attack, or save, you can use your <strong>reaction</strong> to expend inspiration and add the die to the total, potentially turning failure into success.</p>"""),
        _a(cid, cname, ["Magical Secrets"], "6th and 9th level",
           "Learn spells from any source.",
           """<p>Choose two spells (or cantrips) from any spell list at 6th level and two more at 9th. Each must be of a circle you can cast. They count as Arcane spells for you.</p>"""),
        _a(cid, cname, ["Grand Performance"], "8th-level feature",
           "Performance range increases to 60 feet.",
           """<p>Your Bardic Performance now affects creatures within <strong>60 feet</strong> that can hear or see you.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Persistent or valiant inspiration options.",
           """<p>Choose one:</p>
<ul>
<li><strong>Persistent Inspiration.</strong> If a creature adds your inspiration die and still fails, the die is not lost.</li>
<li><strong>Valiant Inspiration.</strong> After a successful attack, the creature can expend the die for extra damage; or as a reaction when taking damage, reduce damage by die + your Willpower modifier.</li>
</ul>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Curtain Call", "Curtain Call"], "10th-level feature",
           "Recover inspiration during performance.",
           """<p><strong>Curtain Call.</strong> If you start your turn with no Bardic Inspiration uses remaining, you can recover uses equal to your Willpower modifier (minimum 1) as part of the action that maintains your performance. Once per long rest.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a technical talent.",
           improvement_body("technical talents")),
    ]

    # ── CLERIC ─────────────────────────────────────────────────────────────
    cid, cname = "cleric", "Cleric"
    abilities += [
        _a(cid, cname, ["Manifestation of Faith"], "1st-level feature",
           "Holy warrior or miracle worker path.",
           """<p>Choose how you manifest your faith:</p>
<ul>
<li><strong>Manifest Might.</strong> Proficiency with heavy armor and one martial weapon. Once per turn when you hit with a weapon attack, deal extra radiant or necrotic damage equal to your proficiency bonus.</li>
<li><strong>Manifest Miracles.</strong> Learn one extra cantrip from any source (counts as Divine). Add your proficiency bonus to damage dealt by your Divine cantrips.</li>
</ul>"""),
        _a(cid, cname, ["Spellcasting"], "1st-level feature",
           "Prepared Divine spells using Spell Power.",
           spellcasting_body("Cleric", "Divine", "prepared", "Insight (INS)")),
        _a(cid, cname, ["Channel Divinity", "Channel Divinity: Turn the Profane", "Turn the Profane",
                        "Channel Divinity (2/rest)", "Channel Divinity (3/rest)"],
           "2nd, 5th, and 9th level",
           "Channel divine energy beyond spells.",
           """<p>You channel divine energy as a <strong>free action</strong>. You start with <strong>Turn the Profane</strong>. Uses: 1/rest at 2nd, 2/rest at 5th, 3/rest at 9th. Regain all uses on a short or long rest.</p>
<p>See <a href="cleric.html#turn-the-profane">Turn the Profane</a> and <a href="cleric.html#destroy-the-profane">Destroy the Profane</a>.</p>""",
           action="free action"),
        _a(cid, cname, ["Turn the Profane"], "2nd-level feature",
           "Turn fiends and undead.",
           """<p>As an <strong>action</strong>, present your holy symbol. Each Fiend and Undead of your choice within 30 feet that can see or hear you makes an <strong>Insight save</strong> against your spell save DC. On a failure, the creature is <strong>turned</strong> for 1 minute or until it takes damage.</p>
<p>A turned creature must move away from you and can only Dash or Dodge on its turn.</p>"""),
        _a(cid, cname, ["Destroy the Profane", "Destroy the Profane (CR ½)", "Destroy the Profane (CR 1)",
                        "Destroy the Profane (CR 2)", "Destroy the Profane (CR 4)"],
           "4th, 6th, 8th, and 10th level",
           "Destroy turned creatures below a CR threshold.",
           """<p>When a Fiend or Undead fails its save against Turn the Profane, it is instantly destroyed if its CR is at or below:</p>
<ul>
<li><strong>4th level:</strong> CR ½</li>
<li><strong>6th level:</strong> CR 1</li>
<li><strong>8th level:</strong> CR 2</li>
<li><strong>10th level:</strong> CR 4</li>
</ul>"""),
        _a(cid, cname, ["Divine Intervention"], "7th-level feature",
           "Call on your deity in dire need.",
           """<p>At the start of your turn, roll d20 + proficiency bonus. On a <strong>19 or lower</strong>, your deity does not intervene. On <strong>20+</strong>, your deity intervenes.</p>
<p>On intervention, use your action to cast any Divine spell (or domain spell) of casting time action without spending Spell Power. If the circle exceeds your max, make a spellcasting ability check DC 10 + circle.</p>
<p>After a successful intervention, you cannot use this feature again for 1 week (or until a long rest once you have Epic Boon: Divine Herald).</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Consecration or wrath gifts.",
           """<p>Choose one:</p>
<ul>
<li><strong>Gift of Consecration.</strong> Immune to disease, poison damage, and poisoned. If you die, your body is preserved as <em>gentle repose</em> for up to a year.</li>
<li><strong>Gift of Wrath.</strong> Resistance to radiant or necrotic (your choice). When you cast a damaging spell, you can change its damage type to radiant or necrotic.</li>
</ul>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Divine Herald", "Divine Herald"], "10th-level feature",
           "Automatic divine intervention.",
           """<p><strong>Divine Herald.</strong> Divine Intervention succeeds automatically. You no longer wait a week between uses, though you can still use it only once per long rest.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a magic talent.",
           improvement_body("magic talents")),
    ]

    # Continue in part 2 - I'll append druid through wizard in same file
    abilities += _register_druid()
    abilities += _register_fighter()
    abilities += _register_artificer()
    abilities += _register_monk()
    abilities += _register_paladin()
    abilities += _register_ranger()
    abilities += _register_rogue()
    abilities += _register_sorcerer()
    abilities += _register_warlock()
    abilities += _register_wizard()

    return abilities


def _register_druid():
    cid, cname = "druid", "Druid"
    return [
        _a(cid, cname, ["Druidic"], "1st-level feature",
           "Secret language of druids.",
           """<p>You know Druidic. You can leave hidden messages in natural elements that only druids understand. Others spot the message with a successful Insight (Perception) check but cannot decipher it without magic.</p>"""),
        _a(cid, cname, ["Nature's Gift"], "1st-level feature",
           "Channel ambient energy to heal.",
           """<p>As an <strong>action</strong>, choose one creature within 5 feet (can be yourself). Roll a number of d4s equal to your proficiency bonus (minimum 2d4). That creature heals Wounds equal to the total. No effect on Constructs or Undead.</p>
<p>Uses per long rest equal to your proficiency bonus.</p>""",
           action="action"),
        _a(cid, cname, ["Spellcasting"], "1st-level feature",
           "Prepared Primordial spells.",
           spellcasting_body("Druid", "Primordial", "prepared", "Insight (INS)")),
        _a(cid, cname, ["Wild Shape", "Wild Shape (Beast Form, Draw Power)", "Wild Shape (2/rest)",
                        "Wild Shape (3/rest)", "Wild Shape (4/rest)"],
           "2nd level and higher",
           "Channel nature for beast forms and spell recovery.",
           """<p>You channel nature as a <strong>free action</strong> (Beast Form) or action (Draw Power). Uses per rest on your progression table.</p>
<ul>
<li><strong>Beast Form.</strong> Assume a known beast form. See <a href="druid.html#improved-beast-form">Improved Beast Form</a> for CR limits by level.</li>
<li><strong>Draw Power.</strong> Recover one expended spell circle up to your proficiency bonus. Cannot use while transformed.</li>
</ul>""",
           action="free action"),
        _a(cid, cname, ["Improved Beast Form", "Improved Beast Form (CR ¼)", "Improved Beast Form (CR ½)",
                        "Improved Beast Form (CR 1)", "Improved Beast Form (CR 2)"],
           "3rd level and higher",
           "Assume more powerful beast forms.",
           """<p>When you learn beast forms, maximum CR by level:</p>
<ul>
<li><strong>3rd:</strong> CR ¼</li>
<li><strong>5th:</strong> CR ½</li>
<li><strong>7th:</strong> CR 1</li>
<li><strong>9th:</strong> CR 2</li>
</ul>"""),
        _a(cid, cname, ["Nature's Grace"], "8th-level feature",
           "Attunement sustains and protects you.",
           """<p>You cannot be magically aged. You do not need food or water. Your ability modifiers and Max Wounds cannot be lowered except by a <em>wish</em>.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Rite of the Kingdom or Shaper.",
           """<p>Choose one:</p>
<ul>
<li><strong>Rite of the Kingdom.</strong> Communicate basic ideas with Beasts; advantage on checks to influence them.</li>
<li><strong>Rite of the Shaper.</strong> When combat begins with no Wild Shape uses left, regain one use (once per long rest).</li>
</ul>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Archdruid", "Archdruid"], "10th-level feature",
           "Unlimited wild shape; effortless spellcasting.",
           """<p><strong>Archdruid.</strong> Wild Shape (Beast Form) has unlimited uses. You can ignore verbal and somatic components of Primordial spells, and material components without a listed cost.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a magic talent.",
           improvement_body("magic talents")),
    ]


def _register_fighter():
    cid, cname = "fighter", "Fighter"
    return [
        _a(cid, cname, ["Last Stand"], "1st-level feature",
           "Emergency healing when badly wounded.",
           """<p>When damage would bring your Wounds above half your Max Wounds, you can use your <strong>reaction</strong> to spend hit dice (up to your proficiency bonus). Roll them and heal Wounds equal to the total + your Fitness modifier.</p>""",
           action="reaction"),
        _a(cid, cname, ["Martial Action"], "1st-level feature",
           "Tactical second action when you hold your ground.",
           """<p>Choose one martial action: <strong>Aim</strong>, <strong>Guard</strong>, <strong>Quick Strike</strong>, or <strong>Wind Up</strong> (see BFRD Fighter).</p>
<p>In YMIAT, use this as your <strong>second action</strong> when you have <strong>not moved</strong> this turn. If the second action is an attack, that attack is at <strong>disadvantage</strong>.</p>"""),
        _a(cid, cname, ["Action Surge", "Action Surge (2/rest)", "Action Surge (3/rest)"],
           "2nd, 7th, and 10th level",
           "Gain an additional action on your turn.",
           """<p>On your turn, gain <strong>another action</strong> in addition to your normal action. Once per short rest at 2nd level; twice at 7th; three times at 10th (still only once per turn).</p>"""),
        _a(cid, cname, ["Multiattack", "Multiattack (2)", "Multiattack (3)", "Multiattack (4)"],
           "3rd, 6th, and 9th level",
           "Multiple attacks per Attack action.",
           """<p>Make <strong>two</strong> attacks with the Attack action at 3rd level, <strong>three</strong> at 6th, and <strong>four</strong> at 9th.</p>
<p>In YMIAT, each successful weapon attack typically inflicts <strong>1 Wound</strong> (2 on a critical hit).</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Defiant saves or unstoppable recovery.",
           """<p>Choose one:</p>
<ul>
<li><strong>Defiant.</strong> When you fail a save, succeed instead. Once per long rest (twice at 7th, three times at 9th).</li>
<li><strong>Unstoppable.</strong> At the start of your turn, end one of: blinded, charmed, frightened, incapacitated, paralyzed, or stunned. Uses equal to proficiency bonus per long rest.</li>
</ul>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Turn the Tide", "Turn the Tide"], "10th-level feature",
           "Devastating blows that ignore defenses.",
           """<p>Once per turn when you hit with a weapon attack, deal extra damage equal to your <strong>Fitness or Insight score</strong> (your choice). The damage ignores resistance and immunity and cannot be reduced.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a martial talent.",
           improvement_body("martial talents")),
    ]


def _register_artificer():
    cid, cname = "artificer", "Artificer"
    return [
        _a(cid, cname, ["Eyes of the Maker"], "1st-level feature",
           "Identify magic items by touch.",
           """<p>When you touch a magic item, you learn its properties, attunement requirements, charges, active spells, and the spell that created it (if any).</p>"""),
        _a(cid, cname, ["Shard of Creation"], "1st-level feature",
           "Magical tool with versatile charges.",
           """<p>You craft a Tiny <strong>shard of creation</strong> (charges = Insight modifier, minimum 1, regained on long rest). Properties include <strong>Inspire</strong>, <strong>Mend</strong>, and other BFRD options. The shard vanishes if you die or if apart from you for 24 hours; recreate with a 1-hour ritual.</p>"""),
        _a(cid, cname, ["Augment"], "2nd-level feature",
           "Apply augment effects to carried items.",
           """<p>You apply augment effects to items you carry. Augment effects known and augmented item limits are on your progression table. See BFRD Mechanist augment list.</p>"""),
        _a(cid, cname, ["Efficient Action"], "2nd-level feature",
           "Augment without wasting effort.",
           """<p>When you use your action to apply an augment effect, you can apply a second effect to a different item as part of the same action.</p>"""),
        _a(cid, cname, ["Multiattack", "Multiattack (2)"], "3rd-level feature",
           "Two attacks per Attack action.", multiattack_body("two")),
        _a(cid, cname, ["Rapid Augment"], "4th-level feature",
           "Augment as a free action.",
           """<p>Once per turn, you can apply an augment effect as a <strong>free action</strong> instead of an action.</p>""",
           action="free action"),
        _a(cid, cname, ["Greater Creation"], "5th-level feature",
           "Craft more potent items.",
           """<p>You can create uncommon magic items using your shard and augment abilities per BFRD Greater Creation rules.</p>"""),
        _a(cid, cname, ["Engineer's Insight"], "6th-level feature",
           "Flash of mechanical genius.",
           """<p>When you fail an Insight check with a tool you are proficient in, you can reroll and take the higher result. Once per short or long rest.</p>"""),
        _a(cid, cname, ["Ranged Augment"], "7th-level feature",
           "Apply augments at range.",
           """<p>You can apply augment effects to items you can see within 30 feet.</p>"""),
        _a(cid, cname, ["Always Prepared"], "8th-level feature",
           "Augments persist through rest.",
           """<p>Augment effects you apply remain until you dismiss them (no action) or apply a new effect to that item.</p>"""),
        _a(cid, cname, ["Perfect Creation"], "9th-level feature",
           "Master-crafted magical items.",
           """<p>You can create rare magic items per BFRD Perfect Creation rules.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Artificer heroic options per BFRD.",
           """<p>Choose a heroic boon from the BFRD Mechanist list, adapted for YMIAT.</p>"""),
        _a(cid, cname, ["Epic Boon"], "10th-level feature",
           "Capstone invention.",
           """<p>Gain the Mechanist Epic Boon from BFRD, adapted for YMIAT.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or technical/martial talent.",
           improvement_body("technical or martial talents")),
    ]


def _register_monk():
    cid, cname = "monk", "Monk"
    return [
        _a(cid, cname, ["Martial Arts"], "1st-level feature",
           "Unarmed strikes and monk weapons.",
           """<p>While unarmed or wielding only monk weapons without armor or shield:</p>
<ul>
<li>Your unarmed strikes use the Martial Arts die from your progression table.</li>
<li>You use <strong>Fitness</strong> for attack and damage with unarmed strikes and monk weapons.</li>
<li>When you take the Attack action with an unarmed strike or monk weapon, you can make one unarmed strike as your <strong>second action</strong> if you have not moved (at disadvantage if it is an attack).</li>
</ul>"""),
        _a(cid, cname, ["Unarmored Defense"], "1st-level feature",
           "AC from agility and insight.",
           """<p>While unarmored and without a shield, AC = <strong>10 + Fitness modifier + Insight modifier</strong>.</p>"""),
        _a(cid, cname, ["Techniques"], "2nd-level feature",
           "Spend technique points on supernatural maneuvers.",
           """<p>Technique points per progression table, regained on short or long rest (30 min meditation). Options include <strong>Flurry of Blows</strong>, <strong>Patient Defense</strong>, <strong>Step of the Wind</strong>, and more. Save DC = 8 + PB + Insight modifier.</p>"""),
        _a(cid, cname, ["Unarmored Movement"], "2nd-level feature",
           "Supernatural speed without armor.",
           """<p>Your speed increases while unarmored per the Movement column on your progression table.</p>"""),
        _a(cid, cname, ["Multiattack", "Multiattack (2)"], "3rd-level feature",
           "Two attacks per Attack action.", multiattack_body("two")),
        _a(cid, cname, ["Stunning Strike"], "3rd-level feature",
           "Stun foes with ki-infused blows.",
           """<p>Once per turn when you hit with an unarmed strike or monk weapon, spend 1 technique point to force a <strong>Fitness save</strong>. On a failure, the target is stunned until the end of your next turn.</p>"""),
        _a(cid, cname, ["Empowered Strikes"], "4th-level feature",
           "Unarmed strikes count as magical.",
           """<p>Your unarmed strikes count as magical for overcoming resistance and immunity to nonmagical attacks.</p>"""),
        _a(cid, cname, ["Evasion"], "4th-level feature",
           "Dodge area effects.",
           """<p>When you make a Fitness save for half damage from an area effect, you take no damage on a success and half on a failure.</p>"""),
        _a(cid, cname, ["Perfect Motion"], "5th-level feature",
           "Run on walls and fall safely.",
           """<p>Reduce falling damage by 5 × monk level as a reaction. Move along vertical surfaces and liquids without falling during the move.</p>"""),
        _a(cid, cname, ["Astral Teachings"], "7th-level feature",
           "Temporarily master any skill.",
           """<p>Spend 2 technique points to gain proficiency in one language, skill, tool, or weapon until incapacitated or you use this again.</p>"""),
        _a(cid, cname, ["Diamond Soul"], "7th-level feature",
           "Proficiency in all saves; reroll failures.",
           """<p>Proficiency in all saves. When you fail a save, spend 1 technique point to reroll (must take the new result).</p>"""),
        _a(cid, cname, ["Timeless Self"], "8th-level feature",
           "Sustained by inner energy.",
           """<p>Cannot be magically aged; no food or water needed; ability modifiers and Max Wounds cannot be lowered except by <em>wish</em>.</p>"""),
        _a(cid, cname, ["Empty Body"], "9th-level feature",
           "Invisibility and astral travel.",
           """<p>Spend 4 technique points to become invisible for 1 minute with resistance to all damage except force. Or spend 8 points to cast <em>astral projection</em> as an action.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Purity of Body or Mind.",
           """<p>Choose <strong>Purity of Body</strong> (immune to disease/poison) or <strong>Purity of Mind</strong> (advantage on Insight saves; end charm/fear as free action).</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Boundless Technique", "Boundless Technique"], "10th-level feature",
           "Technique points refill when combat begins.",
           """<p>When combat begins, regain up to 4 technique points. If you start a turn with 0 points, regain 2.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a martial talent.",
           improvement_body("martial talents")),
    ]


def _register_paladin():
    cid, cname = "paladin", "Paladin"
    return [
        _a(cid, cname, ["Divine Sense"], "1st-level feature",
           "Detect celestials, fiends, and undead.",
           """<p>On your turn, detect Celestials, Fiends, and Undead within 60 feet (not behind total cover) and consecrated/desecrated sites. Uses = proficiency bonus + 1 per long rest.</p>"""),
        _a(cid, cname, ["Lay on Hands"], "1st-level feature",
           "Pool of healing touch.",
           """<p>Pool = 5 × paladin level, restored on long rest. As an <strong>action</strong>, touch a creature and heal Wounds from the pool. Spend 5 healing to cure one disease or poison.</p>""",
           action="action"),
        _a(cid, cname, ["Divine Smite"], "2nd-level feature",
           "Spend Spell Power for radiant burst on hit.",
           """<p>Once per turn when you hit with a melee weapon attack, spend Spell Power to deal extra <strong>radiant</strong> damage: 2d8 for 1st circle + 1d8 per higher circle (max 5d8). +1d8 vs Fiends and Undead.</p>"""),
        _a(cid, cname, ["Martial Action"], "2nd-level feature",
           "Guard or Wind Up as second action.",
           """<p>Choose <strong>Guard</strong> or <strong>Wind Up</strong>. Use as your second action when you have not moved this turn (see <a href="paladin.html#martial-action">Martial Action</a>).</p>"""),
        _a(cid, cname, ["Spellcasting"], "2nd-level feature",
           "Divine spells known (half caster).",
           spellcasting_body("Paladin", "Divine", "known", "Willpower (WIL)")),
        _a(cid, cname, ["Multiattack", "Multiattack (2)"], "3rd-level feature",
           "Two attacks per Attack action.", multiattack_body("two")),
        _a(cid, cname, ["Aura of Protection"], "4th-level feature",
           "Bolster allies' saves.",
           """<p>When you or a friendly creature within 10 feet makes a save, they add your <strong>Willpower modifier</strong> (minimum +1). You must be conscious.</p>"""),
        _a(cid, cname, ["Aura of Courage"], "5th-level feature",
           "Allies cannot be frightened.",
           """<p>You and friendly creatures within 10 feet cannot be frightened while you are conscious.</p>"""),
        _a(cid, cname, ["Channel Divinity", "Channel Divinity (2/rest)", "Channel Divinity (3/rest)"],
           "6th and 9th level",
           "Oath-specific channel divinity.",
           """<p>Your oath grants Channel Divinity options. Uses: 1/rest until 6th level, then 2/rest, then 3/rest at 9th. Regain on short or long rest.</p>"""),
        _a(cid, cname, ["Cleansing Touch"], "7th-level feature",
           "End spells on yourself or allies.",
           """<p>Action to end one spell on yourself or a willing creature you touch. Uses = Willpower modifier per long rest.</p>"""),
        _a(cid, cname, ["Aura Improvements", "Aura Improvements (30 ft)"], "8th-level feature",
           "Aura range increases to 30 feet.",
           """<p>Aura of Protection, Aura of Courage, and oath auras extend to 30 feet.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Divine Recovery or Radiant Strikes.",
           """<p><strong>Divine Recovery</strong> (Lay on Hands lets target expend a Recovery die) or <strong>Radiant Strikes</strong> (+1d8 radiant on weapon hits, 2d8 vs Fiends/Undead).</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Aura of Salvation", "Aura of Salvation"], "10th-level feature",
           "Calming aura of salvation.",
           """<p>Action: 1-hour aura (30 ft). Allies resist nonmagical damage, auto-succeed death saves, and regain Willpower modifier Wounds at start of turn if they have any Wounds remaining. Once per long rest.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a martial talent.",
           improvement_body("martial talents")),
    ]


def _register_ranger():
    cid, cname = "ranger", "Ranger"
    return [
        _a(cid, cname, ["Explorer"], "1st-level feature",
           "Unmatched wilderness mobility.",
           """<p>Climbing or swimming speed equal to walking speed. Advantage on tracking checks. Speed not halved in difficult terrain (other penalties still apply).</p>"""),
        _a(cid, cname, ["Mystic Mark", "Mystic Mark (d6)", "Mystic Mark (d8)", "Mystic Mark (d10)"],
           "1st level and higher",
           "Mark quarry for extra damage.",
           """<p>When you hit a creature, mark it for 1 minute (extra damage d4 → d6 at 3rd → d8 at 6th → d10 at 9th). Uses = proficiency bonus per long rest.</p>"""),
        _a(cid, cname, ["Martial Action"], "2nd-level feature",
           "Aim or Quick Strike as second action.",
           """<p>Choose <strong>Aim</strong> or <strong>Quick Strike</strong>. Second action when you have not moved (see Martial Action).</p>"""),
        _a(cid, cname, ["Spellcasting"], "2nd-level feature",
           "Primordial spells known.",
           spellcasting_body("Ranger", "Primordial", "known", "Insight (INS)")),
        _a(cid, cname, ["Multiattack", "Multiattack (2)"], "3rd-level feature",
           "Two attacks per Attack action.", multiattack_body("two")),
        _a(cid, cname, ["Empowered Mark"], "4th-level feature",
           "Sense and strike your quarry.",
           """<p>While your mark is within 60 feet, you know its location and it cannot gain advantage from being unseen. No disadvantage from invisibility when attacking it.</p>"""),
        _a(cid, cname, ["Stalker's Step"], "5th-level feature",
           "Vanish in natural cover.",
           """<p>In dim light, darkness, or natural obscurement, use an action to become invisible until your next turn (ends if you attack or cast). Uses = PB per long rest.</p>"""),
        _a(cid, cname, ["Keensense"], "7th-level feature",
           "Hearing-based blindsight.",
           """<p>Keensense 10 feet (does not work while deafened).</p>"""),
        _a(cid, cname, ["Strider"], "8th-level feature",
           "Move without provoking opportunity attacks.",
           """<p>Your movement does not provoke opportunity attacks. Advantage on saves vs grapple, restraint, paralysis, and speed reduction.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Path of the Predator or Sage.",
           """<p><strong>Predator:</strong> Mark your quarry when combat begins without needing to hit first; transfer mark when quarry dies. <strong>Sage:</strong> Learn two extra cantrips and two Primordial rituals.</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Foe Slayer", "Foe Slayer"], "10th-level feature",
           "Wisdom guides every blow against your mark.",
           """<p>Add your Insight modifier to the attack or damage roll of each attack against a mystic-marked creature on your turn.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or martial/technical talent.",
           improvement_body("martial or technical talents")),
    ]


def _register_rogue():
    cid, cname = "rogue", "Rogue"
    return [
        _a(cid, cname, ["Sneak Attack"], "1st-level feature",
           "Extra precision damage once per turn.",
           """<p>Once per turn, deal extra Sneak Attack dice when you hit with a finesse or ranged weapon if you have advantage, or if an ally is within 5 feet of the target. Damage per Sneak Attack column.</p>"""),
        _a(cid, cname, ["Expertise", "Expertise (2)", "Expertise (4)"], "1st and 4th level",
           "Advantage on chosen skill checks.",
           """<p>Choose two proficiencies (four at 4th level) for advantage on related ability checks.</p>"""),
        _a(cid, cname, ["Thieves' Cant"], "1st-level feature",
           "Secret criminal dialect.",
           """<p>You know Thieves' Cant for hidden messages and recognize criminal signs.</p>"""),
        _a(cid, cname, ["Cunning Action", "Cunning Action (free action)"], "2nd-level feature",
           "Dash, Disengage, or Hide as a free action.",
           """<p>On your turn, use a <strong>free action</strong> to Dash, Disengage, or Hide.</p>""",
           action="free action"),
        _a(cid, cname, ["Uncanny Dodge"], "3rd-level feature",
           "Halve damage from one attack.",
           """<p>When an attacker you can see hits you, use your <strong>reaction</strong> to halve the Wounds from that attack.</p>"""),
        _a(cid, cname, ["Evasion"], "4th-level feature",
           "Negate area damage on successful saves.",
           """<p>On successful Fitness saves vs area effects, take no damage; half on failure.</p>"""),
        _a(cid, cname, ["Reliable Talent"], "5th-level feature",
           "Treat low rolls as 10 on proficient checks.",
           """<p>Treat d20 rolls of 9 or lower as 10 on ability checks with skills or tools you are proficient in.</p>"""),
        _a(cid, cname, ["Precise Critical", "Precise Critical (1 die)", "Precise Critical (2 dice)"],
           "6th and 8th level",
           "Critical hits on 19–20 with finesse/ranged.",
           """<p>Critical hit on 19–20 with finesse or ranged weapons. Roll 1 extra weapon die on crit at 6th level, 2 extra at 8th.</p>"""),
        _a(cid, cname, ["Keensense"], "7th-level feature",
           "Hearing-based blindsight 10 feet.",
           """<p>Keensense 10 feet unless deafened.</p>"""),
        _a(cid, cname, ["Elusive"], "9th-level feature",
           "Attackers rarely have advantage against you.",
           """<p>While not incapacitated, attack rolls cannot have advantage against you.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Escape Artist or Jack of All Trades.",
           """<p><strong>Escape Artist:</strong> area saves deal no damage on success. <strong>Jack of All Trades:</strong> pick talents from any list; gain one immediately.</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Stroke of Luck", "Stroke of Luck"], "10th-level feature",
           "Turn failure into success.",
           """<p>Turn a missed attack into a hit, or treat a failed ability check d20 as 20. Once per short or long rest.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a technical talent.",
           improvement_body("technical talents")),
    ]


def _register_sorcerer():
    cid, cname = "sorcerer", "Sorcerer"
    return [
        _a(cid, cname, ["Font of Magic"], "1st-level feature",
           "Internal wellspring of sorcery points.",
           """<p>Sorcery points per progression table. Regain on long rest. Convert points ↔ spell circles per BFRD flexible casting (also use Spell Power in YMIAT).</p>"""),
        _a(cid, cname, ["Spellcasting"], "1st-level feature",
           "Arcane spells known.",
           spellcasting_body("Sorcerer", "Arcane", "known", "Willpower (WIL)")),
        _a(cid, cname, ["Metamagic", "Metamagic (2)", "Metamagic (3)", "Metamagic (4)", "Metamagic (5)"],
           "2nd level and higher",
           "Twist spells with sorcery points.",
           """<p>Choose Metamagic options (Careful, Quickened, Twinned, Heightened, etc.). Gain more options at 4th, 8th, and 10th level. One option per spell unless noted.</p>
<p><strong>Quickened Spell</strong> still costs 2 points; the spell uses your action (not a separate bonus action in YMIAT).</p>"""),
        _a(cid, cname, ["Sorcerous Renewal", "Sorcerous Renewal (2 dice)", "Sorcerous Renewal (3 dice)"],
           "3rd level and higher",
           "Recover sorcery points on short rest.",
           """<p>After a short rest, roll 1d4+1 sorcery points (2d4+1 at 6th, 3d4+1 at 9th).</p>"""),
        _a(cid, cname, ["Devour Spell"], "7th-level feature",
           "Absorb hostile spell energy.",
           """<p>Reaction when targeted by a spell: Willpower check DC 10 + circle. On success, targets have advantage on saves and half damage; you gain sorcery points equal to the circle. Once per long rest (or spend 4 points to reuse).</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Arcane Instruction or Innate Spell.",
           """<p><strong>Arcane Instruction:</strong> spend 1 point to add Willpower to failed check. <strong>Innate Spell:</strong> learn a 1st–2nd circle spell castable with sorcery points.</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Arcane Conjunction", "Arcane Conjunction"], "10th-level feature",
           "Share spell effects with another target.",
           """<p>Reaction when a spell affects you: a creature you see within 120 feet is also affected. Once per rest (or spend 10 sorcery points).</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a magic talent.",
           improvement_body("magic talents")),
    ]


def _register_warlock():
    cid, cname = "warlock", "Warlock"
    return [
        _a(cid, cname, ["Pact Magic"], "1st-level feature",
           "Few slots, short-rest recovery.",
           """<p>Pact spell slots per progression table (all slots are your slot level). Regain on <strong>short or long rest</strong>. Also cast using <a href="../core.html#magic-and-spell-resources">Spell Power</a> per YMIAT rules. Spells known per table.</p>"""),
        _a(cid, cname, ["Eldritch Invocations", "Eldritch Invocations (2)", "Eldritch Invocations (3)",
                        "Eldritch Invocations (4)", "Eldritch Invocations (5)", "Eldritch Invocations (6)"],
           "1st level and higher",
           "Customize your pact with invocations.",
           """<p>Choose invocations from the BFRD Warlock list. Gain more at the levels shown on your progression table. Prerequisites apply.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Warlock heroic boon per BFRD.",
           """<p>Choose a heroic boon from the BFRD Warlock list, adapted for YMIAT.</p>"""),
        _a(cid, cname, ["Epic Boon"], "10th-level feature",
           "Warlock epic boon per BFRD.",
           """<p>Gain your Warlock Epic Boon from BFRD, adapted for YMIAT.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a magic talent.",
           improvement_body("magic talents")),
    ]


def _register_wizard():
    cid, cname = "wizard", "Wizard"
    return [
        _a(cid, cname, ["Arcane Recovery"], "1st-level feature",
           "Recover Spell Power on a short rest.",
           """<p>Once per day on a short rest, recover expended spell circles totaling half your wizard level (rounded up) as Spell Power, or per BFRD slot recovery adapted to SP.</p>"""),
        _a(cid, cname, ["Spellcasting", "Spellbook"], "1st-level feature",
           "Prepared Arcane spells from spellbook.",
           spellcasting_body("Wizard", "Arcane", "spellbook", "Insight (INS)")),
        _a(cid, cname, ["Magic Sense"], "2nd-level feature",
           "Detect magic within 30 feet.",
           """<p>Action: until end of next turn, sense spellcasters, ongoing spell effects, and magic items within 30 feet (blocked by 1 ft stone, 1 in metal, thin lead, 3 ft wood/dirt). Uses = PB + 1 per long rest.</p>"""),
        _a(cid, cname, ["Rote Spell", "Rote Spell (1st)", "Rote Spell (2nd)", "Rote Spell (3rd)", "Rote Spell (4th)"],
           "3rd level and higher",
           "Always-prepared signature spells.",
           """<p>Choose one spell each at 3rd (1st circle), 5th (2nd), 7th (3rd), and 9th (4th) level as always-prepared rote spells. Swap during a long rest.</p>"""),
        _a(cid, cname, ["Superior Recovery"], "4th-level feature",
           "Swap prepared spells during Arcane Recovery.",
           """<p>When you use Arcane Recovery, swap up to half your proficiency bonus (rounded down) prepared spells from your spellbook.</p>"""),
        _a(cid, cname, ["Spellguard"], "7th-level feature",
           "Resist hostile magic.",
           """<p>Advantage on saves against spells; resistance to damage from spells and spell attacks.</p>"""),
        _a(cid, cname, ["Spell Mastery"], "9th-level feature",
           "Cast rote spells without spending slots.",
           """<p>Cast each rote spell once per short rest at lowest circle without spending Spell Power.</p>"""),
        _a(cid, cname, ["Heroic Boon"], "5th-level feature",
           "Rite of the Ritualist or Source Master.",
           """<p><strong>Ritualist:</strong> learn rituals from any magic source. <strong>Source Master:</strong> add spells from Divine, Primordial, or Wyrd when leveling.</p>"""),
        _a(cid, cname, ["Epic Boon", "Epic Boon: Archmage", "Archmage"], "10th-level feature",
           "Chance to recover spent spell power.",
           """<p>When you cast a spell of 1st circle or higher using Spell Power, roll d10. If the result exceeds the circle spent, recover that Spell Power. Once per short rest.</p>"""),
        _a(cid, cname, ["Improvement"], "3rd, 5th, 7th, 9th, and 10th level",
           "Ability increases or a magic talent.",
           improvement_body("magic talents")),
    ]


def build_registry(abilities):
    from ability_utils import normalize_feature_name as norm
    registry = {}
    for a in abilities:
        for name in a["names"]:
            registry[(a["class_id"], norm(name))] = a["anchor"]
            registry[(a["class_id"], name.lower())] = a["anchor"]
    return registry


def normalize_feature_name(name: str) -> str:
    from ability_utils import normalize_feature_name as norm
    return norm(name)


def get_abilities_by_class():
    by_class = {}
    for a in all_abilities():
        by_class.setdefault(a["class_id"], []).append(a)
    return by_class
