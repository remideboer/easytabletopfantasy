# Adapter: static-mirror

English HTML lives at the site root. Dutch is a full mirror under `nl/` with the same relative tree.

## Rules

- Shared CSS/JS/images stay in `/assets` (never copy into `nl/assets`).
- Each NL page uses one extra `../` for asset and `includes.js` paths versus its English twin.
- `includes.js` detects locale from the URL (`/nl/…`), sets `{{ROOT}}` to the locale content root and `{{ASSETS}}` to the site root.
- Language toggle navigates to the sibling path (add or strip `/nl`).

## Scaffold / refresh paths

From the repo root:

```bash
python i18n/adapters/static-mirror/mirror_paths.py
```

This copies live English HTML into `nl/` (skipping `foundation/`), sets `lang="nl"`, and rewrites asset/`includes.js` paths. Body translation is done separately per batch.

## Sibling URL examples

| EN | NL |
|----|-----|
| `/index.html` | `/nl/index.html` |
| `/rules/core.html` | `/nl/rules/core.html` |
| `/rules/adventures/wild-sheep-chase.html` | `/nl/rules/adventures/wild-sheep-chase.html` |

Production `BASE_PATH` (e.g. `/easytabletopfantasy`) prefixes both; locale segment is `/nl` after that base.
