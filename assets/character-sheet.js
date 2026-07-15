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

  let data = null;
  let store = loadStore();
  let char = null;
  let eventsBound = false;

  const el = {};

  function cacheElements() {
    el.loading = document.getElementById("cs-loading");
    el.error = document.getElementById("cs-error");
    el.app = document.getElementById("cs-app");
    el.charSelect = document.getElementById("cs-char-select");
    el.sheet = document.getElementById("cs-sheet");
    el.btnNew = document.getElementById("cs-btn-new");
    el.btnImport = document.getElementById("cs-btn-import");
    el.btnDelete = document.getElementById("cs-btn-delete");
  }

  function rootPath() {
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
      hearts: 3,
      abilities: { fit: 0, ins: 0, wil: 0 },
      woundsNow: 0,
      woundsTemp: 0,
      defense: 10,
      resolve: 0,
      spellPowerNow: 0,
      classId: "",
      subclassId: "",
      lineageId: "",
      heritageId: "",
      backgroundId: "",
      speed: 30,
      size: "Medium",
      currency: { gold: 0, silver: 0, copper: 0 },
      equippedText: "",
      inventory: Array(INVENTORY_SLOT_COUNT).fill(""),
    };
  }

  function defaultStore() {
    const first = defaultCharacter();
    return { version: 1, activeId: first.id, characters: [first] };
  }

  function loadStore() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed.characters && parsed.characters.length) {
          parsed.characters = parsed.characters.filter(Boolean).map((c) => {
            try {
              return normalizeCharacter(c);
            } catch (_) {
              return normalizeCharacter(defaultCharacter());
            }
          });
          if (!parsed.activeId || !parsed.characters.some((c) => c.id === parsed.activeId)) {
            parsed.activeId = parsed.characters[0].id;
          }
          return parsed;
        }
      }
    } catch (_) { /* ignore */ }
    return defaultStore();
  }

  function normalizeCharacter(c) {
    c.level = Math.min(10, Math.max(1, Number(c.level) || 1));
    c.hearts = Math.min(3, Math.max(0, Number.isFinite(Number(c.hearts)) ? Number(c.hearts) : 3));
    c.resolve = Math.min(4, Math.max(0, Number(c.resolve) || 0));
    c.abilities = c.abilities || { fit: 0, ins: 0, wil: 0 };
    ABILITIES.forEach((a) => {
      c.abilities[a] = clampAbility(Number(c.abilities[a]) || 0);
    });
    c.woundsNow = Math.max(0, Number(c.woundsNow) || 0);
    c.woundsTemp = Math.max(0, Number(c.woundsTemp) || 0);
    c.defense = Number(c.defense) || 10;
    c.spellPowerNow = Math.max(0, Number(c.spellPowerNow) || 0);
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
    char = store.characters.find((c) => c.id === store.activeId) || store.characters[0];
    store.activeId = char.id;
    return char;
  }

  function byId(list, id) {
    return (list || []).find((item) => item.id === id) || null;
  }

  function levelRange() {
    return data?.levelRange || { min: 1, max: 10, subclassMin: 2 };
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
      <button type="button" class="cs-stepper-btn" data-delta="-1" aria-label="Decrease ${label}">▼</button>
      <span class="cs-stepper-val" aria-live="polite">${escapeHtml(display)}</span>
      <button type="button" class="cs-stepper-btn" data-delta="1" aria-label="Increase ${label}">▲</button>
      ${hint}
    </div>`;
  }

  function renderSheet() {
    if (!el.sheet || !data) return;
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

        <div class="cs-life-level">
          <div class="cs-life">
            <span class="cs-label">Life</span>
            <div class="cs-hearts" role="group" aria-label="Life hearts">${heartsHtml}</div>
            ${stepper("hearts", c.hearts, "Hearts", { min: 0, max: 3, display: String(c.hearts) })}
            ${lost ? `<p class="cs-penalty-note">−${lost} to each ability mod, −${5 * lost} ft speed, −${2 * lost} Max WD</p>` : ""}
          </div>
          <div class="cs-level">
            <span class="cs-label">LVL</span>
            <div class="cs-level-circle">${c.level}</div>
            ${stepper("level", c.level, "Level", { min: range.min, max: range.max, display: String(c.level) })}
          </div>
        </div>

        <div class="cs-abilities-row">${abilityBoxes}</div>

        <div class="cs-combat-row">
          <div class="cs-stat-box cs-stat-box--wd">
            <span class="cs-stat-label">WD</span>
            <div class="cs-wd-grid">
              <div class="cs-wd-cell"><span class="cs-wd-lbl">MAX</span><span class="cs-wd-val cs-wd-val--calc" title="Class ${cls ? cls.maxWd : 8} + FIT ${formatMod(effectiveMod(c, "fit"))} + level −1">${maxWd}</span></div>
              <div class="cs-wd-cell"><span class="cs-wd-lbl">NOW</span>${stepper("wd-now", c.woundsNow, "Current wounds", { min: 0, max: 999, display: String(c.woundsNow) })}</div>
              <div class="cs-wd-cell"><span class="cs-wd-lbl">TMP</span>${stepper("wd-tmp", c.woundsTemp, "Temporary wounds", { min: 0, max: 999, display: String(c.woundsTemp) })}</div>
            </div>
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">DEF</span>
            ${stepper("defense", c.defense, "Defense", { min: 0, max: 30, display: String(c.defense) })}
          </div>
          <div class="cs-stat-box">
            <span class="cs-stat-label">Resolve</span>
            ${stepper("resolve", c.resolve, "Resolve", { min: 0, max: 4, display: String(c.resolve) })}
          </div>
        </div>

        ${spSection}

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

        <div class="cs-pane cs-pane--abilities">
          <h2 class="cs-pane-title">Abilities</h2>
          ${cls ? `<p class="cs-class-summary">${escapeHtml(cls.summary || "")}</p>` : '<p class="cs-muted">Choose a class to see features.</p>'}
          ${abilitiesHtml}
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
          <textarea class="cs-textarea" id="cs-equipped" rows="4" placeholder="Armor, weapons, worn items…">${escapeHtml(c.equippedText)}</textarea>
        </div>

        <div class="cs-pane cs-pane--inventory">
          <h2 class="cs-pane-title">Inventory <span class="cs-inv-count">${unlocked}/${INVENTORY_SLOT_COUNT} slots (FIT ${formatMod(effectiveMod(c, "fit"))})</span></h2>
          <div class="cs-inv-grid">${inventoryRows}</div>
        </div>
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

  function renderCharSelect() {
    el.charSelect.innerHTML = store.characters
      .map((c) => `<option value="${c.id}"${c.id === store.activeId ? " selected" : ""}>${escapeHtml(c.name || "Unnamed")}</option>`)
      .join("");
  }

  function render() {
    activeCharacter();
    renderCharSelect();
    renderSheet();
    clampWoundsAndSp();
  }

  function persistAndRender() {
    normalizeCharacter(char);
    saveStore();
    render();
  }

  function clampWoundsAndSp() {
    const maxWd = computeMaxWd(char);
    if (char.woundsNow > maxWd) char.woundsNow = maxWd;
    const spMax = computeSpellPowerMax(char);
    if (spMax !== null && char.spellPowerNow > spMax) char.spellPowerNow = spMax;
  }

  function setActive(id) {
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
    if (store.characters.length <= 1) {
      alert("You need at least one character. Create another before deleting this one.");
      return;
    }
    const name = char.name || "Unnamed";
    if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
    store.characters = store.characters.filter((c) => c.id !== char.id);
    store.activeId = store.characters[0].id;
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
      store.characters.push(c);
      store.activeId = c.id;
      saveStore();
      render();
    } catch (e) {
      alert("Could not import creator draft.");
    }
  }

  function handleStepper(id, delta) {
    if (id.startsWith("ability-")) {
      const ab = id.slice(8);
      char.abilities[ab] = clampAbility(char.abilities[ab] + delta);
    } else if (id === "hearts") {
      char.hearts = Math.min(3, Math.max(0, char.hearts + delta));
    } else if (id === "level") {
      const range = levelRange();
      char.level = Math.min(range.max, Math.max(range.min, char.level + delta));
      if (char.level < (range.subclassMin || 2)) char.subclassId = "";
    } else if (id === "wd-now") {
      char.woundsNow = Math.max(0, char.woundsNow + delta);
    } else if (id === "wd-tmp") {
      char.woundsTemp = Math.max(0, char.woundsTemp + delta);
    } else if (id === "defense") {
      char.defense = Math.min(30, Math.max(0, char.defense + delta));
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
      if (heart) {
        const idx = parseInt(heart.dataset.heart, 10);
        char.hearts = idx + 1;
        persistAndRender();
      }
    });

    el.sheet.addEventListener("input", (e) => {
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
      const t = e.target;
      if (t.id === "cs-class") {
        char.classId = t.value;
        char.subclassId = "";
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
        persistAndRender();
      } else if (t.id === "cs-background") {
        char.backgroundId = t.value;
        persistAndRender();
      }
    });
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
