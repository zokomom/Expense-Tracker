from jose import jwt, JWTError
from .config import settings
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from .database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .models import User

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_access_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials.", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(User).filter(token.id == User.user_id).first()
    if not user:
        raise credential_exception
    return user
