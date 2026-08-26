# Blott og Bar — Landing Page (`blottogbar.no`)

Minimalist, lightweight, and fast Django landing page for **[blottogbar.no](https://www.blottogbar.no)** — showcasing the **Blott & Bar** suite of focused web utilities, prominently featuring **[Simple Planner](https://simpleplanner.blottogbar.no)**.

---

## ✨ Features

* **⚡ Pure & Simple Aesthetic**: Monochromatic palette, Inter and JetBrains Mono typography, ASCII badges, matching Simple Planner's design philosophy.
* **🎯 Showcase Hub**: Highlights live production apps (Simple Planner) with direct launch links, live status indicator, and preview cards.
* **🛡️ Dual Database Support**: Lightweight SQLite for zero-config local development and PostgreSQL for production.
* **🚀 Production-Ready**: Preconfigured Gunicorn systemd service, Nginx reverse proxy configuration, and 1-command VPS deployment script (`deploy.sh`).
* **🤝 Co-hosting Compatible**: Designed to run seamlessly alongside `simpleplanner.blottogbar.no` on the same VPS without port conflicts.

---

## 🛠️ Local Development Setup

### 1. Clone & Enter Directory
```bash
cd quick-turing
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize Environment & Database
```bash
cp .env.example .env
python manage.py migrate
```

### 4. Run Automated Tests
```bash
python manage.py test
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🚢 Production Deployment & Daily Updates

### Initial Setup
```bash
sudo bash deploy.sh
sudo certbot --nginx -d blottogbar.no -d www.blottogbar.no
```

### Daily Updates (1-Command)
Whenever you push code changes to GitHub, deploy them by running:
```bash
# On the VPS:
cd /var/www/blottogbar && sudo bash deploy.sh

# Or directly from your local terminal via SSH:
ssh root@YOUR_VPS_IP "cd /var/www/blottogbar && bash deploy.sh"
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full architecture and configuration documentation.
