# PARTE 4 — DOCKERHUB
## META Channel Corporation — Arquitectura Multidioma WordPress

---

## Imágenes publicadas en DockerHub

| Imagen | Descripción |
|--------|-------------|
| `jazzcode/mcc-wordpress:1.1` | WordPress 6.7 + PHP-FPM 8.2 con TranslatePress, contenido y BD preconfigurados (corregido: selector sin banderas, bloques nativos Gutenberg) |
| `jazzcode/mcc-nginx:1.1` | Nginx con SSL autofirmado. El .com sirve WordPress, el .ie redirige 301 a .com/en/ |

---

## Cómo levantar el entorno desde cero

### PASO 1 — Requisito: /etc/hosts

Añadir estas dos líneas al archivo `/etc/hosts` del sistema:

**En macOS / Linux:**
```bash
sudo bash -c 'echo "127.0.0.1   metachannelcorp.com" >> /etc/hosts'
sudo bash -c 'echo "127.0.0.1   metachannelcorp.ie"  >> /etc/hosts'
```

**En Windows** (ejecutar como Administrador en Notepad):
Editar `C:\Windows\System32\drivers\etc\hosts` y añadir:
```
127.0.0.1   metachannelcorp.com
127.0.0.1   metachannelcorp.ie
```

---

### PASO 2 — Descargar docker-compose.yml

Descarga el `docker-compose.yml` de este repositorio, o copia el siguiente contenido:

```yaml
services:
  db:
    image: mariadb:10.11
    container_name: mcc_db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE:      wordpress
      MYSQL_USER:          wpuser
      MYSQL_PASSWORD:      wppass
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - mcc_net
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 10

  wordpress:
    image: jazzcode/mcc-wordpress:1.0
    container_name: mcc_wordpress
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      WORDPRESS_DB_HOST:     db:3306
      WORDPRESS_DB_NAME:     wordpress
      WORDPRESS_DB_USER:     wpuser
      WORDPRESS_DB_PASSWORD: wppass
      WORDPRESS_CONFIG_EXTRA: |
        if (isset($$_SERVER['HTTP_X_FORWARDED_PROTO']) && $$_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
            $$_SERVER['HTTPS'] = 'on';
        }
        if (isset($$_SERVER['HTTP_HOST'])) {
            define('WP_SITEURL', 'https://' . $$_SERVER['HTTP_HOST']);
            define('WP_HOME',    'https://' . $$_SERVER['HTTP_HOST']);
        }
        define('FORCE_SSL_ADMIN', false);
    volumes:
      - wp_data:/var/www/html
    networks:
      - mcc_net

  nginx:
    image: jazzcode/mcc-nginx:1.0
    container_name: mcc_nginx
    restart: unless-stopped
    depends_on:
      - wordpress
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - wp_data:/var/www/html
    networks:
      - mcc_net

volumes:
  db_data:
  wp_data:

networks:
  mcc_net:
    driver: bridge
```

---

### PASO 3 — Arrancar el entorno

```bash
docker compose up -d
```

Espera aproximadamente **30-60 segundos** en el primer arranque.
El contenedor de WordPress detecta que es la primera ejecución e importa automáticamente la base de datos.

---

### PASO 4 — Acceder al entorno

| URL | Idioma | Descripción |
|-----|--------|-------------|
| https://metachannelcorp.com | Español | Dominio principal |
| https://metachannelcorp.com/en/ | Inglés | Versión inglesa |
| https://metachannelcorp.ie | — | Redirección 301 → .com/en/ |
| https://metachannelcorp.com/wp-admin/ | — | Panel de administración |

**Credenciales WordPress:**
- Usuario: `admin`
- Contraseña: `admin123`

> **Nota sobre el certificado SSL:**
> Al ser autofirmado, el navegador mostrará una advertencia de seguridad.
> Haz clic en "Avanzado" → "Continuar a metachannelcorp.com (no seguro)" para aceptarlo.
> En Safari: "Visitar este sitio web" → "Visitar sitio web".

---

### PASO 5 — Detener el entorno

```bash
docker compose down
```

Para eliminar también los datos (volúmenes):
```bash
docker compose down -v
```

---

## Arquitectura del entorno

```
┌─────────────────────────────────────────────────────┐
│                     Usuario                         │
│         https://metachannelcorp.com (.ie)           │
└─────────────────────┬───────────────────────────────┘
                      │ puerto 443 (HTTPS)
┌─────────────────────▼───────────────────────────────┐
│              mcc_nginx (nginx:alpine)               │
│   SSL autofirmado · HTTP→HTTPS redirect             │
│   Server: metachannelcorp.com + metachannelcorp.ie  │
└─────────────────────┬───────────────────────────────┘
                      │ FastCGI (puerto 9000)
┌─────────────────────▼───────────────────────────────┐
│      mcc_wordpress (jazzcode/mcc-wordpress:1.0)   │
│   WordPress 6.7 + PHP-FPM 8.2                       │
│   TranslatePress 3.1 · Tema Twenty Twenty-One       │
│   WP_SITEURL dinámico según HTTP_HOST               │
└─────────────────────┬───────────────────────────────┘
                      │ MySQL (puerto 3306)
┌─────────────────────▼───────────────────────────────┐
│               mcc_db (mariadb:10.11)                │
│   DB: wordpress · User: wpuser / wppass             │
└─────────────────────────────────────────────────────┘
```

---

## Contenido incluido en la imagen

- **Plugin:** TranslatePress 3.1 (libre) configurado ES/EN
- **Tema:** Twenty Twenty-One (clásico con soporte de menús)
- **Página de prueba:** "Servicios Jurídico-Tecnológicos de META Channel Corporation"
  - Título H1, párrafos, lista de 5 servicios, botón CTA
  - Menú: Servicios · Nosotros · Contacto
  - Bloque HTML con caso de estudio (h3, p, strong, em, a)
- **Traducciones:** 64 cadenas ES→EN completamente traducidas
- **hreflang:** Generados automáticamente por TranslatePress
