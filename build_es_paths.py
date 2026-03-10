#!/usr/bin/env python3
"""
Create /es/ directory structure in static site.
- Copies Spanish pages (root) to /es/ with corrected relative paths
- Updates ALL pages with correct hreflang (es -> /es/, en -> /en/)
- Updates language switcher links in all pages
"""

import re
import os
import shutil

base = '/Users/minibob/Documents/roberto260226Multilingual/static-site'

# ─── Step 1: Create /es/ pages from root Spanish pages ────────────────────────
print("=== Step 1: Creating /es/ pages ===")

pages_to_copy = [
    ('index.html',            'es/index.html'),
    ('nosotros/index.html',   'es/nosotros/index.html'),
    ('contacto/index.html',   'es/contacto/index.html'),
]

for src_rel, dst_rel in pages_to_copy:
    src = os.path.join(base, src_rel)
    dst = os.path.join(base, dst_rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine depth of destination for relative paths
    # es/index.html → depth 1 → prefix = ../
    # es/nosotros/index.html → depth 2 → prefix = ../../
    depth = dst_rel.count('/') - 1  # es/x = 1 slash → depth 1
    prefix = '../' * (depth + 1)    # es/ needs '../', es/nosotros/ needs '../../'

    # Update relative paths that use './' (root-relative) to use prefix
    # CSS/JS references
    content = content.replace("href='./css/", f"href='{prefix}css/")
    content = content.replace('href="./css/', f'href="{prefix}css/')
    content = content.replace("href='./js/",  f"href='{prefix}js/")
    content = content.replace('href="./js/',  f'href="{prefix}js/')
    content = content.replace("src='./js/",   f"src='{prefix}js/")
    content = content.replace('src="./js/',   f'src="{prefix}js/')
    content = content.replace("src=\"./js/",  f'src="{prefix}js/')

    # Internal navigation links in Spanish pages (./nosotros/ etc)
    content = content.replace('href="./"',         f'href="{prefix[:-1] or "."}/"')
    content = content.replace("href='./'",         f"href='{prefix[:-1] or '.'}/'")
    content = content.replace('href="./nosotros/"', f'href="{prefix}es/nosotros/"')
    content = content.replace('href="./contacto/"', f'href="{prefix}es/contacto/"')
    content = content.replace("href='./nosotros/'", f"href='{prefix}es/nosotros/'")
    content = content.replace("href='./contacto/'", f"href='{prefix}es/contacto/'")

    # Fix canonical and hreflang
    # es/index.html: canonical → /es/, hreflang es → /es/, hreflang en → /en/
    content = re.sub(
        r'<link rel="canonical"[^/]*/?>',
        f'<link rel="canonical" href="{prefix}es/" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="es-ES" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="es-ES" href="{prefix}es/" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="es" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="es" href="{prefix}es/" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="en-GB" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="en-GB" href="{prefix}en/" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="en" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="en" href="{prefix}en/" />',
        content
    )

    # Language switcher: English link should go to /en/ (same depth as /es/)
    content = content.replace(
        f'<a href="{prefix}en/" class="trp-language-item"',
        f'<a href="{prefix}en/" class="trp-language-item"'
    )
    # From /es/ the English link should go to ../../en/ (up 2, then en/)
    # es/index.html → ../en/ (1 up from es/ → root, then en/)
    # es/nosotros/index.html → ../../en/ (2 up → root, then en/)
    # Replace any ./en/ links with the correct relative path
    content = content.replace('href="./en/"', f'href="{prefix}en/"')
    content = content.replace("href='./en/'", f"href='{prefix}en/'")

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {dst_rel}")


# ─── Step 2: Update hreflang in ALL pages (root + en/ + es/) ──────────────────
print("\n=== Step 2: Updating hreflang in all pages ===")

def fix_hreflang(content, es_path, en_path):
    """Update hreflang and canonical to use explicit /es/ and /en/ paths."""
    content = re.sub(
        r'<link rel="alternate" hreflang="es-ES" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="es-ES" href="{es_path}" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="es" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="es" href="{es_path}" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="en-GB" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="en-GB" href="{en_path}" />',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="en" href="[^"]*"[^/]*/?>',
        f'<link rel="alternate" hreflang="en" href="{en_path}" />',
        content
    )
    return content

def fix_language_switcher(content, es_url, en_url, current_lang):
    """Update language switcher links to use explicit language URLs."""
    if current_lang == 'es':
        # On ES page, English link should go to en_url, remove Spanish link (it's current)
        content = re.sub(
            r'<a href="[^"]*" class="trp-language-item" title="English"[^>]*>',
            f'<a href="{en_url}" class="trp-language-item" title="English" data-no-translation>',
            content
        )
    else:
        # On EN page, Spanish link should go to es_url
        content = re.sub(
            r'<a href="[^"]*" class="trp-language-item" title="Spanish"[^>]*>',
            f'<a href="{es_url}" class="trp-language-item" title="Spanish" data-no-translation>',
            content
        )
    return content

# Define all pages with their hreflang absolute paths and switcher URLs
# Using absolute production URLs for hreflang (best practice)
PROD = 'https://meta-channel-multilingual.vercel.app'

all_pages = [
    # (file, es_hreflang, en_hreflang, es_switcher_url, en_switcher_url, current_lang)
    ('index.html',              f'{PROD}/es/',           f'{PROD}/en/',           './es/',     './en/',     'es'),
    ('nosotros/index.html',     f'{PROD}/es/nosotros/',  f'{PROD}/en/nosotros/',  '../es/',    '../en/',    'es'),
    ('contacto/index.html',     f'{PROD}/es/contacto/',  f'{PROD}/en/contacto/',  '../es/',    '../en/',    'es'),
    ('en/index.html',           f'{PROD}/es/',           f'{PROD}/en/',           '../es/',    './',        'en'),
    ('en/nosotros/index.html',  f'{PROD}/es/nosotros/',  f'{PROD}/en/nosotros/',  '../../es/', './',        'en'),
    ('en/contacto/index.html',  f'{PROD}/es/contacto/',  f'{PROD}/en/contacto/',  '../../es/', './',        'en'),
    ('es/index.html',           f'{PROD}/es/',           f'{PROD}/en/',           './',        '../en/',    'es'),
    ('es/nosotros/index.html',  f'{PROD}/es/nosotros/',  f'{PROD}/en/nosotros/',  './',        '../../en/', 'es'),
    ('es/contacto/index.html',  f'{PROD}/es/contacto/',  f'{PROD}/en/contacto/',  './',        '../../en/', 'es'),
]

for (file, es_href, en_href, es_sw, en_sw, lang) in all_pages:
    fpath = os.path.join(base, file)
    if not os.path.exists(fpath):
        print(f"  SKIP: {file}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = fix_hreflang(content, es_href, en_href)
    content = fix_language_switcher(content, es_sw, en_sw, lang)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Fixed: {file}")


# ─── Step 3: Add /es/ redirect in vercel.json ─────────────────────────────────
print("\n=== Step 3: Done - also need vercel.json update ===")
print("Remember to update vercel.json with /es/ routes")

# ─── Verify ───────────────────────────────────────────────────────────────────
print("\n=== Verification ===")
checks = [
    ('es/index.html exists', os.path.exists(os.path.join(base, 'es/index.html'))),
    ('es/nosotros/index.html exists', os.path.exists(os.path.join(base, 'es/nosotros/index.html'))),
    ('es/contacto/index.html exists', os.path.exists(os.path.join(base, 'es/contacto/index.html'))),
]

# Check hreflang in root index.html
with open(os.path.join(base, 'index.html'), 'r') as f:
    idx = f.read()
checks += [
    ('Root hreflang es → /es/', f'{PROD}/es/' in idx),
    ('Root hreflang en → /en/', f'{PROD}/en/' in idx),
    ('Root switcher EN link', './en/' in idx),
]

with open(os.path.join(base, 'en/index.html'), 'r') as f:
    en_idx = f.read()
checks += [
    ('EN page hreflang es → /es/', f'{PROD}/es/' in en_idx),
    ('EN page switcher ES link', '../es/' in en_idx),
]

with open(os.path.join(base, 'es/index.html'), 'r') as f:
    es_idx = f.read()
es_h1 = re.search(r'<h1[^>]*class="wp-block-heading"[^>]*>([^<]*)</h1>', es_idx)
checks += [
    ('ES page has Spanish H1', 'Servicios' in (es_h1.group(0) if es_h1 else '')),
    ('ES page hreflang es → /es/', f'{PROD}/es/' in es_idx),
]

all_ok = True
for name, result in checks:
    icon = '✓' if result else '✗ FAIL'
    print(f"  {icon}  {name}")
    if not result:
        all_ok = False

print('\n' + ('All checks passed!' if all_ok else 'Some checks FAILED'))
