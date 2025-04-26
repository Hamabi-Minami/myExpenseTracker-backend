from pydantic import BaseModel

class BudgetCreate(BaseModel):
    amount: float
    year: int
    month: int

class BudgetOut(BaseModel):
    id: int
    amount: float
    year: int
    month: int

    class Config:
        orm_mode = True

class BudgetWithStats(BaseModel):
    id: int
    amount: int
    year: int
    month: int
    total_spent: float
    remaining: float

    class Config:
        orm_mode = True
