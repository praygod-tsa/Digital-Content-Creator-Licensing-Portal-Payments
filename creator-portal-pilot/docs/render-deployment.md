# Render deployment checklist (Django + Postgres)

This project deploys as:
- **Web Service**: Django app (`creator-portal-pilot` root directory)
- **Postgres**: managed database (`creator-portal-db`) **or** Supabase Postgres

## 1) Required Render services

1. Create **Postgres** database first (Render or Supabase).
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

### Database option A (recommended): Render Postgres
- `DATABASE_URL=<Render Postgres connection string>`

### Database option B: Supabase Postgres
- `SUPABASE_DATABASE_URL=<Supabase Postgres connection string>`
- Optional: `SUPABASE_URL=<https://your-project.supabase.co>`
- Optional: `SUPABASE_PUBLISHABLE_KEY=<sb_publishable_...>`

> Important:
> - Do not wrap DB URLs in quotes.
> - `SUPABASE_URL` + `SUPABASE_PUBLISHABLE_KEY` are **not** a SQL connection string. They cannot replace `DATABASE_URL`.

## 4) First deploy after service is live

Open Render Shell for the Web Service and run:

```bash
python manage.py createsuperuser
python manage.py setup_roles_and_fees
```

## 5) Troubleshooting quick notes

- If build fails before migrations, verify **Root Directory** is exactly `creator-portal-pilot`.
- If DB parse errors appear, check `DATABASE_URL` / `SUPABASE_DATABASE_URL` is present and valid, with no extra quotes.
- If CSRF errors appear on login/admin, verify `CSRF_TRUSTED_ORIGINS` includes your HTTPS URL.
- If static files missing, redeploy once after successful build/migrate.
