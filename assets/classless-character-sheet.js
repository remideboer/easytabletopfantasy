/**
 * YMIAT Classless Character Sheet — local character management.
 * Standalone from the class-based sheet: no shared class data file.
 * Trained abilities are picked from the Classless abilities list via a modal.
 * Persistence in localStorage.
 */
(function () {
  const STORAGE_KEY = "ymiat-classless-characters-v1";
  const ABILITY_LINE_COUNT = 10;

  let store = loadStore();
  let char = null;
  let eventsBound = false;
  let abilitiesData = null;
  let abilityModalLine = null;
  let abilityModalSelectedIds = [];
  let abilityModalMessage = "";
  let abilityEditLine = null;

  const el = {};

  function cacheElements() {
    el.app = document.getElementById("cls-app");
    el.charSelect = document.getElementById("cls-char-select");
    el.sheet = document.getElementById("cls-sheet");
    el.empty = document.getElementById("cls-empty");
    el.hint = document.getElementById("cls-hint");
    el.btnNew = document.getElementById("cls-btn-new");
    el.btnPrint = document.getElementById("cls-btn-print");
    el.printOrientation = document.getElementById("cls-print-orientation");
    el.btnDelete = document.getElementById("cls-btn-delete");
    el.modalRoot = document.getElementById("cls-modal-root");
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

  function applyPrintOrientation(orientation) {
    let styleEl = document.getElementById("cls-print-orientation-style");
    if (!styleEl) {
      styleEl = document.createElement("style");
      styleEl.id = "cls-print-orientation-style";
      document.head.appendChild(styleEl);
    }
    styleEl.textContent = `@media print { @page { size: A4 ${orientation === "portrait" ? "portrait" : "landscape"}; margin: 1cm; } }`;
  }

  function uid() {
    return "cl-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 9);
  }

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  function formatMod(n) {
    if (n > 0) return "+" + n;
    return String(n);
  }

  function heartsLost(c) {
    return 3 - (c.hearts ?? 3);
  }

  function resolveMax(c) {
    return 4 + Math.ceil((c.wil ?? 0) / 2);
  }

  function escapeHtml(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function defaultCharacter() {
    return {
      id: uid(),
      name: "",
      xp: 20,
      hearts: 3,
      fit: 0,
      ins: 0,
      wil: 0,
      def: 0,
      res: 0,
      spMax: 0,
      spNow: 0,
      wdMax: 4,
      wdNow: 0,
      wdTmp: 0,
      speed: 30,
      currency: { gold: 0, silver: 0, copper: 0 },
      abilityLines: Array(ABILITY_LINE_COUNT).fill(null),
      activeText: "",
      lineageText: "",
      heritageText: "",
      backgroundText: "",
      spellListText: "",
      inventoryText: "",
    };
  }

  function normalizeAbilityLine(value) {
    if (value == null || value === "") return null;
    if (typeof value === "object") {
      const name = String(value.name || "").trim();
      const description = String(value.description || "").trim();
      if (!name && !description) return null;
      return {
        id: String(value.id || ""),
        name,
        description,
        notes: String(value.notes || "").trim(),
        xp: value.xp != null ? Number(value.xp) : undefined,
      };
    }
    const text = String(value).trim();
    if (!text) return null;
    const match = text.match(/^([^:]+):\s*([\s\S]*)$/);
    if (match) {
      return { id: "", name: match[1].trim(), description: match[2].trim() };
    }
    return { id: "", name: text, description: "" };
  }

  function abilityById(id) {
    if (!abilitiesData || !id) return null;
    return abilitiesData.abilities.find((a) => a.id === id) || null;
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
          parsed.characters = parsed.characters.filter(Boolean).map((c) => {
            try {
              return normalizeCharacter(c);
            } catch (_) {
              return normalizeCharacter(defaultCharacter());
            }
          });
          if (!parsed.activeId || !parsed.characters.some((c) => c.id === parsed.activeId)) {
            parsed.activeId = parsed.characters.length ? parsed.characters[0].id : null;
          }
          return parsed;
        }
      }
    } catch (_) { /* ignore */ }
    return defaultStore();
  }

  function saveStore() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
  }

  function normalizeCharacter(c) {
    const d = defaultCharacter();
    c.id = c.id || d.id;
    c.name = String(c.name ?? "");
    c.xp = Math.max(0, Number(c.xp) || 0);
    c.hearts = clamp(Number.isFinite(Number(c.hearts)) ? Number(c.hearts) : 3, 0, 3);
    c.fit = clamp(Number(c.fit) || 0, -5, 5);
    c.ins = clamp(Number(c.ins) || 0, -5, 5);
    c.wil = clamp(Number(c.wil) || 0, -5, 5);
    c.def = clamp(Number(c.def) || 0, -5, 30);
    c.res = clamp(Number(c.res) || 0, 0, resolveMax(c));
    c.spMax = Math.max(0, Number(c.spMax) || 0);
    c.spNow = clamp(Number(c.spNow) || 0, 0, c.spMax);
    c.wdMax = Math.max(1, Number(c.wdMax) || 1);
    c.wdNow = clamp(Number(c.wdNow) || 0, 0, c.wdMax);
    c.wdTmp = Math.max(0, Number(c.wdTmp) || 0);
    c.speed = Math.max(0, Number(c.speed) || 0);
    c.currency = {
      gold: Math.max(0, Number(c.currency?.gold) || 0),
      silver: Math.max(0, Number(c.currency?.silver) || 0),
      copper: Math.max(0, Number(c.currency?.copper) || 0),
    };
    const lines = Array.isArray(c.abilityLines) ? c.abilityLines.map(normalizeAbilityLine) : [];
    while (lines.length < ABILITY_LINE_COUNT) lines.push(null);
    c.abilityLines = lines.slice(0, ABILITY_LINE_COUNT);
    c.activeText = String(c.activeText ?? "");
    c.lineageText = String(c.lineageText ?? "");
    c.heritageText = String(c.heritageText ?? "");
    c.backgroundText = String(c.backgroundText ?? "");
    c.spellListText = String(c.spellListText ?? "");
    c.inventoryText = String(c.inventoryText ?? "");
    return c;
  }

  function activeCharacter() {
    char = store.characters.find((c) => c.id === store.activeId) || null;
    return char;
  }

  function stepper(id, value, label, opts) {
    const min = opts?.min ?? -5;
    const max = opts?.max ?? 5;
    const display = opts?.display ?? formatMod(value);
    return `<div class="cs-stepper" data-stepper="${id}" data-min="${min}" data-max="${max}">
      <span class="cs-stepper-val" aria-live="polite">${escapeHtml(display)}</span>
      <div class="cs-stepper-btns">
        <button type="button" class="cs-stepper-btn" data-delta="-1" aria-label="Decrease ${label}">▼</button>
        <button type="button" class="cs-stepper-btn" data-delta="1" aria-label="Increase ${label}">▲</button>
      </div>
    </div>`;
  }

  function handleStepper(id, delta) {
    if (!char) return;
    if (id === "fit" || id === "ins" || id === "wil") {
      char[id] = clamp(char[id] + delta, -5, 5);
    } else if (id === "def") {
      char.def = clamp(char.def + delta, -5, 30);
    } else if (id === "res") {
      char.res = clamp(char.res + delta, 0, resolveMax(char));
    } else if (id === "sp-max") {
      char.spMax = Math.max(0, char.spMax + delta);
      char.spNow = Math.min(char.spNow, char.spMax);
    } else if (id === "sp-now") {
      char.spNow = clamp(char.spNow + delta, 0, char.spMax);
    } else if (id === "wd-max") {
      char.wdMax = Math.max(1, char.wdMax + delta);
      char.wdNow = Math.min(char.wdNow, char.wdMax);
    } else if (id === "wd-now") {
      char.wdNow = clamp(char.wdNow + delta, 0, char.wdMax);
    } else if (id === "wd-tmp") {
      char.wdTmp = Math.max(0, char.wdTmp + delta);
    } else if (id === "speed") {
      char.speed = Math.max(0, char.speed + delta * 5);
    } else if (id === "hearts") {
      char.hearts = clamp(char.hearts + delta, 0, 3);
    }
    persistAndRender();
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
    if (!char) {
      if (el.sheet) el.sheet.innerHTML = "";
      return;
    }
    renderSheet();
  }

  function persistAndRender() {
    if (!char) return;
    normalizeCharacter(char);
    saveStore();
    render();
    if (abilityModalLine != null) renderAbilityModal();
  }

  function setActive(id) {
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
    const c = defaultCharacter();
    store.characters.push(c);
    store.activeId = c.id;
    saveStore();
    render();
  }

  function deleteCharacter() {
    if (!char) return;
    const name = char.name || "Unnamed";
    if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
    store.characters = store.characters.filter((c) => c.id !== char.id);
    store.activeId = store.characters.length ? store.characters[0].id : null;
    saveStore();
    render();
  }

  function renderSheet() {
    if (!el.sheet || !char) return;
    const c = char;

    const heartsHtml = [0, 1, 2].map((i) => {
      const filled = i < c.hearts;
      return `<button type="button" class="cs-heart${filled ? " is-full" : " is-empty"}" data-heart="${i}" aria-label="Heart ${i + 1}${filled ? ", remaining" : ", lost"}">${filled ? "♥" : "♡"}</button>`;
    }).join("");
    const deadIconHtml = c.hearts <= 0
      ? `<img src="assets/dead-head.svg" class="cls-dead-icon" alt="Dead" aria-hidden="true" />`
      : "";
    const lost = heartsLost(c);
    const penaltyNoteHtml = c.hearts <= 0
      ? `<p class="cs-penalty-note">Dead</p>`
      : lost
        ? `<p class="cs-penalty-note">−${lost} to each ability mod, −${5 * lost} ft speed, −${2 * lost} Max WD</p>`
        : "";
    const weakened = c.hearts === 1 || c.hearts === 2;
    const penaltyMark = (effective) => weakened
      ? `<span class="cs-penalty-mark">(${effective})</span>`
      : "";

    const abilityLinesHtml = c.abilityLines.map((entry, i) => {
      if (entry && entry.name) {
        const notesHtml = entry.notes
          ? `<span class="cls-ability-notes">${escapeHtml(entry.notes)}</span>`
          : "";
        return `<div class="cls-ability-row">
          <button type="button" class="cls-ability-slot is-filled" data-ability-line="${i}" aria-label="Ability ${i + 1}: ${escapeHtml(entry.name)}. Click to change selection.">
            <span class="cls-ability-main">
              <strong class="cls-ability-name">${escapeHtml(entry.name)}</strong><span class="cls-ability-sep">: </span><span class="cls-ability-desc">${escapeHtml(entry.description)}</span>
            </span>
            ${notesHtml}
          </button>
          <button type="button" class="cls-ability-edit" data-ability-edit="${i}" title="Edit ability text and notes" aria-label="Edit ability ${i + 1}">✎</button>
        </div>`;
      }
      return `<div class="cls-ability-row">
        <button type="button" class="cls-ability-slot" data-ability-line="${i}" aria-label="Ability ${i + 1}, choose trained ability">
          <span class="cls-ability-empty">Trained ability…</span>
        </button>
      </div>`;
    }).join("");

    el.sheet.innerHTML = `
      <div class="cs-col cs-col--stats">
        <div class="cs-field cs-field--name">
          <label class="cs-label" for="cls-name">Name</label>
          <input type="text" id="cls-name" class="cs-input cs-input--name" value="${escapeHtml(c.name)}" autocomplete="off" />
        </div>

        <div class="cs-life-level">
          <div class="cs-life">
            <span class="cs-label">Life</span>
            <div class="cls-hearts-row">
              ${deadIconHtml}
              <div class="cs-hearts" role="group" aria-label="Life hearts">${heartsHtml}</div>
            </div>
            ${stepper("hearts", c.hearts, "Hearts", { min: 0, max: 3, display: String(c.hearts) })}
            ${penaltyNoteHtml}
          </div>
        </div>

        <div class="cs-abilities-row">
          <div class="cs-stat-box">
            <span class="cs-stat-label">FIT</span>
            ${stepper("fit", c.fit, "Fitness", { display: formatMod(c.fit) })}${penaltyMark(formatMod(c.fit - lost))}
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">INS</span>
            ${stepper("ins", c.ins, "Insight", { display: formatMod(c.ins) })}${penaltyMark(formatMod(c.ins - lost))}
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">WILL</span>
            ${stepper("wil", c.wil, "Willpower", { display: formatMod(c.wil) })}${penaltyMark(formatMod(c.wil - lost))}
          </div>
        </div>

        <div class="cs-abilities-row">
          <div class="cs-stat-box">
            <span class="cs-stat-label">DEF</span>
            ${stepper("def", c.def, "Defense", { min: -5, max: 30, display: formatMod(c.def) })}
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">SP</span>
            <div class="cs-wd-grid">
              <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span>${stepper("sp-max", c.spMax, "Spell Power max", { min: 0, max: 99, display: String(c.spMax) })}</div>
              <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("sp-now", c.spNow, "Spell Power now", { min: 0, max: c.spMax, display: String(c.spNow) })}</div>
            </div>
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">RES</span>
            <div class="cs-wd-grid">
              <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span><span class="cs-wd-val cs-wd-val--calc" title="4 + Willpower modifier ÷ 2, rounded up">${resolveMax(c)}</span></div>
              <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("res", c.res, "Resolve", { min: 0, max: resolveMax(c), display: String(c.res) })}</div>
            </div>
          </div>
        </div>

        <div class="cs-stat-box cs-stat-box--wd">
          <span class="cs-stat-label">WD</span>
          <div class="cs-wd-grid">
            <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span>${stepper("wd-max", c.wdMax, "Max Wounds", { min: 1, max: 99, display: String(c.wdMax) })}${penaltyMark(Math.max(0, c.wdMax - 2 * lost))}</div>
            <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("wd-now", c.wdNow, "Current Wounds", { min: 0, max: c.wdMax, display: String(c.wdNow) })}</div>
            <div class="cs-wd-cell"><span class="cs-wd-lbl">TMP</span>${stepper("wd-tmp", c.wdTmp, "Temporary Wounds", { min: 0, max: 99, display: String(c.wdTmp) })}</div>
          </div>
        </div>

        <div class="cs-pane cs-pane--active">
          <h2 class="cs-pane-title">Active Equipment | Spells | Abilities</h2>
          <textarea class="cs-textarea" id="cls-active" rows="10" placeholder="What's equipped and ready to use right now…">${escapeHtml(c.activeText)}</textarea>
        </div>
      </div>

      <div class="cs-col cs-col--trained">
        <div class="cs-field cs-field--xp">
          <label class="cs-label" for="cls-xp">Available XP</label>
          <input type="number" id="cls-xp" class="cs-input cs-input--xp" min="0" step="1" value="${c.xp}" aria-label="Available experience points" />
          <span class="cs-xp-hint">Banked for training</span>
        </div>

        <div class="cs-currency">
          <div class="cs-coin"><span class="cs-coin-lbl">G</span><input type="number" min="0" class="cs-coin-input" data-coin="gold" value="${c.currency.gold}" aria-label="Gold" /></div>
          <div class="cs-coin"><span class="cs-coin-lbl">S</span><input type="number" min="0" class="cs-coin-input" data-coin="silver" value="${c.currency.silver}" aria-label="Silver" /></div>
          <div class="cs-coin"><span class="cs-coin-lbl">C</span><input type="number" min="0" class="cs-coin-input" data-coin="copper" value="${c.currency.copper}" aria-label="Copper" /></div>
        </div>

        <div class="cs-pane cs-pane--ability-list">
          <h2 class="cs-pane-title">Abilities</h2>
          <div class="cls-ability-lines">${abilityLinesHtml}</div>
        </div>
      </div>

      <div class="cs-col cs-col--identity">
        <div class="cs-pane cs-pane--details">
          <div class="cls-details-header">
            <h2 class="cs-pane-title">Details</h2>
            <div class="cs-stat-box cls-stat-box--speed">
              <span class="cs-stat-label">Speed</span>
              ${stepper("speed", c.speed, "Speed", { min: 0, max: 120, display: `${c.speed} ft` })}${penaltyMark(`${Math.max(0, c.speed - 5 * lost)} ft`)}
            </div>
          </div>
          <div class="cs-field">
            <label class="cs-label" for="cls-lineage">Lineage</label>
            <textarea class="cs-textarea" id="cls-lineage" rows="3" placeholder="Ancestry traits…">${escapeHtml(c.lineageText)}</textarea>
          </div>
          <div class="cs-field">
            <label class="cs-label" for="cls-heritage">Heritage</label>
            <textarea class="cs-textarea" id="cls-heritage" rows="3" placeholder="Cultural traits, languages…">${escapeHtml(c.heritageText)}</textarea>
          </div>
          <div class="cs-field">
            <label class="cs-label" for="cls-background">Background</label>
            <textarea class="cs-textarea" id="cls-background" rows="3" placeholder="Skills, proficiencies, talent…">${escapeHtml(c.backgroundText)}</textarea>
          </div>
        </div>

        <div class="cs-pane cs-pane--spelllist">
          <h2 class="cs-pane-title">Spell List</h2>
          <textarea class="cs-textarea" id="cls-spelllist" rows="8" placeholder="Cantrips and learned/known spells…">${escapeHtml(c.spellListText)}</textarea>
        </div>

        <div class="cs-pane cs-pane--inventory">
          <h2 class="cs-pane-title">Inventory</h2>
          <textarea class="cs-textarea" id="cls-inventory" rows="8" placeholder="Carried gear…">${escapeHtml(c.inventoryText)}</textarea>
        </div>
      </div>`;
  }

  function ownedAbilityIds(excludeLine) {
    if (!char) return new Set();
    const ids = new Set();
    char.abilityLines.forEach((entry, i) => {
      if (i === excludeLine) return;
      if (entry && entry.id) ids.add(entry.id);
    });
    return ids;
  }

  function abilityCost(abilityOrId) {
    const ability = typeof abilityOrId === "string" ? abilityById(abilityOrId) : abilityOrId;
    if (!ability || ability.xp == null) return 0;
    return Number(ability.xp) || 0;
  }

  function availableXpForLine(lineIndex) {
    if (!char) return 0;
    const current = char.abilityLines[lineIndex];
    const refund = current && current.id ? abilityCost(current.id) : 0;
    return char.xp + refund;
  }

  function selectedIdsExcept(excludeId) {
    return abilityModalSelectedIds.filter((id) => id !== excludeId);
  }

  function selectedCostExcept(excludeId) {
    return selectedIdsExcept(excludeId).reduce((sum, id) => sum + abilityCost(id), 0);
  }

  function pendingOwnedIds(lineIndex, excludeId) {
    const owned = ownedAbilityIds(lineIndex);
    selectedIdsExcept(excludeId).forEach((id) => owned.add(id));
    return owned;
  }

  function orderSelectedByRequires(ids) {
    const idSet = new Set(ids);
    const result = [];
    const visiting = new Set();

    function visit(id) {
      if (!idSet.has(id) || result.includes(id)) return;
      if (visiting.has(id)) return;
      visiting.add(id);
      const ability = abilityById(id);
      (ability?.requires || []).forEach(visit);
      visiting.delete(id);
      if (!result.includes(id)) result.push(id);
    }

    ids.forEach(visit);
    ids.forEach((id) => {
      if (!result.includes(id)) result.push(id);
    });
    return result;
  }

  function findTargetSlots(startIndex, count) {
    if (count <= 0) return [];
    const targets = [startIndex];
    for (let i = startIndex + 1; i < ABILITY_LINE_COUNT && targets.length < count; i++) {
      if (!char.abilityLines[i]) targets.push(i);
    }
    return targets;
  }

  function evaluateAbility(ability, lineIndex) {
    const owned = pendingOwnedIds(lineIndex, ability.id);
    const reasons = [];
    const cost = abilityCost(ability);
    const budget = availableXpForLine(lineIndex) - selectedCostExcept(ability.id);
    const currentId = char && char.abilityLines[lineIndex] ? char.abilityLines[lineIndex].id : null;
    const isSelected = abilityModalSelectedIds.includes(ability.id);
    const isCurrent = currentId === ability.id;

    if (!isSelected && owned.has(ability.id)) {
      reasons.push("Already trained in another slot");
    }

    (ability.requires || []).forEach((reqId) => {
      if (owned.has(reqId) || reqId === currentId) return;
      const req = abilityById(reqId);
      reasons.push("Requires " + (req ? req.name : reqId));
    });

    if (Array.isArray(ability.requiresAny) && ability.requiresAny.length) {
      const ok = ability.requiresAny.some((reqId) => owned.has(reqId) || reqId === currentId);
      if (!ok) reasons.push("Requires a matching weapon proficiency");
    }

    if (ability.requiresFit != null && char) {
      const fitEff = char.fit - heartsLost(char);
      if (fitEff < ability.requiresFit) {
        reasons.push("Requires Fitness " + (ability.requiresFit >= 0 ? "+" : "") + ability.requiresFit + " or higher");
      }
    }

    if (ability.requiresCastingMod != null && char) {
      const lost = heartsLost(char);
      const casting = Math.max(char.ins - lost, char.wil - lost);
      if (casting < ability.requiresCastingMod) {
        reasons.push("Requires Insight or Willpower +" + ability.requiresCastingMod + " or higher");
      }
    }

    if (!isSelected && cost > budget) {
      reasons.push("Not enough experience (needs " + cost + " XP, " + Math.max(0, budget) + " available)");
    }

    if (!isSelected) {
      const neededSlots = abilityModalSelectedIds.length + 1;
      const targets = findTargetSlots(lineIndex, neededSlots);
      if (targets.length < neededSlots) {
        reasons.push("Not enough empty ability slots");
      }
    }

    return {
      selectable: reasons.length === 0,
      reasons: reasons,
      cost: cost,
      budget: budget,
      isCurrent: isCurrent,
      isSelected: isSelected,
    };
  }

  function partitionAbilities(lineIndex) {
    const available = [];
    const unavailable = [];
    (abilitiesData && abilitiesData.abilities ? abilitiesData.abilities : []).forEach((ability) => {
      const evalResult = evaluateAbility(ability, lineIndex);
      const item = Object.assign({ ability: ability }, evalResult);
      if (evalResult.selectable) available.push(item);
      else unavailable.push(item);
    });
    return { available: available, unavailable: unavailable };
  }

  function groupItems(items) {
    const groups = [];
    const seen = new Map();
    items.forEach((item) => {
      const ability = item.ability;
      const key = ability.categoryId || "other";
      if (!seen.has(key)) {
        seen.set(key, { id: key, name: ability.category || "Other", items: [] });
        groups.push(seen.get(key));
      }
      seen.get(key).items.push(item);
    });
    return groups;
  }

  function renderAbilityCards(items, sectionDisabled) {
    return items.map((item) => {
      const ability = item.ability;
      const selectable = item.selectable;
      const reasons = item.reasons;
      const cost = item.cost;
      const isCurrent = item.isCurrent;
      const selected = abilityModalSelectedIds.includes(ability.id);
      const xpLabel = cost ? cost + " XP" : "";
      const reasonText = reasons.length ? reasons.join(" · ") : "";
      const classes = [
        "cls-ability-card",
        selected ? "is-selected" : "",
        sectionDisabled || !selectable ? "is-disabled" : "",
        isCurrent ? "is-current" : "",
      ].filter(Boolean).join(" ");
      return `<button type="button" class="${classes}" data-ability-id="${escapeHtml(ability.id)}" data-selectable="${selectable ? "1" : "0"}" aria-pressed="${selected ? "true" : "false"}"${sectionDisabled || !selectable ? ' aria-disabled="true"' : ""}>
        <span class="cls-ability-card-header">
          <span class="cls-ability-card-title">${escapeHtml(ability.name)}</span>
          ${xpLabel ? `<span class="cls-ability-card-xp">${escapeHtml(xpLabel)}</span>` : ""}
        </span>
        <span class="cls-ability-card-body">${escapeHtml(ability.description)}</span>
        ${reasonText ? `<span class="cls-ability-card-reason">${escapeHtml(reasonText)}</span>` : ""}
      </button>`;
    }).join("");
  }

  function renderAbilitySection(title, items) {
    if (!items.length) return "";
    const groups = groupItems(items);
    const disabled = title !== "Available now";
    const groupsHtml = groups.map((group) => `<section class="cls-ability-group">
        <h3 class="cls-ability-group-title">${escapeHtml(group.name)}</h3>
        <div class="cls-ability-card-list">${renderAbilityCards(group.items, disabled)}</div>
      </section>`).join("");
    return `<div class="cls-ability-section">
      <h2 class="cls-ability-section-title">${escapeHtml(title)}</h2>
      ${groupsHtml}
    </div>`;
  }

  function openAbilityModal(lineIndex) {
    if (!abilitiesData || !char || !el.modalRoot) return;
    abilityEditLine = null;
    abilityModalLine = lineIndex;
    const current = char.abilityLines[lineIndex];
    let initialId = current && current.id ? current.id : null;
    if (!initialId && current && current.name) {
      const match = (abilitiesData.abilities || []).find((a) => a.name === current.name);
      initialId = match ? match.id : null;
    }
    abilityModalSelectedIds = initialId ? [initialId] : [];
    abilityModalMessage = "";
    renderAbilityModal();
  }

  function closeAbilityModal() {
    abilityModalLine = null;
    abilityModalSelectedIds = [];
    abilityModalMessage = "";
    if (el.modalRoot && abilityEditLine == null) el.modalRoot.innerHTML = "";
  }

  function openAbilityEditModal(lineIndex) {
    if (!char || !el.modalRoot) return;
    const entry = char.abilityLines[lineIndex];
    if (!entry) return;
    abilityEditLine = lineIndex;
    abilityModalLine = null;
    abilityModalSelectedIds = [];
    abilityModalMessage = "";
    renderAbilityEditModal();
  }

  function closeAbilityEditModal() {
    abilityEditLine = null;
    if (el.modalRoot) el.modalRoot.innerHTML = "";
  }

  function applyAbilityEdit() {
    if (!char || abilityEditLine == null || !el.modalRoot) return;
    const nameInput = el.modalRoot.querySelector("#cls-ability-edit-name");
    const descInput = el.modalRoot.querySelector("#cls-ability-edit-desc");
    const notesInput = el.modalRoot.querySelector("#cls-ability-edit-notes");
    const entry = char.abilityLines[abilityEditLine];
    if (!entry) {
      closeAbilityEditModal();
      return;
    }
    const name = (nameInput?.value || "").trim();
    const description = (descInput?.value || "").trim();
    const notes = (notesInput?.value || "").trim();
    if (!name) {
      abilityModalMessage = "Name is required.";
      renderAbilityEditModal({ name, description, notes });
      return;
    }
    char.abilityLines[abilityEditLine] = {
      ...entry,
      name,
      description,
      notes,
    };
    closeAbilityEditModal();
    persistAndRender();
  }

  function renderAbilityEditModal(draft) {
    if (!el.modalRoot || abilityEditLine == null || !char) return;
    const entry = char.abilityLines[abilityEditLine] || {};
    const name = draft?.name != null ? draft.name : (entry.name || "");
    const description = draft?.description != null ? draft.description : (entry.description || "");
    const notes = draft?.notes != null ? draft.notes : (entry.notes || "");
    const messageHtml = abilityModalMessage
      ? `<p class="cls-ability-modal-message" role="alert">${escapeHtml(abilityModalMessage)}</p>`
      : "";

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cls-ability-edit-overlay">
      <div class="cs-modal cls-ability-edit-modal" role="dialog" aria-modal="true" aria-labelledby="cls-ability-edit-title">
        <div class="cs-modal-header">
          <h2 id="cls-ability-edit-title">Edit Ability</h2>
          <button type="button" class="cs-modal-close" id="cls-ability-edit-close" aria-label="Close">×</button>
        </div>
        <p class="cls-ability-modal-hint">Customize the wording or add personal notes. XP cost and training identity stay linked to the original ability.</p>
        ${messageHtml}
        <div class="cs-modal-body cls-ability-edit-body">
          <label class="cs-label" for="cls-ability-edit-name">Name</label>
          <input type="text" id="cls-ability-edit-name" class="cs-input" value="${escapeHtml(name)}" autocomplete="off" />
          <label class="cs-label" for="cls-ability-edit-desc">Description</label>
          <textarea id="cls-ability-edit-desc" class="cs-textarea" rows="5">${escapeHtml(description)}</textarea>
          <label class="cs-label" for="cls-ability-edit-notes">Notes</label>
          <textarea id="cls-ability-edit-notes" class="cs-textarea" rows="3" placeholder="House rulings, reminders, customization…">${escapeHtml(notes)}</textarea>
        </div>
        <div class="cls-ability-modal-footer">
          <button type="button" class="btn cs-btn-secondary" id="cls-ability-edit-cancel">Cancel</button>
          <button type="button" class="btn" id="cls-ability-edit-save">Save</button>
        </div>
      </div>
    </div>`;
  }

  function applyAbilityChoice() {
    if (!char || abilityModalLine == null) return;
    const lineIndex = abilityModalLine;
    const previous = char.abilityLines[lineIndex];
    const previousCost = previous && previous.id ? abilityCost(previous.id) : 0;

    if (!abilityModalSelectedIds.length) {
      char.xp += previousCost;
      char.abilityLines[lineIndex] = null;
      closeAbilityModal();
      persistAndRender();
      return;
    }

    const orderedIds = orderSelectedByRequires(abilityModalSelectedIds);
    const targets = findTargetSlots(lineIndex, orderedIds.length);
    if (targets.length < orderedIds.length) {
      abilityModalMessage = "Not enough empty ability slots for " + orderedIds.length + " abilities.";
      renderAbilityModal();
      return;
    }

    let budget = availableXpForLine(lineIndex);
    const placements = [];
    for (let i = 0; i < orderedIds.length; i++) {
      const ability = abilityById(orderedIds[i]);
      if (!ability) {
        abilityModalMessage = "That ability could not be found.";
        renderAbilityModal();
        return;
      }
      // Simulate ownership of abilities already placed in this batch
      const simulated = evaluateAbilityForApply(ability, lineIndex, orderedIds.slice(0, i), budget);
      if (!simulated.ok) {
        abilityModalMessage = simulated.reason || "Requirements not met.";
        renderAbilityModal();
        return;
      }
      if (abilityCost(ability) > budget) {
        abilityModalMessage = "Not enough experience (needs " + abilityCost(ability) + " XP, " + budget + " available).";
        renderAbilityModal();
        return;
      }
      budget -= abilityCost(ability);
      placements.push({ slot: targets[i], ability: ability });
    }

    char.xp = budget;
    placements.forEach((placement) => {
      const existing = char.abilityLines[placement.slot];
      const sameAbility = existing && existing.id === placement.ability.id;
      char.abilityLines[placement.slot] = {
        id: placement.ability.id,
        name: sameAbility && existing.name ? existing.name : placement.ability.name,
        description: sameAbility ? (existing.description || "") : placement.ability.description,
        notes: sameAbility ? (existing.notes || "") : "",
        xp: placement.ability.xp,
      };
    });
    closeAbilityModal();
    persistAndRender();
  }

  function evaluateAbilityForApply(ability, lineIndex, priorBatchIds, budget) {
    const owned = ownedAbilityIds(lineIndex);
    priorBatchIds.forEach((id) => owned.add(id));
    const currentId = char.abilityLines[lineIndex]?.id || null;

    if (owned.has(ability.id)) {
      return { ok: false, reason: "Already trained in another slot" };
    }
    for (const reqId of ability.requires || []) {
      if (owned.has(reqId) || reqId === currentId) continue;
      const req = abilityById(reqId);
      return { ok: false, reason: "Requires " + (req ? req.name : reqId) };
    }
    if (Array.isArray(ability.requiresAny) && ability.requiresAny.length) {
      const ok = ability.requiresAny.some((reqId) => owned.has(reqId) || reqId === currentId);
      if (!ok) return { ok: false, reason: "Requires a matching weapon proficiency" };
    }
    if (ability.requiresFit != null) {
      const fitEff = char.fit - heartsLost(char);
      if (fitEff < ability.requiresFit) {
        return { ok: false, reason: "Requires Fitness +" + ability.requiresFit + " or higher" };
      }
    }
    if (ability.requiresCastingMod != null) {
      const lost = heartsLost(char);
      const casting = Math.max(char.ins - lost, char.wil - lost);
      if (casting < ability.requiresCastingMod) {
        return { ok: false, reason: "Requires Insight or Willpower +" + ability.requiresCastingMod + " or higher" };
      }
    }
    if (abilityCost(ability) > budget) {
      return { ok: false, reason: "Not enough experience (needs " + abilityCost(ability) + " XP, " + budget + " available)" };
    }
    return { ok: true };
  }

  function renderAbilityModal() {
    if (!el.modalRoot || !abilitiesData || abilityModalLine == null || !char) return;
    const budget = availableXpForLine(abilityModalLine);
    const remaining = Math.max(0, budget - selectedCostExcept(null));
    const parts = partitionAbilities(abilityModalLine);
    const current = char.abilityLines[abilityModalLine];
    const refund = current && current.id ? abilityCost(current.id) : 0;
    const selectedCount = abilityModalSelectedIds.length;
    const messageHtml = abilityModalMessage
      ? `<p class="cls-ability-modal-message" role="alert">${escapeHtml(abilityModalMessage)}</p>`
      : "";
    const chooseLabel = selectedCount ? `Choose (${selectedCount})` : "Clear slot";

    el.modalRoot.innerHTML = `<div class="cs-modal-overlay" id="cls-ability-overlay">
      <div class="cs-modal cls-ability-modal" role="dialog" aria-modal="true" aria-labelledby="cls-ability-modal-title">
        <div class="cs-modal-header">
          <h2 id="cls-ability-modal-title">Choose Abilities</h2>
          <button type="button" class="cs-modal-close" id="cls-ability-close" aria-label="Close">×</button>
        </div>
        <p class="cls-ability-modal-hint">Select one or more abilities. They fill this slot and the next empty slots. Budget: <strong>${remaining}</strong> XP left of <strong>${budget}</strong> (banked ${char.xp}${refund ? ` + refund ${refund}` : ""})${selectedCount ? ` · ${selectedCount} selected` : ""}.</p>
        ${messageHtml}
        <div class="cs-modal-body cls-ability-modal-body">
          ${renderAbilitySection("Available now", parts.available)}
          ${renderAbilitySection("Not yet available", parts.unavailable)}
        </div>
        <div class="cls-ability-modal-footer">
          <button type="button" class="btn cs-btn-secondary" id="cls-ability-cancel">Cancel</button>
          <button type="button" class="btn" id="cls-ability-choose">${escapeHtml(chooseLabel)}</button>
        </div>
      </div>
    </div>`;
  }

  function trySelectAbilityCard(abilityId) {
    const ability = abilityById(abilityId);
    if (!ability || abilityModalLine == null) return;
    if (abilityModalSelectedIds.includes(abilityId)) {
      abilityModalSelectedIds = abilityModalSelectedIds.filter((id) => id !== abilityId);
      abilityModalMessage = "";
      renderAbilityModal();
      return;
    }
    const evaluation = evaluateAbility(ability, abilityModalLine);
    if (!evaluation.selectable) {
      abilityModalMessage = evaluation.reasons[0] || "Requirements not met.";
      renderAbilityModal();
      return;
    }
    abilityModalSelectedIds = abilityModalSelectedIds.concat(abilityId);
    abilityModalMessage = "";
    renderAbilityModal();
  }

  function bindEvents() {
    if (eventsBound) return;
    eventsBound = true;
    if (!el.charSelect || !el.sheet) return;

    el.charSelect.addEventListener("change", (e) => setActive(e.target.value));
    el.btnNew.addEventListener("click", newCharacter);
    el.btnDelete.addEventListener("click", deleteCharacter);
    if (el.btnPrint) {
      el.btnPrint.addEventListener("click", () => {
        applyPrintOrientation(el.printOrientation ? el.printOrientation.value : "portrait");
        window.print();
      });
    }

    el.sheet.addEventListener("click", (e) => {
      const editBtn = e.target.closest(".cls-ability-edit");
      if (editBtn && char) {
        const idx = parseInt(editBtn.dataset.abilityEdit, 10);
        openAbilityEditModal(idx);
        return;
      }
      const abilitySlot = e.target.closest(".cls-ability-slot");
      if (abilitySlot && char) {
        const idx = parseInt(abilitySlot.dataset.abilityLine, 10);
        openAbilityModal(idx);
        return;
      }
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
      }
    });

    el.sheet.addEventListener("input", (e) => {
      if (!char) return;
      const t = e.target;
      if (t.id === "cls-name") {
        char.name = t.value;
        saveStore();
        renderCharSelect();
        return;
      }
      if (t.id === "cls-active") { char.activeText = t.value; saveStore(); return; }
      if (t.id === "cls-lineage") { char.lineageText = t.value; saveStore(); return; }
      if (t.id === "cls-heritage") { char.heritageText = t.value; saveStore(); return; }
      if (t.id === "cls-background") { char.backgroundText = t.value; saveStore(); return; }
      if (t.id === "cls-spelllist") { char.spellListText = t.value; saveStore(); return; }
      if (t.id === "cls-inventory") { char.inventoryText = t.value; saveStore(); return; }
      if (t.id === "cls-xp") {
        char.xp = Math.max(0, parseInt(t.value, 10) || 0);
        saveStore();
        if (abilityModalLine != null) {
          abilityModalMessage = "";
          renderAbilityModal();
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
      if (t.id === "cls-xp") {
        char.xp = Math.max(0, parseInt(t.value, 10) || 0);
        saveStore();
        if (abilityModalLine != null) {
          abilityModalMessage = "";
          renderAbilityModal();
        }
      }
    });

    if (el.modalRoot) {
      el.modalRoot.addEventListener("click", (e) => {
        if (e.target.id === "cls-ability-overlay" || e.target.id === "cls-ability-close" || e.target.id === "cls-ability-cancel") {
          closeAbilityModal();
          return;
        }
        if (e.target.id === "cls-ability-choose") {
          applyAbilityChoice();
          return;
        }
        if (e.target.id === "cls-ability-edit-overlay" || e.target.id === "cls-ability-edit-close" || e.target.id === "cls-ability-edit-cancel") {
          closeAbilityEditModal();
          return;
        }
        if (e.target.id === "cls-ability-edit-save") {
          applyAbilityEdit();
          return;
        }
        const card = e.target.closest(".cls-ability-card");
        if (card) {
          trySelectAbilityCard(card.dataset.abilityId);
        }
      });
    }
  }

  async function init() {
    cacheElements();
    bindEvents();
    try {
      const res = await fetch(rp("assets/classless-abilities-data.json"));
      if (!res.ok) throw new Error("HTTP " + res.status);
      abilitiesData = await res.json();
    } catch (err) {
      console.error("Could not load classless abilities:", err);
      abilitiesData = { version: 1, abilities: [] };
    }
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
