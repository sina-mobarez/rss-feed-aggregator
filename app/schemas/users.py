
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    is_active: bool

    class Config():
        orm_mode = True
