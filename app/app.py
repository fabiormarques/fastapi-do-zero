from http import HTTPStatus

from fastapi import FastAPI

from app.routers import auth, users
from app.schemas import Message


app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Exemplo de documentação do Python
    """
    return {"message": "Olá Mundo Novo!"}
