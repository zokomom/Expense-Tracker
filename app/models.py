from .database import Base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String


class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
