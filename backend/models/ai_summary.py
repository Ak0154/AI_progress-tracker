
from beanie import Document
from pydantic import Field
import datetime

class AISummary(Document):

    owner_id: str 
    
    
    generated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    summary_text: str
    suggestions: list[str]

    class Settings:
        name = "ai_summaries" 