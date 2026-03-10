# GUIA DE PRUEBAS - META Channel Corporation

## Arquitectura del Proyecto

```
roberto260226Multilingual/
├── parte4-dockerhub/          # Docker images custom (DockerHub)
│   ├── docker-compose.yml     # Orquestacion: MariaDB + WordPress + Nginx
│   ├── wordpress-custom/      # Dockerfile + entrypoint WordPress
│   ├── nginx-custom/          # Dockerfile + config Nginx + SSL
│   └── README.md              # Documentacion Docker
├── meta-channel-multilingual/ # Docker Compose con imagenes oficiales
│   ├── docker-compose.yml
│   ├── nginx/default.conf
│   └── ssl/                   # Certificados SSL autofirmados
├── static-site/               # Exportacion estatica para Vercel
│   ├── index.html             # Pagina principal (ES)
│   ├── en/                    # Version inglesa
│   ├── nosotros/              # Pagina Nosotros (ES)
│   ├── contacto/              # Pagina Contacto (ES)
│   ├── css/                   # Hojas de estilo
│   └── js/                    # Scripts
├── vercel.json                # Configuracion de despliegue Vercel
└── .gitignore
```

---

## URLs de Acceso

| Recurso | URL |
|---------|-----|
| **Vercel (produccion)** | https://meta-channel-multilingual.vercel.app |
| **Vercel EN** | https://meta-channel-multilingual.vercel.app/en/ |
| **GitHub repo** | https://github.com/RobertGiantSteps/roberto260226Multilingual |
| **Docker local (ES)** | https://metachannelcorp.com (requiere /etc/hosts) |
| **Docker local (EN)** | https://metachannelcorp.com/en/ |
| **Docker admin** | https://metachannelcorp.com/wp-admin/ (admin/admin123) |

---

## PASO 1 - Verificar GitHub

1. Abrir: https://github.com/RobertGiantSteps/roberto260226Multilingual
2. Confirmar que existen las carpetas:
   - `parte4-dockerhub/` con docker-compose.yml, Dockerfiles, README.md
   - `meta-channel-multilingual/` con docker-compose.yml, nginx config, SSL
   - `static-site/` con index.html, en/, css/, js/
   - `vercel.json` en la raiz
3. Verificar que NO esta el archivo .mp4 (excluido por .gitignore)
4. Verificar que NO hay archivos .DS_Store

---

## PASO 2 - Verificar Vercel (sitio estatico)

### 2.1 Pagina principal (ES)
1. Abrir: https://meta-channel-multilingual.vercel.app
2. Verificar:
   - Titulo: "META Channel Corporation"
   - Heading H1: "Servicios Juridico-Tecnologicos de META Channel Corporation"
   - Menu de navegacion visible
   - Estilos CSS cargados (tema Twenty Twenty-One)
   - Selector de idioma visible (Spanish/English)

### 2.2 Pagina principal (EN)
1. Abrir: https://meta-channel-multilingual.vercel.app/en/
2. Verificar:
   - Heading H1: "Legal-Technological Services of META Channel Corporation"
   - Contenido traducido al ingles
   - Selector de idioma visible

### 2.3 Paginas internas
1. Abrir: https://meta-channel-multilingual.vercel.app/nosotros/
   - Verificar que carga la pagina "Nosotros" en espanol
2. Abrir: https://meta-channel-multilingual.vercel.app/contacto/
   - Verificar que carga la pagina "Contacto" en espanol
3. Abrir: https://meta-channel-multilingual.vercel.app/en/nosotros/
   - Verificar version inglesa de "Nosotros"
4. Abrir: https://meta-channel-multilingual.vercel.app/en/contacto/
   - Verificar version inglesa de "Contacto"

### 2.4 Assets (CSS/JS)
1. Abrir DevTools (F12) > Network
2. Recargar la pagina
3. Verificar que cargan sin errores (HTTP 200):
   - css/style.css
   - css/block-library.css
   - css/trp-switcher.css
   - js/primary-navigation.js
   - js/trp-frontend-switcher.js

### 2.5 HTTPS
1. Verificar el candado verde en la barra de direcciones
2. Vercel proporciona SSL automaticamente (no certificado autofirmado)

---

## PASO 3 - Verificar Docker local

### 3.1 Requisitos previos
```bash
# Verificar que /etc/hosts tiene las entradas
cat /etc/hosts | grep metachannelcorp

# Verificar contenedores corriendo
docker ps | grep mcc
```

### 3.2 Probar acceso
1. https://metachannelcorp.com - Pagina ES (aceptar certificado autofirmado)
2. https://metachannelcorp.com/en/ - Pagina EN
3. https://metachannelcorp.ie - Debe redirigir 301 a metachannelcorp.com/en/
4. https://metachannelcorp.com/wp-admin/ - Panel WordPress (admin/admin123)

### 3.3 Verificar multiidioma
1. En wp-admin, ir a Ajustes > TranslatePress
2. Verificar idiomas configurados: Espanol (default) + English
3. Verificar que las 64 cadenas estan traducidas

---

## PASO 4 - Verificar imagenes DockerHub

```bash
# Las imagenes estan publicadas en DockerHub:
docker pull jazzcode/mcc-wordpress:1.1
docker pull jazzcode/mcc-nginx:1.1

# Verificar que se descargan correctamente
docker images | grep jazzcode
```

---

## PASO 5 - Prueba completa desde cero

Para verificar que todo funciona desde un entorno limpio:

```bash
# 1. Clonar el repositorio
git clone https://github.com/RobertGiantSteps/roberto260226Multilingual.git
cd roberto260226Multilingual

# 2. Levantar Docker (parte4-dockerhub)
cd parte4-dockerhub
docker compose up -d

# 3. Esperar 30-60 segundos para la primera inicializacion

# 4. Verificar contenedores
docker ps | grep mcc

# 5. Acceder a las URLs (requiere /etc/hosts configurado)
# https://metachannelcorp.com
# https://metachannelcorp.com/en/
# https://metachannelcorp.com/wp-admin/

# 6. Para el sitio estatico en Vercel, ya esta desplegado en:
# https://meta-channel-multilingual.vercel.app
```

---

## Resumen de Verificacion

| Componente | Estado | URL/Comando |
|-----------|--------|-------------|
| GitHub repo | Subido | https://github.com/RobertGiantSteps/roberto260226Multilingual |
| Vercel deploy | Desplegado | https://meta-channel-multilingual.vercel.app |
| Pagina ES (Vercel) | Funcionando | /  |
| Pagina EN (Vercel) | Funcionando | /en/ |
| Nosotros ES | Funcionando | /nosotros/ |
| Contacto ES | Funcionando | /contacto/ |
| Nosotros EN | Funcionando | /en/nosotros/ |
| Contacto EN | Funcionando | /en/contacto/ |
| CSS/JS assets | Cargando OK | DevTools > Network |
| HTTPS (Vercel) | SSL automatico | Candado verde |
| Docker local | 3 contenedores | docker ps |
| DockerHub images | Publicadas | jazzcode/mcc-wordpress:1.1, jazzcode/mcc-nginx:1.1 |

---

## Notas Importantes

1. **Vercel sirve la version estatica** (HTML/CSS/JS exportado de WordPress). No tiene backend PHP ni base de datos. El panel de administracion WordPress solo funciona en Docker local.

2. **Docker sirve la version dinamica** completa con WordPress, MariaDB y Nginx. Permite editar contenido, instalar plugins, etc.

3. **El selector de idioma** en Vercel es visual pero la navegacion entre idiomas funciona mediante links estaticos (/en/).

4. **El certificado SSL** en Docker es autofirmado (advertencia del navegador). En Vercel el SSL es automatico y valido.
