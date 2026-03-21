import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="1234")


@pytest.fixture
def auth_client(user):
    client = APIClient()

    response = client.post("/api/users/login/", {"username": "test", "password": "1234"})

    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client


@pytest.fixture
def habit(user):
    from habits.models import Habit

    return Habit.objects.create(user=user, place="home", time="12:00", action="drink water", execution_time=60)
