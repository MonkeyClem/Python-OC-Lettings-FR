## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`





## Déploiement (CI/CD)

### Vue d’ensemble
- **Branches ≠ `master`** : la CI exécute `flake8` + `pytest` avec couverture ≥ 80%.
- **Branche `master`** : si tests OK → **build & push** de l’image Docker sur Docker Hub
  (`clementjeulin/oc-lettings` tags `latest` + `<commit_sha>`) → **déclenchement** du
  déploiement Render via **Deploy Hook** → Render redémarre le conteneur et exécute :
  `migrate` + `collectstatic` + (optionnel) création superuser + (optionnel) chargement d’une fixture.

### Prérequis
- **Docker Hub**
  - Repo public : `clementjeulin/oc-lettings`
  - Secrets GitHub :  
    - `DOCKERHUB_USERNAME=clementjeulin`  
    - `DOCKERHUB_TOKEN=<Access Token Docker Hub (Read/Write)>`
- **Render (Web Service → Existing Image)**
  - Image : `docker.io/clementjeulin/oc-lettings:latest`
  - Port : `8000` (Gunicorn écoute sur `0.0.0.0:8000`)
  - Start command : _vide_ (on garde le `CMD` du Dockerfile)
  - Variables d’environnement minimales :
    - `DJANGO_DEBUG=0`
    - `DJANGO_SECRET_KEY=<valeur robuste>`
    - `DJANGO_ALLOWED_HOSTS=<mon-service>.onrender.com`
    - `DJANGO_CSRF_TRUSTED_ORIGINS=https://<mon-service>.onrender.com`
    - `DJANGO_SECURE_SSL_REDIRECT=1`
  - Variables d’environnement conseillées (prod SQLite **éphémère**) :
    - `DJANGO_CREATE_SUPERUSER=1`
    - `DJANGO_SUPERUSER_USERNAME=admin`
    - `DJANGO_SUPERUSER_EMAIL=admin@example.com`
    - `DJANGO_SUPERUSER_PASSWORD=<unmotdepassesolide>`
    - `DJANGO_LOAD_FIXTURES=1` (si `fixtures/seed.json` est présent dans le repo)
- **GitHub Actions (secrets)** :
  - `RENDER_DEPLOY_HOOK_URL=<URL du Deploy Hook Render>` (sinon l’étape `deploy` est skippée)

### Déployer (pipeline complet)
1. Pousser sur **`master`** (ou **Run workflow** dans l’onglet *Actions* → *Release*).
2. La CI lance : lint + tests + couverture (≥80%).  
3. Si OK : build & push de l’image (`latest` + `<commit_sha>`) sur Docker Hub.
4. Si OK : appel du **Deploy Hook** Render → Render redéploie et exécute au boot :
   - `python manage.py migrate --noinput`
   - `python manage.py collectstatic --noinput`
   - si `DJANGO_CREATE_SUPERUSER=1` : crée/maj un superuser
   - si `DJANGO_LOAD_FIXTURES=1` : `python manage.py loaddata fixtures/seed.json`
5. Le site est disponible sur `https://<mon-service>.onrender.com/`.



### Tester localement depuis l’image du registre (Docker uniquement)
docker pull docker.io/clementjeulin/oc-lettings:latest
docker run --rm -p 8000:8000 `
  -e DJANGO_DEBUG=0 `
  -e DJANGO_SECRET_KEY=local-prod-key `
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 `
  -e DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1 `
  -e DJANGO_SECURE_SSL_REDIRECT=0 `
  docker.io/clementjeulin/oc-lettings:latest

Option : persister la DB locale entre runs (Windows)
docker run --rm -p 8000:8000 `
  -v "${PWD}\oc-lettings-site.sqlite3:/app/oc-lettings-site.sqlite3" `
  -e DJANGO_DEBUG=0 `
  -e DJANGO_SECRET_KEY=local-prod-key `
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 `
  -e DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1 `
  -e DJANGO_SECURE_SSL_REDIRECT=0 `
  docker.io/clementjeulin/oc-lettings:latest

## Notes 
SQLite en prod sur Render (offre Free/Starter) : la DB est éphémère → on garde
DJANGO_CREATE_SUPERUSER=1 et, si besoin, DJANGO_LOAD_FIXTURES=1 pour regarnir la base à chaque déploiement.

Pour une prod persistante : passer à PostgreSQL managé (Render), exposé par DATABASE_URL