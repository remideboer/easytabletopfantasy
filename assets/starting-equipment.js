/**
 * Starting equipment packages (class option A + background) → sheet inventory/currency.
 * Class lists follow BFRD/ToV option (a) defaults; homebrew classes use close analogues.
 */
(function (global) {
  const CLASS_STARTING_EQUIPMENT = {
    barbarian: ["Greataxe", "2 handaxes", "Explorer's pack", "4 javelins"],
    bard: ["Rapier", "Diplomat's pack", "Musical instrument", "Leather armor", "Dagger"],
    cleric: ["Mace", "Scale mail", "Light crossbow", "20 bolts", "Priest's pack", "Shield", "Holy symbol"],
    druid: ["Shield", "Scimitar", "Leather armor", "Explorer's pack", "Druidic focus"],
    fighter: ["Chain mail", "Longsword", "Shield", "Light crossbow", "20 bolts", "Dungeoneer's pack"],
    artificer: ["Longsword", "Shield", "Light crossbow", "20 bolts", "Scale mail", "Tinker tools", "Dungeoneer's pack"],
    monk: ["Quarterstaff", "Dungeoneer's pack", "10 darts"],
    paladin: ["Longsword", "Shield", "5 javelins", "Priest's pack", "Chain mail", "Holy symbol"],
    ranger: ["Scale mail", "2 shortswords", "Dungeoneer's pack", "Longbow", "20 arrows"],
    rogue: ["Rapier", "Shortbow", "20 arrows", "Burglar's pack", "Leather armor", "2 daggers", "Thieves' tools"],
    sorcerer: ["Light crossbow", "20 bolts", "Component pouch", "Dungeoneer's pack", "2 daggers"],
    warlock: ["Light crossbow", "20 bolts", "Component pouch", "Scholar's pack", "Leather armor", "Quarterstaff", "2 daggers"],
    wizard: ["Quarterstaff", "Component pouch", "Scholar's pack", "Spellbook"],
    theurge: ["Quarterstaff", "Component pouch", "Scholar's pack", "Mystic libram", "Holy symbol"],
    vanguard: ["Chain mail", "Longsword", "Shield", "Light crossbow", "20 bolts", "Dungeoneer's pack"],
    witch: ["Leather armor", "Quarterstaff", "Component pouch", "Explorer's pack", "2 daggers"],
  };

  const ARMOR_NAME_TO_ID = [
    { re: /\bplate\b/i, id: "plate" },
    { re: /\bsplint\b/i, id: "splint" },
    { re: /\bchain\s*mail\b/i, id: "chain-mail" },
    { re: /\bring\s*mail\b/i, id: "ring-mail" },
    { re: /\bhalf\s*plate\b/i, id: "half-plate" },
    { re: /\bbreastplate\b/i, id: "breastplate" },
    { re: /\bscale\s*mail\b/i, id: "scale-mail" },
    { re: /\bchain\s*shirt\b/i, id: "chain-shirt" },
    { re: /\bhide\b/i, id: "hide" },
    { re: /\bstudded\s*leather\b/i, id: "studded-leather" },
    { re: /\bleather\s*armor\b/i, id: "leather" },
    { re: /\bpadded\b/i, id: "padded" },
  ];

  const WEAPON_NAME_TO_ID = [
    { re: /\blongbow\b/i, id: "longbow" },
    { re: /\bshortbow\b/i, id: "shortbow" },
    { re: /\blight\s*crossbow\b/i, id: "light-crossbow" },
    { re: /\bheavy\s*crossbow\b/i, id: "heavy-crossbow" },
    { re: /\bhand\s*crossbow\b/i, id: "hand-crossbow" },
    { re: /\bgreataxe\b/i, id: "greataxe" },
    { re: /\bgreatsword\b/i, id: "greatsword" },
    { re: /\blongsword\b/i, id: "longsword" },
    { re: /\bshortsword\b/i, id: "shortsword" },
    { re: /\bwarhammer\b/i, id: "warhammer" },
    { re: /\bquarterstaff\b/i, id: "quarterstaff" },
    { re: /\bscimitar\b/i, id: "scimitar" },
    { re: /\brapier\b/i, id: "rapier" },
    { re: /\bmaul\b/i, id: "maul" },
    { re: /\bmace\b/i, id: "mace" },
    { re: /\bhandaxe\b/i, id: "handaxe" },
    { re: /\bjavelin\b/i, id: "javelin" },
    { re: /\bdagger\b/i, id: "dagger" },
    { re: /\bspear\b/i, id: "spear" },
    { re: /\bclub\b/i, id: "club" },
    { re: /\bdart\b/i, id: "dart" },
    { re: /\bsling\b/i, id: "sling" },
  ];

  function cleanItemLabel(raw) {
    let s = String(raw || "").trim().replace(/^and\s+/i, "");
    s = s.replace(/^(a|an|the)\s+/i, "");
    s = s.replace(/\s+/g, " ").trim();
    if (!s) return "";
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  function extractEquipmentProse(body) {
    if (!body) return "";
    const m = String(body).match(/Equipment:<\/strong>\s*([^<]+)/i);
    if (!m) return "";
    let text = m[1].trim().replace(/\.$/, "");
    const choose = text.match(/^Choose A or B:\s*\(A\)\s*(.+?);\s*or\s*\(B\)\s*.+$/i);
    if (choose) text = choose[1].trim().replace(/\.$/, "");
    return text;
  }

  function pullCurrency(text, currency) {
    let rest = text;

    rest = rest.replace(/,?\s*(?:and\s+)?(?:two|2)\s+purses?\s+of\s+(\d+)\s*gp\s+each/gi, (_, n) => {
      currency.gold += 2 * (parseInt(n, 10) || 0);
      return "";
    });

    rest = rest.replace(
      /,?\s*(?:and\s+)?(?:a\s+)?(?:pouch\s+containing|coin\s+purse\s+with)\s+(\d+)\s*gp/gi,
      (_, n) => {
        currency.gold += parseInt(n, 10) || 0;
        return "";
      }
    );

    rest = rest.replace(/,?\s*(?:and\s+)?(\d+)\s*gp\s+(?:of|in)\s+([^,]+)/gi, (_, n, desc) => {
      currency.gold += parseInt(n, 10) || 0;
      const d = String(desc || "").trim();
      if (/^(small coin|shavings or dust|copper and silver)\b/i.test(d)) return "";
      return ", " + d;
    });

    rest = rest.replace(/,?\s*(?:and\s+)?(\d+)\s*gp\b/gi, (_, n) => {
      currency.gold += parseInt(n, 10) || 0;
      return "";
    });
    rest = rest.replace(/,?\s*(?:and\s+)?(\d+)\s*sp\b/gi, (_, n) => {
      currency.silver += parseInt(n, 10) || 0;
      return "";
    });
    rest = rest.replace(/,?\s*(?:and\s+)?(\d+)\s*cp\b/gi, (_, n) => {
      currency.copper += parseInt(n, 10) || 0;
      return "";
    });

    return rest;
  }

  function splitEquipmentItems(text) {
    let rest = String(text || "")
      .replace(/\s+/g, " ")
      .replace(/^[\s,]+|[\s,]+$/g, "")
      .trim();
    if (!rest) return [];

    const parts = rest.split(/\s*,\s*/).filter(Boolean);
    const items = [];
    parts.forEach((part, idx) => {
      let chunk = part.replace(/^and\s+/i, "").trim();
      if (!chunk) return;
      if (idx === parts.length - 1 && /^and\s+/i.test(part) === false) {
        // last comma-segment may still start with "and "
      }
      items.push(cleanItemLabel(chunk));
    });
    return items.filter(Boolean);
  }

  function parseBackgroundEquipment(body) {
    const currency = { gold: 0, silver: 0, copper: 0 };
    let prose = extractEquipmentProse(body);
    if (!prose) return { items: [], currency };

    prose = pullCurrency(prose, currency);
    const items = splitEquipmentItems(prose);
    return { items, currency };
  }

  function applyEquippedFromItems(character, items) {
    if (!character) return;
    // Walk package order so the primary weapon/armor wins (e.g. Longsword before Light crossbow).
    for (const item of items) {
      const line = String(item || "");
      if (/\bshield\b/i.test(line)) character.hasShield = true;
      if (!character.armorId) {
        for (const entry of ARMOR_NAME_TO_ID) {
          if (entry.re.test(line)) {
            character.armorId = entry.id;
            break;
          }
        }
      }
      if (!character.weaponId) {
        for (const entry of WEAPON_NAME_TO_ID) {
          if (entry.re.test(line)) {
            character.weaponId = entry.id;
            break;
          }
        }
      }
    }
  }

  /**
   * Fill inventory + currency (+ equipped armor/weapon/shield) from packages.
   * @param {object} character sheet character object (mutated)
   * @param {{ classId?: string, background?: object|null, slotCount: number }} opts
   */
  function applyPackageEquipment(character, opts) {
    const slotCount = Math.max(0, Number(opts && opts.slotCount) || 0);
    const classId = (opts && opts.classId) || "";
    const background = opts && opts.background;

    const items = [];
    const currency = { gold: 0, silver: 0, copper: 0 };

    const classItems = CLASS_STARTING_EQUIPMENT[classId];
    if (Array.isArray(classItems)) items.push.apply(items, classItems);

    if (background && background.body) {
      const parsed = parseBackgroundEquipment(background.body);
      items.push.apply(items, parsed.items);
      currency.gold += parsed.currency.gold;
      currency.silver += parsed.currency.silver;
      currency.copper += parsed.currency.copper;
    }

    const inventory = Array(slotCount).fill("");
    items.slice(0, slotCount).forEach((item, i) => {
      inventory[i] = item;
    });
    character.inventory = inventory;
    character.currency = {
      gold: Math.max(0, (character.currency && character.currency.gold) || 0) + currency.gold,
      silver: Math.max(0, (character.currency && character.currency.silver) || 0) + currency.silver,
      copper: Math.max(0, (character.currency && character.currency.copper) || 0) + currency.copper,
    };

    applyEquippedFromItems(character, items);
    return { items, currency };
  }

  global.ymiatStartingEquipment = {
    CLASS_STARTING_EQUIPMENT,
    parseBackgroundEquipment,
    applyPackageEquipment,
  };
})(typeof window !== "undefined" ? window : globalThis);
