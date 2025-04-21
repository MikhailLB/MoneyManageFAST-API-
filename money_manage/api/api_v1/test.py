from fastapi import APIRouter

router = APIRouter(prefix='/notes', tags=['notes'],)

@router.get('/notes')
async def get_notes():
    return {"Hello,": "World"}