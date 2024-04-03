from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from ..schemas.oauth import TokenData
from pydantic import ValidationError
from ..core.config import apiSettings

SECRET_KEY = apiSettings.secret_key
ALGORITHM = apiSettings.algorithm
ACESS_TOKEN_EXPIRE_MINUTES = apiSettings.access_token_expire_minutes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> dict:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str)->TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = TokenData.model_validate(payload)
        return payload
    except ValidationError:
        return None
    except JWTError:
        return None
    
