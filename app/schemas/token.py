from pydantic import BaseModel, EmailStr, validator
import re


class Token(BaseModel):
    access_token: str
    refresh_token: str
