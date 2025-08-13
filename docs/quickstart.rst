Guide de démarrage rapide
=========================

1. Créer des données via l’admin (http://127.0.0.1:8000/admin/)
2. Parcourir:
   - /lettings/
   - /profiles/
3. Lancer les tests:
.. code-block:: bash

   pytest --cov=. --cov-report=term-missing
