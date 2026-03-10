# Sistema Multilenguaje MetaChannelCorp

Sitio web corporativo bilingüe **(Español / English)** de **META Channel Corporation**, desplegado como sitio estático en Vercel a partir de una arquitectura WordPress + Docker + PHP-FPM.

---

## Acceso Rápido

| Entorno | URL | Idioma |
|---------|-----|--------|
| **Vercel — Español** | https://meta-channel-multilingual.vercel.app/es/ | Español |
| **Vercel — Inglés** | https://meta-channel-multilingual.vercel.app/en/ | Inglés |
| **Docker local — ES** | https://metachannelcorp.com | Español |
| **Docker local — EN** | https://metachannelcorp.com/en/ | Inglés |
| **Docker local — IE** | https://metachannelcorp.ie | → 301 a .com/en/ |
| **Panel Admin WP** | https://metachannelcorp.com/wp-admin/ | admin / admin123 |

---

## Tecnologías Utilizadas

| Tecnología | Versión | Rol |
|-----------|---------|-----|
| **WordPress** | 6.7.2 | CMS y gestión de contenido multiidioma |
| **PHP-FPM** | 8.2 | Procesamiento server-side (FastCGI) |
| **TranslatePress Free** | 3.1 | Plugin de traducción ES/EN |
| **Twenty Twenty-One** | 2.7 | Tema WordPress |
| **Nginx** | Alpine | Proxy inverso + SSL + redirección .ie |
| **MariaDB** | 10.11 | Base de datos relacional |
| **Docker** | 28.x | Containerización del entorno completo |
| **Docker Compose** | v2 | Orquestación de 3 servicios (db + wp + nginx) |
| **DockerHub** | — | Registro de imágenes custom (`jazzcode/*`) |
| **GitHub** | — | Control de versiones y distribución |
| **Vercel** | — | Hosting del sitio estático en producción |

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                          PRODUCCIÓN                         │
│                                                             │
│   https://meta-channel-multilingual.vercel.app/es/  (ES)   │
│   https://meta-channel-multilingual.vercel.app/en/  (EN)   │
│                             │                               │
│              Vercel Edge Network (CDN global)               │
│       Sitio estático: HTML + CSS + JS exportado de WP       │
│       SSL automático · hreflang es/en · sin backend PHP     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DESARROLLO LOCAL (Docker)                │
│                                                             │
│   metachannelcorp.com  (ES)  ·  metachannelcorp.com/en/ (EN)│
│   metachannelcorp.ie → 301 → metachannelcorp.com/en/        │
│                             │                               │
│        mcc_nginx  (nginx:alpine, puertos 80/443)            │
│        SSL autofirmado · HTTP→HTTPS · .ie→.com/en/ 301      │
│                             │  FastCGI :9000                │
│        mcc_wordpress  (jazzcode/mcc-wordpress:1.1)          │
│        WordPress 6.7 + PHP-FPM 8.2 + TranslatePress 3.1    │
│                             │  MySQL :3306                  │
│        mcc_db  (mariadb:10.11)                              │
│        DB: wordpress · wpuser / wppass                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Estructura del Repositorio

```
Sistema-Multilenguaje-MetaChannelCorp/
├── parte4-dockerhub/               # Imágenes Docker custom (DockerHub)
│   ├── docker-compose.yml          # Orquestación con jazzcode/* images
│   ├── wordpress-custom/
│   │   ├── Dockerfile
│   │   ├── docker-entrypoint-mcc.sh
│   │   └── wp-content/             # Plugins + temas + mcc-init.sql
│   ├── nginx-custom/
│   │   ├── Dockerfile
│   │   ├── default.conf            # .ie→301 + .com HTTPS config
│   │   └── generate-ssl-and-start.sh
│   └── README.md
│
├── meta-channel-multilingual/      # Entorno alternativo (imágenes oficiales)
│   ├── docker-compose.yml
│   ├── nginx/default.conf
│   └── ssl/
│
├── static-site/                    # Exportación estática para Vercel
│   ├── index.html                  # Español (raíz, para compatibilidad)
│   ├── es/                         # Español (subdirectorio explícito SEO)
│   │   ├── index.html
│   │   ├── nosotros/
│   │   └── contacto/
│   ├── en/                         # English
│   │   ├── index.html
│   │   ├── nosotros/
│   │   └── contacto/
│   ├── nosotros/index.html         # ES (compatibilidad con links internos)
│   ├── contacto/index.html
│   ├── css/                        # Estilos (Twenty Twenty-One + TranslatePress)
│   └── js/                         # Scripts (jQuery + navegación)
│
├── vercel.json                     # Configuración Vercel (rutas + headers)
├── GUIA-PRUEBAS.md                 # Paso a paso de verificación
├── build_es_paths.py               # Script generación /es/ paths
├── fix_html.py                     # Script limpieza HTML WordPress
├── fix_switcher.py                 # Script selector de idioma estático
└── .gitignore
```

---

## Imágenes en DockerHub

| Imagen | Descripción |
|--------|-------------|
| `jazzcode/mcc-wordpress:1.1` | WordPress 6.7 + PHP-FPM 8.2 + TranslatePress preconfigurado + BD inicializada |
| `jazzcode/mcc-nginx:1.1` | Nginx con SSL autofirmado. `.ie` hace 301 → `.com/en/`. `.com` sirve WordPress |

---

## Cómo Usar Este Repositorio

### A — Ver el sitio en Vercel (sin instalación)

```
https://meta-channel-multilingual.vercel.app/es/   ← Español
https://meta-channel-multilingual.vercel.app/en/   ← English
```

### B — Levantar entorno Docker local

**Requisitos:** Docker Desktop instalado.

**Paso 1 — /etc/hosts** (macOS/Linux):
```bash
sudo bash -c 'echo "127.0.0.1 metachannelcorp.com" >> /etc/hosts'
sudo bash -c 'echo "127.0.0.1 metachannelcorp.ie"  >> /etc/hosts'
```
Windows (Administrador): editar `C:\Windows\System32\drivers\etc\hosts` y añadir las mismas líneas.

**Paso 2 — Arrancar:**
```bash
git clone https://github.com/RobertGiantSteps/Sistema-Multilenguaje-MetaChannelCorp.git
cd Sistema-Multilenguaje-MetaChannelCorp/parte4-dockerhub
docker compose up -d
# Esperar 30–60 segundos en el primer arranque
```

**Paso 3 — Acceder:**
```
https://metachannelcorp.com          → Español (aceptar aviso SSL autofirmado)
https://metachannelcorp.com/en/      → English
https://metachannelcorp.ie           → 301 → .com/en/
https://metachannelcorp.com/wp-admin/ → admin / admin123
```

**Parar el entorno:**
```bash
docker compose down           # Solo detiene
docker compose down -v        # Detiene y borra la BD
```

---

