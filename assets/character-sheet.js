/**
 * YMIAT Character Sheet — local character management.
 * Options from assets/character-creator-data.json; persistence in localStorage.
 */
(function () {
  const STORAGE_KEY = "ymiat-characters-v1";
  const ABILITIES = ["fit", "ins", "wil"];
  const ABILITY_LABELS = { fit: "FIT", ins: "INS", wil: "WIL" };
  const ABILITY_FULL = { fit: "Fitness", ins: "Insight", wil: "Willpower" };
  // YMIAT skill → ability (3-score model). Used for pregen-format PDF export.
  const SKILL_ABILITY = {
    Athletics: "fit",
    Acrobatics: "fit",
    "Sleight of Hand": "fit",
    Stealth: "fit",
    "Animal Handling": "ins",
    Arcana: "ins",
    History: "ins",
    Insight: "ins",
    Investigation: "ins",
    Medicine: "ins",
    Nature: "ins",
    Perception: "ins",
    Religion: "ins",
    Survival: "ins",
    Deception: "wil",
    Intimidation: "wil",
    Performance: "wil",
    Persuasion: "wil",
  };

  function t(key, fallback) {
    const pack = (window.ymiatAppStrings && window.ymiatAppStrings("sheet")) || {};
    return pack[key] != null && pack[key] !== "" ? pack[key] : fallback;
  }
  const WEAPON_SLOT_COUNT = 5;
  // True while an empty “choose weapon” row is shown after + Add weapon.
  let weaponPickPending = false;

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

  // Attack bonus per gear.html weapon tables: weapon bonus + FIT mod (+ PB when proficient).
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
  let TALENTS = [];
  let store = loadStore();
  let char = null;
  let eventsBound = false;
  let spellModalOpen = false;
  let spellModalFilter = "";
  const spellModalExpandedIds = new Set();
  let spellViewId = null;
  let talentViewName = null;
  let skillModalOpen = false;
  let languageModalOpen = false;
  let talentModalOpen = false;
  let ddbModalOpen = false;
  let ddbReview = null; // { name, lines } after import, shown as in-app modal
  let ddbFallbackVisible = false;
  let portraitClearOpen = false;
  const talentModalExpandedIds = new Set();

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
    el.btnCreator = document.getElementById("cs-btn-creator");
    el.btnImportDdb = document.getElementById("cs-btn-import-ddb");
    el.btnPrint = document.getElementById("cs-btn-print");
    el.btnExportPdf = document.getElementById("cs-btn-export-pdf");
    el.printOrientation = document.getElementById("cs-print-orientation");
    el.btnDelete = document.getElementById("cs-btn-delete");
    el.modalRoot = document.getElementById("cs-modal-root");
    el.toolbar = document.getElementById("cs-toolbar");
    el.toolbarToggle = document.getElementById("cs-toolbar-toggle");
    el.pgExport = document.getElementById("cs-pg-export");
  }

  // Overrides the static @page rule in character-sheet.html by appending a
  // later style at the end of <head>. Interactive Print uses 1cm margins;
  // Export PDF uses landscape + 8mm to match pregenerated sheets.
  function applyPrintOrientation(orientation, options) {
    let styleEl = document.getElementById("cs-print-orientation-style");
    if (!styleEl) {
      styleEl = document.createElement("style");
      styleEl.id = "cs-print-orientation-style";
    }
    // Always move to end of head so this @page wins over page/inline rules.
    document.head.appendChild(styleEl);
    const margin = (options && options.margin) || "1cm";
    const size = orientation === "portrait" ? "portrait" : "landscape";
    styleEl.textContent = `@media print { @page { size: A4 ${size}; margin: ${margin}; } }`;
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

  function assetsPath() {
    if (typeof window.ymiatGetAssetsPath === "function") {
      return window.ymiatGetAssetsPath();
    }
    return rootPath();
  }

  function rp(url) {
    if (!url || url.startsWith("http")) return url;
    if (url.startsWith("assets/")) return assetsPath() + url;
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
      grantedSpellIds: [],
      grantedSpellChoices: {},
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
      weaponIds: [],
      speed: 30,
      size: "Medium",
      currency: { gold: 0, silver: 0, copper: 0 },
      equippedText: "",
      portraitUrl: "",
      inventoryText: "",
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
    c.abilities = c.abilities || { fit: 0, ins: 0, wil: 0 };
    ABILITIES.forEach((a) => {
      c.abilities[a] = clampAbility(Number(c.abilities[a]) || 0);
    });
    c.resolve = Math.min(resolveMax(c), Math.max(0, Number(c.resolve) || 0));
    c.woundsNow = Math.max(0, Number(c.woundsNow) || 0);
    c.woundsTemp = Math.max(0, Number(c.woundsTemp) || 0);
    c.armorId = typeof c.armorId === "string" ? c.armorId : "";
    c.hasShield = Boolean(c.hasShield);
    c.weaponId = typeof c.weaponId === "string" ? c.weaponId : "";
    normalizeWeaponIds(c);
    c.spellPowerNow = Math.max(0, Number(c.spellPowerNow) || 0);
    c.learnedSpellIds = Array.isArray(c.learnedSpellIds)
      ? [...new Set(c.learnedSpellIds.filter((id) => typeof id === "string"))]
      : [];
    c.preparedSpellIds = Array.isArray(c.preparedSpellIds)
      ? [...new Set(c.preparedSpellIds.filter((id) => typeof id === "string"))].filter((id) => c.learnedSpellIds.includes(id))
      : [];
    c.grantedSpellChoices =
      c.grantedSpellChoices && typeof c.grantedSpellChoices === "object" && !Array.isArray(c.grantedSpellChoices)
        ? { ...c.grantedSpellChoices }
        : {};
    c.grantedSpellIds = Array.isArray(c.grantedSpellIds)
      ? [...new Set(c.grantedSpellIds.filter((id) => typeof id === "string"))]
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
    c.portraitUrl = normalizePortrait(c.portraitUrl);
    // Older sheets stored a fixed slot array. Fold non-empty lines into inventoryText once.
    if (Array.isArray(c.inventory)) {
      const lines = c.inventory.map((s) => String(s || "").trim()).filter(Boolean);
      if (!String(c.inventoryText || "").trim() && lines.length) {
        c.inventoryText = lines.join("\n");
      }
      delete c.inventory;
    }
    c.inventoryText = c.inventoryText == null ? "" : String(c.inventoryText);
    return c;
  }

  function saveStore() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    try {
      window.dispatchEvent(new CustomEvent("ymiat-characters-changed"));
    } catch (_) { /* ignore */ }
    if (typeof window.ymiatRefreshNavCharacters === "function") {
      window.ymiatRefreshNavCharacters();
    }
  }

  let playMode = false;
  let manageDocumentTitle = "";

  function syncDocumentTitle() {
    if (!manageDocumentTitle) {
      manageDocumentTitle = document.title || "Character Manager | You-Meet-In-A-Tavern (YMIAT)";
    }
    if (!playMode) {
      document.title = manageDocumentTitle;
      return;
    }
    const c = activeCharacter();
    const name = (c && String(c.name || "").trim()) || "Unnamed";
    document.title = name + " | You-Meet-In-A-Tavern (YMIAT)";
  }

  function applySheetModeFromUrl() {
    let params;
    try {
      params = new URLSearchParams(window.location.search || "");
    } catch (_) {
      playMode = false;
      document.body.classList.remove("cs-mode-play");
      syncDocumentTitle();
      return;
    }
    // DDB import wins — keep manage chrome.
    if (params.get("ddb")) {
      playMode = false;
      document.body.classList.remove("cs-mode-play");
      syncDocumentTitle();
      return;
    }
    const playId = params.get("id");
    if (!playId) {
      playMode = false;
      document.body.classList.remove("cs-mode-play");
      syncDocumentTitle();
      return;
    }
    if (store.characters.some((c) => c.id === playId)) {
      playMode = true;
      document.body.classList.add("cs-mode-play");
      store.activeId = playId;
      saveStore();
    } else {
      playMode = false;
      document.body.classList.remove("cs-mode-play");
      try {
        history.replaceState(null, "", window.location.pathname + window.location.hash);
      } catch (_) { /* ignore */ }
    }
    syncDocumentTitle();
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
  // of a descriptive hint - those just leave options empty; the language
  // dropdown (built from ALL_LANGUAGES) still covers picking a real one.
  // Standard set per 5e SRD (Common is granted separately, not listed here).
  const ALL_LANGUAGES = [
    "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orcish",
    "Abyssal", "Celestial", "Deep Speech", "Draconic", "Infernal", "Primordial", "Sylvan", "Undercommon",
  ];

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

  // XP threshold per core.html#experience-points: 100 * (level - 1) * level / 2.
  function xpThreshold(level) {
    const n = Math.max(0, level - 1);
    return (n * level * 100) / 2;
  }

  function levelFromXp(xp, range) {
    const total = Math.max(0, Number(xp) || 0);
    let level = range.min;
    for (let L = range.min; L <= range.max; L++) {
      if (xpThreshold(L) <= total) level = L;
      else break;
    }
    return level;
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

  function resolveMax(c) {
    return 4 + Math.ceil(effectiveMod(c, "wil") / 2);
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

  /** "Spellcasting: Willpower (WIL +2)" or null for non-casters. */
  function formatSpellcastingLine(c) {
    const cls = findClass(c);
    const ab = spellcastingAbility(cls);
    if (!ab) return null;
    const full = ABILITY_FULL[ab] || ab;
    const code = ABILITY_LABELS[ab] || String(ab).toUpperCase();
    const mod = formatMod(effectiveMod(c, ab));
    return "Spellcasting: " + full + " (" + code + " " + mod + ")";
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
    return Math.max(0, 2 + 2 * mod);
  }

  // Proficiency Bonus per core.html#proficiency-and-advantage: PB = level / 2, rounded up.
  function computePB(c) {
    return Math.ceil(c.level / 2);
  }

  // Max spell level by character level, per classes.html progression tables.
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
  // Max Spell Level, not counts) — those are derived from the matching 5e SRD
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
  // spellbook but is stated outright (6 spells at 1st level, +2/level).
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

  function talentByName(name) {
    return TALENTS.find((t) => t.name === name) || null;
  }

  function eligibleSpells(c) {
    const cls = findClass(c);
    if (!cls) return [];
    const maxCircle = maxSpellCircle(cls, c.level);
    return SPELLS.filter((s) => s.classes.includes(cls.id) && s.circle <= maxCircle);
  }

  // Bonus spells from lineage/heritage/background — outside class caps.
  // Fixed grants resolve immediately; choice/legacy grants need grantedSpellChoices.
  // Missing SPELLS ids are skipped (not invented).
  const TIEFLING_LEGACY_BRANCHES = {
    abyssal: { label: "Abyssal", cantrip: "poison-spray", level3: "ray-of-sickness", level5: "hold-person" },
    chthonic: { label: "Chthonic", cantrip: "chill-touch", level3: "false-life", level5: "ray-of-enfeeblement" },
    infernal: { label: "Infernal", cantrip: "firebolt", level3: "hellish-rebuke", level5: "darkness" },
  };

  const GRANT_DEFS = [
    {
      key: "anointed-favored-disciple",
      sourceType: "heritage",
      sourceId: "anointed",
      label: "Favored Disciple",
      kind: "fixed",
      spellIds: ["thaumaturgy"],
    },
    {
      key: "fireforge-forgecraft",
      sourceType: "heritage",
      sourceId: "fireforge",
      label: "Forgecraft",
      kind: "fixed",
      spellIds: ["mending"],
    },
    {
      key: "feysworn-trickery",
      sourceType: "heritage",
      sourceId: "feysworn",
      label: "Accustomed to Trickery",
      kind: "fixed",
      spellIds: ["prestidigitation"],
    },
    {
      key: "kithren-search-rescue",
      sourceType: "heritage",
      sourceId: "kithren",
      label: "Search and Rescue",
      kind: "fixed",
      spellIds: ["mending"],
    },
    {
      key: "cloud-cantrip",
      sourceType: "heritage",
      sourceId: "cloud",
      label: "Touch of Magic",
      kind: "choice",
      choiceLabel: "Cantrip",
      filter: { circle: 0 },
    },
    {
      key: "cloud-circle1",
      sourceType: "heritage",
      sourceId: "cloud",
      label: "Touch of Magic",
      kind: "choice",
      choiceLabel: "Spell Level 1",
      minLevel: 3,
      filter: { circle: 1 },
    },
    {
      key: "covenant-cantrip",
      sourceType: "heritage",
      sourceId: "covenant",
      label: "Expert Caster",
      kind: "choice",
      choiceLabel: "Cantrip",
      filter: { circle: 0 },
    },
    {
      key: "tiefling-legacy",
      sourceType: "lineage",
      sourceId: "tiefling",
      label: "Fiendish Legacy",
      kind: "legacy",
      branches: TIEFLING_LEGACY_BRANCHES,
    },
  ];

  function grantSourceMatches(c, def) {
    if (!c || !def) return false;
    if (def.sourceType === "heritage") return c.heritageId === def.sourceId;
    if (def.sourceType === "lineage") return c.lineageId === def.sourceId;
    if (def.sourceType === "background") return c.backgroundId === def.sourceId;
    return false;
  }

  function grantSourceTag(sourceType) {
    if (sourceType === "heritage") return t("heritage", "Heritage");
    if (sourceType === "lineage") return t("lineage", "Lineage");
    if (sourceType === "background") return t("background", "Background");
    return t("granted", "Granted");
  }

  function grantChoiceOptions(def) {
    if (!def || def.kind !== "choice" || !def.filter) return [];
    const circle = def.filter.circle;
    return SPELLS.filter((s) => s.circle === circle).sort((a, b) => a.name.localeCompare(b.name));
  }

  function resolveLegacySpellIds(def, branchKey, level) {
    const branch = def.branches && def.branches[branchKey];
    if (!branch) return [];
    const ids = [];
    if (branch.cantrip) ids.push(branch.cantrip);
    if (level >= 3 && branch.level3) ids.push(branch.level3);
    if (level >= 5 && branch.level5) ids.push(branch.level5);
    return ids.filter((id) => Boolean(spellById(id)));
  }

  function activeGrantDefs(c) {
    const level = Number(c && c.level) || 1;
    return GRANT_DEFS.filter((def) => {
      if (!grantSourceMatches(c, def)) return false;
      if (def.minLevel && level < def.minLevel) return false;
      return true;
    });
  }

  /**
   * Rebuild grantedSpellIds from catalog + choices; drop stale choice keys.
   * Never invents spell ids — missing SPELLS entries are skipped.
   */
  function syncGrantedSpells(c) {
    if (!c) return;
    const choices =
      c.grantedSpellChoices && typeof c.grantedSpellChoices === "object" && !Array.isArray(c.grantedSpellChoices)
        ? c.grantedSpellChoices
        : {};
    c.grantedSpellChoices = choices;

    const activeKeys = new Set();
    const ids = [];
    const metaById = {};

    activeGrantDefs(c).forEach((def) => {
      activeKeys.add(def.key);
      let resolved = [];
      if (def.kind === "fixed") {
        resolved = (def.spellIds || []).filter((id) => Boolean(spellById(id)));
      } else if (def.kind === "choice") {
        const pick = choices[def.key];
        if (typeof pick === "string" && pick && spellById(pick)) {
          const opts = grantChoiceOptions(def);
          if (opts.some((s) => s.id === pick)) resolved = [pick];
        }
      } else if (def.kind === "legacy") {
        const branch = choices[def.key];
        if (typeof branch === "string" && def.branches && def.branches[branch]) {
          resolved = resolveLegacySpellIds(def, branch, Number(c.level) || 1);
        }
      }
      resolved.forEach((id) => {
        if (!ids.includes(id)) ids.push(id);
        metaById[id] = { sourceType: def.sourceType, label: def.label, key: def.key };
      });
    });

    Object.keys(choices).forEach((key) => {
      if (!activeKeys.has(key)) delete choices[key];
    });

    c.grantedSpellIds = ids;
    c._grantedSpellMeta = metaById;
  }

  function isGrantedSpellId(c, id) {
    return Boolean(c && Array.isArray(c.grantedSpellIds) && c.grantedSpellIds.includes(id));
  }

  function grantedSpellMeta(c, id) {
    if (!c) return null;
    if (c._grantedSpellMeta && c._grantedSpellMeta[id]) return c._grantedSpellMeta[id];
    syncGrantedSpells(c);
    return (c._grantedSpellMeta && c._grantedSpellMeta[id]) || null;
  }

  function hasBonusSpellUi(c) {
    if (!c) return false;
    syncGrantedSpells(c);
    if ((c.grantedSpellIds || []).length) return true;
    return activeGrantDefs(c).some((def) => def.kind === "choice" || def.kind === "legacy");
  }

  function countClassCantrips(c) {
    return (c.learnedSpellIds || []).filter((id) => {
      if (isGrantedSpellId(c, id)) return false;
      const s = spellById(id);
      return s && s.circle === 0;
    }).length;
  }

  function countClassLeveledLearned(c) {
    return (c.learnedSpellIds || []).filter((id) => {
      if (isGrantedSpellId(c, id)) return false;
      const s = spellById(id);
      return s && s.circle > 0;
    }).length;
  }

  function countClassLeveledPrepared(c) {
    return (c.preparedSpellIds || []).filter((id) => {
      if (isGrantedSpellId(c, id)) return false;
      const s = spellById(id);
      return s && s.circle > 0;
    }).length;
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

  function normalizeWeaponIds(c) {
    let ids = Array.isArray(c.weaponIds)
      ? c.weaponIds.filter((id) => typeof id === "string")
      : [];
    if (!ids.some(Boolean) && c.weaponId) ids = [c.weaponId];
    const filled = ids
      .map((id) => (id && byId(WEAPONS, id) ? id : ""))
      .filter(Boolean)
      .slice(0, WEAPON_SLOT_COUNT);
    c.weaponIds = filled;
    if (weaponPickPending && c.weaponIds.length < WEAPON_SLOT_COUNT) {
      c.weaponIds.push("");
    } else {
      weaponPickPending = false;
    }
    c.weaponId = c.weaponIds.find(Boolean) || "";
  }

  function activeWeaponRowIds(c) {
    return Array.isArray(c.weaponIds) ? c.weaponIds.slice() : [];
  }

  function canAddWeaponRow(c) {
    const rows = activeWeaponRowIds(c);
    if (rows.length >= WEAPON_SLOT_COUNT) return false;
    if (rows.length && !rows[rows.length - 1]) return false; // already picking
    return true;
  }

  function addWeaponRow(c) {
    if (!c || !canAddWeaponRow(c)) return false;
    normalizeWeaponIds(c);
    if (c.weaponIds.length >= WEAPON_SLOT_COUNT) return false;
    weaponPickPending = true;
    c.weaponIds.push("");
    return true;
  }

  // Attack bonus per gear.html: weapon table bonus + FIT mod.
  // When proficient with the weapon, also add Proficiency Bonus (PB).
  function computeAttackBonusForWeaponId(c, weaponId) {
    const weapon = byId(WEAPONS, weaponId);
    if (!weapon) return null;
    let total = effectiveMod(c, "fit") + weapon.bonus;
    if (isWeaponProficient(c, weaponId)) total += computePB(c);
    return total;
  }

  function computeAttackBonus(c) {
    return computeAttackBonusForWeaponId(c, c.weaponId);
  }

  function attackBonusBreakdownTitle(c, weaponId) {
    const weapon = byId(WEAPONS, weaponId);
    if (!weapon) return "";
    const fit = effectiveMod(c, "fit");
    const parts = [`FIT ${formatMod(fit)}`, `weapon ${formatMod(weapon.bonus)}`];
    if (isWeaponProficient(c, weaponId)) parts.push(`PB ${formatMod(computePB(c))}`);
    return parts.join(" + ");
  }

  function computeSpeed(c) {
    const base = Number(c.speed) || 30;
    return Math.max(0, base + heartPenalties(c).speed);
  }

  function featuresAtLevel(items, level) {
    if (!items || !items.length) return [];
    return items.filter((item) => (item.minLevel || 1) <= level);
  }

  function skillAbility(name) {
    return SKILL_ABILITY[name] || "ins";
  }

  function deriveProficiencyLines(cls) {
    const combat = parseClassCombatProficiency(cls);
    if (combat.lines && combat.lines.length) return combat.lines.slice();
    if (!cls || !cls.proficiencies) return [];
    const text = String(cls.proficiencies).replace(/\s*Skills?:[\s\S]*$/i, "").trim();
    if (!text) return [];
    return text
      .split(/,\s*/)
      .map((s) => s.replace(/\.$/, "").trim())
      .filter(Boolean);
  }

  const ARMOR_STEP_LABELS = { 0: "None", 1: "Light", 2: "Medium", 3: "Heavy" };

  function armorCategoryStep(category) {
    const c = String(category || "").toLowerCase();
    if (c.includes("heavy")) return 3;
    if (c.includes("medium")) return 2;
    if (c.includes("light")) return 1;
    return 0;
  }

  /**
   * Parse class.proficiencies into structured combat proficiency.
   * Skills clause is ignored; subclass grants are not included (v1).
   */
  function parseClassCombatProficiency(cls) {
    const empty = {
      armorStep: 0,
      shields: false,
      weaponSummary: "",
      weaponFlags: { all: false, simple: false, martial: false, martialFinesseOnly: false, shortswords: false },
      lines: [],
      armorLabel: "None",
    };
    if (!cls || !cls.proficiencies) return empty;
    const combatText = String(cls.proficiencies).replace(/\s*Skills?:[\s\S]*$/i, "").trim().replace(/\.$/, "");
    if (!combatText) return empty;
    const lower = combatText.toLowerCase();

    let armorStep = 0;
    if (/\bno armor\b/.test(lower)) {
      armorStep = 0;
    } else if (/\ball armor\b/.test(lower)) {
      armorStep = 3;
    } else if (/\bheavy\b/.test(lower) && /\barmor\b/.test(lower)) {
      armorStep = 3;
    } else if (/\blight and medium armor\b/.test(lower) || /\bmedium armor\b/.test(lower)) {
      armorStep = 2;
    } else if (/\blight armor\b/.test(lower)) {
      armorStep = 1;
    }

    const shields = /\bshields?\b/.test(lower);

    const weaponFlags = {
      all: false,
      simple: false,
      martial: false,
      martialFinesseOnly: false,
      shortswords: false,
    };
    // Phrases like "simple and martial finesse weapons" (Rogue) must grant
    // simple weapons — not only the martial-finesse half.
    if (/\ball weapons\b/.test(lower) || /\bsimple and martial weapons\b/.test(lower)) {
      weaponFlags.all = true;
      weaponFlags.simple = true;
      weaponFlags.martial = true;
    } else {
      if (
        /\bsimple weapons\b/.test(lower) ||
        /\bsimple and martial\b/.test(lower) ||
        /\bsimple melee\b/.test(lower) ||
        /\bsimple ranged\b/.test(lower)
      ) {
        weaponFlags.simple = true;
      }
      if (/\bmartial finesse weapons\b/.test(lower)) {
        weaponFlags.martialFinesseOnly = true;
        weaponFlags.martial = true;
      } else if (/\bmartial weapons\b/.test(lower)) {
        weaponFlags.martial = true;
      }
      if (/\bshortswords?\b/.test(lower)) weaponFlags.shortswords = true;
    }

    const parts = combatText
      .split(/;\s*|,\s*/)
      .map((s) => s.replace(/\.$/, "").trim())
      .filter(Boolean);
    const weaponParts = parts.filter((p) => {
      const l = p.toLowerCase();
      if (/\barmor\b/.test(l) || /\bshields?\b/.test(l) || /\bno armor\b/.test(l)) return false;
      if (/\btools?\b/.test(l) || /\binstrument/.test(l) || /\bskills?\b/.test(l)) return false;
      return /\bweapon/.test(l) || /\bshortsword/.test(l) || /\bfinesse/.test(l);
    });
    const weaponSummary = weaponParts.length
      ? weaponParts.join("; ")
      : weaponFlags.all
        ? "Simple and martial weapons"
        : "";

    const lines = [];
    if (armorStep >= 3) lines.push("All armor");
    else if (armorStep === 2) lines.push("Light and medium armor");
    else if (armorStep === 1) lines.push("Light armor");
    else lines.push("No armor");
    if (shields) lines.push("Shields");
    if (weaponSummary) lines.push(weaponSummary);

    return {
      armorStep: armorStep,
      shields: shields,
      weaponSummary: weaponSummary,
      weaponFlags: weaponFlags,
      lines: lines,
      armorLabel: ARMOR_STEP_LABELS[armorStep] || "None",
    };
  }

  function wornArmorStep(c) {
    const armor = byId(ARMOR, c && c.armorId);
    if (!armor) return 0;
    return armorCategoryStep(armor.category);
  }

  function armorProficiencyGap(c) {
    const cls = findClass(c);
    const prof = parseClassCombatProficiency(cls);
    const worn = wornArmorStep(c);
    return Math.max(0, worn - prof.armorStep);
  }

  function isWeaponProficient(c, weaponId) {
    const weapon = byId(WEAPONS, weaponId);
    if (!weapon) return null;
    const prof = parseClassCombatProficiency(findClass(c));
    const flags = prof.weaponFlags || {};
    if (flags.all) return true;
    const cat = String(weapon.category || "").toLowerCase();
    const isSimple = cat.includes("simple");
    const isMartial = cat.includes("martial");
    if (isSimple && flags.simple) return true;
    if (weapon.id === "shortsword" && flags.shortswords) return true;
    if (isMartial && flags.martial) {
      if (flags.martialFinesseOnly) {
        return /\bfinesse\b/i.test(weapon.props || "");
      }
      return true;
    }
    return false;
  }

  function formatArmorWarning(c) {
    const gap = armorProficiencyGap(c);
    if (gap <= 0) return "";
    const armor = byId(ARMOR, c.armorId);
    const prof = parseClassCombatProficiency(findClass(c));
    const langNl = sheetLocale() === "nl";
    const stepsWord = gap === 1 ? (langNl ? "stap" : "step") : langNl ? "stappen" : "steps";
    const dice = gap + 1;
    if (langNl) {
      return (
        "Niet proficient met " +
        (armor ? armor.name : "dit pantser") +
        " (" +
        gap +
        " " +
        stepsWord +
        " boven " +
        (prof.armorLabel || "None") +
        "). Stapelend nadeel: rol " +
        dice +
        "d20, neem de laagste op alle d20-rollen; nadeel op Fitness-tests, Verdedigingsrollen en spellcasting-rollen."
      );
    }
    return (
      "Not proficient with " +
      (armor ? armor.name : "this armor") +
      " (" +
      gap +
      " " +
      stepsWord +
      " above " +
      (prof.armorLabel || "None") +
      "). Stacking disadvantage: roll " +
      dice +
      "d20, take lowest on all d20 rolls; disadvantage on Fitness checks, Defense rolls, and spellcasting rolls."
    );
  }

  function renderCombatProficiencyBlock(c, cls) {
    const prof = parseClassCombatProficiency(cls);
    if (!cls) {
      return `<div class="cs-prof-block">
        <h3 class="cs-spell-group-sheet-title">${escapeHtml(t("armorWeapons", "Armor & weapons"))}</h3>
        <p class="cs-muted">${escapeHtml(t("chooseClassProf", "Choose a class to see armor and weapon proficiencies."))}</p>
      </div>`;
    }
    const armorCats = [];
    if (prof.armorStep >= 1) armorCats.push("Light");
    if (prof.armorStep >= 2) armorCats.push("Medium");
    if (prof.armorStep >= 3) armorCats.push("Heavy");
    const armorText = armorCats.length ? armorCats.join(", ") : "None";
    const shieldText = prof.shields ? t("yes", "Yes") : t("no", "No");
    const weaponsText = prof.weaponSummary || "—";
    const coreHref = rp(sheetLocale() === "nl" ? "nl/rules/core.html#armor-proficiency" : "rules/core.html#armor-proficiency");
    return `<div class="cs-prof-block">
      <h3 class="cs-spell-group-sheet-title">${escapeHtml(t("armorWeapons", "Armor & weapons"))} <span class="cs-muted">(${escapeHtml(t("fromClass", "from Class"))})</span></h3>
      <ul class="cs-prof-list">
        <li><strong>${escapeHtml(t("armor", "Armor"))}:</strong> ${escapeHtml(armorText)}</li>
        <li><strong>${escapeHtml(t("shield", "Shield"))}:</strong> ${escapeHtml(shieldText)}</li>
        <li><strong>${escapeHtml(t("weapons", "Weapons"))}:</strong> ${escapeHtml(weaponsText)}</li>
      </ul>
      <p class="cs-hint"><a href="${escapeHtml(coreHref)}" target="_blank" rel="noopener">${escapeHtml(t("armorProfRules", "Armor proficiency rules"))}</a></p>
    </div>`;
  }

  function renderArmorProficiencyWarning(c) {
    const gap = armorProficiencyGap(c);
    if (gap <= 0) return "";
    const warn = formatArmorWarning(c);
    const coreHref = rp(sheetLocale() === "nl" ? "nl/rules/core.html#armor-proficiency" : "rules/core.html#armor-proficiency");
    const dice = gap + 1;
    return `<div class="cs-armor-warn" role="status">
      <p class="cs-armor-warn-title"><span class="cs-armor-warn-tag">${escapeHtml(t("notProficient", "Not proficient"))}</span> ${gap} ${escapeHtml(gap === 1 ? t("stepAbove", "step above training") : t("stepsAbove", "steps above training"))}</p>
      <ul class="cs-armor-warn-list">
        <li>${escapeHtml(t("stackingDisadv", "Stacking disadvantage"))}: ${dice}d20 ${escapeHtml(t("takeLowest", "take lowest"))} ${escapeHtml(t("onAllD20", "on all d20 rolls"))}</li>
        <li>${escapeHtml(t("disadvFitness", "Disadvantage on Fitness checks"))}</li>
        <li>${escapeHtml(t("disadvDefense", "Disadvantage on Defense rolls"))}</li>
        <li>${escapeHtml(t("disadvSpellcasting", "Disadvantage on spellcasting rolls"))}</li>
      </ul>
      <p class="cs-hint"><a href="${escapeHtml(coreHref)}" target="_blank" rel="noopener">${escapeHtml(t("fullArmorRules", "Full rules"))}</a> · ${escapeHtml(warn)}</p>
    </div>`;
  }

  /** Parse lineage HTML body into { name, text } trait lines for PDF Person block. */
  function parseLineageTraits(lineage) {
    if (!lineage || !lineage.body) return [];
    const traits = [];
    const re = /<p>\s*<strong>([^<]+)<\/strong>\s*([\s\S]*?)<\/p>/gi;
    let m;
    while ((m = re.exec(lineage.body))) {
      const name = String(m[1] || "").replace(/\.$/, "").trim();
      const text = String(m[2] || "")
        .replace(/<[^>]+>/g, "")
        .replace(/\s+/g, " ")
        .trim();
      if (name && text) traits.push({ name: name, text: text });
    }
    return traits;
  }

  function formatSaveShort(cls) {
    if (!cls || !cls.saves) return "—";
    return String(cls.saves).replace(/\s+on save/i, "").trim() || "—";
  }

  function truncateSummary(text, maxLen) {
    const s = String(text || "").trim();
    if (!s) return "";
    if (s.length <= maxLen) return s;
    return s.slice(0, maxLen - 1).trim() + "…";
  }

  /**
   * Map a live sheet character to the pregen sheet view-model shape.
   * Uses live formulas (level, hearts, effective mods) so export matches play.
   */
  function buildPregenViewModel(c) {
    const cls = findClass(c);
    const sub = findSubclass(c);
    const lineage = byId(data.lineages, c.lineageId);
    const heritage = byId(data.heritages, c.heritageId);
    const background = byId(data.backgrounds, c.backgroundId);
    const armor = byId(ARMOR, c.armorId);
    const weapon = byId(WEAPONS, c.weaponId);
    const pb = computePB(c);
    const langNl = document.documentElement.lang === "nl" || /\/nl\//.test(location.pathname);

    const abilities = {
      fit: effectiveMod(c, "fit"),
      ins: effectiveMod(c, "ins"),
      wil: effectiveMod(c, "wil"),
    };

    const skillChoice = parseBackgroundSkillChoice(background);
    const skillNames = [];
    if (skillChoice) {
      skillChoice.fixed.forEach((s) => skillNames.push(s));
      c.chosenSkills.filter((s) => skillChoice.options.includes(s)).forEach((s) => skillNames.push(s));
    } else {
      c.chosenSkills.forEach((s) => skillNames.push(s));
    }
    const skills = skillNames.map((name) => {
      const ability = skillAbility(name);
      return {
        name: name,
        ability: ability,
        expertise: false,
        bonus: (Number(abilities[ability]) || 0) + pb,
      };
    });

    const classFeatures = cls ? featuresAtLevel(cls.abilities, c.level) : [];
    const subFeatures = sub ? featuresAtLevel(sub.features, c.level) : [];
    const features = classFeatures.concat(subFeatures).map((f) => ({
      name: f.name,
      summary: truncateSummary(f.summary, 90),
    }));

    const talentName = c.chosenTalents[0] || "";
    const talent = talentName ? talentByName(talentName) : null;

    const attacks = [];
    const seenWeaponIds = new Set();
    (c.weaponIds || []).forEach((wid) => {
      if (!wid || seenWeaponIds.has(wid)) return;
      const w = byId(WEAPONS, wid);
      if (!w) return;
      seenWeaponIds.add(wid);
      const atk = computeAttackBonusForWeaponId(c, wid);
      attacks.push({
        weapon: w.name,
        bonus: atk != null ? atk : pb,
        wounds: 1,
      });
    });
    if (!attacks.length && weapon) {
      const atk = computeAttackBonus(c);
      attacks.push({
        weapon: weapon.name,
        bonus: atk != null ? atk : pb,
        wounds: 1,
      });
    }

    const equipment = [];
    if (armor) {
      equipment.push(armor.name + (c.hasShield ? (langNl ? " + schild" : " + shield") : ""));
    } else if (c.hasShield) {
      equipment.push(langNl ? "Schild" : "Shield");
    }
    String(c.inventoryText || "")
      .split(/\r?\n/)
      .forEach((item) => {
        const line = item.trim();
        if (line) equipment.push(line);
      });
    const equippedNotes = String(c.equippedText || "").trim();
    if (equippedNotes) equipment.push(equippedNotes);

    let spells = null;
    syncGrantedSpells(c);
    const grantedIds = c.grantedSpellIds || [];
    if (isCaster(c) || grantedIds.length) {
      function formatSpellExportLabel(spell) {
        if (!spell) return "";
        if (spell.circle === 0) return spell.name;
        return spell.name + " (" + spell.circle + ")";
      }
      function mergeUniqueSpellIds(primary, extra) {
        const out = [];
        const seen = new Set();
        (primary || []).concat(extra || []).forEach((id) => {
          if (!id || seen.has(id)) return;
          seen.add(id);
          out.push(id);
        });
        return out;
      }
      const allIds = mergeUniqueSpellIds(c.learnedSpellIds, grantedIds);
      const learned = allIds.map(spellById).filter(Boolean);
      const cantrips = learned.filter((s) => s.circle === 0).map((s) => s.name);
      const mode = spellMode(cls);
      const leveledLabels = learned.filter((s) => s.circle > 0).map(formatSpellExportLabel);
      const grantedNote = grantedIds.length
        ? (langNl ? "Inclusief bonus-spells van lineage/heritage." : "Includes bonus spells from lineage/heritage.")
        : "";
      if (usesLearnedTier(mode)) {
        const preparedIds = new Set(c.preparedSpellIds);
        grantedIds.forEach((id) => {
          const s = spellById(id);
          if (s && s.circle > 0) preparedIds.add(id);
        });
        const prepared = learned
          .filter((s) => s.circle > 0 && preparedIds.has(s.id))
          .map(formatSpellExportLabel);
        const knownUnprepared = learned
          .filter((s) => s.circle > 0 && !preparedIds.has(s.id))
          .map(formatSpellExportLabel);
        spells = { cantrips: cantrips, prepared: prepared, knownUnprepared: knownUnprepared, note: grantedNote };
      } else if (mode === "known" || mode === "known-formula") {
        spells = { cantrips: cantrips, known: leveledLabels, note: grantedNote };
      } else if (mode) {
        // full (and any other prepare-from-list mode)
        spells = { cantrips: cantrips, prepared: leveledLabels, note: grantedNote };
      } else {
        spells = { cantrips: cantrips, known: leveledLabels, note: grantedNote || (langNl ? "Bonus-spells." : "Bonus spells.") };
      }
    }

    const className = cls ? cls.name : "—";
    const bgName = background ? background.name : "";
    const subclassName = sub ? sub.name : "";

    return {
      name: c.name || (langNl ? "Naamloos" : "Unnamed"),
      portraitUrl: c.portraitUrl || "",
      className: className,
      level: c.level,
      // Meta line after Level: subclass (background already appears in the facts row).
      concept: subclassName,
      role: subclassName || className,
      lineageName: lineage ? lineage.name : "—",
      heritageName: heritage ? heritage.name : "—",
      backgroundName: bgName || "—",
      armorLabel: armor
        ? armor.name + (c.hasShield ? (langNl ? " + schild" : " + shield") : "")
        : c.hasShield
          ? langNl
            ? "Schild"
            : "Shield"
          : langNl
            ? "Geen"
            : "None",
      abilities: abilities,
      hearts: c.hearts,
      spellPower: computeSpellPowerMax(c),
      spellcastingAbility: spellcastingAbility(cls),
      spellcastingLine: formatSpellcastingLine(c) || "",
      pb: pb,
      maxWd: computeMaxWd(c),
      resolve: resolveMax(c),
      defense: computeDefense(c),
      speed: computeSpeed(c),
      save: formatSaveShort(cls),
      features: features,
      talentName: talentName,
      talentSummary: talent ? truncateSummary(talent.description || talent.summary || "", 90) : "",
      skills: skills,
      proficiencies: deriveProficiencyLines(cls),
      attacks: attacks,
      spells: spells,
      motivation: "",
      personality: "",
      background: "",
      lineageTraits: parseLineageTraits(lineage),
      equipment: equipment,
      armorWarning: formatArmorWarning(c),
      footer: "YMIAT · " + (langNl ? "Personageblad" : "Character sheet") + " · L" + c.level,
      downloadHref: "",
    };
  }

  function sheetLocale() {
    return document.documentElement.lang === "nl" || /\/nl\//.test(location.pathname) ? "nl" : "en";
  }

  function syncToolbarFoldout(hasChar, force) {
    if (!el.toolbar) return;
    const open = force != null ? force : !hasChar;
    el.toolbar.classList.toggle("is-open", open);
    if (el.toolbarToggle) {
      el.toolbarToggle.setAttribute("aria-expanded", open ? "true" : "false");
      el.toolbarToggle.textContent = open
        ? t("toolbarHide", t("toolbarToggle", "Controls"))
        : t("toolbarShow", t("toolbarToggle", "Controls"));
    }
  }

  function applyToolbarI18n() {
    if (el.btnExportPdf) el.btnExportPdf.textContent = t("exportPdf", "Export PDF");
    if (el.btnCreator) {
      el.btnCreator.textContent = t("openCreator", "Character Creator");
      el.btnCreator.setAttribute("href", rp("character-creator.html"));
    }
    if (el.toolbarToggle) {
      const open = el.toolbar && el.toolbar.classList.contains("is-open");
      el.toolbarToggle.textContent = open
        ? t("toolbarHide", t("toolbarToggle", "Controls"))
        : t("toolbarShow", t("toolbarToggle", "Controls"));
    }
  }

  function loadScriptOnce(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[data-cs-lib="${src}"]`);
      if (existing) {
        if (existing.dataset.loaded === "1") resolve();
        else existing.addEventListener("load", () => resolve(), { once: true });
        return;
      }
      const s = document.createElement("script");
      s.src = rp(src);
      s.async = true;
      s.dataset.csLib = src;
      s.onload = () => {
        s.dataset.loaded = "1";
        resolve();
      };
      s.onerror = () => reject(new Error("Failed to load " + src));
      document.head.appendChild(s);
    });
  }

  function pdfSafeFilename(name) {
    const base = String(name || "character")
      .trim()
      .replace(/[<>:"/\\|?*\x00-\x1f]/g, "")
      .replace(/\s+/g, "-")
      .slice(0, 60);
    return (base || "character") + ".pdf";
  }

  function cleanupPgExport() {
    if (!el.pgExport) return;
    el.pgExport.classList.remove("cs-pg-export--ready");
    el.pgExport.innerHTML = "";
    el.pgExport.hidden = true;
    el.pgExport.setAttribute("aria-hidden", "true");
    document.body.classList.remove("cs-pg-exporting");
  }

  /** Mount the pregen-format sheet for the active character into #cs-pg-export. */
  function mountPregenExportSheet() {
    if (!char || typeof window.ymiatRenderPregenSheetHtml !== "function" || !el.pgExport) return null;
    const lang = sheetLocale();
    const vm = buildPregenViewModel(char);
    const html = window.ymiatRenderPregenSheetHtml(vm, { lang: lang, includeChrome: false });
    el.pgExport.innerHTML = html;
    el.pgExport.hidden = false;
    el.pgExport.setAttribute("aria-hidden", "false");
    return el.pgExport.querySelector(".pg-sheet");
  }

  /**
   * All learned spells as printable card objects, sorted by circle then name.
   * Spellbook casters get prepared true/false on leveled spells; others null.
   */
  function buildSpellCardsForExport(c) {
    if (!c) return [];
    syncGrantedSpells(c);
    const grantedIds = c.grantedSpellIds || [];
    const learnedIds = Array.isArray(c.learnedSpellIds) ? c.learnedSpellIds : [];
    const allIds = [];
    const seen = new Set();
    learnedIds.concat(grantedIds).forEach((id) => {
      if (!id || seen.has(id)) return;
      seen.add(id);
      allIds.push(id);
    });
    if (!allIds.length) return [];
    const cls = findClass(c);
    const tiered = usesLearnedTier(spellMode(cls));
    const preparedIds = new Set(c.preparedSpellIds || []);
    grantedIds.forEach((id) => {
      const s = spellById(id);
      if (s && s.circle > 0) preparedIds.add(id);
    });
    return allIds
      .map(spellById)
      .filter(Boolean)
      .sort(function (a, b) {
        const d = (a.circle || 0) - (b.circle || 0);
        return d !== 0 ? d : String(a.name).localeCompare(String(b.name));
      })
      .map(function (s) {
        const granted = grantedIds.includes(s.id);
        return {
          id: s.id,
          name: s.name,
          circle: s.circle,
          school: s.school || "",
          castingTime: s.castingTime || "",
          range: s.range || "",
          duration: s.duration || "",
          components: s.components || "",
          description: s.description || "",
          prepared: granted ? true : tiered && s.circle > 0 ? preparedIds.has(s.id) : null,
          granted: granted,
        };
      });
  }

  function renderSpellPagesHtmlForChar(c) {
    if (typeof window.ymiatRenderPregenSpellPagesHtml !== "function") return "";
    const cards = buildSpellCardsForExport(c);
    if (!cards.length) return "";
    return window.ymiatRenderPregenSpellPagesHtml(cards, {
      characterName: c.name || "",
      lang: sheetLocale(),
      perPage: 6,
    });
  }

  function addCanvasToPdf(pdf, canvas, margin) {
    const pageW = pdf.internal.pageSize.getWidth();
    const pageH = pdf.internal.pageSize.getHeight();
    const maxW = pageW - margin * 2;
    const maxH = pageH - margin * 2;
    const ratio = Math.min(maxW / canvas.width, maxH / canvas.height);
    const drawW = canvas.width * ratio;
    const drawH = canvas.height * ratio;
    const x = (pageW - drawW) / 2;
    const y = (pageH - drawH) / 2;
    pdf.addImage(canvas.toDataURL("image/png"), "PNG", x, y, drawW, drawH);
  }

  /** Print uses an isolated iframe so conflicting page @page/portrait rules cannot win. */
  function printPregenSheet() {
    if (!char || typeof window.ymiatRenderPregenSheetHtml !== "function") return;
    const lang = sheetLocale();
    const vm = buildPregenViewModel(char);
    const sheetHtml = window.ymiatRenderPregenSheetHtml(vm, { lang: lang, includeChrome: false });
    const spellHtml = renderSpellPagesHtmlForChar(char);
    const cssHref = new URL(rp("assets/pregenerated-characters.css"), window.location.href).href;

    const iframe = document.createElement("iframe");
    iframe.setAttribute("title", "Print character sheet");
    iframe.style.cssText = "position:fixed;right:0;bottom:0;width:0;height:0;border:0;opacity:0;pointer-events:none;";
    document.body.appendChild(iframe);

    const doc = iframe.contentDocument;
    doc.open();
    doc.write(
      "<!DOCTYPE html><html><head><meta charset=\"utf-8\" />" +
      "<title>" + (vm.name || "Character") + "</title>" +
      "<link rel=\"stylesheet\" href=\"" + cssHref + "\" />" +
      "<style>" +
      "@page{size:A4 landscape;margin:8mm}" +
      "html,body{margin:0;padding:0;background:#fff !important;color:#111}" +
      ".pg-sheet-wrap{max-width:none;margin:0}" +
      ".pg-sheet{" +
      "display:grid !important;" +
      "grid-template-columns:1.05fr 1fr 1fr !important;" +
      "box-shadow:none !important;" +
      "break-inside:avoid;page-break-inside:avoid;" +
      "-webkit-print-color-adjust:exact;print-color-adjust:exact" +
      "}" +
      ".pg-head{display:grid !important;grid-template-columns:minmax(11rem,1.05fr) minmax(0,1.7fr) !important}" +
      ".pg-head:has(.pg-avatar){grid-template-columns:56px minmax(9rem,1.05fr) minmax(0,1.7fr) !important}" +
      ".pg-avatar{width:56px;height:56px;object-fit:cover;display:block}" +
      ".pg-col{border-right:1px solid #bbb !important;border-bottom:0 !important}" +
      ".pg-col:last-child{border-right:0 !important}" +
      ".pg-spell-page{page-break-before:always;break-before:page;width:auto;min-height:0;border:0;padding:0}" +
      "</style></head><body>" + sheetHtml + spellHtml + "</body></html>"
    );
    doc.close();

    const cleanup = () => {
      if (iframe.parentNode) iframe.parentNode.removeChild(iframe);
    };

    let printed = false;
    const runPrint = () => {
      if (printed) return;
      printed = true;
      try {
        iframe.contentWindow.focus();
        iframe.contentWindow.print();
      } finally {
        // Keep iframe briefly so the print dialog can read it, then remove.
        setTimeout(cleanup, 2000);
      }
    };

    const link = doc.querySelector("link[rel=\"stylesheet\"]");
    if (link) {
      link.addEventListener("load", runPrint, { once: true });
      link.addEventListener("error", runPrint, { once: true });
      // Fallback if load already fired or is cached without event.
      setTimeout(runPrint, 400);
    } else {
      runPrint();
    }
  }

  async function exportPregenPdf() {
    if (!char || !el.pgExport) return;
    if (el.btnExportPdf && el.btnExportPdf.dataset.busy === "1") return;

    const sheetEl = mountPregenExportSheet();
    if (!sheetEl) {
      cleanupPgExport();
      return;
    }
    const spellHtml = renderSpellPagesHtmlForChar(char);
    if (spellHtml) el.pgExport.insertAdjacentHTML("beforeend", spellHtml);
    el.pgExport.classList.add("cs-pg-export--ready");

    const label = t("exportPdf", "Export PDF");
    if (el.btnExportPdf) {
      el.btnExportPdf.dataset.busy = "1";
      el.btnExportPdf.disabled = true;
      el.btnExportPdf.textContent = t("exportPdfBusy", "Creating PDF…");
    }

    try {
      await loadScriptOnce("assets/lib/html2canvas.min.js");
      await loadScriptOnce("assets/lib/jspdf.umd.min.js");
      const html2canvas = window.html2canvas;
      const jsPDF = window.jspdf && window.jspdf.jsPDF;
      if (typeof html2canvas !== "function" || typeof jsPDF !== "function") {
        throw new Error("PDF libraries unavailable");
      }

      const margin = 8;
      const captureOpts = {
        scale: 2,
        backgroundColor: "#ffffff",
        logging: false,
        useCORS: true,
      };
      const pdf = new jsPDF({ orientation: "landscape", unit: "mm", format: "a4" });

      const sheetCanvas = await html2canvas(sheetEl, captureOpts);
      addCanvasToPdf(pdf, sheetCanvas, margin);

      const spellPages = el.pgExport.querySelectorAll(".pg-spell-page");
      for (let i = 0; i < spellPages.length; i++) {
        pdf.addPage();
        const pageCanvas = await html2canvas(spellPages[i], captureOpts);
        addCanvasToPdf(pdf, pageCanvas, margin);
      }

      pdf.save(pdfSafeFilename(char.name));
    } catch (err) {
      console.error(err);
      if (window.ymiatDialog) {
        window.ymiatDialog({
          title: t("exportPdfFailed", "Could not create the PDF. Try again, or use Print."),
        });
      }
    } finally {
      cleanupPgExport();
      if (el.btnExportPdf) {
        el.btnExportPdf.dataset.busy = "0";
        el.btnExportPdf.disabled = !char;
        el.btnExportPdf.textContent = label;
      }
    }
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

  function normalizePortrait(value) {
    if (typeof value !== "string") return "";
    if (!value.startsWith("data:image/jpeg;base64,")) return "";
    if (value.length > 200000) return "";
    return value;
  }

  function resizeBitmapToPortrait(bitmap) {
    const w = bitmap.width;
    const h = bitmap.height;
    if (!w || !h) throw new Error("Empty image");
    const side = 256;
    const scale = Math.max(side / w, side / h);
    const dw = w * scale;
    const dh = h * scale;
    const canvas = document.createElement("canvas");
    canvas.width = side;
    canvas.height = side;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(bitmap, (side - dw) / 2, (side - dh) / 2, dw, dh);
    return canvas.toDataURL("image/jpeg", 0.85);
  }

  async function blobToPortrait(blob) {
    const bitmap = await createImageBitmap(blob);
    try {
      return resizeBitmapToPortrait(bitmap);
    } finally {
      if (bitmap.close) bitmap.close();
    }
  }

  function portraitFrameHtml(c, ids) {
    const url = c.portraitUrl || "";
    const addLabel = t("addPortrait", "Add photo");
    const removeLabel = t("removePortrait", "Clear image");
    const portraitLabel = t("portrait", "Portrait");
    const img = url
      ? `<img class="cs-avatar-img" src="${escapeHtml(url)}" alt="${escapeHtml(portraitLabel)}" />`
      : `<span class="cs-avatar-placeholder">${escapeHtml(addLabel)}</span>`;
    const clear = url
      ? `<button type="button" class="cs-avatar-clear" id="${ids.clear}">${escapeHtml(removeLabel)}</button>`
      : "";
    return `<div class="cs-avatar">
      <div class="cs-avatar-wrap">
        <button type="button" class="cs-avatar-frame" id="${ids.pick}" aria-label="${escapeHtml(url ? portraitLabel : addLabel)}">${img}</button>
      </div>
      ${clear}
      <input type="file" id="${ids.file}" class="cs-avatar-file" accept="image/*" hidden />
    </div>`;
  }

  function ddbAvatarSourceUrl(ddbChar) {
    const dec = (ddbChar && ddbChar.decorations) || {};
    return (
      dec.avatarUrl ||
      dec.thumbnailBackdropAvatarUrl ||
      (dec.defaultBackdrop && dec.defaultBackdrop.thumbnailBackdropAvatarUrl) ||
      ""
    );
  }

  function isAllowedDdbImageUrl(raw) {
    try {
      const u = new URL(raw);
      const host = u.hostname.toLowerCase();
      return u.protocol === "https:" && (host === "dndbeyond.com" || host.endsWith(".dndbeyond.com"));
    } catch (_) {
      return false;
    }
  }

  async function fetchDdbPortrait(remoteUrl) {
    const proxyBase = String(window.YMIAT_DDB_PROXY_URL || "").replace(/\/$/, "");
    if (!proxyBase || !isAllowedDdbImageUrl(remoteUrl)) return "";
    const res = await fetch(proxyBase + "?img=" + encodeURIComponent(remoteUrl));
    if (!res.ok) return "";
    const blob = await res.blob();
    if (!blob || !blob.size) return "";
    return blobToPortrait(blob);
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
      node.innerHTML = html || `<p class="cs-muted">${escapeHtml(t("selectOption", "Select an option to see details."))}</p>`;
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
      const pill = chosen
        ? `<span class="cs-spell-chip is-active" data-talent-view="${escapeHtml(chosen)}" title="Click for details">${escapeHtml(chosen)}</span>`
        : '<span class="cs-muted">None chosen yet</span>';
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

  function renderGrantChoiceUi(c) {
    const defs = activeGrantDefs(c).filter((def) => def.kind === "choice" || def.kind === "legacy");
    if (!defs.length) return "";
    const rows = defs
      .map((def) => {
        const current = (c.grantedSpellChoices && c.grantedSpellChoices[def.key]) || "";
        const sourceTag = grantSourceTag(def.sourceType);
        if (def.kind === "legacy") {
          const opts = Object.keys(def.branches || {})
            .map((key) => {
              const branch = def.branches[key];
              return `<option value="${escapeHtml(key)}"${current === key ? " selected" : ""}>${escapeHtml(branch.label || key)}</option>`;
            })
            .join("");
          return `<div class="cs-grant-pick">
            <label class="cs-label" for="cs-grant-${escapeHtml(def.key)}">${escapeHtml(def.label)} <span class="cs-muted">(${escapeHtml(sourceTag)} · Willpower)</span></label>
            <select id="cs-grant-${escapeHtml(def.key)}" class="cs-select" data-grant-choice="${escapeHtml(def.key)}">
              <option value="">— Choose legacy —</option>
              ${opts}
            </select>
          </div>`;
        }
        const spells = grantChoiceOptions(def);
        const opts = spells
          .map((s) => `<option value="${escapeHtml(s.id)}"${current === s.id ? " selected" : ""}>${escapeHtml(s.name)}${s.school ? ` (${escapeHtml(s.school)})` : ""}</option>`)
          .join("");
        const pickLabel = def.choiceLabel ? `${def.label} — ${def.choiceLabel}` : def.label;
        return `<div class="cs-grant-pick">
          <label class="cs-label" for="cs-grant-${escapeHtml(def.key)}">${escapeHtml(pickLabel)} <span class="cs-muted">(${escapeHtml(sourceTag)})</span></label>
          <select id="cs-grant-${escapeHtml(def.key)}" class="cs-select" data-grant-choice="${escapeHtml(def.key)}">
            <option value="">— Choose spell —</option>
            ${opts}
          </select>
        </div>`;
      })
      .join("");
    return `<div class="cs-grant-picks">${rows}</div>`;
  }

  function renderSpellChip(s, opts) {
    const granted = Boolean(opts && opts.granted);
    const active = granted || Boolean(opts && opts.active);
    const stateLabel = granted
      ? `Always active · from ${opts.sourceTag || "Granted"}`
      : opts && opts.stateLabel
        ? opts.stateLabel
        : "Active";
    const tag = granted
      ? ` <span class="cs-spell-chip-tag">${escapeHtml(opts.sourceTag || "Granted")}</span>`
      : "";
    const circleLabel = s.circle === 0 ? "Cantrip" : `Spell Level ${s.circle}`;
    return `<span class="cs-spell-chip${active ? " is-active" : " is-inactive"}${granted ? " is-granted" : ""}" data-spell-view="${s.id}" title="${escapeHtml(s.school)} · ${circleLabel} · ${escapeHtml(stateLabel)} · Click for details">${escapeHtml(s.name)}${tag}</span>`;
  }

  function renderSpellsPane(c, cls) {
    syncGrantedSpells(c);
    const mode = spellMode(cls);
    const tiered = usesLearnedTier(mode);
    const cCap = mode ? cantripCap(cls, c.level) : 0;
    const activeCap = mode ? computeActiveCap(c) : 0;
    const label = mode ? activeCapLabel(mode) : "Spells";
    const grantedSet = new Set(c.grantedSpellIds || []);

    const classLearned = mode
      ? c.learnedSpellIds.map(spellById).filter((s) => s && cls && s.classes.includes(cls.id) && !grantedSet.has(s.id))
      : [];
    const grantedSpells = (c.grantedSpellIds || []).map(spellById).filter(Boolean);

    const byIdMap = new Map();
    classLearned.forEach((s) => byIdMap.set(s.id, { spell: s, granted: false }));
    grantedSpells.forEach((s) => byIdMap.set(s.id, { spell: s, granted: true }));

    const all = [...byIdMap.values()];
    const cantrips = all.filter((x) => x.spell.circle === 0).sort((a, b) => a.spell.name.localeCompare(b.spell.name));
    const leveled = all.filter((x) => x.spell.circle > 0).sort((a, b) => a.spell.circle - b.spell.circle || a.spell.name.localeCompare(b.spell.name));

    const classCantripCount = cantrips.filter((x) => !x.granted).length;
    const classLeveled = leveled.filter((x) => !x.granted);

    let counterText = "";
    if (mode) {
      if (tiered) {
        const learnedCap = computeLearnedCap(c);
        const activeCount = classLeveled.filter((x) => c.preparedSpellIds.includes(x.spell.id)).length;
        counterText = `Learned ${classLeveled.length}/${learnedCap} · Prepared ${activeCount}/${activeCap}`;
      } else {
        counterText = `${label} ${classLeveled.length}/${activeCap}`;
      }
    }

    const groups = [];
    if (cantrips.length) {
      const chips = cantrips
        .map((x) => {
          const meta = x.granted ? grantedSpellMeta(c, x.spell.id) : null;
          return renderSpellChip(x.spell, {
            granted: x.granted,
            active: true,
            sourceTag: meta ? grantSourceTag(meta.sourceType) : "",
            stateLabel: "Always active",
          });
        })
        .join("");
      groups.push(renderSpellChipGroup("Cantrips", chips));
    }

    const maxCircle = leveled.length ? leveled[leveled.length - 1].spell.circle : 0;
    for (let circle = 1; circle <= maxCircle; circle++) {
      const spells = leveled.filter((x) => x.spell.circle === circle);
      if (!spells.length) continue;
      const chips = spells
        .map((x) => {
          if (x.granted) {
            const meta = grantedSpellMeta(c, x.spell.id);
            return renderSpellChip(x.spell, {
              granted: true,
              active: true,
              sourceTag: meta ? grantSourceTag(meta.sourceType) : "",
            });
          }
          const active = tiered ? c.preparedSpellIds.includes(x.spell.id) : true;
          const stateLabel = tiered ? (active ? "Prepared" : "Learned") : label;
          return renderSpellChip(x.spell, { granted: false, active: active, stateLabel: stateLabel });
        })
        .join("");
      groups.push(renderSpellChipGroup(`Spell Level ${circle}`, chips));
    }

    const manageBtn =
      mode || grantedSpells.length
        ? `<button type="button" class="btn cs-btn-secondary cs-btn-small" id="cs-manage-spells">${escapeHtml(t("manageSpells", "Manage Spells"))}</button>`
        : "";
    const counterLine = mode
      ? `<p class="cs-muted">Cantrips ${classCantripCount}/${cCap} · ${counterText}</p>`
      : `<p class="cs-muted">${escapeHtml(t("grantedSpellsOnly", "Bonus spells from lineage / heritage (outside class caps)."))}</p>`;

    return `<div class="cs-pane cs-pane--spells">
      <h2 class="cs-pane-title cs-pane-title--with-action">${escapeHtml(t("spells", "Spells"))} ${manageBtn}</h2>
      ${counterLine}
      ${renderGrantChoiceUi(c)}
      ${groups.length ? groups.join("") : '<p class="cs-muted">No spells learned yet.</p>'}
    </div>`;
  }

  function renderModals() {
    if (!el.modalRoot) return;
    // Toggling a checkbox rebuilds the whole modal via innerHTML, which
    // would otherwise reset .cs-modal-body's scroll position to the top
    // on every click - save and restore it across the rebuild.
    const prevBody = el.modalRoot.querySelector(".cs-modal-body");
    const scrollTop = prevBody ? prevBody.scrollTop : 0;

    if (portraitClearOpen && char) {
      renderPortraitClearModal();
    } else if (spellModalOpen && char) {
      renderManageSpellsModal();
    } else if (spellViewId && char) {
      renderSpellViewModal();
    } else if (talentViewName && char) {
      renderTalentViewModal();
    } else if (skillModalOpen && char) {
      renderSkillModal();
    } else if (languageModalOpen && char) {
      renderLanguageModal();
    } else if (talentModalOpen && char) {
      renderTalentModal();
    } else if (ddbReview) {
      renderDdbReviewModal();
    } else if (ddbModalOpen) {
      renderDdbImportModal();
    } else {
      el.modalRoot.innerHTML = "";
    }

    const newBody = el.modalRoot.querySelector(".cs-modal-body");
    if (newBody) newBody.scrollTop = scrollTop;
  }

  function renderPortraitClearModal() {
    const title = t("removePortrait", "Clear image");
    const message = t("clearPortraitConfirm", "Clear this image?");
    const cancel = t("cancel", "Cancel");
    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-portrait-clear-overlay">
      <div class="cs-modal cs-modal--confirm" role="dialog" aria-modal="true" aria-labelledby="cs-portrait-clear-title">
        <div class="cs-modal-header">
          <h2 id="cs-portrait-clear-title">${escapeHtml(title)}</h2>
          <button type="button" class="cs-modal-close" id="cs-portrait-clear-close" aria-label="${escapeHtml(t("close", "Close"))}">×</button>
        </div>
        <p class="cs-portrait-clear-message">${escapeHtml(message)}</p>
        <div class="cls-ability-modal-footer">
          <button type="button" class="btn cs-btn-secondary" id="cs-portrait-clear-cancel">${escapeHtml(cancel)}</button>
          <button type="button" class="btn cs-btn-danger" id="cs-portrait-clear-confirm">${escapeHtml(title)}</button>
        </div>
      </div>
    </div>`;
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
      .map((opt) => {
        const talent = talentByName(opt);
        const expanded = talentModalExpandedIds.has(opt);
        const detailId = "cs-talent-details-" + String(opt).toLowerCase().replace(/[^a-z0-9]+/g, "-");
        const label = expanded ? t("hideDetails", "Hide details") : t("showDetails", "Show details");
        const chevron = expanded ? "⌄" : "›";
        const toggle = `<button type="button" class="cs-spell-details-toggle" data-talent-details="${escapeHtml(opt)}" aria-expanded="${expanded ? "true" : "false"}" aria-controls="${escapeHtml(detailId)}">
          ${label} <span class="cs-spell-chevron" aria-hidden="true">${chevron}</span>
        </button>`;
        let details = "";
        if (expanded) {
          if (talent) {
            details = `<div class="cs-spell-details" id="${escapeHtml(detailId)}">
              ${talent.prerequisite ? `<p class="cs-spell-view-meta">Prerequisite: ${escapeHtml(talent.prerequisite)}</p>` : ""}
              <p class="cs-spell-view-desc">${escapeHtml(talent.description || "")}</p>
            </div>`;
          } else {
            details = `<div class="cs-spell-details" id="${escapeHtml(detailId)}">
              <p class="cs-spell-view-desc cs-muted">No details available for this talent.</p>
            </div>`;
          }
        }
        const rowClass = `cs-choice-row cs-choice-row--talent${expanded ? " is-expanded" : ""}`;
        return `<li class="${rowClass}">
          <label class="cs-spell-check">
            <input type="radio" name="cs-talent-radio" data-talent-option="${escapeHtml(opt)}"${opt === chosen ? " checked" : ""} />
            <span class="cs-spell-name">${escapeHtml(opt)}</span>
          </label>
          ${toggle}
          ${details}
        </li>`;
      })
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
    const otherLanguages = ALL_LANGUAGES.filter(
      (l) => !choice.options.includes(l) && !char.chosenLanguages.includes(l)
    );

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
          ${otherLanguages.length ? `<div class="cs-choice-add-row">
            <select id="cs-language-dropdown" class="cs-select"${atCap ? " disabled" : ""}>
              <option value="">— Add another language —</option>
              ${otherLanguages.map((l) => `<option value="${escapeHtml(l)}">${escapeHtml(l)}</option>`).join("")}
            </select>
          </div>` : ""}
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
    const circleLabel = spell.circle === 0 ? "Cantrip" : `Spell Level ${spell.circle}`;

    // Only Wizard/Theurge-style tiered casters have a Learned-vs-Prepared
    // split worth toggling; everyone else's learned leveled spells (and
    // all cantrips) are already always active.
    const cls = findClass(char);
    const mode = spellMode(cls);
    const canTogglePrepare =
      spell.circle > 0 &&
      usesLearnedTier(mode) &&
      cls &&
      spell.classes.includes(cls.id) &&
      char.learnedSpellIds.includes(spell.id);
    const prepared = canTogglePrepare && char.preparedSpellIds.includes(spell.id);
    const preparedLeveledCount = char.preparedSpellIds.filter((pid) => {
      const s = spellById(pid);
      return s && s.circle > 0;
    }).length;
    const atCap = !prepared && preparedLeveledCount >= computeActiveCap(char);
    const toggleButton = canTogglePrepare
      ? `<button type="button" class="btn cs-btn-secondary cs-btn-small" id="cs-spell-view-toggle-prepare" data-spell-id="${escapeHtml(spell.id)}"${atCap ? " disabled" : ""}>${prepared ? "Unprepare" : "Prepare"}</button>`
      : "";

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-spell-view-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="${escapeHtml(spell.name)}">
        <div class="cs-modal-header">
          <div class="cs-modal-header-title">
            <h2>${escapeHtml(spell.name)}</h2>
            ${toggleButton}
          </div>
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

  function renderTalentViewModal() {
    const talent = talentByName(talentViewName);
    if (!talent) {
      el.modalRoot.innerHTML = "";
      return;
    }
    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-talent-view-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="${escapeHtml(talent.name)}">
        <div class="cs-modal-header">
          <h2>${escapeHtml(talent.name)}</h2>
          <button type="button" class="cs-modal-close" id="cs-talent-view-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-body">
          ${talent.prerequisite ? `<p class="cs-spell-view-meta">Prerequisite: ${escapeHtml(talent.prerequisite)}</p>` : ""}
          <p class="cs-spell-view-desc">${escapeHtml(talent.description)}</p>
        </div>
      </div>
    </div>`;
  }

  function spellRowDetailsToggle(s, expanded) {
    const label = expanded ? t("hideDetails", "Hide details") : t("showDetails", "Show details");
    const chevron = expanded ? "⌄" : "›";
    return `<button type="button" class="cs-spell-details-toggle" data-spell-details="${escapeHtml(s.id)}" aria-expanded="${expanded ? "true" : "false"}" aria-controls="cs-spell-details-${escapeHtml(s.id)}">
      ${label} <span class="cs-spell-chevron" aria-hidden="true">${chevron}</span>
    </button>`;
  }

  function spellRowDetailsPanel(s, expanded) {
    if (!expanded) return "";
    return `<div class="cs-spell-details" id="cs-spell-details-${escapeHtml(s.id)}">
      <p class="cs-spell-view-meta">Range: ${escapeHtml(s.range)} · Duration: ${escapeHtml(s.duration)} · Components: ${escapeHtml(s.components)}</p>
      <p class="cs-spell-view-desc">${escapeHtml(s.description)}</p>
    </div>`;
  }

  function renderManageSpellsModal() {
    const cls = findClass(char);
    const mode = spellMode(cls);
    syncGrantedSpells(char);
    const grantedSet = new Set(char.grantedSpellIds || []);
    const tiered = usesLearnedTier(mode);
    const label = activeCapLabel(mode);
    const maxCircle = mode ? maxSpellCircle(cls, char.level) : 0;
    const cCap = mode ? cantripCap(cls, char.level) : 0;
    const activeCap = mode ? computeActiveCap(char) : 0;
    const learnedCap = tiered ? computeLearnedCap(char) : null;
    const filterText = spellModalFilter.trim().toLowerCase();
    const eligible = mode
      ? eligibleSpells(char).filter((s) => !filterText || s.name.toLowerCase().includes(filterText))
      : [];

    const cantripLearnedCount = countClassCantrips(char);
    const learnedLeveledCount = countClassLeveledLearned(char);
    const activeLeveledCount = tiered ? countClassLeveledPrepared(char) : learnedLeveledCount;

    const grantedSpells = (char.grantedSpellIds || [])
      .map(spellById)
      .filter((s) => s && (!filterText || s.name.toLowerCase().includes(filterText)))
      .sort((a, b) => a.circle - b.circle || a.name.localeCompare(b.name));

    const groups = [];

    if (grantedSpells.length) {
      const rows = grantedSpells
        .map((s) => {
          const meta = grantedSpellMeta(char, s.id);
          const sourceTag = meta ? grantSourceTag(meta.sourceType) : t("granted", "Granted");
          const featureLabel = meta && meta.label ? meta.label : sourceTag;
          const expanded = spellModalExpandedIds.has(s.id);
          const rowClass = `cs-spell-row-modal is-granted${expanded ? " is-expanded" : ""}`;
          return `<li class="${rowClass}">
            <label class="cs-spell-check">
              <input type="checkbox" checked disabled data-granted-spell="${s.id}" />
              <span class="cs-spell-name">${escapeHtml(s.name)}</span>
            </label>
            <span class="cs-spell-tag">Always active · from ${escapeHtml(sourceTag)}</span>
            ${spellRowDetailsToggle(s, expanded)}
            <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(featureLabel)}</span>
            ${spellRowDetailsPanel(s, expanded)}
          </li>`;
        })
        .join("");
      groups.push(`<div class="cs-spell-group">
        <h3 class="cs-spell-group-title">${escapeHtml(t("grantedSpells", "Granted spells"))}</h3>
        <ul class="cs-spell-list">${rows}</ul>
      </div>`);
    }

    if (mode) {
      for (let circle = 0; circle <= maxCircle; circle++) {
        const spells = eligible
          .filter((s) => s.circle === circle && !grantedSet.has(s.id))
          .sort((a, b) => a.name.localeCompare(b.name));
        if (!spells.length) continue;
        const isCantrip = circle === 0;
        const rows = spells
          .map((s) => {
            const learned = char.learnedSpellIds.includes(s.id);
            const prepared = char.preparedSpellIds.includes(s.id);
            const expanded = spellModalExpandedIds.has(s.id);
            const rowClass = `cs-spell-row-modal${expanded ? " is-expanded" : ""}`;
            const toggle = spellRowDetailsToggle(s, expanded);
            const details = spellRowDetailsPanel(s, expanded);

            if (isCantrip) {
              const disabled = !learned && cantripLearnedCount >= cCap;
              return `<li class="${rowClass}">
                <label class="cs-spell-check">
                  <input type="checkbox" data-spell-learn="${s.id}"${learned ? " checked" : ""}${disabled ? " disabled" : ""} />
                  <span class="cs-spell-name">${escapeHtml(s.name)}</span>
                </label>
                <span class="cs-spell-tag">Always active</span>
                ${toggle}
                <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(s.castingTime)}</span>
                ${details}
              </li>`;
            }

            if (!tiered) {
              const disabled = !learned && activeLeveledCount >= activeCap;
              return `<li class="${rowClass}">
                <label class="cs-spell-check">
                  <input type="checkbox" data-spell-learn="${s.id}"${learned ? " checked" : ""}${disabled ? " disabled" : ""} />
                  <span class="cs-spell-name">${escapeHtml(s.name)}</span>
                </label>
                <span class="cs-spell-tag">${label}</span>
                ${toggle}
                <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(s.castingTime)}</span>
                ${details}
              </li>`;
            }

            const learnDisabled = !learned && learnedLeveledCount >= learnedCap;
            const prepDisabled = !learned || (!prepared && activeLeveledCount >= activeCap);
            return `<li class="${rowClass}">
              <label class="cs-spell-check">
                <input type="checkbox" data-spell-learn="${s.id}"${learned ? " checked" : ""}${learnDisabled ? " disabled" : ""} />
                <span class="cs-spell-name">${escapeHtml(s.name)}</span>
              </label>
              <label class="cs-spell-check cs-spell-check--prep">
                <input type="checkbox" data-spell-prepare="${s.id}"${prepared ? " checked" : ""}${prepDisabled ? " disabled" : ""} />
                Prepared
              </label>
              ${toggle}
              <span class="cs-spell-meta">${escapeHtml(s.school)} · ${escapeHtml(s.castingTime)}</span>
              ${details}
            </li>`;
          })
          .join("");
        groups.push(`<div class="cs-spell-group">
          <h3 class="cs-spell-group-title">${circle === 0 ? "Cantrips" : `Spell Level ${circle}`}</h3>
          <ul class="cs-spell-list">${rows}</ul>
        </div>`);
      }
    }

    const counterText = !mode
      ? escapeHtml(t("grantedSpellsOnly", "Bonus spells from lineage / heritage (outside class caps)."))
      : tiered
        ? `Learned ${learnedLeveledCount}/${learnedCap} · Prepared ${activeLeveledCount}/${activeCap}`
        : `${label} ${activeLeveledCount}/${activeCap}`;

    const titleClass = cls ? cls.name : t("grantedSpells", "Granted spells");
    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-spell-modal-overlay">
      <div class="cs-modal" role="dialog" aria-modal="true" aria-label="${escapeHtml(t("manageSpells", "Manage Spells"))}">
        <div class="cs-modal-header">
          <h2>${escapeHtml(t("manageSpells", "Manage Spells"))} — ${escapeHtml(titleClass)}</h2>
          <button type="button" class="cs-modal-close" id="cs-spell-modal-close" aria-label="${escapeHtml(t("close", "Close"))}">×</button>
        </div>
        <div class="cs-modal-sub">
          <input type="text" id="cs-spell-search" class="cs-input" placeholder="Search spells…" value="${escapeHtml(spellModalFilter)}" />
          <span class="cs-modal-counter">${mode ? `Cantrips ${cantripLearnedCount}/${cCap} · ` : ""}${counterText}</span>
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
    const showSpells = caster || hasBonusSpellUi(c);
    const effSpeed = computeSpeed(c);
    const lost = heartsLost(c);
    const range = levelRange();
    const subclassMin = range.subclassMin || 2;

    const classFeatures = cls ? featuresAtLevel(cls.abilities, c.level) : [];
    const subFeatures = sub ? featuresAtLevel(sub.features, c.level) : [];
    const abilitiesHtml = renderFeatureList(classFeatures) +
      (subFeatures.length ? `<h4 class="cs-subheading">${escapeHtml(sub.name)}</h4>${renderFeatureList(subFeatures)}` : "");

    const heartsHtml = [0, 1, 2].map((i) => {
      const filled = i < c.hearts;
      return `<button type="button" class="cs-heart${filled ? " is-full" : " is-empty"}" data-heart="${i}" aria-label="Heart ${i + 1}${filled ? ", remaining" : ", lost"}">${filled ? "♥" : "♡"}</button>`;
    }).join("");

    const spellAb = spellcastingAbility(cls);
    const abilityBoxes = ABILITIES.map((ab) => {
      const base = c.abilities[ab];
      const eff = effectiveMod(c, ab);
      const effHint = lost ? `<span class="cs-eff-mod" title="After ${lost} lost heart(s)">→ ${formatMod(eff)}</span>` : "";
      const isSpellAb = spellAb === ab;
      const label = ABILITY_LABELS[ab] + (isSpellAb ? "*" : "");
      const labelTitle = isSpellAb ? ' title="Spellcasting ability"' : "";
      const labelClass = isSpellAb ? "cs-stat-label is-spellcasting" : "cs-stat-label";
      return `<div class="cs-stat-box">
        <span class="${labelClass}"${labelTitle}>${label}</span>
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
    const defBonus = computeDefense(c);
    const pb = computePB(c);
    const selectedArmor = byId(ARMOR, c.armorId);
    const weaponRows = activeWeaponRowIds(c);
    const weaponRowsHtml = weaponRows
      .map((wid, idx) => {
        const emptyLabel = wid
          ? t("removeWeapon", "Remove weapon")
          : t("chooseWeapon", "Choose weapon");
        const opts = groupedOptionList(WEAPONS, wid, emptyLabel, weaponOptionLabel);
        const atk = wid ? computeAttackBonusForWeaponId(c, wid) : null;
        const atkTitle = wid ? attackBonusBreakdownTitle(c, wid) : "";
        const proficient = wid ? isWeaponProficient(c, wid) === true : false;
        const atkLabel =
          atk !== null
            ? `${escapeHtml(t("attackBonus", "Attack"))}: ${formatMod(atk)}`
            : "—";
        const profTitle = proficient
          ? (atkTitle ? `${atkTitle} · ${t("includesPb", "Includes proficiency bonus")}` : t("includesPb", "Includes proficiency bonus"))
          : atkTitle;
        const star = proficient
          ? `<span class="cs-atk-star is-on" aria-label="${escapeHtml(t("proficient", "Proficient"))}">*</span>`
          : `<span class="cs-atk-star" aria-hidden="true"></span>`;
        return `<div class="cs-weapon-row">
          <select id="cs-weapon-${idx}" class="cs-select" data-weapon-slot="${idx}" aria-label="${escapeHtml(t("weapon", "Weapon"))} ${idx + 1}">${opts}</select>
          <span class="cs-atk-bonus${proficient ? " is-proficient" : ""}" title="${escapeHtml(profTitle)}" aria-label="${escapeHtml(t("attackBonus", "Attack bonus"))}${profTitle ? ` (${profTitle})` : ""}">${atkLabel}</span>
          ${star}
        </div>`;
      })
      .join("");
    const addWeaponDisabled = !canAddWeaponRow(c);
    const addWeaponBtn = `<button type="button" class="cs-btn-link" id="cs-add-weapon"${addWeaponDisabled ? " disabled" : ""}>${escapeHtml(t("addWeapon", "+ Add weapon"))}</button>`;

    const spellcastingLine = formatSpellcastingLine(c);
    const armorGap = armorProficiencyGap(c);
    const combatProf = parseClassCombatProficiency(cls);
    const shieldWarn =
      c.hasShield && cls && !combatProf.shields
        ? `<p class="cs-muted cs-shield-warn">${escapeHtml(t("shieldNotProficient", "Not proficient with shields — expect disadvantage while using one."))}</p>`
        : "";
    const spSection = caster
      ? `<div class="cs-stat-box cs-stat-box--wide">
          <span class="cs-stat-label">Spell Power</span>
          <div class="cs-wd-row">
            <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span><span class="cs-wd-val cs-wd-val--calc">${spMax}</span></div>
            <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("sp-now", c.spellPowerNow, "Spell Power now", { min: 0, max: spMax, display: String(c.spellPowerNow) })}</div>
          </div>
          ${spellcastingLine ? `<p class="cs-muted cs-spellcasting-line">${escapeHtml(spellcastingLine)}</p>` : ""}
        </div>`
      : "";
    const defWarnNote =
      armorGap > 0
        ? `<span class="cs-armor-warn-tag cs-armor-warn-tag--inline" title="${escapeHtml(formatArmorWarning(c))}">${escapeHtml(t("notProficient", "Not proficient"))}</span>`
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
            <p class="cs-print-value">${escapeHtml(cls ? cls.name : "—")}</p>
          </div>
          <div class="cs-field">
            <label class="cs-label" for="cs-subclass">Subclass</label>
            <select id="cs-subclass" class="cs-select"${c.level < subclassMin ? " disabled" : ""}>${subclassOptions}</select>
            <p class="cs-print-value">${escapeHtml(sub ? sub.name : "—")}</p>
          </div>
        </div>

        <div class="cs-life-level">
          ${portraitFrameHtml(c, { pick: "cs-avatar-pick", clear: "cs-avatar-clear", file: "cs-avatar-file" })}
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
            ${defWarnNote}
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">Resolve</span>
            ${stepper("resolve", c.resolve, "Resolve", { min: 0, max: resolveMax(c), display: String(c.resolve) })}
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">PB</span>
            <span class="cs-wd-val cs-wd-val--calc" title="Proficiency Bonus = level ÷ 2, rounded up. Add PB to proficient ability checks and attack rolls (+2×PB Expert, +3×PB Master). Features may also call for flat PB for uses, DCs, or damage.">${formatMod(pb)}</span>
          </div>
        </div>

        ${spSection}

        <div class="cs-pane cs-pane--abilities">
          <h2 class="cs-pane-title">Abilities</h2>
          ${cls ? `<p class="cs-class-summary">${escapeHtml(cls.summary || "")}</p>` : '<p class="cs-muted">Choose a class to see features.</p>'}
          ${renderCombatProficiencyBlock(c, cls)}
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
          <h2 class="cs-pane-title">${escapeHtml(t("equipped", "Equipped"))}</h2>
          <div class="cs-field">
            <label class="cs-label" for="cs-armor">${escapeHtml(t("armor", "Armor"))}</label>
            <select id="cs-armor" class="cs-select">${armorOptions}</select>
            <p class="cs-print-value">${escapeHtml(selectedArmor ? selectedArmor.name : "None")}</p>
            <p class="cs-props">${selectedArmor ? escapeHtml(selectedArmor.props || "—") : "—"}</p>
            ${renderArmorProficiencyWarning(c)}
          </div>
          <div class="cs-equip-summary-row">
            <label class="cs-checkbox-field">
              <input type="checkbox" id="cs-shield"${c.hasShield ? " checked" : ""} />
              ${escapeHtml(t("shield", "Shield"))} (+${SHIELD_BONUS} DEF)
            </label>
          </div>
          ${shieldWarn}
          <div class="cs-weapon-head">
            <h3 class="cs-subhead">${escapeHtml(t("weapons", "Weapons"))}</h3>
            ${addWeaponBtn}
          </div>
          <div class="cs-weapon-rows">${weaponRowsHtml || ""}</div>
          <p class="cs-hint cs-weapon-atk-hint">${escapeHtml(t("attackBonusPbHint", "Attack = FIT + weapon bonus (+ PB when proficient). * means proficient — hover for the breakdown. Pick Remove weapon to drop a row."))}</p>
          <textarea class="cs-textarea" id="cs-equipped" rows="3" placeholder="${escapeHtml(t("equippedPlaceholder", "Notes on weapons, gear, ammo…"))}">${escapeHtml(c.equippedText)}</textarea>
        </div>

        <div class="cs-pane cs-pane--inventory">
          <h2 class="cs-pane-title">${escapeHtml(t("inventory", "Inventory"))}</h2>
          <textarea class="cs-textarea cs-textarea--inventory" id="cs-inventory" placeholder="${escapeHtml(t("inventoryPlaceholder", "What you're carrying…"))}">${escapeHtml(c.inventoryText)}</textarea>
        </div>

        ${showSpells ? renderSpellsPane(c, cls) : ""}
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
    if (el.btnExportPdf) el.btnExportPdf.disabled = !hasChar;
    if (el.btnPrint) el.btnPrint.disabled = !hasChar;
  }

  function render() {
    activeCharacter();
    renderCharSelect();
    updateSheetVisibility();
    renderModals();
    syncDocumentTitle();
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
    syncGrantedSpells(char);
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
      const granted = new Set(char.grantedSpellIds || []);
      const cCap = cantripCap(cls, char.level);
      const cantripIds = char.learnedSpellIds.filter((id) => {
        if (granted.has(id)) return false;
        const s = spellById(id);
        return s && s.circle === 0;
      });
      if (cantripIds.length > cCap) {
        const keep = new Set(cantripIds.slice(0, cCap));
        char.learnedSpellIds = char.learnedSpellIds.filter((id) => {
          if (granted.has(id)) return true;
          const s = spellById(id);
          return !s || s.circle > 0 || keep.has(id);
        });
      }

      const activeCap = computeActiveCap(char);
      if (usesLearnedTier(mode)) {
        const learnedCap = computeLearnedCap(char);
        const learnedLeveledIds = char.learnedSpellIds.filter((id) => {
          if (granted.has(id)) return false;
          const s = spellById(id);
          return s && s.circle > 0;
        });
        if (learnedLeveledIds.length > learnedCap) {
          const keep = new Set(learnedLeveledIds.slice(0, learnedCap));
          char.learnedSpellIds = char.learnedSpellIds.filter((id) => {
            if (granted.has(id)) return true;
            const s = spellById(id);
            return !s || s.circle === 0 || keep.has(id);
          });
        }
        const preparedLeveledIds = char.preparedSpellIds.filter((id) => {
          if (granted.has(id)) return false;
          const s = spellById(id);
          return s && s.circle > 0;
        });
        if (preparedLeveledIds.length > activeCap) {
          const keep = new Set(preparedLeveledIds.slice(0, activeCap));
          char.preparedSpellIds = char.preparedSpellIds.filter((id) => {
            if (granted.has(id)) return true;
            const s = spellById(id);
            return !s || s.circle === 0 || keep.has(id);
          });
        }
      } else {
        const activeLeveledIds = char.learnedSpellIds.filter((id) => {
          if (granted.has(id)) return false;
          const s = spellById(id);
          return s && s.circle > 0;
        });
        if (activeLeveledIds.length > activeCap) {
          const keep = new Set(activeLeveledIds.slice(0, activeCap));
          char.learnedSpellIds = char.learnedSpellIds.filter((id) => {
            if (granted.has(id)) return true;
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
    talentViewName = null;
    skillModalOpen = false;
    languageModalOpen = false;
    talentModalOpen = false;
    talentModalExpandedIds.clear();
    ddbModalOpen = false;
    ddbReview = null;
    ddbFallbackVisible = false;
    weaponPickPending = false;
    if (!id) {
      store.activeId = null;
      saveStore();
      render();
      syncToolbarFoldout(false);
      return;
    }
    if (store.characters.some((c) => c.id === id)) {
      store.activeId = id;
      saveStore();
      render();
      syncToolbarFoldout(true);
    }
  }

  function newCharacter() {
    spellModalOpen = false;
    spellViewId = null;
    talentViewName = null;
    skillModalOpen = false;
    languageModalOpen = false;
    talentModalOpen = false;
    talentModalExpandedIds.clear();
    ddbModalOpen = false;
    ddbReview = null;
    ddbFallbackVisible = false;
    weaponPickPending = false;
    const c = defaultCharacter();
    store.characters.push(c);
    store.activeId = c.id;
    saveStore();
    render();
    syncToolbarFoldout(true);
  }

  async function deleteCharacter() {
    if (!char || !window.ymiatDialog) return;
    const name = char.name || "Unnamed";
    const message = t("deleteCharacterConfirm", 'Delete "{name}"? This cannot be undone.').replace("{name}", name);
    const ok = await window.ymiatDialog({
      title: t("deleteCharacter", "Delete character"),
      message: message,
      confirmLabel: t("deleteCharacterAction", "Delete"),
      cancelLabel: t("cancel", "Cancel"),
    });
    if (!ok || !char) return;
    spellModalOpen = false;
    spellViewId = null;
    talentViewName = null;
    skillModalOpen = false;
    languageModalOpen = false;
    talentModalOpen = false;
    talentModalExpandedIds.clear();
    ddbModalOpen = false;
    ddbReview = null;
    ddbFallbackVisible = false;
    store.characters = store.characters.filter((c) => c.id !== char.id);
    store.activeId = store.characters.length ? store.characters[0].id : null;
    saveStore();
    render();
    syncToolbarFoldout(Boolean(store.activeId));
  }



  // ─── D&D Beyond import ──────────────────────────────────────────────────────
  // Direct browser fetch to character-service.dndbeyond.com is blocked by CORS.
  // With window.YMIAT_DDB_PROXY_URL set (Cloudflare Worker in workers/ddb-character-proxy),
  // fetch goes through that proxy — same pattern as dprcalc.com /api/c.
  // Without a proxy, paste the public character JSON URL contents into the modal.
  const DDB_ALIASES = {
    lineage: {
      halfling: "Smallfolk",
      "half orc": "Orc",
      genasi: "Elemental Scion",
      warforged: "Gearforged",
    },
    background: {
      sage: "Scholar",
    },
  };

  function extractDdbId(input) {
    if (!input) return null;
    const m = String(input).match(/\/characters\/(\d+)/);
    if (m) return m[1];
    const bare = String(input).trim();
    return /^\d+$/.test(bare) ? bare : null;
  }

  function ddbNormalizeName(name) {
    return String(name || "")
      .toLowerCase()
      .replace(/\([^)]*\)/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function ddbMatchExact(list, name) {
    if (!name) return null;
    const target = ddbNormalizeName(name);
    if (!target) return null;
    return list.find((item) => ddbNormalizeName(item.name) === target) || null;
  }

  const SUBCLASS_PREFIXES = [
    "path of the", "path of", "college of", "circle of the", "circle of",
    "domain of", "oath of the", "oath of", "way of the", "way of",
    "school of", "martial archetype", "roguish archetype", "ranger archetype",
    "sacred oath", "divine domain", "primal path", "bard college",
    "otherworldly patron", "bloodline of",
  ];

  function ddbNormalizeSubclass(name) {
    let n = ddbNormalizeName(name).replace(/\bbloodline\b/, "").trim();
    for (const prefix of SUBCLASS_PREFIXES) {
      if (n.startsWith(prefix + " ")) {
        n = n.slice(prefix.length).trim();
        break;
      }
    }
    return n;
  }

  function ddbMatchSubclass(subclasses, name) {
    if (!name) return null;
    const target = ddbNormalizeSubclass(name);
    if (!target) return null;
    let hit = subclasses.find((s) => ddbNormalizeSubclass(s.name) === target);
    if (hit) return hit;
    hit = subclasses.find((s) => {
      const n = ddbNormalizeSubclass(s.name);
      return n.length > 2 && (target.includes(n) || n.includes(target));
    });
    return hit || null;
  }

  // Ability composites per conversion.html#converting-ability-scores:
  // Fitness = floor((STR+DEX+CON)/3); Insight = floor((INT+WIS)/2);
  // Willpower = floor((WIS+CHA)/2). Each composite then uses the standard
  // 5e modifier formula floor((score-10)/2).
  function ddbComputeAbilities(scores) {
    const mod = (score) => Math.floor((score - 10) / 2);
    const fit = Math.floor((scores.str + scores.dex + scores.con) / 3);
    const ins = Math.floor((scores.int + scores.wis) / 2);
    const wil = Math.floor((scores.wis + scores.cha) / 2);
    return {
      fit: clampAbility(mod(fit)),
      ins: clampAbility(mod(ins)),
      wil: clampAbility(mod(wil)),
    };
  }

  // D&D Beyond's raw char.stats/overrideStats/bonusStats only carry the
  // character-builder base scores; racial/feat/item bonuses live in the
  // modifiers lists and must be folded in separately (mirrors how D&D
  // Beyond's own character sheet computes final scores).
  function ddbRawScores(char) {
    const ids = { str: 1, dex: 2, con: 3, int: 4, wis: 5, cha: 6 };
    const statSubTypeToId = {
      "strength-score": 1, "dexterity-score": 2, "constitution-score": 3,
      "intelligence-score": 4, "wisdom-score": 5, "charisma-score": 6,
    };
    const allMods = [
      ...(char.modifiers?.class || []),
      ...(char.modifiers?.race || []),
      ...(char.modifiers?.background || []),
      ...(char.modifiers?.feat || []),
      ...(char.modifiers?.item || []),
    ];
    const modBonuses = allMods
      .filter((m) => m.type === "bonus" && statSubTypeToId[m.subType] && m.value != null)
      .map((m) => ({ id: statSubTypeToId[m.subType], value: m.value }));
    const bonusStats = [...(char.bonusStats || []).filter((s) => s.value != null), ...modBonuses];
    const stats = char.stats || [];
    const overrides = char.overrideStats || [];
    const getVal = (id) => {
      const base = stats.find((s) => s.id === id)?.value ?? 10;
      const override = overrides.find((s) => s.id === id)?.value;
      if (override != null) return override;
      const bonus = bonusStats.filter((b) => b.id === id).reduce((sum, b) => sum + (b.value || 0), 0);
      return base + bonus;
    };
    const out = {};
    Object.keys(ids).forEach((key) => {
      out[key] = getVal(ids[key]);
    });
    return out;
  }

  function ddbEquippedName(item) {
    return (item?.definition?.name || "").replace(/^\+\d+\s+/, "").trim();
  }

  // Per conversion.html's guidance (and Tales of the Valiant's own conversion
  // guide): a 5e race splits into Lineage (innate/physical traits, matched by
  // name above) and Heritage (learned/cultural traits — languages, weapon and
  // tool training, trained skills). Heritage names are original YMIAT/ToV
  // cultural concepts with no 5e name to match against, so instead of a
  // lookup table this scores every heritage by how much its granted
  // languages/skills overlap with what the race actually grants in the
  // fetched character — the same signal the conversion guide says to keep.
  const DDB_LANGUAGE_TO_YMIAT = {
    orc: "Orcish", common: null, dwarvish: "Dwarvish", elvish: "Elvish",
    giant: "Giant", gnomish: "Gnomish", goblin: "Goblin", halfling: "Halfling",
    abyssal: "Abyssal", celestial: "Celestial", "deep speech": "Deep Speech",
    draconic: "Draconic", infernal: "Infernal", primordial: "Primordial",
    sylvan: "Sylvan", undercommon: "Undercommon",
  };

  const DDB_SKILL_SUBTYPE_TO_NAME = {
    acrobatics: "Acrobatics", "animal-handling": "Animal Handling", arcana: "Arcana",
    athletics: "Athletics", deception: "Deception", history: "History", insight: "Insight",
    intimidation: "Intimidation", investigation: "Investigation", medicine: "Medicine",
    nature: "Nature", perception: "Perception", performance: "Performance",
    persuasion: "Persuasion", religion: "Religion", "sleight-of-hand": "Sleight of Hand",
    stealth: "Stealth", survival: "Survival",
  };

  function ddbRaceLanguages(char) {
    return (char.modifiers?.race || [])
      .filter((m) => m.type === "language")
      .map((m) => DDB_LANGUAGE_TO_YMIAT[m.subType])
      .filter(Boolean);
  }

  function ddbRaceSkillProficiencies(char) {
    return (char.modifiers?.race || [])
      .filter((m) => m.type === "proficiency" && DDB_SKILL_SUBTYPE_TO_NAME[m.subType])
      .map((m) => DDB_SKILL_SUBTYPE_TO_NAME[m.subType]);
  }

  // Scores each heritage against the race's languages/skills and returns the
  // best match plus its score, or null if nothing scored above 0 — heritage
  // is thematic/roleplay content, so a guess is only worth making when there's
  // an actual overlap to point to, never a blind default.
  function ddbMatchHeritage(char) {
    const languages = ddbRaceLanguages(char);
    const skills = ddbRaceSkillProficiencies(char);
    if (!languages.length && !skills.length) return null;
    let best = null;
    let bestScore = 0;
    for (const heritage of data.heritages) {
      const bodyLower = (heritage.body || "").toLowerCase();
      let score = 0;
      const matchedLangs = languages.filter((lang) => bodyLower.includes(lang.toLowerCase()));
      const matchedSkills = skills.filter((skill) => bodyLower.includes(skill.toLowerCase()));
      score += matchedLangs.length * 3;
      score += matchedSkills.length * 2;
      if (score > bestScore) {
        bestScore = score;
        best = { heritage, matchedLangs, matchedSkills };
      }
    }
    return best;
  }

  // BUSINESS: YMIAT gear costs 6× the D&D gold price, paid in silver, so an imported
  // purse must buy the same items as on the gear tables. Exchange is 1 gp = 10 sp = 100 cp.
  function ddbCurrencyToYmiat(curr) {
    const n = (v) => Math.max(0, Number(v) || 0);
    const src = curr || {};
    const ddbCopper = n(src.cp) + n(src.sp) * 10 + n(src.ep) * 50 + n(src.gp) * 100 + n(src.pp) * 1000;
    const ymiatCopper = Math.round(ddbCopper * 6 / 10);
    return {
      gold: Math.floor(ymiatCopper / 100),
      silver: Math.floor((ymiatCopper % 100) / 10),
      copper: ymiatCopper % 10,
    };
  }

  // Maps a fetched D&D Beyond character JSON payload onto a fresh YMIAT
  // character. Returns { character, report } where report lists every field
  // that couldn't be matched, so the caller can tell the player what to set
  // by hand rather than silently guessing wrong.
  function convertDdbCharacter(payload) {
    const char = payload?.data;
    if (!char) throw new Error("Unexpected D&D Beyond response — is the character set to Public?");

    const report = [];
    const c = defaultCharacter();
    c.name = char.name || c.name;

    const classes = Array.isArray(char.classes) ? char.classes : [];
    const totalLevel = classes.reduce((sum, cl) => sum + (cl.level || 0), 0) || 1;
    const range = levelRange();
    c.level = Math.min(range.max, Math.max(range.min, Math.ceil(totalLevel / 2)));
    c.xp = xpThreshold(c.level);

    const scores = ddbRawScores(char);
    c.abilities = ddbComputeAbilities(scores);

    if (classes.length > 1) {
      report.push(`Multiclassed (${classes.map((cl) => `${cl.definition?.name || "?"} ${cl.level || 0}`).join(" / ")}) — only the highest-level class was imported; YMIAT tracks one class per character.`);
    }
    const primaryClass = classes.slice().sort((a, b) => (b.level || 0) - (a.level || 0))[0];
    const classMatch = primaryClass ? ddbMatchExact(data.classes, primaryClass.definition?.name) : null;
    if (classMatch) {
      c.classId = classMatch.id;
      if (c.level >= (range.subclassMin || 2) && primaryClass.subclassDefinition?.name) {
        const subMatch = ddbMatchSubclass(classMatch.subclasses || [], primaryClass.subclassDefinition.name);
        if (subMatch) c.subclassId = subMatch.id;
        else report.push(`Subclass "${primaryClass.subclassDefinition.name}" has no clear YMIAT equivalent for ${classMatch.name} — pick one manually.`);
      }
    } else if (primaryClass) {
      report.push(`Class "${primaryClass.definition?.name || "?"}" not found in YMIAT — pick one manually.`);
    }

    const raceName = char.race?.fullName || char.race?.baseName || "";
    let lineageMatch = ddbMatchExact(data.lineages, char.race?.fullName) || ddbMatchExact(data.lineages, char.race?.baseName);
    if (!lineageMatch) {
      const aliasKey = ddbNormalizeName(char.race?.baseName || raceName);
      const alias = DDB_ALIASES.lineage[aliasKey];
      if (alias) lineageMatch = ddbMatchExact(data.lineages, alias);
    }
    if (lineageMatch) {
      c.lineageId = lineageMatch.id;
      Object.assign(c, parseLineageDefaults(lineageMatch));
    } else if (raceName) {
      report.push(`Race "${raceName}" has no clear YMIAT lineage match — pick one manually.`);
    }

    const heritageMatch = ddbMatchHeritage(char);
    if (heritageMatch) {
      c.heritageId = heritageMatch.heritage.id;
      const why = [...heritageMatch.matchedLangs.map((l) => `${l} language`), ...heritageMatch.matchedSkills.map((s) => `${s} proficiency`)].join(", ");
      report.push(`Heritage guessed as "${heritageMatch.heritage.name}" based on your race's ${why} — verify this fits, or pick a different one (heritage is cultural/roleplay, not a hard rule).`);
    } else {
      report.push("No confident Heritage match from your race's languages/proficiencies — pick one manually (see the conversion guide: Heritage carries a race's learned/cultural traits, Lineage carries its innate/physical ones).");
    }

    const bgName = char.background?.definition?.name || "";
    let bgMatch = ddbMatchExact(data.backgrounds, bgName);
    if (!bgMatch && bgName) {
      const alias = DDB_ALIASES.background[ddbNormalizeName(bgName)];
      if (alias) bgMatch = ddbMatchExact(data.backgrounds, alias);
    }
    if (bgMatch) c.backgroundId = bgMatch.id;
    else if (bgName) {
      report.push(`Background "${bgName}" has no clear YMIAT match — pick one manually.`);
    }

    const inventory = Array.isArray(char.inventory) ? char.inventory : [];
    const equipped = inventory.filter((item) => item.equipped && item.definition);
    let shieldFound = false;
    let armorMatch = null;
    for (const item of equipped) {
      const nm = ddbEquippedName(item);
      if (/shield/i.test(nm)) {
        shieldFound = true;
        continue;
      }
      if (item.definition.armorClass != null) {
        const m = ddbMatchExact(ARMOR, nm);
        if (m) armorMatch = m;
      }
    }
    if (armorMatch) c.armorId = armorMatch.id;
    c.hasShield = shieldFound;

    // Weapons: equipped first, then unequipped; fill weaponIds (max WEAPON_SLOT_COUNT).
    const weaponIds = [];
    const pushWeapon = (item) => {
      if (weaponIds.length >= WEAPON_SLOT_COUNT) return;
      const nm = ddbEquippedName(item);
      if (/shield/i.test(nm)) return;
      const m = ddbMatchExact(WEAPONS, nm);
      if (m && !weaponIds.includes(m.id)) weaponIds.push(m.id);
    };
    equipped.forEach(pushWeapon);
    inventory.filter((item) => item && item.definition && !item.equipped).forEach(pushWeapon);
    c.weaponIds = weaponIds.slice(0, WEAPON_SLOT_COUNT);
    c.weaponId = c.weaponIds.find(Boolean) || "";
    weaponPickPending = false;

    // Every DDB item line goes in the inventory notes, including past the old slot cap.
    const invLines = [];
    inventory.forEach((item) => {
      if (!item || !item.definition) return;
      const nm = ddbEquippedName(item);
      if (!nm) return;
      const qty = Number(item.quantity) || 1;
      invLines.push(qty > 1 ? `${nm} ×${qty}` : nm);
    });
    c.inventoryText = invLines.join("\n");

    const curr = char.currencies || {};
    c.currency = ddbCurrencyToYmiat(curr);
    const hadCoins = ["cp", "sp", "ep", "gp", "pp"].some((k) => (Number(curr[k]) || 0) > 0);
    if (hadCoins) {
      report.push(`Currency converted to YMIAT prices: ${c.currency.gold} gold, ${c.currency.silver} silver, ${c.currency.copper} copper.`);
    }

    if (char.race?.weightSpeeds?.normal?.walk) c.speed = char.race.weightSpeeds.normal.walk;

    const spMax = computeSpellPowerMax(c);
    c.spellPowerNow = spMax !== null ? spMax : 0;

    applyDdbSpells(c, char, report);
    report.push("Talents aren't auto-imported — pick your background/class talent on this sheet.");

    normalizeCharacter(c);
    syncGrantedSpells(c);
    return { character: c, report };
  }

  function ddbCollectSpellEntries(char) {
    const entries = [];
    const pushList = (list) => {
      (list || []).forEach((s) => {
        if (s) entries.push(s);
      });
    };
    const spells = char.spells || {};
    pushList(spells.class);
    pushList(spells.race);
    pushList(spells.feat);
    pushList(spells.item);
    pushList(spells.background);
    (char.classSpells || []).forEach((block) => pushList(block.spells));
    pushList(char.knownSpells);
    pushList(char.subclassSpells);
    return entries;
  }

  function applyDdbSpells(c, ddbChar, report) {
    const cls = findClass(c);
    const mode = spellMode(cls);
    if (!mode) {
      report.push("Class is not a caster on this sheet — D&D Beyond spells were skipped.");
      return;
    }

    const entries = ddbCollectSpellEntries(ddbChar);
    if (!entries.length) {
      report.push("No spells found on the D&D Beyond character to import.");
      return;
    }

    const unmatched = [];
    const notOnListCantrips = [];
    const notOnListSpells = [];
    const learned = [];
    const prepared = [];
    const seen = new Set();
    // Only import spells/cantrips the sheet can manage (class list + circle for level);
    // otherwise they land in learnedSpellIds with no unlearn checkbox.
    const eligibleIds = new Set(eligibleSpells(c).map((s) => s.id));

    entries.forEach((entry) => {
      const def = entry.definition || entry;
      const name = def.name || entry.name;
      if (!name) return;
      const match = ddbMatchExact(SPELLS, name);
      if (!match) {
        unmatched.push(name);
        return;
      }
      if (!eligibleIds.has(match.id)) {
        const bucket = match.circle === 0 ? notOnListCantrips : notOnListSpells;
        if (!bucket.includes(name)) bucket.push(name);
        return;
      }
      if (seen.has(match.id)) {
        if (entry.prepared || entry.alwaysPrepared || def.alwaysPrepared) {
          if (!prepared.includes(match.id)) prepared.push(match.id);
        }
        return;
      }
      seen.add(match.id);
      learned.push(match.id);
      if (entry.prepared || entry.alwaysPrepared || def.alwaysPrepared) {
        prepared.push(match.id);
      }
    });

    const cantrips = learned.filter((id) => {
      const s = spellById(id);
      return s && s.circle === 0;
    });
    const leveled = learned.filter((id) => {
      const s = spellById(id);
      return s && s.circle > 0;
    });

    const isKnownMode = mode === "known" || mode === "known-formula";
    c.learnedSpellIds = cantrips.concat(leveled);
    if (isKnownMode) {
      c.preparedSpellIds = [];
    } else if (mode === "full") {
      const prepSource = prepared.length ? prepared : leveled;
      c.learnedSpellIds = cantrips.concat(prepSource);
      c.preparedSpellIds = prepSource.slice();
    } else {
      // spellbook / spellbook-fixed
      c.preparedSpellIds = prepared.filter((id) => c.learnedSpellIds.includes(id));
    }

    const beforeLearn = c.learnedSpellIds.length;
    const beforePrep = c.preparedSpellIds.length;
    const prevActive = char;
    char = c;
    try {
      clampWoundsAndSp();
    } finally {
      char = prevActive;
    }

    // Known casters: keep the full imported known list (cantrips + leveled) for
    // sheet/export even if over YMIAT caps. Soft over-cap on import only.
    // Never re-add anything outside eligibleIds (unlearnable otherwise).
    if (isKnownMode) {
      const eligibleCantrips = cantrips.filter((id) => eligibleIds.has(id));
      const eligibleLeveled = leveled.filter((id) => eligibleIds.has(id));
      c.learnedSpellIds = eligibleCantrips.concat(eligibleLeveled);
      const activeCap = computeActiveCap(c);
      const cCap = cantripCap(cls, c.level);
      if (eligibleCantrips.length > cCap) {
        report.push(
          `Imported ${eligibleCantrips.length} cantrip(s) (YMIAT cantrip cap is ${cCap}) — all kept for listing; trim in Manage Spells if needed.`
        );
      }
      if (eligibleLeveled.length > activeCap) {
        report.push(
          `Imported ${eligibleLeveled.length} known spell(s) (YMIAT known cap is ${activeCap}) — all kept for listing; trim in Manage Spells if needed.`
        );
      }
    } else {
      // Belt-and-suspenders: drop anything not on this class's YMIAT list.
      c.learnedSpellIds = c.learnedSpellIds.filter((id) => eligibleIds.has(id));
      c.preparedSpellIds = c.preparedSpellIds.filter((id) => c.learnedSpellIds.includes(id));
      if (c.learnedSpellIds.length < beforeLearn || c.preparedSpellIds.length < beforePrep) {
        report.push("Some imported spells were trimmed to fit YMIAT cantrip/known/prepared caps for this class and level.");
      }
    }

    if (unmatched.length) {
      const sample = unmatched.slice(0, 8).join(", ");
      const more = unmatched.length > 8 ? ` (+${unmatched.length - 8} more)` : "";
      report.push(`Could not match ${unmatched.length} D&D Beyond spell(s) to YMIAT: ${sample}${more}.`);
    }
    function pushSkipped(kind, names) {
      if (!names.length) return;
      const sample = names.slice(0, 8).join(", ");
      const more = names.length > 8 ? ` (+${names.length - 8} more)` : "";
      report.push(
        `Skipped ${names.length} ${kind} not on this class's YMIAT list (not marked known): ${sample}${more}.`
      );
    }
    pushSkipped("cantrip(s)", notOnListCantrips);
    pushSkipped("spell(s)", notOnListSpells);

    if (c.learnedSpellIds.length) {
      const names = c.learnedSpellIds
        .map(spellById)
        .filter(Boolean)
        .map((s) => s.name);
      const sample = names.slice(0, 12).join(", ");
      const more = names.length > 12 ? ` (+${names.length - 12} more)` : "";
      const kind = isKnownMode ? "known" : mode === "full" ? "prepared" : "spellbook";
      report.push(`Imported ${names.length} ${kind} spell(s): ${sample}${more}.`);
    }
  }

  async function applyDdbImport(payload) {
    const { character, report } = convertDdbCharacter(payload);
    const remote = ddbAvatarSourceUrl(payload && payload.data);
    if (remote) {
      try {
        const dataUrl = await fetchDdbPortrait(remote);
        if (dataUrl) character.portraitUrl = dataUrl;
      } catch (_) { /* leave empty if the avatar cannot be fetched */ }
    }
    store.characters.push(character);
    store.activeId = character.id;
    saveStore();
    ddbModalOpen = false;
    ddbFallbackVisible = false;
    if (report.length) {
      ddbReview = { name: character.name || "Unnamed", lines: report.slice() };
    } else {
      ddbReview = null;
    }
    render();
    syncToolbarFoldout(true);
  }

  async function fetchDdbCharacter(idOrUrl) {
    const id = extractDdbId(idOrUrl);
    if (!id) throw new Error("Couldn't find a D&D Beyond character ID in that input.");

    const proxyBase = String(window.YMIAT_DDB_PROXY_URL || "").replace(/\/$/, "");
    if (!proxyBase) {
      throw new Error("No proxy configured — use the paste fallback below.");
    }
    const url = `${proxyBase}/?id=${encodeURIComponent(id)}`;

    const res = await fetch(url, { headers: { Accept: "application/json" } });
    let payload = null;
    try {
      payload = await res.json();
    } catch (_) {
      payload = null;
    }

    if (!res.ok) {
      if (payload && payload.error === "private") {
        throw new Error("Character is private — set it to Public on D&D Beyond, then try again.");
      }
      if (payload && payload.error === "not_found") {
        throw new Error("Character not found on D&D Beyond.");
      }
      throw new Error(`Proxy returned HTTP ${res.status}.`);
    }
    if (!payload || !payload.data) {
      throw new Error("Unexpected response — is the character set to Public?");
    }
    return payload;
  }

  function ddbProxyConfigured() {
    return Boolean(String(window.YMIAT_DDB_PROXY_URL || "").trim());
  }

  function ddbJsonUrl(idOrUrl) {
    const id = extractDdbId(idOrUrl);
    return id ? `https://character-service.dndbeyond.com/character/v5/character/${id}` : null;
  }

  function renderDdbReviewModal() {
    if (!ddbReview) {
      el.modalRoot.innerHTML = "";
      return;
    }
    const bullets = (ddbReview.lines || [])
      .map((line) => `<li>${escapeHtml(line)}</li>`)
      .join("");
    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-ddb-review-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="Import review">
        <div class="cs-modal-header">
          <h2>Imported “${escapeHtml(ddbReview.name)}”</h2>
          <button type="button" class="cs-modal-close" id="cs-ddb-review-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-body">
          <p class="cs-hint">Review these notes and adjust the sheet if needed.</p>
          <ul class="cs-ddb-review-list">${bullets}</ul>
          <div class="cs-ddb-actions">
            <button type="button" class="btn" id="cs-ddb-review-done">Done</button>
          </div>
        </div>
      </div>
    </div>`;
  }

  function renderDdbImportModal() {
    const proxyOn = ddbProxyConfigured();
    const showFallback = !proxyOn || ddbFallbackVisible;
    const fallbackHidden = showFallback ? "" : " hidden";
    const primaryHint = proxyOn
      ? "Paste a Public D&amp;D Beyond character URL (or ID), then Import — fetched via proxy in one step."
      : "Proxy is not configured. Use the paste fallback below.";
    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cs-ddb-overlay">
      <div class="cs-modal cs-modal--view" role="dialog" aria-modal="true" aria-label="Import from D&D Beyond">
        <div class="cs-modal-header">
          <h2>Import from D&amp;D Beyond</h2>
          <button type="button" class="cs-modal-close" id="cs-ddb-close" aria-label="Close">×</button>
        </div>
        <div class="cs-modal-body">
          <p class="cs-hint">${primaryHint} See <a href="${rp("rules/conversion.html")}" target="_blank" rel="noopener">conversion rules</a>. Talents stay manual.</p>
          <label class="cs-label" for="cs-ddb-input">Character URL or ID</label>
          <input type="text" id="cs-ddb-input" class="cs-input" placeholder="https://www.dndbeyond.com/characters/12345678" autocomplete="off" />
          ${
            proxyOn
              ? `<div class="cs-ddb-actions">
            <button type="button" class="btn" id="cs-ddb-import">Import</button>
          </div>`
              : ""
          }
          <p id="cs-ddb-status" class="cs-hint" aria-live="polite">${
            proxyOn ? "Enter a URL, then Import." : "Paste JSON below to import."
          }</p>
          <div id="cs-ddb-fallback" class="cs-ddb-fallback"${fallbackHidden}>
            <h3 class="cs-subhead">Paste fallback</h3>
            <ol class="cs-ddb-steps">
              <li>Open the <a id="cs-ddb-json-link" href="#" target="_blank" rel="noopener">character JSON</a> (Public characters only).</li>
              <li>Select all → copy (<kbd>Ctrl</kbd>+<kbd>A</kbd>, <kbd>Ctrl</kbd>+<kbd>C</kbd>).</li>
              <li>Paste here, then Import pasted JSON.</li>
            </ol>
            <div class="cs-ddb-actions cs-ddb-actions--row">
              <button type="button" class="btn cs-btn-secondary" id="cs-ddb-paste">Paste from clipboard</button>
            </div>
            <label class="cs-label" for="cs-ddb-json">Character JSON</label>
            <textarea id="cs-ddb-json" class="cs-input" rows="5" placeholder="Paste JSON here (Ctrl+V)…" spellcheck="false"></textarea>
            <div class="cs-ddb-actions">
              <button type="button" class="btn" id="cs-ddb-import-paste">Import pasted JSON</button>
            </div>
          </div>
        </div>
      </div>
    </div>`;
    updateDdbJsonLink();
    const input = document.getElementById("cs-ddb-input");
    if (input) {
      requestAnimationFrame(() => input.focus());
    }
  }

  function setDdbStatus(msg, isHtml) {
    const status = document.getElementById("cs-ddb-status");
    if (!status) return;
    if (isHtml) status.innerHTML = msg;
    else status.textContent = msg;
  }

  function showDdbFallback() {
    ddbFallbackVisible = true;
    const block = document.getElementById("cs-ddb-fallback");
    if (block) block.hidden = false;
    updateDdbJsonLink();
  }

  function updateDdbJsonLink() {
    const link = document.getElementById("cs-ddb-json-link");
    const input = document.getElementById("cs-ddb-input");
    if (!link) return;
    const url = ddbJsonUrl(input ? input.value.trim() : "");
    if (url) {
      link.href = url;
      link.removeAttribute("aria-disabled");
      link.classList.remove("is-disabled");
    } else {
      link.href = "#";
      link.setAttribute("aria-disabled", "true");
      link.classList.add("is-disabled");
    }
  }

  function parseDdbPayloadText(raw) {
    const text = String(raw || "").trim();
    if (!text) throw new Error("Nothing to import — paste the JSON first.");
    const payload = JSON.parse(text);
    if (!payload || !payload.data) {
      throw new Error("JSON must include a top-level \"data\" object (open the character JSON URL, not the character sheet page).");
    }
    return payload;
  }

  function fillDdbJsonBox(raw) {
    const jsonBox = document.getElementById("cs-ddb-json");
    if (jsonBox) jsonBox.value = typeof raw === "string" ? raw : JSON.stringify(raw);
  }

  async function tryImportDdbFromBox() {
    const jsonBox = document.getElementById("cs-ddb-json");
    const payload = parseDdbPayloadText(jsonBox ? jsonBox.value : "");
    await applyDdbImport(payload);
  }

  async function importDdbViaProxy() {
    const input = document.getElementById("cs-ddb-input");
    const btn = document.getElementById("cs-ddb-import");
    const idOrUrl = input ? input.value.trim() : "";
    if (!extractDdbId(idOrUrl)) {
      setDdbStatus("Enter a valid D&D Beyond character URL or numeric ID first.");
      if (input) input.focus();
      return;
    }
    if (!ddbProxyConfigured()) {
      setDdbStatus("No proxy configured — use the paste fallback below.");
      showDdbFallback();
      return;
    }
    setDdbStatus("Importing…");
    if (btn) btn.disabled = true;
    try {
      const payload = await fetchDdbCharacter(idOrUrl);
      await applyDdbImport(payload);
    } catch (err) {
      setDdbStatus(err && err.message ? err.message : "Import failed.");
      showDdbFallback();
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  /**
   * Home page (and deep links) pass ?ddb=<url-or-id>. After the sheet boots,
   * run the same proxy import, then strip the query so refresh doesn't re-import.
   */
  async function maybeImportDdbFromQuery() {
    let params;
    try {
      params = new URLSearchParams(window.location.search || "");
    } catch (_) {
      return;
    }
    const raw = params.get("ddb");
    if (raw == null || raw === "") return;
    const idOrUrl = String(raw).trim();
    try {
      history.replaceState(null, "", window.location.pathname + window.location.hash);
    } catch (_) {
      /* ignore */
    }
    if (!extractDdbId(idOrUrl)) {
      ddbFallbackVisible = true;
      ddbModalOpen = true;
      render();
      const input = document.getElementById("cs-ddb-input");
      if (input) input.value = idOrUrl;
      setDdbStatus("Enter a valid D&D Beyond character URL or numeric ID first.");
      return;
    }
    if (!ddbProxyConfigured()) {
      ddbFallbackVisible = true;
      ddbModalOpen = true;
      render();
      const input = document.getElementById("cs-ddb-input");
      if (input) input.value = idOrUrl;
      setDdbStatus("No proxy configured — use the paste fallback below.");
      updateDdbJsonLink();
      return;
    }
    ddbModalOpen = true;
    ddbFallbackVisible = false;
    render();
    const input = document.getElementById("cs-ddb-input");
    if (input) input.value = idOrUrl;
    setDdbStatus("Importing…");
    try {
      const payload = await fetchDdbCharacter(idOrUrl);
      await applyDdbImport(payload);
    } catch (err) {
      showDdbFallback();
      setDdbStatus(err && err.message ? err.message : "Import failed.");
      updateDdbJsonLink();
    }
  }

  async function pasteDdbClipboard() {
    const jsonBox = document.getElementById("cs-ddb-json");
    try {
      if (!navigator.clipboard || !navigator.clipboard.readText) {
        setDdbStatus("Clipboard read isn’t available here — click the JSON box and press Ctrl+V (⌘+V).");
        if (jsonBox) jsonBox.focus();
        return;
      }
      const text = await navigator.clipboard.readText();
      if (!String(text || "").trim()) {
        setDdbStatus("Clipboard is empty — copy the JSON tab first (Ctrl+A, Ctrl+C).");
        return;
      }
      fillDdbJsonBox(text);
      parseDdbPayloadText(text);
      setDdbStatus("JSON looks good — click Import pasted JSON.");
      const convertBtn = document.getElementById("cs-ddb-import-paste");
      if (convertBtn) convertBtn.focus();
    } catch (err) {
      if (err && err.name === "NotAllowedError") {
        setDdbStatus("Clipboard permission denied — click the JSON box and press Ctrl+V (⌘+V), then Import.");
      } else if (err instanceof SyntaxError) {
        setDdbStatus("Clipboard isn’t valid character JSON. Open the JSON link, copy everything, try again.");
      } else {
        setDdbStatus(err && err.message ? err.message : "Couldn’t read clipboard — paste manually into the box.");
      }
      if (jsonBox) jsonBox.focus();
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
      char.resolve = Math.min(resolveMax(char), Math.max(0, char.resolve + delta));
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
    if (el.btnImportDdb) {
      el.btnImportDdb.addEventListener("click", () => {
        ddbReview = null;
        ddbFallbackVisible = !ddbProxyConfigured();
        ddbModalOpen = true;
        renderModals();
      });
    }
    if (el.btnPrint) {
      el.btnPrint.addEventListener("click", printPregenSheet);
    }
    if (el.btnExportPdf) {
      el.btnExportPdf.addEventListener("click", exportPregenPdf);
    }
    if (el.toolbarToggle && el.toolbar) {
      el.toolbarToggle.addEventListener("click", () => {
        const open = !el.toolbar.classList.contains("is-open");
        syncToolbarFoldout(Boolean(char), open);
      });
    }

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
        spellModalExpandedIds.clear();
        spellViewId = null;
        renderModals();
        return;
      }
      if (e.target.closest("#cs-avatar-pick")) {
        const input = el.sheet.querySelector("#cs-avatar-file");
        if (input) input.click();
        return;
      }
      if (e.target.closest("#cs-avatar-clear")) {
        if (!char || !char.portraitUrl) return;
        portraitClearOpen = true;
        renderModals();
        return;
      }
      if (e.target.closest("#cs-add-weapon")) {
        if (!char) return;
        if (addWeaponRow(char)) persistAndRender();
        return;
      }
      if (e.target.closest("#cs-choose-skills")) {
        skillModalOpen = true;
        renderModals();
        return;
      }
      if (e.target.closest("#cs-choose-languages")) {
        languageModalOpen = true;
        renderModals();
        return;
      }
      if (e.target.closest("#cs-choose-talent")) {
        talentModalOpen = true;
        talentModalExpandedIds.clear();
        renderModals();
        return;
      }
      const chip = e.target.closest(".cs-spell-chip[data-spell-view]");
      if (chip) {
        spellViewId = chip.dataset.spellView;
        renderModals();
        return;
      }
      const talentChip = e.target.closest(".cs-spell-chip[data-talent-view]");
      if (talentChip) {
        talentViewName = talentChip.dataset.talentView;
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
      if (t.id === "cs-inventory") {
        char.inventoryText = t.value;
        saveStore();
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
      if (t.id === "cs-avatar-file" && t.files && t.files[0]) {
        const file = t.files[0];
        blobToPortrait(file).then((dataUrl) => {
          if (!char) return;
          char.portraitUrl = dataUrl;
          persistAndRender();
        }).catch(() => {});
        return;
      }
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
      } else if (t.dataset && t.dataset.weaponSlot != null) {
        const slot = parseInt(t.dataset.weaponSlot, 10);
        if (!Array.isArray(char.weaponIds)) char.weaponIds = [];
        if (Number.isFinite(slot) && slot >= 0 && slot < char.weaponIds.length) {
          const next = t.value || "";
          if (!next) {
            // Choosing empty / "Remove weapon" removes this row and compacts.
            weaponPickPending = false;
            char.weaponIds.splice(slot, 1);
          } else {
            char.weaponIds[slot] = next;
            if (slot === char.weaponIds.length - 1) weaponPickPending = false;
          }
          normalizeWeaponIds(char);
          persistAndRender();
        }
      } else if (t.id === "cs-shield") {
        char.hasShield = t.checked;
        persistAndRender();
      } else if (t.id === "cs-xp") {
        const range = levelRange();
        char.xp = Math.max(0, parseInt(t.value, 10) || 0);
        char.level = levelFromXp(char.xp, range);
        if (char.level < (range.subclassMin || 2)) char.subclassId = "";
        persistAndRender();
      } else if (t.dataset && t.dataset.grantChoice) {
        const key = t.dataset.grantChoice;
        if (!char.grantedSpellChoices || typeof char.grantedSpellChoices !== "object") {
          char.grantedSpellChoices = {};
        }
        if (t.value) char.grantedSpellChoices[key] = t.value;
        else delete char.grantedSpellChoices[key];
        syncGrantedSpells(char);
        persistAndRender();
      }
    });

    if (el.modalRoot) {
      el.modalRoot.addEventListener("click", (e) => {
        if (portraitClearOpen) {
          if (e.target.id === "cs-portrait-clear-confirm") {
            portraitClearOpen = false;
            if (char) char.portraitUrl = "";
            persistAndRender();
            return;
          }
          if (
            e.target.id === "cs-portrait-clear-overlay" ||
            e.target.id === "cs-portrait-clear-close" ||
            e.target.id === "cs-portrait-clear-cancel"
          ) {
            portraitClearOpen = false;
            renderModals();
            return;
          }
        }
        const detailsBtn = e.target.closest("[data-spell-details]");
        if (detailsBtn) {
          const id = detailsBtn.dataset.spellDetails;
          if (spellModalExpandedIds.has(id)) spellModalExpandedIds.delete(id);
          else spellModalExpandedIds.add(id);
          renderModals();
          return;
        }
        const talentDetailsBtn = e.target.closest("[data-talent-details]");
        if (talentDetailsBtn) {
          const name = talentDetailsBtn.dataset.talentDetails;
          if (talentModalExpandedIds.has(name)) talentModalExpandedIds.delete(name);
          else talentModalExpandedIds.add(name);
          renderModals();
          return;
        }
        if (e.target.id === "cs-spell-modal-overlay" || e.target.id === "cs-spell-modal-close") {
          spellModalOpen = false;
          renderModals();
        } else if (e.target.id === "cs-spell-view-overlay" || e.target.id === "cs-spell-view-close") {
          spellViewId = null;
          renderModals();
        } else if (e.target.id === "cs-talent-view-overlay" || e.target.id === "cs-talent-view-close") {
          talentViewName = null;
          renderModals();
        } else if (e.target.id === "cs-choice-modal-overlay" || e.target.id === "cs-choice-modal-close") {
          skillModalOpen = false;
          languageModalOpen = false;
          talentModalOpen = false;
          talentModalExpandedIds.clear();
          renderModals();
        } else if (e.target.id === "cs-ddb-overlay" || e.target.id === "cs-ddb-close") {
          ddbModalOpen = false;
          ddbFallbackVisible = false;
          renderModals();
        } else if (e.target.id === "cs-ddb-review-overlay" || e.target.id === "cs-ddb-review-close" || e.target.id === "cs-ddb-review-done") {
          ddbReview = null;
          renderModals();
        } else if (e.target.id === "cs-ddb-import") {
          importDdbViaProxy();
        } else if (e.target.id === "cs-ddb-paste") {
          pasteDdbClipboard();
        } else if (e.target.id === "cs-ddb-import-paste") {
          tryImportDdbFromBox().catch((err) => {
            setDdbStatus(err && err.message ? err.message : "Couldn't import that JSON.");
          });
        } else if (e.target.id === "cs-ddb-json-link" && e.target.classList.contains("is-disabled")) {
          e.preventDefault();
          setDdbStatus("Enter a valid character URL or ID first so the JSON link works.");
        } else if (e.target.dataset.languageRemove) {
          const lang = e.target.dataset.languageRemove;
          char.chosenLanguages = char.chosenLanguages.filter((l) => l !== lang);
          persistAndRender();
        } else if (e.target.id === "cs-spell-view-toggle-prepare") {
          const id = e.target.dataset.spellId;
          if (char.preparedSpellIds.includes(id)) {
            char.preparedSpellIds = char.preparedSpellIds.filter((x) => x !== id);
            persistAndRender();
          } else {
            const preparedLeveledCount = char.preparedSpellIds.filter((pid) => {
              const s = spellById(pid);
              return s && s.circle > 0;
            }).length;
            if (preparedLeveledCount < computeActiveCap(char)) {
              char.preparedSpellIds.push(id);
              persistAndRender();
            }
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
        } else if (e.target.id === "cs-ddb-json") {
          const raw = e.target.value.trim();
          if (!raw) {
            setDdbStatus("Paste JSON here, or use Paste from clipboard.");
            return;
          }
          try {
            parseDdbPayloadText(raw);
            setDdbStatus("JSON looks good — click Import pasted JSON.");
          } catch (_) {
            setDdbStatus("Paste the full character JSON (must include a \"data\" field).");
          }
        } else if (e.target.id === "cs-ddb-input") {
          updateDdbJsonLink();
        }
      });

      el.modalRoot.addEventListener("keydown", (e) => {
        if (ddbReview) return;
        if (!ddbModalOpen) return;
        if (e.key === "Enter" && e.target && e.target.id === "cs-ddb-input") {
          e.preventDefault();
          if (ddbProxyConfigured()) importDdbViaProxy();
          else {
            showDdbFallback();
            setDdbStatus("Proxy not configured — use paste fallback.");
          }
        }
      });

      el.modalRoot.addEventListener("paste", (e) => {
        if (!ddbModalOpen || !e.target || e.target.id !== "cs-ddb-json") return;
        // After paste settles, validate.
        requestAnimationFrame(() => {
          const jsonBox = document.getElementById("cs-ddb-json");
          const raw = jsonBox ? jsonBox.value.trim() : "";
          if (!raw) return;
          try {
            parseDdbPayloadText(raw);
            setDdbStatus("JSON looks good — click Import.");
          } catch (_) {
            setDdbStatus("That paste isn’t valid character JSON yet.");
          }
        });
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
        } else if (t.id === "cs-language-dropdown") {
          const lang = t.value;
          const heritage = byId(data.heritages, char.heritageId);
          const choice = parseHeritageLanguageChoice(heritage);
          if (lang && choice && char.chosenLanguages.length < choice.count && !char.chosenLanguages.includes(lang)) {
            char.chosenLanguages.push(lang);
            persistAndRender();
          }
        }
      });

      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && portraitClearOpen) {
          portraitClearOpen = false;
          renderModals();
          return;
        }
        if (e.key === "Escape" && (spellModalOpen || spellViewId || talentViewName || skillModalOpen || languageModalOpen || talentModalOpen || ddbModalOpen || ddbReview)) {
          spellModalOpen = false;
          spellViewId = null;
          talentViewName = null;
          skillModalOpen = false;
          languageModalOpen = false;
          talentModalOpen = false;
          talentModalExpandedIds.clear();
          ddbModalOpen = false;
          ddbReview = null;
          ddbFallbackVisible = false;
          renderModals();
        }
      });
    }
  }

  /**
   * Fetch a sheet data JSON, preferring assets/nl/ on the Dutch sheet.
   * Falls back to the English assets/ path when the NL pack is missing.
   */
  async function fetchSheetDataJson(fileName) {
    const enPath = "assets/" + fileName;
    if (sheetLocale() === "nl") {
      try {
        const nlRes = await fetch(rp("assets/nl/" + fileName));
        if (nlRes.ok) return await nlRes.json();
      } catch (_) {
        /* fall through to EN */
      }
    }
    const res = await fetch(rp(enPath));
    if (!res.ok) throw new Error("Could not load " + fileName + " (HTTP " + res.status + ").");
    return await res.json();
  }

  async function init() {
    cacheElements();
    if (!el.loading || !el.app || !el.sheet) {
      showLoadError("Character sheet UI failed to load. Try refreshing the page.");
      return;
    }

    try {
      data = await fetchSheetDataJson("character-creator-data.json");
      if (!data || !Array.isArray(data.classes)) {
        throw new Error("Character options file is invalid. Regenerate it with generate-character-creator-data.py.");
      }
      try {
        SPELLS = await fetchSheetDataJson("spells-data.json");
        if (!Array.isArray(SPELLS)) SPELLS = [];
      } catch (_) {
        SPELLS = [];
      }
      try {
        TALENTS = await fetchSheetDataJson("talents-data.json");
        if (!Array.isArray(TALENTS)) TALENTS = [];
      } catch (_) {
        TALENTS = [];
      }
      // Resolve bonus spells now that SPELLS is loaded (store init runs earlier).
      store.characters.forEach((c) => {
        normalizeCharacter(c);
        syncGrantedSpells(c);
      });
      saveStore();
      manageDocumentTitle = document.title || manageDocumentTitle;
      applySheetModeFromUrl();
      showApp();
      applyToolbarI18n();
      bindEvents();
      try {
        render();
        syncToolbarFoldout(Boolean(store.activeId));
        maybeImportDdbFromQuery();
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
