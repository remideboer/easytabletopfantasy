/**
 * Generate landscape A4 B&W PDFs for pregenerated character sheets.
 * Usage: node scripts/generate-pregen-pdfs.mjs
 * Requires: npm i -D playwright  (one-time) and npx playwright install chromium
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const outDir = path.join(root, 'assets', 'pdfs', 'pregenerated-characters');
const IDS = ['mara-marshward', 'alden-crowe', 'rik-tanner', 'elias-voss', 'dane-ironhart'];

function contentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return ({
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.woff2': 'font/woff2',
  })[ext] || 'application/octet-stream';
}

function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      try {
        let urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
        if (urlPath.endsWith('/')) urlPath += 'index.html';
        const filePath = path.normalize(path.join(root, urlPath.replace(/^\//, '')));
        if (!filePath.startsWith(root)) {
          res.writeHead(403);
          res.end('Forbidden');
          return;
        }
        if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
          res.writeHead(404);
          res.end('Not found');
          return;
        }
        res.writeHead(200, { 'Content-Type': contentType(filePath) });
        fs.createReadStream(filePath).pipe(res);
      } catch (err) {
        res.writeHead(500);
        res.end(String(err));
      }
    });
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, port });
    });
  });
}

async function main() {
  let playwright;
  try {
    playwright = await import('playwright');
  } catch (err) {
    console.error('Install Playwright first:\n  npm i -D playwright\n  npx playwright install chromium');
    process.exit(1);
  }

  fs.mkdirSync(outDir, { recursive: true });
  const { server, port } = await startServer();
  const base = `http://127.0.0.1:${port}`;
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage();

  for (const id of IDS) {
    const url = `${base}/rules/pregenerated-characters/${id}.html`;
    console.log('Rendering', id);
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForSelector('.pg-sheet');
    // Isolate the sheet so global print chrome/hide rules cannot clip the topline.
    await page.evaluate(() => {
      const sheet = document.querySelector('.pg-sheet');
      if (!sheet) return;
      document.body.replaceChildren(sheet);
      document.body.style.margin = '0';
      document.body.style.padding = '0';
      document.body.style.background = '#fff';
      document.documentElement.style.background = '#fff';
    });
    await page.addStyleTag({
      content: `
        @page { size: A4 landscape; margin: 8mm; }
        .pg-sheet { box-shadow: none !important; margin: 0 !important; }
        .pg-head {
          display: grid !important;
          grid-template-columns: minmax(11rem, 1.05fr) minmax(0, 1.7fr) !important;
          align-items: center !important;
        }
        .pg-head-facts {
          display: flex !important;
          flex-direction: column !important;
          gap: 5px !important;
        }
        .pg-name, .pg-meta, .pg-tags-row, .pg-head-id { display: block !important; visibility: visible !important; }
      `,
    });
    const headText = await page.locator('.pg-head').innerText();
    if (!/Lineage/i.test(headText) || !/\n/.test(headText.replace(/\r/g, ''))) {
      // soft check: facts should span multiple lines via two .pg-tags-row
      const rows = await page.locator('.pg-tags-row').count();
      if (rows < 2) throw new Error('expected 2 tag rows for ' + id);
    }
    const outPath = path.join(outDir, `${id}.pdf`);
    await page.pdf({
      path: outPath,
      format: 'A4',
      landscape: true,
      printBackground: true,
      margin: { top: '8mm', right: '8mm', bottom: '8mm', left: '8mm' },
      preferCSSPageSize: true,
    });
    console.log('Wrote', outPath, '| head ok');
  }

  await browser.close();
  server.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
