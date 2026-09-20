/**
 * Optional D&D Beyond character fetch proxy (Cloudflare Worker).
 * Leave empty to keep paste-JSON as the reliable path.
 *
 * Deploy: cd workers/ddb-character-proxy && npx wrangler deploy
 * Then set the workers.dev (or custom) URL below, e.g.:
 *   window.YMIAT_DDB_PROXY_URL = "https://ymiat-ddb-proxy.YOUR_SUBDOMAIN.workers.dev";
 */
window.YMIAT_DDB_PROXY_URL = window.YMIAT_DDB_PROXY_URL || "";
