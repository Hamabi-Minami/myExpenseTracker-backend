from pydantic import BaseModel

from app.schemas.budget import BudgetOut


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    budget_id: int

class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    budget: BudgetOut

    class Config:
        orm_mode = True

