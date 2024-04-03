
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..utils import auth
from ..schemas.oauth import Token, TokenData
from ..crud import user as userCRUD
from typing import Annotated

authRouter = APIRouter( tags=["auth"])
@authRouter.post("/token", response_model=Token)
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session,Depends(get_db)]):
    
    userDb = userCRUD.read_user_by_email(db, user_credentials.username)
    if not userDb:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not auth.verify_password(user_credentials.password, userDb.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    tokenDAta = TokenData.model_validate(userDb)
    token = auth.create_access_token(tokenDAta.model_dump())
    return Token(access_token=token, token_type="bearer")
