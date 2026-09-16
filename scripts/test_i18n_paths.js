// Quick sanity checks for locale path helpers (node --run)
const fs = require("fs");
const vm = require("vm");
const code = fs.readFileSync("d:/projecten/dndlite/assets/includes.js", "utf8");

function withLocation(pathname, hostname, protocol) {
  const sandbox = {
    window: {
      location: { pathname, hostname, protocol, hash: "", search: "" },
      matchMedia: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }),
      YMIAT_I18N_CHROME: { en: { nav: {}, toggle: {}, footer: {} }, nl: { nav: {}, toggle: {}, footer: {} } },
    },
    document: {
      readyState: "complete",
      querySelector: () => null,
      querySelectorAll: () => [],
      addEventListener() {},
    },
    localStorage: { setItem() {}, getItem() { return null; } },
    console,
  };
  sandbox.window.document = sandbox.document;
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);
  return sandbox.window;
}

const cases = [
  ["file:", "", "/d:/projecten/dndlite/index.html", "en", "", ""],
  ["file:", "", "/d:/projecten/dndlite/rules/core.html", "en", "../", "../"],
  ["file:", "", "/d:/projecten/dndlite/nl/index.html", "nl", "", "../"],
  ["file:", "", "/d:/projecten/dndlite/nl/rules/core.html", "nl", "../", "../../"],
  ["file:", "", "/d:/projecten/dndlite/nl/rules/adventures/index.html", "nl", "../../", "../../../"],
  ["http:", "example.com", "/easytabletopfantasy/nl/rules/core.html", "nl", "/easytabletopfantasy/nl/", "/easytabletopfantasy/"],
];

for (const [protocol, host, path, wantLoc, wantRoot, wantAssets] of cases) {
  const w = withLocation(path, host, protocol);
  const loc = w.ymiatDetectLocale();
  const root = w.ymiatGetRootPath();
  const assets = w.ymiatGetAssetsPath();
  const ok = loc === wantLoc && root === wantRoot && assets === wantAssets;
  console.log(ok ? "OK" : "FAIL", { path, loc, root, assets, wantLoc, wantRoot, wantAssets });
}
