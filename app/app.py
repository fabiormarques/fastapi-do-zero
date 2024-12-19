from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import Message, UserList, UserPublic, UserSchema


app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Exemplo de documentação do Python
    """
    return {"message": "Olá Mundo Novo!"}


@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Username already exists")
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists")
        
    db_user = User(username=user.username, password=user.password, email=user.email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users", response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@app.put("/users/{id}", response_model=UserPublic)
def update_user(id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    try:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email

        session.commit()
        session.refresh(db_user)

        return db_user
    
    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Username or Email already exists")


@app.delete("/users/{id}", response_model=Message)
def delete_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    session.delete(db_user)
    session.commit()

    return { "message": "User deleted" }


@app.get("/users/{id}", response_model=UserPublic)
def read_user(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    return db_user
