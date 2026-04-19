#!/usr/bin/env python3
"""
Script to update all HTML files with cookie consent functionality.
Handles both English and Arabic files with appropriate relative paths.
"""

import os
import re
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.resolve()

# Files to update (English)
ENGLISH_FILES = [
    "blog/index.html",
    "clients/dealerships/index.html",
    "clients/insurers-experts/index.html",
    "clients/leasing/index.html",
    "clients/oem/index.html",
    "clients/rental-cars-car-sharing/index.html",
    "clients/software-publishers/index.html",
    "clients/uv-marketplaces/index.html",
    "company/career/index.html",
    "company/partners/index.html",
    "contact/index.html",
    "demo/index.html",
    "how-it-works/index.html",
    "privacy.html",
    "pricing.html",
    "terms.html",
    "technology/index.html",
    "our-app.html",
    "benefits.html",
    "solution/car-traders/index.html",
    "solution/car-fleet/index.html",
    "solution/inspection/index.html",
    "solution/on-site-trade-in/index.html",
    "solution/remarkeeting/index.html",
    "solution/remote-trade-in/index.html",
    "solution/rental-companies/index.html",
    "solution/private-car-owners/index.html",
]

# Arabic files - will be determined dynamically
ARABIC_FILES = [
    "ar/blog/index.html",
    "ar/clients/dealerships/index.html",
    "ar/clients/insurers-experts/index.html",
    "ar/clients/leasing/index.html",
    "ar/clients/oem/index.html",
    "ar/clients/rental-cars-car-sharing/index.html",
    "ar/clients/software-publishers/index.html",
    "ar/clients/uv-marketplaces/index.html",
    "ar/company/career/index.html",
    "ar/company/partners/index.html",
    "ar/contact/index.html",
    "ar/demo/index.html",
    "ar/how-it-works/index.html",
    "ar/privacy.html",
    "ar/pricing.html",
    "ar/terms.html",
    "ar/technology/index.html",
    "ar/our-app.html",
    "ar/benefits.html",
    "ar/solution/car-traders/index.html",
    "ar/solution/car-fleet/index.html",
    "ar/solution/inspection/index.html",
    "ar/solution/on-site-trade-in/index.html",
    "ar/solution/remarketing/index.html",
    "ar/solution/remote-trade-in/index.html",
    "ar/solution/rental-companies/index.html",
    "ar/solution/private-car-owners/index.html",
]


def get_depth(file_path):
    """Calculate directory depth of the file."""
    # Remove leading filename, count slashes
    parts = file_path.split('/')
    return len(parts) - 1


def get_relative_paths(file_path, is_arabic=False):
    """
    Calculate relative paths for a given file location.
    Returns (css_path, cookies_html_path, js_path)
    """
    depth = get_depth(file_path)

    if is_arabic:
        # Arabic files are always in ar/ directory
        # So always one level up from ar/
        css_path = "../css/cookies.css"
        cookies_html_path = "cookies.html"
        js_path = "../js/cookies.js"
    else:
        # English files
        if depth == 0:  # Root level files like privacy.html, pricing.html, terms.html, our-app.html, benefits.html
            css_path = "css/cookies.css"
            cookies_html_path = "cookies.html"
            js_path = "js/cookies.js"
        elif depth == 1:  # Files like blog/index.html, contact/index.html, etc.
            css_path = "../css/cookies.css"
            cookies_html_path = "../cookies.html"
            js_path = "../js/cookies.js"
        else:  # depth >= 2, Files like clients/dealerships/index.html
            css_path = "../../css/cookies.css"
            cookies_html_path = "../../cookies.html"
            js_path = "../../js/cookies.js"

    return css_path, cookies_html_path, js_path


def file_already_has_cookies_js(content):
    """Check if file already has cookies.js script."""
    return 'cookies.js' in content


def file_already_has_cookies_css(content):
    """Check if file already has cookies.css link."""
    return 'cookies.css' in content


def file_already_has_cookies_settings_id(content):
    """Check if Cookies Settings link already has the id."""
    return 'id="cookiesSettings"' in content


def add_css_link(content, css_path):
    """Add CSS link to head section if not already present."""
    if file_already_has_cookies_css(content):
        return content, False

    # Find the last </link> or stylesheet link before </head>
    # Look for the last CSS link
    css_link_pattern = r'(<link[^>]*rel="stylesheet"[^>]*>)'
    matches = list(re.finditer(css_link_pattern, content))

    if matches:
        last_match = matches[-1]
        insert_pos = last_match.end()
        css_tag = f'\n    <link rel="stylesheet" href="{css_path}">'
        return content[:insert_pos] + css_tag + content[insert_pos:], True
    else:
        # Fallback: insert before </head>
        head_close = content.find('</head>')
        if head_close != -1:
            css_tag = f'    <link rel="stylesheet" href="{css_path}">\n    '
            return content[:head_close] + css_tag + content[head_close:], True

    return content, False


def add_cookies_settings_id(content):
    """Add id="cookiesSettings" to the Cookies Settings link."""
    if file_already_has_cookies_settings_id(content):
        return content, False

    # Look for <a href="#">Cookies Settings</a>
    pattern = r'<a\s+href="#"\s*>\s*Cookies\s+Settings\s*</a>'
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        replacement = '<a href="#" id="cookiesSettings">Cookies Settings</a>'
        return content[:match.start()] + replacement + content[match.end():], True

    return content, False


def add_cookies_policy_link(content, cookies_html_path, is_arabic=False):
    """Add Cookies Policy link after Privacy Policy link."""
    privacy_pattern = r'<a\s+href="[^"]*privacy\.html"\s*>\s*Privacy\s+Policy\s*</a>'
    match = re.search(privacy_pattern, content, re.IGNORECASE)

    if match:
        # Check if Cookies Policy link already exists
        if 'href="' + cookies_html_path + '"' in content and 'Cookies' in content:
            return content, False

        # Determine if there's a separator after the Privacy Policy link
        insert_pos = match.end()
        following_text = content[insert_pos:insert_pos+50]

        # Add the Cookies Policy link
        if is_arabic:
            cookies_text = "سياسة ملفات التعريف"
        else:
            cookies_text = "Cookies Policy"

        # Check what comes after - might be a span separator
        if '<span>' in following_text or '<span ' in following_text:
            cookies_link = f'<span>·</span>\n                        <a href="{cookies_html_path}">سياسة ملفات التعريف</a>'
        else:
            cookies_link = f'\n                        <span>·</span>\n                        <a href="{cookies_html_path}">{cookies_text}</a>'

        return content[:insert_pos] + cookies_link + content[insert_pos:], True

    return content, False


def add_js_script(content, js_path):
    """Add cookies.js script before closing body tag."""
    if file_already_has_cookies_js(content):
        return content, False

    # Find the last </body> tag
    body_close = content.rfind('</body>')
    if body_close == -1:
        return content, False

    # Insert before </body>
    script_tag = f'    <script src="{js_path}"></script>\n'
    return content[:body_close] + script_tag + content[body_close:], True


def update_file(file_path):
    """Update a single HTML file with cookie consent functionality."""
    full_path = BASE_DIR / file_path

    if not full_path.exists():
        return False, f"File not found: {file_path}"

    # Determine if this is an Arabic file
    is_arabic = file_path.startswith('ar/')

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"

    # Get relative paths
    css_path, cookies_html_path, js_path = get_relative_paths(file_path, is_arabic)

    changes = []

    # Add CSS link
    new_content, added = add_css_link(content, css_path)
    if added:
        changes.append("CSS link")
    content = new_content

    # Add Cookies Settings ID
    new_content, added = add_cookies_settings_id(content)
    if added:
        changes.append("Cookies Settings ID")
    content = new_content

    # Add Cookies Policy link
    new_content, added = add_cookies_policy_link(content, cookies_html_path, is_arabic)
    if added:
        changes.append("Cookies Policy link")
    content = new_content

    # Add JS script
    new_content, added = add_js_script(content, js_path)
    if added:
        changes.append("JS script")
    content = new_content

    # Write back to file
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return False, f"Error writing file: {e}"

    if changes:
        return True, f"Updated: {', '.join(changes)}"
    else:
        return True, "Already up to date"


def main():
    """Main function to update all files."""
    all_files = ENGLISH_FILES + ARABIC_FILES

    print("=" * 80)
    print("CARSEE COOKIE CONSENT UPDATE SCRIPT")
    print("=" * 80)
    print(f"\nProcessing {len(all_files)} files...\n")

    successful = []
    failed = []

    for file_path in sorted(all_files):
        success, message = update_file(file_path)

        status = "✓" if success else "✗"
        print(f"{status} {file_path:<60} {message}")

        if success:
            successful.append(file_path)
        else:
            failed.append((file_path, message))

    print("\n" + "=" * 80)
    print(f"SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {len(all_files)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed files:")
        for file_path, error in failed:
            print(f"  - {file_path}: {error}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
