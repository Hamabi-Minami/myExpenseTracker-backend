from pydantic import BaseModel, Field

class PasswordUpdate(BaseModel):
    old_password: str = Field(..., example="oldpassword123")
    new_password: str = Field(..., min_length=6, example="newpassword456")