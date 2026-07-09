#!/usr/bin/env python3
"""
Updates the navigation header across all HTML pages to the new unified structure.
Run from the website root directory.
"""
import os
import re
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent)

SKIP_FILES = {'_update_headers.py'}
SKIP_DIRS  = {'includes', '.git', 'node_modules', '__pycache__'}

def _language_switch_href(rel_posix: str) -> str:
    """Relative href from current page to the equivalent page in the other language."""
    rel_path = Path(rel_posix)
    parts = rel_path.parts
    if parts and parts[0] == "ar":
        en_rel = Path(*parts[1:]) if len(parts) > 1 else Path("index.html")
        target, start = en_rel, rel_path.parent
    else:
        target, start = Path("ar") / rel_path, rel_path.parent
    return os.path.relpath(target, start).replace("\\", "/")


def get_params(filepath):
    rel = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")
    parts = rel.split("/")
    depth = len(parts) - 1  # 0 = root, 1 = one sub-dir, etc.
    is_ar = parts[0] == "ar"

    if is_ar:
        ar_parts = parts[1:]  # strip the 'ar/' prefix
        ar_depth = len(ar_parts) - 1
        ar_prefix = "../" * ar_depth  # reaches ar/ root
        en_link = _language_switch_href(rel)
        logo_href = ar_prefix + "index.html"
        assets = ar_prefix + "../assets/"
        return dict(
            is_ar=True,
            prefix=ar_prefix,
            logo_href=logo_href,
            lang_link=en_link,
            assets=assets,
        )
    else:
        en_prefix = "../" * depth
        ar_link = _language_switch_href(rel)
        logo_href = en_prefix + "index.html"
        assets = en_prefix + "assets/"
        return dict(
            is_ar=False,
            prefix=en_prefix,
            logo_href=logo_href,
            lang_link=ar_link,
            assets=assets,
        )


def build_header(p):
    px  = p['prefix']
    lh  = p['logo_href']
    as_ = p['assets']
    ll  = p['lang_link']

    if p['is_ar']:
        subtitle = 'تقييم الأضرار بالذكاء الاصطناعي'
        menu = (
            f'                    <ul class="nav-menu" id="navMenu">\n'
            f'                        <li class="nav-item"><a href="{px}how-it-works/index.html" class="nav-link">كيف يعمل</a></li>\n'
            f'                        <li class="nav-item dropdown">\n'
            f'                            <a href="#" class="nav-link">حلولنا تشمل <span class="dropdown-arrow">▼</span></a>\n'
            f'                            <ul class="dropdown-menu">\n'
            f'                                <li><a href="{px}solution/car-traders/index.html">تجار السيارات</a></li>\n'
            f'                                <li><a href="{px}solution/rental-companies/index.html">شركات التأجير</a></li>\n'
            f'                                <li><a href="{px}solution/private-car-owners/index.html">أصحاب السيارات الخاصة</a></li>\n'
            f'                            </ul>\n'
            f'                        </li>\n'
            f'                        <li class="nav-item"><a href="{px}pricing.html" class="nav-link">الأسعار</a></li>\n'
            f'                        <li class="nav-item"><a href="{px}blog/index.html" class="nav-link">المدونة</a></li>\n'
            f'                        <li class="nav-item"><a href="{px}benefits.html" class="nav-link">لماذا CarSee؟</a></li>\n'
            f'                        <li class="nav-item"><a href="{px}our-app.html" class="nav-link">تطبيقنا</a></li>\n'
            f'                        <li class="nav-item dropdown">\n'
            f'                            <a href="#" class="nav-link">عن CarSee <span class="dropdown-arrow">▼</span></a>\n'
            f'                            <ul class="dropdown-menu">\n'
            f'                                <li><a href="{px}company/career/index.html">الوظائف</a></li>\n'
            f'                                <li><a href="{px}company/partners/index.html">انضم كشريك</a></li>\n'
            f'                                <li><a href="{px}contact/index.html">اتصل بنا</a></li>\n'
            f'                            </ul>\n'
            f'                        </li>\n'
            f'                    </ul>'
        )
        actions = (
            f'                    <div class="nav-actions">\n'
            f'                        <div class="language-selector">\n'
            f'                            <span>AR</span>\n'
            f'                            <ul class="language-menu">\n'
            f'                                <li><a href="{ll}">EN</a></li>\n'
            f'                            </ul>\n'
            f'                        </div>\n'
            f'                        <a href="{px}our-app.html" class="btn-demo">تنزيل الآن</a>\n'
            f'                        <button class="mobile-menu-toggle" id="mobileMenuToggle">\n'
            f'                            <span></span>\n'
            f'                            <span></span>\n'
            f'                            <span></span>\n'
            f'                        </button>\n'
            f'                    </div>'
        )
    else:
        subtitle = 'AI Damage Evaluation'
        menu = (
            f'                    <ul class="nav-menu" id="navMenu">\n'
            f'                        <li class="nav-item"><a href="{px}how-it-works/index.html" class="nav-link">How it works</a></li>\n'
            f'                        <li class="nav-item dropdown">\n'
            f'                            <a href="#" class="nav-link">Our Solutions Include <span class="dropdown-arrow">▼</span></a>\n'
            f'                            <ul class="dropdown-menu">\n'
            f'                                <li><a href="{px}solution/car-traders/index.html">Car Traders</a></li>\n'
            f'                                <li><a href="{px}solution/rental-companies/index.html">Rental Companies</a></li>\n'
            f'                                <li><a href="{px}solution/private-car-owners/index.html">Private Car Owners</a></li>\n'
            f'                            </ul>\n'
            f'                        </li>\n'
            f'                        <li class="nav-item"><a href="{px}pricing.html" class="nav-link">Pricing</a></li>\n'
            f'                        <li class="nav-item"><a href="{px}blog/index.html" class="nav-link">Blog</a></li>\n'
            f'                        <li class="nav-item"><a href="{px}benefits.html" class="nav-link">Why CarSee?</a></li>\n'
            f'                        <li class="nav-item"><a href="{px}our-app.html" class="nav-link">Our App</a></li>\n'
            f'                        <li class="nav-item dropdown">\n'
            f'                            <a href="#" class="nav-link">About <span class="dropdown-arrow">▼</span></a>\n'
            f'                            <ul class="dropdown-menu">\n'
            f'                                <li><a href="{px}company/career/index.html">Career</a></li>\n'
            f'                                <li><a href="{px}company/partners/index.html">Become a Partner</a></li>\n'
            f'                                <li><a href="{px}contact/index.html">Contact us</a></li>\n'
            f'                            </ul>\n'
            f'                        </li>\n'
            f'                    </ul>'
        )
        actions = (
            f'                    <div class="nav-actions">\n'
            f'                        <div class="language-selector">\n'
            f'                            <span>EN</span>\n'
            f'                            <ul class="language-menu">\n'
            f'                                <li><a href="{ll}">AR</a></li>\n'
            f'                            </ul>\n'
            f'                        </div>\n'
            f'                        <a href="{px}our-app.html" class="btn-demo">Download Now!</a>\n'
            f'                        <button class="mobile-menu-toggle" id="mobileMenuToggle">\n'
            f'                            <span></span>\n'
            f'                            <span></span>\n'
            f'                            <span></span>\n'
            f'                        </button>\n'
            f'                    </div>'
        )

    return (
        f'    <!-- Header -->\n'
        f'    <header class="header">\n'
        f'        <nav class="navbar">\n'
        f'            <div class="container">\n'
        f'                <div class="nav-wrapper">\n'
        f'                    <div class="logo">\n'
        f'                        <a href="{lh}" class="logo-link">\n'
        f'                            <img src="{as_}logos/logo-png-big.png" alt="CarSee Logo" id="logo">\n'
        f'                            <span class="logo-text-wrap">\n'
        f'                                <span class="nav-logo-text">Car<span class="logo-see">See</span></span>\n'
        f'                                <span class="nav-logo-subtitle">{subtitle}</span>\n'
        f'                            </span>\n'
        f'                        </a>\n'
        f'                    </div>\n'
        f'{menu}\n'
        f'{actions}\n'
        f'                </div>\n'
        f'            </div>\n'
        f'        </nav>\n'
        f'    </header>'
    )


HEADER_RE = re.compile(
    r'(?:[ \t]*<!-- Header -->[ \t]*\n)?[ \t]*<header class="header">.*?</header>',
    re.DOTALL
)

def process(filepath):
    params = get_params(filepath)
    new_hdr = build_header(params)

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    new_content = HEADER_RE.sub(new_hdr, content)
    if new_content == content:
        return 'skip'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return 'ok'


updated = skipped = errors = 0
for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        if not fname.endswith('.html') or fname in SKIP_FILES:
            continue
        fp = os.path.join(root, fname)
        try:
            r = process(fp)
            if r == 'ok':
                updated += 1
                print(f'  OK  {os.path.relpath(fp, BASE_DIR)}')
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f'  ERR {os.path.relpath(fp, BASE_DIR)}: {e}')

print(f'\nDone — updated: {updated}, skipped (no header found): {skipped}, errors: {errors}')
