/**
 * YMIAT D&D Beyond character proxy
 * Server-side fetch of public character JSON (same idea as dprcalc.com /api/c).
 *
 * Deploy: npx wrangler deploy
 * Then set window.YMIAT_DDB_PROXY_URL in assets/ddb-proxy-config.js
 */
export default {
  async fetch(request) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Accept, Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    if (request.method !== "GET") {
      return json({ error: "method_not_allowed" }, 405, cors);
    }

    const url = new URL(request.url);
    const img = (url.searchParams.get("img") || "").trim();
    if (img) {
      return proxyDdbImage(img, cors);
    }

    const id = (url.searchParams.get("id") || url.searchParams.get("cid") || "").trim();
    if (!/^\d+$/.test(id)) {
      return json({ error: "missing_id", message: "Pass ?id= or ?cid= with a numeric D&D Beyond character id." }, 400, cors);
    }

    const ddbUrl = `https://character-service.dndbeyond.com/character/v5/character/${id}`;
    let upstream;
    try {
      upstream = await fetch(ddbUrl, {
        headers: { Accept: "application/json" },
      });
    } catch (err) {
      return json({ error: "upstream_fetch_failed", message: String(err && err.message ? err.message : err) }, 502, cors);
    }

    const text = await upstream.text();
    let body;
    try {
      body = text ? JSON.parse(text) : null;
    } catch (_) {
      body = { error: "invalid_upstream_json", raw: text.slice(0, 200) };
    }

    if (upstream.status === 404) {
      return json({ error: "not_found", message: "Character not found.", data: body }, 404, cors);
    }
    if (upstream.status === 403) {
      return json({ error: "private", message: "Character is private or not accessible.", signedIn: false }, 403, cors);
    }
    if (!upstream.ok) {
      return json({ error: "upstream_error", status: upstream.status, data: body }, upstream.status, cors);
    }

    return new Response(JSON.stringify(body), {
      status: 200,
      headers: {
        ...cors,
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "public, max-age=60",
      },
    });
  },
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      ...cors,
      "Content-Type": "application/json; charset=utf-8",
    },
  });
}

async function proxyDdbImage(raw, cors) {
  let target;
  try {
    target = new URL(raw);
  } catch (_) {
    return json({ error: "bad_img" }, 400, cors);
  }
  const host = target.hostname.toLowerCase();
  const allowed = target.protocol === "https:" && (host === "dndbeyond.com" || host.endsWith(".dndbeyond.com"));
  if (!allowed) {
    return json({ error: "forbidden_host" }, 403, cors);
  }
  let upstream;
  try {
    upstream = await fetch(target.toString(), { headers: { Accept: "image/*" } });
  } catch (err) {
    return json({ error: "image_fetch_failed", message: String(err && err.message ? err.message : err) }, 502, cors);
  }
  if (!upstream.ok) {
    return json({ error: "image_fetch_failed", status: upstream.status }, 502, cors);
  }
  const type = (upstream.headers.get("content-type") || "").split(";")[0].trim().toLowerCase();
  if (!type.startsWith("image/")) {
    return json({ error: "not_an_image" }, 502, cors);
  }
  const buf = await upstream.arrayBuffer();
  if (buf.byteLength > 2 * 1024 * 1024) {
    return json({ error: "too_large" }, 413, cors);
  }
  return new Response(buf, {
    status: 200,
    headers: {
      ...cors,
      "Content-Type": type,
      "Cache-Control": "public, max-age=86400",
    },
  });
}
