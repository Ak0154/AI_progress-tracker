from fastapi import APIRouter, Depends
from ..models.progress import ProgressEntry
from ..models.ai_summary import AISummary
from ..models.user import User 
from ..schemas.schemas import ProgressCreate, ProgressRead, AISummaryRead 
from ..ai.gemini import get_ai_summary

from .auth import get_current_user 

router = APIRouter(
    tags=["Progress"]
)

@router.post("/", response_model=ProgressRead)
async def create_progress_entry(
    entry: ProgressCreate, 
    user: User = Depends(get_current_user)
):
    db_entry = ProgressEntry(
        **entry.model_dump(),
        owner_id=str(user.id) 
    )
    await db_entry.insert()

    return ProgressRead(id=str(db_entry.id), **entry.model_dump())

@router.get("/", response_model=list[ProgressRead])
async def get_all_progress(user: User = Depends(get_current_user)):

    entries = await ProgressEntry.find(ProgressEntry.owner_id == str(user.id)).to_list()
  
    response_entries = [
    ProgressRead(id=str(entry.id), **entry.model_dump(exclude={'id'})) for entry in entries
]
    return response_entries

@router.get("/summary", response_model=AISummaryRead) 
async def generate_summary(user: User = Depends(get_current_user)):

    entries = await ProgressEntry.find(ProgressEntry.owner_id == str(user.id)).to_list()

    ai_response = await get_ai_summary(entries)
   
    summary_doc = AISummary(
        owner_id=str(user.id), 
        summary_text=ai_response["summary"],
        suggestions=ai_response["suggestions"]
    )
    
    await summary_doc.insert()
   
    return AISummaryRead(
        id=str(summary_doc.id), 
        generated_at=summary_doc.generated_at,
        **ai_response
    )
@router.delete("/all")
async def delete_all_progress(user: User = Depends(get_current_user)):
 
    owner_id = str(user.id)
   
    await ProgressEntry.find(ProgressEntry.owner_id == owner_id).delete()

    await AISummary.find(AISummary.owner_id == owner_id).delete()
    
    return {"message": "All history deleted"}