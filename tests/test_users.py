import pytest

from users.models import User


@pytest.mark.django_db
def test_register(client):
    response = client.post("/api/users/register/", {"username": "new_user", "password": "1234"})

    assert response.status_code == 201
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_login(client, user):
    response = client.post("/api/users/login/", {"username": "test", "password": "1234"})

    assert response.status_code == 200
    assert "access" in response.data
