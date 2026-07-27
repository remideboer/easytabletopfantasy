/**
 * YMIAT Classless Character Sheet — local character management.
 * Standalone from the class-based sheet: no shared data file, everything
 * beyond the core stat boxes (FIT/INS/WILL, DEF, RES, SP, WD, Speed) is
 * free-form text, since Classless abilities are trained individually
 * rather than picked from a fixed class list. Persistence in localStorage.
 */
(function () {
  const STORAGE_KEY = "ymiat-classless-characters-v1";
  const ABILITY_LINE_COUNT = 10;

  let store = loadStore();
  let char = null;
  let eventsBound = false;

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
      xp: 0,
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
      abilityLines: Array(ABILITY_LINE_COUNT).fill(""),
      activeText: "",
      lineageText: "",
      heritageText: "",
      backgroundText: "",
      spellListText: "",
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
    const lines = Array.isArray(c.abilityLines) ? c.abilityLines.map((v) => String(v ?? "")) : [];
    while (lines.length < ABILITY_LINE_COUNT) lines.push("");
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

    const abilityLinesHtml = c.abilityLines.map((val, i) =>
      `<textarea class="cs-input cls-ability-line" rows="1" data-ability-line="${i}" placeholder="Trained ability…" aria-label="Ability ${i + 1}">${escapeHtml(val)}</textarea>`
    ).join("");

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
          <label class="cs-label" for="cls-xp">Experience Points</label>
          <input type="number" id="cls-xp" class="cs-input cs-input--xp" min="0" step="1" value="${c.xp}" aria-label="Experience points" />
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
      if (t.dataset.abilityLine != null) {
        const idx = parseInt(t.dataset.abilityLine, 10);
        char.abilityLines[idx] = t.value;
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
      if (t.id === "cls-xp") {
        char.xp = Math.max(0, parseInt(t.value, 10) || 0);
        saveStore();
      }
    });
  }

  function init() {
    cacheElements();
    bindEvents();
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
