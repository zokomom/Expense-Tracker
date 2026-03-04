from pydantic import BaseModel, field_validator
import re


class UserOut(BaseModel):
    user_id: int
    email: str


class UserIn(BaseModel):
    email: str
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


class TokenData:
    id: int


class TokenOut(BaseModel):
    access_token: str
    token_type: str
