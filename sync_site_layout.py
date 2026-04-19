#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unify site headers (EN / AR), remove survey banners from all pages.
Uses the same navigation structure as includes/header.html and ar/includes/header.html.
"""
from __future__ import annotations

import re
import sys
import os
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = Path(__file__).parent

SKIP_PREFIXES = ("my-video/",)
SKIP_NAMES = {
    "googleafb76d3b93629f91.html",
    "sync_site_layout.py",
}

# Match through the close button and outer </div> (first </div> would only close .survey-content).
SURVEY_BLOCK = re.compile(
    r"\s*(?:<!--\s*Survey\s*Banner\s*-->\s*)?"
    r'<div\s+class="survey-banner"[^>]*>.*?</button>\s*</div>\s*',
    re.DOTALL | re.IGNORECASE,
)

# Leftovers if an older regex stripped only the opening wrapper.
ORPHAN_SURVEY_TAIL = re.compile(
    r"(<body[^>]*>\s*)<button\s+class=\"banner-close\"[^>]*>.*?</button>\s*</div>\s*",
    re.DOTALL | re.IGNORECASE,
)

HEADER_BLOCK = re.compile(
    r"(?:<!--\s*Header\s*-->\s*)?<header\s+class=\"header\">.*?</header>\s*",
    re.DOTALL | re.IGNORECASE,
)


def should_skip(path: Path) -> bool:
    s = path.as_posix()
    if "my-video" in s:
        return True
    if path.name in SKIP_NAMES:
        return True
    # Fragment templates live here; paths are not page-relative.
    if "includes" in path.parts:
        return True
    return False


def en_prefix(path: Path) -> str:
    rel = path.relative_to(BASE)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else ""


def ar_prefix(path: Path) -> str:
    rel = path.relative_to(BASE)
    depth = len(rel.parts) - 2
    return "../" * depth if depth > 0 else ""


def language_switch_href(path: Path) -> str:
    """Relative href to the equivalent page in the other language."""
    rel = path.relative_to(BASE)
    parts = rel.parts
    if parts and parts[0] == "ar":
        en_rel = Path(*parts[1:]) if len(parts) > 1 else Path("index.html")
        target, start = en_rel, rel.parent
    else:
        target, start = Path("ar") / rel, rel.parent
    return os.path.relpath(target, start).replace("\\", "/")


def build_en_header(p: str, lang_href: str) -> str:
    return f"""    <!-- Header -->
    <header class="header">
        <nav class="navbar">
            <div class="container">
                <div class="nav-wrapper">
                    <div class="logo">
                        <a href="{p}index.html" class="logo-link">
                            <img src="{p}assets/logos/logo-png-big.png" alt="CarSee Logo" id="logo">
                            <span class="logo-text-wrap">
                                <span class="nav-logo-text">Car<span class="logo-see">See</span></span>
                                <span class="nav-logo-subtitle">AI Damage Evaluation</span>
                            </span>
                        </a>
                    </div>
                    <ul class="nav-menu" id="navMenu">
                        <li class="nav-item"><a href="{p}how-it-works/index.html" class="nav-link">How it works</a></li>
                        <li class="nav-item dropdown">
                            <a href="#" class="nav-link">Our Solutions Include <span class="dropdown-arrow">▼</span></a>
                            <ul class="dropdown-menu">
                                <li><a href="{p}solution/car-traders/index.html">Car Traders</a></li>
                                <li><a href="{p}solution/rental-companies/index.html">Rental Companies</a></li>
                                <li><a href="{p}solution/private-car-owners/index.html">Private Car Owners</a></li>
                            </ul>
                        </li>
                        <li class="nav-item"><a href="{p}pricing.html" class="nav-link">Pricing</a></li>
                        <li class="nav-item"><a href="{p}blog/index.html" class="nav-link">Blog</a></li>
                        <li class="nav-item"><a href="{p}benefits.html" class="nav-link">Why CarSee?</a></li>
                        <li class="nav-item"><a href="{p}our-app.html" class="nav-link">Our App</a></li>
                        <li class="nav-item"><a href="{p}where-we-work/index.html" class="nav-link">Where we work</a></li>
                        <li class="nav-item dropdown">
                            <a href="#" class="nav-link">About <span class="dropdown-arrow">▼</span></a>
                            <ul class="dropdown-menu">
                                <li><a href="{p}company/career/index.html">Career</a></li>
                                <li><a href="{p}company/partners/index.html">Become a Partner</a></li>
                                <li><a href="{p}contact/index.html">Contact us</a></li>
                            </ul>
                        </li>
                    </ul>
                    <div class="nav-actions">
                        <div class="language-selector">
                            <span>EN</span>
                            <ul class="language-menu">
                                <li><a href="{lang_href}">AR</a></li>
                            </ul>
                        </div>
                        <a href="{p}our-app.html" class="btn-demo">Download Now!</a>
                        <button class="mobile-menu-toggle" id="mobileMenuToggle">
                            <span></span>
                            <span></span>
                            <span></span>
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    </header>
"""


def build_ar_header(b: str, lang_href: str) -> str:
    return f"""    <!-- Header -->
    <header class="header">
        <nav class="navbar">
            <div class="container">
                <div class="nav-wrapper">
                    <div class="logo">
                        <a href="{b}index.html" class="logo-link">
                            <img src="{b}../assets/logos/logo-png-big.png" alt="CarSee Logo" id="logo">
                            <span class="logo-text-wrap">
                                <span class="nav-logo-text">Car<span class="logo-see">See</span></span>
                                <span class="nav-logo-subtitle">تقييم الأضرار بالذكاء الاصطناعي</span>
                            </span>
                        </a>
                    </div>
                    <ul class="nav-menu" id="navMenu">
                        <li class="nav-item"><a href="{b}how-it-works/index.html" class="nav-link">كيف يعمل</a></li>
                        <li class="nav-item dropdown">
                            <a href="#" class="nav-link">حلولنا تشمل <span class="dropdown-arrow">▼</span></a>
                            <ul class="dropdown-menu">
                                <li><a href="{b}solution/car-traders/index.html">تجار السيارات</a></li>
                                <li><a href="{b}solution/rental-companies/index.html">شركات التأجير</a></li>
                                <li><a href="{b}solution/private-car-owners/index.html">أصحاب السيارات الخاصة</a></li>
                            </ul>
                        </li>
                        <li class="nav-item"><a href="{b}pricing.html" class="nav-link">الأسعار</a></li>
                        <li class="nav-item"><a href="{b}blog/index.html" class="nav-link">المدونة</a></li>
                        <li class="nav-item"><a href="{b}benefits.html" class="nav-link">لماذا CarSee؟</a></li>
                        <li class="nav-item"><a href="{b}our-app.html" class="nav-link">تطبيقنا</a></li>
                        <li class="nav-item"><a href="{b}where-we-work/index.html" class="nav-link">أين نعمل</a></li>
                        <li class="nav-item dropdown">
                            <a href="#" class="nav-link">عن CarSee <span class="dropdown-arrow">▼</span></a>
                            <ul class="dropdown-menu">
                                <li><a href="{b}company/career/index.html">الوظائف</a></li>
                                <li><a href="{b}company/partners/index.html">انضم كشريك</a></li>
                                <li><a href="{b}contact/index.html">اتصل بنا</a></li>
                            </ul>
                        </li>
                    </ul>
                    <div class="nav-actions">
                        <div class="language-selector">
                            <span>AR</span>
                            <ul class="language-menu">
                                <li><a href="{lang_href}">EN</a></li>
                            </ul>
                        </div>
                        <a href="{b}our-app.html" class="btn-demo">تنزيل التطبيق الآن</a>
                        <button class="mobile-menu-toggle" id="mobileMenuToggle">
                            <span></span>
                            <span></span>
                            <span></span>
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    </header>
"""


def process_file(path: Path) -> tuple[bool, str]:
    rel = path.relative_to(BASE).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"read error: {e}"

    orig = text
    text = SURVEY_BLOCK.sub("\n", text, count=1)
    text = ORPHAN_SURVEY_TAIL.sub(r"\1", text, count=1)

    if '<header class="header">' not in text:
        if text != orig:
            path.write_text(text, encoding="utf-8")
            return True, "survey removed only"
        return False, "no standard header"

    is_ar = rel.startswith("ar/")
    p = ar_prefix(path) if is_ar else en_prefix(path)
    lang_href = language_switch_href(path)
    new_h = build_ar_header(p, lang_href) if is_ar else build_en_header(p, lang_href)

    new_text, n = HEADER_BLOCK.subn(new_h, text, count=1)
    if n == 0:
        if text != orig:
            path.write_text(text, encoding="utf-8")
            return True, "survey removed; header regex miss"
        return False, "header regex miss"

    if new_text == orig:
        return False, "unchanged"

    path.write_text(new_text, encoding="utf-8")
    return True, "survey + header" if orig != text else "header"


def main() -> None:
    htmls = sorted(p for p in BASE.rglob("*.html") if not should_skip(p))
    ok = 0
    for p in htmls:
        changed, msg = process_file(p)
        if changed:
            print(f"[OK] {p.relative_to(BASE)}: {msg}")
            ok += 1
        else:
            print(f"[--] {p.relative_to(BASE)}: {msg}")
    print(f"\nUpdated: {ok} / {len(htmls)}")


if __name__ == "__main__":
    main()
