"""This file contains functions to test category's methods of the Django"""
import pytest

# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_get_category_list_not_authorized(client) -> None:
    """This function serves to test get category's list method if user isn't
    authorized
    :param client: a test client
    """
    response = client.get("/goals/goal_category/list")

    assert response.status_code == 403
    assert response.json() == {"detail": "Учетные данные не были предоставлены."}


def test_create_category(client, create_category) -> None:
    """This functions tests a create category method
    :param client: a test client
    :param create_category: a fixture created new category and provided
    response with result of the operation
    """
    response = create_category

    created = response.json()
    assert response.status_code == 201
    assert created == {
        "title": "Test_Category",
        "id": created.get("id"),
        "is_deleted": False,
        "created": created.get("created"),
        "updated": created.get("updated"),
        "board": created.get("board"),
    }


def test_get_category_list(client, create_category) -> None:
    """This functions tests a get category list method
    :param client: a test client
    :param create_category: a fixture created new category and provided
    response with result of the operation
    """
    response = client.get("/goals/goal_category/list")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert type(response.json()) is list


def test_get_single_category(client, create_category) -> None:
    """This functions tests a retrieve category method
    :param client: a test client
    :param create_category: a fixture created new category and provided
    response with result of the operation
    """
    category_data = create_category.data
    pk = category_data.get("id")
    response = client.get(f"/goals/goal_category/{pk}")

    received = response.json()
    received.pop("user")
    assert response.status_code == 200
    assert type(received) is dict
    assert received == category_data


def test_delete_category(client, create_category) -> None:
    """This functions tests a delete category method
    :param client: a test client
    :param create_category: a fixture created new category and provided
    response with result of the operation
    """
    category_data = create_category.data
    pk = category_data.get("id")

    response = client.delete(f"/goals/goal_category/{pk}")

    assert response.status_code == 204

    new_response = client.get(f"/goals/goal_category/{pk}")

    assert new_response.status_code == 404
