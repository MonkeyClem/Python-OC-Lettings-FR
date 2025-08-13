Procédures de déploiement & gestion
===================================

Docker local
------------
.. code-block:: bash

   docker build -t oclettings:local .
   docker run --rm -p 8000:8000 \
     -e DJANGO_SECRET_KEY=devsecret \
     -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost \
     oclettings:local

CI/CD (GitHub Actions)
----------------------
- Job *test*: flake8 + pytest + coverage
- Job *docker*: build & push image (tag latest + SHA)
- Job *deploy*: déclenche le déploiement (ex: Render)

Production (ex: Render)
-----------------------
- Déployer l’image Docker Hub
- Variables d’env: SECRET_KEY, ALLOWED_HOSTS, SENTRY_DSN
- Gunicorn + Whitenoise (servir statiques)
- Migrations au démarrage (CMD du Dockerfile)
