from typing import Union
from pydantic import BaseModel



class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    username: Union[str, None] = None