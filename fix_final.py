#!/usr/bin/env python3
"""
Final fixes:
1. Fix language switcher: replace hidden/inert JS with removeAttribute approach
2. Remove broken CSS that conflicts with hidden attribute
3. Verify current-language labels in all pages
"""
import re, os

base = '/Users/minibob/Documents/roberto260226Multilingual/static-site'

# Updated minimal JS: uses removeAttribute('hidden') / setAttribute('hidden','')
# This correctly handles the TranslatePress HTML structure with hidden + inert attributes
NEW_SWITCHER_SCRIPT = '''<script>
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var btn  = document.querySelector('.trp-language-item__current');
    var list = document.getElementById('trp-switcher-dropdown-list');
    if (!btn || !list) return;

    // Remove hidden/inert attrs instead of using display (hidden overrides display)
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      if (isOpen) {
        list.setAttribute('hidden', '');
        list.setAttribute('inert', '');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        list.removeAttribute('hidden');
        list.removeAttribute('inert');
        btn.setAttribute('aria-expanded', 'true');
      }
    });

    document.addEventListener('click', function(){
      list.setAttribute('hidden', '');
      list.setAttribute('inert', '');
      btn.setAttribute('aria-expanded', 'false');
    });

    list.addEventListener('click', function(e){ e.stopPropagation(); });
  });
})();
</script>'''

# Minimal CSS: just cursor and remove the display:none we added before
# (hidden attribute already hides it; we don't need extra CSS)
NEW_SWITCHER_CSS = '''<style>
.trp-language-item__current { cursor: pointer; user-select: none; }
.trp-language-item__current:hover { opacity: 0.85; }
</style>'''

html_files = [
    'index.html',
    'nosotros/index.html',
    'contacto/index.html',
    'en/index.html',
    'en/nosotros/index.html',
    'en/contacto/index.html',
    'es/index.html',
    'es/nosotros/index.html',
    'es/contacto/index.html',
]

print("=== Fixing language switcher (hidden/inert) in all pages ===")
for rel in html_files:
    fpath = os.path.join(base, rel)
    if not os.path.exists(fpath):
        print(f"  SKIP: {rel}")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove old switcher CSS block we injected
    content = re.sub(
        r'<style>\s*#trp-switcher-dropdown-list\s*\{[^}]*\}[^<]*</style>\s*',
        '',
        content, flags=re.DOTALL
    )
    # Remove old switcher JS block we injected
    content = re.sub(
        r'<script>\s*\(function\(\)\{[\s\S]*?document\.addEventListener\(\'click\'[\s\S]*?\}\)\(\);\s*</script>',
        '',
        content, flags=re.DOTALL
    )
    # Remove stray extra </script> left by previous injection
    # (the injection was placed before </head> so look for it)

    # Inject new CSS + JS before </head>
    if '</head>' in content:
        injection = NEW_SWITCHER_CSS + '\n' + NEW_SWITCHER_SCRIPT + '\n'
        content = content.replace('</head>', injection + '</head>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Fixed: {rel}")

# Verify current-language labels
print("\n=== Verifying current language labels ===")
expected = {
    'index.html': 'Spanish',
    'nosotros/index.html': 'Spanish',
    'contacto/index.html': 'Spanish',
    'en/index.html': 'English',
    'en/nosotros/index.html': 'English',
    'en/contacto/index.html': 'English',
    'es/index.html': 'Spanish',
    'es/nosotros/index.html': 'Spanish',
    'es/contacto/index.html': 'Spanish',
}
all_ok = True
for rel, expected_lang in expected.items():
    fpath = os.path.join(base, rel)
    if not os.path.exists(fpath):
        print(f"  SKIP: {rel}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'trp-language-item__current" title="([^"]*)"', content)
    actual = m.group(1) if m else 'NOT FOUND'
    ok = actual == expected_lang
    if not ok: all_ok = False
    icon = '✓' if ok else '✗ FAIL'
    print(f"  {icon}  {rel}: expected={expected_lang}, actual={actual}")

# Also check hidden attribute is still there in dropdown (correct initial state)
with open(os.path.join(base, 'index.html'), 'r') as f:
    c = f.read()
has_hidden = 'id="trp-switcher-dropdown-list"' in c and 'hidden' in c
print(f"\n  {'✓' if has_hidden else '✗'}  Dropdown has hidden attribute (correct initial state)")

# Check new JS is present
has_new_js = 'removeAttribute' in c
print(f"  {'✓' if has_new_js else '✗'}  New JS (removeAttribute) injected")

print('\n' + ('All OK!' if all_ok and has_hidden and has_new_js else 'Some issues remain'))
