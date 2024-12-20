from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import Token
from app.security import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email not exists")
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Password incorrect")
    
    access_token = create_access_token(data={ "sub": user.email })

    return { "access_token": access_token, "token_type": "bearer" }
