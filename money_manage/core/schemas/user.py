from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

class UserIn(UserBase):
    password: str

class UserForm(UserBase):
    username: str = Form()
    email: EmailStr = Form()
    password: str = Form()

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime