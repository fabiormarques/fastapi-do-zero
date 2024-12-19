from http import HTTPStatus

from fastapi.testclient import TestClient

from app.app import app
from app.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/") # Act

    assert response.status_code == HTTPStatus.OK # Assert
    assert response.json() == {"message": "Olá Mundo Novo!"} # Assert


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_create_user_username_alreary_exists(client, user):
    response = client.post(
        "/users",
        json={
            "username": user.username, 
            "email": "alice@test.com", 
            "password": "testtest"
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == { "detail": "Username already exists" }


def test_create_user_email_alreary_exists(client, user):
    response = client.post(
        "/users",
        json={
            "username": "Alice", 
            "email": user.email, 
            "password": "testtest"
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == { "detail": "Email already exists" }


def test_read_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { "users": [] }


def test_read_user_only(client, user):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
            "username": "Teste",
            "email": "teste@test.com",
            "id": 1,
        }
    

def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.json() == { "users": [user_schema] }
    

def test_read_user_only_not_found(client, user):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == { "detail": "User not found" }


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_integrity_error(client, user):
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret"
        }
    )

    response_update = client.put(
        f"/users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        }
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == { "detail": "Username or Email already exists" }


def test_update_user_not_found(client):
    response = client.put(
        "/users/2",
        json={
            "username": "bill",
            "email": "bill@example.com",
            "password": "pass_bill",
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == { "detail": "User not found" }


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { "message": "User deleted" }


def test_delete_user_not_found(client):
    response = client.delete("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == { "detail": "User not found" }
