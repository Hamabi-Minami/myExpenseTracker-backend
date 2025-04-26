from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import schemas
from app.models import Budget
from app.schemas.expense import ExpenseCreate, ExpenseOut

from app.core.dependencies import get_db, get_current_user
from app.models.expense import Expense
from app.models.user import User

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)

@router.post("/", response_model=ExpenseOut)
def create_expense(
    expense_in: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = db.query(Budget).filter(
        Budget.id == expense_in.budget_id,
        Budget.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found.")

    expense = Expense(
        description=expense_in.description,
        amount=expense_in.amount,
        budget_id=expense_in.budget_id,
        user_id=current_user.id
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


from sqlalchemy.orm import joinedload


@router.get("/", response_model=list[schemas.expense.ExpenseOut])
def get_user_expenses(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    expenses = db.query(Expense) \
        .options(joinedload(Expense.budget)) \
        .filter(Expense.user_id == current_user.id) \
        .order_by(Expense.created_at.desc()) \
        .all()

    return expenses


@router.delete("/{expense_id}", status_code=200)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Deleted successfully"}


class ExpenseUpdate(BaseModel):
    description: str
    amount: float

@router.patch("/{expense_id}")
def update_expense(
    expense_id: int,
    body: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.description = body.description
    expense.amount = body.amount

    db.commit()
    db.refresh(expense)

    return {"message": "Expense updated successfully"}