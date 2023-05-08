"""This file contains functions to test board's methods of the Django"""
import pytest

# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_get_list_not_authorized(client) -> None:
    """This function serves to test get board's list method if user isn't
    authorized
    :param client: a test client
    """
    response = client.get("/goals/board/list")

    assert response.status_code == 403
    assert response.json() == {"detail": "Учетные данные не были предоставлены."}


@pytest.mark.django_db
def test_create_board(client, create_board) -> None:
    """This functions tests a create board method
    :param client: a test client
    :param create_board: a fixture created new board and provided response
    with result of the operation
    """
    response = create_board

    created = response.json()
    assert response.status_code == 201
    assert created == {
        "title": "Test_Board",
        "id": created.get("id"),
        "is_deleted": False,
        "created": created.get("created"),
        "updated": created.get("updated"),
    }


@pytest.mark.django_db
def test_get_board_list(client, create_board) -> None:
    """This functions tests a get board list method
    :param client: a test client
    :param create_board: a fixture created new board and provided response
    with result of the operation
    """
    response = client.get("/goals/board/list")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert type(response.json()) is list


@pytest.mark.django_db
def test_get_single_board(client, create_board) -> None:
    """This functions tests a retrieve board method
    :param client: a test client
    :param create_board: a fixture created new board and provided response
    with result of the operation
    """
    board_data = create_board.data
    pk = board_data.get("id")
    response = client.get(f"/goals/board/{pk}")

    received = response.json()
    received.pop("participants")
    assert response.status_code == 200
    assert type(received) is dict
    assert received == board_data


@pytest.mark.django_db
def test_update_board(client, create_board, get_authorized_user) -> None:
    """This functions tests an update board method
    :param client: a test client
    :param create_board: a fixture created new board and provided response
    with result of the operation
    :param get_authorized_user: a fixture that returns a user model
    """
    board_data = create_board.data
    pk = board_data.get("id")
    board_data["title"] = "Updated Board"
    board_data["participants"] = [
        {
            "user": get_authorized_user.username,
            "role": 2,
            "board": pk,
        }
    ]
    response = client.put(
        f"/goals/board/{pk}", data=board_data, content_type="application/json"
    )

    received = response.json()
    board_data["participants"][0].update(
        {
            "created": received["participants"][0]["created"],
            "updated": received["participants"][0]["updated"],
            "id": received["participants"][0]["id"],
            "role": 1,
        }
    )

    assert response.status_code == 200
    assert type(received) is dict
    assert received == board_data


def test_delete_board(client, create_board) -> None:
    """This functions tests a delete board method
    :param client: a test client
    :param create_board: a fixture created new board and provided response
    with result of the operation
    """
    board_data = create_board.data
    pk = board_data.get("id")

    response = client.delete(f"/goals/board/{pk}")
    assert response.status_code == 204

    new_response = client.get(f"/goals/board/{pk}")
    assert new_response.status_code == 404
