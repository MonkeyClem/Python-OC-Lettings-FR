"""Vues publiques de l'app profiles (liste et détail)."""

from django.shortcuts import get_object_or_404, render
from profiles.models import Profile


# Create your views here.
def index(request):
    """Liste tous les profils utilisateurs.

    Args:
        request (HttpRequest): Requête HTTP.

    Returns:
        HttpResponse: Page HTML avec la liste des profils.
    """
    profiles_list = Profile.objects.all()
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)

def profile(request, username):
    """Affiche le profil d'un utilisateur.

    Args:
        request (HttpRequest): Requête HTTP.
        username (str): Nom d'utilisateur (auth.User.username).

    Returns:
        HttpResponse: Page HTML du profil.

    Raises:
        Http404: Si aucun profil n'est lié à ce nom d'utilisateur.
    """
    
    # profile = Profile.objects.get(user__username=username)
    profile = get_object_or_404(Profile, user__username = username )
    context = {"profile": profile}
    return render(request, "profile.html", context)
