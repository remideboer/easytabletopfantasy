/**
 * D&D Beyond character fetch proxy (Cloudflare Worker).
 * Default: set the workers.dev URL so Import fetches in one click.
 * Leave empty for paste-only fallback.
 *
 * Deploy: cd workers/ddb-character-proxy && npx wrangler deploy
 */
window.YMIAT_DDB_PROXY_URL = "https://ymiat-ddb-character-proxy.gitaarremi.workers.dev";
