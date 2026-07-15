/**
 * YMIAT Character Creator — data-driven wizard.
 * Options loaded from assets/character-creator-data.json (generated from Python sources).
 */
(function () {
  const STORAGE_KEY = "ymiat-character-creator-v1";
  const ABILITIES = ["fit", "ins", "wil"];
  const ABILITY_LABELS = { fit: "Fitness", ins: "Insight", wil: "Willpower" };

  let data = null;
  let stepIndex = 0;

  const defaultState = () => ({
    name: "",
    level: 1,
    conceptArchetype: "",
    conceptNotes: "",
    classId: "",
    subclassId: "",
    abilityMethod: "standard-array",
    abilities: { fit: null, ins: null, wil: null },
    lineageId: "",
    heritageId: "",
    backgroundId: "",
    equipmentMethod: "packages",
  });

  let state = loadState();
  let eventsBound = false;

  const el = {};

  function cacheElements() {
    el.loading = document.getElementById("cc-loading");
    el.app = document.getElementById("cc-app");
    el.error = document.getElementById("cc-error");
    el.progress = document.getElementById("cc-progress");
    el.kicker = document.getElementById("cc-step-kicker");
    el.title = document.getElementById("cc-step-title");
    el.desc = document.getElementById("cc-step-desc");
    el.rulesLink = document.getElementById("cc-rules-link");
    el.body = document.getElementById("cc-step-body");
    el.summary = document.getElementById("cc-summary-list");
    el.summaryFeatures = document.getElementById("cc-summary-features");
    el.detailPanel = document.getElementById("cc-detail-panel");
    el.detailPlaceholder = document.getElementById("cc-detail-placeholder");
    el.detailTitle = document.getElementById("cc-detail-title");
    el.detailBody = document.getElementById("cc-detail-body");
    el.detailLink = document.getElementById("cc-detail-link");
    el.btnBack = document.getElementById("cc-btn-back");
    el.btnNext = document.getElementById("cc-btn-next");
  }

  function showLoadError(message) {
    if (el.loading) el.loading.hidden = true;
    if (el.app) el.app.hidden = true;
    if (el.error) {
      el.error.hidden = false;
      const p = el.error.querySelector("p");
      if (p && message) p.textContent = message;
    }
  }

  function showApp() {
    if (el.loading) el.loading.hidden = true;
    if (el.error) el.error.hidden = true;
    if (el.app) el.app.hidden = false;
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = { ...defaultState(), ...JSON.parse(raw) };
        parsed.level = Number(parsed.level) || 1;
        return parsed;
      }
    } catch (_) { /* ignore */ }
    return defaultState();
  }

  function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    if (data) renderSummary();
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

  function byId(list, id) {
    return list.find((item) => item.id === id) || null;
  }

  function activeSteps() {
    return data.steps.filter((step) => {
      if (step.minLevel && state.level < step.minLevel) return false;
      if (!step.requires) return true;
      return step.requires.every((key) => {
        if (key === "class") return Boolean(state.classId);
        if (key === "lineage") return Boolean(state.lineageId);
        if (key === "background") return Boolean(state.backgroundId);
        return Boolean(state[key]);
      });
    });
  }

  function levelRange() {
    const range = data.levelRange || { min: 1, max: 10, subclassMin: 2 };
    return range;
  }

  function setLevel(nextLevel) {
    const range = levelRange();
    const level = Math.min(range.max, Math.max(range.min, nextLevel));
    state.level = level;
    if (level < range.subclassMin) {
      state.subclassId = "";
    }
    saveState();
    render();
  }

  function featuresAtLevel(items, level) {
    if (!items || !items.length) return [];
    return items.filter((item) => (item.minLevel || 1) <= level);
  }

  function renderFeatureList(items) {
    return `<ul class="cc-summary-feats">${items
      .map(
        (item) =>
          `<li><strong>${escapeHtml(item.name)}</strong>${item.summary ? ` — ${escapeHtml(item.summary)}` : ""}</li>`
      )
      .join("")}</ul>`;
  }

  function renderFeatureBlock(title, subtitle, items) {
    if (!items.length) return "";
    return `<div class="cc-summary-block">
      <h3 class="cc-summary-block-title">${escapeHtml(title)}${subtitle ? ` <span class="cc-summary-block-sub">${escapeHtml(subtitle)}</span>` : ""}</h3>
      ${renderFeatureList(items)}
    </div>`;
  }

  function currentStep() {
    const steps = activeSteps();
    return steps[Math.min(stepIndex, steps.length - 1)];
  }

  function findClass() {
    return byId(data.classes, state.classId);
  }

  function findSubclass() {
    const cls = findClass();
    if (!cls) return null;
    return byId(cls.subclasses, state.subclassId);
  }

  function recommendedHeritages() {
    const lineage = byId(data.lineages, state.lineageId);
    if (!lineage) return [];
    const rec = data.heritageRecommendations[lineage.name] || data.heritageRecommendations[lineage.id] || [];
    return rec;
  }

  function sortedHeritages() {
    const rec = new Set(recommendedHeritages());
    return [...data.heritages].sort((a, b) => {
      const ar = rec.has(a.name) ? 0 : 1;
      const br = rec.has(b.name) ? 0 : 1;
      if (ar !== br) return ar - br;
      return a.name.localeCompare(b.name);
    });
  }

  function sortedClasses() {
    const arch = data.conceptArchetypes.find((a) => a.id === state.conceptArchetype);
    if (!arch) return [...data.classes];
    const order = new Map(arch.suggestedClasses.map((id, i) => [id, i]));
    return [...data.classes].sort((a, b) => {
      const ao = order.has(a.id) ? order.get(a.id) : 999;
      const bo = order.has(b.id) ? order.get(b.id) : 999;
      if (ao !== bo) return ao - bo;
      return a.name.localeCompare(b.name);
    });
  }

  function abilityValuesValid() {
    const vals = ABILITIES.map((k) => state.abilities[k]);
    if (vals.some((v) => v === null || v === undefined || Number.isNaN(v))) return false;
    if (state.abilityMethod === "standard-array") {
      const sorted = [...vals].sort((a, b) => b - a);
      return sorted[0] === 2 && sorted[1] === 1 && sorted[2] === 0;
    }
    if (state.abilityMethod === "point-buy") {
      let spent = 0;
      for (const v of vals) {
        if (v < -1 || v > 2) return false;
        spent += v;
      }
      return spent === 3;
    }
    return true;
  }

  function computeMaxWd() {
    const cls = findClass();
    if (!cls || state.abilities.fit === null) return null;
    return cls.maxWd + state.abilities.fit;
  }

  function validateStep(step) {
    switch (step.type) {
      case "concept":
        return Boolean(state.conceptArchetype);
      case "class":
        return Boolean(state.classId);
      case "subclass":
        return Boolean(state.subclassId);
      case "abilities":
        return state.abilityMethod !== "gm-roll" && abilityValuesValid();
      case "lineage":
        return Boolean(state.lineageId);
      case "heritage":
        return Boolean(state.heritageId);
      case "background":
        return Boolean(state.backgroundId);
      case "equipment":
        return Boolean(state.equipmentMethod);
      case "review":
        return true;
      default:
        return true;
    }
  }

  function stepMessage(step) {
    if (validateStep(step)) return "";
    switch (step.type) {
      case "concept":
        return "Pick an archetype to continue.";
      case "class":
        return "Select a class.";
      case "subclass":
        return "Select a subclass.";
      case "abilities":
        return "Complete ability assignment for your chosen method.";
      case "lineage":
        return "Select a lineage.";
      case "heritage":
        return "Select a heritage.";
      case "background":
        return "Select a background.";
      default:
        return "Complete this step to continue.";
    }
  }

  /* ── Render helpers ── */

  function renderProgress() {
    const steps = activeSteps();
    el.progress.innerHTML = steps
      .map((step, i) => {
        const done = i < stepIndex;
        const current = i === stepIndex;
        const cls = ["cc-progress-item", done ? "is-done" : "", current ? "is-current" : ""]
          .filter(Boolean)
          .join(" ");
        return `<button type="button" class="${cls}" data-step="${i}" ${current ? 'aria-current="step"' : ""}>
          <span class="cc-progress-num">${i + 1}</span>
          <span class="cc-progress-label">${step.shortTitle}</span>
        </button>`;
      })
      .join("");

    el.progress.querySelectorAll("[data-step]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = Number(btn.dataset.step);
        if (target <= stepIndex || validateStep(currentStep())) {
          stepIndex = target;
          render();
        }
      });
    });
  }

  function renderSummary() {
    const cls = findClass();
    const sub = findSubclass();
    const lineage = byId(data.lineages, state.lineageId);
    const heritage = byId(data.heritages, state.heritageId);
    const bg = byId(data.backgrounds, state.backgroundId);
    const arch = data.conceptArchetypes.find((a) => a.id === state.conceptArchetype);
    const maxWd = computeMaxWd();
    const range = levelRange();
    const subclassMin = range.subclassMin || 2;

    const rows = [
      ["Name", state.name || "—"],
      ["Level", String(state.level)],
      ["Concept", arch ? arch.label : "—"],
      ["Class", cls ? cls.name : "—"],
      [
        "Subclass",
        state.level < subclassMin ? `— (level ${subclassMin}+)` : sub ? sub.name : "—",
      ],
      [
        "Abilities",
        ABILITIES.every((k) => state.abilities[k] !== null)
          ? ABILITIES.map((k) => `${ABILITY_LABELS[k].slice(0, 3)} ${fmtMod(state.abilities[k])}`).join(" · ")
          : "—",
      ],
      ["Max Wounds", maxWd !== null ? String(maxWd) : "—"],
      ["Lineage", lineage ? lineage.name : "—"],
      ["Heritage", heritage ? heritage.name : "—"],
      ["Background", bg ? bg.name : "—"],
      [
        "Equipment",
        data.equipmentMethods.find((m) => m.id === state.equipmentMethod)?.label || "—",
      ],
    ];

    el.summary.innerHTML = rows
      .map(
        ([label, value]) =>
          `<div class="cc-summary-row"><dt>${label}</dt><dd>${escapeHtml(String(value))}</dd></div>`
      )
      .join("");

    const blocks = [];
    if (cls) {
      const classFeats = featuresAtLevel(cls.abilities, state.level);
      if (classFeats.length) {
        blocks.push(renderFeatureBlock("Class features", cls.name, classFeats));
      }
    }
    if (state.level >= subclassMin && sub) {
      const subFeats = featuresAtLevel(sub.features, state.level);
      if (subFeats.length) {
        blocks.push(renderFeatureBlock("Subclass features", sub.name, subFeats));
      }
    }
    if (lineage?.features?.length) {
      blocks.push(renderFeatureBlock("Lineage traits", lineage.name, lineage.features));
    }
    if (heritage?.features?.length) {
      blocks.push(renderFeatureBlock("Heritage traits", heritage.name, heritage.features));
    }
    if (bg) {
      let bgHtml = "";
      if (bg.features?.length) {
        bgHtml += renderFeatureBlock("Background traits", bg.name, bg.features);
      }
      if (bg.talentChoices?.length) {
        bgHtml += `<div class="cc-summary-block">
          <h3 class="cc-summary-block-title">Background talent <span class="cc-summary-block-sub">${escapeHtml(bg.name)}</span></h3>
          <p class="cc-summary-talents">Choose one: ${bg.talentChoices.map((t) => `<em>${escapeHtml(t)}</em>`).join(", ")}</p>
        </div>`;
      }
      if (bgHtml) blocks.push(bgHtml);
    }

    if (el.summaryFeatures) {
      if (blocks.length) {
        el.summaryFeatures.hidden = false;
        el.summaryFeatures.innerHTML = blocks.join("");
      } else {
        el.summaryFeatures.hidden = true;
        el.summaryFeatures.innerHTML = "";
      }
    }
  }

  function fmtMod(n) {
    if (n === null || n === undefined) return "—";
    return n >= 0 ? `+${n}` : String(n);
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function cardGrid(items, options = {}) {
    const { badge } = options;
    return `<div class="cc-card-grid" role="listbox">${items
      .map((item) => {
        const selected = false;
        const badgeHtml = badge ? badge(item) : "";
        return `<button type="button" class="cc-card" role="option" aria-selected="false" data-id="${item.id}">
          ${badgeHtml}
          <span class="cc-card-title">${escapeHtml(item.name || item.label)}</span>
          <span class="cc-card-teaser">${escapeHtml(item.teaser || item.summary || item.hint || "")}</span>
          ${item.tag ? `<span class="cc-card-tag">${escapeHtml(item.tag)}</span>` : ""}
          ${item.maxWd ? `<span class="cc-card-meta">Max WD ${item.maxWd}</span>` : ""}
          ${item.keyAbilityLabel ? `<span class="cc-card-meta">${escapeHtml(item.keyAbilityLabel)}</span>` : ""}
        </button>`;
      })
      .join("")}</div>`;
  }

  function clearDetailPanel(message) {
    if (el.detailPlaceholder) {
      el.detailPlaceholder.hidden = false;
      el.detailPlaceholder.textContent =
        message || "Select or hover an option to see its full description.";
    }
    if (el.detailTitle) el.detailTitle.hidden = true;
    if (el.detailBody) el.detailBody.innerHTML = "";
    if (el.detailLink) el.detailLink.hidden = true;
  }

  function showDetailPanel(item, detailKey = "body") {
    if (!item) {
      clearDetailPanel();
      return;
    }
    if (el.detailPlaceholder) el.detailPlaceholder.hidden = true;
    if (el.detailTitle) {
      el.detailTitle.hidden = false;
      el.detailTitle.textContent = item.name || item.label || "";
    }
    if (el.detailBody) {
      el.detailBody.innerHTML = item[detailKey] || item.summary || item.hint || "";
    }
    if (el.detailLink) {
      if (item.rulesUrl) {
        el.detailLink.href = rp(item.rulesUrl);
        el.detailLink.hidden = false;
      } else {
        el.detailLink.hidden = true;
      }
    }
  }

  function bindCardGrid(container, items, selectedId, onSelect, detailKey = "body") {
    const cards = container.querySelectorAll(".cc-card");

    cards.forEach((card) => {
      const id = card.dataset.id;
      const selected = id === selectedId;
      card.classList.toggle("is-selected", selected);
      card.setAttribute("aria-selected", selected ? "true" : "false");

      card.addEventListener("click", () => {
        onSelect(id);
        cards.forEach((c) => {
          const sel = c.dataset.id === id;
          c.classList.toggle("is-selected", sel);
          c.setAttribute("aria-selected", sel ? "true" : "false");
        });
        showDetailPanel(byId(items, id), detailKey);
        saveState();
        updateNavButtons();
      });
      card.addEventListener("mouseenter", () => showDetailPanel(byId(items, card.dataset.id), detailKey));
      card.addEventListener("focus", () => showDetailPanel(byId(items, card.dataset.id), detailKey));
    });

    showDetailPanel(byId(items, selectedId), detailKey);
  }

  /* ── Step renderers ── */

  function renderConcept() {
    const range = levelRange();
    el.body.innerHTML = `
      <div class="form-group">
        <label for="cc-name">Character name <span class="cc-optional">(optional)</span></label>
        <input type="text" id="cc-name" class="cc-input" placeholder="Name your hero" value="${escapeHtml(state.name)}" maxlength="80" />
      </div>
      <fieldset class="cc-fieldset">
        <legend>Starting level</legend>
        <div class="cc-level-row">
          <button type="button" class="cc-stepper-btn" id="cc-level-down" aria-label="Lower level" ${state.level <= range.min ? "disabled" : ""}>−</button>
          <span class="cc-stepper-val" id="cc-level-val" aria-live="polite">${state.level}</span>
          <button type="button" class="cc-stepper-btn" id="cc-level-up" aria-label="Raise level" ${state.level >= range.max ? "disabled" : ""}>+</button>
        </div>
        <p class="cc-hint">Subclass choice unlocks at level ${range.subclassMin || 2}. Features in the summary update with level.</p>
      </fieldset>
      <fieldset class="cc-fieldset">
        <legend>Character archetype</legend>
        <div class="cc-chip-grid">
          ${data.conceptArchetypes
            .map(
              (a) =>
                `<button type="button" class="cc-chip${state.conceptArchetype === a.id ? " is-selected" : ""}" data-id="${a.id}">
                  <span class="cc-chip-label">${escapeHtml(a.label)}</span>
                  <span class="cc-chip-hint">${escapeHtml(a.hint)}</span>
                </button>`
            )
            .join("")}
        </div>
      </fieldset>
      <div class="form-group">
        <label for="cc-notes">Concept notes</label>
        <textarea id="cc-notes" class="cc-textarea" rows="3" placeholder="Motivation, personality, party role…">${escapeHtml(state.conceptNotes)}</textarea>
      </div>`;

    el.body.querySelector("#cc-name").addEventListener("input", (e) => {
      state.name = e.target.value;
      saveState();
    });
    el.body.querySelector("#cc-notes").addEventListener("input", (e) => {
      state.conceptNotes = e.target.value;
      saveState();
    });
    el.body.querySelector("#cc-level-down").addEventListener("click", () => setLevel(state.level - 1));
    el.body.querySelector("#cc-level-up").addEventListener("click", () => setLevel(state.level + 1));
    el.body.querySelectorAll(".cc-chip").forEach((chip) => {
      const arch = () => data.conceptArchetypes.find((a) => a.id === chip.dataset.id);
      chip.addEventListener("mouseenter", () => {
        const a = arch();
        if (a) showDetailPanel({ label: a.label, hint: a.hint, summary: a.hint }, "hint");
      });
      chip.addEventListener("focus", () => {
        const a = arch();
        if (a) showDetailPanel({ label: a.label, hint: a.hint, summary: a.hint }, "hint");
      });
      chip.addEventListener("click", () => {
        state.conceptArchetype = chip.dataset.id;
        el.body.querySelectorAll(".cc-chip").forEach((c) =>
          c.classList.toggle("is-selected", c.dataset.id === state.conceptArchetype)
        );
        showDetailPanel(arch(), "hint");
        saveState();
        updateNavButtons();
      });
    });

    if (state.conceptArchetype) {
      showDetailPanel(data.conceptArchetypes.find((a) => a.id === state.conceptArchetype), "hint");
    } else {
      clearDetailPanel("Pick an archetype to see how it guides your build.");
    }
  }

  function renderClass() {
    const items = sortedClasses();
    el.body.innerHTML = cardGrid(items);
    bindCardGrid(el.body, items, state.classId, (id) => {
      state.classId = id;
      state.subclassId = "";
    }, "summary");
  }

  function renderSubclass() {
    const cls = findClass();
    if (!cls) {
      el.body.innerHTML = `<p class="cc-hint">Choose a class first.</p>`;
      clearDetailPanel();
      return;
    }
    el.body.innerHTML = `<p class="cc-hint">Subclass for <strong>${escapeHtml(cls.name)}</strong> — taken at level ${levelRange().subclassMin || 2} in YMIAT.</p>` + cardGrid(cls.subclasses);
    bindCardGrid(el.body, cls.subclasses, state.subclassId, (id) => {
      state.subclassId = id;
    }, "summary");
  }

  function renderAbilities() {
    const cls = findClass();
    const keyHint = cls
      ? `Your ${cls.name} favors <strong>${escapeHtml(cls.keyAbilityLabel)}</strong>.`
      : "";

    el.body.innerHTML = `
      <div class="cc-method-row">
        ${data.abilityMethods
          .map(
            (m) =>
              `<label class="cc-method${m.disabled ? " is-disabled" : ""}">
                <input type="radio" name="ability-method" value="${m.id}" ${state.abilityMethod === m.id ? "checked" : ""} ${m.disabled ? "disabled" : ""} />
                <span class="cc-method-label">${escapeHtml(m.label)}</span>
                <span class="cc-method-desc">${escapeHtml(m.description)}</span>
              </label>`
          )
          .join("")}
      </div>
      <p class="cc-hint">${keyHint}</p>
      <div class="cc-ability-grid" id="cc-ability-grid"></div>
      <div class="cc-ability-preview" id="cc-ability-preview"></div>`;

    el.body.querySelectorAll('input[name="ability-method"]').forEach((input) => {
      input.addEventListener("change", () => {
        state.abilityMethod = input.value;
        state.abilities = { fit: null, ins: null, wil: null };
        renderAbilities();
        saveState();
        updateNavButtons();
      });
    });

    renderAbilityControls();
    clearDetailPanel("Ability scores are assigned here—see the preview below your choices.");
  }

  function renderAbilityControls() {
    const grid = el.body.querySelector("#cc-ability-grid");
    const preview = el.body.querySelector("#cc-ability-preview");
    if (!grid) return;

    if (state.abilityMethod === "standard-array") {
      const pool = [2, 1, 0];
      const used = ABILITIES.map((k) => state.abilities[k]).filter((v) => v !== null);
      grid.innerHTML = ABILITIES.map((key) => {
        const val = state.abilities[key];
        const options = ['<option value="">—</option>']
          .concat(
            pool.map((p) => {
              const taken = used.includes(p) && val !== p;
              return `<option value="${p}" ${val === p ? "selected" : ""} ${taken ? "disabled" : ""}>${fmtMod(p)}</option>`;
            })
          )
          .join("");
        return `<label class="cc-ability-cell">
          <span class="cc-ability-name">${ABILITY_LABELS[key]}</span>
          <select class="cc-select" data-ability="${key}">${options}</select>
        </label>`;
      }).join("");

      grid.querySelectorAll("select").forEach((sel) => {
        sel.addEventListener("change", () => {
          state.abilities[sel.dataset.ability] = sel.value === "" ? null : Number(sel.value);
          renderAbilityControls();
          saveState();
          updateNavButtons();
        });
      });
    } else if (state.abilityMethod === "point-buy") {
      grid.innerHTML = ABILITIES.map((key) => {
        const val = state.abilities[key] ?? 0;
        return `<label class="cc-ability-cell">
          <span class="cc-ability-name">${ABILITY_LABELS[key]}</span>
          <div class="cc-stepper">
            <button type="button" class="cc-stepper-btn" data-ability="${key}" data-delta="-1" aria-label="Decrease">−</button>
            <span class="cc-stepper-val">${fmtMod(val)}</span>
            <button type="button" class="cc-stepper-btn" data-ability="${key}" data-delta="1" aria-label="Increase">+</button>
          </div>
        </label>`;
      }).join("");

      grid.querySelectorAll(".cc-stepper-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const key = btn.dataset.ability;
          const delta = Number(btn.dataset.delta);
          const next = (state.abilities[key] ?? 0) + delta;
          if (next < -1 || next > 2) return;
          state.abilities[key] = next;
          renderAbilityControls();
          saveState();
          updateNavButtons();
        });
      });
    }

    const total = ABILITIES.reduce((s, k) => s + (state.abilities[k] ?? 0), 0);
    const maxWd = computeMaxWd();
    preview.innerHTML = `
      <p><strong>Point total:</strong> ${total}${state.abilityMethod === "point-buy" ? " / 3" : ""}
      ${abilityValuesValid() ? '<span class="cc-ok">Valid</span>' : '<span class="cc-warn">Incomplete</span>'}</p>
      ${maxWd !== null ? `<p><strong>Est. Max Wounds (level 1):</strong> ${maxWd} <span class="cc-muted">(class base + Fitness)</span></p>` : ""}`;
  }

  function renderLineage() {
    el.body.innerHTML = cardGrid(data.lineages, {
      badge: (item) => (item.tag ? `<span class="cc-card-badge">${escapeHtml(item.tag)}</span>` : ""),
    });
    bindCardGrid(el.body, data.lineages, state.lineageId, (id) => {
      state.lineageId = id;
    });
  }

  function renderHeritage() {
    const rec = new Set(recommendedHeritages());
    const items = sortedHeritages();
    const lineage = byId(data.lineages, state.lineageId);
    el.body.innerHTML =
      (lineage
        ? `<p class="cc-hint">Recommended for <strong>${escapeHtml(lineage.name)}</strong>: ${rec.size ? [...rec].join(", ") : "any heritage"}.</p>`
        : "") +
      cardGrid(items, {
        badge: (item) =>
          rec.has(item.name) ? '<span class="cc-card-badge cc-card-badge--rec">Recommended</span>' : "",
      });
    bindCardGrid(el.body, items, state.heritageId, (id) => {
      state.heritageId = id;
    });
  }

  function renderBackground() {
    el.body.innerHTML = cardGrid(data.backgrounds);
    bindCardGrid(el.body, data.backgrounds, state.backgroundId, (id) => {
      state.backgroundId = id;
    });
  }

  function renderEquipment() {
    const cls = findClass();
    const bg = byId(data.backgrounds, state.backgroundId);
    el.body.innerHTML = `
      <div class="cc-method-row">
        ${data.equipmentMethods
          .map(
            (m) =>
              `<label class="cc-method">
                <input type="radio" name="equipment-method" value="${m.id}" ${state.equipmentMethod === m.id ? "checked" : ""} />
                <span class="cc-method-label">${escapeHtml(m.label)}</span>
                <span class="cc-method-desc">${escapeHtml(m.description)}</span>
              </label>`
          )
          .join("")}
      </div>
      <div class="cc-equipment-summary">
        ${cls ? `<p><strong>Class:</strong> See starting equipment on <a href="${rp(cls.rulesUrl)}">${escapeHtml(cls.name)}</a>.</p>` : ""}
        ${bg ? `<p><strong>Background:</strong> ${escapeHtml(bg.name)} — see equipment in the panel on the right.</p>` : ""}
      </div>`;

    el.body.querySelectorAll('input[name="equipment-method"]').forEach((input) => {
      input.addEventListener("change", () => {
        state.equipmentMethod = input.value;
        saveState();
      });
    });

    if (bg) showDetailPanel(bg);
    else clearDetailPanel("Choose how you receive starting gear.");
  }

  function renderReview() {
    const maxWd = computeMaxWd();
    el.body.innerHTML = `
      <div class="cc-review-card">
        <h3>Character summary</h3>
        <dl class="cc-review-list">${el.summary.innerHTML}</dl>
        ${el.summaryFeatures && !el.summaryFeatures.hidden ? `<div class="cc-review-features">${el.summaryFeatures.innerHTML}</div>` : ""}
        ${maxWd !== null ? `<p class="cc-review-wd">Level ${state.level} Max Wounds: <strong>${maxWd}</strong></p>` : ""}
        ${state.conceptNotes ? `<p><strong>Notes:</strong> ${escapeHtml(state.conceptNotes)}</p>` : ""}
      </div>
      <div class="cc-review-actions">
        <button type="button" class="btn" id="cc-copy-summary">Copy summary</button>
        <button type="button" class="btn cc-btn-secondary" id="cc-reset">Start over</button>
      </div>
      <textarea class="cc-export" id="cc-export" readonly rows="8"></textarea>`;

    const exportText = buildExportText();
    el.body.querySelector("#cc-export").value = exportText;

    el.body.querySelector("#cc-copy-summary").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(exportText);
        el.body.querySelector("#cc-copy-summary").textContent = "Copied!";
        setTimeout(() => {
          el.body.querySelector("#cc-copy-summary").textContent = "Copy summary";
        }, 2000);
      } catch (_) {
        el.body.querySelector("#cc-export").select();
      }
    });

    el.body.querySelector("#cc-reset").addEventListener("click", () => {
      if (window.confirm("Clear this character draft and start over?")) {
        state = defaultState();
        stepIndex = 0;
        saveState();
        render();
      }
    });
  }

  function buildExportText() {
    const cls = findClass();
    const sub = findSubclass();
    const lineage = byId(data.lineages, state.lineageId);
    const heritage = byId(data.heritages, state.heritageId);
    const bg = byId(data.backgrounds, state.backgroundId);
    const arch = data.conceptArchetypes.find((a) => a.id === state.conceptArchetype);
    const range = levelRange();
    const lines = [
      `YMIAT Character (level ${state.level} draft)`,
      "==============================",
      state.name ? `Name: ${state.name}` : null,
      `Level: ${state.level}`,
      arch ? `Concept: ${arch.label}` : null,
      state.conceptNotes ? `Notes: ${state.conceptNotes}` : null,
      cls ? `Class: ${cls.name}` : null,
      state.level >= (range.subclassMin || 2) && sub ? `Subclass: ${sub.name}` : null,
      `Fitness ${fmtMod(state.abilities.fit)} · Insight ${fmtMod(state.abilities.ins)} · Willpower ${fmtMod(state.abilities.wil)}`,
      computeMaxWd() !== null ? `Max Wounds: ${computeMaxWd()}` : null,
      lineage ? `Lineage: ${lineage.name}` : null,
      heritage ? `Heritage: ${heritage.name}` : null,
      bg ? `Background: ${bg.name}` : null,
      bg?.talentChoices?.length ? `Background talent (choose one): ${bg.talentChoices.join(", ")}` : null,
      `Equipment: ${data.equipmentMethods.find((m) => m.id === state.equipmentMethod)?.label || ""}`,
    ].filter(Boolean);

    if (cls) {
      const classFeats = featuresAtLevel(cls.abilities, state.level);
      if (classFeats.length) {
        lines.push("", "Class features:");
        classFeats.forEach((feat) => lines.push(`- ${feat.name}: ${feat.summary}`));
      }
    }
    if (state.level >= (range.subclassMin || 2) && sub) {
      const subFeats = featuresAtLevel(sub.features, state.level);
      if (subFeats.length) {
        lines.push("", "Subclass features:");
        subFeats.forEach((feat) => lines.push(`- ${feat.name}: ${feat.summary}`));
      }
    }
    if (lineage?.features?.length) {
      lines.push("", "Lineage traits:");
      lineage.features.forEach((feat) => lines.push(`- ${feat.name}: ${feat.summary}`));
    }
    if (heritage?.features?.length) {
      lines.push("", "Heritage traits:");
      heritage.features.forEach((feat) => lines.push(`- ${feat.name}: ${feat.summary}`));
    }
    if (bg?.features?.length) {
      lines.push("", "Background traits:");
      bg.features.forEach((feat) => lines.push(`- ${feat.name}: ${feat.summary}`));
    }

    return lines.join("\n");
  }

  function renderStepBody(step) {
    switch (step.type) {
      case "concept":
        renderConcept();
        break;
      case "class":
        renderClass();
        break;
      case "subclass":
        renderSubclass();
        break;
      case "abilities":
        renderAbilities();
        break;
      case "lineage":
        renderLineage();
        break;
      case "heritage":
        renderHeritage();
        break;
      case "background":
        renderBackground();
        break;
      case "equipment":
        renderEquipment();
        break;
      case "review":
        clearDetailPanel("Review your complete character below.");
        renderReview();
        break;
      default:
        el.body.innerHTML = `<p>Unknown step type.</p>`;
    }
  }

  function updateNavButtons() {
    const steps = activeSteps();
    const step = currentStep();
    const valid = validateStep(step);
    el.btnBack.disabled = stepIndex === 0;
    el.btnNext.textContent = stepIndex >= steps.length - 1 ? "Finish" : "Next";
    el.btnNext.disabled = !valid && step.type !== "review";
    el.btnNext.setAttribute("aria-describedby", valid ? "" : "cc-step-error");
  }

  function render() {
    if (!data || !el.kicker || !el.title) return;
    const steps = activeSteps();
    if (stepIndex >= steps.length) stepIndex = steps.length - 1;

    const step = currentStep();
    const stepNum = steps.indexOf(step) + 1;

    el.kicker.textContent = `Step ${stepNum} of ${steps.length}`;
    el.title.textContent = step.title;
    el.desc.textContent = step.description;
    el.rulesLink.href = rp(`rules/characters.html#${step.overviewAnchor || "character-creation-overview"}`);

    renderProgress();
    renderStepBody(step);
    renderSummary();
    updateNavButtons();

    let err = document.getElementById("cc-step-error");
    const msg = stepMessage(step);
    if (msg && !validateStep(step)) {
      if (!err) {
        err = document.createElement("p");
        err.id = "cc-step-error";
        err.className = "cc-step-error";
        el.body.insertAdjacentElement("afterend", err);
      }
      err.textContent = msg;
    } else if (err) {
      err.remove();
    }
  }

  function goNext() {
    const steps = activeSteps();
    const step = currentStep();
    if (!validateStep(step)) return;
    if (stepIndex < steps.length - 1) {
      stepIndex += 1;
      render();
      el.title.focus({ preventScroll: false });
    }
  }

  function goBack() {
    if (stepIndex > 0) {
      stepIndex -= 1;
      render();
    }
  }

  function bindEvents() {
    if (eventsBound || !el.btnNext || !el.btnBack) return;
    eventsBound = true;
    el.btnNext.addEventListener("click", goNext);
    el.btnBack.addEventListener("click", goBack);
  }

  function updateNavOffset(){
    const header = document.querySelector("header");
    if(!header) return;
    const height = Math.ceil(header.getBoundingClientRect().height);
    document.body.style.setProperty("--cc-nav-offset", height + "px");
  }

  function scheduleNavOffsetUpdate(){
    updateNavOffset();
    requestAnimationFrame(() => {
      updateNavOffset();
      requestAnimationFrame(updateNavOffset);
    });
  }

  async function init() {
    cacheElements();
    if (!el.loading || !el.app || !el.progress) {
      showLoadError("Character creator UI failed to load. Try refreshing the page.");
      return;
    }

    scheduleNavOffsetUpdate();
    window.addEventListener("resize", scheduleNavOffsetUpdate);
    if (window.ResizeObserver) {
      const header = document.querySelector("header");
      if (header) {
        new ResizeObserver(scheduleNavOffsetUpdate).observe(header);
      }
    }
    try {
      const res = await fetch(rp("assets/character-creator-data.json"));
      if (!res.ok) throw new Error("Could not load character options (HTTP " + res.status + ").");
      data = await res.json();
      if (!data || !Array.isArray(data.steps) || !Array.isArray(data.classes)) {
        throw new Error("Character options file is invalid. Regenerate it with generate-character-creator-data.py.");
      }
      const range = data.levelRange || { min: 1, max: 10, subclassMin: 2 };
      state.level = Math.min(range.max, Math.max(range.min, Number(state.level) || 1));
      if (state.level < range.subclassMin) state.subclassId = "";
      showApp();
      bindEvents();
      scheduleNavOffsetUpdate();
      try {
        render();
      } catch (renderErr) {
        console.error(renderErr);
        throw new Error("Character creator failed to render. Try clearing saved data or refreshing.");
      }
      scheduleNavOffsetUpdate();
    } catch (err) {
      console.error(err);
      const hint = window.location.protocol === "file:"
        ? " Open this site through a local web server (for example: python -m http.server) instead of the file:// URL."
        : "";
      showLoadError((err && err.message ? err.message : "Could not load character data.") + hint);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
