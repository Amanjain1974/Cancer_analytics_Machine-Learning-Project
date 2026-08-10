# 🚀 Production Deployment Guide

This guide outlines step-by-step instructions for deploying the **Cancer Risk & Survival Prognosis Intelligence System** to cloud providers (Render, Railway, Heroku), Docker containers, or virtual private servers (VPS/AWS/DigitalOcean).

---

## 🛠️ Environment Variables Checklist

Before deploying, ensure the following environment variables are set in your platform's configuration dashboard:

| Variable | Recommended Production Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(A long randomly generated string)* | Django secret key for cryptographic signing |
| `DEBUG` | `False` | Disables verbose debug pages and security leak warnings |
| `ALLOWED_HOSTS` | `.onrender.com,yourdomain.com` | Comma-separated list of allowed host domains |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com,https://yourdomain.com` | Trusted origins for CSRF protection over HTTPS |
| `PORT` | `8000` | Port for Gunicorn server (automatically set by most PaaS) |

---

## Option 1: Deploy on Render (Recommended)

Render natively reads the included `render.yaml` and `build.sh` configuration files.

1. **Push your code to GitHub / GitLab**.
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** -> **Blueprint**.
4. Connect your GitHub repository.
5. Render will automatically detect `render.yaml` and configure:
   - **Build Command**: `./build.sh` (installs dependencies, applies database migrations, collects static files)
   - **Start Command**: `gunicorn cancer_ai.wsgi:application`
6. Click **Apply**. Your app will build and deploy live with an HTTPS URL.

---

## Option 2: Deploy with Docker & Docker Compose

### Using Docker Compose
Run the entire production web stack locally or on a VPS with a single command:

```bash
# 1. Build and start container in detached mode
docker-compose up --build -d

# 2. Verify running status
docker-compose ps

# 3. View container logs
docker-compose logs -f
```

### Using Standalone Docker Container

```bash
# Build Docker image
docker build -t cancer-ai-app .

# Run Docker container on port 8000
docker run -d -p 8000:8000 --name cancer-ai -e DEBUG=False -e SECRET_KEY="your-secret-key" cancer-ai-app
```

---

## Option 3: Deploy on Railway / Heroku / PaaS

The repository includes a production `Procfile`.

1. **Connect Repository**: Link your GitHub repo to Railway / Heroku.
2. **Build Settings**:
   - Build Command: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn cancer_ai.wsgi:application`
3. **Environment Variables**: Add `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=*`, and `CSRF_TRUSTED_ORIGINS`.

---

## Option 4: Deploy on Linux VPS (Ubuntu / AWS EC2 / DigitalOcean)

### 1. System Setup
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip nginx git
git clone <your-repo-url> /var/www/cancer-ml-project
cd /var/www/cancer-ml-project

# Virtual Environment Setup
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Database & Static Assets
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3. Setup Systemd Gunicorn Service (`/etc/systemd/system/cancer_ai.service`)
```ini
[Unit]
Description=Cancer AI Gunicorn Daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/cancer-ml-project
ExecStart=/var/www/cancer-ml-project/venv/bin/gunicorn --config gunicorn.conf.py cancer_ai.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start cancer_ai
sudo systemctl enable cancer_ai
```

---

## 🔍 Verification & Health Check

After deploying, verify the deployment:

1. **Run System Checks**:
   ```bash
   python manage.py check --deploy
   ```
2. **Static Asset Verification**: Confirm CSS, JavaScript, and Bootstrap icons load cleanly (served by WhiteNoise).
3. **AI Model Verification**: Perform a test prediction in both **Module 1 (Pre-Diagnosis Risk Assessment)** and **Module 2 (Post-Diagnosis Survival Prognosis)** to confirm `model_pipeline.pkl` and `survival_pipeline.pkl` are loaded in memory.
