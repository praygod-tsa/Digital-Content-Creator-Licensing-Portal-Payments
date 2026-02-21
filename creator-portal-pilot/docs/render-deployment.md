# Render deployment checklist (Django + Postgres)

This project deploys as:
- **Web Service**: Django app (`creator-portal-pilot` root directory)
- **Postgres**: managed database (`creator-portal-db`)

## 1) Required Render services

1. Create **Postgres** database first.
2. Create **Web Service** and connect this repository.

If using Render Blueprint, deploy from `render.yaml` at repository root.

## 2) Web Service settings (manual setup)

- **Runtime**: Python
- **Root Directory**: `creator-portal-pilot`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`

## 3) Environment variables

Set these in Web Service > Environment:

- `PYTHON_VERSION=3.11.9`
- `SECRET_KEY=<strong-random-value>`
- `DEBUG=False`
- `ALLOWED_HOSTS=<your-web-service-host>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-web-service-host>.onrender.com`
- `DATABASE_URL=<Render Postgres connection string>`

> Important: do not wrap `DATABASE_URL` in quotes.

## 4) First deploy after service is live

Open Render Shell for the Web Service and run:

```bash
python manage.py createsuperuser
python manage.py setup_roles_and_fees
```

## 5) Troubleshooting quick notes

- If build fails before migrations, verify **Root Directory** is exactly `creator-portal-pilot`.
- If DB parse errors appear, check `DATABASE_URL` is present and valid, no extra quotes.
- If CSRF errors appear on login/admin, verify `CSRF_TRUSTED_ORIGINS` includes your HTTPS URL.
- If static files missing, redeploy once after successful build/migrate.
