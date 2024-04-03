from pydantic import BaseModel, ConfigDict
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    email: str
    model_config =ConfigDict(from_attributes = True)