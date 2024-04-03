from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    full_name: str | None = None
    class ConfigDict:
        from_attributes = True
class UserCreate(User):
    password: str

class UserAdminCreate(UserCreate):
    admin: bool = True

class UserResponse(User):
    created_at: datetime
    disabled: bool
    class ConfigDict:
        from_attributes = True

