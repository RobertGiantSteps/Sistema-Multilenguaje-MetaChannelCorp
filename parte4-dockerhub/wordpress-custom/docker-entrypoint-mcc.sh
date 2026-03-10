#!/bin/bash
set -e

# ─────────────────────────────────────────────────────────────────────────────
# Entrypoint personalizado META Channel Corporation
# 1. Espera a MariaDB
# 2. Importa el SQL en la primera ejecución
# 3. Llama al entrypoint oficial de WordPress (que configura wp-config.php
#    y arranca PHP-FPM)
# ─────────────────────────────────────────────────────────────────────────────

# Extraer host y puerto de WORDPRESS_DB_HOST (formato "host:puerto")
DB_HOST="${WORDPRESS_DB_HOST%%:*}"
DB_PORT_RAW="${WORDPRESS_DB_HOST##*:}"
# Si no hay ":" en la cadena, host y "port" serán iguales → usar 3306
if [ "$DB_HOST" = "$DB_PORT_RAW" ]; then
    DB_PORT="3306"
else
    DB_PORT="$DB_PORT_RAW"
fi

# ─── 1. Esperar a que MariaDB esté lista ─────────────────────────────────────
echo "[MCC] Esperando a que la base de datos esté disponible en ${DB_HOST}:${DB_PORT}..."
MAX_TRIES=40
COUNT=0
until mysql -h "$DB_HOST" -P "$DB_PORT" \
            -u "${WORDPRESS_DB_USER}" \
            -p"${WORDPRESS_DB_PASSWORD}" \
            "${WORDPRESS_DB_NAME}" \
            -e "SELECT 1;" > /dev/null 2>&1; do
    COUNT=$((COUNT + 1))
    if [ "$COUNT" -ge "$MAX_TRIES" ]; then
        echo "[MCC] ERROR: Base de datos no disponible tras ${MAX_TRIES} intentos. Abortando."
        exit 1
    fi
    echo "[MCC] Intento ${COUNT}/${MAX_TRIES} — reintentando en 3s..."
    sleep 3
done
echo "[MCC] ✓ Base de datos disponible."

# ─── 2. Importar SQL en primera ejecución ────────────────────────────────────
TABLE_COUNT=$(mysql -h "$DB_HOST" -P "$DB_PORT" \
                    -u "${WORDPRESS_DB_USER}" \
                    -p"${WORDPRESS_DB_PASSWORD}" \
                    "${WORDPRESS_DB_NAME}" \
                    -e "SHOW TABLES LIKE 'wp_options';" 2>/dev/null | wc -l)

if [ "$TABLE_COUNT" -eq "0" ]; then
    SQL_FILE="/docker/mcc-init.sql"
    if [ -f "$SQL_FILE" ]; then
        echo "[MCC] Primera ejecución detectada — importando base de datos..."
        mysql -h "$DB_HOST" -P "$DB_PORT" \
              -u "${WORDPRESS_DB_USER}" \
              -p"${WORDPRESS_DB_PASSWORD}" \
              "${WORDPRESS_DB_NAME}" < "$SQL_FILE"
        echo "[MCC] ✓ Base de datos importada correctamente."
    else
        echo "[MCC] AVISO: No se encontró ${SQL_FILE}. Iniciando sin datos precargados."
    fi
else
    echo "[MCC] ✓ Base de datos ya inicializada — omitiendo importación."
fi

# ─── 3. Llamar al entrypoint oficial de WordPress ────────────────────────────
# Este entrypoint configura wp-config.php y lanza PHP-FPM
echo "[MCC] Iniciando WordPress..."
exec /usr/local/bin/docker-entrypoint.sh "$@"
