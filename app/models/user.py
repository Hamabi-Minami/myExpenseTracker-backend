
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    account = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, default=2)

    role = relationship("Role", back_populates="users")
    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")

