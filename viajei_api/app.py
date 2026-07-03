from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from viajei_api.database import get_session
from viajei_api.models import User
from viajei_api.schemas.message import Message
from viajei_api.schemas.user import UserList, UserPublic, UserSchema
from viajei_api.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)

app = FastAPI()

database = []


@app.get("/")
def read_root():
    return {"message": "Bem vindo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = session.scalar(select(User).where((User.email == user.email)))

    if db_user:
        raise HTTPException(HTTPStatus.CONFLICT, detail="Esse email já existe")

    hashed_password = get_password_hash(user.password)

    db_user = User(email=user.email, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found!"
        )

    session.delete(db_user)
    session.commit()

    return {"message": "User deleted!"}


@app.get("/users/{user_id}", response_model=UserPublic)
def user_exercicio(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found!"
        )
    return database[user_id - 1]


@app.post("/auth/")
def retrieve_token(
    dados_form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.email == dados_form.username)
    )

    if not user:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, detail="Esse email não existe"
        )

    if not verify_password(dados_form.password, user.password):
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, detail="Email ou senha incorretos"
        )

    token_acesso = create_access_token(dados={"sub": user.email})

    return {"access_token": token_acesso, "token_type": "bearer"}
