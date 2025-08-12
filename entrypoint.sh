# #!/usr/bin/env bash
# set -e
# python manage.py migrate --noinput
# python manage.py collectstatic --noinput
# exec "$@"

#!/usr/bin/env bash
set -e

# Migrations + statiques (pour WhiteNoise)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# (Option) Superuser auto si demandé via env vars
# A garder EN PERMANENCE en prod si ta DB est éphémère
#   DJANGO_CREATE_SUPERUSER=1
#   DJANGO_SUPERUSER_USERNAME=admin
#   DJANGO_SUPERUSER_EMAIL=toi@example.com
#   DJANGO_SUPERUSER_PASSWORD=UnMotDePasseSolide
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
fi

# Charger une fixture de démo à chaque déploiement
#   DJANGO_LOAD_FIXTURES=1   (à laisser activé si on veut des données à chaque redeploy)
if [ "${DJANGO_LOAD_FIXTURES}" = "1" ] && [ -f "fixtures/seed.json" ]; then
  python manage.py loaddata fixtures/seed.json || true
  echo "[entrypoint] Loaded fixtures/seed.json"
fi

# Démarre Gunicorn (CMD du Dockerfile)
exec "$@"
