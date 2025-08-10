"""Vues publiques de l'app racine oc_lettings_site (homepage)."""

from django.shortcuts import render

def index(request):
    """Page d'accueil du site.

    Affiche un aperçu et des liens vers lettings et profiles.

    Args:
        request (HttpRequest): Requête HTTP.

    Returns:
        HttpResponse: Page HTML d'accueil.
    """
    
    return render(request, "index.html")
