# i18n

Shared locale catalogs and adapters for You-Meet-In-A-Tavern (YMIAT).

## Layout

```
i18n/
  glossary/          # Term choices (natural Dutch, not calques)
  locales/
    en/              # English catalogs
    nl/              # Dutch catalogs
  adapters/
    static-mirror/   # Current: mirrored HTML under /nl/
```

## Adding a locale

1. Copy `locales/en/` to `locales/<code>/`.
2. Translate `chrome.json` (nav/footer/toggle) and `apps.json` (creator/sheet UI).
3. Follow `glossary/` for consistent game terms.
4. Wire the locale in the active adapter (see `adapters/`).

## Catalogs

| File | Used by |
|------|---------|
| `locales/*/chrome.json` | Site chrome (nav, footer, language toggle) via `assets/includes.js` |
| `locales/*/apps.json` | Character creator / sheets via app JS |

Catalogs are implementation-agnostic. Adapters decide how strings reach the page (HTML mirror, runtime keys, etc.).

## Current adapter

**static-mirror** — English pages at site root; Dutch mirrors under `nl/`. Shared assets stay in `/assets`. See `adapters/static-mirror/README.md`.
