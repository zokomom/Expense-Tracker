from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import ExpenseOut, ExpenseIn
from ..database import get_db
from typing import List
from ..oauth2 import get_access_token
from ..models import Expense

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.get("", response_model=List[ExpenseOut])
def get_expenses(db: Session = Depends(get_db), get_user: int = Depends(get_access_token)):
    expenses = db.query(Expense).filter(
        get_user.user_id == Expense.user_id).all()
    return expenses


@router.post("", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseIn, db: Session = Depends(get_db), get_user: int = Depends(get_access_token)):
    create_expense = Expense(user_id=get_user.user_id, **expense.model_dump())
    db.add(create_expense)
    db.commit()
    db.refresh(create_expense)
    return create_expense


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int, db: Session = Depends(get_db), get_user: int = Depends(get_access_token)):
    delete_expense_query = db.query(Expense).filter(
        id == Expense.id).first()

    if not delete_expense_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist.")

    if not get_user.user_id == delete_expense_query.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(delete_expense_query)
    db.commit()
