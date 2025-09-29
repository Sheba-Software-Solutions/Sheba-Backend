# Render Deployment Setup (Backend + Admin Frontend)

This guide walks you through deploying the Django backend to Render with a one-time admin creation (no shell access) and configuring the Admin frontend to talk to the backend API.

---

## 1) Backend (Render) – Service settings

Create a “Web Service” on Render pointing to your GitHub repo (Sheba-Backend). Use these settings.

- Build Command:
```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

- Start Command (normal, for every deploy after the admin is created):
```
python manage.py migrate && gunicorn sheba_admin_backend.wsgi:application --bind 0.0.0.0:8000
```

- Health Check Path (recommended):
```
/admin/login/
```

- Python Version
  - If needed, set this environment variable:
```
RENDER_PYTHON_VERSION=3.12
```

### Required environment variables (copy/paste)

Replace domains and secrets with your actual values. Do NOT include trailing slashes in CORS origins, and ALWAYS include schemes (https://) in CSRF trusted origins.

```
# Security & settings
DJANGO_SETTINGS_MODULE=sheba_admin_backend.production_settings
SECRET_KEY=generate-a-strong-secret
DEBUG=False

# Hosts (no scheme)
ALLOWED_HOSTS=sheba-backend-EXAMPLE.onrender.com,.onrender.com,localhost,127.0.0.1

# CSRF: must include scheme and no trailing slash
CSRF_TRUSTED_ORIGINS=https://sheba-backend-EXAMPLE.onrender.com,https://sheba-admin-EXAMPLE.vercel.app

# CORS: origins only, no paths and no trailing slashes
CORS_ALLOWED_ORIGINS=https://sheba-admin-EXAMPLE.vercel.app,https://your-website-domain.com

# Database
# Either let Render inject DATABASE_URL from a managed Postgres:
# DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
```

Notes:
- ALLOWED_HOSTS should contain your exact Render URL and optionally “.onrender.com”.
- CSRF_TRUSTED_ORIGINS must start with https:// (Django 4+ requirement).
- CORS_ALLOWED_ORIGINS must not contain paths or trailing slashes.

---

## 2) One-time superuser creation on Render (no shell access)

Add these environment variables temporarily (so Django can create the superuser non-interactively):

```
DJANGO_SUPERUSER_USERNAME=admin_username
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=ChangeMeToAStrongPassword
```

Then temporarily change the Start Command to this one-liner (copy/paste):

```
python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py shell -c 'import os; from authentication.models import User; u=User.objects.filter(username=os.environ.get("DJANGO_SUPERUSER_USERNAME")).first(); 
if u:
    u.role="admin"; u.is_staff=True; u.is_superuser=True; u.save()' || true && gunicorn sheba_admin_backend.wsgi:application --bind 0.0.0.0:8000
```

- Deploy once. This will:
  - Run migrations
  - Create the superuser (idempotent due to “|| true”)
  - Ensure the user has role="admin", is_staff=True, is_superuser=True
  - Start gunicorn
- After it’s live and you’ve confirmed login, revert the Start Command back to:

```
python manage.py migrate && gunicorn sheba_admin_backend.wsgi:application --bind 0.0.0.0:8000
```

- Optionally remove the three DJANGO_SUPERUSER_* env vars after the account is created.

---

## 3) Alternative: Create users locally into the Render database

If you prefer creating users from your machine directly into the Render Postgres:

```
# In your local terminal (with your virtualenv active)
export DATABASE_URL="paste-render-postgres-connection-string"

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Force role=admin (since default role is "client")
python manage.py shell -c "from authentication.models import User; u=User.objects.get(username='YOUR_USERNAME'); u.role='admin'; u.is_staff=True; u.is_superuser=True; u.save()"
```

This writes directly into the production DB, no Render shell needed.

---

## 4) Admin Frontend configuration (Sheba-Admin)

Set the following environment variables in your Admin frontend hosting (e.g., Vercel):

```
VITE_API_BASE_URL=https://sheba-backend-EXAMPLE.onrender.com/api

# Optional (override defaults)
# VITE_TOKEN_KEY=auth_token
# VITE_USER_KEY=user_data
```

Notes:
- The Admin expects APIs under “/api/...”.
- We’ve normalized API helper paths to be relative to the base URL.

---

## 5) Verify deployment

- Backend (Render)
  - Django Admin: https://sheba-backend-EXAMPLE.onrender.com/admin/login/
  - Health check should return 200 OK at /admin/login/
  - 404s at “/” are normal unless you add a root route

- API quick checks (requires token auth)
  - POST https://sheba-backend-EXAMPLE.onrender.com/api/auth/login/
  - GET  https://sheba-backend-EXAMPLE.onrender.com/api/dashboard/overview/
  - Use “Authorization: Token <your_token>”

- Admin Frontend (Vercel)
  - Confirm network calls go to https://sheba-backend-EXAMPLE.onrender.com/api/*
  - If you see 401s, verify VITE_API_BASE_URL and that login succeeded (token present).

---

## 6) Common errors and fixes

- DisallowedHost / Invalid HTTP_HOST
  - Add your Render domain to ALLOWED_HOSTS (no schemes)
  - Example: `ALLOWED_HOSTS=sheba-backend-EXAMPLE.onrender.com,.onrender.com,localhost,127.0.0.1`

- CSRF_TRUSTED_ORIGINS format error
  - Must include scheme (https://) and no trailing slash.
  - Example: `CSRF_TRUSTED_ORIGINS=https://sheba-backend-EXAMPLE.onrender.com,https://sheba-admin-EXAMPLE.vercel.app`

- CORS origin error (E014)
  - Remove trailing slash, and ensure there’s no path.
  - Example: `CORS_ALLOWED_ORIGINS=https://sheba-admin-EXAMPLE.vercel.app,https://your-website-domain.com`

- collectstatic flag typo
  - Use `--noinput` (two dashes), not `-noinput`.

- PostgreSQL driver on different Python versions
  - requirements.txt selects a compatible driver automatically:
    - `psycopg2-binary` for Python < 3.13
    - `psycopg[binary]` for Python >= 3.13
  - On Render (Python 3.12), `psycopg2-binary` installs as a prebuilt wheel (no pg_config needed).

---

## 7) Optional niceties

- If you want “/” to return 200 instead of 404, add a simple root view and URL in your Django project. Not required; setting the Health Check Path to `/admin/login/` is cleaner.

---

That’s it! After the one-time admin creation, you can manage all users and roles from Django Admin (or through your API) and keep deploying normally with the standard Start Command.