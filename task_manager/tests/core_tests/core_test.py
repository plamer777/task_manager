"""This file contains functions to test core app of the Django"""
import pytest

# -------------------------------------------------------------------------


@pytest.mark.django_db
def test_signup(client, get_user_data) -> None:
    """This functions serves to test registration of a new user
    :param client: a test client
    :param get_user_data: a fixture providing dictionary with user data
    """
    user_data = get_user_data

    response = client.post(
        "/core/signup", data=user_data, content_type="application/json"
    )

    result = response.json()
    result.pop("password")

    assert response.status_code == 201
    assert result == {
        "username": user_data.get("username"),
        "first_name": "",
        "last_name": "",
        "email": user_data.get("email"),
    }


def test_login(client, get_authorized_user, get_user_data) -> None:
    """This functions serves to test login method of a CBV
    :param client: a test client
    :param get_user_data: a fixture providing dictionary with user data
    :param get_authorized_user: a fixture providing a user model
    """
    user_data = {
        "username": get_user_data.get("username"),
        "password": get_user_data.get("password"),
    }

    response = client.post(
        "/core/login", data=user_data, content_type="application/json"
    )
    result = response.json()

    assert response.status_code == 201
    assert result["username"] == get_authorized_user.username


def test_get_profile(client, get_authorized_user) -> None:
    """This functions serves to test get profile method of a CBV
    :param client: a test client
    :param get_authorized_user: a fixture providing a user model
    """
    user_data = {
        "id": get_authorized_user.id,
        "username": get_authorized_user.username,
        "first_name": get_authorized_user.first_name,
        "last_name": get_authorized_user.last_name,
        "email": get_authorized_user.email,
    }

    response = client.get("/core/profile")
    result = response.json()

    assert response.status_code == 200
    assert result == user_data


def test_change_profile(client, updated_user_data) -> None:
    """This functions serves to test update profile method of a CBV
    :param client: a test client
    :param updated_user_data: a fixture providing a dictionary with user
    data to update
    """
    user_data = updated_user_data

    response = client.put(
        "/core/profile", data=user_data, content_type="application/json"
    )
    result = response.json()

    assert response.status_code == 200
    assert result == user_data


def test_delete_profile(client, get_authorized_user) -> None:
    """This functions serves to test delete profile method of a CBV
    :param client: a test client
    :param get_authorized_user: a fixture providing a user model
    """
    response = client.delete("/core/profile")
    assert response.status_code == 204

    new_response = client.get("/core/profile")
    assert new_response.status_code == 403


def test_update_password(client, get_authorized_user, get_user_data) -> None:
    """This functions serves to test update password method of a CBV
    :param client: a test client
    :param get_authorized_user: a fixture providing a user model
    :param get_user_data: a fixture providing dictionary with user data
    """
    passwords = {
        "old_password": get_user_data.get("password"),
        "new_password": "new_test_password",
    }

    response = client.put(
        "/core/update_password", data=passwords, content_type="application/json"
    )
    result = response.json()
    assert response.status_code == 200
    assert result.get("password") != get_authorized_user.password
