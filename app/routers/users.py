from fastapi import APIRouter, Depends
from fastapi import status
from ..schemas import UserOut, UserIn
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import hash_password
from ..models import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Entered email already exists.")
    return new_user
