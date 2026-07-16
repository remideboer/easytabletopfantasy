#!/usr/bin/env python3
"""ToV Player's Guide 2 subclasses not yet inlined in class_subclasses_data.py."""

from class_subclasses_data import _sf, _sub, _ymiat_level_label

TOV_PG2 = "https://www.talesofthevaliant.com/"

def artificer_pg2_subclasses():
    cid, cname = "artificer", "Artificer"
    return [
        _sub(
            cid, cname, "cog-augur", "Cog Augur",
            "Some mechanists see the universe and its workings as mathematical calculations. They turn their expertise toward crafting baroque devices to help them read these",
            [
                _sf(cid, cname, "cog-augur", "Cog Augur", ["Augment: Clairvoyant"], _ymiat_level_label("3rd"),
                    "Item Requirement: Equipment or Object that Can Fit in One Hand",
                    "<p>Item Requirement: Equipment or Object that Can Fit in One Hand</p>"),
                _sf(cid, cname, "cog-augur", "Cog Augur", ["Auguring Device"], _ymiat_level_label("3rd"),
                    "You learn to transmute a small device into an augury tool ",
                    "<p>You learn to transmute a small device into an augury tool that aids you in calculating and predicting the future. If you spend 1 hour of uninterrupted focus in contact with an object small enough for you to hold in one hand (which can be done as part of a short or long rest), you can transmute that object into an auguring device. The chosen object must be a single object (though that object can have internal moving parts, like a watch or lock) and can\u2019t be a set of tools. The transformation lasts until you choose to end it or until you use this feature to transmute a different object.</p>"),
                _sf(cid, cname, "cog-augur", "Cog Augur", ["Intricate Predictions"], _ymiat_level_label("7th"),
                    "You learn to upgrade your Auguring Device feature, which ",
                    "<p>You learn to upgrade your Auguring Device feature, which gains the following additional properties: \u2022 When you consult the device to learn a detail about a creature, you can now learn two pieces of information from that list. \u2022 When you use the weather prediction aspect of the device, you now have advantage on WIS (Survival) checks to predict the weather within the next 7 days. \u2022 While holding the device, you can spend 10 minutes communing with the device to learn details about current or future events or to learn the direction to a specific creature or object. These effects work like the divination or locate spells, except the device serves as the material component and isn\u2019t consumed by the spell.</p>"),
                _sf(cid, cname, "cog-augur", "Cog Augur", ["Improved Divining"], _ymiat_level_label("11th"),
                    "You learn to adjust your Auguring Device feature\u2019s ",
                    "<p>You learn to adjust your Auguring Device feature\u2019s calculations to reduce its chances of failure. When you use the augury or divination aspects of the device, the chance of receiving a random answer or no answer, respectively, is a cumulative 10 percent instead of 25 percent. If the device is imbued with the Clairvoyant augment, you can choose for one of the targets to have advantage on all its attack rolls instead of only one.</p>"),
                _sf(cid, cname, "cog-augur", "Cog Augur", ["Clarity of Vision"], _ymiat_level_label("15th"),
                    "You can spend 1 minute communing with the device of your",
                    "<p>You can spend 1 minute communing with the device of your</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "grenadier", "Grenadier",
            "Mechanists who pursue the Grenadier\u2019s craft are disciples of entropy, more interested in how things come apart than how they come together. Grenadiers expertly manipulate",
            [
                _sf(cid, cname, "grenadier", "Grenadier", ["Arcane Grenades (1d8, 1/turn)"], _ymiat_level_label("3rd"),
                    "You have learned to construct potent magical devices ",
                    "<p>You have learned to construct potent magical devices called arcane grenades. As an action (counts as the Use an</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "toymaker", "Toymaker",
            "Toymakers are mechanists who revel in creating miniature replicas of animals and humans for their own entertainment, to help with various tasks, and to inflict a",
            [
                _sf(cid, cname, "toymaker", "Toymaker", ["Augment: Messenger"], _ymiat_level_label("3rd"),
                    "You gain the following unique effect for your Augment ",
                    "<p>You gain the following unique effect for your Augment feature. This effect can\u2019t be replaced and doesn\u2019t count against the number of effects that you know, as shown in the Augment Effects Known column of the Mechanist</p>"),
                _sf(cid, cname, "toymaker", "Toymaker", ["Autonomous Toys"], _ymiat_level_label("3rd"),
                    "You design and animate intricate Tiny objects that follow ",
                    "<p>You design and animate intricate Tiny objects that follow your instructions. During a long rest, you can create up to two autonomous toys in the shapes of animals. Each toy is modeled after a Small or smaller Beast (or creature with the</p>"),
                _sf(cid, cname, "toymaker", "Toymaker", ["Automated Power"], _ymiat_level_label("7th"),
                    "The toys from your Autonomous Toys feature gain a bonus ",
                    "<p>The toys from your Autonomous Toys feature gain a bonus to their saves and to their ACs equal to your PB, and when one of your toys is destroyed while within 30 feet of you, you become empowered until the end of your next turn. While empowered, you have advantage on attack rolls and saves.</p>"),
                _sf(cid, cname, "toymaker", "Toymaker", ["Eyes Everywhere"], _ymiat_level_label("11th"),
                    "While you are within 10 feet of at least two of the toys from ",
                    "<p>While you are within 10 feet of at least two of the toys from your Autonomous Toys feature, you have advantage on</p>"),
                _sf(cid, cname, "toymaker", "Toymaker", ["Ultimate Toymaker"], _ymiat_level_label("15th"),
                    "Your maximum number of augmented items (see Augment ",
                    "<p>Your maximum number of augmented items (see Augment feature in Player\u2019s Guide) increases by 3, but these extra augments must be on toys from your Autonomous Toys feature. A toy can have up to two augments on it at one time. As normal, multiple instances of one augment aren\u2019t cumulative on the toy.</p>"),
            ],
            TOV_PG2,
        ),
    ]
def bard_pg2_subclasses():
    cid, cname = "bard", "Bard"
    return [
        _sub(
            cid, cname, "allure", "Allure",
            "Bards who align with the college of Allure understand the power of the mind and how the smallest nudge can bend that power in their favor. These bards are masters of subtle",
            [
                _sf(cid, cname, "allure", "Allure", ["Bardic Performance: Mirror Mirror"], _ymiat_level_label("3rd"),
                    "You weave illusions to protect your companions. When ",
                    "<p>You weave illusions to protect your companions. When you use your Bardic Performance feature (see Player\u2019s</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "mockery", "Mockery",
            "Bards aligned with the college of Mockery have devoted their lives to perfecting their mordant repartee\u2014both to entertain audiences and to use as a devastating weapon",
            [
                _sf(cid, cname, "mockery", "Mockery", ["Bardic Performance: Playful Banter"], _ymiat_level_label("3rd"),
                    "Your jests and banter bolster your allies\u2019 defenses against ",
                    "<p>Your jests and banter bolster your allies\u2019 defenses against similar assaults on the mind. While your performance lasts, each ally within range that takes psychic damage reduces that damage by an amount equal to your bard level + your</p>"),
                _sf(cid, cname, "mockery", "Mockery", ["Razor Wit"], _ymiat_level_label("3rd"),
                    "You learn the vicious mockery cantrip and the hideous laughter ",
                    "<p>You learn the vicious mockery cantrip and the hideous laughter spell if you don\u2019t already know them. When you cast vicious mockery, you add your CHA modifier to the damage roll.</p>"),
                _sf(cid, cname, "mockery", "Mockery", ["Infectious Laughter"], _ymiat_level_label("7th"),
                    "When you cast vicious mockery, you can target a number ",
                    "<p>When you cast vicious mockery, you can target a number of creatures equal to one + half your PB (rounded down).</p>"),
                _sf(cid, cname, "mockery", "Mockery", ["Crushing Jest"], _ymiat_level_label("11th"),
                    "Your insults are so crushing that even creatures with ",
                    "<p>Your insults are so crushing that even creatures with strong mental defenses wilt beneath the verbal assault.</p>"),
                _sf(cid, cname, "mockery", "Mockery", ["Mocking Rage"], _ymiat_level_label("15th"),
                    "Your banter and mockery can enrage creatures. As an ",
                    "<p>Your banter and mockery can enrage creatures. As an action, choose a number of creatures up to your PB that you can see within 30 feet of you. Each target must make a WIS save against your spell save DC or succumb to a fit of rage for 1 minute. While in such a fit, a target is unable to distinguish friend from foe and must attack the nearest creature on its turn. If no other creature is near enough to move to and attack, the target stalks off in a random direction, seeking a target for its rage. A target can repeat the save at the end of each of its turns, ending the effect on itself on a success.</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "sound", "Sound",
            "Bards aligned with the college of Sound are often drawn to it out of a desire to master their musical talents. Those with perfect pitch or who are virtuosos with the lute are",
            [
                _sf(cid, cname, "sound", "Sound", ["Amplify/Dampen"], _ymiat_level_label("3rd"),
                    "You learn the message and thaumaturgy cantrips and the ",
                    "<p>You learn the message and thaumaturgy cantrips and the silence spell if you don\u2019t already know them. These spells count as Arcane spells when you cast them, but they don\u2019t count against the number of cantrips or spells you know as listed in the Bard Progression table (see Player\u2019s Guide).</p>"),
                _sf(cid, cname, "sound", "Sound", ["Bardic Performance: Spell"], _ymiat_level_label("3rd"),
                    "The bard class receives new features and subclasses in this ",
                    "<p>The bard class receives new features and subclasses in this section.</p>"),
            ],
            TOV_PG2,
        ),
    ]
def cleric_pg2_subclasses():
    cid, cname = "cleric", "Cleric"
    return [
        _sub(
            cid, cname, "death", "Death",
            "Gods of the Death domain govern death and the afterlife, exemplifying the inevitability and mystery of the beyond. Devotees of this domain bring peace to the bereaved,",
            [
                _sf(cid, cname, "death", "Death", ["Channel Divinity: Forsee Doom"], _ymiat_level_label("3rd"),
                    "Death Domain Spells, Death\u2019s Sentinel",
                    "<p>Death Domain Spells, Death\u2019s Sentinel 7th</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "nature", "Nature",
            "Gods of the Nature domain protect and govern the overgrown wilds and fertile lands. Dogmatic followers of this domain are entrusted with the safety and prosperity",
            [
                _sf(cid, cname, "nature", "Nature", ["Apostle of Nature"], _ymiat_level_label("3rd"),
                    "You gain proficiency in any two of the following skills or ",
                    "<p>You gain proficiency in any two of the following skills or tools: Animal Handling, Nature, Survival; herbalist tools, land vehicles, or water vehicles.</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "tempest", "Tempest",
            "Gods of the Tempest domain embody the awesome destructive power of storms, earthquakes, wildfires, and similar natural disasters. Clerics of this domain are often as",
            [
                _sf(cid, cname, "tempest", "Tempest", ["Channel Divinity: Storm\u2019s Fury"], _ymiat_level_label("3rd"),
                    "You can use your Channel Divinity feature to invoke the ",
                    "<p>You can use your Channel Divinity feature to invoke the wrath of thunderstorms. When you deal lightning or thunder damage, you can use Storm\u2019s Fury to deal the maximum damage on each of those damage dice instead of rolling them.</p>"),
                _sf(cid, cname, "tempest", "Tempest", ["Tempest"], _ymiat_level_label("3rd"),
                    "You gain domain spells at the cleric levels listed in the",
                    "<p>You gain domain spells at the cleric levels listed in the</p>"),
            ],
            TOV_PG2,
        ),
    ]
def fighter_pg2_subclasses():
    cid, cname = "fighter", "Fighter"
    return [
        _sub(
            cid, cname, "scrapper", "Scrapper",
            "Fighters typically engage with their opponents with manufactured weapons. However, some of them enjoy the physicality of using their bodies as weapons and become",
            [
                _sf(cid, cname, "scrapper", "Scrapper", ["Grappling Superiority"], _ymiat_level_label("3rd"),
                    "You gain proficiency in the Athletics skill. If you are already ",
                    "<p>You gain proficiency in the Athletics skill. If you are already proficient, double your PB instead for checks made with that skill.</p>"),
                _sf(cid, cname, "scrapper", "Scrapper", ["Mighty Fists"], _ymiat_level_label("3rd"),
                    "Your unarmed attacks become more powerful. When ",
                    "<p>Your unarmed attacks become more powerful. When you make an unarmed strike, the damage increases from 1 + your STR modifier to 1d4 + your STR modifier. This further increases to 1d6 at 7th level, 1d8 at 11th level, and 1d10 at 15th level.</p>"),
                _sf(cid, cname, "scrapper", "Scrapper", ["Grappling Maneuvers"], _ymiat_level_label("7th"),
                    "As a bonus action while grappling a creature, you can ",
                    "<p>As a free action while grappling a creature, you can perform one of the following grappling maneuvers. You must make a STR (Athletics) check contested by the grappled creature\u2019s STR (Athletics) or DEX (Acrobatics) check (target\u2019s choice). If you succeed, the target is affected by the maneuver until the grapple ends or until you use a different grappling maneuver on it: \u2022 Chokehold. You choke a breathing or speaking creature, and it can\u2019t speak or cast spells with verbal components. If the target remains in a chokehold for two consecutive turns, it begins suffocating and continues suffocating until the grapple or this maneuver ends. \u2022 Makeshift Shield. You pull the creature between you and danger. You have half cover if the target is your size or smaller and three-quarters cover if it is larger than you. \u2022 Pin. You pin, hold, or otherwise immobilize the creature. The target is restrained.</p>"),
                _sf(cid, cname, "scrapper", "Scrapper", ["Expert Grappler"], _ymiat_level_label("11th"),
                    "You are an expert at holding onto and locking down foes.",
                    "<p>You are an expert at holding onto and locking down foes.</p>"),
                _sf(cid, cname, "scrapper", "Scrapper", ["Knockout Punch"], _ymiat_level_label("15th"),
                    "When you hit a creature with two unarmed strikes in ",
                    "<p>When you hit a creature with two unarmed strikes in the same turn (and it has less than half of its Wound maximum) or when you score a critical hit with an unarmed strike, the target must succeed on a CON save (DC 8 + your PB + your STR modifier) or be stunned for 1 minute. The target can repeat the save at the end of each of its turns, ending the effect on itself on a success.</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "stunt-archer", "Stunt Archer",
            "Some fighters eschew melee weapons completely, choosing the greater range afforded by bows and crossbows. They become so comfortable with these weapons that they can",
            [
                _sf(cid, cname, "stunt-archer", "Stunt Archer", ["Bow Mastery"], _ymiat_level_label("3rd"),
                    "You have focused your training on ranged weapons, ",
                    "<p>You have focused your training on ranged weapons, specifically bows and crossbows, and gain several bonuses when wielding them. When you make an attack roll with one, you don\u2019t have disadvantage from being within 5 feet of a hostile creature, though you can still have disadvantage from other sources.</p>"),
                _sf(cid, cname, "stunt-archer", "Stunt Archer", ["Stunt Shots"], _ymiat_level_label("3rd"),
                    "You have developed such familiarity with bows and ",
                    "<p>You have developed such familiarity with bows and crossbows that you can use them to make shots considered improbable by others. You gain access to special maneuvers called stunt shots. 1 CLASS OPTIONS 29</p>"),
                _sf(cid, cname, "stunt-archer", "Stunt Archer", ["Keen Eye"], _ymiat_level_label("7th"),
                    "You increase the normal range for any bow or crossbow ",
                    "<p>You increase the normal range for any bow or crossbow you wield: \u2022 If the normal range is less than 50 feet, it increases by 10 feet. \u2022 If the normal range is between 50 and 100 feet, it increases by 20 feet. \u2022 If the normal range is greater than 100 feet, it increases by 30 feet.</p>"),
                _sf(cid, cname, "stunt-archer", "Stunt Archer", ["Advanced Stunt Shots"], _ymiat_level_label("11th"),
                    "The following powerful stunt shots are available to you ",
                    "<p>The following powerful stunt shots are available to you whenever you could use a stunt shot. Some advanced stunt shots require you to be wielding a specific type of bow or crossbow to use them.</p>"),
                _sf(cid, cname, "stunt-archer", "Stunt Archer", ["Absolute Mastery"], _ymiat_level_label("15th"),
                    "You treat all bows and crossbows as if they had the",
                    "<p>You treat all bows and crossbows as if they had the</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "twinblade", "Twinblade",
            "Fighters that choose the Twinblade discipline are master dual-wielders, forgoing cumbersome armaments to become a whirling death that moves through battles with",
            [
                _sf(cid, cname, "twinblade", "Twinblade", ["Blade Dance"], _ymiat_level_label("3rd"),
                    "As a bonus action, you can begin a blade dance as long ",
                    "<p>As a free action, you can begin a blade dance as long as you are neither grappled or restrained nor your speed is otherwise reduced to 0. While engaged in a blade dance, you gain the following benefits if you are wielding a melee weapon in each hand and aren\u2019t wearing medium or heavy armor: \u2022 You have advantage on DEX saves and DEX ability checks made to avoid being grappled or restrained or having your movement speed reduced. If you become grappled or restrained, you have advantage on checks made to escape or end the effect as long as your blade dance is active. \u2022 Your movement doesn\u2019t provoke opportunity attacks. \u2022 Your speed increases by 10 feet.</p>"),
                _sf(cid, cname, "twinblade", "Twinblade", ["Deadly Grace"], _ymiat_level_label("3rd"),
                    "You gain proficiency in either the Acrobatics or Performance ",
                    "<p>You gain proficiency in either the Acrobatics or Performance skill. If you are already proficient in one or both of these skills, double your PB for checks made with that skill.</p>"),
                _sf(cid, cname, "twinblade", "Twinblade", ["Double Edged"], _ymiat_level_label("7th"),
                    "When you take the Attack action on your turn and then use ",
                    "<p>When you take the Attack action on your turn and then use a free action to make one or more additional attacks (such as for two-weapon fighting and the Quick Strike martial action), you can add your DEX modifier to the damage dealt by the bonus attacks. If you have at least one use remaining of your Blade Dance feature, you can activate it as part of the same free action you used to make these attacks.</p>"),
                _sf(cid, cname, "twinblade", "Twinblade", ["One Thousand Cuts"], _ymiat_level_label("11th"),
                    "When you take the Attack action on your turn while your ",
                    "<p>When you take the Attack action on your turn while your blade dance is active, you can forgo the normal number of attacks granted by your Multiattack to instead make one melee weapon attack that targets each creature within 5 feet of you, using a single attack roll and damage roll.</p>"),
                _sf(cid, cname, "twinblade", "Twinblade", ["Moving Target"], _ymiat_level_label("15th"),
                    "As long as you aren\u2019t incapacitated, you can\u2019t be grappled or ",
                    "<p>As long as you aren\u2019t incapacitated, you can\u2019t be grappled or restrained, and your speed can\u2019t be reduced by any means.</p>"),
            ],
            TOV_PG2,
        ),
    ]
def monk_pg2_subclasses():
    cid, cname = "monk", "Monk"
    return [
        _sub(
            cid, cname, "affliction-eater", "Affliction Eater",
            "Some monks realize the careful balance between life and death, and they\u2019ve honed their bodies and minds to ensure the balance tips in their favor. However, they",
            [
                _sf(cid, cname, "affliction-eater", "Affliction Eater", ["Absorb Affliction"], _ymiat_level_label("3rd"),
                    "As a bonus action, you can touch a creature within 5 feet of ",
                    "<p>As a free action, you can touch a creature within 5 feet of you and heal it at a cost to you. The target regains a number of Wounds up to your CON modifier + your monk level or loses a condition affecting it. In exchange, you take damage equal to the Wounds the target regained, or you gain the condition you removed from the target. If the condition allowed a save and has a duration of 1 minute or less, you can make that save at the end of each of your turns, ending the effect on yourself on a success, even if the effect allowed no repeat saves. If the condition has a longer duration, you can make the save every hour.</p>"),
                _sf(cid, cname, "affliction-eater", "Affliction Eater", ["Stay Execution"], _ymiat_level_label("3rd"),
                    "When a creature within 30 feet of you is reduced to 0 HP, ",
                    "<p>When a creature within 30 feet of you is reduced to 0 HP, you can spend 2 technique points to stay its death. The target is unconscious but stable, or you can choose for it to regain Wounds equal to one roll of your martial arts die + your WIS modifier and become conscious. If the target was hostile toward you before it was reduced to 0 HP, you have advantage on CHA checks to interact with it for the next 24 hours, as it understands you spared its life.</p>"),
                _sf(cid, cname, "affliction-eater", "Affliction Eater", ["Intercedence"], _ymiat_level_label("7th"),
                    "You grant good fortune to your ally at the cost of your own.",
                    "<p>You grant good fortune to your ally at the cost of your own.</p>"),
                _sf(cid, cname, "affliction-eater", "Affliction Eater", ["Shield from Harm"], _ymiat_level_label("11th"),
                    "You link yourself to another creature, reducing harm to ",
                    "<p>You link yourself to another creature, reducing harm to it as you channel some of its wounds to yourself. As an action, you can spend 3 technique points to cast the warding bond spell on a friendly creature, without requiring a material component.</p>"),
                _sf(cid, cname, "affliction-eater", "Affliction Eater", ["Merciful Burst"], _ymiat_level_label("15th"),
                    "As a bonus action, you can reduce your current hit points ",
                    "<p>As a free action, you can reduce your current Wounds by 40, reducing your Max Wounds by the same amount, to release a burst of healing energy in a 60-foot radius centered on you. If you spend 11 technique points when activating this feature, you don\u2019t reduce your hit points or Max Wounds. Each creature you choose within the area regains a number of Wounds equal to your</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "elemental-voice", "Elemental Voice",
            "Monks that pursue the way of the Elemental Voice seek to reshape the primordial world around them with their will. These monks often share similarities in manner or dress",
            [
                _sf(cid, cname, "elemental-voice", "Elemental Voice", ["Elemental Voice Feature"], _ymiat_level_label("3rd"),
                    "Elemental Voice subclass feature from ToV Player's Guide 2.",
                    "<p>Elemental Voice subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "elemental-voice", "Elemental Voice", ["Elemental Voice Feature"], _ymiat_level_label("7th"),
                    "Elemental Voice subclass feature from ToV Player's Guide 2.",
                    "<p>Elemental Voice subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "elemental-voice", "Elemental Voice", ["Elemental Voice Feature"], _ymiat_level_label("11th"),
                    "Elemental Voice subclass feature from ToV Player's Guide 2.",
                    "<p>Elemental Voice subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "elemental-voice", "Elemental Voice", ["Elemental Voice Feature"], _ymiat_level_label("15th"),
                    "Elemental Voice subclass feature from ToV Player's Guide 2.",
                    "<p>Elemental Voice subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "seal-guardian", "Seal Guardian",
            "Seal Guardian monks apply the knowledge they gain from transcribing written works to the creation of magical seals, which they can offer to others for protection or to drive out",
            [
                _sf(cid, cname, "seal-guardian", "Seal Guardian", ["Seal Guardian Feature"], _ymiat_level_label("3rd"),
                    "Seal Guardian subclass feature from ToV Player's Guide 2.",
                    "<p>Seal Guardian subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "seal-guardian", "Seal Guardian", ["Seal Guardian Feature"], _ymiat_level_label("7th"),
                    "Seal Guardian subclass feature from ToV Player's Guide 2.",
                    "<p>Seal Guardian subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "seal-guardian", "Seal Guardian", ["Seal Guardian Feature"], _ymiat_level_label("11th"),
                    "Seal Guardian subclass feature from ToV Player's Guide 2.",
                    "<p>Seal Guardian subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "seal-guardian", "Seal Guardian", ["Seal Guardian Feature"], _ymiat_level_label("15th"),
                    "Seal Guardian subclass feature from ToV Player's Guide 2.",
                    "<p>Seal Guardian subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
            ],
            TOV_PG2,
        ),
    ]
def paladin_pg2_subclasses():
    cid, cname = "paladin", "Paladin"
    return [
        _sub(
            cid, cname, "anathema", "Anathema",
            "Paladins wishing to end immediate threats posed by evil creatures and who don\u2019t mind the stains of close dealings with such creatures swear an oath of Anathema. These",
            [
                _sf(cid, cname, "anathema", "Anathema", ["Anathema Oath Spells"], _ymiat_level_label("3rd"),
                    "You gain oath spells at the paladin levels listed in the",
                    "<p>You gain oath spells at the paladin levels listed in the</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "safekeeping", "Safekeeping",
            "Swearing an oath of Safekeeping binds a paladin to a person, place, or object, which they steadfastly guard. These paladins might change the subjects of their protection, but",
            [
                _sf(cid, cname, "safekeeping", "Safekeeping", ["Channel Divinity: Divine Blockade"], _ymiat_level_label("3rd"),
                    "As a bonus action, you can ward an object or space, no ",
                    "<p>As a free action, you can ward an object or space, no larger than 5 feet on a side, from a single target creature you can see within 30 feet. For 1 minute, the target\u2019s speed is halved when trying to move toward the object or space.</p>"),
                _sf(cid, cname, "safekeeping", "Safekeeping", ["Channel"], _ymiat_level_label("3rd"),
                    "Death Domain Spells, Death\u2019s Sentinel",
                    "<p>Death Domain Spells, Death\u2019s Sentinel 7th</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "unbound", "Unbound",
            "Paladins who have witnessed duplicity in their leaders or that feel taken advantage of often swear an oath of the Unbound. They saw their leaders\u2019 corruption and blas\u00e9",
            [
                _sf(cid, cname, "unbound", "Unbound", ["Channel Divinity: Forceful Unyoking"], _ymiat_level_label("3rd"),
                    "As an action, you can present your holy symbol and utter ",
                    "<p>As an action, you can present your holy symbol and utter a rebuke in a 30-foot cone. Each creature in the area that is charmed, grappled, or restrained by another creature is immediately freed and has advantage on checks and saves against these conditions for 1 minute. Each creature within 30 feet of you that caused a creature in the cone to suffer one of the removed conditions takes psychic damage equal to twice your CHA modifier (minimum of 1).</p>"),
            ],
            TOV_PG2,
        ),
    ]
def ranger_pg2_subclasses():
    cid, cname = "ranger", "Ranger"
    return [
        _sub(
            cid, cname, "arrow-binder", "Arrow Binder",
            "Arrow binders are rangers who have melded their mastery of the wilds with their mastery of the bow. They channel primordial magic into their ammunition, unleashing spell",
            [
                _sf(cid, cname, "arrow-binder", "Arrow Binder", ["Arrow Binder Calling Spells"], _ymiat_level_label("3rd"),
                    "You gain calling spells at the ranger levels listed in the",
                    "<p>You gain calling spells at the ranger levels listed in the</p>"),
                _sf(cid, cname, "arrow-binder", "Arrow Binder", ["Bind Spell"], _ymiat_level_label("3rd"),
                    "As an action, you can expend a spell slot to cast a",
                    "<p>As an action, you can expend a spell level to cast a</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "shadow", "Shadow",
            "The Shadow\u2019s calling is a rare one, often drawing in rangers who have lost much to the world\u2019s monsters. Such rangers draw on the gloom of night and the dark of sunless caves",
            [
                _sf(cid, cname, "shadow", "Shadow", ["Night\u2019s Gaze"], _ymiat_level_label("3rd"),
                    "Your attunement to the dark corners of the world sharpens ",
                    "<p>Your attunement to the dark corners of the world sharpens your senses. You gain darkvision to a range of 60 feet, if you don\u2019t already have it, and can see in magical darkness as if it was normal darkness. You have advantage on DEX (Stealth) checks made while in magical darkness.</p>"),
                _sf(cid, cname, "shadow", "Shadow", ["Predator\u2019s Strike"], _ymiat_level_label("3rd"),
                    "You have advantage on attack rolls against surprised ",
                    "<p>You have advantage on attack rolls against surprised creatures. Once on your turn, when you make a weapon attack that hits a creature that can\u2019t see you or that has no allies within 5 feet of it, you deal extra damage to the creature. The extra damage is equal to the amount your</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "trailblazer", "Trailblazer",
            "Trailblazers lead expeditions into the unknown and guard travelers through the most dangerous wilds. They are unparalleled experts of the natural world, navigating",
            [
                _sf(cid, cname, "trailblazer", "Trailblazer", ["Expert Guide"], _ymiat_level_label("3rd"),
                    "You gain proficiency in the Nature and Survival skills. If ",
                    "<p>You gain proficiency in the Nature and Survival skills. If you are already proficient in one or both of these skills, double your PB instead for checks made with that skill.</p>"),
                _sf(cid, cname, "trailblazer", "Trailblazer", ["Focus Fire"], _ymiat_level_label("3rd"),
                    "When you mark a creature with your Mystic Mark feature ",
                    "<p>When you mark a creature with your Mystic Mark feature (see Player\u2019s Guide), you can share some of its power with an ally. Choose one friendly creature within 30 feet that can see or hear you. While the mark lasts, the chosen ally deals extra damage of their weapon\u2019s type equal to your Mystic</p>"),
                _sf(cid, cname, "trailblazer", "Trailblazer", ["Trailblazer"], _ymiat_level_label("3rd"),
                    "You gain calling spells at the ranger levels listed in the",
                    "<p>You gain calling spells at the ranger levels listed in the</p>"),
            ],
            TOV_PG2,
        ),
    ]
def rogue_pg2_subclasses():
    cid, cname = "rogue", "Rogue"
    return [
        _sub(
            cid, cname, "con-arcanist", "Con Arcanist",
            "You add magic to your bag of tricks to confound your foes or relieve others of their possessions. Your spellcasting allows you to perform more dangerous stunts from a distance.",
            [
                _sf(cid, cname, "con-arcanist", "Con Arcanist", ["Con Arcanist Feature"], _ymiat_level_label("3rd"),
                    "Con Arcanist subclass feature from ToV Player's Guide 2.",
                    "<p>Con Arcanist subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "con-arcanist", "Con Arcanist", ["Con Arcanist Feature"], _ymiat_level_label("7th"),
                    "Con Arcanist subclass feature from ToV Player's Guide 2.",
                    "<p>Con Arcanist subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "con-arcanist", "Con Arcanist", ["Con Arcanist Feature"], _ymiat_level_label("11th"),
                    "Con Arcanist subclass feature from ToV Player's Guide 2.",
                    "<p>Con Arcanist subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
                _sf(cid, cname, "con-arcanist", "Con Arcanist", ["Con Arcanist Feature"], _ymiat_level_label("15th"),
                    "Con Arcanist subclass feature from ToV Player's Guide 2.",
                    "<p>Con Arcanist subclass features from Tales of the Valiant Player's Guide 2. Apply using YMIAT terminology (Wounds, Fitness/Insight/Willpower, spell levels).</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "nightblade", "Nightblade",
            "Instead of relying on physical weapons, you draw from your inner resolve to manifest soul-bound knives. As you progress in power, you can use these knives to impose your",
            [
                _sf(cid, cname, "nightblade", "Nightblade", ["Psychic Blade"], _ymiat_level_label("3rd"),
                    "You manifest a portion of your soul into psychic blades.",
                    "<p>You manifest a portion of your soul into psychic blades.</p>"),
                _sf(cid, cname, "nightblade", "Nightblade", ["Psychic Bulwark"], _ymiat_level_label("3rd"),
                    "You have spent time honing the power of your mind. You ",
                    "<p>You have spent time honing the power of your mind. You are resistant to psychic damage.</p>"),
                _sf(cid, cname, "nightblade", "Nightblade", ["Enhanced Blades (+1)"], _ymiat_level_label("7th"),
                    "Your psychic blade becomes magical, and you gain a +1 ",
                    "<p>Your psychic blade becomes magical, and you gain a +1 bonus to attack and damage rolls with it.</p>"),
                _sf(cid, cname, "nightblade", "Nightblade", ["Home In"], _ymiat_level_label("11th"),
                    "Your psychic blades now act as beacons. The range of your",
                    "<p>Your psychic blades now act as beacons. The range of your</p>"),
                _sf(cid, cname, "nightblade", "Nightblade", ["Enhanced Blades (+2, spiritual weapon)"], _ymiat_level_label("15th"),
                    "Your psychic blade becomes magical, and you gain a +1 ",
                    "<p>Your psychic blade becomes magical, and you gain a +1 bonus to attack and damage rolls with it.</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "trapsmith", "Trapsmith",
            "Some rogues focus all their attention on understanding traps. This fixation makes them better at avoiding dangers and keeping their companions safe. Trapsmith rogues also",
            [
                _sf(cid, cname, "trapsmith", "Trapsmith", ["Makeshift Trap"], _ymiat_level_label("3rd"),
                    "You can spend 1 minute crafting a simple, makeshift trap, ",
                    "<p>You can spend 1 minute crafting a simple, makeshift trap, using the materials at hand. The trap is a Small or smaller object with an AC of 10 + your PB and Wounds equal to twice your rogue level. You can place the trap as an action,</p>"),
                _sf(cid, cname, "trapsmith", "Trapsmith", ["Trap Expertise"], _ymiat_level_label("3rd"),
                    "You have advantage on checks to find or notice traps, ",
                    "<p>You have advantage on checks to find or notice traps, checks to determine how traps work, and checks to disarm or disable traps with thieves\u2019 tools. If you don\u2019t have thieves\u2019 tools, you can attempt to disarm or disable a trap with the materials at hand, but you have disadvantage on the check.</p>"),
                _sf(cid, cname, "trapsmith", "Trapsmith", ["Rework Trap"], _ymiat_level_label("7th"),
                    "When you disarm a trap you didn\u2019t make or set, you can ",
                    "<p>When you disarm a trap you didn\u2019t make or set, you can leave the trap untriggered and change the DC to disable it to your trap save DC. You can also add effects from the</p>"),
                _sf(cid, cname, "trapsmith", "Trapsmith", ["Improved Traps"], _ymiat_level_label("11th"),
                    "You can now create a trap as an action and set it as a bonus ",
                    "<p>You can now create a trap as an action and set it as a bonus action. When you set a trap you created, it can now be in any unoccupied space you can see within 30 feet of you, and the distance at which you can remotely trigger a trap with the Rework Trap feature increases to 60 feet.</p>"),
                _sf(cid, cname, "trapsmith", "Trapsmith", ["Trap Mastery"], _ymiat_level_label("15th"),
                    "When you fail to disarm a trap that automatically triggers ",
                    "<p>When you fail to disarm a trap that automatically triggers when a disarm attempt fails, the trap doesn\u2019t trigger, and you can try to disarm the trap again. If you fail a second time, the trap triggers.</p>"),
            ],
            TOV_PG2,
        ),
    ]
def sorcerer_pg2_subclasses():
    cid, cname = "sorcerer", "Sorcerer"
    return [
        _sub(
            cid, cname, "abominable", "Abominable",
            "You receive your magic from the primordial beings who existed before the creation of reality and that remain uncaring about its existence or their horrific",
            [
                _sf(cid, cname, "abominable", "Abominable", ["Abominable Origin Spells"], _ymiat_level_label("3rd"),
                    "You gain origin spells at the sorcerer levels listed in ",
                    "<p>You gain origin spells at the sorcerer levels listed in the Abominable Origin Spells table. See the Sorcerer</p>"),
                _sf(cid, cname, "abominable", "Abominable", ["Physical"], _ymiat_level_label("3rd"),
                    "Your body undergoes subtle transformations as you ",
                    "<p>Your body undergoes subtle transformations as you embrace your otherworldly origin. Vital organs shift or merge without any negative impact to you, but they make it more difficult for others to inflict grievous harm to you.</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "cyclonic", "Cyclonic",
            "The power of the storm thunders within you. The magic that courses through you is as inescapable as a blizzard, as undeniable as a hurricane. Highly prized as sailors",
            [
                _sf(cid, cname, "cyclonic", "Cyclonic", ["Cyclonic Origin Spells"], _ymiat_level_label("3rd"),
                    "You gain origin spells at the sorcerer levels listed in the",
                    "<p>You gain origin spells at the sorcerer levels listed in the</p>"),
                _sf(cid, cname, "cyclonic", "Cyclonic", ["Stormborn"], _ymiat_level_label("3rd"),
                    "The storm magic within you is tied forever to the elemental ",
                    "<p>The storm magic within you is tied forever to the elemental planes. You gain the following benefits: \u2022 While you are outdoors on the Material Plane or the</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "sacred", "Sacred",
            "Your magical power derives from a deity. An avatar or a powerful celestial or fiendish proxy might feature in your distant ancestry, or you might be linked to a major",
            [
                _sf(cid, cname, "sacred", "Sacred", ["Divine Providence"], _ymiat_level_label("3rd"),
                    "Your divine nature grants you a minor amount of grace.",
                    "<p>Your divine nature grants you a minor amount of grace.</p>"),
                _sf(cid, cname, "sacred", "Sacred", ["Metamagic: Divine"], _ymiat_level_label("3rd"),
                    "You gain the following unique option for your Metamagic ",
                    "<p>You gain the following unique option for your Metamagic feature (see Player\u2019s Guide). This option can\u2019t be replaced and doesn\u2019t count against the number of Metamagic options that you know.</p>"),
            ],
            TOV_PG2,
        ),
    ]
def warlock_pg2_subclasses():
    cid, cname = "warlock", "Warlock"
    return [
        _sub(
            cid, cname, "archon", "Archon",
            "Your patron is an otherworldly being bound to the forces of law and order. Archon patrons relentlessly pursue whichever cosmic plan guides their path, eliminating anything that",
            [
                _sf(cid, cname, "archon", "Archon", ["Archon Pact Spells"], _ymiat_level_label("3rd"),
                    "You gain pact spells at the warlock levels listed in the",
                    "<p>You gain pact spells at the warlock levels listed in the</p>"),
                _sf(cid, cname, "archon", "Archon", ["Equalize"], _ymiat_level_label("3rd"),
                    "As a reaction when you or a creature you can see would ",
                    "<p>As a reaction when you or a creature you can see would make an ability check, attack roll, or save with advantage or disadvantage, you can cancel out all sources of advantage or disadvantage, forcing the creature to roll a single d20 to determine the outcome. Once you use this feature to modify a check, that check can\u2019t be modified by any sources of advantage or disadvantage or by spending any amount of Luck.</p>"),
                _sf(cid, cname, "archon", "Archon", ["Restore Efficiency"], _ymiat_level_label("7th"),
                    "As a bonus action, you can expend a Wyrd spell slot of ",
                    "<p>As a free action, you can expend a Wyrd spell level of 1st level or higher to end one condition or magical effect that affects you or a creature you touch. If the effect is the product of a spell equal to or less than the level expended, it automatically ends. For effects created by spells of a higher level than expended, make a</p>"),
                _sf(cid, cname, "archon", "Archon", ["Entropic Dispersal"], _ymiat_level_label("11th"),
                    "As a reaction when you take damage, you can disperse ",
                    "<p>As a reaction when you take damage, you can disperse some of that damage into a nearby creature. The damage you take is reduced by an amount up to your warlock level, and one creature you can see within 5 feet of you instead takes that amount of damage. If the target is unwilling, it can make a CON save against your spell save DC. On a success or if the target is immune to that type of damage, the target doesn\u2019t take the damage, and the damage you take isn\u2019t reduced.</p>"),
                _sf(cid, cname, "archon", "Archon", ["Invoke Order"], _ymiat_level_label("15th"),
                    "You can call upon your patron to correct imbalances that ",
                    "<p>You can call upon your patron to correct imbalances that threaten fulfilment of the cosmic plan. As an action, you can expend a use of your Pact Magic feature (see Player\u2019s</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "elemental-regent", "Elemental Regent",
            "Your patron is an elemental entity with dominion over a sizeable territory within its elemental plane. You are one of its elemental representatives on the Material Plane, and",
            [
                _sf(cid, cname, "elemental-regent", "Elemental Regent", ["Elemental Blast"], _ymiat_level_label("3rd"),
                    "Whenever you use your Eldritch Blast feature (see Player\u2019s",
                    "<p>Whenever you use your Eldritch Blast feature (see Player\u2019s</p>"),
                _sf(cid, cname, "elemental-regent", "Elemental Regent", ["Elemental Regent Pact"], _ymiat_level_label("3rd"),
                    "You gain pact spells at the warlock levels listed in the",
                    "<p>You gain pact spells at the warlock levels listed in the</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "fey-noble", "Fey Noble",
            "Your patron is an immortal fey, one whose existence predates the advent of mortals. The patron\u2019s intentions remain unknown to you, or it might deceive you about",
            [
                _sf(cid, cname, "fey-noble", "Fey Noble", ["Fey Noble Pact Spells"], _ymiat_level_label("3rd"),
                    "You gain pact spells at the warlock levels listed in the Fey",
                    "<p>You gain pact spells at the warlock levels listed in the Fey</p>"),
                _sf(cid, cname, "fey-noble", "Fey Noble", ["Fey Presence"], _ymiat_level_label("3rd"),
                    "Your patron\u2019s power inures you to fey trickery and allows ",
                    "<p>Your patron\u2019s power inures you to fey trickery and allows you to use some of it yourself. You are resistant to the charmed and unconscious conditions, and you have advantage on ability checks and saves to discern the truth of an illusion.</p>"),
                _sf(cid, cname, "fey-noble", "Fey Noble", ["Death Ruse"], _ymiat_level_label("7th"),
                    "As a reaction when you take damage, you can fall prone ",
                    "<p>As a reaction when you take damage, you can fall prone and appear to have been reduced to 0 HP. Make a CHA (Deception) check. This becomes the DC for creatures making WIS (Insight or Medicine) checks to determine if you\u2019re actually dead. If you attack a creature that hasn\u2019t successfully determined that you aren\u2019t dead or unconscious, you have advantage on your attack roll, and if you target such a creature with a spell, it has disadvantage on the save. Once you have gained this benefit against a creature or once a creature has seen through your ruse, that creature can\u2019t be affected by this feature again for 1 hour.</p>"),
                _sf(cid, cname, "fey-noble", "Fey Noble", ["Emotional Redirection"], _ymiat_level_label("11th"),
                    "The emotional frivolity of the fey has steeled you against ",
                    "<p>The emotional frivolity of the fey has steeled you against attempts at manipulating your emotions and made you better at influencing the emotions of others. You are immune to the charmed and frightened conditions, and you can use your Fey Presence feature a number of times equal to your PB, regaining all expended uses when you finish a short or long rest.</p>"),
                _sf(cid, cname, "fey-noble", "Fey Noble", ["Induce Fugue State"], _ymiat_level_label("15th"),
                    "As an action, you can create an illusory scenario that ",
                    "<p>As an action, you can create an illusory scenario that draws creatures into it. Choose a number of targets equal to your PB within 60 feet of you that you can see. Each target must make a WIS save against your spell save</p>"),
            ],
            TOV_PG2,
        ),
    ]
def wizard_pg2_subclasses():
    cid, cname = "wizard", "Wizard"
    return [
        _sub(
            cid, cname, "arcanist", "Arcanist",
            "Among wizards, who might mollify their curiosity with any manner of research, the Arcanist is often considered the most preoccupied with the empirical and esoteric",
            [
                _sf(cid, cname, "arcanist", "Arcanist", ["Economical Transcription"], _ymiat_level_label("3rd"),
                    "Your ability to collect, decipher, and recall spells is ",
                    "<p>Your ability to collect, decipher, and recall spells is unmatched. When you finish a short or long rest, you can replace one Arcane cantrip that you know with another cantrip from the Arcane source spell list.</p>"),
                _sf(cid, cname, "arcanist", "Arcanist", ["Swift Ritual"], _ymiat_level_label("3rd"),
                    "As an action, you can cast an Arcane ritual that you have ",
                    "<p>As an action, you can cast an Arcane ritual that you have scribed within your spellbook, instead of requiring the ritual\u2019s normal casting time. To do so, the ritual can\u2019t be an evocation spell, and it can\u2019t have a casting time greater than 10 minutes. You must still provide all components necessary for the casting of the spell. Once used, you can\u2019t use this feature again until you finish a long rest. 1 CLASS OPTIONS 99</p>"),
                _sf(cid, cname, "arcanist", "Arcanist", ["Arcane Conflux"], _ymiat_level_label("7th"),
                    "Each time you miss a spell attack roll and for each creature ",
                    "<p>Each time you miss a spell attack roll and for each creature that succeeds on a save against a spell you cast, you gain a cumulative +1 bonus to spell attack rolls and your spell save</p>"),
                _sf(cid, cname, "arcanist", "Arcanist", ["Eidetic Scribe"], _ymiat_level_label("11th"),
                    "As a reaction when a creature that you can see and hear ",
                    "<p>As a reaction when a creature that you can see and hear casts a spell from the Arcane source list, you can attempt to memorize it. Make an INT (Arcana) check with a DC of 10 + the spell\u2019s level. On a success, you can cast that spell as though you have it prepared until you finish a short or long rest.</p>"),
                _sf(cid, cname, "arcanist", "Arcanist", ["Mastered Spell"], _ymiat_level_label("15th"),
                    "As part of a long rest, you can select one non\u2011ritual ",
                    "<p>As part of a long rest, you can select one non\u2011ritual spell of 3rd level or lower that you have scribed within your spellbook and master it. That spell is always prepared for you and doesn\u2019t count against the number of spells you can prepare. You can cast that spell at its lowest level without expending Spell Power, though you must still supply any spell components.</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "necromancer", "Necromancer",
            "Some wizards are naturally drawn to necromancy, and others are turned to it by trauma\u2014learning the incredible power of using the dead to do their bidding as they attempt",
            [
                _sf(cid, cname, "necromancer", "Necromancer", ["Reanimation Rites"], _ymiat_level_label("3rd"),
                    "Your study of death and the Undead has made you adept at ",
                    "<p>Your study of death and the Undead has made you adept at using necromantic magic. You can add any spell from the necromancy school to your spellbook, regardless of its spell source. These spells count as Arcane spells for you.</p>"),
                _sf(cid, cname, "necromancer", "Necromancer", ["Undead Thrall"], _ymiat_level_label("3rd"),
                    "You can spend 1 minute touching a pile of bones or the ",
                    "<p>You can spend 1 minute touching a pile of bones or the corpse of a Medium or Small Beast or Humanoid (or</p>"),
                _sf(cid, cname, "necromancer", "Necromancer", ["Enhanced Undead"], _ymiat_level_label("7th"),
                    "You can cast the animate dead ritual spell as an action instead ",
                    "<p>You can cast the animate dead ritual spell as an action instead of its normal casting time, and you can ignore the material spell component when you do so. You can use this feature a number of times equal to your PB, and you regain all expended uses when you finish a long rest.</p>"),
                _sf(cid, cname, "necromancer", "Necromancer", ["Necromantic Reversal"], _ymiat_level_label("11th"),
                    "Necromantic Reversal \u2014 Necromancer subclass feature.",
                    "<p>Necromantic Reversal: see Tales of the Valiant Player's Guide 2 (Necromancer subclass).</p>"),
                _sf(cid, cname, "necromancer", "Necromancer", ["Monstrous Creations"], _ymiat_level_label("15th"),
                    "When you cast the animate dead ritual spell, you can now ",
                    "<p>When you cast the animate dead ritual spell, you can now target Medium or Small Beasts and Humanoids (and</p>"),
            ],
            TOV_PG2,
        ),
        _sub(
            cid, cname, "summoner", "Summoner",
            "Every good adventurer knows that surrounding yourself with quality companions is a must. Summoners know that quantity is just as important. Why put yourself in jeopardy",
            [
                _sf(cid, cname, "summoner", "Summoner", ["Conjuration Specialist"], _ymiat_level_label("3rd"),
                    "You are adept at using magic that creates or summons ",
                    "<p>You are adept at using magic that creates or summons creatures. You can add any spell from the conjuration school to your spellbook, provided that spell conjures, creates, or summons one or more creatures, such as the find steed and conjure woodland beings spells. These spells count as Arcane spells for you. This feature doesn\u2019t apply to spells from the conjuration school that don\u2019t create or summon actual creatures, such as the guardian of faith and spirit guardians spells. 1 CLASS OPTIONS 101</p>"),
                _sf(cid, cname, "summoner", "Summoner", ["Unbreakable Focus"], _ymiat_level_label("3rd"),
                    "You have advantage on CON saves to maintain ",
                    "<p>You have advantage on CON saves to maintain concentration on spells from the conjuration school.</p>"),
                _sf(cid, cname, "summoner", "Summoner", ["Master Summoner"], _ymiat_level_label("7th"),
                    "You can have one additional spell from your Rote Spell ",
                    "<p>You can have one additional spell from your Rote Spell feature (see Player\u2019s Guide) per spell level for which you already have a rote spell. These extra rote spells must be spells from the conjuration school that create or summon one or more creatures.</p>"),
                _sf(cid, cname, "summoner", "Summoner", ["Synchronized Companions"], _ymiat_level_label("11th"),
                    "A friendly creature that isn\u2019t a creature you created or ",
                    "<p>A friendly creature that isn\u2019t a creature you created or summoned with a spell has advantage on attack rolls against any creature within 5 feet of a creature that you created or summoned with a spell from the conjuration school, provided the creature you created or summoned isn\u2019t incapacitated.</p>"),
                _sf(cid, cname, "summoner", "Summoner", ["Twinned Conjuration"], _ymiat_level_label("15th"),
                    "When you cast a spell from the conjuration school that ",
                    "<p>When you cast a spell from the conjuration school that creates or summons a creature, you can create or summon twice as many creatures, unless the spell prevents you from having more than one creature at a time, such as the create familiar spell.</p>"),
            ],
            TOV_PG2,
        ),
    ]

def pg2_only_subclasses():
    groups = [
        artificer_pg2_subclasses,
        bard_pg2_subclasses,
        cleric_pg2_subclasses,
        fighter_pg2_subclasses,
        monk_pg2_subclasses,
        paladin_pg2_subclasses,
        ranger_pg2_subclasses,
        rogue_pg2_subclasses,
        sorcerer_pg2_subclasses,
        warlock_pg2_subclasses,
        wizard_pg2_subclasses,
    ]
    result = []
    for fn in groups:
        result.extend(fn())
    return result

