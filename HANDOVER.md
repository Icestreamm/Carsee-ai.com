# Handover: Restore Progress After Font/Hero Updates

**Purpose:** This document lets another AI agent restore or redo all progress that was made before font size and hero style changes. After those updates, the following were lost or broken and need to be restored.

**Date:** March 2025  
**Scope:** English site (`index.html` + root), Arabic site (`ar/`), `css/style.css`, `js/main.js`, 404 and legal pages.

---

## 1. What Was Lost (Restoration Targets)

- **Arabic link from English version** — The English homepage nav must offer a way to switch to Arabic. The language selector should include **AR** linking to `ar/index.html`.
- **Favicon and fonts in English head** — `index.html` should include favicon and Google Fonts (e.g. Oswald, DM Sans / Inter) in `<head>` so hero and typography match design.
- **Floating CTA** — Sticky “Book a demo” / “احجز عرضاً” button that appears after scroll, hidden near footer. Present in both `index.html` and `ar/index.html`, with `id="floatingCta"` and `#demo` target.
- **Footer legal links** — In both EN and AR footers: Privacy Policy, Terms of Service, Legal (mailto), using `.legal-links` and correct hrefs (`privacy.html`, `terms.html`, `mailto:legal@carsee.app` or equivalent).
- **Section id for demo** — The final CTA section should have `id="demo"` so the floating CTA anchor works (`href="#demo"`).
- **Brand consistency** — If the project is **CarSee**, ensure English pages use CarSee (title, logo, company paths like `company/carsee/index.html`, footer “CarSee”). If it was rebranded to **Tchek**, keep Tchek but still restore the AR link, floating CTA, legal links, and hero/font setup.

---

## 2. Arabic Site (ar/) — Current Intended State

### 2.1 Page list (all under `ar/`)

| Path | Purpose |
|------|--------|
| `ar/index.html` | Arabic homepage |
| `ar/blog/index.html` | Blog |
| `ar/contact/index.html` | Contact |
| `ar/demo/index.html` | Demo |
| `ar/technology/index.html` | Technology / AI features |
| `ar/company/carsee/index.html` | Company (or company/tchek if rebranded) |
| `ar/company/career/index.html` | Career |
| `ar/company/partners/index.html` | Partners |
| `ar/company/press/index.html` | Press |
| `ar/clients/dealerships/index.html` | Dealerships |
| `ar/clients/uv-marketplaces/index.html` | UV marketplaces |
| `ar/clients/oem/index.html` | OEM |
| `ar/clients/rental-cars-car-sharing/index.html` | Rental & car sharing |
| `ar/clients/insurers-experts/index.html` | Insurers & experts |
| `ar/clients/software-publishers/index.html` | Software publishers |
| `ar/clients/leasing/index.html` | Leasing |
| `ar/solution/remote-trade-in/index.html` | Remote trade-in |
| `ar/solution/on-site-trade-in/index.html` | On-site trade-in |
| `ar/solution/car-fleet/index.html` | Car fleet |
| `ar/solution/inspection/index.html` | Inspection |
| `ar/solution/remarketing/index.html` | Remarketing |
| `ar/404.html` | Arabic 404 |
| `ar/privacy.html` | Arabic privacy policy |
| `ar/terms.html` | Arabic terms of service |

### 2.2 Arabic rules (every ar/*.html page)

- **HTML:** `<html lang="ar" dir="rtl">`.
- **Font:** Cairo only. In `<head>`:
  - Preconnect to Google Fonts.
  - Link: `https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap`.
- **No letter-spacing** on Arabic text (use `letter-spacing: 0` in RTL styles).
- **Paths:**
  - From `ar/index.html`: `../css/`, `../assets/`, `../js/`, and links like `technology/index.html`, `contact/index.html` (no `../` for other ar/ pages).
  - From `ar/company/*` or `ar/clients/*` or `ar/solution/*`: `../../../css/`, `../../../assets/`, `../../index.html` for Arabic home, `../../../` for assets; internal nav stays under `ar/` (e.g. `../../technology/index.html`).
- **Language switcher:** “EN” must link to the **English** homepage: `../index.html` (so from `ar/index.html` going to EN goes to site root).
- **RTL style block:** Each Arabic page includes a `<style>` block that forces Cairo on `[dir="rtl"]`, sets type scale (h1–h4, p, nav, footer, cards, section titles), and RTL layout (e.g. nav-menu margin, dropdown position). The exact block is in `ar/index.html` and was replicated to all other ar/ pages (blog, contact, demo, technology, company/*, clients/*, solution/*).

### 2.3 Reference for RTL/Cairo block

- **Source of truth:** `ar/index.html` — copy the full `<style>...</style>` that starts with `[dir="rtl"]` font and type scale and ends with `.solution-card.reverse .solution-image { direction: rtl; }` (or equivalent).
- **Subpages:** Same block; only difference is CSS paths (`../../` for ar/blog, ar/contact, ar/demo, ar/technology vs `../../../` for ar/company/*, ar/clients/*, ar/solution/*). Do **not** change `href` paths to `style.css` / `responsive.css` when restoring; only ensure font link is Cairo and the RTL block is present.

---

## 3. English Homepage (index.html) — Restoration Checklist

Apply these in order so nothing is overwritten incorrectly.

1. **`<head>`**
   - Add favicon: `<link rel="icon" type="image/png" href="assets/favicon.png">` (or correct path).
   - Add Google Fonts (e.g. Oswald, DM Sans or Inter) so hero and body match the design. Example:  
     `<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">`  
     (adjust if the project uses Inter or Tchek-specific fonts.)
   - Keep: `<link rel="stylesheet" href="css/style.css">` and `responsive.css`.

2. **Language selector (nav)**
   - Inside the dropdown that lists languages (ES, DE, FR, NL, PT), add **AR** as the first option:
     ```html
     <li><a href="ar/index.html">AR</a></li>
     ```
   - So users on the English site can switch to the Arabic version.

3. **Hero section**
   - Keep existing structure: `hero-title`, `hero-subtitle`, `hero-stats`, `hero-cta` (or `hero-cta-group` if that class exists). These are used by CSS/JS for micro-animations and hero entrance.
   - Ensure the final CTA section (e.g. `.cta-final`) has `id="demo"` for the floating CTA anchor:  
     `<section class="cta-final" id="demo">`.

4. **Footer**
   - In the footer bottom bar, add the legal links block (or restore it if removed):
     ```html
     <div class="footer-bottom">
         <p>&copy; 2026 CarSee. All right reserved.</p>
         <div class="footer-links">
             <span class="legal-links">
                 <a href="privacy.html">Privacy Policy</a>
                 <span>·</span>
                 <a href="terms.html">Terms of Service</a>
                 <span>·</span>
                 <a href="mailto:legal@carsee.app">Legal</a>
             </span>
             <a href="#">Cookies Settings</a>
         </div>
     </div>
     ```
   - Replace “CarSee” / legal@carsee.app with project branding if the site is now Tchek or another brand.

5. **Floating CTA (before `</body>`)**
   - Insert immediately before `<script src="js/main.js"></script>`:
     ```html
     <a href="#demo" class="floating-cta" id="floatingCta" aria-label="Book a Demo">
         <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
             <rect x="3" y="4" width="18" height="18" rx="2"/>
             <line x1="16" y1="2" x2="16" y2="6"/>
             <line x1="8"  y1="2" x2="8"  y2="6"/>
             <line x1="3"  y1="10" x2="21" y2="10"/>
         </svg>
         <span>Book a Demo</span>
     </a>
     ```

---

## 4. Arabic Homepage (ar/index.html) — Restoration Checklist

1. **Language selector**
   - “EN” must point to the English site: `<a href="../index.html">EN</a>`.

2. **Footer**
   - Legal links in Arabic:
     ```html
     <span class="legal-links">
         <a href="privacy.html">سياسة الخصوصية</a>
         <span>·</span>
         <a href="terms.html">شروط الخدمة</a>
         <span>·</span>
         <a href="mailto:legal@carsee.app">قانوني</a>
     </span>
     ```
   - Keep “CarSee” in Latin if that’s the brand; adjust mailto if needed.

3. **Floating CTA (before script)**
   - Same as English but with RTL class and Arabic label:
     ```html
     <a href="#demo" class="floating-cta floating-cta--rtl" id="floatingCta" aria-label="احجز عرضاً">
         <!-- same SVG as English -->
         <span>احجز عرضاً</span>
     </a>
     ```

4. **Section id**
   - Final CTA section: `<section class="cta-final" id="demo">`.

5. **Cairo + RTL**
   - Keep Cairo as the only font in `<head>` and the full RTL `<style>` block; no letter-spacing on Arabic.

---

## 5. CSS (css/style.css) — Features That Must Be Present

If any of these were removed during font/hero updates, re-add them (at the end of the file or in the right section).

- **Micro-animations**
  - `.carsee-animate` / `.carsee-animate.is-visible` (opacity + translateY, cubic-bezier).
  - Nth-child stagger delays for `.carsee-animate` (e.g. 0ms, 90ms, 180ms, …).
  - `.carsee-animate-title` / `.carsee-animate-title.is-visible`.
  - Hero: `.hero-title`, `.hero-subtitle`, `.hero-cta-group`, `.hero-cta`, `.hero-stats` start hidden; `body.page-loaded` reveals them with staggered transition-delays.
  - `.stat-number[data-target]` (min-width for counter).
  - `.hero-scan-line` and `@keyframes scanPulse` (if used).
  - Card hover: `.feature-card`, `.solution-card`, `.professional-card` — hover translateY(-5px) and box-shadow.
  - `@media (prefers-reduced-motion: reduce)` to disable these animations.

- **Floating CTA**
  - `.floating-cta`: fixed position, bottom-right, hidden by default (opacity 0, translateY), `.is-visible` to show, hover styles.
  - `.floating-cta--rtl`: right: auto; left: 36px; Cairo; letter-spacing: 0.
  - Mobile (e.g. max-width 768px): icon only (span hidden), circular button, adjusted padding.

- **Footer legal links**
  - `.legal-links` (flex, gap, wrap).
  - `.legal-links a` (font-size, color, hover).
  - `.legal-links span` (separator).
  - `[dir="rtl"] .legal-links a` (Cairo, letter-spacing: 0).

---

## 6. JavaScript (js/main.js) — Features That Must Be Present

- **Page load**
  - On `DOMContentLoaded`, after a short delay (e.g. 60ms), add class `page-loaded` to `document.body` so hero entrance animations run.

- **Scroll animation observer**
  - Add `.carsee-animate` to: `.feature-card`, `.solution-card`, `.professional-card`, `.step-item`, `.stat-item`, and (if present) `.process-step`, partner logo elements.
  - Add `.carsee-animate-title` to: `.section-title`, `.section-subtitle`.
  - Single IntersectionObserver (e.g. threshold 0.12, rootMargin bottom -40px) that adds `.is-visible` and then unobserves each element (fire once).

- **Stat number counter**
  - For elements with `.stat-number` or `.stat-value`, if they contain a number: set `data-target` and `data-suffix`, set initial text to `0` + suffix, observe with IntersectionObserver, and animate from 0 to target (easeOutExpo, ~1.8s) when in view.

- **Floating CTA visibility**
  - Get `#floatingCta`; on scroll, add `.is-visible` when scrollY > 600 and remove when near footer (e.g. within 100px of footer top or last 300px of page). Use passive scroll listener and run once on load.

Do **not** leave an old observer that sets inline `opacity`/`transform` on the same cards; the new class-based animation should be the only one controlling them.

---

## 7. 404 and Legal Pages — Ensure They Exist and Link Correctly

### 7.1 Files

- `404.html` (English) — Branded 404, link to `index.html` and `index.html#contact`.
- `ar/404.html` (Arabic) — Same idea, Cairo, RTL, link to `ar/index.html` (i.e. `index.html` in ar/), “العودة للرئيسية”, “تواصل معنا”.
- `privacy.html` (English) — Same nav/footer as main site, Ice Surface background, max-width content, 8 sections (intro, data we collect, how we use, storage & security, sharing, your rights, contact, last updated).
- `ar/privacy.html` (Arabic) — Same structure, Cairo, RTL, all content in Arabic, “CarSee” in Latin.
- `terms.html` (English) — Same template as privacy, 9 sections (acceptance, description of service, user responsibilities, IP, limitation of liability, termination, governing law, changes, contact).
- `ar/terms.html` (Arabic) — Same structure, Cairo, RTL, Arabic content, “CarSee” in Latin.

### 7.2 Links

- From English footer: `privacy.html`, `terms.html`, `mailto:legal@carsee.app` (or project email).
- From Arabic footer: `privacy.html`, `terms.html` (relative to `ar/`), same mailto.
- 404 EN: “Go to Homepage” → `index.html`; “Contact Us” → `index.html#contact`.
- 404 AR: “العودة للرئيسية” → `index.html` (Arabic home); “تواصل معنا” → `index.html#contact`.

---

## 8. Quick Verification List for the Next Agent

- [ ] English `index.html`: has favicon + Google Fonts in `<head>`.
- [ ] English `index.html`: language selector includes **AR** with `href="ar/index.html"`.
- [ ] English `index.html`: footer has `.legal-links` with Privacy, Terms, Legal mailto.
- [ ] English `index.html`: floating CTA present before `main.js`, `id="floatingCta"`, `href="#demo"`.
- [ ] English `index.html`: CTA section has `id="demo"`.
- [ ] `ar/index.html`: “EN” in language selector links to `../index.html`.
- [ ] `ar/index.html`: footer has legal links (Arabic labels), floating CTA with `.floating-cta--rtl`, `id="demo"` on CTA section.
- [ ] All `ar/**/*.html` pages: Cairo font in head, full RTL style block, no letter-spacing on Arabic, internal links stay under `ar/`.
- [ ] `css/style.css`: micro-animation classes, hero `.page-loaded` rules, floating CTA and `.legal-links` styles, `prefers-reduced-motion` override.
- [ ] `js/main.js`: `page-loaded` on body, scroll observer for `.carsee-animate` / `.carsee-animate-title`, stat counter, floating CTA visibility; no duplicate inline-style observer for cards.
- [ ] `404.html`, `ar/404.html`, `privacy.html`, `ar/privacy.html`, `terms.html`, `ar/terms.html` exist and link as above.
- [ ] Branding: if CarSee — logo, title, company paths, footer “CarSee”; if Tchek — same structure but Tchek branding, and still keep AR link and all features.

---

## 9. Path Reference (Arabic Subpages)

- **From `ar/blog/`, `ar/contact/`, `ar/demo/`, `ar/technology/`:**
  - CSS: `../../css/style.css`, `../../css/responsive.css`
  - Assets: `../../assets/`
  - Home: `../index.html` (Arabic home = `ar/index.html`)

- **From `ar/company/*`, `ar/clients/*`, `ar/solution/*`:**
  - CSS: `../../../css/style.css`, `../../../css/responsive.css`
  - Assets: `../../../assets/`
  - Home: `../../index.html` (Arabic home)

- **From `ar/index.html`:**
  - CSS: `../css/`, assets: `../assets/`, js: `../js/main.js`
  - Other ar pages: `technology/index.html`, `contact/index.html`, etc. (sibling or child of ar/)

Use this handover to restore the Arabic link from the English version, hero/font setup, floating CTA, footer legal links, and all micro-animations and 404/legal pages without changing unrelated code.
