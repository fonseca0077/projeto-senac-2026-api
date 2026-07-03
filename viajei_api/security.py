from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

CHAVE_SECRETA = "your-very-secret-and-exclusive-key"
ALGORITIMO = "HS256"
TOKEN_ACESSO_MINUTOS_EXPIRAR = 30
contexto_senha = PasswordHash.recommended()


def create_access_token(dados: dict):
    para_codificar = dados.copy()

    expira = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=TOKEN_ACESSO_MINUTOS_EXPIRAR
    )

    para_codificar.update({"exp": expira})
    jwt_codificado = encode(
        para_codificar, CHAVE_SECRETA, algorithm=ALGORITIMO
    )

    return jwt_codificado


def get_password_hash(password: str):
    return contexto_senha.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return contexto_senha.verify(plain_password, hashed_password)
