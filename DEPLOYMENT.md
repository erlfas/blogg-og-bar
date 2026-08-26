# Blott og Bar - Production Deployment Guide (Ubuntu 22.04 LTS)

This guide walks you through deploying **`blottogbar.no`** and **`www.blottogbar.no`** to an **Ubuntu 22.04 LTS** VPS using **PostgreSQL**, **Gunicorn (Systemd)**, **Nginx**, and **Let's Encrypt (Certbot)** for SSL/TLS.

It is designed to run independently or **co-exist seamlessly on the same VPS alongside `simpleplanner.blottogbar.no`**.

---

## Architecture Overview & Co-hosting Setup

| Resource | Blott og Bar Landing (`blottogbar.no`) | Simple Planner (`simpleplanner.blottogbar.no`) |
| :--- | :--- | :--- |
| **Domain(s)** | `blottogbar.no`, `www.blottogbar.no` | `simpleplanner.blottogbar.no` |
| **Path** | `/var/www/blottogbar` | `/var/www/simpleplanner` |
| **Gunicorn Port** | `127.0.0.1:8001` | `127.0.0.1:8000` |
| **Systemd Service** | `gunicorn_blottogbar.service` | `gunicorn_simpleplanner.service` |
| **Database** | PostgreSQL (`blottogbar`) | PostgreSQL (`simple_planner`) |
| **Nginx Site** | `/etc/nginx/sites-available/blottogbar.no` | `/etc/nginx/sites-available/simpleplanner.blottogbar.no` |

---

## ⚡ Fast Automated 1-Command Deployment (Recommended)

After cloning the repository onto your VPS, you can run the included automated setup script to handle everything (packages, PostgreSQL, `.env`, virtualenv, migrations, static assets, Gunicorn service, and Nginx site config):

```bash
# 1. Create web directory & clone repository
sudo mkdir -p /var/www/blottogbar
sudo chown -R $USER:www-data /var/www/blottogbar
git clone <YOUR_GIT_REPO_URL> /var/www/blottogbar

# 2. Run the automated deployment script
cd /var/www/blottogbar
sudo bash deploy.sh
```

*(Once complete, follow the prompt to activate SSL with `sudo certbot --nginx -d blottogbar.no -d www.blottogbar.no`)*

---

## Step-by-Step Manual Setup

### 1. PostgreSQL Database & User
```bash
sudo -u postgres psql -c "CREATE USER blottogbar_user WITH PASSWORD 'YOUR_STRONG_DB_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE blottogbar OWNER blottogbar_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE blottogbar TO blottogbar_user;"
```

### 2. Virtual Environment & Dependencies
```bash
cd /var/www/blottogbar
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Production Environment Variables (`.env`)
Create `/var/www/blottogbar/.env`:
```ini
DEBUG=False
SECRET_KEY=GENERATE_A_LONG_RANDOM_SECRET_KEY
ALLOWED_HOSTS=blottogbar.no,www.blottogbar.no,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://blottogbar.no,https://www.blottogbar.no
DB_NAME=blottogbar
DB_USER=blottogbar_user
DB_PASSWORD=YOUR_STRONG_DB_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=5432
```
```bash
chmod 600 /var/www/blottogbar/.env
```

### 4. Migrations & Static Collection
```bash
cd /var/www/blottogbar
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo chown -R www-data:www-data /var/www/blottogbar
sudo chmod -R 755 /var/www/blottogbar/static
```

### 5. Systemd Gunicorn Service (`/etc/systemd/system/gunicorn_blottogbar.service`)
```ini
[Unit]
Description=Gunicorn daemon for Blott og Bar Landing Page
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/blottogbar
EnvironmentFile=/var/www/blottogbar/.env
ExecStart=/var/www/blottogbar/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8001 \
          --access-logfile - \
          --error-logfile - \
          blottogbar_project.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn_blottogbar
sudo systemctl enable gunicorn_blottogbar
```

### 6. Nginx Reverse Proxy (`/etc/nginx/sites-available/blottogbar.no`)
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name blottogbar.no www.blottogbar.no;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/blottogbar/static/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public, max-age=2592000";
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and test:
```bash
sudo ln -sf /etc/nginx/sites-available/blottogbar.no /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Issue SSL Certificate (Let's Encrypt)
```bash
sudo certbot --nginx -d blottogbar.no -d www.blottogbar.no --non-interactive --agree-tos --redirect -m your-email@example.com
```

---

## Verification & Logs

* **Check Service Status:** `sudo systemctl status gunicorn_blottogbar`
* **Live Gunicorn Logs:** `sudo journalctl -u gunicorn_blottogbar -f`
* **Nginx Error Logs:** `sudo tail -f /var/log/nginx/error.log`
* **Health Check:** `curl http://127.0.0.1:8001/health/`
