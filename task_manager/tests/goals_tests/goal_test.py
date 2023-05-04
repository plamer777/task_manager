"""This file contains functions to test goal's methods of the Django"""
import pytest

# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_get_goal_list_not_authorized(client) -> None:
    """This function serves to test get goal's list method if user isn't
    authorized
    :param client: a test client
    """
    response = client.get("/goals/goal/list")

    assert response.status_code == 403
    assert response.json() == {"detail": "Учетные данные не были предоставлены."}


def test_create_goal(client, create_goal) -> None:
    """This functions tests a create goal method
    :param client: a test client
    :param create_goal: a fixture created new goal and provided
    response with result of the operation
    """
    response = create_goal

    created = response.json()
    assert response.status_code == 201
    assert created == {
        "title": "Test_Goal",
        "id": created.get("id"),
        "status": 1,
        "priority": 2,
        "description": None,
        "due_date": created.get("due_date"),
        "created": created.get("created"),
        "updated": created.get("updated"),
        "category": created.get("category"),
    }


def test_get_goal_list(client, create_goal) -> None:
    """This functions tests a get goal list method
    :param client: a test client
    :param create_goal: a fixture created new goal and provided
    response with result of the operation
    """
    response = client.get("/goals/goal/list")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert type(response.json()) is list


def test_get_single_goal(client, create_goal) -> None:
    """This functions tests a retrieve goal method
    :param client: a test client
    :param create_goal: a fixture created new goal and provided
    response with result of the operation
    """
    goal_data = create_goal.data
    pk = goal_data.get("id")
    response = client.get(f"/goals/goal/{pk}")

    received = response.json()
    received.pop("user")
    assert response.status_code == 200
    assert type(received) is dict
    assert received == goal_data


def test_delete_goal(client, create_goal) -> None:
    """This functions tests a delete goal method
    :param client: a test client
    :param create_goal: a fixture created new goal and provided
    response with result of the operation
    """
    goal_data = create_goal.data
    pk = goal_data.get("id")

    response = client.delete(f"/goals/goal/{pk}")

    assert response.status_code == 204

    new_response = client.get(f"/goals/goal/{pk}")

    assert new_response.status_code == 404
