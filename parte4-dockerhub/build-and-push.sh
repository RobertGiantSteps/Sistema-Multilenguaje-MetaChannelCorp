#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# BUILD & PUSH — META Channel Corporation Docker Images
# Ejecutar DESPUÉS de que Docker Desktop esté corriendo
# y DESPUÉS de haber exportado BD y wp-content (ver README)
# ═══════════════════════════════════════════════════════════════════

set -e

# ── CONFIGURA TU USUARIO DE DOCKERHUB AQUÍ ──────────────────────
DOCKERHUB_USER="${1:-jazzcode}"
TAG="1.0"
WP_IMAGE="${DOCKERHUB_USER}/mcc-wordpress:${TAG}"
NGINX_IMAGE="${DOCKERHUB_USER}/mcc-nginx:${TAG}"

echo "=============================================="
echo " META Channel Corp — Build & Push a DockerHub"
echo " Usuario: ${DOCKERHUB_USER}"
echo " WP Image: ${WP_IMAGE}"
echo " Nginx Image: ${NGINX_IMAGE}"
echo "=============================================="

# ── PASO 1: Login en DockerHub ────────────────────────────────────
echo ""
echo "► PASO 1: Login en DockerHub..."
docker login

# ── PASO 2: Build imagen WordPress ───────────────────────────────
echo ""
echo "► PASO 2: Construyendo imagen WordPress..."
docker build \
    --platform linux/amd64 \
    -t "${WP_IMAGE}" \
    ./wordpress-custom/
echo "  ✓ Imagen WordPress construida: ${WP_IMAGE}"

# ── PASO 3: Build imagen Nginx ────────────────────────────────────
echo ""
echo "► PASO 3: Construyendo imagen Nginx..."
docker build \
    --platform linux/amd64 \
    -t "${NGINX_IMAGE}" \
    ./nginx-custom/
echo "  ✓ Imagen Nginx construida: ${NGINX_IMAGE}"

# ── PASO 4: Push WordPress a DockerHub ───────────────────────────
echo ""
echo "► PASO 4: Subiendo imagen WordPress a DockerHub..."
docker push "${WP_IMAGE}"
echo "  ✓ Push completado: ${WP_IMAGE}"

# ── PASO 5: Push Nginx a DockerHub ───────────────────────────────
echo ""
echo "► PASO 5: Subiendo imagen Nginx a DockerHub..."
docker push "${NGINX_IMAGE}"
echo "  ✓ Push completado: ${NGINX_IMAGE}"

# ── PASO 6: Actualizar docker-compose.yml con el usuario real ────
echo ""
echo "► PASO 6: Actualizando docker-compose.yml con tu usuario..."
sed -i.bak \
    "s|jazzcode_DOCKERHUB|${DOCKERHUB_USER}|g" \
    docker-compose.yml
echo "  ✓ docker-compose.yml actualizado"

echo ""
echo "=============================================="
echo " ✅ PROCESO COMPLETADO"
echo "=============================================="
echo ""
echo " Imágenes publicadas:"
echo "   ${WP_IMAGE}"
echo "   ${NGINX_IMAGE}"
echo ""
echo " Para levantar el entorno en cualquier máquina:"
echo "   1. Añadir a /etc/hosts:"
echo "      127.0.0.1   metachannelcorp.com"
echo "      127.0.0.1   metachannelcorp.ie"
echo "   2. docker compose up -d"
echo "   3. Abrir https://metachannelcorp.com"
echo "=============================================="
