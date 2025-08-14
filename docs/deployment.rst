Procédures de déploiement & gestion
===================================

Docker local (développement/test)
----------------------------------
Pour tester localement l’image *sans Docker Compose* :

.. code-block:: bash

   docker build -t oclettings:local .
   docker run --rm -p 8000:8000 \
     -e DJANGO_SECRET_KEY=devsecret \
     -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost \
     oclettings:local

Alternativement, utiliser `docker-compose` :

.. code-block:: bash

   docker-compose up --build

Ce mode permet :
- De monter un volume pour conserver la base SQLite (`volumes`)
- De tester l'app avec la configuration proche de la prod

CI/CD (GitHub Actions)
----------------------
Le pipeline `release.yml` est déclenché sur `push` vers `master`.  
Il contient 3 jobs :

- **test-and-lint** :
  - Linting (flake8)
  - Tests unitaires (pytest)
  - Couverture de code (≥ 80%)
  - Échec = pipeline stoppé

- **build-and-push** :
  - Construction de l’image Docker
  - Push sur Docker Hub (tag `latest` et `SHA`)

- **deploy** :
  - Déclenchement du déploiement via `RENDER_DEPLOY_HOOK_URL` (webhook Render)

Production (Render)
-------------------
Le service Render est configuré pour tirer l’image Docker *depuis Docker Hub*.  
Le déploiement se fait automatiquement après un push réussi.

Rappel de configuration :

- Déploiement via image Docker (pas depuis GitHub)
- Variables d’environnement :
  - `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, `SENTRY_DSN`, etc.
- Port exposé : `8000`
- Commande finale : `gunicorn oc_lettings_site.wsgi:application`

Le fichier `entrypoint.sh` exécuté au lancement :
- Applique les migrations Django
- Collecte les fichiers statiques (`collectstatic`)
- Crée un superuser si demandé (`DJANGO_CREATE_SUPERUSER`)
- Charge les fixtures si configuré (`DJANGO_LOAD_FIXTURES`)
- Lance ensuite Gunicorn

Base de données en production :
- SQLite embarquée dans le conteneur
- Pas de persistance hors du conteneur (⚠️ perte de données possible si pas sauvegardées dans `seed.json`)
