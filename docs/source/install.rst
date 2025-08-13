Installation du projet
======================

Prérequis: Python 3.10, Git, pip.

Clonage & env
-------------
.. code-block:: bash

   git clone https://github.com/MonkeyClem/Python-OC-Lettings-FR
   cd Python-OC-Lettings-FR
   python -m venv venv
   Windows: venv\Scripts\activate # MAC : source venv/bin/activate  #
   pip install -r requirements.txt

Configuration
-------------
Variables d’environnement minimales:

- ``DJANGO_SECRET_KEY`` (obligatoire en prod)
- ``DJANGO_ALLOWED_HOSTS`` (ex: 127.0.0.1,localhost en dev)
- ``DJANGO_DEBUG`` (true/false - 0 ou 1 -)
- ``SENTRY_DSN`` (optionnel)

Lancement
--------
.. code-block:: bash

   python manage.py migrate
   python manage.py runserver
