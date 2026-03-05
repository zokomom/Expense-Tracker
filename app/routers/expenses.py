from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import ExpenseOut, ExpenseIn
from ..database import get_db
from typing import List, Optional
from ..oauth2 import get_access_token
from ..models import Expense
from datetime import datetime, timedelta, timezone
from fastapi import Query

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.get("", response_model=List[ExpenseOut])
def get_expenses(db: Session = Depends(get_db),
                 get_user: int = Depends(get_access_token),
                 filter: Optional[str] = Query(
                     None, enum=["past_week", "past_month", "last_3_months", "custom"]),
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 search: Optional[str] = None):

    now = datetime.now(timezone.utc)
    expenses_query = db.query(Expense).filter(
        get_user.user_id == Expense.user_id)
    if filter == "past_week":
        expenses_query = expenses_query.filter(
            Expense.created_at >= (now-timedelta(weeks=1)))
    elif filter == "past_month":
        expenses_query = expenses_query.filter(
            Expense.created_at >= (now-timedelta(days=30)))
    elif filter == "last_3_months":
        expenses_query = expenses_query.filter(
            Expense.created_at >= (now-timedelta(days=90)))
    elif filter == "custom":
        try:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            end = datetime.strptime(end_date, "%d-%m-%Y")
            expenses_query = expenses_query.filter(
                Expense.created_at >= start, Expense.created_at <= end)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid date format. Use dd-mm-yyyy or dd-mm-yy")
    if search:
        expenses_query = expenses_query.filter(
            Expense.category == search.strip().capitalize())
    return expenses_query.all()


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist.")

    db.delete(delete_expense_query)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_expense(id: int, expense: ExpenseIn, db: Session = Depends(get_db), get_user: int = Depends(get_access_token)):
    update_expense_query = db.query(Expense).filter(id == Expense.id)
    update_expense_data = update_expense_query.first()
    if not update_expense_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist.")
    if not get_user.user_id == update_expense_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist.")
    update_expense_query.update(
        expense.model_dump(), synchronize_session=False)
    db.commit()
    return update_expense_query.first()
