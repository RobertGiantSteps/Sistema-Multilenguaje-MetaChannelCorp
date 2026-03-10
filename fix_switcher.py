#!/usr/bin/env python3
"""
Inject minimal language switcher JS into all HTML pages.
TranslatePress JS was removed to prevent failed AJAX calls.
This replaces it with a pure static implementation.
"""
import re
import os

# Minimal JS: handles dropdown toggle without WordPress/AJAX dependency
LANG_SWITCHER_JS = '''<script>
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.querySelector('.trp-language-item__current');
    var list = document.getElementById('trp-switcher-dropdown-list');
    if(!btn || !list) return;
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      list.style.display = open ? 'none' : 'block';
    });
    document.addEventListener('click', function(){
      btn.setAttribute('aria-expanded', 'false');
      list.style.display = 'none';
    });
  });
})();
</script>'''

# CSS to ensure dropdown is hidden by default (in case trp-switcher.css doesn't cover it)
LANG_SWITCHER_CSS = '''<style>
#trp-switcher-dropdown-list { display: none; }
.trp-language-item__current { cursor: pointer; }
</style>'''

base = '/Users/minibob/Documents/roberto260226Multilingual/static-site'

html_files = [
    'index.html',
    'nosotros/index.html',
    'contacto/index.html',
    'en/index.html',
    'en/nosotros/index.html',
    'en/contacto/index.html',
]

print("=== Injecting static language switcher ===")
for rel_path in html_files:
    full_path = os.path.join(base, rel_path)
    if not os.path.exists(full_path):
        print(f"  SKIP (not found): {rel_path}")
        continue

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS + JS just before </head>
    if '</head>' in content:
        injection = LANG_SWITCHER_CSS + '\n' + LANG_SWITCHER_JS + '\n'
        content = content.replace('</head>', injection + '</head>', 1)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Injected: {rel_path}")
    else:
        print(f"  ✗ No </head> found: {rel_path}")

print("\n=== Verifying language switcher links ===")
for rel_path in ['en/index.html', 'index.html']:
    full_path = os.path.join(base, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    switcher_links = re.findall(r'<a[^>]*class="trp-language-item"[^>]*href="([^"]*)"', content)
    current = re.findall(r'title="([^"]*)"[^>]*aria-expanded', content)
    print(f"  {rel_path}: current={current}, switch links={switcher_links}")

print("\nDone!")
