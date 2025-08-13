# # Configuration file for the Sphinx documentation builder.
# #
# # For the full list of built-in configuration values, see the documentation:
# # https://www.sphinx-doc.org/en/master/usage/configuration.html

# # -- Project information -----------------------------------------------------
# # https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# project = 'Orange County Lettings'
# copyright = '2025, Clément Jeulin'
# author = 'Clément Jeulin'
# release = '1.0.0'

# # -- General configuration ---------------------------------------------------
# # https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []

# templates_path = ['_templates']
# exclude_patterns = []

# language = 'fr'

# # -- Options for HTML output -------------------------------------------------
# # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']




# -- Path & Django setup -----------------------------------------------------
import os
import sys
import django  # noqa
django.setup()

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
os.environ.setdefault("DJANGO_SECRET_KEY", "docs-build")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")



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
html_static_path = ["_static"]

# -- Intersphinx (optionnel) -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", {}),
    "django": ("https://docs.djangoproject.com/en/3.2/", {}),
}
