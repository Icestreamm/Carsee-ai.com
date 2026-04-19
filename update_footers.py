#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update all HTML files with standardized footers based on language and directory depth.
"""

import os
import re
import sys
from pathlib import Path

# Fix Windows encoding issues
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Base directory
BASE_DIR = Path(__file__).parent

# Files to exclude
EXCLUDE_FILES = {
    '404.html',
    'test_animation.html',
    'includes/header.html',
    'googleafb76d3b93629f91.html',
    'ar/404.html',
    'ar/includes/header.html'
}

def get_relative_depth(file_path):
    """Calculate directory depth relative to base."""
    rel_path = file_path.relative_to(BASE_DIR)
    # Count directory levels
    return len(rel_path.parts) - 1

def get_path_prefix(depth):
    """Get the path prefix for the depth level."""
    if depth == 0:
        return ""
    return "../" * depth

def adjust_footer_paths(footer_html, prefix):
    """Adjust all relative paths in the footer based on prefix."""
    if not prefix:
        return footer_html

    # Pattern to match href="path/to/file" (but not mailto: or #)
    pattern_href = r'href="(?!(?:mailto:|#|https?:))([^"]+)"'

    def replace_href(match):
        path = match.group(1)
        if path.startswith(('../', '/')):
            return match.group(0)
        return f'href="{prefix}{path}"'

    footer_html = re.sub(pattern_href, replace_href, footer_html)

    pattern_src = r'src="(?!(?:https?:))([^"]+)"'

    def replace_src(match):
        path = match.group(1)
        if path.startswith(('../', '/')):
            return match.group(0)
        return f'src="{prefix}{path}"'

    return re.sub(pattern_src, replace_src, footer_html)

def create_english_footer(depth):
    """Create English footer with adjusted paths."""
    prefix = get_path_prefix(depth)
    footer = '''    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-brand-row">
                <a href="index.html" class="footer-logo-link" aria-label="CarSee home">
                    <img src="assets/logos/logo_banner.png" alt="CarSee" class="footer-logo-img" loading="lazy">
                </a>
                <nav class="footer-social" aria-label="Social media">
                    <a class="footer-social-link" href="https://www.youtube.com/@carseeai" target="_blank" rel="noopener noreferrer" title="YouTube — @carseeai" aria-label="YouTube @carseeai">
                        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.7 31.7 0 0 0 0 12a31.7 31.7 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1 31.7 31.7 0 0 0 .5-5.8 31.7 31.7 0 0 0-.5-5.8zM9.7 15.5V8.5L15.7 12l-6 3.5z"/></svg>
                    </a>
                    <a class="footer-social-link" href="https://www.instagram.com/carseeai/" target="_blank" rel="noopener noreferrer" title="Instagram — @carseeai" aria-label="Instagram @carseeai">
                        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7zm5 3.5A5.5 5.5 0 1 1 6.5 13 5.5 5.5 0 0 1 12 7.5zm0 2A3.5 3.5 0 1 0 15.5 13 3.5 3.5 0 0 0 12 9.5zm5.25-4a1.25 1.25 0 1 1-1.25 1.25A1.25 1.25 0 0 1 17.25 5.5z"/></svg>
                    </a>
                    <a class="footer-social-link" href="https://x.com/carseeai" target="_blank" rel="noopener noreferrer" title="X — @carseeai" aria-label="X @carseeai">
                        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M18.22 3h3.22l-7.04 8.04L22 21h-6.44l-5.04-6.6L5.5 21H2.28l7.53-8.6L2 3h6.59l4.56 6.02L18.22 3z"/></svg>
                    </a>
                    <a class="footer-social-link" href="https://www.facebook.com/carseeeai" target="_blank" rel="noopener noreferrer" title="Facebook — carseeeai" aria-label="Facebook carseeeai">
                        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 1 0-11.5 9.9v-7h-2v-3h2v-2.3c0-2 1.2-3.1 3-3.1.9 0 1.8.1 1.8.1v2h-1c-1 0-1.3.6-1.3 1.2V12h2.2l-.35 3H14.5v7A10 10 0 0 0 22 12z"/></svg>
                    </a>
                </nav>
            </div>
            <div class="footer-content">
                <div class="footer-section">
                    <h4>Product</h4>
                    <ul>
                        <li><a href="how-it-works/index.html">How it works</a></li>
                        <li><a href="pricing.html">Pricing</a></li>
                        <li><a href="blog/index.html">Blog</a></li>
                        <li><a href="benefits.html">Why CarSee?</a></li>
                        <li><a href="our-app.html">Our App</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Our Solutions Include</h4>
                    <ul>
                        <li><a href="solution/car-traders/index.html">Car Traders</a></li>
                        <li><a href="solution/rental-companies/index.html">Rental Companies</a></li>
                        <li><a href="solution/private-car-owners/index.html">Private Car Owners</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>About</h4>
                    <ul>
                        <li><a href="company/career/index.html">Career</a></li>
                        <li><a href="company/partners/index.html">Become a Partner</a></li>
                        <li><a href="contact/index.html">Contact us</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 CarSee. All right reserved.</p>
                <div class="footer-links">
                    <span class="legal-links">
                        <a href="privacy.html">Privacy Policy</a>
                        <span>·</span>
                        <a href="cookies.html">Cookies Policy</a>
                        <span>·</span>
                        <a href="terms.html">Terms of Service</a>
                        <span>·</span>
                        <a href="mailto:legal@carsee.app">Legal</a>
                    </span>
                    <a href="#" id="cookiesSettings">Cookies Settings</a>
                </div>
            </div>
        </div>
    </footer>'''

    return adjust_footer_paths(footer, prefix)

def create_arabic_footer(depth):
    """Create Arabic footer with adjusted paths."""
    prefix = get_path_prefix(depth)
    ar_logo_src = ("../" * (depth + 1)) + "assets/logos/logo_banner.png"
    footer = '''    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-brand-row">
                <a href="index.html" class="footer-logo-link" aria-label="CarSee home">
                    <img src="__AR_FOOTER_LOGO_SRC__" alt="CarSee" class="footer-logo-img" loading="lazy">
                </a>
                <nav class="footer-social" aria-label="Social media">
                    <a class="footer-social-link" href="https://www.youtube.com/@carseeai" target="_blank" rel="noopener noreferrer" title="YouTube — @carseeai" aria-label="YouTube @carseeai">
                        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.7 31.7 0 0 0 0 12a31.7 31.7 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1 31.7 31.7 0 0 0 .5-5.8 31.7 31.7 0 0 0-.5-5.8zM9.7 15.5V8.5L15.7 12l-6 3.5z"/></svg>
                    </a>
                    <a class="footer-social-link" href="https://www.instagram.com/carseeai/" target="_blank" rel="noopener noreferrer" title="Instagram — @carseeai" aria-label="Instagram @carseeai">
                        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7zm5 3.5A5.5 5.5 0 1 1 6.5 13 5.5 5.5 0 0 1 12 7.5zm0 2A3.5 3.5 0 1 0 15.5 13 3.5 3.5 0 0 0 12 9.5zm5.25-4a1.25 1.25 0 1 1-1.25 1.25A1.25 1.25 0 0 1 17.25 5.5z"/></svg>
                    </a>
                    <a class="footer-social-link" href="https://x.com/carseeai" target="_blank" rel="noopener noreferrer" title="X — @carseeai" aria-label="X @carseeai">
                        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M18.22 3h3.22l-7.04 8.04L22 21h-6.44l-5.04-6.6L5.5 21H2.28l7.53-8.6L2 3h6.59l4.56 6.02L18.22 3z"/></svg>
                    </a>
                    <a class="footer-social-link" href="https://www.facebook.com/carseeeai" target="_blank" rel="noopener noreferrer" title="Facebook — carseeeai" aria-label="Facebook carseeeai">
                        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 1 0-11.5 9.9v-7h-2v-3h2v-2.3c0-2 1.2-3.1 3-3.1.9 0 1.8.1 1.8.1v2h-1c-1 0-1.3.6-1.3 1.2V12h2.2l-.35 3H14.5v7A10 10 0 0 0 22 12z"/></svg>
                    </a>
                </nav>
            </div>
            <div class="footer-content">
                <div class="footer-section">
                    <h4>المنتج</h4>
                    <ul>
                        <li><a href="how-it-works/index.html">كيف يعمل</a></li>
                        <li><a href="pricing.html">الأسعار</a></li>
                        <li><a href="blog/index.html">المدونة</a></li>
                        <li><a href="benefits.html">لماذا CarSee؟</a></li>
                        <li><a href="our-app.html">تطبيقنا</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>حلولنا تشمل</h4>
                    <ul>
                        <li><a href="solution/car-traders/index.html">تجار السيارات</a></li>
                        <li><a href="solution/rental-companies/index.html">شركات التأجير</a></li>
                        <li><a href="solution/private-car-owners/index.html">أصحاب السيارات الخاصة</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>عن CarSee</h4>
                    <ul>
                        <li><a href="company/career/index.html">الوظائف</a></li>
                        <li><a href="company/partners/index.html">انضم كشريك</a></li>
                        <li><a href="contact/index.html">اتصل بنا</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 CarSee. جميع الحقوق محفوظة.</p>
                <div class="footer-links">
                    <span class="legal-links">
                        <a href="privacy.html">سياسة الخصوصية</a>
                        <span>·</span>
                        <a href="cookies.html">سياسة ملفات تعريف الارتباط</a>
                        <span>·</span>
                        <a href="terms.html">شروط الخدمة</a>
                        <span>·</span>
                        <a href="mailto:legal@carsee.app">قانوني</a>
                    </span>
                    <a href="#" id="cookiesSettings">إعدادات ملفات التعريف</a>
                </div>
            </div>
        </div>
    </footer>'''

    footer = footer.replace("__AR_FOOTER_LOGO_SRC__", ar_logo_src)
    return adjust_footer_paths(footer, prefix)

def find_footer(content):
    """Find the footer section in HTML content."""
    pattern = r'(\s*)<footer class="footer">.*?</footer>'
    match = re.search(pattern, content, re.DOTALL)
    return match

def update_html_file(file_path):
    """Update a single HTML file with the appropriate footer."""
    rel_path = file_path.relative_to(BASE_DIR)
    rel_path_str = str(rel_path).replace('\\', '/')

    # Check if file should be excluded
    if rel_path_str in EXCLUDE_FILES:
        return False, "Excluded"

    # Determine if Arabic or English
    is_arabic = rel_path_str.startswith('ar/')

    # Calculate depth
    if is_arabic:
        # For ar/ files, depth is parts - 2 (to account for 'ar' directory)
        depth = len(rel_path.parts) - 2
    else:
        depth = len(rel_path.parts) - 1

    # Read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Read error: {e}"

    # Find existing footer
    footer_match = find_footer(content)
    if not footer_match:
        return False, "No footer found"

    # Generate new footer
    if is_arabic:
        new_footer = create_arabic_footer(depth)
    else:
        new_footer = create_english_footer(depth)

    # Replace footer
    new_content = content[:footer_match.start()] + new_footer + content[footer_match.end():]

    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f"Updated (depth={depth}, {'AR' if is_arabic else 'EN'})"
    except Exception as e:
        return False, f"Write error: {e}"

def main():
    """Main function."""
    # Find all HTML files
    html_files = list(BASE_DIR.glob('**/*.html'))
    html_files.sort()

    print(f"Found {len(html_files)} HTML files\n")

    updated = 0
    skipped = 0
    errors = 0

    for file_path in html_files:
        rel_path = file_path.relative_to(BASE_DIR)
        success, message = update_html_file(file_path)

        if success:
            print(f"[OK] {rel_path}: {message}")
            updated += 1
        else:
            print(f"[SKIP] {rel_path}: {message}")
            if "Excluded" not in message:
                errors += 1
            else:
                skipped += 1

    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors:  {errors}")
    print(f"  Total:   {len(html_files)}")

if __name__ == '__main__':
    main()
