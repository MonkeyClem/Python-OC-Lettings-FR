import pytest
from lettings.models import Address, Letting
from django.urls import reverse

# Create your tests here.
@pytest.mark.django_db
def test_address_str():
    addr = Address.objects.create(
        number=10, street="Main", city="LA", state="CA", zip_code=90001, country_iso_code="USA"
    )
    assert str(addr) == "10 Main"

@pytest.mark.django_db
def test_letting_str():
    addr = Address.objects.create(
        number=1, street="X", city="Y", state="CA", zip_code=1, country_iso_code="USA"
    )
    letting = Letting.objects.create(title="Nice house", address=addr)
    assert str(letting) == "Nice house"
    
    
    
"""Tests d'URLs de l'app lettings."""

@pytest.mark.django_db
def test_lettings_index_url_ok(client):
    resp = client.get(reverse("lettings:index"))
    assert resp.status_code == 200

@pytest.mark.django_db
def test_letting_detail_url_ok(client):
    addr = Address.objects.create(number=1, street="X", city="Y", state="CA", zip_code=1, country_iso_code="USA")
    letting = Letting.objects.create(title="Test", address=addr)
    url = reverse("lettings:letting", kwargs={"letting_id": letting.id})
    resp = client.get(url)
    assert resp.status_code == 200  

"""Tests des vues lettings (liste et détail)."""

@pytest.mark.django_db
def test_index_lists_lettings(client):
    addr = Address.objects.create(number=2, street="Rue", city="Paris", state="CA", zip_code=75000, country_iso_code="FRA")
    Letting.objects.create(title="T1", address=addr)
    resp = client.get(reverse("lettings:index"))
    assert resp.status_code == 200
    assert b"T1" in resp.content 

@pytest.mark.django_db
def test_detail_404_when_missing(client):
    resp = client.get(reverse("lettings:letting", kwargs={"letting_id": 999999}))
    assert resp.status_code == 404
