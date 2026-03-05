from pydantic import BaseModel, field_validator,EmailStr
import re
from datetime import datetime


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime


class UserIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain at least one special character")
        return value


class TokenData(BaseModel):
    id: int


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str


class ExpenseIn(BaseModel):
    amount: float
    category: str

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value):
        return value.strip().capitalize()
