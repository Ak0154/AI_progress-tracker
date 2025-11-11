from beanie import Document
from pydantic import BaseModel
from typing import Optional
import datetime

class ProgressEntry(Document):
    
    owner_id: str  
    date: datetime.date
    subject: str
    time_spent_minutes: int
    marks: Optional[float] = None
    notes: Optional[str] = None

    class Settings:
        name = "progress_entries" 

class AISummary(Document):
    owner_id: str
    generated_at: datetime.datetime = datetime.datetime.now()
    summary_text: str
    suggestions: list[str]
    
    class Settings:
        name = "ai_summaries"
        