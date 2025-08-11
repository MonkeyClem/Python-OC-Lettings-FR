"""Vues publiques de l'app racine oc_lettings_site (homepage)."""

from venv import logger
from django.shortcuts import render
import sentry_sdk

def index(request):
    """Page d'accueil du site.

    Affiche un aperçu et des liens vers lettings et profiles.

    Args:
        request (HttpRequest): Requête HTTP.

    Returns:
        HttpResponse: Page HTML d'accueil.
    """
    
    sentry_sdk.set_tag("feature", "home_page")
    logger.info("Accessing home page")
    
    return render(request, "index.html")


def custom_404_view(request, exception):
    """Vue personnalisée pour les 404."""
    sentry_sdk.set_tag("feature", "404_page")
    sentry_sdk.set_context("404_details", {
        "path": request.path,
        "method": request.method,
    })
    logger.info("404 Not Found: %s", request.path)
    return render(request, "404.html", status=404)
