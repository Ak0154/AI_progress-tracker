
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.user import User
from backend.models.progress import ProgressEntry
from backend.models.ai_summary import AISummary 

async def init_db():
    connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
    
    if not connection_string:
        raise Exception("MONGODB_CONNECTION_STRING is not set in .env file")

    client = AsyncIOMotorClient(connection_string)
    
    
    database = client["aiProgressTrackerDB"]

    print(f"Connecting to database: {database.name}")


    await init_beanie(
        database=database,
        document_models=[
            User,
            ProgressEntry,
            AISummary
        ]
    )
    print("Beanie initialization complete.")