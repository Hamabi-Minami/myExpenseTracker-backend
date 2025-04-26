from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schemas
from app.core.dependencies import get_db, get_current_user
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.user import User
from app.schemas.budget import BudgetOut, BudgetCreate

router = APIRouter(
    prefix="/budget",
    tags=["budget"]
)

@router.post("/", response_model=BudgetOut)
def create_budget(
    budget_in: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budget = Budget(
        amount=budget_in.amount,
        year=budget_in.year,
        month=budget_in.month,
        user_id=current_user.id
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

@router.get("/", response_model=List[schemas.budget.BudgetWithStats])
def get_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()

    result = []
    for b in budgets:
        total_spent = sum(e.amount for e in b.expenses)
        result.append({
            "id": b.id,
            "amount": b.amount,
            "year": b.year,
            "month": b.month,
            "total_spent": total_spent,
            "remaining": b.amount - total_spent,
        })
    return result

