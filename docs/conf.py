# -- Path & Django setup -----------------------------------------------------
import os
import sys
from pathlib import Path

# 1) Ajouter la racine du projet au PYTHONPATH (docs/ -> racine)
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

# 2) Définir les variables d'env AVANT d'importer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
os.environ.setdefault("DJANGO_SECRET_KEY", "docs-build")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

import django  # noqa
django.setup()


# -- Project information -----------------------------------------------------
project = "Orange County Lettings"
author = "Équipe OC Lettings"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]
autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = []

# Intersphinx : utiliser None (et pointer la bonne version de Django)
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": ("https://docs.djangoproject.com/en/5.2/", None),
}
