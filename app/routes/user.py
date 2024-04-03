from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user import UserCreate,UserResponse, User
from ..core.database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..crud import user as userCRUD
from ..utils import auth
from typing import Annotated

userRoute = APIRouter(prefix="/user",tags=["user"])

@userRoute.post("",response_model=User, status_code=201)
async def create_user(user: UserCreate,db:Session = Depends(get_db)):
    if userCRUD.read_user_by_email(db, user.email) is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = auth.get_password_hash(user.password)
    userDb = userCRUD.create_user(db, user)
    return userDb

@userRoute.get("",response_model=List[UserResponse])
async def read_users(db:Session = Depends(get_db)):
    users = userCRUD.read_users(db)
    return users

@userRoute.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(userCRUD.get_current_user)]
):
    return current_user

@userRoute.get("/{username}",response_model=UserResponse, status_code=200)
async def read_user(username: str,db:Session = Depends(get_db)):
    user = userCRUD.read_user_by_email(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@userRoute.delete("/{username}",response_model=UserResponse, status_code=200)
async def delete_user(username: str,db : Annotated[Session, Depends(get_db)],current_user: Annotated[User, Depends(userCRUD.get_current_active_user)]):
    if current_user.admin or current_user.email == username:
        if current_user.email != username:
            user = userCRUD.read_user_by_email(db, username)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
        user = userCRUD.delete_user(db, current_user)
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


    