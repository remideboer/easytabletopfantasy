/**
 * Home-page D&D Beyond import: validate public URL/ID, then open the character
 * sheet with ?ddb= so the sheet runs the existing proxy import + review flow.
 */
(function () {
  function extractDdbId(input) {
    if (!input) return null;
    const m = String(input).match(/\/characters\/(\d+)/);
    if (m) return m[1];
    const bare = String(input).trim();
    return /^\d+$/.test(bare) ? bare : null;
  }

  function init() {
    const form = document.getElementById("home-ddb-form");
    const input = document.getElementById("home-ddb-input");
    const status = document.getElementById("home-ddb-status");
    const submit = document.getElementById("home-ddb-submit");
    if (!form || !input) return;

    const langNl = document.documentElement.lang === "nl";
    const msgEmpty = langNl
      ? "Plak eerst een openbare D&D Beyond-personagelink of numeriek ID."
      : "Paste a public D&D Beyond character link or numeric ID first.";
    const msgInvalid = langNl
      ? "Geen geldige D&D Beyond-personage-URL of ID gevonden."
      : "Couldn't find a valid D&D Beyond character URL or ID.";
    const msgGo = langNl ? "Personagebeheer openen…" : "Opening character manager…";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const value = String(input.value || "").trim();
      if (!value) {
        if (status) status.textContent = msgEmpty;
        input.focus();
        return;
      }
      if (!extractDdbId(value)) {
        if (status) status.textContent = msgInvalid;
        input.focus();
        return;
      }
      if (status) status.textContent = msgGo;
      if (submit) submit.disabled = true;
      const sheetHref = form.getAttribute("data-sheet-href") || "character-sheet.html";
      const url = sheetHref + (sheetHref.indexOf("?") >= 0 ? "&" : "?") + "ddb=" + encodeURIComponent(value);
      window.location.href = url;
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
