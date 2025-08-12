# scripts/run-from-registry.ps1
param(
  [string]$Image = "docker.io/clementjeulin/oc-lettings:latest",
  [switch]$UseLocalSqlite
)

Write-Host "Pulling $Image ..."
docker pull $Image | Out-Host

$envs = @(
  "-e","DJANGO_DEBUG=0",
  "-e","DJANGO_SECRET_KEY=local-prod-key",
  "-e","DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1",
  "-e","DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1",
  "-e","DJANGO_SECURE_SSL_REDIRECT=0"
)

$vol = @()
if ($UseLocalSqlite) {
  $vol = @("-v","${PWD}\oc-lettings-site.sqlite3:/app/oc-lettings-site.sqlite3")
}

Write-Host "Running on http://localhost:8000 ..."
docker run --rm -p 8000:8000 @vol @envs $Image
