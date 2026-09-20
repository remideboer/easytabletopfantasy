/**
 * USER STORY: As a new player, I want ready-made YMIAT characters on compact
 * printable sheets so I can start playing without building from scratch.
 * FEATURE: Pregenerated Characters
 * COMPONENT: assets/pregenerated-characters.js
 */
(function () {
  const ABILITY_LABEL = { fit: "FIT", ins: "INS", wil: "WIL" };

  function locale() {
    return document.documentElement.lang === "nl" || /\/nl\//.test(location.pathname) ? "nl" : "en";
  }

  function t(obj, lang) {
    if (obj == null) return "";
    if (typeof obj === "string") return obj;
    return obj[lang] || obj.en || "";
  }

  function fmtMod(n) {
    const v = Number(n) || 0;
    return (v >= 0 ? "+" : "") + v;
  }

  function maxResolve(wil) {
    return 4 + Math.ceil(Math.max(0, Number(wil) || 0) / 2);
  }

  function computeDefense(char, data) {
    const armor = char.armorId ? data.armorTable[char.armorId] : null;
    let def = 0;
    if (armor) {
      def = armor.base + (armor.addFit ? Number(char.abilities.fit) || 0 : 0);
    }
    if (char.shield) def += 2;
    return def;
  }

  function computeMaxWd(char, data) {
    const base = data.classMaxWd[char.classId] || 8;
    return base + (Number(char.abilities.fit) || 0);
  }

  function computeSpellPower(char, data) {
    if (!data.spellcasters.includes(char.classId)) return null;
    const mod = char.classId === "cleric" || char.classId === "wizard"
      ? Number(char.abilities.ins) || 0
      : Number(char.abilities.ins) || 0;
    return 2 + 2 * mod;
  }

  function skillBonus(char, skill) {
    const ab = Number(char.abilities[skill.ability]) || 0;
    const pb = Number(char.pb) || 1;
    let bonus = ab;
    if (skill.proficient) bonus += skill.expertise ? 2 * pb : pb;
    return bonus;
  }

  function attackBonus(char, attack) {
    return (Number(attack.weaponBonus) || 0) + (Number(char.abilities.fit) || 0) + (Number(char.pb) || 1);
  }

  function assetPrefix() {
    const depth = (location.pathname.match(/\//g) || []).length;
    // rough: /rules/pregenerated-characters/x.html → ../../assets/
    if (/\/nl\/rules\//.test(location.pathname)) return "../../../assets/";
    if (/\/rules\//.test(location.pathname)) return "../../assets/";
    return "assets/";
  }

  function rootPrefix() {
    if (/\/nl\/rules\//.test(location.pathname)) return "../../../";
    if (/\/rules\/pregenerated-characters\//.test(location.pathname)) return "../../";
    if (/\/nl\//.test(location.pathname)) return "../";
    return "";
  }

  function renderSheet(char, data, lang) {
    const copy = char.copy[lang] || char.copy.en;
    const maxWd = computeMaxWd(char, data);
    const defense = computeDefense(char, data);
    const resolve = maxResolve(char.abilities.wil);
    const sp = computeSpellPower(char, data);
    const pdfHref = assetPrefix() + "pdfs/pregenerated-characters/" + char.id + ".pdf";

    const abilitiesHtml = ["fit", "ins", "wil"].map(function (key) {
      return (
        '<div class="pg-ability">' +
        '<span class="pg-ability-lbl">' + ABILITY_LABEL[key] + "</span>" +
        '<span class="pg-ability-val">' + fmtMod(char.abilities[key]) + "</span>" +
        "</div>"
      );
    }).join("");

    const heartsHtml =
      '<span class="pg-hearts" aria-label="' + (lang === "nl" ? "Leven 3 van 3" : "Life 3 of 3") + '">' +
      '<span class="pg-heart-mark" aria-hidden="true">♥</span>' +
      '<span class="pg-heart-mark" aria-hidden="true">♥</span>' +
      '<span class="pg-heart-mark" aria-hidden="true">♥</span>' +
      "</span>";

    const blankVal = '<span class="pg-track-val"><span class="pg-track-blank" aria-hidden="true">&nbsp;</span></span>';

    let trackHtml =
      '<div class="pg-track' + (sp != null ? " pg-track--caster" : "") + '" role="group" aria-label="' + (lang === "nl" ? "Leven en wonden" : "Life and wounds") + '">' +
      '<div class="pg-track-cell pg-track-cell--life">' +
      '<span class="pg-track-lbl">' + (lang === "nl" ? "Leven" : "Life") + "</span>" +
      heartsHtml +
      "</div>" +
      '<div class="pg-track-cell">' +
      '<span class="pg-track-lbl">' + (lang === "nl" ? "WD Nu" : "WD Now") + "</span>" +
      blankVal +
      "</div>" +
      '<div class="pg-track-cell">' +
      '<span class="pg-track-lbl">Temp</span>' +
      blankVal +
      "</div>";
    if (sp != null) {
      trackHtml +=
        '<div class="pg-track-cell">' +
        '<span class="pg-track-lbl">SP</span>' +
        blankVal +
        "</div>";
    }
    trackHtml += "</div>";

    const stats = [
      ["PB", fmtMod(char.pb)],
      ["Max WD", String(maxWd)],
      [lang === "nl" ? "Resolve" : "Resolve", String(resolve)],
      [lang === "nl" ? "Defense" : "Defense", fmtMod(defense)],
      [lang === "nl" ? "Speed" : "Speed", char.speed + " ft"],
      [lang === "nl" ? "Save" : "Save", t(char.save, lang)],
    ];
    if (sp != null) stats.push(["Spell Power", String(sp)]);

    const statsHtml = stats.map(function (pair) {
      return '<div class="pg-stat"><dt>' + pair[0] + "</dt><dd>" + pair[1] + "</dd></div>";
    }).join("");

    const featuresHtml = (char.features || []).map(function (f) {
      return (
        '<div class="pg-feature">' +
        '<span class="pg-feature-name">' + t(f.name, lang) + "</span>" +
        '<span class="pg-feature-sum">' + t(f.summary, lang) + "</span>" +
        "</div>"
      );
    }).join("");

    const talentHtml =
      '<div class="pg-feature">' +
      '<span class="pg-feature-name">' + (lang === "nl" ? "Talent: " : "Talent: ") + t(char.talent, lang) + "</span>" +
      '<span class="pg-feature-sum">' + t(char.talentSummary, lang) + "</span>" +
      "</div>";

    const skillsHtml = (char.skills || []).map(function (s) {
      const label = t(s.name, lang) + (s.expertise ? " ★" : "");
      return "<li><strong>" + label + "</strong> " + fmtMod(skillBonus(char, s)) + " <span>(" + ABILITY_LABEL[s.ability] + ")</span></li>";
    }).join("");

    const profList = t(char.proficiencies, lang) || [];
    const profHtml = profList.length
      ? ('<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Behendigheden" : "Proficiencies") + "</h3>" +
        '<ul class="pg-list pg-list--compact">' + profList.map(function (line) {
          return "<li>" + line + "</li>";
        }).join("") + "</ul></div>")
      : "";

    const attacksHtml = (char.attacks || []).map(function (a) {
      return (
        "<li><strong>" + t(a.weapon, lang) + "</strong> " + fmtMod(attackBonus(char, a)) +
        " · " + a.wounds + (lang === "nl" ? " Wound" : " Wound") + "</li>"
      );
    }).join("");

    let spellsHtml = "";
    if (char.spells) {
      spellsHtml =
        '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Spells" : "Spells") + "</h3>" +
        '<p class="pg-prose"><span class="pg-label">Cantrips</span>' + t(char.spells.cantrips, lang).join(", ") + "</p>" +
        '<p class="pg-prose"><span class="pg-label">' + (lang === "nl" ? "Voorbereid" : "Prepared") + "</span>" + t(char.spells.prepared, lang).join(", ") + "</p>";
      if (char.spells.spellbookNote) {
        spellsHtml += '<p class="pg-prose">' + t(char.spells.spellbookNote, lang) + "</p>";
      }
      spellsHtml += "</div>";
    }

    const equipHtml = (t(char.equipment, lang) || []).map(function (item) {
      return "<li>" + item + "</li>";
    }).join("");

    const armorLabel = t(char.armorName, lang) + (char.shield ? (lang === "nl" ? " + schild" : " + shield") : "");

    return (
      '<div class="pg-toolbar pg-no-print">' +
      '<a class="btn" href="' + rootPrefix() + (lang === "nl" ? "nl/" : "") + 'rules/pregenerated-characters/index.html">' +
      (lang === "nl" ? "← Overzicht" : "← Party overview") + "</a>" +
      '<button type="button" class="btn" id="pg-print">' + (lang === "nl" ? "Afdrukken" : "Print") + "</button>" +
      '<a class="btn" href="' + pdfHref + '" download>' + (lang === "nl" ? "Download PDF" : "Download PDF") + "</a>" +
      "</div>" +
      '<div class="pg-sheet-wrap">' +
      '<article class="pg-sheet" aria-label="' + copy.name + '">' +
      '<div class="pg-head">' +
      '<div class="pg-head-id"><p class="pg-name">' + copy.name + "</p>" +
      '<p class="pg-meta"><strong>' + t(char.className, lang) + "</strong> · " + (lang === "nl" ? "Level" : "Level") + " 1 · " + copy.concept + "</p></div>" +
      '<div class="pg-head-facts">' +
      '<p class="pg-tags-row"><strong>' + (lang === "nl" ? "Lineage" : "Lineage") + ":</strong> " + t(char.lineageName, lang) +
      " · <strong>Heritage:</strong> " + t(char.heritageName, lang) +
      " · <strong>" + (lang === "nl" ? "Achtergrond" : "Background") + ":</strong> " + t(char.backgroundName, lang) + "</p>" +
      '<p class="pg-tags-row"><strong>' + (lang === "nl" ? "Pantser" : "Armor") + ":</strong> " + armorLabel +
      " · <strong>" + (lang === "nl" ? "Rol" : "Role") + ":</strong> " + copy.role + "</p>" +
      "</div></div>" +
      '<div class="pg-col">' +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Eigenschappen" : "Abilities") + "</h3>" +
      '<div class="pg-abilities">' + abilitiesHtml + "</div>" +
      trackHtml +
      '<dl class="pg-stat-grid">' + statsHtml + "</dl></div>" +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Features" : "Features") + "</h3>" +
      featuresHtml + talentHtml + "</div>" +
      "</div>" +
      '<div class="pg-col">' +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Skills" : "Skills") + "</h3>" +
      '<ul class="pg-list">' + skillsHtml + "</ul></div>" +
      profHtml +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Aanvallen" : "Attacks") + "</h3>" +
      '<ul class="pg-list">' + attacksHtml + "</ul></div>" +
      spellsHtml +
      "</div>" +
      '<div class="pg-col">' +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Persoon" : "Person") + "</h3>" +
      '<p class="pg-prose"><span class="pg-label">' + (lang === "nl" ? "Motivatie" : "Motivation") + "</span>" + copy.motivation + "</p>" +
      '<p class="pg-prose"><span class="pg-label">' + (lang === "nl" ? "Persoonlijkheid" : "Personality") + "</span>" + copy.personality + "</p>" +
      '<p class="pg-prose"><span class="pg-label">' + (lang === "nl" ? "Achtergrond" : "Background") + "</span>" + copy.background + "</p>" +
      "</div>" +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Inventaris" : "Inventory") + "</h3>" +
      '<ul class="pg-list">' + equipHtml + "</ul></div>" +
      "</div>" +
      '<p class="pg-foot-note">YMIAT · ' + (lang === "nl" ? "Voorgemaakt personage" : "Pregenerated character") + " · L1</p>" +
      "</article></div>"
    );
  }

  function renderHub(data, lang) {
    const note = t(data.meta.note, lang);
    const rows = data.characters.map(function (c) {
      const copy = c.copy[lang] || c.copy.en;
      const sheetHref = c.id + ".html";
      const pdfHref = assetPrefix() + "pdfs/pregenerated-characters/" + c.id + ".pdf";
      return (
        "<tr>" +
        "<td><strong>" + copy.name + "</strong><br><span class=\"text-muted\">" + copy.concept + "</span></td>" +
        "<td>" + t(c.className, lang) + "</td>" +
        "<td>" + copy.role + "</td>" +
        '<td class="pg-hub-actions">' +
        '<a class="btn" href="' + sheetHref + '">' + (lang === "nl" ? "Sheet" : "Sheet") + "</a>" +
        '<a class="btn" href="' + pdfHref + '" download>PDF</a>' +
        "</td></tr>"
      );
    }).join("");

    return (
      '<p class="lede">' + note + "</p>" +
      '<div class="table-wrap pg-hub-only"><table class="pg-hub-table">' +
      "<thead><tr>" +
      "<th>" + (lang === "nl" ? "Personage" : "Character") + "</th>" +
      "<th>" + (lang === "nl" ? "Klasse" : "Class") + "</th>" +
      "<th>" + (lang === "nl" ? "Rol" : "Role") + "</th>" +
      "<th></th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
      '<p class="pg-hub-only">' + (lang === "nl"
        ? "Elke sheet is één A4-liggend pagina (zwart-wit). Gebruik Afdrukken of Download PDF."
        : "Each sheet is one landscape A4 page (black and white). Use Print or Download PDF.") + "</p>"
    );
  }

  async function loadData() {
    const url = assetPrefix() + "pregenerated-characters.json";
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to load pregenerated characters");
    return res.json();
  }

  async function boot() {
    const root = document.getElementById("pg-root");
    if (!root) return;
    const lang = locale();
    const mode = root.getAttribute("data-pg-mode") || "hub";
    const id = root.getAttribute("data-pg-id");
    let data;
    try {
      data = await loadData();
    } catch (err) {
      root.innerHTML = "<p>Could not load pregenerated characters.</p>";
      return;
    }
    if (mode === "sheet") {
      const char = data.characters.find(function (c) { return c.id === id; });
      if (!char) {
        root.innerHTML = "<p>Character not found.</p>";
        return;
      }
      root.innerHTML = renderSheet(char, data, lang);
      const btn = document.getElementById("pg-print");
      if (btn) btn.addEventListener("click", function () { window.print(); });
      document.title = (char.copy[lang] || char.copy.en).name + " | YMIAT";
    } else {
      root.innerHTML = renderHub(data, lang);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
