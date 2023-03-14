
from pydantic import BaseModel, EmailStr, validator
import re


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str

    @validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+98|0)?9\d{9}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    @validator("password")
    def password_validation(cls, v):
        regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("password Invalid.")
        return v


class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    is_active: bool
    is_verified: bool

    class Config():
        orm_mode = True


class Message(BaseModel):
    message: str


class SendCodeOTP(BaseModel):
    upe: str


class VerifyCodeOTP(SendCodeOTP):
    code: str
