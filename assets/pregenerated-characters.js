/**
 * USER STORY: As a new player, I want ready-made YMIAT characters on compact
 * printable sheets so I can start playing without building from scratch.
 * FEATURE: Pregenerated Characters + character-sheet PDF export
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
    const mod = Number(char.abilities.ins) || 0;
    return 2 + 2 * mod;
  }

  function skillBonus(abilities, pb, skill) {
    const ab = Number(abilities[skill.ability]) || 0;
    const p = Number(pb) || 1;
    let bonus = ab;
    if (skill.proficient) bonus += skill.expertise ? 2 * p : p;
    return bonus;
  }

  function attackBonus(abilities, pb, attack) {
    return (Number(attack.weaponBonus) || 0) + (Number(abilities.fit) || 0) + (Number(pb) || 1);
  }

  function assetPrefix() {
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

  /**
   * Build a locale-ready view model from pregenerated-characters.json entry.
   */
  function viewModelFromJsonChar(char, data, lang) {
    const copy = char.copy[lang] || char.copy.en;
    const maxWd = computeMaxWd(char, data);
    const defense = computeDefense(char, data);
    const resolve = maxResolve(char.abilities.wil);
    const sp = computeSpellPower(char, data);
    const armorLabel = t(char.armorName, lang) + (char.shield ? (lang === "nl" ? " + schild" : " + shield") : "");

    return {
      name: copy.name,
      className: t(char.className, lang),
      level: 1,
      concept: copy.concept,
      role: copy.role,
      lineageName: t(char.lineageName, lang),
      heritageName: t(char.heritageName, lang),
      backgroundName: t(char.backgroundName, lang),
      armorLabel: armorLabel,
      abilities: char.abilities,
      hearts: 3,
      spellPower: sp,
      pb: char.pb,
      maxWd: maxWd,
      resolve: resolve,
      defense: defense,
      speed: char.speed,
      save: t(char.save, lang),
      features: (char.features || []).map(function (f) {
        return { name: t(f.name, lang), summary: t(f.summary, lang) };
      }),
      talentName: t(char.talent, lang),
      talentSummary: t(char.talentSummary, lang),
      skills: (char.skills || []).map(function (s) {
        return {
          name: t(s.name, lang),
          ability: s.ability,
          expertise: Boolean(s.expertise),
          bonus: skillBonus(char.abilities, char.pb, s),
        };
      }),
      proficiencies: t(char.proficiencies, lang) || [],
      attacks: (char.attacks || []).map(function (a) {
        return {
          weapon: t(a.weapon, lang),
          bonus: attackBonus(char.abilities, char.pb, a),
          wounds: a.wounds,
        };
      }),
      spells: char.spells
        ? {
            cantrips: t(char.spells.cantrips, lang) || [],
            prepared: t(char.spells.prepared, lang) || [],
            note: char.spells.spellbookNote ? t(char.spells.spellbookNote, lang) : "",
          }
        : null,
      motivation: copy.motivation,
      personality: copy.personality,
      background: copy.background,
      equipment: t(char.equipment, lang) || [],
      footer: "YMIAT · " + (lang === "nl" ? "Voorgemaakt personage" : "Pregenerated character") + " · L1",
      downloadHref: assetPrefix() + "pdfs/pregenerated-characters/" + char.id + ".pdf",
    };
  }

  /**
   * Render compact landscape sheet HTML from a view model.
   * @param {object} vm locale-ready view model
   * @param {object} [options]
   * @param {boolean} [options.includeChrome=true] party overview / print / download toolbar
   * @param {string} [options.lang] for chrome labels
   */
  function renderPgSheetHtml(vm, options) {
    options = options || {};
    const lang = options.lang || locale();
    const includeChrome = options.includeChrome !== false;

    const abilitiesHtml = ["fit", "ins", "wil"].map(function (key) {
      const isSpell = vm.spellcastingAbility === key;
      return (
        '<div class="pg-ability' + (isSpell ? " is-spellcasting" : "") + '">' +
        '<span class="pg-ability-lbl"' + (isSpell ? ' title="Spellcasting ability"' : "") + ">" +
        ABILITY_LABEL[key] + (isSpell ? "*" : "") +
        "</span>" +
        '<span class="pg-ability-val">' + fmtMod(vm.abilities[key]) + "</span>" +
        "</div>"
      );
    }).join("");

    const heartCount = Math.max(0, Math.min(3, Number(vm.hearts) || 3));
    let heartsMarks = "";
    for (let i = 0; i < 3; i++) {
      heartsMarks += '<span class="pg-heart-mark" aria-hidden="true">' + (i < heartCount ? "♥" : "♡") + "</span>";
    }
    const heartsHtml =
      '<span class="pg-hearts" aria-label="' + (lang === "nl" ? "Leven" : "Life") + " " + heartCount + "/3\">" +
      heartsMarks + "</span>";

    const blankVal = '<span class="pg-track-val"><span class="pg-track-blank" aria-hidden="true">&nbsp;</span></span>';
    const hasSp = vm.spellPower != null;

    let trackHtml =
      '<div class="pg-track' + (hasSp ? " pg-track--caster" : "") + '" role="group" aria-label="' + (lang === "nl" ? "Leven en wonden" : "Life and wounds") + '">' +
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
    if (hasSp) {
      trackHtml +=
        '<div class="pg-track-cell">' +
        '<span class="pg-track-lbl">SP</span>' +
        blankVal +
        "</div>";
    }
    trackHtml += "</div>";

    const stats = [
      ["PB", fmtMod(vm.pb)],
      ["Max WD", String(vm.maxWd)],
      ["Resolve", String(vm.resolve)],
      [lang === "nl" ? "Defense" : "Defense", fmtMod(vm.defense)],
      [lang === "nl" ? "Speed" : "Speed", vm.speed + " ft"],
      ["Save", vm.save || "—"],
    ];
    if (hasSp) stats.push(["Spell Power", String(vm.spellPower)]);
    if (vm.spellcastingLine) {
      stats.push([lang === "nl" ? "Spellcasting" : "Spellcasting", String(vm.spellcastingLine).replace(/^Spellcasting:\s*/i, "")]);
    }

    const statsHtml = stats.map(function (pair) {
      return '<div class="pg-stat"><dt>' + pair[0] + "</dt><dd>" + pair[1] + "</dd></div>";
    }).join("");

    const featuresHtml = (vm.features || []).map(function (f) {
      return (
        '<div class="pg-feature">' +
        '<span class="pg-feature-name">' + f.name + "</span>" +
        '<span class="pg-feature-sum">' + (f.summary || "") + "</span>" +
        "</div>"
      );
    }).join("");

    let talentHtml = "";
    if (vm.talentName) {
      talentHtml =
        '<div class="pg-feature">' +
        '<span class="pg-feature-name">' + (lang === "nl" ? "Talent: " : "Talent: ") + vm.talentName + "</span>" +
        '<span class="pg-feature-sum">' + (vm.talentSummary || "") + "</span>" +
        "</div>";
    }

    const skillsHtml = (vm.skills || []).map(function (s) {
      const label = s.name + (s.expertise ? " ★" : "");
      return "<li><strong>" + label + "</strong> " + fmtMod(s.bonus) + " <span>(" + ABILITY_LABEL[s.ability] + ")</span></li>";
    }).join("");

    const profList = vm.proficiencies || [];
    const profHtml = profList.length
      ? ('<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Behendigheden" : "Proficiencies") + "</h3>" +
        '<ul class="pg-list pg-list--compact">' + profList.map(function (line) {
          return "<li>" + line + "</li>";
        }).join("") + "</ul></div>")
      : "";

    const attacksHtml = (vm.attacks || []).map(function (a) {
      return (
        "<li><strong>" + a.weapon + "</strong> " + fmtMod(a.bonus) +
        " · " + a.wounds + " Wound</li>"
      );
    }).join("") || "<li>—</li>";

    let spellsHtml = "";
    if (vm.spells) {
      function spellListOrSpace(items) {
        const list = items || [];
        if (list.length) return list.join(", ");
        // Two blank writing rows (no ruled lines) when nothing is selected yet.
        return '<div class="pg-write-space pg-write-space--spells" aria-hidden="true"></div>';
      }
      spellsHtml =
        '<div class="pg-section"><h3 class="pg-section-title">Spells</h3>' +
        '<div class="pg-person-field"><span class="pg-label">Cantrips</span>' + spellListOrSpace(vm.spells.cantrips) + "</div>";
      if (Array.isArray(vm.spells.known)) {
        spellsHtml +=
          '<div class="pg-person-field"><span class="pg-label">' +
          (lang === "nl" ? "Bekend" : "Known") +
          "</span>" + spellListOrSpace(vm.spells.known) + "</div>";
      } else {
        spellsHtml +=
          '<div class="pg-person-field"><span class="pg-label">' +
          (lang === "nl" ? "Voorbereid" : "Prepared") +
          "</span>" + spellListOrSpace(vm.spells.prepared) + "</div>";
      }
      if (Array.isArray(vm.spells.knownUnprepared)) {
        spellsHtml +=
          '<div class="pg-person-field"><span class="pg-label">' +
          (lang === "nl" ? "Known (niet voorbereid)" : "Known (unprepared)") +
          "</span>" + spellListOrSpace(vm.spells.knownUnprepared) + "</div>";
      }
      if (vm.spells.note) {
        spellsHtml += '<p class="pg-prose">' + vm.spells.note + "</p>";
      }
      spellsHtml += "</div>";
    }

    const equipHtml = (vm.equipment || []).map(function (item) {
      return "<li>" + item + "</li>";
    }).join("") || "<li>—</li>";

    const personBits = [];
    const lineageTraits = Array.isArray(vm.lineageTraits) ? vm.lineageTraits : [];
    if (lineageTraits.length) {
      const traitLines = lineageTraits.map(function (trait) {
        const label = String(trait.name || "").replace(/\.$/, "");
        const body = String(trait.text || "").trim();
        if (!label || !body) return "";
        return '<p class="pg-trait"><strong>' + label + ".</strong> " + body + "</p>";
      }).filter(Boolean).join("");
      personBits.push(
        '<div class="pg-person-field">' +
        '<span class="pg-label">' + (lang === "nl" ? "Lineage-traits" : "Lineage traits") + "</span>" +
        '<div class="pg-trait-list">' + traitLines + "</div>" +
        "</div>"
      );
    }
    const personFields = [
      { key: "motivation", en: "Motivation", nl: "Motivatie" },
      { key: "personality", en: "Personality", nl: "Persoonlijkheid" },
      { key: "background", en: "Background", nl: "Achtergrond" },
    ];
    personFields.forEach(function (field) {
      const label = lang === "nl" ? field.nl : field.en;
      const text = String(vm[field.key] || "").trim();
      // Always keep header + writing room so players can fill blanks on paper/PDF.
      const body = text
        ? '<p class="pg-prose">' + text + "</p>"
        : '<div class="pg-write-space" aria-hidden="true"></div>';
      personBits.push('<div class="pg-person-field"><span class="pg-label">' + label + "</span>" + body + "</div>");
    });

    let chrome = "";
    if (includeChrome) {
      chrome =
        '<div class="pg-toolbar pg-no-print">' +
        '<a class="btn" href="' + rootPrefix() + (lang === "nl" ? "nl/" : "") + 'rules/pregenerated-characters/index.html">' +
        (lang === "nl" ? "← Overzicht" : "← Party overview") + "</a>" +
        '<button type="button" class="btn" id="pg-print">' + (lang === "nl" ? "Afdrukken" : "Print") + "</button>" +
        (vm.downloadHref
          ? '<a class="btn" href="' + vm.downloadHref + '" download>' + (lang === "nl" ? "Download PDF" : "Download PDF") + "</a>"
          : "") +
        "</div>";
    }

    const sheet =
      '<div class="pg-sheet-wrap">' +
      '<article class="pg-sheet" aria-label="' + vm.name + '">' +
      '<div class="pg-head">' +
      '<div class="pg-head-id"><p class="pg-name">' + vm.name + "</p>" +
      '<p class="pg-meta"><strong>' + vm.className + "</strong> · " + (lang === "nl" ? "Level" : "Level") + " " + vm.level +
      (vm.concept ? " · " + vm.concept : "") + "</p></div>" +
      '<div class="pg-head-facts">' +
      '<p class="pg-tags-row"><strong>Lineage:</strong> ' + (vm.lineageName || "—") +
      " · <strong>Heritage:</strong> " + (vm.heritageName || "—") +
      " · <strong>" + (lang === "nl" ? "Achtergrond" : "Background") + ":</strong> " + (vm.backgroundName || "—") + "</p>" +
      '<p class="pg-tags-row"><strong>' + (lang === "nl" ? "Pantser" : "Armor") + ":</strong> " + (vm.armorLabel || "—") +
      " · <strong>" + (lang === "nl" ? "Rol" : "Role") + ":</strong> " + (vm.role || vm.className || "—") + "</p>" +
      (vm.armorWarning
        ? '<p class="pg-armor-warn"><strong>' + (lang === "nl" ? "Niet proficient" : "Not proficient") + ":</strong> " + vm.armorWarning + "</p>"
        : "") +
      "</div></div>" +
      '<div class="pg-col">' +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Eigenschappen" : "Abilities") + "</h3>" +
      '<div class="pg-abilities">' + abilitiesHtml + "</div>" +
      trackHtml +
      '<dl class="pg-stat-grid">' + statsHtml + "</dl></div>" +
      '<div class="pg-section"><h3 class="pg-section-title">Features</h3>' +
      featuresHtml + talentHtml + "</div>" +
      "</div>" +
      '<div class="pg-col">' +
      '<div class="pg-section"><h3 class="pg-section-title">Skills</h3>' +
      '<ul class="pg-list">' + (skillsHtml || "<li>—</li>") + "</ul></div>" +
      profHtml +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Aanvallen" : "Attacks") + "</h3>" +
      '<ul class="pg-list">' + attacksHtml + "</ul></div>" +
      spellsHtml +
      "</div>" +
      '<div class="pg-col">' +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Persoon" : "Person") + "</h3>" +
      personBits.join("") +
      "</div>" +
      '<div class="pg-section"><h3 class="pg-section-title">' + (lang === "nl" ? "Inventaris" : "Inventory") + "</h3>" +
      '<ul class="pg-list">' + equipHtml + "</ul></div>" +
      "</div>" +
      '<p class="pg-foot-note">' + (vm.footer || "YMIAT") + "</p>" +
      "</article></div>";

    return chrome + sheet;
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
      const vm = viewModelFromJsonChar(char, data, lang);
      root.innerHTML = renderPgSheetHtml(vm, { lang: lang, includeChrome: true });
      const btn = document.getElementById("pg-print");
      if (btn) btn.addEventListener("click", function () { window.print(); });
      document.title = vm.name + " | YMIAT";
    } else {
      root.innerHTML = renderHub(data, lang);
    }
  }

  window.ymiatRenderPregenSheetHtml = renderPgSheetHtml;
  window.ymiatPregenViewModelFromJson = viewModelFromJsonChar;
  window.ymiatRenderPregenSpellPagesHtml = renderPregenSpellPagesHtml;

  /**
   * Render B&W spell-card pages (4 cards / landscape page) for PDF/print.
   * @param {Array} spells card objects from the character sheet
   * @param {object} [options]
   * @param {string} [options.characterName]
   * @param {string} [options.lang]
   * @param {number} [options.perPage=6]
   */
  function renderPregenSpellPagesHtml(spells, options) {
    options = options || {};
    const lang = options.lang || locale();
    const perPage = options.perPage || 6;
    const charName = options.characterName || "";
    const list = Array.isArray(spells) ? spells.slice() : [];
    if (!list.length) return "";

    function esc(s) {
      return String(s == null ? "" : s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    function levelBadge(circle) {
      const n = Number(circle) || 0;
      if (n <= 0) return lang === "nl" ? "Cantrip" : "Cantrip";
      return "L" + n;
    }

    function statusBadge(prepared) {
      if (prepared === true) return lang === "nl" ? "Voorbereid" : "Prepared";
      if (prepared === false) return lang === "nl" ? "Known" : "Known";
      return "";
    }

    function descHtml(text) {
      const raw = String(text || "").trim();
      if (!raw) return "<p>—</p>";
      return raw.split(/\n+/).filter(Boolean).map(function (para) {
        return "<p>" + esc(para) + "</p>";
      }).join("");
    }

    function cardHtml(spell) {
      const level = levelBadge(spell.circle);
      const status = statusBadge(spell.prepared);
      const metaBits = [
        spell.school,
        spell.castingTime,
        spell.range ? (lang === "nl" ? "Bereik: " : "Range: ") + spell.range : "",
        spell.duration ? (lang === "nl" ? "Duur: " : "Duration: ") + spell.duration : "",
        spell.components ? (lang === "nl" ? "Comp: " : "Comp: ") + spell.components : "",
      ].filter(Boolean);
      return (
        '<article class="pg-spell-card">' +
        '<div class="pg-spell-card-head">' +
        '<h4 class="pg-spell-card-name">' + esc(spell.name) + "</h4>" +
        '<div class="pg-spell-card-badges">' +
        '<span class="pg-spell-badge pg-spell-badge--level">' + esc(level) + "</span>" +
        (status ? '<span class="pg-spell-badge pg-spell-badge--status">' + esc(status) + "</span>" : "") +
        "</div></div>" +
        '<p class="pg-spell-card-meta">' + esc(metaBits.join(" · ")) + "</p>" +
        '<div class="pg-spell-card-body">' + descHtml(spell.description) + "</div>" +
        "</article>"
      );
    }

    const pages = [];
    for (let i = 0; i < list.length; i += perPage) {
      pages.push(list.slice(i, i + perPage));
    }

    const title = lang === "nl" ? "Spells" : "Spells";
    return (
      '<div class="pg-spell-pages">' +
      pages.map(function (pageSpells, pageIdx) {
        const cards = pageSpells.map(cardHtml).join("");
        // Pad empty slots so the 3-column grid stays even on the last page.
        let pad = "";
        for (let p = pageSpells.length; p < perPage; p++) {
          pad += '<div class="pg-spell-card" aria-hidden="true" style="visibility:hidden;border:0"></div>';
        }
        return (
          '<section class="pg-spell-page" data-spell-page="' + (pageIdx + 1) + '">' +
          '<div class="pg-spell-page-head">' +
          '<p class="pg-spell-page-title">' + esc(title) + (charName ? " · " + esc(charName) : "") + "</p>" +
          '<p class="pg-spell-page-sub">' + (lang === "nl" ? "Pagina" : "Page") + " " + (pageIdx + 2) + "</p>" +
          "</div>" +
          '<div class="pg-spell-grid">' + cards + pad + "</div>" +
          "</section>"
        );
      }).join("") +
      "</div>"
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();