import pytest

from habits.models import Habit


@pytest.mark.django_db
def test_create_habit(auth_client):
    response = auth_client.post(
        "/api/habits/", {"place": "home", "time": "12:00:00", "action": "read", "execution_time": 60}
    )

    assert response.status_code == 201
    assert Habit.objects.count() == 1


@pytest.mark.django_db
def test_get_habits(auth_client, habit):
    response = auth_client.get("/api/habits/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_get_single_habit(auth_client, habit):
    response = auth_client.get(f"/api/habits/{habit.id}/")

    assert response.status_code == 200
    assert response.data["action"] == habit.action


@pytest.mark.django_db
def test_update_habit(auth_client, habit):
    response = auth_client.patch(f"/api/habits/{habit.id}/", {"action": "new action"})

    assert response.status_code == 200
    habit.refresh_from_db()
    assert habit.action == "new action"


@pytest.mark.django_db
def test_delete_habit(auth_client, habit):
    response = auth_client.delete(f"/api/habits/{habit.id}/")

    assert response.status_code == 204
    assert Habit.objects.count() == 0


@pytest.mark.django_db
def test_cannot_access_other_user_habit(client, habit):
    response = client.get(f"/api/habits/{habit.id}/")

    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_other_user_cannot_edit(client, habit):

    response = client.post("/api/users/login/", {"username": "other", "password": "1234"})

    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.patch(f"/api/habits/{habit.id}/", {"action": "hack"})

    assert response.status_code == 403


@pytest.mark.django_db
def test_public_habits(client, habit):
    habit.is_public = True
    habit.save()

    response = client.get("/api/public/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_reward_and_related_error(auth_client, habit):
    response = auth_client.post(
        "/api/habits/",
        {
            "place": "home",
            "time": "12:00:00",
            "action": "test",
            "execution_time": 60,
            "reward": "coffee",
            "related_habit": habit.id,
        },
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_execution_time_limit(auth_client):
    response = auth_client.post(
        "/api/habits/", {"place": "home", "time": "12:00:00", "action": "test", "execution_time": 200}
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_periodicity_limit(auth_client):
    response = auth_client.post(
        "/api/habits/",
        {"place": "home", "time": "12:00:00", "action": "test", "execution_time": 60, "periodicity": 10},
    )

    assert response.status_code == 400
