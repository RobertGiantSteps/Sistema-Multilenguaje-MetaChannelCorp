# Sistema Multilenguaje MetaChannelCorp

Sitio web corporativo bilingüe **(Español / English)** de **META Channel Corporation**, desplegado como sitio estático en Vercel a partir de una arquitectura WordPress + Docker + PHP-FPM.

---

## Acceso Rápido

| Entorno | URL | Idioma |
|---------|-----|--------|
| **Vercel — Español** | https://meta-channel-multilingual.vercel.app/es/ | Español |
| **Vercel — English** | https://meta-channel-multilingual.vercel.app/en/ | English |
| **Docker local — ES** | https://metachannelcorp.com | Español |
| **Docker local — EN** | https://metachannelcorp.com/en/ | English |
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

## Análisis Técnico: Decisiones de Diseño y Limitaciones

Esta sección documenta las decisiones tomadas en la implementación y sus fundamentos técnicos, incluyendo las áreas que requerirían consulta con dirección antes de una puesta en producción real.

### 1. Estructura de URLs multiidioma: subdirectorios /es/ y /en/

**Decisión implementada:** subdirectorios explícitos por idioma.

- `/es/` → Español
- `/en/` → English

**Por qué es correcto según Google:** Un dominio `.com` es un gTLD genérico, neutral en cuanto a idioma y país. No comunica ningún idioma por sí solo. La forma estándar y recomendada por Google Search Central para sitios multiidioma dentro de un mismo dominio es el uso de subdirectorios por idioma (`/es/`, `/en/`). Esto permite a los buscadores identificar, indexar y servir la versión correcta según el idioma del usuario mediante las etiquetas `hreflang`.

**Implementación actual:** TranslatePress Free configura el idioma por defecto en la raíz del dominio. Como solución, el sitio estático sirve el contenido español tanto en `/` (compatibilidad) como en `/es/` (SEO estándar), y el contenido inglés en `/en/`.

---

### 2. Configuración del dominio .ie

**Decisión implementada:** `.ie` configurado como **redirección 301 permanente** a `metachannelcorp.com/en/`.

```nginx
server {
    listen 443 ssl;
    server_name metachannelcorp.ie;
    return 301 https://metachannelcorp.com/en/$request_uri;
}
```

**Por qué es correcto:** El `.ie` (ccTLD irlandés) solo actúa como señal geográfica si tiene contenido propio indexado. Un dominio que solo redirige **no genera señal geográfica** ante Google porque no tiene contenido que indexar. Servir el mismo WordPress en `.ie` y `.com` constituyría **contenido duplicado**, con riesgo de penalización SEO para ambos dominios. La redirección 301 es la configuración correcta: indica a Google que el dominio .ie no es un sitio activo, y concentra toda la autoridad en `.com`.

---

### 3. Español como idioma principal: decisión pendiente de consulta con dirección

**Decisión tomada:** Español como idioma por defecto (raíz `/`), Inglés en `/en/`.

**Por qué requería consulta:** La URL raíz concentra la mayor autoridad de dominio. Datos objetivos del sitio apuntan a que el inglés podría ser más adecuado como idioma principal:

- Sede corporativa en **Dublín** (Irlanda, país angloparlante)
- Oficinas en **Washington D.C.** y **Miami** (EE.UU.)
- Dominio principal `.com` (genérico internacional, lingua franca = inglés)
- Dominio secundario `.ie` (Irlanda)

Si el mercado objetivo prioritario es angloparlante, la URL raíz debería servir en inglés, con el español en `/es/`. Esta decisión depende de datos de tráfico y estrategia comercial, y **debe definirse desde dirección**.

---

### 4. Plugin de traducción: TranslatePress Free — Limitaciones y alternativas

**Decisión tomada:** TranslatePress Free 3.1 (limitado a 2 idiomas, sin SEO Pack).

**Limitaciones críticas para un proyecto corporativo:**

| Característica | TranslatePress Free | TranslatePress Premium | WPML | Polylang Pro |
|---|---|---|---|---|
| Número de idiomas | **2 máximo** | Ilimitados | Ilimitados | Ilimitados |
| Traducir meta titles/descriptions | ✗ | ✓ | ✓ | ✓ |
| Traducir slugs de URL por idioma | ✗ | ✓ | ✓ | ✓ |
| Integración Google Translate / DeepL | ✗ | ✓ | Parcial | ✗ |
| Cuentas de traductor independientes | ✗ | ✓ | ✓ | ✓ |
| Open Graph por idioma | ✗ | ✓ | ✓ | ✓ |
| Coste anual aprox. | Gratis | ~$89 | ~$99 | ~$99 |

**Impacto real:** Sin SEO Pack, Google no indexa meta descriptions ni Open Graph distintos por idioma, lo que afecta directamente al rendimiento en búsquedas internacionales. Si se planea añadir francés, portugués u otros idiomas (empresa activa en 30 países), es necesario migrar a versión de pago.

**Recomendación:** para producción real, evaluar TranslatePress Premium o WPML según presupuesto y requerimientos de flujo de trabajo de traducción.

---

### 5. Inglés británico (en_GB) vs. Inglés americano (en_US)

**Decisión tomada:** `en_GB` (English UK).

**Por qué requería consulta:** Con oficinas en Washington D.C. y Miami, parte del mercado angloparlante objetivo es estadounidense. Existen diferencias de ortografía y vocabulario (`colour/color`, `organisation/organization`) que pueden afectar al posicionamiento en búsquedas desde EE.UU. La elección entre `en_GB`, `en_US` o el código genérico `en` depende del análisis del mercado objetivo y los datos de tráfico, y **debería consultarse con dirección**.

---

### 6. Selector de idioma: sin banderas, solo texto

**Decisión implementada:** selector textual `Spanish | English`, sin banderas de países.

**Por qué es correcto:** El español se habla en más de 20 países. Una bandera de España no representa a usuarios de México, Colombia, Argentina, etc. El inglés tampoco pertenece exclusivamente al Reino Unido. La práctica estándar para webs corporativas internacionales es usar texto (`ES | EN` o `Español | English`) sin asociar idiomas a países específicos. TranslatePress está configurado con `flags: no`.

---

### 7. Contenido con HTML inline y CSS inline

**Observación:** Algunas secciones del sitio (por ejemplo, Casos de Éxito) utilizan bloques de Custom HTML con etiquetas `<style>` y atributos `style=` en lugar de bloques nativos de Gutenberg.

**Problemas que genera:**
1. **Mantenimiento difícil:** cualquier cambio de diseño requiere editar HTML manualmente
2. **Conflictos con TranslatePress:** el plugin traduce de forma óptima contenido en bloques nativos de WordPress; el HTML crudo puede no procesarse correctamente

**Recomendación para producción:** reemplazar todos los bloques Custom HTML por bloques estándar de Gutenberg (Párrafo, Lista, Imagen, Botón, Grupo), y aplicar estilos a nivel de tema o mediante CSS global. Si se requiere diseño avanzado, valorar un page builder compatible con plugins de traducción (Elementor es compatible con TranslatePress Premium y WPML).

---

### 8. Plan de despliegue en producción real

Para un despliegue en producción real con dominios propios y SLA corporativo:

| Fase | Acción | Herramienta |
|------|--------|-------------|
| **Hosting** | VPS o Cloud con soporte Docker (para WP dinámico) | DigitalOcean, Render, Railway, AWS EC2 |
| **SSL** | Certificados válidos (no autofirmados) | Let's Encrypt (Certbot) o Cloudflare |
| **DNS** | Apuntar `.com` y `.ie` al servidor | Registro de dominio (ej. Namecheap, GoDaddy) |
| **Backups** | BD + wp-content automatizados | UpdraftPlus o scripts cron + S3 |
| **CDN** | Caché global para assets estáticos | Cloudflare (gratis) o Vercel Pro |
| **Monitoring** | Uptime + alertas | UptimeRobot o Better Uptime |
| **Plugin** | Evaluar TranslatePress Premium o WPML | Según presupuesto y requerimientos |
| **Idioma principal** | Definir EN vs ES como raíz | Decisión de dirección según mercado |

---

## Verificación Rápida

```bash
# Comprobar que todos los endpoints responden
curl -o /dev/null -w "%{http_code} %{url}\n" \
  https://meta-channel-multilingual.vercel.app/es/ \
  https://meta-channel-multilingual.vercel.app/en/ \
  https://meta-channel-multilingual.vercel.app/es/nosotros/ \
  https://meta-channel-multilingual.vercel.app/en/nosotros/

# Verificar redirección .ie (Docker local)
curl -sk -o /dev/null -w "%{http_code} -> %{redirect_url}\n" https://metachannelcorp.ie
# Esperado: 301 -> https://metachannelcorp.com/en/
```
