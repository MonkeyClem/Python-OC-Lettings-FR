"""Vues publiques de l'app lettings (liste et détail)."""

from django.shortcuts import get_object_or_404, render
from lettings.models import Letting

def index(request):
    """Liste toutes les locations.

    Args:
        request (HttpRequest): Requête HTTP.

    Returns:
        HttpResponse: Page HTML avec la liste des locations.
    """
    
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)



def letting(request, letting_id):
    """Affiche le détail d'une location.

    Args:
        request (HttpRequest): Requête HTTP.
        letting_id (int): Identifiant de la location.

    Returns:
        HttpResponse: Page HTML du détail de la location.

    Raises:
        Http404: Si aucune location ne correspond à l'ID fourni.
    """
    
    letting = get_object_or_404(Letting, id=letting_id) 
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "letting.html", context)
