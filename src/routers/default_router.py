from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix='', tags=['default'])


@router.get('/')
async def get():
    return RedirectResponse("/docs")
