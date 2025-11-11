# models/user.py
from beanie import Document, Indexed
from pydantic import Field
from typing import Optional

class User(Document):

    username: Indexed(str, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    disabled: bool = False 

    class Settings:
        name = "users"