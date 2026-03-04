from .database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, TIMESTAMP, DECIMAL
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
