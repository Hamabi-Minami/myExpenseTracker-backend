from fastapi import APIRouter
from app.api.v1 import user, auth, post, expenses, budget

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(post.router, prefix="/post", tags=["post"])
api_router.include_router(expenses.router, prefix="/expense", tags=["expenses"])
api_router.include_router(budget.router, prefix="/budget", tags=["budget"])