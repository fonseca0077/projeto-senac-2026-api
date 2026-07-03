from http import HTTPStatus

from viajei_api.schemas.user import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Bem vindo!"}


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "email": "alice@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "email": "alice@example.com",
        "id": 1,
    }


def test_read_user(client):

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}

    def test_read_user_with_users(client, user):
        user_schema = UserPublic.model_validate(user).model_dump()
        response = client.get("/users")

        assert response.json() == {"users": [user_schema]}


def test_delete_user(client):

    response = client.delete("/users/1")

    response.status_code == HTTPStatus.OK
    response.json() == {"message": "User deleted!"}


def test_delete_user_not_found(client):

    response = client.delete("/users2/")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "user not found"}


def test_user_exercicio(client):

    response = client.get("/users2/")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "user not found"}


def test_get_token(client, user):

    response = client.post(
        "/auth",
        data={"username": user.email, "password": user.clean_passwd},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "token_type" in token
    assert "access_token" in token
