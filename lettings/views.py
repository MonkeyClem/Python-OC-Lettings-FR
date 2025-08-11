"""Vues publiques de l'app lettings (liste et détail)."""

import logging
from django.http import Http404
from django.shortcuts import get_object_or_404, render
import sentry_sdk
from lettings.models import Letting
from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """Liste toutes les locations.

    Args:
        request (HttpRequest): Requête HTTP.

    Returns:
        HttpResponse: Page HTML avec la liste des locations.
    """

    logger.info("Listing all lettings")
    sentry_sdk.set_tag("feature", "lettings_index")
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

    sentry_sdk.set_tag("feature", "letting_detail")
    sentry_sdk.set_context("letting_lookup", {"letting_id": letting_id})
    if request.user.is_authenticated:
        sentry_sdk.set_user({"id": str(request.user.id)})

    logger.info("Fetching letting id=%s", letting_id)
    # Déclenchement d'un log ERROR pour test
    # logger.error("Test log ERROR pour Sentry")

    try:
        # Astuce perf: va chercher l'adresse en même temps
        letting = get_object_or_404(
            Letting.objects.select_related("address"), id=letting_id
        )
    except Http404:
        # 404 attendue -> breadcrumb seulement (pas un event)
        logger.info("Letting not found id=%s", letting_id)
        raise
    except Exception:
        # Erreur inattendue -> event Sentry + stacktrace
        logger.exception("Unexpected error fetching letting id=%s", letting_id)
        raise

    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "letting.html", context)
