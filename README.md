# Sistema Multilenguaje MetaChannelCorp

Sitio web corporativo bilingüe (Español / English) de **META Channel Corporation**, desplegado como sitio estático en Vercel a partir de una arquitectura WordPress + Docker.

---

## Tecnologías Utilizadas

| Tecnología | Versión | Rol |
|-----------|---------|-----|
| **WordPress** | 6.7.2 | CMS y gestión de contenido |
| **PHP-FPM** | 8.2 | Procesamiento del lado servidor |
| **TranslatePress** | 3.1 | Plugin de traducción ES/EN |
| **Twenty Twenty-One** | 2.7 | Tema de WordPress |
| **Nginx** | Alpine | Servidor web + proxy inverso + SSL |
| **MariaDB** | 10.11 | Base de datos relacional |
| **Docker** | 28.x | Containerización del entorno |
| **Docker Compose** | v2 | Orquestación de servicios |
| **DockerHub** | — | Registro de imágenes custom |
| **GitHub** | — | Control de versiones y CI/CD |
| **Vercel** | — | Hosting del sitio estático |

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                     Usuario                         │
│     https://meta-channel-multilingual.vercel.app    │
└─────────────────────┬───────────────────────────────┘
                      │ HTTPS (SSL automático Vercel)
┌─────────────────────▼───────────────────────────────┐
│              Vercel CDN (Edge Network)               │
│   Sitio estático HTML/CSS/JS exportado de WP        │
│   ES: /   ·   EN: /en/   ·   6 páginas estáticas   │
└─────────────────────────────────────────────────────┘

── Entorno local Docker (desarrollo) ──────────────────
┌─────────────────────────────────────────────────────┐
│              mcc_nginx (nginx:alpine)               │
│   SSL autofirmado · Redirige .ie → .com/en/         │
└────────────────────┬────────────────────────────────┘
                     │ FastCGI (puerto 9000)
┌────────────────────▼────────────────────────────────┐
│   mcc_wordpress (jazzcode/mcc-wordpress:1.1)        │
│   WordPress 6.7 + PHP-FPM 8.2 + TranslatePress     │
└────────────────────┬────────────────────────────────┘
                     │ MySQL (puerto 3306)
┌────────────────────▼────────────────────────────────┐
│            mcc_db (mariadb:10.11)                   │
└─────────────────────────────────────────────────────┘
```

---

## Estructura del Repositorio

```
Sistema-Multilenguaje-MetaChannelCorp/
├── parte4-dockerhub/           # Imágenes Docker custom publicadas en DockerHub
│   ├── docker-compose.yml      # Orquestación con imágenes jazzcode/*
│   ├── wordpress-custom/
│   │   ├── Dockerfile          # Imagen WordPress con TranslatePress preinstalado
│   │   ├── docker-entrypoint-mcc.sh  # Script de inicialización y BD
│   │   └── wp-content/         # Plugins, temas y SQL de inicialización
│   ├── nginx-custom/
│   │   ├── Dockerfile          # Imagen Nginx con SSL autofirmado
│   │   ├── default.conf        # Virtual hosts: .com + .ie → 301
│   │   └── generate-ssl-and-start.sh
│   └── README.md               # Instrucciones de uso del entorno Docker
│
├── meta-channel-multilingual/  # Entorno alternativo con imágenes oficiales
│   ├── docker-compose.yml
│   ├── nginx/default.conf
│   └── ssl/                    # Certificados SSL autofirmados
│
├── static-site/                # Exportación estática para Vercel
│   ├── index.html              # Página principal (Español)
│   ├── nosotros/index.html
│   ├── contacto/index.html
│   ├── en/                     # Versión English
│   │   ├── index.html
│   │   ├── nosotros/index.html
│   │   └── contacto/index.html
│   ├── css/                    # Hojas de estilo (Twenty Twenty-One + plugins)
│   └── js/                     # Scripts (jQuery + navegación)
│
├── vercel.json                 # Configuración de despliegue Vercel
├── GUIA-PRUEBAS.md             # Paso a paso de verificación
└── .gitignore
```

---

## Imágenes en DockerHub

| Imagen | Descripción |
|--------|-------------|
| `jazzcode/mcc-wordpress:1.1` | WordPress 6.7 + PHP-FPM 8.2 con TranslatePress, contenido y BD preconfigurados |
| `jazzcode/mcc-nginx:1.1` | Nginx con SSL autofirmado. `.com` sirve WordPress, `.ie` redirige 301 → `.com/en/` |

---

## URLs de Acceso

| Entorno | URL | Idioma |
|---------|-----|--------|
| **Vercel (producción)** | https://meta-channel-multilingual.vercel.app | Español |
| **Vercel EN** | https://meta-channel-multilingual.vercel.app/en/ | English |
| **Docker local** | https://metachannelcorp.com | Español |
| **Docker local EN** | https://metachannelcorp.com/en/ | English |
| **Docker local IE** | https://metachannelcorp.ie | → 301 a .com/en/ |
| **Admin WP** | https://metachannelcorp.com/wp-admin/ | admin / admin123 |

---

## Cómo Usar Este Repositorio

### Opción A — Ver el sitio desplegado en Vercel

Accede directamente a la URL de producción, no requiere instalación:

```
https://meta-channel-multilingual.vercel.app
```

### Opción B — Levantar el entorno Docker local

**Requisitos:** Docker Desktop instalado.

**Paso 1 — Configurar /etc/hosts** (macOS/Linux):
```bash
sudo bash -c 'echo "127.0.0.1   metachannelcorp.com" >> /etc/hosts'
sudo bash -c 'echo "127.0.0.1   metachannelcorp.ie"  >> /etc/hosts'
```

En Windows (como Administrador), editar `C:\Windows\System32\drivers\etc\hosts`:
```
127.0.0.1   metachannelcorp.com
127.0.0.1   metachannelcorp.ie
```

**Paso 2 — Clonar y arrancar:**
```bash
git clone https://github.com/RobertGiantSteps/Sistema-Multilenguaje-MetaChannelCorp.git
cd Sistema-Multilenguaje-MetaChannelCorp/parte4-dockerhub
docker compose up -d
```

**Paso 3 — Esperar 30–60 segundos** (primera inicialización de la BD).

**Paso 4 — Acceder:**
- https://metachannelcorp.com (Español) — aceptar advertencia de certificado autofirmado
- https://metachannelcorp.com/en/ (English)
- https://metachannelcorp.ie (redirige a .com/en/)
- https://metachannelcorp.com/wp-admin/ → `admin` / `admin123`

**Paso 5 — Detener:**
```bash
docker compose down
# Para eliminar también la BD:
docker compose down -v
```

### Opción C — Redesplegar en Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Desplegar desde la raíz del repositorio
vercel --prod
```

---

## Configuración Multiidioma

El sitio implementa las mejores prácticas SEO para sitios multiidioma:

- **Subdirectorios por idioma:** `/` para Español, `/en/` para English (estándar recomendado por Google)
- **Etiquetas hreflang:** generadas por TranslatePress para correcta indexación por buscadores
- **Dominio .ie con redirección 301** → `metachannelcorp.com/en/` (no sirve contenido propio, evitando contenido duplicado)
- **Selector de idioma textual** (sin banderas), accesible y estándar para audiencias internacionales
- **Atributo `lang` en `<html>`:** `es-ES` en páginas españolas, `en-GB` en páginas inglesas

---

## Notas Técnicas

- El **sitio estático en Vercel** es una exportación del contenido WordPress renderizado server-side (PHP). No tiene backend dinámico: los formularios y el panel de administración solo funcionan en el entorno Docker local.
- Los scripts de TranslatePress que hacen llamadas AJAX al backend WordPress han sido eliminados del sitio estático para evitar errores de red y garantizar que las traducciones (ya embebidas en el HTML) se muestren correctamente.
- La **arquitectura de dos capas** (Docker para desarrollo/CMS + Vercel para producción estática) es un patrón común en proyectos que necesitan la potencia de WordPress como headless CMS sin los costes de hosting dinámico.
