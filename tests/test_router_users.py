from http import HTTPStatus

from app.schemas import UserPublic


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
    response = client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }
    

def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.json() == { "users": [user_schema] }
    

def test_read_user_only_not_found(client, user):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == { "detail": "User not found" }


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={ "Authorization": f"Bearer {token}" },
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
        "id": user.id,
    }


def test_update_integrity_error(client, user, token):
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
        headers={ "Authorization": f"Bearer {token}" },
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        }
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == { "detail": "Username or Email already exists" }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={ "Authorization": f"Bearer {token}" },
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        }
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == { "detail": "Not enough permissions" }


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={ "Authorization": f"Bearer {token}" }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { "message": "User deleted" }


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={ "Authorization": f"Bearer {token}" }
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == { "detail": "Not enough permissions" }
