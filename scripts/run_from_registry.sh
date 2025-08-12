#!/usr/bin/env bash
set -euo pipefail
IMAGE="${1:-docker.io/clementjeulin/oc-lettings:latest}"
USE_LOCAL_SQLITE="${USE_LOCAL_SQLITE:-0}"

echo "Pulling $IMAGE ..."
docker pull "$IMAGE"

OPTS=(
  -p 8000:8000
  -e DJANGO_DEBUG=0
  -e DJANGO_SECRET_KEY=local-prod-key
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
  -e DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
  -e DJANGO_SECURE_SSL_REDIRECT=0
  --rm
)

if [ "$USE_LOCAL_SQLITE" = "1" ]; then
  OPTS+=(-v "$PWD/oc-lettings-site.sqlite3:/app/oc-lettings-site.sqlite3")
fi

echo "Running on http://localhost:8000 ..."
exec docker run "${OPTS[@]}" "$IMAGE"
