"""This file contains functions to test a bot app"""
import pytest

# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_bot_update_view(client, get_authorized_user) -> None:
    """This function serves to test a CBV of a bot app
    :param client: the test client
    :param get_authorized_user: a fixture providing an authorized user model
    """
    verification_data = {"verification_code": None}

    response = client.patch(
        "/bot/verify", data=verification_data, content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json() == {"verification_code": "incorrect"}
