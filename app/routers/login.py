from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import verify_password
from ..schemas import TokenOut
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..models import User
from .. import oauth2

router = APIRouter(
    prefix="/login",
    tags=["authentication"]
)


@router.post("", response_model=TokenOut, status_code=status.HTTP_200_OK)
def user_login(db: Session = Depends(get_db), user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(
        user_credentials.username == User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Invalid Credentials.")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials.")
    access_token = oauth2.create_access_token(data={'user_id': user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
