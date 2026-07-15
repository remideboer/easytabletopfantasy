/**
 * YMIAT Character Sheet — local character management.
 * Options from assets/character-creator-data.json; persistence in localStorage.
 */
(function () {
  const STORAGE_KEY = "ymiat-characters-v1";
  const CREATOR_KEY = "ymiat-character-creator-v1";
  const ABILITIES = ["fit", "ins", "wil"];
  const ABILITY_LABELS = { fit: "FIT", ins: "INS", wil: "WIL" };
  const INVENTORY_THRESHOLDS = [-2, -2, -1, -1, 0, 1, 1, 2, 2];
  const INVENTORY_SLOT_COUNT = INVENTORY_THRESHOLDS.length * 2;

  // Defense bonus per gear.html Armor table: base + FIT mod (capped where noted; heavy excludes FIT).
  const ARMOR = [
    { id: "padded", name: "Padded", category: "Light Armor", base: 1, addFit: true, fitCap: null, props: "Natural Materials" },
    { id: "leather", name: "Leather", category: "Light Armor", base: 1, addFit: true, fitCap: null, props: "Natural Materials" },
    { id: "studded-leather", name: "Studded Leather", category: "Light Armor", base: 2, addFit: true, fitCap: null, props: "" },
    { id: "brigandine", name: "Brigandine", category: "Light Armor", base: 2, addFit: true, fitCap: null, props: "" },
    { id: "hide", name: "Hide", category: "Medium Armor", base: 2, addFit: true, fitCap: 2, props: "Natural Materials" },
    { id: "chain-shirt", name: "Chain Shirt", category: "Medium Armor", base: 3, addFit: true, fitCap: 2, props: "" },
    { id: "scale-mail", name: "Scale Mail", category: "Medium Armor", base: 4, addFit: true, fitCap: 2, props: "Noisy" },
    { id: "breastplate", name: "Breastplate", category: "Medium Armor", base: 4, addFit: true, fitCap: 2, props: "" },
    { id: "half-plate", name: "Half Plate", category: "Medium Armor", base: 5, addFit: true, fitCap: 2, props: "Noisy" },
    { id: "ring-mail", name: "Ring Mail", category: "Heavy Armor", base: 4, addFit: false, fitCap: null, props: "Noisy" },
    { id: "chain-mail", name: "Chain Mail", category: "Heavy Armor", base: 6, addFit: false, fitCap: null, props: "Cumbersome (Fitness +1), Noisy" },
    { id: "splint", name: "Splint", category: "Heavy Armor", base: 7, addFit: false, fitCap: null, props: "Cumbersome (Fitness +2), Noisy" },
    { id: "plate", name: "Plate", category: "Heavy Armor", base: 8, addFit: false, fitCap: null, props: "Cumbersome (Fitness +2), Noisy" },
  ];
  const SHIELD_BONUS = 2;

  // Attack bonus per gear.html weapon tables: weapon bonus + FIT mod.
  const WEAPONS = [
    { id: "club", name: "Club", category: "Simple Melee", bonus: 1, props: "Bludgeoning, Light, Slow" },
    { id: "dagger", name: "Dagger", category: "Simple Melee", bonus: 1, props: "Piercing, Finesse, Light, Thrown (Range 20/60)" },
    { id: "greatclub", name: "Greatclub", category: "Simple Melee", bonus: 3, props: "Bludgeoning, Two-Handed" },
    { id: "handaxe", name: "Handaxe", category: "Simple Melee", bonus: 2, props: "Slashing, Light, Thrown (Range 20/60)" },
    { id: "javelin", name: "Javelin", category: "Simple Melee", bonus: 2, props: "Piercing, Thrown (Range 30/120)" },
    { id: "light-hammer", name: "Light Hammer", category: "Simple Melee", bonus: 1, props: "Bludgeoning, Light, Thrown (Range 20/60)" },
    { id: "mace", name: "Mace", category: "Simple Melee", bonus: 2, props: "Bludgeoning" },
    { id: "quarterstaff", name: "Quarterstaff", category: "Simple Melee", bonus: 2, props: "Bludgeoning, Versatile (+3)" },
    { id: "sickle", name: "Sickle", category: "Simple Melee", bonus: 1, props: "Slashing, Light" },
    { id: "spear", name: "Spear", category: "Simple Melee", bonus: 2, props: "Piercing, Thrown (Range 20/60), Versatile (+3)" },
    { id: "dart", name: "Dart", category: "Simple Ranged", bonus: 1, props: "Piercing, Finesse, Thrown (Range 20/60)" },
    { id: "light-crossbow", name: "Light Crossbow", category: "Simple Ranged", bonus: 3, props: "Piercing, Ammunition (Range 80/320; Bolt), Loading, Two-Handed" },
    { id: "shortbow", name: "Shortbow", category: "Simple Ranged", bonus: 2, props: "Piercing, Ammunition (Range 80/320; Arrow), Two-Handed" },
    { id: "sling", name: "Sling", category: "Simple Ranged", bonus: 1, props: "Bludgeoning, Ammunition (Range 30/120; Bullet)" },
    { id: "battleaxe", name: "Battleaxe", category: "Martial Melee", bonus: 3, props: "Slashing, Versatile (+4)" },
    { id: "flail", name: "Flail", category: "Martial Melee", bonus: 3, props: "Bludgeoning" },
    { id: "glaive", name: "Glaive", category: "Martial Melee", bonus: 4, props: "Slashing, Heavy, Reach, Two-Handed" },
    { id: "greataxe", name: "Greataxe", category: "Martial Melee", bonus: 5, props: "Slashing, Heavy, Two-Handed" },
    { id: "greatsword", name: "Greatsword", category: "Martial Melee", bonus: 6, props: "Slashing, Heavy, Two-Handed" },
    { id: "halberd", name: "Halberd", category: "Martial Melee", bonus: 4, props: "Slashing, Heavy, Reach, Two-Handed" },
    { id: "lance", name: "Lance", category: "Martial Melee", bonus: 4, props: "Piercing, Heavy, Reach, Two-Handed (unless mounted)" },
    { id: "longsword", name: "Longsword", category: "Martial Melee", bonus: 3, props: "Slashing, Versatile (+4)" },
    { id: "maul", name: "Maul", category: "Martial Melee", bonus: 6, props: "Bludgeoning, Heavy, Two-Handed" },
    { id: "morningstar", name: "Morningstar", category: "Martial Melee", bonus: 3, props: "Piercing" },
    { id: "pike", name: "Pike", category: "Martial Melee", bonus: 4, props: "Piercing, Heavy, Reach, Two-Handed" },
    { id: "rapier", name: "Rapier", category: "Martial Melee", bonus: 3, props: "Piercing, Finesse" },
    { id: "scimitar", name: "Scimitar", category: "Martial Melee", bonus: 2, props: "Slashing, Finesse, Light" },
    { id: "shortsword", name: "Shortsword", category: "Martial Melee", bonus: 2, props: "Piercing, Finesse, Light" },
    { id: "trident", name: "Trident", category: "Martial Melee", bonus: 3, props: "Piercing, Thrown (Range 20/60), Versatile (+4)" },
    { id: "warhammer", name: "Warhammer", category: "Martial Melee", bonus: 3, props: "Bludgeoning, Versatile (+4)" },
    { id: "war-pick", name: "War Pick", category: "Martial Melee", bonus: 3, props: "Piercing, Versatile (+4)" },
    { id: "whip", name: "Whip", category: "Martial Melee", bonus: 1, props: "Slashing, Finesse, Reach" },
    { id: "blowgun", name: "Blowgun", category: "Martial Ranged", bonus: 0, props: "Piercing, Ammunition (Range 25/100; Needle), Loading" },
    { id: "hand-crossbow", name: "Hand Crossbow", category: "Martial Ranged", bonus: 2, props: "Piercing, Ammunition (Range 30/120; Bolt), Light, Loading" },
    { id: "heavy-crossbow", name: "Heavy Crossbow", category: "Martial Ranged", bonus: 4, props: "Piercing, Ammunition (Range 100/400; Bolt), Heavy, Loading, Two-Handed" },
    { id: "longbow", name: "Longbow", category: "Martial Ranged", bonus: 3, props: "Piercing, Ammunition (Range 150/600; Arrow), Heavy, Two-Handed" },
    { id: "musket", name: "Musket", category: "Martial Ranged", bonus: 5, props: "Piercing, Ammunition (Range 40/120; Bullet), Loading, Two-Handed" },
    { id: "pistol", name: "Pistol", category: "Martial Ranged", bonus: 4, props: "Piercing, Ammunition (Range 30/90; Bullet), Loading" },
  ];

  let data = null;
  let SPELLS = [];
  let store = loadStore();
  let char = null;
  let eventsBound = false;
  let spellModalOpen = false;
  let spellModalFilter = "";
  let spellViewId = null;
  let skillModalOpen = false;
  let languageModalOpen = false;
  let talentModalOpen = false;
  let languageCustomDraft = "";

  const el = {};

  function cacheElements() {
    el.loading = document.getElementById("cs-loading");
    el.error = document.getElementById("cs-error");
    el.app = document.getElementById("cs-app");
    el.charSelect = document.getElementById("cs-char-select");
    el.sheet = document.getElementById("cs-sheet");
    el.empty = document.getElementById("cs-empty");
    el.hint = document.getElementById("cs-hint");
    el.btnNew = document.getElementById("cs-btn-new");
    el.btnImport = document.getElementById("cs-btn-import");
    el.btnDelete = document.getElementById("cs-btn-delete");
    el.modalRoot = document.getElementById("cs-modal-root");
  }

  function rootPath() {
    if (typeof window.ymiatGetRootPath === "function") {
      return window.ymiatGetRootPath();
    }
    const path = window.location.pathname;
    const depth = path.replace(/^\//, "").split("/").filter(Boolean).length - 1;
    if (depth <= 0) return "";
    return "../".repeat(depth);
  }

  function rp(url) {
    if (!url || url.startsWith("http")) return url;
    return rootPath() + url;
  }

  function showLoadError(message) {
    if (el.loading) el.loading.hidden = true;
    if (el.app) el.app.hidden = true;
    if (el.error) {
      el.error.hidden = false;
      const p = el.error.querySelector("p");
      if (p && message) {
        p.textContent = message;
      }
    }
  }

  function showApp() {
    if (el.loading) el.loading.hidden = true;
    if (el.error) el.error.hidden = true;
    if (el.app) el.app.hidden = false;
  }

  function uid() {
    return "c-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 9);
  }

  function defaultCharacter() {
    return {
      id: uid(),
      name: "Unnamed Hero",
      level: 1,
      xp: 0,
      hearts: 3,
      abilities: { fit: 0, ins: 0, wil: 0 },
      woundsNow: 0,
      woundsTemp: 0,
      resolve: 0,
      spellPowerNow: 0,
      learnedSpellIds: [],
      preparedSpellIds: [],
      chosenSkills: [],
      chosenLanguages: [],
      chosenTalents: [],
      classId: "",
      subclassId: "",
      lineageId: "",
      heritageId: "",
      backgroundId: "",
      armorId: "",
      hasShield: false,
      weaponId: "",
      speed: 30,
      size: "Medium",
      currency: { gold: 0, silver: 0, copper: 0 },
      equippedText: "",
      inventory: Array(INVENTORY_SLOT_COUNT).fill(""),
    };
  }

  function defaultStore() {
    return { version: 1, activeId: null, characters: [] };
  }

  function loadStore() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed.characters)) {
          if (parsed.characters.length) {
            parsed.characters = parsed.characters.filter(Boolean).map((c) => {
              try {
                return normalizeCharacter(c);
              } catch (_) {
                return normalizeCharacter(defaultCharacter());
              }
            });
          }
          if (!parsed.activeId || !parsed.characters.some((c) => c.id === parsed.activeId)) {
            parsed.activeId = parsed.characters.length ? parsed.characters[0].id : null;
          }
          return parsed;
        }
      }
    } catch (_) { /* ignore */ }
    return defaultStore();
  }

  function normalizeCharacter(c) {
    c.level = Math.min(10, Math.max(1, Number(c.level) || 1));
    c.xp = Math.max(0, Number(c.xp) || 0);
    c.hearts = Math.min(3, Math.max(0, Number.isFinite(Number(c.hearts)) ? Number(c.hearts) : 3));
    c.resolve = Math.min(4, Math.max(0, Number(c.resolve) || 0));
    c.abilities = c.abilities || { fit: 0, ins: 0, wil: 0 };
    ABILITIES.forEach((a) => {
      c.abilities[a] = clampAbility(Number(c.abilities[a]) || 0);
    });
    c.woundsNow = Math.max(0, Number(c.woundsNow) || 0);
    c.woundsTemp = Math.max(0, Number(c.woundsTemp) || 0);
    c.armorId = typeof c.armorId === "string" ? c.armorId : "";
    c.hasShield = Boolean(c.hasShield);
    c.weaponId = typeof c.weaponId === "string" ? c.weaponId : "";
    c.spellPowerNow = Math.max(0, Number(c.spellPowerNow) || 0);
    c.learnedSpellIds = Array.isArray(c.learnedSpellIds)
      ? [...new Set(c.learnedSpellIds.filter((id) => typeof id === "string"))]
      : [];
    c.preparedSpellIds = Array.isArray(c.preparedSpellIds)
      ? [...new Set(c.preparedSpellIds.filter((id) => typeof id === "string"))].filter((id) => c.learnedSpellIds.includes(id))
      : [];
    c.chosenSkills = Array.isArray(c.chosenSkills)
      ? [...new Set(c.chosenSkills.filter((s) => typeof s === "string"))]
      : [];
    c.chosenLanguages = Array.isArray(c.chosenLanguages)
      ? [...new Set(c.chosenLanguages.filter((s) => typeof s === "string"))]
      : [];
    c.chosenTalents = Array.isArray(c.chosenTalents)
      ? [...new Set(c.chosenTalents.filter((s) => typeof s === "string"))].slice(0, 1)
      : [];
    c.currency = c.currency || { gold: 0, silver: 0, copper: 0 };
    if (!Array.isArray(c.inventory) || c.inventory.length !== INVENTORY_SLOT_COUNT) {
      const inv = Array.isArray(c.inventory) ? c.inventory.slice(0, INVENTORY_SLOT_COUNT) : [];
      while (inv.length < INVENTORY_SLOT_COUNT) inv.push("");
      c.inventory = inv;
    }
    return c;
  }

  function saveStore() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
  }

  function activeCharacter() {
    if (!store.activeId) {
      char = null;
      return null;
    }
    char = store.characters.find((c) => c.id === store.activeId) || null;
    if (!char) {
      store.activeId = null;
      return null;
    }
    return char;
  }

  function byId(list, id) {
    return (list || []).find((item) => item.id === id) || null;
  }

  const WORD_TO_NUMBER = { one: 1, two: 2, three: 3, four: 4, five: 5 };

  function wordToNumber(w) {
    if (!w) return null;
    return WORD_TO_NUMBER[w.toLowerCase()] || parseInt(w, 10) || null;
  }

  function splitChoiceList(text) {
    return text
      .split(",")
      .flatMap((part) => part.split(/\s+or\s+|\s+and\s+/i))
      .map((s) => s.trim())
      .filter(Boolean);
  }

  // Backgrounds state their skill choice as one of two shapes:
  // "Choose two from A, B, C, or D." or "X and one of A, B, or C."
  function parseBackgroundSkillChoice(background) {
    if (!background || !background.body) return null;
    const m = background.body.match(/Skill Proficiencies:?<\/strong>\s*([^<]+)/i);
    if (!m) return null;
    const text = m[1].trim().replace(/\.$/, "");
    const oneOf = text.match(/^(.+?)\s+and\s+one of\s+(.+)$/i);
    if (oneOf) {
      return { fixed: [oneOf[1].trim()], count: 1, options: splitChoiceList(oneOf[2]) };
    }
    const chooseN = text.match(/^Choose (\w+) from\s+(.+)$/i);
    if (chooseN) {
      return { fixed: [], count: wordToNumber(chooseN[1]) || 1, options: splitChoiceList(chooseN[2]) };
    }
    return null;
  }

  // Backgrounds already ship a structured talentChoices array (always "choose one").
  function parseBackgroundTalentChoice(background) {
    if (!background || !Array.isArray(background.talentChoices) || !background.talentChoices.length) return null;
    return { fixed: [], count: 1, options: background.talentChoices };
  }

  // Heritages state their language grant as "Common plus N additional
  // (<lead-in>: A, B, or C)." The lead-in wording varies (typical, often,
  // "overlord's tongue", etc.) and a few omit a pick-list entirely in favor
  // of a descriptive hint - those just get an empty option list and the
  // character sheet's free-text "add custom language" input covers it.
  function parseHeritageLanguageChoice(heritage) {
    if (!heritage || !heritage.body) return null;
    const m = heritage.body.match(/Languages?\.?<\/strong>\s*([^<]+)/i);
    if (!m) return null;
    const text = m[1].trim().replace(/\.$/, "");
    const plusM = text.match(/^Common plus (\w+) additional\s*(?:\(([^)]*)\))?/i);
    if (!plusM) return { fixed: ["Common"], count: 0, options: [] };
    const count = wordToNumber(plusM[1]) || 1;
    let paren = (plusM[2] || "").trim();
    paren = paren.replace(/^(typical\s+esoteric|typical|often|overlord's tongue|language of the)\s*:?\s*/i, "");
    const options = splitChoiceList(paren);
    return { fixed: ["Common"], count, options };
  }

  function levelRange() {
    return data?.levelRange || { min: 1, max: 10, subclassMin: 2 };
  }

  // XP threshold per core.html#experience-points: (level - 1) * 100.
  function xpThreshold(level) {
    return Math.max(0, level - 1) * 100;
  }

  function levelFromXp(xp, range) {
    const lvl = Math.floor(Math.max(0, xp) / 100) + 1;
    return Math.min(range.max, Math.max(range.min, lvl));
  }

  function clampAbility(n) {
    return Math.min(5, Math.max(-5, n));
  }

  function heartsLost(c) {
    return 3 - (c.hearts ?? 3);
  }

  function heartPenalties(c) {
    const lost = heartsLost(c);
    return { ability: -lost, speed: -5 * lost, maxWd: -2 * lost };
  }

  function effectiveMod(c, ability) {
    return c.abilities[ability] + heartPenalties(c).ability;
  }

  function findClass(c) {
    return byId(data.classes, c.classId);
  }

  function findSubclass(c) {
    const cls = findClass(c);
    if (!cls) return null;
    return byId(cls.subclasses, c.subclassId);
  }

  function spellcastingAbility(cls) {
    if (!cls || !cls.spellcasting) return null;
    const sc = cls.spellcasting.toLowerCase();
    if (sc.includes("divine") || sc.includes("primordial")) {
      if (cls.keyAbility === "fit") return "ins";
    }
    if (sc.includes("wyrd")) return "wil";
    return cls.keyAbility;
  }

  function isCaster(c) {
    const cls = findClass(c);
    return Boolean(cls && cls.spellcasting);
  }

  function computeMaxWd(c) {
    const cls = findClass(c);
    const base = cls ? cls.maxWd : 8;
    const fitEff = effectiveMod(c, "fit");
    const levelBonus = Math.max(0, c.level - 1);
    const hp = heartPenalties(c).maxWd;
    return Math.max(1, base + fitEff + levelBonus + hp);
  }

  function computeSpellPowerMax(c) {
    const cls = findClass(c);
    const spellAb = spellcastingAbility(cls);
    if (!spellAb) return null;
    const mod = effectiveMod(c, spellAb);
    return Math.max(0, 3 * mod);
  }

  // Max spell circle by level per classes.html progression tables.
  const FULL_CASTER_CIRCLE = [null, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9];
  const HALF_CASTER_CIRCLE = [null, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5];
  const WARLOCK_CIRCLE = [null, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5];
  const CLASS_CIRCLE_TABLE = {
    bard: FULL_CASTER_CIRCLE,
    cleric: FULL_CASTER_CIRCLE,
    druid: FULL_CASTER_CIRCLE,
    sorcerer: FULL_CASTER_CIRCLE,
    wizard: FULL_CASTER_CIRCLE,
    theurge: FULL_CASTER_CIRCLE,
    witch: FULL_CASTER_CIRCLE,
    paladin: HALF_CASTER_CIRCLE,
    ranger: HALF_CASTER_CIRCLE,
    warlock: WARLOCK_CIRCLE,
  };

  function maxSpellCircle(cls, level) {
    if (!cls) return 0;
    const table = CLASS_CIRCLE_TABLE[cls.id];
    if (!table) return 0;
    return table[Math.min(10, Math.max(1, level))] || 0;
  }

  // Cleric/Druid/Wizard state their formula outright: spellcasting mod + level
  // (minimum 1). No class page gives numeric cantrip/known-spell counts (each
  // just says "as shown on your progression table," but that table only has
  // Max Circle, not counts) — those are derived from the matching 5e SRD
  // class table, read at the 5e level this ruleset's own conversion method
  // (conversion.html) maps a YMIAT level to: 5e level = 2*level - 1.
  // Witch and Theurge are homebrew with no 5e equivalent, so their numbers
  // are approximated from the closest same-speed 5e class (flagged below).
  function cantripsFromBreakpoints(level, base, at4, at10) {
    const e5 = 2 * level - 1;
    if (e5 >= 10) return at10;
    if (e5 >= 4) return at4;
    return base;
  }

  const CANTRIP_BREAKPOINTS = {
    bard: [2, 3, 4],
    cleric: [3, 4, 5],
    druid: [2, 3, 4],
    sorcerer: [4, 5, 6],
    warlock: [2, 3, 4],
    wizard: [3, 4, 5],
    witch: [4, 5, 6], // approximated as Sorcerer (same full-caster-speed known type)
    theurge: [3, 4, 5], // approximated as Wizard (same full-caster-speed prepared type)
    paladin: [0, 0, 0],
    ranger: [0, 0, 0],
  };

  function cantripCap(cls, level) {
    const bp = cls && CANTRIP_BREAKPOINTS[cls.id];
    if (!bp) return 0;
    return cantripsFromBreakpoints(level, bp[0], bp[1], bp[2]);
  }

  // 5e SRD "Spells Known" columns, resolved at 5e level (2*YMIAT level - 1)
  // and indexed 0..9 for YMIAT levels 1..10.
  const KNOWN_SPELLS_TABLE = {
    bard: [4, 6, 8, 10, 12, 15, 16, 19, 20, 22],
    sorcerer: [2, 4, 6, 8, 10, 12, 13, 14, 15, 15],
    warlock: [2, 4, 6, 8, 10, 11, 12, 13, 14, 15],
    ranger: [0, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    witch: [2, 4, 6, 8, 10, 12, 13, 14, 15, 15], // approximated as Sorcerer
  };

  // "known": fixed 5e known-spells table, all known spells are always active.
  // "known-formula": Paladin has no 5e known-spell table (5e Paladin prepares
  // instead) — this ruleset made Paladin a known caster, so its own 5e prepare
  // formula (mod + half level, min 1) is reused as the known-count instead.
  // "full": Cleric/Druid prepare directly from the whole eligible list, no
  // personal spellbook — only a Prepared cap exists.
  // "spellbook": Wizard's stated spellbook (6 spells at 1st, +2/level) gates a
  // Learned pool, with Prepared (mod + level) a subset of it.
  // "spellbook-fixed": Theurge's libram uses the same shape as Wizard's
  // spellbook but is stated outright (6 spells at 1st circle, +2/level).
  const SPELL_MODE = {
    bard: "known",
    sorcerer: "known",
    warlock: "known",
    ranger: "known",
    witch: "known",
    paladin: "known-formula",
    cleric: "full",
    druid: "full",
    wizard: "spellbook",
    theurge: "spellbook-fixed",
  };

  function spellMode(cls) {
    return (cls && SPELL_MODE[cls.id]) || null;
  }

  // The number of leveled spells actually usable at once: "Known" for known
  // casters, "Prepared" for full/spellbook casters.
  function computeActiveCap(c) {
    const cls = findClass(c);
    const mode = spellMode(cls);
    if (!mode) return 0;
    const spellAb = spellcastingAbility(cls);
    if (!spellAb) return 0;
    const mod = effectiveMod(c, spellAb);
    if (mode === "known") {
      const table = KNOWN_SPELLS_TABLE[cls.id];
      return table ? table[Math.min(10, Math.max(1, c.level)) - 1] : 0;
    }
    if (mode === "known-formula") {
      return Math.max(1, mod + Math.floor(c.level / 2));
    }
    return Math.max(1, mod + c.level);
  }

  function activeCapLabel(mode) {
    return mode === "known" || mode === "known-formula" ? "Known" : "Prepared";
  }

  // "spellbook"/"spellbook-fixed" are the only modes with a personal pool
  // distinct from the active cap (Wizard's spellbook / Theurge's libram: 6 at
  // 1st, +2/level). "full" (Cleric/Druid prepare straight from the whole
  // eligible list) and "known"/"known-formula" (fixed known-spell count) have
  // no separate pool — learnedSpellIds itself is the capped active set.
  function usesLearnedTier(mode) {
    return mode === "spellbook" || mode === "spellbook-fixed";
  }

  // Only meaningful when usesLearnedTier(mode) is true.
  function computeLearnedCap(c) {
    return 6 + 2 * Math.max(0, c.level - 1);
  }

  function spellById(id) {
    return SPELLS.find((s) => s.id === id) || null;
  }

  function eligibleSpells(c) {
    const cls = findClass(c);
    if (!cls) return [];
    const maxCircle = maxSpellCircle(cls, c.level);
    return SPELLS.filter((s) => s.classes.includes(cls.id) && s.circle <= maxCircle);
  }

  function computeDefense(c) {
    const fitMod = effectiveMod(c, "fit");
    const armor = byId(ARMOR, c.armorId);
    const base = armor
      ? armor.base + (armor.addFit ? (armor.fitCap != null ? Math.min(fitMod, armor.fitCap) : fitMod) : 0)
      : fitMod;
    return base + (c.hasShield ? SHIELD_BONUS : 0);
  }

  function armorOptionLabel(armor) {
    const mod = armor.addFit
      ? armor.fitCap != null
        ? `+${armor.base} + FIT (max +${armor.fitCap})`
        : `+${armor.base} + FIT`
      : formatMod(armor.base);
    return `${armor.name} (${mod})`;
  }

  function weaponOptionLabel(weapon) {
    return `${weapon.name} (${formatMod(weapon.bonus)})`;
  }

  function computeAttackBonus(c) {
    const weapon = byId(WEAPONS, c.weaponId);
    if (!weapon) return null;
    return effectiveMod(c, "fit") + weapon.bonus;
  }

  function computeSpeed(c) {
    const base = Number(c.speed) || 30;
    return Math.max(0, base + heartPenalties(c).speed);
  }

  function inventoryUnlockedRows(c) {
    const fit = effectiveMod(c, "fit");
    return INVENTORY_THRESHOLDS.filter((t) => fit >= t).length;
  }

  function inventoryUnlockedSlots(c) {
    return inventoryUnlockedRows(c) * 2;
  }

  function isSlotUnlocked(c, index) {
    const row = Math.floor(index / 2);
    return row < inventoryUnlockedRows(c);
  }

  function featuresAtLevel(items, level) {
    if (!items || !items.length) return [];
    return items.filter((item) => (item.minLevel || 1) <= level);
  }

  function parseLineageDefaults(lineage) {
    const text = (lineage?.body || lineage?.teaser || "").replace(/\n/g, " ");
    const speedMatch = text.match(/Speed\.?\s*([^.<]+)/i);
    const sizeMatch = text.match(/Size\.?\s*([^.<]+)/i);
    let speed = 30;
    if (speedMatch) {
      const num = speedMatch[1].match(/(\d+)/);
      if (num) speed = parseInt(num[1], 10);
    }
    let size = "Medium";
    if (sizeMatch) {
      const s = sizeMatch[1].trim();
      if (/small/i.test(s)) size = "Small";
      else if (/large/i.test(s)) size = "Large";
      else size = "Medium";
    }
    return { speed, size };
  }

  function formatMod(n) {
    if (n > 0) return "+" + n;
    return String(n);
  }

  function escapeHtml(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderFeatureList(items) {
    if (!items.length) return '<p class="cs-muted">No features at this level.</p>';
    return `<ul class="cs-feature-list">${items
      .map(
        (item) =>
          `<li><strong>${escapeHtml(item.name)}</strong>${item.summary ? ` — ${escapeHtml(item.summary)}` : ""}</li>`
      )
      .join("")}</ul>`;
  }

  function renderDetailPaneShell(title, rulesUrl) {
    const link = rulesUrl
      ? `<a class="cs-detail-link" href="${escapeHtml(rp(rulesUrl))}" target="_blank" rel="noopener">Open full rules</a>`
      : "";
    return `<div class="cs-detail-pane">
      <h3 class="cs-detail-title">${escapeHtml(title)}</h3>
      <div class="cs-detail-body"></div>
      ${link}
    </div>`;
  }

  function fillDetailPanes(lineage, heritage, background) {
    if (!el.sheet) return;
    const bodies = el.sheet.querySelectorAll(".cs-detail-body");
    const items = [
      { item: lineage, fallback: "Lineage" },
      { item: heritage, fallback: "Heritage" },
      { item: background, fallback: "Background" },
    ];
    bodies.forEach((node, i) => {
      const entry = items[i];
      const html = entry.item?.body || entry.item?.teaser;
      node.innerHTML = html || '<p class="cs-muted">Select an option to see details.</p>';
      const title = node.closest(".cs-detail-pane")?.querySelector(".cs-detail-title");
      if (title) title.textContent = entry.item?.name || entry.fallback;
    });
  }

  function stepper(id, value, label, opts) {
    const min = opts?.min ?? -5;
    const max = opts?.max ?? 5;
    const display = opts?.display ?? formatMod(value);
    const hint = opts?.hint ? `<span class="cs-stepper-hint">${opts.hint}</span>` : "";
    return `<div class="cs-stepper" data-stepper="${id}" data-min="${min}" data-max="${max}">
      <span class="cs-stepper-val" aria-live="polite">${escapeHtml(display)}</span>
      <div class="cs-stepper-btns">
        <button type="button" class="cs-stepper-btn" data-delta="-1" aria-label="Decrease ${label}">▼</button>
        <button type="button" class="cs-stepper-btn" data-delta="1" aria-label="Increase ${label}">▲</button>
      </div>
      ${hint}
    </div>`;
  }

  function levelControl(c, range) {
    const atMax = c.level >= range.max;
    const nextXpHint = atMax ? "Max level" : `Next: ${xpThreshold(c.level + 1)} XP`;
    return `<div class="cs-level-control">
      <span class="cs-label">LVL</span>
      <div class="cs-stepper cs-stepper--level" data-stepper="level" data-min="${range.min}" data-max="${range.max}">
        <div class="cs-level-circle" aria-live="polite">${c.level}</div>
        <div class="cs-stepper-btns">
          <button type="button" class="cs-stepper-btn" data-delta="-1" aria-label="Decrease level">▼</button>
          <button type="button" class="cs-stepper-btn" data-delta="1" aria-label="Increase level">▲</button>
        </div>
      </div>
      <div class="cs-xp-field">
        <label class="cs-label" for="cs-xp">XP</label>
        <input type="number" id="cs-xp" class="cs-input cs-input--xp" min="0" step="5" value="${c.xp}" aria-label="Experience points" />
        <span class="cs-xp-hint">${nextXpHint}</span>
      </div>
    </div>`;
  }

  function renderSpellChipGroup(title, chipsHtml) {
    return `<div class="cs-spell-group-sheet">
      <h3 class="cs-spell-group-sheet-title">${escapeHtml(title)}</h3>
      <div class="cs-spell-chips">${chipsHtml}</div>
    </div>`;
  }

  function renderSkillsLanguagesSection(c, background, heritage) {
    const skillChoice = parseBackgroundSkillChoice(background);
    const langChoice = parseHeritageLanguageChoice(heritage);
    const talentChoice = parseBackgroundTalentChoice(background);
    if (!skillChoice && !langChoice && !talentChoice) return "";

    let talentBlock = "";
    if (talentChoice) {
      const chosen = c.chosenTalents[0];
      const pill = chosen ? `<span class="cs-spell-chip is-active">${escapeHtml(chosen)}</span>` : '<span class="cs-muted">None chosen yet</span>';
      talentBlock = `<div class="cs-choice-section">
        <h3 class="cs-spell-group-sheet-title">Talent <button type="button" class="cs-btn-link" id="cs-choose-talent">Choose (${c.chosenTalents.length}/${talentChoice.count})</button></h3>
        <div class="cs-spell-chips">${pill}</div>
      </div>`;
    }

    let skillsBlock = "";
    if (skillChoice) {
      const chosenOptions = c.chosenSkills.filter((s) => skillChoice.options.includes(s));
      const pills = [...skillChoice.fixed, ...chosenOptions]
        .map((s) => `<span class="cs-spell-chip is-active">${escapeHtml(s)}</span>`)
        .join("");
      skillsBlock = `<div class="cs-choice-section">
        <h3 class="cs-spell-group-sheet-title">Skills <button type="button" class="cs-btn-link" id="cs-choose-skills">Choose (${chosenOptions.length}/${skillChoice.count})</button></h3>
        <div class="cs-spell-chips">${pills || '<span class="cs-muted">None chosen yet</span>'}</div>
      </div>`;
    }

    let languagesBlock = "";
    if (langChoice) {
      const pills = [...langChoice.fixed, ...c.chosenLanguages]
        .map((s) => `<span class="cs-spell-chip is-active">${escapeHtml(s)}</span>`)
        .join("");
      languagesBlock = `<div class="cs-choice-section">
        <h3 class="cs-spell-group-sheet-title">Languages <button type="button" class="cs-btn-link" id="cs-choose-languages">Choose (${c.chosenLanguages.length}/${langChoice.count})</button></h3>
        <div class="cs-spell-chips">${pills}</div>
      </div>`;
    }

    return talentBlock + skillsBlock + languagesBlock;
  }

  function renderSpellsPane(c, cls) {
    const mode = spellMode(cls);
    const tiered = usesLearnedTier(mode);
    const cCap = cantripCap(cls, c.level);
    const activeCap = computeActiveCap(c);
    const label = activeCapLabel(mode);

    const learned = c.learnedSpellIds.map(spellById).filter((s) => s && s.classes.includes(cls.id));
    const cantrips = learned.filter((s) => s.circle === 0).sort((a, b) => a.name.localeCompare(b.name));
    const leveled = learned.filter((s) => s.circle > 0).sort((a, b) => a.circle - b.circle || a.name.localeCompare(b.name));

    let counterText;
    if (tiered) {
      const learnedCap = computeLearnedCap(c);
      const activeCount = leveled.filter((s) => c.preparedSpellIds.includes(s.id)).length;
      counterText = `Learned ${leveled.length}/${learnedCap} · Prepared ${activeCount}/${activeCap}`;
    } else {
      counterText = `${label} ${leveled.length}/${activeCap}`;
    }

    const groups = [];
    if (cantrips.length) {
      const chips = cantrips
        .map((s) => `<span class="cs-spell-chip is-active" data-spell-view="${s.id}" title="${escapeHtml(s.school)} · Cantrip · Click for details">${escapeHtml(s.name)}</span>`)
        .join("");
      groups.push(renderSpellChipGroup("Cantrips", chips));
    }

    const maxCircle = leveled.length ? leveled[leveled.length - 1].circle : 0;
    for (let circle = 1; circle <= maxCircle; circle++) {
      const spells = leveled.filter((s) => s.circle === circle);
      if (!spells.length) continue;
      const chips = spells
        .map((s) => {
          const active = tiered ? c.preparedSpellIds.includes(s.id) : true;
          const stateLabel = tiered ? (active ? "Prepared" : "Learned") : label;
          return `<span class="cs-spell-chip${active ? " is-active" : " is-inactive"}" data-spell-view="${s.id}" title="${escapeHtml(s.school)} · Circle ${circle} · ${stateLabel} · Click for details">${escapeHtml(s.name)}</span>`;
        })
        .join("");
      groups.push(renderSpellChipGroup(`Circle ${circle}`, chips));
    }

    return `<div class="cs-pane cs-pane--spells">
      <h2 class="cs-pane-title cs-pane-title--with-action">Spells <button type="button" class="btn cs-btn-secondary cs-btn-small" id="cs-manage-spells">Manage Spells</button></h2>
      <p class="cs-muted">Cantrips ${cantrips.length}/${cCap} · ${counterText}</p>
      ${groups.length ? groups.join("") : '<p class="cs-muted">No spells learned yet.</p>'}
    </div>`;
  }

  function renderModals() {
    if (!el.modalRoot) return;
    if (spellModalOpen && char) {
      renderManageSpellsModal();
    } else if (spellViewId && char) {
      renderSpellViewModal();
    } else if (skillModalOpen && char) {
      renderSkillModal();
    } else if (languageModalOpen && char) {
      renderLanguageModal();
    } else if (talentModalOpen && char) {
      renderTalentModal();
    } else {
      el.modalRoot.innerHTML = "";
    }
  }

  function renderTalentModal() {
    const background = byId(data.backgrounds, char.backgroundId);
    const choice = parseBackgroundTalentChoice(background);
    if (!background || !choice) {
      el.modalRoot.innerHTML = "";
      return;
    }
    const chosen = char.chosenTalents[0] || "";
    const rows = choice.options
      .map(
        (opt) => `<li class="cs-choice-row">
          <label class="cs-spell-check">
            <input type="radio" name="cs-talent-radio" data-talent-option="${escapeHtml(opt)}"${opt === chosen ? " checked" : ""} />
            ${escapeHtml(opt)}
          </label>
        </li>`
      )
      .join("");

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-choice-modal-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="Choose Talent">
        <div class="cs-modal-header">
          <h2>Choose Talent — ${escapeHtml(background.name)}</h2>
          <button type="button" class="cs-modal-close" id="cs-choice-modal-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-body">
          <ul class="cs-spell-list">${rows}</ul>
        </div>
      </div>
    </div>`;
  }

  function renderSkillModal() {
    const background = byId(data.backgrounds, char.backgroundId);
    const choice = parseBackgroundSkillChoice(background);
    if (!background || !choice) {
      el.modalRoot.innerHTML = "";
      return;
    }
    const chosenOptions = char.chosenSkills.filter((s) => choice.options.includes(s));
    const rows = choice.options
      .map((opt) => {
        const checked = chosenOptions.includes(opt);
        const disabled = !checked && chosenOptions.length >= choice.count;
        return `<li class="cs-choice-row">
          <label class="cs-spell-check">
            <input type="checkbox" data-skill-option="${escapeHtml(opt)}"${checked ? " checked" : ""}${disabled ? " disabled" : ""} />
            ${escapeHtml(opt)}
          </label>
        </li>`;
      })
      .join("");
    const fixedPills = choice.fixed
      .map((f) => `<span class="cs-spell-chip is-active">${escapeHtml(f)}</span>`)
      .join("");

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-choice-modal-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="Choose Skills">
        <div class="cs-modal-header">
          <h2>Choose Skills — ${escapeHtml(background.name)}</h2>
          <button type="button" class="cs-modal-close" id="cs-choice-modal-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-sub">
          <span class="cs-modal-counter">Chosen ${chosenOptions.length}/${choice.count}</span>
        </div>
        <div class="cs-modal-body">
          ${choice.fixed.length ? `<p class="cs-muted">Granted automatically:</p><div class="cs-spell-chips">${fixedPills}</div>` : ""}
          <ul class="cs-spell-list">${rows}</ul>
        </div>
      </div>
    </div>`;
  }

  function renderLanguageModal() {
    const heritage = byId(data.heritages, char.heritageId);
    const choice = parseHeritageLanguageChoice(heritage);
    if (!heritage || !choice) {
      el.modalRoot.innerHTML = "";
      return;
    }
    const suggestedChosen = char.chosenLanguages.filter((l) => choice.options.includes(l));
    const customChosen = char.chosenLanguages.filter((l) => !choice.options.includes(l));
    const atCap = char.chosenLanguages.length >= choice.count;

    const suggestedRows = choice.options
      .map((opt) => {
        const checked = suggestedChosen.includes(opt);
        const disabled = !checked && atCap;
        return `<li class="cs-choice-row">
          <label class="cs-spell-check">
            <input type="checkbox" data-language-option="${escapeHtml(opt)}"${checked ? " checked" : ""}${disabled ? " disabled" : ""} />
            ${escapeHtml(opt)}
          </label>
        </li>`;
      })
      .join("");
    const customRows = customChosen
      .map(
        (lang) => `<li class="cs-choice-row">
          <span class="cs-spell-name">${escapeHtml(lang)}</span>
          <button type="button" class="cs-modal-close" data-language-remove="${escapeHtml(lang)}" aria-label="Remove ${escapeHtml(lang)}">×</button>
        </li>`
      )
      .join("");
    const fixedPills = choice.fixed
      .map((f) => `<span class="cs-spell-chip is-active">${escapeHtml(f)}</span>`)
      .join("");

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-choice-modal-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="Choose Languages">
        <div class="cs-modal-header">
          <h2>Choose Languages — ${escapeHtml(heritage.name)}</h2>
          <button type="button" class="cs-modal-close" id="cs-choice-modal-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-sub">
          <span class="cs-modal-counter">Chosen ${char.chosenLanguages.length}/${choice.count}</span>
        </div>
        <div class="cs-modal-body">
          ${choice.fixed.length ? `<p class="cs-muted">Granted automatically:</p><div class="cs-spell-chips">${fixedPills}</div>` : ""}
          ${choice.options.length ? `<p class="cs-muted">Suggested:</p><ul class="cs-spell-list">${suggestedRows}</ul>` : '<p class="cs-muted">No suggested list for this heritage - add languages below.</p>'}
          ${customChosen.length ? `<p class="cs-muted">Added:</p><ul class="cs-spell-list">${customRows}</ul>` : ""}
          <div class="cs-choice-add-row">
            <input type="text" id="cs-language-custom" class="cs-input" placeholder="Add another language…" value="${escapeHtml(languageCustomDraft)}"${atCap ? " disabled" : ""} />
            <button type="button" class="btn cs-btn-secondary cs-btn-small" id="cs-language-add"${atCap ? " disabled" : ""}>Add</button>
          </div>
        </div>
      </div>
    </div>`;
  }

  function renderSpellViewModal() {
    const spell = spellById(spellViewId);
    if (!spell) {
      el.modalRoot.innerHTML = "";
      return;
    }
    const circleLabel = spell.circle === 0 ? "Cantrip" : `Circle ${spell.circle}`;
    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-spell-view-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="${escapeHtml(spell.name)}">
        <div class="cs-modal-header">
          <h2>${escapeHtml(spell.name)}</h2>
          <button type="button" class="cs-modal-close" id="cs-spell-view-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-body">
          <p class="cs-spell-view-meta">${escapeHtml(spell.school)} · ${escapeHtml(circleLabel)} · ${escapeHtml(spell.castingTime)}</p>
          <p class="cs-spell-view-meta">Range: ${escapeHtml(spell.range)} · Duration: ${escapeHtml(spell.duration)} · Components: ${escapeHtml(spell.components)}</p>
          <p class="cs-spell-view-desc">${escapeHtml(spell.description)}</p>
        </div>
      </div>
    </div>`;
  }

  function renderManageSpellsModal() {
    const cls = findClass(char);
    const mode = spellMode(cls);
    const tiered = usesLearnedTier(mode);
    const label = activeCapLabel(mode);
    const maxCircle = maxSpellCircle(cls, char.level);
    const cCap = cantripCap(cls, char.level);
    const activeCap = computeActiveCap(char);
    const learnedCap = tiered ? computeLearnedCap(char) : null;
    const filterText = spellModalFilter.trim().toLowerCase();
    const eligible = eligibleSpells(char).filter((s) => !filterText || s.name.toLowerCase().includes(filterText));

    const cantripLearnedCount = char.learnedSpellIds.filter((id) => {
      const s = spellById(id);
      return s && s.circle === 0;
    }).length;
    const learnedLeveledCount = char.learnedSpellIds.filter((id) => {
      const s = spellById(id);
      return s && s.circle > 0;
    }).length;
    const activeLeveledCount = tiered
      ? char.preparedSpellIds.filter((id) => {
          const s = spellById(id);
          return s && s.circle > 0;
        }).length
      : learnedLeveledCount;

    const groups = [];
    for (let circle = 0; circle <= maxCircle; circle++) {
      const spells = eligible.filter((s) => s.circle === circle).sort((a, b) => a.name.localeCompare(b.name));
      if (!spells.length) continue;
      const isCantrip = circle === 0;
      const rows = spells
        .map((s) => {
          const learned = char.learnedSpellIds.includes(s.id);
          const prepared = char.preparedSpellIds.includes(s.id);

          if (isCantrip) {
            const disabled = !learned && cantripLearnedCount >= cCap;
            return `<li class="cs-spell-row-modal">
              <label class="cs-spell-check">
                <input type="checkbox" data-spell-learn="${s.id}"${learned ? " checked" : ""}${disabled ? " disabled" : ""} />
                <span class="cs-spell-name">${escapeHtml(s.name)}</span>
              </label>
              <span class="cs-spell-tag">Always active</span>
              <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(s.castingTime)}</span>
            </li>`;
          }

          if (!tiered) {
            const disabled = !learned && activeLeveledCount >= activeCap;
            return `<li class="cs-spell-row-modal">
              <label class="cs-spell-check">
                <input type="checkbox" data-spell-learn="${s.id}"${learned ? " checked" : ""}${disabled ? " disabled" : ""} />
                <span class="cs-spell-name">${escapeHtml(s.name)}</span>
              </label>
              <span class="cs-spell-tag">${label}</span>
              <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(s.castingTime)}</span>
            </li>`;
          }

          const learnDisabled = !learned && learnedLeveledCount >= learnedCap;
          const prepDisabled = !learned || (!prepared && activeLeveledCount >= activeCap);
          return `<li class="cs-spell-row-modal">
            <label class="cs-spell-check">
              <input type="checkbox" data-spell-learn="${s.id}"${learned ? " checked" : ""}${learnDisabled ? " disabled" : ""} />
              <span class="cs-spell-name">${escapeHtml(s.name)}</span>
            </label>
            <label class="cs-spell-check cs-spell-check--prep">
              <input type="checkbox" data-spell-prepare="${s.id}"${prepared ? " checked" : ""}${prepDisabled ? " disabled" : ""} />
              Prepared
            </label>
            <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(s.castingTime)}</span>
          </li>`;
        })
        .join("");
      groups.push(`<div class="cs-spell-group">
        <h3 class="cs-spell-group-title">${circle === 0 ? "Cantrips" : `Circle ${circle}`}</h3>
        <ul class="cs-spell-list">${rows}</ul>
      </div>`);
    }

    const counterText = tiered
      ? `Learned ${learnedLeveledCount}/${learnedCap} · Prepared ${activeLeveledCount}/${activeCap}`
      : `${label} ${activeLeveledCount}/${activeCap}`;

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-spell-modal-overlay">
      <div class="cs-modal" role="dialog" aria-modal="true" aria-label="Manage Spells">
        <div class="cs-modal-header">
          <h2>Manage Spells — ${escapeHtml(cls ? cls.name : "")}</h2>
          <button type="button" class="cs-modal-close" id="cs-spell-modal-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-sub">
          <input type="text" id="cs-spell-search" class="cs-input" placeholder="Search spells…" value="${escapeHtml(spellModalFilter)}" />
          <span class="cs-modal-counter">Cantrips ${cantripLearnedCount}/${cCap} · ${counterText}</span>
        </div>
        <div class="cs-modal-body">
          ${groups.length ? groups.join("") : '<p class="cs-muted">No spells match.</p>'}
        </div>
      </div>
    </div>`;
  }

  function renderSheet() {
    if (!el.sheet || !data || !char) return;
    const c = char;
    const cls = findClass(c);
    const sub = findSubclass(c);
    const lineage = byId(data.lineages, c.lineageId);
    const heritage = byId(data.heritages, c.heritageId);
    const background = byId(data.backgrounds, c.backgroundId);
    const maxWd = computeMaxWd(c);
    const spMax = computeSpellPowerMax(c);
    const caster = isCaster(c);
    const effSpeed = computeSpeed(c);
    const lost = heartsLost(c);
    const range = levelRange();
    const subclassMin = range.subclassMin || 2;
    const unlocked = inventoryUnlockedSlots(c);

    const classFeatures = cls ? featuresAtLevel(cls.abilities, c.level) : [];
    const subFeatures = sub ? featuresAtLevel(sub.features, c.level) : [];
    const abilitiesHtml = renderFeatureList(classFeatures) +
      (subFeatures.length ? `<h4 class="cs-subheading">${escapeHtml(sub.name)}</h4>${renderFeatureList(subFeatures)}` : "");

    const heartsHtml = [0, 1, 2].map((i) => {
      const filled = i < c.hearts;
      return `<button type="button" class="cs-heart${filled ? " is-full" : " is-empty"}" data-heart="${i}" aria-label="Heart ${i + 1}${filled ? ", remaining" : ", lost"}">${filled ? "♥" : "♡"}</button>`;
    }).join("");

    const abilityBoxes = ABILITIES.map((ab) => {
      const base = c.abilities[ab];
      const eff = effectiveMod(c, ab);
      const effHint = lost ? `<span class="cs-eff-mod" title="After ${lost} lost heart(s)">→ ${formatMod(eff)}</span>` : "";
      return `<div class="cs-stat-box">
        <span class="cs-stat-label">${ABILITY_LABELS[ab]}</span>
        ${stepper(`ability-${ab}`, base, ABILITY_LABELS[ab], { display: formatMod(base) })}
        ${effHint}
      </div>`;
    }).join("");

    const classOptions = `<option value="">— Class —</option>${data.classes
      .map((item) => `<option value="${item.id}"${c.classId === item.id ? " selected" : ""}>${escapeHtml(item.name)}</option>`)
      .join("")}`;

    const subclassList = cls ? cls.subclasses : [];
    const subclassOptions = c.level >= subclassMin
      ? `<option value="">— Subclass —</option>${subclassList
          .map((item) => `<option value="${item.id}"${c.subclassId === item.id ? " selected" : ""}>${escapeHtml(item.name)}</option>`)
          .join("")}`
      : `<option value="">Subclass at level ${subclassMin}+</option>`;

    const lineageOptions = optionList(data.lineages, c.lineageId, "Lineage");
    const heritageOptions = optionList(data.heritages, c.heritageId, "Heritage");
    const backgroundOptions = optionList(data.backgrounds, c.backgroundId, "Background");
    const armorOptions = groupedOptionList(ARMOR, c.armorId, "No Armor", armorOptionLabel);
    const weaponOptions = groupedOptionList(WEAPONS, c.weaponId, "No Weapon", weaponOptionLabel);
    const defBonus = computeDefense(c);
    const attackBonus = computeAttackBonus(c);
    const selectedArmor = byId(ARMOR, c.armorId);
    const selectedWeapon = byId(WEAPONS, c.weaponId);

    const inventoryRows = INVENTORY_THRESHOLDS.map((threshold, rowIdx) => {
      const rowOpen = rowIdx < inventoryUnlockedRows(c);
      const slots = [0, 1].map((col) => {
        const idx = rowIdx * 2 + col;
        const disabled = !rowOpen ? " disabled" : "";
        return `<input type="text" class="cs-inv-slot${rowOpen ? "" : " is-locked"}" data-inv="${idx}" value="${escapeHtml(c.inventory[idx])}" placeholder="Item"${disabled} aria-label="Inventory slot ${idx + 1}" />`;
      }).join("");
      return `<div class="cs-inv-row${rowOpen ? "" : " is-locked"}">
        <span class="cs-inv-fit" title="FIT mod needed">${formatMod(threshold)}</span>
        ${slots}
      </div>`;
    }).join("");

    const spSection = caster
      ? `<div class="cs-stat-box cs-stat-box--wide">
          <span class="cs-stat-label">Spell Power</span>
          <div class="cs-wd-row">
            <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span><span class="cs-wd-val cs-wd-val--calc">${spMax}</span></div>
            <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("sp-now", c.spellPowerNow, "Spell Power now", { min: 0, max: spMax, display: String(c.spellPowerNow) })}</div>
          </div>
        </div>`
      : "";

    el.sheet.innerHTML = `
      <div class="cs-col cs-col--stats">
        <div class="cs-field cs-field--name">
          <label class="cs-label" for="cs-name">Name</label>
          <input type="text" id="cs-name" class="cs-input cs-input--name" value="${escapeHtml(c.name)}" autocomplete="off" />
        </div>

        <div class="cs-class-row">
          <div class="cs-field">
            <label class="cs-label" for="cs-class">Class</label>
            <select id="cs-class" class="cs-select">${classOptions}</select>
          </div>
          <div class="cs-field">
            <label class="cs-label" for="cs-subclass">Subclass</label>
            <select id="cs-subclass" class="cs-select"${c.level < subclassMin ? " disabled" : ""}>${subclassOptions}</select>
          </div>
        </div>

        <div class="cs-life-level">
          <div class="cs-life">
            <span class="cs-label">Life</span>
            <div class="cs-hearts" role="group" aria-label="Life hearts">${heartsHtml}</div>
            ${stepper("hearts", c.hearts, "Hearts", { min: 0, max: 3, display: String(c.hearts) })}
            ${lost ? `<p class="cs-penalty-note">−${lost} to each ability mod, −${5 * lost} ft speed, −${2 * lost} Max WD</p>` : ""}
          </div>
          ${levelControl(c, range)}
        </div>

        <div class="cs-abilities-row">${abilityBoxes}</div>

        <div class="cs-combat-row">
          <div class="cs-stat-box cs-stat-box--wd">
            <span class="cs-stat-label">WD</span>
            <div class="cs-wd-grid">
              <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span><span class="cs-wd-val cs-wd-val--calc" title="Class ${cls ? cls.maxWd : 8} + FIT ${formatMod(effectiveMod(c, "fit"))} + level −1">${maxWd}</span></div>
              <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("wd-now", c.woundsNow, "Current wounds", { min: 0, max: maxWd, display: String(c.woundsNow) })}</div>
              <div class="cs-wd-cell"><span class="cs-wd-lbl">TMP</span>${stepper("wd-tmp", c.woundsTemp, "Temporary wounds", { min: 0, max: 999, display: String(c.woundsTemp) })}</div>
            </div>
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">DEF</span>
            <span class="cs-wd-val cs-wd-val--calc" title="Armor bonus + FIT mod (or FIT mod alone, unarmored), + shield if carried">${formatMod(defBonus)}</span>
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">Resolve</span>
            ${stepper("resolve", c.resolve, "Resolve", { min: 0, max: 4, display: String(c.resolve) })}
          </div>
        </div>

        ${spSection}

        <div class="cs-pane cs-pane--abilities">
          <h2 class="cs-pane-title">Abilities</h2>
          ${cls ? `<p class="cs-class-summary">${escapeHtml(cls.summary || "")}</p>` : '<p class="cs-muted">Choose a class to see features.</p>'}
          ${abilitiesHtml}
          ${renderSkillsLanguagesSection(c, background, heritage)}
        </div>
      </div>

      <div class="cs-col cs-col--gear">
        <div class="cs-currency">
          <div class="cs-coin"><span class="cs-coin-lbl">G</span><input type="number" min="0" class="cs-coin-input" data-coin="gold" value="${c.currency.gold}" aria-label="Gold" /></div>
          <div class="cs-coin"><span class="cs-coin-lbl">S</span><input type="number" min="0" class="cs-coin-input" data-coin="silver" value="${c.currency.silver}" aria-label="Silver" /></div>
          <div class="cs-coin"><span class="cs-coin-lbl">C</span><input type="number" min="0" class="cs-coin-input" data-coin="copper" value="${c.currency.copper}" aria-label="Copper" /></div>
        </div>

        <div class="cs-pane cs-pane--equipped">
          <h2 class="cs-pane-title">Equipped</h2>
          <div class="cs-class-row">
            <div class="cs-field">
              <label class="cs-label" for="cs-armor">Armor</label>
              <select id="cs-armor" class="cs-select">${armorOptions}</select>
              <p class="cs-props">${selectedArmor ? escapeHtml(selectedArmor.props || "—") : "—"}</p>
            </div>
            <div class="cs-field">
              <label class="cs-label" for="cs-weapon">Weapon</label>
              <select id="cs-weapon" class="cs-select">${weaponOptions}</select>
              <p class="cs-props">${selectedWeapon ? escapeHtml(selectedWeapon.props) : "—"}</p>
            </div>
          </div>
          <div class="cs-equip-summary-row">
            <label class="cs-checkbox-field">
              <input type="checkbox" id="cs-shield"${c.hasShield ? " checked" : ""} />
              Shield (+${SHIELD_BONUS} DEF)
            </label>
            ${attackBonus !== null ? `<span class="cs-atk-bonus">Attack bonus: ${formatMod(attackBonus)}</span>` : ""}
          </div>
          <textarea class="cs-textarea" id="cs-equipped" rows="3" placeholder="Other worn items, ammo, tools…">${escapeHtml(c.equippedText)}</textarea>
        </div>

        <div class="cs-pane cs-pane--inventory">
          <h2 class="cs-pane-title">Inventory <span class="cs-inv-count">${unlocked}/${INVENTORY_SLOT_COUNT} slots (FIT ${formatMod(effectiveMod(c, "fit"))})</span></h2>
          <div class="cs-inv-grid">${inventoryRows}</div>
        </div>

        ${caster ? renderSpellsPane(c, cls) : ""}
      </div>

      <div class="cs-col cs-col--identity">
        <div class="cs-field">
          <label class="cs-label" for="cs-lineage">Lineage</label>
          <select id="cs-lineage" class="cs-select">${lineageOptions}</select>
        </div>
        <div class="cs-pane cs-pane--lineage">
          <div class="cs-lineage-stats">
            <div class="cs-mini-stat"><span class="cs-mini-lbl">Speed</span><span class="cs-mini-val">${effSpeed} ft</span></div>
            <div class="cs-mini-stat"><span class="cs-mini-lbl">Size</span><span class="cs-mini-val">${escapeHtml(c.size)}</span></div>
          </div>
          ${renderDetailPaneShell(lineage?.name || "Lineage", lineage?.rulesUrl)}
        </div>

        <div class="cs-field">
          <label class="cs-label" for="cs-heritage">Heritage</label>
          <select id="cs-heritage" class="cs-select">${heritageOptions}</select>
        </div>
        <div class="cs-pane cs-pane--heritage">
          ${renderDetailPaneShell(heritage?.name || "Heritage", heritage?.rulesUrl)}
        </div>

        <div class="cs-field">
          <label class="cs-label" for="cs-background">Background</label>
          <select id="cs-background" class="cs-select">${backgroundOptions}</select>
        </div>
        <div class="cs-pane cs-pane--background">
          ${renderDetailPaneShell(background?.name || "Background", background?.rulesUrl)}
        </div>
      </div>`;
    fillDetailPanes(lineage, heritage, background);
  }

  function optionList(items, selectedId, placeholder) {
    return `<option value="">— ${placeholder} —</option>${(items || [])
      .map((item) => `<option value="${item.id}"${selectedId === item.id ? " selected" : ""}>${escapeHtml(item.name)}</option>`)
      .join("")}`;
  }

  function groupedOptionList(items, selectedId, placeholder, labelFn) {
    const groups = [];
    const byCategory = {};
    items.forEach((item) => {
      if (!byCategory[item.category]) {
        byCategory[item.category] = [];
        groups.push(item.category);
      }
      byCategory[item.category].push(item);
    });
    const optgroups = groups
      .map((cat) => {
        const opts = byCategory[cat]
          .map((item) => `<option value="${item.id}"${selectedId === item.id ? " selected" : ""}>${escapeHtml(labelFn(item))}</option>`)
          .join("");
        return `<optgroup label="${escapeHtml(cat)}">${opts}</optgroup>`;
      })
      .join("");
    return `<option value="">— ${placeholder} —</option>${optgroups}`;
  }

  function renderCharSelect() {
    if (!el.charSelect) return;
    const options = ['<option value="">— Select a character —</option>'];
    options.push(
      ...store.characters.map(
        (c) => `<option value="${c.id}"${c.id === store.activeId ? " selected" : ""}>${escapeHtml(c.name || "Unnamed")}</option>`
      )
    );
    el.charSelect.innerHTML = options.join("");
    el.charSelect.value = store.activeId || "";
  }

  function updateSheetVisibility() {
    const hasChar = Boolean(char);
    if (el.sheet) el.sheet.hidden = !hasChar;
    if (el.empty) el.empty.hidden = hasChar;
    if (el.hint) el.hint.hidden = !hasChar;
    if (el.btnDelete) el.btnDelete.disabled = !hasChar;
  }

  function render() {
    activeCharacter();
    renderCharSelect();
    updateSheetVisibility();
    renderModals();
    if (!char) {
      if (el.sheet) el.sheet.innerHTML = "";
      return;
    }
    clampWoundsAndSp();
    renderSheet();
  }

  function persistAndRender() {
    if (!char) return;
    normalizeCharacter(char);
    clampWoundsAndSp();
    saveStore();
    render();
  }

  function clampWoundsAndSp() {
    const maxWd = computeMaxWd(char);
    if (char.woundsNow > maxWd) char.woundsNow = maxWd;
    const spMax = computeSpellPowerMax(char);
    if (spMax !== null && char.spellPowerNow > spMax) char.spellPowerNow = spMax;

    const cls = findClass(char);
    const mode = spellMode(cls);
    if (mode) {
      const cCap = cantripCap(cls, char.level);
      const cantripIds = char.learnedSpellIds.filter((id) => {
        const s = spellById(id);
        return s && s.circle === 0;
      });
      if (cantripIds.length > cCap) {
        const keep = new Set(cantripIds.slice(0, cCap));
        char.learnedSpellIds = char.learnedSpellIds.filter((id) => {
          const s = spellById(id);
          return !s || s.circle > 0 || keep.has(id);
        });
      }

      const activeCap = computeActiveCap(char);
      if (usesLearnedTier(mode)) {
        const learnedCap = computeLearnedCap(char);
        const learnedLeveledIds = char.learnedSpellIds.filter((id) => {
          const s = spellById(id);
          return s && s.circle > 0;
        });
        if (learnedLeveledIds.length > learnedCap) {
          const keep = new Set(learnedLeveledIds.slice(0, learnedCap));
          char.learnedSpellIds = char.learnedSpellIds.filter((id) => {
            const s = spellById(id);
            return !s || s.circle === 0 || keep.has(id);
          });
        }
        const preparedLeveledIds = char.preparedSpellIds.filter((id) => {
          const s = spellById(id);
          return s && s.circle > 0;
        });
        if (preparedLeveledIds.length > activeCap) {
          const keep = new Set(preparedLeveledIds.slice(0, activeCap));
          char.preparedSpellIds = char.preparedSpellIds.filter((id) => {
            const s = spellById(id);
            return !s || s.circle === 0 || keep.has(id);
          });
        }
      } else {
        const activeLeveledIds = char.learnedSpellIds.filter((id) => {
          const s = spellById(id);
          return s && s.circle > 0;
        });
        if (activeLeveledIds.length > activeCap) {
          const keep = new Set(activeLeveledIds.slice(0, activeCap));
          char.learnedSpellIds = char.learnedSpellIds.filter((id) => {
            const s = spellById(id);
            return !s || s.circle === 0 || keep.has(id);
          });
        }
      }
    }
  }

  function setActive(id) {
    spellModalOpen = false;
    spellViewId = null;
    skillModalOpen = false;
    languageModalOpen = false;
    talentModalOpen = false;
    if (!id) {
      store.activeId = null;
      saveStore();
      render();
      return;
    }
    if (store.characters.some((c) => c.id === id)) {
      store.activeId = id;
      saveStore();
      render();
    }
  }

  function newCharacter() {
    spellModalOpen = false;
    spellViewId = null;
    skillModalOpen = false;
    languageModalOpen = false;
    talentModalOpen = false;
    const c = defaultCharacter();
    store.characters.push(c);
    store.activeId = c.id;
    saveStore();
    render();
  }

  function deleteCharacter() {
    if (!char) return;
    spellModalOpen = false;
    spellViewId = null;
    skillModalOpen = false;
    languageModalOpen = false;
    talentModalOpen = false;
    const name = char.name || "Unnamed";
    if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
    store.characters = store.characters.filter((c) => c.id !== char.id);
    store.activeId = store.characters.length ? store.characters[0].id : null;
    saveStore();
    render();
  }

  function importCreatorDraft() {
    try {
      const raw = localStorage.getItem(CREATOR_KEY);
      if (!raw) {
        alert("No character creator draft found in this browser.");
        return;
      }
      const draft = JSON.parse(raw);
      const c = defaultCharacter();
      c.name = draft.name || c.name;
      c.level = Number(draft.level) || 1;
      c.xp = xpThreshold(c.level);
      c.classId = draft.classId || "";
      c.subclassId = draft.subclassId || "";
      c.lineageId = draft.lineageId || "";
      c.heritageId = draft.heritageId || "";
      c.backgroundId = draft.backgroundId || "";
      if (draft.abilities) {
        ABILITIES.forEach((ab) => {
          if (draft.abilities[ab] != null) c.abilities[ab] = clampAbility(draft.abilities[ab]);
        });
      }
      if (c.lineageId) {
        const lin = byId(data.lineages, c.lineageId);
        if (lin) Object.assign(c, parseLineageDefaults(lin));
      }
      const spMax = computeSpellPowerMax(c);
      c.spellPowerNow = spMax !== null ? spMax : 0;
      store.characters.push(c);
      store.activeId = c.id;
      saveStore();
      render();
    } catch (e) {
      alert("Could not import creator draft.");
    }
  }

  function handleStepper(id, delta) {
    if (!char) return;
    if (id.startsWith("ability-")) {
      const ab = id.slice(8);
      char.abilities[ab] = clampAbility(char.abilities[ab] + delta);
      if (ab === spellcastingAbility(findClass(char))) {
        const spMax = computeSpellPowerMax(char);
        char.spellPowerNow = spMax !== null ? spMax : 0;
      }
    } else if (id === "hearts") {
      char.hearts = Math.min(3, Math.max(0, char.hearts + delta));
    } else if (id === "level") {
      const range = levelRange();
      char.level = Math.min(range.max, Math.max(range.min, char.level + delta));
      if (char.level < (range.subclassMin || 2)) char.subclassId = "";
      char.xp = xpThreshold(char.level);
    } else if (id === "wd-now") {
      char.woundsNow = Math.max(0, Math.min(computeMaxWd(char), char.woundsNow + delta));
    } else if (id === "wd-tmp") {
      char.woundsTemp = Math.max(0, char.woundsTemp + delta);
    } else if (id === "resolve") {
      char.resolve = Math.min(4, Math.max(0, char.resolve + delta));
    } else if (id === "sp-now") {
      char.spellPowerNow = Math.max(0, char.spellPowerNow + delta);
    }
    persistAndRender();
  }

  function bindEvents() {
    if (eventsBound) return;
    eventsBound = true;
    if (!el.charSelect || !el.sheet) return;
    el.charSelect.addEventListener("change", (e) => setActive(e.target.value));
    el.btnNew.addEventListener("click", newCharacter);
    el.btnDelete.addEventListener("click", deleteCharacter);
    el.btnImport.addEventListener("click", importCreatorDraft);

    el.sheet.addEventListener("click", (e) => {
      const btn = e.target.closest(".cs-stepper-btn");
      if (btn) {
        const stepperEl = btn.closest("[data-stepper]");
        const delta = parseInt(btn.dataset.delta, 10);
        handleStepper(stepperEl.dataset.stepper, delta);
        return;
      }
      const heart = e.target.closest(".cs-heart");
      if (heart && char) {
        const idx = parseInt(heart.dataset.heart, 10);
        char.hearts = idx + 1;
        persistAndRender();
        return;
      }
      if (e.target.closest("#cs-manage-spells")) {
        spellModalOpen = true;
        spellModalFilter = "";
        spellViewId = null;
        renderModals();
        return;
      }
      if (e.target.closest("#cs-choose-skills")) {
        skillModalOpen = true;
        renderModals();
        return;
      }
      if (e.target.closest("#cs-choose-languages")) {
        languageModalOpen = true;
        languageCustomDraft = "";
        renderModals();
        return;
      }
      if (e.target.closest("#cs-choose-talent")) {
        talentModalOpen = true;
        renderModals();
        return;
      }
      const chip = e.target.closest(".cs-spell-chip[data-spell-view]");
      if (chip) {
        spellViewId = chip.dataset.spellView;
        renderModals();
      }
    });

    el.sheet.addEventListener("input", (e) => {
      if (!char) return;
      const t = e.target;
      if (t.id === "cs-name") {
        char.name = t.value;
        saveStore();
        renderCharSelect();
        return;
      }
      if (t.id === "cs-equipped") {
        char.equippedText = t.value;
        saveStore();
        return;
      }
      if (t.dataset.inv != null) {
        const idx = parseInt(t.dataset.inv, 10);
        if (isSlotUnlocked(char, idx)) {
          char.inventory[idx] = t.value;
          saveStore();
        }
        return;
      }
      if (t.dataset.coin) {
        char.currency[t.dataset.coin] = Math.max(0, parseInt(t.value, 10) || 0);
        saveStore();
      }
    });

    el.sheet.addEventListener("change", (e) => {
      if (!char) return;
      const t = e.target;
      if (t.id === "cs-class") {
        char.classId = t.value;
        char.subclassId = "";
        const spMax = computeSpellPowerMax(char);
        char.spellPowerNow = spMax !== null ? spMax : 0;
        persistAndRender();
      } else if (t.id === "cs-subclass") {
        char.subclassId = t.value;
        persistAndRender();
      } else if (t.id === "cs-lineage") {
        char.lineageId = t.value;
        const lin = byId(data.lineages, t.value);
        if (lin) Object.assign(char, parseLineageDefaults(lin));
        persistAndRender();
      } else if (t.id === "cs-heritage") {
        char.heritageId = t.value;
        char.chosenLanguages = [];
        persistAndRender();
      } else if (t.id === "cs-background") {
        char.backgroundId = t.value;
        char.chosenSkills = [];
        char.chosenTalents = [];
        persistAndRender();
      } else if (t.id === "cs-armor") {
        char.armorId = t.value;
        persistAndRender();
      } else if (t.id === "cs-weapon") {
        char.weaponId = t.value;
        persistAndRender();
      } else if (t.id === "cs-shield") {
        char.hasShield = t.checked;
        persistAndRender();
      } else if (t.id === "cs-xp") {
        const range = levelRange();
        char.xp = Math.max(0, parseInt(t.value, 10) || 0);
        char.level = levelFromXp(char.xp, range);
        if (char.level < (range.subclassMin || 2)) char.subclassId = "";
        persistAndRender();
      }
    });

    if (el.modalRoot) {
      el.modalRoot.addEventListener("click", (e) => {
        if (e.target.id === "cs-spell-modal-overlay" || e.target.id === "cs-spell-modal-close") {
          spellModalOpen = false;
          renderModals();
        } else if (e.target.id === "cs-spell-view-overlay" || e.target.id === "cs-spell-view-close") {
          spellViewId = null;
          renderModals();
        } else if (e.target.id === "cs-choice-modal-overlay" || e.target.id === "cs-choice-modal-close") {
          skillModalOpen = false;
          languageModalOpen = false;
          talentModalOpen = false;
          renderModals();
        } else if (e.target.dataset.languageRemove) {
          const lang = e.target.dataset.languageRemove;
          char.chosenLanguages = char.chosenLanguages.filter((l) => l !== lang);
          persistAndRender();
        } else if (e.target.id === "cs-language-add") {
          const heritage = byId(data.heritages, char.heritageId);
          const choice = parseHeritageLanguageChoice(heritage);
          const name = languageCustomDraft.trim();
          if (name && choice && char.chosenLanguages.length < choice.count && !char.chosenLanguages.includes(name)) {
            char.chosenLanguages.push(name);
            languageCustomDraft = "";
            persistAndRender();
          }
        }
      });

      el.modalRoot.addEventListener("input", (e) => {
        if (e.target.id === "cs-spell-search") {
          spellModalFilter = e.target.value;
          renderModals();
          const input = document.getElementById("cs-spell-search");
          if (input) {
            input.focus();
            const pos = spellModalFilter.length;
            input.setSelectionRange(pos, pos);
          }
        } else if (e.target.id === "cs-language-custom") {
          languageCustomDraft = e.target.value;
        }
      });

      el.modalRoot.addEventListener("change", (e) => {
        if (!char) return;
        const t = e.target;
        if (t.dataset.spellLearn) {
          const id = t.dataset.spellLearn;
          if (t.checked) {
            if (!char.learnedSpellIds.includes(id)) char.learnedSpellIds.push(id);
          } else {
            char.learnedSpellIds = char.learnedSpellIds.filter((x) => x !== id);
            char.preparedSpellIds = char.preparedSpellIds.filter((x) => x !== id);
          }
          persistAndRender();
        } else if (t.dataset.spellPrepare) {
          const id = t.dataset.spellPrepare;
          if (t.checked) {
            if (!char.preparedSpellIds.includes(id)) char.preparedSpellIds.push(id);
          } else {
            char.preparedSpellIds = char.preparedSpellIds.filter((x) => x !== id);
          }
          persistAndRender();
        } else if (t.dataset.skillOption) {
          const skill = t.dataset.skillOption;
          if (t.checked) {
            if (!char.chosenSkills.includes(skill)) char.chosenSkills.push(skill);
          } else {
            char.chosenSkills = char.chosenSkills.filter((s) => s !== skill);
          }
          persistAndRender();
        } else if (t.dataset.languageOption) {
          const lang = t.dataset.languageOption;
          if (t.checked) {
            if (!char.chosenLanguages.includes(lang)) char.chosenLanguages.push(lang);
          } else {
            char.chosenLanguages = char.chosenLanguages.filter((l) => l !== lang);
          }
          persistAndRender();
        } else if (t.dataset.talentOption) {
          char.chosenTalents = [t.dataset.talentOption];
          persistAndRender();
        }
      });

      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && (spellModalOpen || spellViewId || skillModalOpen || languageModalOpen || talentModalOpen)) {
          spellModalOpen = false;
          spellViewId = null;
          skillModalOpen = false;
          languageModalOpen = false;
          talentModalOpen = false;
          renderModals();
        }
      });
    }
  }

  async function init() {
    cacheElements();
    if (!el.loading || !el.app || !el.sheet) {
      showLoadError("Character sheet UI failed to load. Try refreshing the page.");
      return;
    }

    try {
      const res = await fetch(rp("assets/character-creator-data.json"));
      if (!res.ok) throw new Error("Could not load character options (HTTP " + res.status + ").");
      data = await res.json();
      if (!data || !Array.isArray(data.classes)) {
        throw new Error("Character options file is invalid. Regenerate it with generate-character-creator-data.py.");
      }
      try {
        const spellsRes = await fetch(rp("assets/spells-data.json"));
        SPELLS = spellsRes.ok ? await spellsRes.json() : [];
      } catch (_) {
        SPELLS = [];
      }
      showApp();
      bindEvents();
      try {
        render();
      } catch (renderErr) {
        console.error(renderErr);
        throw new Error("Character sheet failed to render. Try clearing saved data or refreshing.");
      }
    } catch (err) {
      console.error(err);
      const hint = window.location.protocol === "file:"
        ? " Open this site through a local web server (for example: python -m http.server) instead of the file:// URL."
        : "";
      showLoadError((err && err.message ? err.message : "Could not load character options.") + hint);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
