#!/bin/bash
set -e

SSL_DIR="/etc/nginx/ssl"
mkdir -p "$SSL_DIR"

# Generar certificado autofirmado si no existe
if [ ! -f "$SSL_DIR/server.crt" ]; then
    echo "[MCC-Nginx] Generando certificados SSL autofirmados..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -subj "/CN=metachannelcorp.com/O=META Channel Corporation/C=IE" \
        -addext "subjectAltName=DNS:metachannelcorp.com,DNS:metachannelcorp.ie" \
        -keyout "$SSL_DIR/server.key" \
        -out    "$SSL_DIR/server.crt"
    echo "[MCC-Nginx] Certificados generados en $SSL_DIR"
else
    echo "[MCC-Nginx] Certificados SSL ya existen — omitiendo generación."
fi

echo "[MCC-Nginx] Iniciando Nginx..."
exec nginx -g "daemon off;"
