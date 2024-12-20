from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={ "username": user.email, "password": user.clean_password }
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_get_token_email_not_exists(client, user):
    response = client.post(
        "/auth/token",
        data={ "username": "test@test", "password": user.password }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == { "detail": "Email not exists" }


def test_get_token_password_incorret(client, user):
    response = client.post(
        "/auth/token",
        data={ "username": user.email, "password": "incorrect"}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == { "detail": "Password incorrect" }
