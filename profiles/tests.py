import pytest
from django.contrib.auth.models import User
from profiles.models import Profile
from django.urls import reverse

"""Tests des modèles profiles."""

@pytest.mark.django_db
def test_profile_str():
    user = User.objects.create_user(username="alice", password="x")
    profile = Profile.objects.create(user=user, favorite_city="Paris")
    assert str(profile) == "alice"

"""Tests d'URLs de l'app profiles."""

@pytest.mark.django_db
def test_profiles_index_url_ok(client):
    resp = client.get(reverse("profiles:index"))
    assert resp.status_code == 200

@pytest.mark.django_db
def test_profile_detail_url_ok(client):
    user = User.objects.create_user(username="bob", password="x")
    Profile.objects.create(user=user, favorite_city="Lyon")
    url = reverse("profiles:profile", kwargs={"username": "bob"})
    resp = client.get(url)
    assert resp.status_code == 200



@pytest.mark.django_db
def test_index_lists_profiles(client):
    """Tests des vues profiles (liste et détail)."""
    user = User.objects.create_user(username="zoe", password="x")
    Profile.objects.create(user=user, favorite_city="Nice")
    resp = client.get(reverse("profiles:index"))
    assert resp.status_code == 200
    assert b"zoe" in resp.content

@pytest.mark.django_db
def test_detail_404_when_missing(client):
    resp = client.get(reverse("profiles:profile", kwargs={"username": "nope"}))
    assert resp.status_code == 404

@pytest.mark.django_db
def test_profile_view_ok(client):
    user = User.objects.create(username="john")
    Profile.objects.create(user=user, favorite_city="Paris")
    url = reverse("profiles:profile", kwargs={"username": "john"})
    response = client.get(url)
    assert response.status_code == 200
    assert b"Paris" in response.content

@pytest.mark.django_db
def test_profile_view_404(client):
    url = reverse("profiles:profile", kwargs={"username": "nope"})
    response = client.get(url)
    assert response.status_code == 404
    