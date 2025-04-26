from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Budget(BaseModel):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="budgets")

    expenses = relationship("Expense", back_populates="budget", cascade="all, delete-orphan")


