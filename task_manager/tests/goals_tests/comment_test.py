"""This file contains functions to test comment's methods of the Django"""
import pytest

# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_get_comment_list_not_authorized(client) -> None:
    """This function serves to test get comment's list method if user isn't
    authorized
    :param client: a test client
    """
    response = client.get("/goals/goal_comment/list")

    assert response.status_code == 403
    assert response.json() == {"detail": "Учетные данные не были предоставлены."}


def test_create_comment(client, create_comment) -> None:
    """This functions tests a create comment method
    :param client: a test client
    :param create_comment: a fixture created new comment and provided
    response with result of the operation
    """
    response = create_comment

    created = response.json()
    assert response.status_code == 201
    assert created == {
        "id": created.get("id"),
        "text": "Test_text",
        "created": created.get("created"),
        "updated": created.get("updated"),
        "goal": created.get("goal"),
    }


def test_get_comment_list(client, create_comment) -> None:
    """This functions tests a get comment list method
    :param client: a test client
    :param create_comment: a fixture created new comment and provided
    response with result of the operation
    """
    goal = create_comment.data.get("goal")
    response = client.get(f"/goals/goal_comment/list?goal={goal}")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert type(response.json()) is list


def test_get_single_comment(client, create_comment) -> None:
    """This functions tests a retrieve comment method
    :param client: a test client
    :param create_comment: a fixture created new comment and provided
    response with result of the operation
    """
    comment_data = create_comment.data
    pk = comment_data.get("id")
    response = client.get(f"/goals/goal_comment/{pk}")

    received = response.json()
    received.pop("user")
    assert response.status_code == 200
    assert type(received) is dict
    assert received == comment_data


def test_delete_comment(client, create_comment) -> None:
    """This functions tests a delete comment method
    :param client: a test client
    :param create_comment: a fixture created new comment and provided
    response with result of the operation
    """
    comment_data = create_comment.data
    pk = comment_data.get("id")

    response = client.delete(f"/goals/goal_comment/{pk}")

    assert response.status_code == 204

    new_response = client.get(f"/goals/goal_comment/{pk}")

    assert new_response.status_code == 404
