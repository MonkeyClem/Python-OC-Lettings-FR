"""Vues publiques de l'app profiles (liste et détail)."""

from django.http import Http404
from django.shortcuts import get_object_or_404, render
import sentry_sdk
from profiles.models import Profile
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    """Liste tous les profils utilisateurs.

    Args:
        request (HttpRequest): Requête HTTP.

    Returns:
        HttpResponse: Page HTML avec la liste des profils.
    """
    
    sentry_sdk.set_tag("feature", "profiles_index")
    logger.info("Listing all profiles")
    
    
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
    
    sentry_sdk.set_tag('feature', 'user_profile')
    sentry_sdk.set_context('user_profile', {'username' : username})

    if request.user.is_authenticated:
        # pas de PII: id uniquement
        sentry_sdk.set_user({"id": str(request.user.id)})
        
    try: 
        profile = get_object_or_404(Profile, user__username=username)
    except Http404:
        # 404 attendue -> breadcrumb seulement (pas un event)
        logger.info("User profile not found username=%s", username)
        raise
    except Exception:
        logger.exception('Unexpected error fetching username=%s',username)
        raise

    context = {"profile": profile}
    return render(request, "profile.html", context)
