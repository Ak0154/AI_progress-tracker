from pydantic import BaseModel
from typing import Optional
import datetime

class ProgressCreate(BaseModel):
    date: datetime.date
    subject: str
    time_spent_minutes: int
    marks: Optional[float] = None
    notes: Optional[str] = None

class ProgressRead(ProgressCreate):
    id: str 

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AISummaryRead(BaseModel):
    id: str
    generated_at: datetime.datetime
    summary: str
    suggestions: list[str]