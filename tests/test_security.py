from jwt import decode

from viajei_api.security import CHAVE_SECRETA, create_access_token


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, CHAVE_SECRETA, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert "exp" in decoded
