# CarSee website — webpage inventory

**Site type:** Static HTML (no app router). **Locales:** English at repo root, Arabic under [`ar/`](ar/).

**Not counted as "webpages" for visitors:** [`includes/header.html`](includes/header.html), [`ar/includes/header.html`](ar/includes/header.html) (partials); [`googleafb76d3b93629f91.html`](googleafb76d3b93629f91.html) (Google Search Console verification); [`my-video/`](my-video/) (separate Remotion/video project, not site content).

---

## English (`/` — paths relative to site root)

| URL path | File |
|----------|------|
| `/` | [`index.html`](index.html) |
| `/how-it-works/` | [`how-it-works/index.html`](how-it-works/index.html) |
| `/demo/` | [`demo/index.html`](demo/index.html) |
| `/technology/` | [`technology/index.html`](technology/index.html) |
| `/blog/` | [`blog/index.html`](blog/index.html) |
| `/contact/` | [`contact/index.html`](contact/index.html) |
| `/pricing.html` | [`pricing.html`](pricing.html) |
| `/benefits.html` | [`benefits.html`](benefits.html) |
| `/our-app.html` | [`our-app.html`](our-app.html) |
| `/terms.html` | [`terms.html`](terms.html) |
| `/privacy.html` | [`privacy.html`](privacy.html) |
| `/cookies.html` | [`cookies.html`](cookies.html) |
| `/404.html` | [`404.html`](404.html) |
| `/test_animation.html` | [`test_animation.html`](test_animation.html) *(likely internal / dev)* |

**Solutions** (`/solution/.../`):

- [`solution/car-traders/index.html`](solution/car-traders/index.html)
- [`solution/rental-companies/index.html`](solution/rental-companies/index.html)
- [`solution/private-car-owners/index.html`](solution/private-car-owners/index.html)
- [`solution/remote-trade-in/index.html`](solution/remote-trade-in/index.html)
- [`solution/on-site-trade-in/index.html`](solution/on-site-trade-in/index.html)
- [`solution/car-fleet/index.html`](solution/car-fleet/index.html)
- [`solution/inspection/index.html`](solution/inspection/index.html)
- [`solution/remarketing/index.html`](solution/remarketing/index.html)

**Company** (`/company/.../`):

- [`company/carsee/index.html`](company/carsee/index.html)
- [`company/career/index.html`](company/career/index.html)
- [`company/press/index.html`](company/press/index.html)
- [`company/partners/index.html`](company/partners/index.html)

**Clients** (`/clients/.../`):

- [`clients/dealerships/index.html`](clients/dealerships/index.html)
- [`clients/uv-marketplaces/index.html`](clients/uv-marketplaces/index.html)
- [`clients/oem/index.html`](clients/oem/index.html)
- [`clients/rental-cars-car-sharing/index.html`](clients/rental-cars-car-sharing/index.html)
- [`clients/insurers-experts/index.html`](clients/insurers-experts/index.html)
- [`clients/leasing/index.html`](clients/leasing/index.html)
- [`clients/software-publishers/index.html`](clients/software-publishers/index.html)

**English total (counting `test_animation.html`):** 34 HTML pages.

---

## Arabic (`/ar/...` — mirror structure)

Same paths as English, prefixed with `ar/`:

- [`ar/index.html`](ar/index.html)
- [`ar/how-it-works/index.html`](ar/how-it-works/index.html), [`ar/demo/index.html`](ar/demo/index.html), [`ar/technology/index.html`](ar/technology/index.html), [`ar/blog/index.html`](ar/blog/index.html), [`ar/contact/index.html`](ar/contact/index.html)
- [`ar/pricing.html`](ar/pricing.html), [`ar/benefits.html`](ar/benefits.html), [`ar/our-app.html`](ar/our-app.html), [`ar/terms.html`](ar/terms.html), [`ar/privacy.html`](ar/privacy.html), [`ar/cookies.html`](ar/cookies.html), [`ar/404.html`](ar/404.html)
- All eight [`ar/solution/.../index.html`](ar/solution/car-traders/index.html) pages (same slugs as EN)
- All four [`ar/company/.../index.html`](ar/company/carsee/index.html) pages
- All seven [`ar/clients/.../index.html`](ar/clients/dealerships/index.html) pages

**Arabic total:** 33 HTML pages (no `ar/test_animation.html` in the repo).

---

## Summary

| Locale | Count |
|--------|--------|
| English | 34 |
| Arabic | 33 |
| **Grand total (unique HTML entry points)** | **67** |

Main nav in [`index.html`](index.html) highlights a subset (How it works, three solution links, Pricing, Blog, Why CarSee, Our App, About submenu); additional solution, client, technology, and demo pages exist as full pages linked from footers or elsewhere.
