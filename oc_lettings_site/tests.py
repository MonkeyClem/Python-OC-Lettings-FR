import pytest
from django.contrib.auth.models import User
from profiles.models import Profile


def test_dummy():
    assert 1


@pytest.mark.django_db
def test_profile_str():
    user = User.objects.create_user(username="alice", password="x")
    profile = Profile.objects.create(user=user, favorite_city="Paris")
    assert str(profile) == "alice"
