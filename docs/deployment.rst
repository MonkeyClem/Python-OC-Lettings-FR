Tests en local avec Docker
===========================

Deux possibilités pour tester l’application localement avec Docker :

1. **Utiliser le code local** pour builder une image et tester les derniers changements
2. **Utiliser l’image depuis Docker Hub**, pour simuler l’environnement de production (image déployée)

Méthode 1 : Docker local (avec code source)
-------------------------------------------

.. code-block:: bash

   docker build -t oclettings:local .
   docker run --rm -p 8000:8000 \
     -e DJANGO_SECRET_KEY=devsecret \
     -e DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost \
     oclettings:local

Alternativement, avec `docker-compose` :

.. code-block:: bash

   docker-compose up --build

Ce mode permet :
- De monter un volume pour conserver la base SQLite (`volumes`)
- De tester avec la même stack (gunicorn, etc.) que la prod

Méthode 2 : Docker Hub (image de production)
--------------------------------------------

.. code-block:: bash

   docker run --rm -p 8000:8000 \
     -e DJANGO_SECRET_KEY=devsecret \
     -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
     -e DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1 \
     -e DJANGO_SECURE_SSL_REDIRECT=0 \
     clementjeulin/oc-lettings:latest

Tester une version spécifique (rollback possible) :

.. code-block:: bash

   docker run ... clementjeulin/oc-lettings:<sha_git_commit>

Utiliser le script Bash ou PowerShell fourni :

.. code-block:: bash

