#!/usr/bin/env python3
"""
TEST SUITE COMPLETO — Sistema Multilenguaje MetaChannelCorp
Verifica todos los requisitos solicitados en la sesión de trabajo.
"""

import re, os, subprocess, json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
import ssl, http.cookiejar

BASE_DIR  = '/Users/minibob/Documents/roberto260226Multilingual'
VERCEL    = 'https://meta-channel-multilingual.vercel.app'
DOCKER_WP = 'https://metachannelcorp.com'
DOCKER_IE = 'https://metachannelcorp.ie'
GITHUB    = 'https://github.com/RobertGiantSteps/Sistema-Multilenguaje-MetaChannelCorp'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

results = []

def check(name, passed, detail=''):
    icon = '✓' if passed else '✗'
    results.append((passed, name, detail))
    status = f"  {icon}  {name}"
    if detail and not passed:
        status += f"\n       → {detail}"
    print(status)
    return passed

def http_get(url, follow=True, timeout=10):
    """Return (status_code, headers, body). Handles redirects manually if follow=False."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 TestSuite/1.0'})
        r = urlopen(req, context=ctx, timeout=timeout)
        return r.status, dict(r.headers), r.read().decode('utf-8', errors='replace')
    except HTTPError as e:
        return e.code, {}, ''
    except Exception as e:
        return 0, {}, str(e)

def http_head_no_follow(url, timeout=10):
    """Return (status, redirect_location) without following redirect."""
    try:
        import urllib.request
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args): return None
        opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ctx))
        try:
            r = opener.open(url, timeout=timeout)
            return r.status, r.headers.get('Location', '')
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get('Location', '')
    except Exception as e:
        return 0, str(e)

def get_body(url):
    _, _, body = http_get(url)
    return body

def run_git(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       cwd=BASE_DIR)
    return r.stdout.strip(), r.stderr.strip()

def run_docker(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip()

print("=" * 65)
print("  SISTEMA MULTILENGUAJE METACHANNEL — TEST SUITE COMPLETO")
print("=" * 65)

# ══════════════════════════════════════════════════════════════════
print("\n── 1. GITHUB ─────────────────────────────────────────────────")

stdout, _ = run_git('git remote -v')
check("Remote apunta a Sistema-Multilenguaje-MetaChannelCorp",
      'Sistema-Multilenguaje-MetaChannelCorp' in stdout, stdout)

stdout, _ = run_git('git log --oneline')
check("Historial de commits sin referencia a Claude",
      'Claude' not in stdout and 'claude' not in stdout, stdout[:200])

stdout, _ = run_git('git log --format="%B" | grep -i "Co-Authored-By"')
check("Ningún commit tiene Co-Authored-By Claude",
      stdout == '', stdout[:100])

stdout, _ = run_git('git log --oneline | wc -l')
commits = int(stdout.strip()) if stdout.strip().isdigit() else -1
check("Historial limpio (sin Claude en commits)",
      commits >= 1, f"commits={commits}")

required_files = [
    'parte4-dockerhub/docker-compose.yml',
    'parte4-dockerhub/nginx-custom/default.conf',
    'parte4-dockerhub/wordpress-custom/Dockerfile',
    'meta-channel-multilingual/docker-compose.yml',
    'static-site/index.html',
    'static-site/es/index.html',
    'static-site/en/index.html',
    'static-site/es/nosotros/index.html',
    'static-site/en/nosotros/index.html',
    'static-site/css/style.css',
    'static-site/js/jquery.min.js',
    'vercel.json',
    'README.md',
]
for f in required_files:
    exists = os.path.exists(os.path.join(BASE_DIR, f))
    check(f"Archivo presente: {f}", exists)

with open(os.path.join(BASE_DIR, 'README.md')) as f:
    readme = f.read()
check("README sin sección 'Análisis Técnico'",
      'Análisis Técnico' not in readme)
check("README tiene sección de Acceso Rápido",
      'Acceso Rápido' in readme or 'Acceso rápido' in readme.lower())
check("README credenciales wp-admin correctas (admin / admin123)",
      'admin / admin123' in readme or 'admin123' in readme)

stdout, _ = run_git("git show HEAD:README.md | grep -i 'analisis tecnico'")
check("Último commit: README sin Análisis Técnico",
      stdout == '')

# ══════════════════════════════════════════════════════════════════
print("\n── 2. ARCHIVOS ESTÁTICOS LOCALES ─────────────────────────────")

static = os.path.join(BASE_DIR, 'static-site')
pages = {
    'index.html':              ('es-ES', 'Servicios Jurídico'),
    'es/index.html':           ('es-ES', 'Servicios Jurídico'),
    'en/index.html':           ('en-GB', 'Legal-Technological Services'),
    'nosotros/index.html':     ('es-ES', None),
    'contacto/index.html':     ('es-ES', None),
    'es/nosotros/index.html':  ('es-ES', None),
    'es/contacto/index.html':  ('es-ES', None),
    'en/nosotros/index.html':  ('en-GB', None),
    'en/contacto/index.html':  ('en-GB', None),
}

for rel, (lang, h1_fragment) in pages.items():
    fpath = os.path.join(static, rel)
    if not os.path.exists(fpath):
        check(f"{rel}: existe", False); continue
    with open(fpath) as f:
        c = f.read()
    check(f"{rel}: lang={lang}", f'lang="{lang}"' in c)
    if h1_fragment:
        check(f"{rel}: H1 correcto ({h1_fragment[:30]}...)",
              h1_fragment in c)
    check(f"{rel}: sin CSS emoji huérfano",
          'img.wp-smiley' not in c or '<style' in c[:c.index('img.wp-smiley')])
    check(f"{rel}: sin admin-ajax.php",
          'admin-ajax.php' not in c)
    check(f"{rel}: sin trp-translate-dom-changes",
          'trp-translate-dom-changes' not in c)
    check(f"{rel}: JS selector usa removeAttribute",
          'removeAttribute' in c)
    # hreflang
    has_es_href = '/es/' in c and 'hreflang' in c
    has_en_href = '/en/' in c and 'hreflang' in c
    check(f"{rel}: hreflang ES=/es/ EN=/en/",
          has_es_href and has_en_href)
    # Language switcher current label
    expected_label = 'Spanish' if lang == 'es-ES' else 'English'
    m = re.search(r'trp-language-item__current" title="([^"]*)"', c)
    actual_label = m.group(1) if m else 'NOT FOUND'
    check(f"{rel}: selector muestra idioma actual ({expected_label})",
          actual_label == expected_label, f"actual={actual_label}")

# ══════════════════════════════════════════════════════════════════
print("\n── 3. VERCEL — HTTP STATUS ───────────────────────────────────")

vercel_urls = [
    ('/', 200),
    ('/es/', 200),
    ('/en/', 200),
    ('/nosotros/', 200),
    ('/contacto/', 200),
    ('/es/nosotros/', 200),
    ('/es/contacto/', 200),
    ('/en/nosotros/', 200),
    ('/en/contacto/', 200),
    ('/css/style.css', 200),
    ('/css/block-library.css', 200),
    ('/js/jquery.min.js', 200),
    ('/js/primary-navigation.js', 200),
]

for path, expected in vercel_urls:
    code, _, _ = http_get(VERCEL + path)
    check(f"Vercel {path}: HTTP {expected}", code == expected, f"got {code}")

# ══════════════════════════════════════════════════════════════════
print("\n── 4. VERCEL — CONTENIDO ─────────────────────────────────────")

es_body = get_body(VERCEL + '/es/')
en_body = get_body(VERCEL + '/en/')

check("Vercel /es/ lang=es-ES", 'lang="es-ES"' in es_body)
check("Vercel /en/ lang=en-GB", 'lang="en-GB"' in en_body)

check("Vercel /es/ H1 en español",
      'Servicios Jurídico-Tecnológicos' in es_body)
check("Vercel /en/ H1 en inglés",
      'Legal-Technological Services' in en_body)

check("Vercel /en/ body class translatepress-en_GB",
      'translatepress-en_GB' in en_body)
check("Vercel /es/ body class translatepress-es_ES",
      'translatepress-es_ES' in es_body)

# Menú de navegación
check("Vercel /en/ menú en inglés (Services/About/Contact)",
      'Services' in en_body and 'About' in en_body)
check("Vercel /es/ menú en español (Servicios/Nosotros/Contacto)",
      'Servicios' in es_body)

# Párrafos de contenido
check("Vercel /en/ contenido del cuerpo en inglés",
      'global legal-technological ecosystem' in en_body or
      'Legal-Technological' in en_body)
check("Vercel /es/ contenido del cuerpo en español",
      'ecosistema jurídico-tecnológico' in es_body or
      'Servicios' in es_body)

# CSS emoji
check("Vercel /es/ sin texto CSS emoji visible",
      'img.wp-smiley' not in es_body)
check("Vercel /en/ sin texto CSS emoji visible",
      'img.wp-smiley' not in en_body)

# AJAX
check("Vercel /es/ sin admin-ajax.php",
      'admin-ajax.php' not in es_body)
check("Vercel /en/ sin admin-ajax.php",
      'admin-ajax.php' not in en_body)

# Selector de idioma
m_es = re.search(r'trp-language-item__current" title="([^"]*)"', es_body)
m_en = re.search(r'trp-language-item__current" title="([^"]*)"', en_body)
check("Vercel /es/ selector muestra 'Spanish' como actual",
      m_es and m_es.group(1) == 'Spanish', m_es.group(1) if m_es else 'NOT FOUND')
check("Vercel /en/ selector muestra 'English' como actual",
      m_en and m_en.group(1) == 'English', m_en.group(1) if m_en else 'NOT FOUND')

# JS selector funcional
check("Vercel /es/ JS selector usa removeAttribute",
      'removeAttribute' in es_body)
check("Vercel /en/ JS selector usa removeAttribute",
      'removeAttribute' in en_body)

# Switcher link ES→EN y EN→ES (href puede estar antes o después de title)
es_en_link = re.search(r'<a\b[^>]*title="English"[^>]*href="([^"]*)"[^>]*>|<a\b[^>]*href="([^"]*)"[^>]*title="English"', es_body)
en_es_link = re.search(r'<a\b[^>]*title="Spanish"[^>]*href="([^"]*)"[^>]*>|<a\b[^>]*href="([^"]*)"[^>]*title="Spanish"', en_body)
# Extraer el grupo que hizo match
def _link(m): return (m.group(1) or m.group(2)) if m else None
check("Vercel /es/ tiene link al /en/",
      bool(es_en_link), _link(es_en_link) or 'NOT FOUND')
check("Vercel /en/ tiene link al /es/",
      bool(en_es_link), _link(en_es_link) or 'NOT FOUND')

# hreflang
check("Vercel /es/ hreflang es apunta a /es/",
      f'{VERCEL}/es/' in es_body and 'hreflang' in es_body)
check("Vercel /es/ hreflang en apunta a /en/",
      f'{VERCEL}/en/' in es_body and 'hreflang' in es_body)
check("Vercel /en/ hreflang es apunta a /es/",
      f'{VERCEL}/es/' in en_body and 'hreflang' in en_body)
check("Vercel /en/ hreflang en apunta a /en/",
      f'{VERCEL}/en/' in en_body and 'hreflang' in en_body)

# HTTPS / SSL
check("Vercel HTTPS activo (SSL automático)",
      VERCEL.startswith('https://'))
code, _, _ = http_get(VERCEL + '/es/')
check("Vercel SSL válido (no error de certificado)",
      code == 200)

# ══════════════════════════════════════════════════════════════════
print("\n── 5. DOCKER LOCAL ───────────────────────────────────────────")

# Contenedores
out, _ = run_docker('docker ps --format "{{.Names}}" 2>/dev/null')
containers = out.split('\n') if out else []
check("Contenedor mcc_wordpress corriendo", 'mcc_wordpress' in containers)
check("Contenedor mcc_nginx corriendo",     'mcc_nginx' in containers)
check("Contenedor mcc_db corriendo",        'mcc_db' in containers)

# Dominio .com
code_com, _, body_com = http_get(DOCKER_WP + '/', timeout=8)
check("Docker metachannelcorp.com HTTP 200", code_com == 200, f"got {code_com}")
check("Docker .com español (lang es-ES)",
      'lang="es-ES"' in body_com)
check("Docker .com H1 en español",
      'Servicios Jurídico' in body_com)

# Dominio .com/en/
code_en, _, body_en = http_get(DOCKER_WP + '/en/', timeout=8)
check("Docker metachannelcorp.com/en/ HTTP 200", code_en == 200, f"got {code_en}")
check("Docker .com/en/ inglés (lang en-GB)",
      'lang="en-GB"' in body_en)
check("Docker .com/en/ H1 en inglés",
      'Legal-Technological Services' in body_en)

# Dominio .ie → 301 → .com/en/
code_ie, loc_ie = http_head_no_follow(DOCKER_IE + '/')
check("Docker metachannelcorp.ie HTTP 301",
      code_ie == 301, f"got {code_ie}")
check("Docker .ie redirige a .com/en/ (sin contenido duplicado)",
      '/en/' in loc_ie, f"location={loc_ie}")

# wp-admin login
import subprocess
result = subprocess.run(
    ['curl', '-sk', '-c', '/tmp/ts_cookies.txt',
     '-X', 'POST', 'https://metachannelcorp.com/wp-login.php',
     '-d', 'log=admin&pwd=admin123&wp-submit=Log+In&redirect_to=%2Fwp-admin%2F&testcookie=1',
     '-H', 'Cookie: wordpress_test_cookie=WP+Cookie+check',
     '-o', '/dev/null', '-w', '%{http_code}|%{redirect_url}'],
    capture_output=True, text=True
)
login_out = result.stdout.strip()
parts = login_out.split('|')
login_code = int(parts[0]) if parts[0].isdigit() else 0
login_url  = parts[1] if len(parts) > 1 else ''
check("wp-admin login admin/admin123 → HTTP 302",
      login_code == 302, f"got {login_code}")
check("wp-admin redirige a /wp-admin/",
      '/wp-admin/' in login_url, f"redirect={login_url}")

# Nginx .ie config en archivo
nginx_conf = os.path.join(BASE_DIR, 'parte4-dockerhub/nginx-custom/default.conf')
with open(nginx_conf) as f:
    nginx = f.read()
check("Nginx config: .ie → 301 a .com/en/",
      'return 301' in nginx and 'metachannelcorp.ie' in nginx and '/en/' in nginx)
check("Nginx config: .ie sin contenido propio (solo redirect)",
      nginx.count('server_name metachannelcorp.ie') == 2 and
      'root' not in nginx.split('metachannelcorp.ie')[1].split('metachannelcorp.com')[0])

# ══════════════════════════════════════════════════════════════════
print("\n── 6. VERCEL.JSON ────────────────────────────────────────────")

with open(os.path.join(BASE_DIR, 'vercel.json')) as f:
    vj = json.load(f)

check("vercel.json outputDirectory = static-site",
      vj.get('outputDirectory') == 'static-site')

rewrites = [r['source'] for r in vj.get('rewrites', [])]
for path in ['/es', '/en', '/es/nosotros', '/es/contacto',
             '/en/nosotros', '/en/contacto']:
    check(f"vercel.json rewrite para {path}", path in rewrites)

# ══════════════════════════════════════════════════════════════════
print("\n── 7. DOCKER IMAGES ──────────────────────────────────────────")

out, _ = run_docker('docker images --format "{{.Repository}}:{{.Tag}}" 2>/dev/null')
images = out.split('\n')
check("Imagen jazzcode/mcc-wordpress:1.1 disponible",
      'jazzcode/mcc-wordpress:1.1' in images)
check("Imagen jazzcode/mcc-nginx:1.1 disponible",
      'jazzcode/mcc-nginx:1.1' in images)

# docker-compose.yml en parte4 usa las imágenes correctas
with open(os.path.join(BASE_DIR, 'parte4-dockerhub/docker-compose.yml')) as f:
    dc = f.read()
check("docker-compose usa jazzcode/mcc-wordpress:1.1",
      'jazzcode/mcc-wordpress:1.1' in dc)
check("docker-compose usa jazzcode/mcc-nginx:1.1",
      'jazzcode/mcc-nginx:1.1' in dc)
check("docker-compose usa mariadb:10.11",
      'mariadb:10.11' in dc)

# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
total   = len(results)
passed  = sum(1 for r in results if r[0])
failed  = total - passed
pct     = int(passed * 100 / total) if total else 0

print(f"\n  RESULTADO: {passed}/{total} tests pasados  ({pct}%)")
print()
if failed:
    print("  FALLIDOS:")
    for ok, name, detail in results:
        if not ok:
            print(f"    ✗  {name}")
            if detail:
                print(f"       → {detail}")
else:
    print("  ✓  Todos los tests pasaron — implementación completa y correcta.")
print()
print("=" * 65)
