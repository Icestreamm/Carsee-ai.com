const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = process.cwd();
const BASE_URL = "http://127.0.0.1:4173";
const VIEWPORTS = [
  { name: "320x720", width: 320, height: 720 },
  { name: "375x812", width: 375, height: 812 },
  { name: "390x844", width: 390, height: 844 },
  { name: "414x896", width: 414, height: 896 },
];

function walkHtmlFiles(dir, acc = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    const rel = path.relative(ROOT, full).replace(/\\/g, "/");
    if (entry.isDirectory()) {
      if (
        ["node_modules", ".git", "assets", "playwright-report", "test-results", ".claude"].includes(entry.name)
      ) {
        continue;
      }
      walkHtmlFiles(full, acc);
      continue;
    }
    if (!entry.name.endsWith(".html")) continue;
    if (rel.startsWith("includes/") || rel.startsWith("ar/includes/")) continue;
    if (rel.startsWith("_tmp_")) continue;
    acc.push(rel);
  }
  return acc;
}

async function run() {
  const htmlFiles = walkHtmlFiles(ROOT).sort();
  const browser = await chromium.launch({ headless: true });
  const report = {
    scannedAt: new Date().toISOString(),
    pageCount: htmlFiles.length,
    totals: {
      pagesWithMissingViewportMeta: 0,
      pagesWithConsoleErrors: 0,
      pagesWithBrokenImages: 0,
      pagesWithFormLabelIssues: 0,
      pagesWithTargetBlankNoNoopener: 0,
      pagesWithHorizontalOverflow: 0,
      pagesWithSmallTapTargets: 0,
    },
    pages: [],
  };

  for (const file of htmlFiles) {
    const pageFindings = {
      file,
      hasViewportMeta: true,
      consoleErrors: [],
      brokenImages: [],
      formLabelIssues: [],
      targetBlankNoNoopener: [],
      overflowByViewport: {},
      smallTapTargetsByViewport: {},
    };

    const context = await browser.newContext({
      viewport: { width: VIEWPORTS[1].width, height: VIEWPORTS[1].height },
      locale: file.startsWith("ar/") ? "ar" : "en-US",
    });
    const page = await context.newPage();

    page.on("console", (msg) => {
      if (msg.type() === "error") {
        pageFindings.consoleErrors.push(msg.text());
      }
    });

    const url = `${BASE_URL}/${file}`;
    try {
      await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
    } catch (e) {
      pageFindings.consoleErrors.push(`Navigation failed: ${String(e.message || e)}`);
      await context.close();
      report.pages.push(pageFindings);
      continue;
    }

    let metaCheck = true;
    try {
      metaCheck = await page.evaluate(() => {
        const m = document.querySelector('meta[name="viewport"]');
        if (!m) return false;
        const content = (m.getAttribute("content") || "").toLowerCase();
        return content.includes("width=device-width");
      });
    } catch (_) {}
    pageFindings.hasViewportMeta = metaCheck;

    try { pageFindings.brokenImages = await page.evaluate(() =>
      Array.from(document.images)
        .filter((img) => img.src && img.complete && img.naturalWidth === 0)
        .map((img) => img.getAttribute("src") || img.src)
    ); } catch (_) {}

    try { pageFindings.formLabelIssues = await page.evaluate(() => {
      const controls = Array.from(
        document.querySelectorAll("input, textarea, select")
      ).filter((el) => {
        const type = (el.getAttribute("type") || "").toLowerCase();
        if (["hidden", "submit", "button", "reset", "image"].includes(type)) return false;
        if (el.hasAttribute("aria-hidden")) return false;
        return true;
      });
      return controls
        .filter((el) => {
          if (el.getAttribute("aria-label") || el.getAttribute("aria-labelledby")) return false;
          if (el.closest("label")) return false;
          const id = el.id;
          if (!id) return true;
          return !document.querySelector(`label[for="${CSS.escape(id)}"]`);
        })
        .map((el) => el.outerHTML.slice(0, 160));
    }); } catch (_) {}

    try { pageFindings.targetBlankNoNoopener = await page.evaluate(() =>
      Array.from(document.querySelectorAll('a[target="_blank"]'))
        .filter((a) => {
          const rel = (a.getAttribute("rel") || "").toLowerCase();
          return !rel.includes("noopener");
        })
        .map((a) => a.getAttribute("href") || "")
    ); } catch (_) {}

    for (const vp of VIEWPORTS) {
      try {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.waitForTimeout(100);

        const overflow = await page.evaluate(() => {
          const doc = document.documentElement;
          return Math.max(0, doc.scrollWidth - window.innerWidth);
        });
        pageFindings.overflowByViewport[vp.name] = overflow;

        const smallTapTargets = await page.evaluate(() => {
          const nodes = Array.from(
            document.querySelectorAll("a, button, [role='button'], input, select, textarea, summary")
          ).filter((el) => {
            const style = window.getComputedStyle(el);
            if (style.display === "none" || style.visibility === "hidden") return false;
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0;
          });

          let count = 0;
          for (const el of nodes) {
            const r = el.getBoundingClientRect();
            if (r.width < 44 || r.height < 44) count += 1;
          }
          return count;
        });
        pageFindings.smallTapTargetsByViewport[vp.name] = smallTapTargets;
      } catch (_) {}
    }

    await context.close();

    if (!pageFindings.hasViewportMeta) report.totals.pagesWithMissingViewportMeta += 1;
    if (pageFindings.consoleErrors.length) report.totals.pagesWithConsoleErrors += 1;
    if (pageFindings.brokenImages.length) report.totals.pagesWithBrokenImages += 1;
    if (pageFindings.formLabelIssues.length) report.totals.pagesWithFormLabelIssues += 1;
    if (pageFindings.targetBlankNoNoopener.length) report.totals.pagesWithTargetBlankNoNoopener += 1;
    if (Object.values(pageFindings.overflowByViewport).some((v) => v > 0)) {
      report.totals.pagesWithHorizontalOverflow += 1;
    }
    if (Object.values(pageFindings.smallTapTargetsByViewport).some((v) => v > 0)) {
      report.totals.pagesWithSmallTapTargets += 1;
    }
    report.pages.push(pageFindings);
  }

  await browser.close();
  const outPath = path.join(ROOT, "tools", "mobile-audit-report.json");
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2), "utf8");

  console.log(`Scanned ${report.pageCount} pages.`);
  console.log(JSON.stringify(report.totals, null, 2));
  console.log(`Detailed report: ${outPath}`);
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
