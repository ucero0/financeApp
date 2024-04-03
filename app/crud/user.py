from sqlalchemy.orm import Session
from ..models import user as modelUser
from ..schemas.user import UserCreate,User, UserAdminCreate
from ..schemas.oauth import TokenData, Token
from ..utils import auth
from fastapi import HTTPException, status, Depends
from typing import Annotated
from ..core.database import get_db
from ..schemas.oauth import  oauth2_scheme
from ..utils import auth

def create_user(db:Session, user: UserCreate) -> modelUser.User:
    dbUser = modelUser.User(**user.model_dump())
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser
def create_adminUser(db:Session, user: UserAdminCreate) -> modelUser.User:
    dbUser = modelUser.User(**user.model_dump())
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)

def read_user_by_email(db:Session, email: str) -> modelUser.User:
    return db.query(modelUser.User).filter(modelUser.User.email == email).first()

def read_users(db:Session)->list[modelUser.User]:
    return db.query(modelUser.User).all()

def delete_user(db:Session, user: modelUser.User)->modelUser.User:
    db.delete(user)
    db.commit()
    return user

def get_current_user(token: Annotated[Token, Depends(oauth2_scheme)], db: Annotated[Session,Depends(get_db)] ) -> modelUser.User:
    payload = auth.verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    userDb = read_user_by_email(db, payload.email)
    return userDb

def get_current_active_user(
    current_user: Annotated[modelUser.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def isAdmin(current_user: Annotated[modelUser.User, Depends(get_current_user)]) -> bool:
    return current_user.admin
