from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.security import pwd_context
from app.models.user import User
from app.schemas.user import PasswordUpdate

router = APIRouter()

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    # get current user

    return {user}

# @router.get("/")
# def get_users(db: Session=Depends(get_db)):
#     #  get all users
#     return {'': ''}


@router.put("/password")
def change_password(
    body: PasswordUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not pwd_context.verify(body.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.hashed_password = pwd_context.hash(body.new_password)
    db.commit()

    return {"message": "Password updated successfully"}