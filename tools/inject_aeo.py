# -*- coding: utf-8 -*-
"""
Idempotent AEO/SEO injection for static CarSee HTML pages.
Adds: canonical + Open Graph, JSON-LD @graph, hidden AI summary (display:none).
Skips fragment includes and non-site HTML. Re-run safe.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://carsee.ai"
ORG_ID = f"{BASE}/#organization"
TODAY = date.today().isoformat()

SKIP_DIR_PARTS = ("playwright-report", "test-results", "node_modules")
SKIP_FILES = {
    "_tmp_ar_post1.html",
    "_tmp_ar_post2.html",
}
SKIP_NAME_PREFIXES = ("google",)


def should_process(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix().lower()
    if "includes/" in rel:
        return False
    for p in SKIP_DIR_PARTS:
        if p in rel:
            return False
    if path.name.lower() in {s.lower() for s in SKIP_FILES}:
        return False
    if path.name.lower().startswith(SKIP_NAME_PREFIXES):
        return False
    return path.suffix.lower() == ".html"


def file_to_url(rel_posix: str) -> str:
    rel = rel_posix.replace("\\", "/")
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[: -len('index.html')]}".rstrip("/") + "/"
    return f"{BASE}/{rel}"


def is_arabic(rel_posix: str, content: str) -> bool:
    if rel_posix.startswith("ar/"):
        return True
    return bool(re.search(r'<html[^>]*\blang=["\']ar["\']', content, re.I))


def strip_injection(content: str) -> str:
    content = re.sub(
        r"<!-- AEO:inject v1 -->.*?<!-- /AEO:inject v1 -->\s*",
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"<!-- AEO:body v1 -->.*?<!-- /AEO:body v1 -->\s*",
        "",
        content,
        flags=re.DOTALL,
    )
    return content


def extract_title(c: str) -> str:
    m = re.search(r"<title>(.*?)</title>", c, re.DOTALL | re.I)
    return html.unescape(re.sub(r"\s+", " ", m.group(1).strip())) if m else "CarSee"


def extract_description(c: str) -> str:
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
        c,
        re.I,
    )
    if not m:
        m = re.search(
            r'<meta\s+content=["\']([^"\']*)["\']\s+name=["\']description["\']',
            c,
            re.I,
        )
    if not m:
        return ""
    return html.unescape(m.group(1).strip())


def improve_description(desc: str, ar: bool) -> str:
    d = re.sub(r"\s+", " ", desc).strip()
    if not d:
        return (
            "CarSee: منصة فحص أضرار المركبات بالذكاء الاصطناعي للأسواق الخليجية."
            if ar
            else "CarSee: AI-powered vehicle damage inspection and bilingual reporting for fleets, insurers, and automotive businesses."
        )
    if d[-1] not in ".!?؟":
        d += "."
    if len(d) < 95:
        d += (
            " تفاصيل إضافية على موقع CarSee."
            if ar
            else " More detail on the official CarSee site."
        )
    return d


def improve_title(title: str, ar: bool) -> str:
    t = re.sub(r"\s+", " ", title).strip()
    if "CarSee" not in t and "carsee" not in t.lower():
        t += " | CarSee" if not ar else " | CarSee"
    return t


def slug_label(seg: str, ar: bool) -> str:
    mapping_en = {
        "solution": "Solutions",
        "solutions": "Solutions",
        "blog": "Blog",
        "company": "Company",
        "contact": "Contact",
        "clients": "Clients",
        "how-it-works": "How it works",
        "where-we-work": "Where we work",
        "ar": "Arabic",
        "career": "Career",
        "partners": "Partners",
        "demo": "Demo",
        "technology": "Technology",
    }
    mapping_ar = {
        "solution": "الحلول",
        "solutions": "الحلول",
        "blog": "المدونة",
        "company": "الشركة",
        "contact": "اتصل بنا",
        "clients": "العملاء",
        "how-it-works": "كيف يعمل",
        "where-we-work": "أين نعمل",
        "ar": "العربية",
        "career": "الوظائف",
        "partners": "الشركاء",
        "demo": "تجربة",
        "technology": "التقنية",
    }
    m = mapping_ar if ar else mapping_en
    key = seg.lower().replace(".html", "")
    if key in m:
        return m[key]
    return seg.replace("-", " ").replace("_", " ").title()


def breadcrumb_items(rel_posix: str, ar: bool) -> list[tuple[str, str]]:
    url = file_to_url(rel_posix)
    norm = rel_posix.replace("\\", "/")
    home_label = "Home" if not ar else "الرئيسية"
    items: list[tuple[str, str]] = [(f"{BASE}/", home_label)]
    if norm == "index.html":
        return items
    if norm.endswith("/index.html"):
        norm = norm[: -len("index.html")].rstrip("/")
    segs = [s for s in norm.split("/") if s]
    for i in range(len(segs)):
        sub = "/".join(segs[: i + 1])
        if sub.endswith(".html"):
            u = file_to_url(sub)
            label = slug_label(segs[i].replace(".html", ""), ar)
        else:
            u = file_to_url(sub + "/index.html")
            label = slug_label(segs[i], ar)
        items.append((u, label))
    items[-1] = (url, items[-1][1])
    return items[-12:]


def faq_entities(title: str, desc: str, ar: bool) -> list[dict]:
    if ar:
        qs = [
            ("ما هي CarSee؟", "CarSee منصة لفحص أضرار المركبات بالذكاء الاصطناعي وتقدير تكاليف الإصلاح وفق السوق المحلي."),
            ("من يستفيد من هذه الصفحة؟", "الفرق التجارية والتقنية والمهتمون بخدمات CarSee في منطقة الخليج والشرق الأوسط."),
            ("هل التقارير ثنائية اللغة؟", "نعم، يدعم CarSee مخرجات بالعربية والإنجليزية حيث ينطبق ذلك على المنتج."),
            ("كيف أتواصل مع CarSee؟", "يمكن التواصل عبر نموذج الاتصال في الموقع أو البريد الرسمي للشركة."),
            ("هل يوجد تطبيق جوال؟", "تتوفر تجربة التطبيق عبر صفحة «تطبيقنا» مع روابط المتاجر عند توفرها."),
            ("أين تعمل CarSee جغرافياً؟", "تركز CarSee على أسواق الخليج والشرق الأوسط مع توسع وفق الإعلانات الرسمية."),
            ("هل البيانات آمنة؟", "تُطبّق ممارسات أمنية قياسية لخدمات SaaS؛ راجع سياسة الخصوصية للتفاصيل."),
            ("هل تدعم المنصات التكامل API؟", "تتوفر قدرات تكامل للفرق التي تحتاج إشارة فحص موحدة ضمن منتجاتها."),
            ("ما المخرجات التي يولدها CarSee؟", "سرد منظم للفحص وتصنيف الأضرار وإشارات تكلفة إصلاح متوافقة مع اقتصاديات الإصلاح في المنطقة."),
            ("هل يستبدل CarSee المقيم الميداني؟", "يعزز CarSee سير العمل بأتمتة ثابتة من الصورة إلى التقرير؛ القرار النهائي يبقى لدى فريقكم وسياساتكم."),
        ]
    else:
        qs = [
            ("What is CarSee?", "CarSee is an AI-assisted vehicle damage inspection platform that produces structured assessments and repair cost signals."),
            ("Who is this page for?", "Automotive, insurance, fleet, and platform teams evaluating CarSee for GCC and MENA workflows."),
            ("Does CarSee support bilingual reporting?", "CarSee is built to support Arabic and English outputs where applicable to the product surface."),
            ("How can I contact CarSee?", "Use the on-site contact form or the official email channels referenced in the footer."),
            ("Is there a mobile app?", "See the Our App page for download links and onboarding guidance when available."),
            ("Where does CarSee operate?", "CarSee focuses on GCC/MENA markets; see Where we work for market context."),
            ("Is my data handled securely?", "CarSee follows common SaaS security practices; read the privacy policy for specifics."),
            ("Can CarSee integrate via API?", "API-oriented inspection workflows exist for teams that need a consistent vehicle condition signal."),
            ("What outputs does CarSee generate?", "Structured inspection narratives, damage categorization, and repair cost signals aligned to regional repair economics."),
            ("Does CarSee replace a physical appraiser?", "CarSee augments workflows with consistent photo-to-report automation; final decisions remain with your team and policies."),
        ]
    out = []
    for q, a in qs[:12]:
        out.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    return out


def service_node(rel_posix: str, url: str, title: str, desc: str) -> dict | None:
    rp = rel_posix.lower()
    if "our-app" in rp:
        return {
            "@type": "SoftwareApplication",
            "@id": url + "#software",
            "name": "CarSee mobile app",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "iOS, Android",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "description": desc or title,
        }
    if "/solution/" in "/" + rp or rp.startswith("solution/"):
        return {
            "@type": "Service",
            "@id": url + "#service",
            "name": title,
            "serviceType": "Vehicle inspection software",
            "provider": {"@id": ORG_ID},
            "areaServed": ["AE", "SA", "QA", "KW", "BH", "OM", "EG", "JO"],
            "description": desc or title,
        }
    return None


def local_business_node(ar: bool) -> dict | None:
    return {
        "@type": "ProfessionalService",
        "@id": f"{BASE}/#professionalService",
        "name": "CarSee",
        "image": f"{BASE}/assets/logos/logo_banner.png",
        "url": BASE,
        "description": (
            "خدمات برمجية لفحص أضرار المركبات بالذكاء الاصطناعي."
            if ar
            else "Software-enabled AI vehicle damage inspection and reporting."
        ),
        "areaServed": ["GCC", "Middle East", "North Africa"],
        "parentOrganization": {"@id": ORG_ID},
    }


def build_graph(
    rel_posix: str, url: str, title: str, desc: str, ar: bool
) -> list[dict]:
    crumbs = breadcrumb_items(rel_posix, ar)
    bl_items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": name,
            "item": u,
        }
        for i, (u, name) in enumerate(crumbs)
    ]
    graph: list[dict] = [
        {
            "@type": "Organization",
            "@id": ORG_ID,
            "name": "CarSee",
            "url": BASE,
            "logo": f"{BASE}/assets/logos/logo-png-big.png",
            "sameAs": [
                "https://x.com/carseeai",
                "https://www.youtube.com/@carseeai",
                "https://www.instagram.com/carseeai/",
                "https://www.facebook.com/carseeeai",
            ],
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "inLanguage": "ar" if ar else "en",
            "isPartOf": {"@type": "WebSite", "url": BASE, "name": "CarSee"},
            "about": {"@id": ORG_ID},
        },
        {
            "@type": "FAQPage",
            "@id": url + "#faq",
            "mainEntity": faq_entities(title, desc, ar),
        },
        {
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumb",
            "itemListElement": bl_items,
        },
        local_business_node(ar),
    ]
    svc = service_node(rel_posix, url, title, desc)
    if svc:
        graph.append(svc)
    return graph


def og_block(url: str, title: str, desc: str, ar: bool) -> str:
    loc = "ar_AE" if ar else "en_US"
    esc = lambda s: (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    t, d = esc(title), esc(desc)
    u = esc(url)
    img = esc(f"{BASE}/assets/logos/logo_banner.png")
    return f"""<link rel="canonical" href="{u}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="CarSee">
    <meta property="og:locale" content="{loc}">
    <meta property="og:url" content="{u}">
    <meta property="og:title" content="{t}">
    <meta property="og:description" content="{d}">
    <meta property="og:image" content="{img}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{t}">
    <meta name="twitter:description" content="{d}">
    <meta name="twitter:image" content="{img}">"""


def ai_summary_html(title: str, desc: str, url: str, ar: bool) -> str:
    if ar:
        bullets = [
            f"الصفحة: {html.escape(title)}.",
            "الجمهور: فرق الأعمال والتقنية في قطاع السيارات والتأمين والأساطيل في المنطقة.",
            f"الوصف المختصر: {html.escape(desc[:220])}{'…' if len(desc) > 220 else ''}",
            "قيمة مميزة: تقييم أضرار أسرع مع مخرجات منظمة ودعم سياقات سوق الخليج.",
            f"المصدر الرسمي للرابط: {html.escape(url)}",
        ]
    else:
        bullets = [
            f"Page topic: {html.escape(title)}.",
            "Audience: automotive, insurance, fleet, and marketplace teams evaluating AI inspection workflows.",
            f"Key facts: {html.escape(desc[:220])}{'…' if len(desc) > 220 else ''}",
            "Unique value: structured, bilingual-ready inspection outputs with GCC-aware repair economics where applicable.",
            f"Canonical reference: {html.escape(url)}",
        ]
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""<!-- AEO:body v1 -->
<div style="display:none" data-ai-summary="true" aria-hidden="true">
<ul>{lis}</ul>
</div>
<!-- /AEO:body v1 -->"""


def inject_head(content: str, head_inject: str) -> str:
    low = content.lower()
    if "</head>" in low:
        idx = low.rfind("</head>")
        return content[:idx] + head_inject + "\n" + content[idx:]
    return content


def inject_body(content: str, body_block: str) -> str:
    m = re.search(r"<body([^>]*)>", content, re.I)
    if not m:
        return content
    end = m.end()
    return content[:end] + "\n" + body_block + "\n" + content[end:]


def replace_meta_description(content: str, new_desc: str) -> str:
    esc_attr = (
        new_desc.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    def repl1(m):
        return f'<meta name="description" content="{esc_attr}">'

    def repl2(m):
        return f'<meta content="{esc_attr}" name="description">'

    c2, n = re.subn(
        r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*>',
        repl1,
        content,
        count=1,
        flags=re.I,
    )
    if n:
        return c2
    c2, n = re.subn(
        r'<meta\s+content=["\'][^"\']*["\']\s+name=["\']description["\']\s*>',
        repl2,
        content,
        count=1,
        flags=re.I,
    )
    if n:
        return c2
    return content


def replace_title(content: str, new_title: str) -> str:
    esc = (
        new_title.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return re.sub(
        r"<title>.*?</title>",
        f"<title>{esc}</title>",
        content,
        count=1,
        flags=re.DOTALL | re.I,
    )


def add_landmarks(content: str) -> str:
    c, n = re.subn(
        r'<header\s+class="header"(?![^>]*\brole=)',
        '<header class="header" role="banner"',
        content,
        count=1,
        flags=re.I,
    )
    c, n2 = re.subn(
        r'<footer\s+class="footer"(?![^>]*\brole=)',
        '<footer class="footer" role="contentinfo"',
        c,
        count=1,
        flags=re.I,
    )
    return c


def process_file(path: Path) -> tuple[bool, str | None]:
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8")
    cleaned = strip_injection(raw)
    ar = is_arabic(rel, cleaned)
    title0 = extract_title(cleaned)
    desc0 = extract_description(cleaned)
    desc = improve_description(desc0, ar)
    title = improve_title(title0, ar)
    url = file_to_url(rel)
    graph = build_graph(rel, url, title, desc, ar)
    ld = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    head_inject = f"""<!-- AEO:inject v1 -->
{og_block(url, title, desc, ar)}
    <script type="application/ld+json">{ld}</script>
<!-- /AEO:inject v1 -->"""
    body_block = ai_summary_html(title0, desc0, url, ar)
    out = cleaned
    out = replace_title(out, title)
    out = replace_meta_description(out, desc)
    out = inject_head(out, head_inject)
    out = inject_body(out, body_block)
    out = add_landmarks(out)
    if out != raw:
        path.write_text(out, encoding="utf-8", newline="\n")
        return True, url
    return False, None


def main() -> int:
    urls: list[str] = []
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not should_process(path):
            continue
        ok, u = process_file(path)
        if ok and u:
            changed += 1
            urls.append(u)
    urls = sorted(set(urls))
    sitemap_path = ROOT / "aeo-sitemap.xml"
    body = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        + [
            f"  <url><loc>{html.escape(u)}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>"
            for u in urls
        ]
        + ["</urlset>", ""]
    )
    sitemap_path.write_text(body, encoding="utf-8", newline="\n")
    print("Updated pages:", changed)
    print("AEO sitemap URLs:", len(urls))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
