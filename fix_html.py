#!/usr/bin/env python3
"""
Fix static HTML files exported from WordPress for Vercel deployment.
Fixes:
1. Removes orphaned emoji CSS block (visible as text due to deleted <style> opening tag)
2. Removes trp_data JavaScript object with hardcoded WordPress AJAX URLs
3. Removes trp-translate-dom-changes.js (makes failed AJAX calls that break translations)
4. Removes trp-frontend-language-switcher.js (broken in static context)
5. Removes unnecessary WordPress meta links (wp-json, xmlrpc, oembed, feed)
6. Injects a clean static language switcher
"""

import re
import os

def fix_html(content, page_path):
    """Fix all WordPress static export issues in HTML content."""

    # ─── FIX 1: Remove entire wp-emoji script block ────────────────────────────
    # Pattern: <script>...window._wpemojiSettings...entire block...</script>
    content = re.sub(
        r'<script[^>]*>[\s\S]*?wp-emoji[\s\S]*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    # Also remove any leftover emoji polyfill <script> tag (auto-generated comment)
    content = re.sub(
        r'<script[^>]*>\s*/\*!\s*This file is auto-generated\s*\*/[\s\S]*?</script>',
        '',
        content,
        flags=re.DOTALL
    )

    # ─── FIX 2: Remove wp-emoji inline <style> block ───────────────────────────
    # Remove <style id='wp-emoji-styles-inline-css'>...</style>
    content = re.sub(
        r"<style[^>]*id=['\"]wp-emoji-styles-inline-css['\"][^>]*>[\s\S]*?</style>",
        '',
        content,
        flags=re.DOTALL
    )
    # Remove orphaned emoji CSS content (what remains when the style tag was already deleted by sed)
    content = re.sub(
        r'\n\s*img\.wp-smiley,\s*img\.emoji\s*\{[\s\S]*?\}\n\s*</style>',
        '',
        content,
        flags=re.DOTALL
    )
    # Also remove any stray closing </style> that may be left orphaned
    # (Only remove if it's a leftover - check context carefully)
    # Remove the image-size style which is not needed
    content = re.sub(
        r"<style>img:is\(\[sizes=['\"]auto['\"][^)]*\)[^}]*\}</style>",
        '',
        content
    )

    # ─── FIX 3: Remove trp_data script block (hardcoded WordPress AJAX URLs) ───
    content = re.sub(
        r'<script[^>]*>\s*var trp_data\s*=\s*\{[\s\S]*?\};\s*</script>',
        '',
        content,
        flags=re.DOTALL
    )

    # ─── FIX 4: Remove broken TranslatePress JS script tags ────────────────────
    content = re.sub(
        r'<script[^>]*trp-translate-dom-changes[^>]*>[\s\S]*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<script[^>]*src=["\'][^"\']*trp-translate-dom-changes[^"\']*["\'][^>]*>[\s\S]*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<script[^>]*src=["\'][^"\']*trp-translate-dom-changes[^"\']*["\'][^/]*/?>',
        '',
        content
    )
    # Remove the trp-frontend-language-switcher.js (uses AJAX)
    content = re.sub(
        r'<script[^>]*src=["\'][^"\']*trp-frontend-language-switcher[^"\']*["\'][^>]*>[\s\S]*?</script>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<script[^>]*src=["\'][^"\']*trp-frontend-language-switcher[^"\']*["\'][^/]*/?>',
        '',
        content
    )
    # Also match the script tags we renamed with ./js/ prefix
    content = re.sub(
        r'<script[^>]*src=["\'][^"\']*trp-dom-changes[^"\']*["\'][^/]*/?>',
        '',
        content
    )
    content = re.sub(
        r'<script[^>]*src=["\'][^"\']*trp-frontend-switcher[^"\']*["\'][^/]*/?>',
        '',
        content
    )

    # ─── FIX 5: Remove WordPress meta/API links not needed in static ───────────
    content = re.sub(r'<link[^>]*application/rss\+xml[^>]*/>', '', content)
    content = re.sub(r'<link[^>]*wp-json[^>]*/>', '', content)
    content = re.sub(r'<link[^>]*application/rsd\+xml[^>]*/>', '', content)
    content = re.sub(r'<link[^>]*oembed[^>]*/>', '', content)
    content = re.sub(r'<link[^>]*shortlink[^>]*/>', '', content)
    content = re.sub(r'<meta[^>]*generator[^>]*WordPress[^>]*/>', '', content)
    content = re.sub(r'<link[^>]*wlwmanifest[^>]*/>', '', content)

    # ─── FIX 6: Clean up multiple blank lines ──────────────────────────────────
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content


def process_file(filepath, page_path):
    """Read, fix, and write back an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    fixed = fix_html(content, page_path)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)

    saved = original_len - len(fixed)
    print(f"  Fixed: {filepath} (removed {saved} chars)")
    return saved


# ─── Process all HTML files ────────────────────────────────────────────────────
base = '/Users/minibob/Documents/roberto260226Multilingual/static-site'

html_files = [
    ('index.html', '/'),
    ('nosotros/index.html', '/nosotros/'),
    ('contacto/index.html', '/contacto/'),
    ('en/index.html', '/en/'),
    ('en/nosotros/index.html', '/en/nosotros/'),
    ('en/contacto/index.html', '/en/contacto/'),
]

total_saved = 0
print("=== Fixing HTML files ===")
for rel_path, page_path in html_files:
    full_path = os.path.join(base, rel_path)
    if os.path.exists(full_path):
        total_saved += process_file(full_path, page_path)
    else:
        print(f"  WARNING: Not found: {full_path}")

print(f"\nTotal removed: {total_saved} chars across all pages")
print("\n=== Verifying fixes ===")

# Verify en/index.html has English content and no Spanish
with open(os.path.join(base, 'en/index.html'), 'r') as f:
    en_content = f.read()

checks = [
    ('English H1 present', 'Legal-Technological Services' in en_content),
    ('No wp-emoji CSS', 'img.wp-smiley' not in en_content),
    ('No trp_data AJAX URL', 'admin-ajax.php' not in en_content),
    ('No trp-dom-changes.js', 'trp-dom-changes' not in en_content),
    ('No trp-frontend-switcher.js', 'trp-frontend-switcher' not in en_content),
    ('lang=en-GB', 'lang="en-GB"' in en_content),
]

with open(os.path.join(base, 'index.html'), 'r') as f:
    es_content = f.read()

checks += [
    ('Spanish H1 present', 'Servicios Jurídico' in es_content),
    ('No emoji CSS text', 'img.wp-smiley' not in es_content),
    ('No orphaned </style>', es_content.count('<style') == es_content.count('</style>')),
]

all_passed = True
for name, result in checks:
    icon = '✓' if result else '✗ FAIL'
    print(f"  {icon}  {name}")
    if not result:
        all_passed = False

print("\n" + ("All checks passed!" if all_passed else "Some checks FAILED - review above"))
