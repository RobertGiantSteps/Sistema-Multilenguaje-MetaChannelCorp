#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# EXPORT — Extrae BD y wp-content del entorno Docker actual
# Ejecutar desde: /Users/minibob/Desktop/roberto260226/parte4-dockerhub/
# REQUISITO: Docker Desktop corriendo + contenedores mcc_* activos
# ═══════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WP_CUSTOM_DIR="${SCRIPT_DIR}/wordpress-custom"

echo "══════════════════════════════════════════"
echo " MCC — Exportando entorno actual"
echo "══════════════════════════════════════════"

# ── PASO 1: Verificar que los contenedores están corriendo ────────
echo ""
echo "► PASO 1: Verificando contenedores..."
if ! docker ps --format '{{.Names}}' | grep -q "mcc_db"; then
    echo "  ERROR: El contenedor mcc_db no está corriendo."
    echo "  Ejecuta: cd ~/Desktop/roberto260226/meta-channel-multilingual && docker compose up -d"
    exit 1
fi
echo "  ✓ Contenedores mcc_* detectados"

# ── PASO 2: Exportar base de datos ───────────────────────────────
echo ""
echo "► PASO 2: Exportando base de datos WordPress..."
docker exec mcc_db mysqldump \
    -u wpuser -pwppass \
    --single-transaction \
    --routines \
    --triggers \
    wordpress > "${WP_CUSTOM_DIR}/wp-content/mcc-init.sql"
echo "  ✓ BD exportada en: wordpress-custom/wp-content/mcc-init.sql"

# ── PASO 3: Copiar wp-content del contenedor ─────────────────────
echo ""
echo "► PASO 3: Copiando wp-content..."
# Limpiar destino primero (excepto .gitkeep si existe)
rm -rf "${WP_CUSTOM_DIR}/wp-content/plugins" \
       "${WP_CUSTOM_DIR}/wp-content/themes" \
       "${WP_CUSTOM_DIR}/wp-content/uploads"

# Copiar desde el contenedor
docker cp mcc_wordpress:/var/www/html/wp-content/plugins \
          "${WP_CUSTOM_DIR}/wp-content/plugins"
docker cp mcc_wordpress:/var/www/html/wp-content/themes \
          "${WP_CUSTOM_DIR}/wp-content/themes"
docker cp mcc_wordpress:/var/www/html/wp-content/uploads \
          "${WP_CUSTOM_DIR}/wp-content/uploads"

echo "  ✓ wp-content copiado:"
echo "    - plugins/"
echo "    - themes/"
echo "    - uploads/"

# ── RESUMEN ───────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════"
echo " ✅ EXPORTACIÓN COMPLETADA"
echo "══════════════════════════════════════════"
echo ""
echo " Ahora ejecuta el build:"
echo "   bash build-and-push.sh TU_USUARIO_DOCKERHUB"
echo ""
