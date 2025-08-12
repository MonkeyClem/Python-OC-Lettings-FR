#!/usr/bin/env bash
set -e

echo "[entrypoint] Starting…"
echo "[entrypoint] PWD=$(pwd)"
echo "[entrypoint] DJANGO_CREATE_SUPERUSER=${DJANGO_CREATE_SUPERUSER:-0} (password hidden)"
echo "[entrypoint] DJANGO_LOAD_FIXTURES=${DJANGO_LOAD_FIXTURES:-0}"

# 0) Sanity: manage.py présent ?
if [ ! -f "manage.py" ]; then
  echo "[entrypoint][FATAL] manage.py not found in PWD. Check WORKDIR/COPY in Dockerfile."
  exit 1
fi

# 1) Migrations + collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 2) Superuser (création/màj si demandé)
if [ "${DJANGO_CREATE_SUPERUSER}" = "1" ]; then
python <<'PY'
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
u = User.objects.filter(username=username).first()
if u:
    if password:
        u.set_password(password); u.email=email; u.is_superuser=True; u.is_staff=True; u.save()
        print(f"[entrypoint] Updated superuser '{username}'")
    else:
        print(f"[entrypoint] Superuser '{username}' exists; no password change.")
else:
    if not password:
        raise SystemExit("[entrypoint] Set DJANGO_SUPERUSER_PASSWORD to create the superuser.")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"[entrypoint] Created superuser '{username}'")
PY
else
  echo "[entrypoint] DJANGO_CREATE_SUPERUSER != 1 (skip)"
fi

# 3) Fixtures (chargement strict)
if [ "${DJANGO_LOAD_FIXTURES}" = "1" ]; then
  if [ -f "fixtures/seed.json" ]; then
    echo "[entrypoint] Loading fixtures/seed.json…"
    python manage.py loaddata fixtures/seed.json
    echo "[entrypoint] Fixtures loaded OK."
  else
    echo "[entrypoint][FATAL] DJANGO_LOAD_FIXTURES=1 but fixtures/seed.json is missing."
    ls -la fixtures || true
    exit 1
  fi
else
  echo "[entrypoint] DJANGO_LOAD_FIXTURES != 1 (skip)"
fi

echo "[entrypoint] Handing off to CMD: $*"
exec "$@"
