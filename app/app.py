from http import HTTPStatus
from fastapi import FastAPI, HTTPException

from app.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Exemplo de documentação do Python
    """
    return {"message": "Olá Mundo Novo!"}


@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database)+1)

    database.append(user_with_id)

    return user_with_id


@app.get("/users", response_model=UserList)
def read_users():
    return {"users": database}


@app.put("/users/{id}", response_model=UserPublic)
def update_user(id: int, user: UserSchema):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    user_with_id = UserDB(**user.model_dump(), id=id)
    database[id-1] = user_with_id

    return user_with_id


@app.delete("/users/{id}", response_model=Message)
def delete_user(id: int):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    del database[id-1]

    return { "message": "User deleted" }
