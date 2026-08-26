#!/usr/bin/env bash
# ==============================================================================
# Blott og Bar - Automated VPS Deployment & Daily Update Script
# Target OS: Ubuntu 22.04 LTS
# Designed to run standalone or co-hosted alongside simpleplanner.blottogbar.no
# ==============================================================================

set -euo pipefail

APP_DIR="/var/www/blottogbar"
DOMAIN="blottogbar.no"
WWW_DOMAIN="www.blottogbar.no"
GUNICORN_PORT="8001"
DB_NAME="blottogbar"
DB_USER="blottogbar_user"
DB_PASS="${DB_PASSWORD:-$(openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c 16)}"
SSL_EMAIL="${SSL_EMAIL:-admin@${DOMAIN}}"

echo "========================================================="
echo "   🚀 Blott og Bar Landing Page - Deployment & Update"
echo "========================================================="

# 1. Require root / sudo
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script with sudo: sudo bash deploy.sh"
  exit 1
fi

# Detect if this is a first-time setup or a daily update
FIRST_TIME=false
if [ ! -f "${APP_DIR}/.env" ] || [ ! -d "${APP_DIR}/venv" ]; then
  FIRST_TIME=true
  echo "[*] First-time setup detected. Installing system prerequisites..."
  apt update -y
  apt install -y python3-venv python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx certbot python3-certbot-nginx git ufw
  
  # Stop default Apache or remove default Nginx site if present
  systemctl stop apache2 2>/dev/null || true
  systemctl disable apache2 2>/dev/null || true
  rm -f /etc/nginx/sites-enabled/default
else
  echo "[*] Existing installation detected. Performing safe update..."
fi

# 2. Configure PostgreSQL (Idempotent - safe to run repeatedly)
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';"

sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

# 3. Pull latest code or sync directory
echo "[*] Updating application code in ${APP_DIR}..."
mkdir -p "${APP_DIR}"
if [ -d "${APP_DIR}/.git" ]; then
  git config --global --add safe.directory "${APP_DIR}" 2>/dev/null || true
  cd "${APP_DIR}"
  git pull origin master || true
elif [ "$(pwd)" != "${APP_DIR}" ]; then
  cp -r . "${APP_DIR}/"
fi
cd "${APP_DIR}"

# 4. Virtual Environment & Dependencies
if [ ! -d "${APP_DIR}/venv" ]; then
  echo "[*] Creating Python virtual environment..."
  python3 -m venv "${APP_DIR}/venv"
fi
echo "[*] Installing/updating Python dependencies..."
"${APP_DIR}/venv/bin/pip" install --quiet --upgrade pip
"${APP_DIR}/venv/bin/pip" install --quiet -r "${APP_DIR}/requirements.txt"

# 5. Environment configuration (.env preserved if exists)
if [ ! -f "${APP_DIR}/.env" ]; then
  echo "[*] Generating production .env configuration..."
  SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
  cat << EOF > "${APP_DIR}/.env"
DEBUG=False
SECRET_KEY=${SECRET_KEY}
ALLOWED_HOSTS=${DOMAIN},${WWW_DOMAIN},127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://${DOMAIN},https://${WWW_DOMAIN}
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASS}
DB_HOST=127.0.0.1
DB_PORT=5432
EOF
  chmod 600 "${APP_DIR}/.env"
fi

# 6. Run Migrations & Collect Static Assets
echo "[*] Running database migrations..."
"${APP_DIR}/venv/bin/python" "${APP_DIR}/manage.py" migrate --noinput

echo "[*] Collecting static assets..."
"${APP_DIR}/venv/bin/python" "${APP_DIR}/manage.py" collectstatic --noinput

# Set web server file ownership
chown -R www-data:www-data "${APP_DIR}"
chmod -R 755 "${APP_DIR}/static"

# 7. Configure Gunicorn Systemd Service (Port 8001 / gunicorn_blottogbar)
if [ ! -f "/etc/systemd/system/gunicorn_blottogbar.service" ]; then
  echo "[*] Installing Gunicorn systemd service from systemd/gunicorn_blottogbar.service..."
  cp "${APP_DIR}/systemd/gunicorn_blottogbar.service" /etc/systemd/system/gunicorn_blottogbar.service
  systemctl daemon-reload
  systemctl enable gunicorn_blottogbar
fi

# Restart Gunicorn to apply new code
echo "[*] Restarting Gunicorn..."
systemctl restart gunicorn_blottogbar

# 8. Configure Nginx (Preserves existing SSL / Certbot configuration!)
if [ ! -f "/etc/nginx/sites-available/${DOMAIN}" ]; then
  echo "[*] Installing initial Nginx configuration from nginx/blottogbar.no.conf..."
  cp "${APP_DIR}/nginx/blottogbar.no.conf" "/etc/nginx/sites-available/${DOMAIN}"
  ln -sf "/etc/nginx/sites-available/${DOMAIN}" /etc/nginx/sites-enabled/
fi

nginx -t
systemctl reload nginx

# 9. Configure UFW Firewall (if active)
if command -v ufw >/dev/null 2>&1; then
  ufw allow OpenSSH >/dev/null 2>&1 || true
  ufw allow 'Nginx Full' >/dev/null 2>&1 || true
fi

echo "========================================================="
echo "   ✅ Blott og Bar is live at http://${DOMAIN} & http://${WWW_DOMAIN}!"
echo "========================================================="
if [ "$FIRST_TIME" = true ]; then
  echo ""
  echo "🔒 First time setup: Activate your SSL certificate by running:"
  echo "   sudo certbot --nginx -d ${DOMAIN} -d ${WWW_DOMAIN} --non-interactive --agree-tos -m ${SSL_EMAIL} --redirect"
fi
echo ""
