from django.contrib import admin
from django.urls import include, path
from . import views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("", views.index, name="index"),
    path("lettings/", include("lettings.urls", namespace="lettings")),
    # path("lettings/<int:letting_id>/", views.letting, name="letting"),
    path("profiles/", include("profiles.urls", namespace="profiles")),
    # path("profiles/<str:username>/", views.profile, name="profile"),
    path('sentry-debug/', trigger_error),
    path("admin/", admin.site.urls),
]
